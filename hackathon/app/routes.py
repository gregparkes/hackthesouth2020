from flask import render_template, flash, redirect, url_for,request
from app import app
from app.models import Image
import csv 

def select(imageS, df1, df3):
    '''Selects the images for the next question.
    Based on the previously selected image (imageS)
    '''
    img = df1[df1['OriginalURL']==imageS]
    labels = img.iloc[0,6].split(";")
    images = []
    if len(labels) >= 4:
        for i in range(4):
            match = df3[df3['LabelName']==labels[i]]
            mtch = match[match['ImageID']==img.index[0]]
            tmp = df3[df3["LabelName"] == mtch.iloc[0]["LabelName"]]
            index = tmp["Confidence"].idxmax()
            imageid = df3.iloc[index]["ImageID"]
            image = df1[df1.index==imageid]["OriginalURL"][0]
            images.append(image)
    else:
        list1 = []
        for i in range(4):
            r = randint(0,len(df1))
            if r not in list1: 
                list1.append(r)
            image = df1.iloc[list[i], 1]
            images.append(image)
    return images[0],images[1],images[2],images[3]

@app.route('/')
@app.route('/index')
def index():
    
    image1= 'https://farm7.staticflickr.com/5769/21094803716_da3cea21b8_o.jpg'
    image2='https://c8.staticflickr.com/7/6007/6010263871_9d6dbce6ce_o.jpg'
    image3='https://farm1.staticflickr.com/2934/14439122755_d4af7552d1_o.jpg'
    image4='https://c2.staticflickr.com/9/8089/8416776003_9f2636ca56_o.jpg'
    
    return render_template('index.html', title='Home',image1=image1,image2=image2,image3=image3,image4=image4)


@app.route('/getdata',methods=['GET', 'POST'])
def ajax_receive():
    
    if request.method == "POST":
        x = request.form['url']
        text_file = open("C:/users/zuzan/desktop/sample.txt", "w")
        text_file.write(x)
        text_file.close()
        image5, image6, image7, image8 = select(x, df1, df3)
        
        
    return render_template('index.html')
