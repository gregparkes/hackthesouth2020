#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:03:32 2020

@author: Greg
"""
import os
import itertools as it
import gensim
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

def generate_nlp(filename='df__nlp.csv'):
    
    from nltk.tokenize import RegexpTokenizer
    # read file
    df = (pd.read_csv(filename, 
                        header=0, 
                        sep=',',
                        encoding='latin-1')
            .dropna(subset=['title', 'id', 'overview'])
            .drop('original_title', axis=1)
            .set_index('title'))
    
    df['overview'] = df['overview'].str.lower()
    df['tagline'] = df['tagline'].str.lower()
    
    df.loc[df['overview'].str.endswith('.'), 'overview'] = df.loc[df['overview'].str.endswith('.'), 'overview'].str[:-1]
    df.loc[df['tagline'].str.endswith('.'), 'tagline'] = df.loc[df['tagline'].str.endswith('.'), 'tagline'].str[:-1]
    
    # tokenize sentences        
    tokenizer = RegexpTokenizer(r'\w+')
    
    df['tokened'] = ((df['overview'] + df['tagline'])
        .apply(tokenizer.tokenize)
        .apply(lambda x: ' '.join(x)))
    
    return df
    
    

def generate_image_label_pairing(label_file='dict.csv', 
                                 image_file='image_to_label.csv'):
    """This function reads in our df files and prepares a library
    for use."""
    if not os.path.isfile(image_file):
        raise IOError('{} not found in file directory'.format(image_file))
    if not os.path.isfile(label_file):
        raise IOError('{} not found in file directory'.format(label_file))
    
    img = pd.read_csv(image_file)
    
    col_Names=["LabelNames", "Label"]
    lbl = pd.read_csv(label_file,names=col_Names)
    # return two dfs
    return img, lbl


def generate_w2v(in_filename='df__nlp.csv', out_filename='w2v.bin'):
    """Generates or reads the w2v."""
    
    if os.path.isfile(out_filename):
        # read in file
        X = gensim.models.KeyedVectors.load_word2vec_format(out_filename)
    
    else:
        
        from nltk.corpus import stopwords
        
        nltk.download('punkt')
        nltk.download('stopwords')
        stop = stopwords.words('english')
        
        df = generate_nlp(in_filename)

        # expand
        tokened_exp = df['tokened'].str.split(" ", expand=True)
        # use NLTK corpora to cleanse 
        w_filter = "^(?:" + "|".join(stop).replace("'", "\'") + '|\s)$'
        # filtering words
        repl = (tokened_exp.replace(w_filter, np.nan, regex=True)
                    .replace('', np.nan))
        list_lists = repl.apply(lambda x: x.str.cat(sep=';'), axis=1).str.split(';')
        
        # create word2vec model here and return
        X = gensim.models.Word2Vec(list_lists.tolist(), 
                                       min_count=2, size=100, workers=3,
                                       window=5, sg=1)
        # save
        X.wv.save_word2vec_format(out_filename)
        
    return X


def plot_pca(model):
    from sklearn.decomposition import PCA
    pca_t = PCA(2).fit_transform(model.wv[model.wv.vocab])
    # scatter
    plt.scatter(pca_t[:,0], pca_t[:,1], alpha=.3)
    plt.show()
    
    
def link_url_to_words(img_df, label_df, url):
    """Given one url, extract the labels associated with it."""
    
    #img_df has column 'OriginalURL'
    selection = img_df[img_df['Thumbnail300KURL']==url].squeeze()
    # if selection > 1,hmmm.
    if len(selection) == 0:
        raise ValueError('no images found to match url: {}'.format(url))
    elif not isinstance(selection, pd.Series):
        warnings.warn('more than one selection found with url: taking top.', UserWarning)
        selection = selection.iloc[0, :]
    
    label_ids = selection['LabelName'].split(';')
    # get labels
    labs = label_df.loc[label_df['LabelNames'].isin(label_ids), 'Label'].tolist()
    return labs
        
    
def link_words_to_movies(w, nlp_df):
    """Given list of words w, produce best movie?
    
    Returns 4 movies, top one is 'best' option.
    """
    """Take a list of words and get predicted close words from NLTK"""
    #model = open('w2v.bin', 'rb').read()
    model = gensim.models.KeyedVectors.load_word2vec_format('w2v.bin')
    assert isinstance(w, (list, tuple)), "w must be a list"
    res_l = list(it.chain.from_iterable([nltk.word_tokenize(word) for word in w]))
    skipped_res = [s for s in res_l if s in model.vocab]
    
    # get positive and negative contributors
    pos = set(np.random.choice(skipped_res, size=int(len(skipped_res)*.666667), replace=False))
    neg = set(skipped_res) - pos
    _w = model.most_similar(pos, neg, topn=100)
    _top_w = list(dict(_w[:10]).keys())
    #print(_w)
    # using top words, access nlp and fetch some movies
    top_movies = pd.concat(
        [nlp_df['tokened'].str.contains(word).astype(int) for word in _top_w]
    , axis=1, sort=False).sum(axis=1).nlargest(4).index
    return top_movies.tolist()


   











