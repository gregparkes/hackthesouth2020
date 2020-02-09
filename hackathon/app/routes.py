from flask import render_template, flash, redirect, url_for,request,jsonify
from app import app
from app.models import Image,select
import pandas as pd
from random import randint
from app import word2vectorizer as w2v
#df1 = pd.read_csv("C:/Users/zuzan/desktop/images.csv")
#df2 = pd.read_csv("C:/Users/zuzan/desktop/dict.csv")
@app.route('/')
@app.route('/index')
def index():
    list_random = []
    for i in range(4):
        r = randint(0,167053)
        if r not in list_random: 
            list_random.append(r)
            
    image1= Image.query.get(list_random[0]).Thumbnail300kurl
    image2= Image.query.get(list_random[1]).Thumbnail300kurl
    image3=Image.query.get(list_random[2]).Thumbnail300kurl
    image4=Image.query.get(list_random[3]).Thumbnail300kurl

    
    return render_template('index.html', title='Home',image1=image1,image2=image2,image3=image3,image4=image4)


@app.route('/getdata',methods=['GET', 'POST'])
def ajax_receive():
    img, lbl = w2v.generate_image_label_pairing()
    df = w2v.generate_nlp()
    if request.method == "POST":
        tw = None
        image_url = request.form['url']
        c = request.form['c']
        subset = w2v.link_url_to_words(img, lbl, image_url)
        if int(c)>=3:
            tw = w2v.link_words_to_movies(list(subset), df)
        if subset:
            subset1 = w2v.link_url_to_words(img, lbl, image_url)
            for i in range(len(subset1)):
                subset.append(subset1[i])        
        list_random = []
        for i in range(4):
            r = randint(0,167053)
            if r not in list_random: 
                list_random.append(r)
            
        new_image1= Image.query.get(list_random[0]).Thumbnail300kurl
        new_image2= Image.query.get(list_random[1]).Thumbnail300kurl
        new_image3=Image.query.get(list_random[2]).Thumbnail300kurl
        new_image4=Image.query.get(list_random[3]).Thumbnail300kurl
        if tw:
            data=jsonify({'image1': new_image1, 'image2': new_image2,'image3': new_image3,'image4': new_image4,"tw":tw})
        else:
            data=jsonify({'image1': new_image1, 'image2': new_image2,'image3': new_image3,'image4': new_image4,"tw":None})
        return data

        
        
    return render_template('index.html')