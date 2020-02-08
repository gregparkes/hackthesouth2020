from flask import render_template, flash, redirect, url_for,request
from app import app
from app.models import Image
import csv 

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
        
        
    return render_template('index.html')