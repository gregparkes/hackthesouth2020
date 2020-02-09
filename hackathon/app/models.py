from app import db
from random import randint


def select(imageS, df1, df3):
    '''Selects the images for the next question.
    Based on the previously selected image (imageS)
    '''
    #img = df1[df1['OriginalURL']==imageS]
    img =Image.query.filter_by(Originalurl=imageS).first()
    labels = img.LabelName.split(";")
    #labels = img.iloc[0,6].split(";")
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



class Dict(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    label = db.Column(db.String(100))
    names = db.Column(db.String(100))
    labels = db.relationship('Label', backref='dict', lazy='dynamic')
    
    

class Image(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    imageid = db.Column(db.String(50))
    Originalurl=db.Column(db.String(500))
    Thumbnail300kurl = db.Column(db.String(500))
    LabelName= db.Column(db.String(500))
    labels =db.relationship('Label', backref='image', lazy='dynamic')


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageid= db.Column(db.Integer,db.ForeignKey('image.id'),nullable=False)
    labelname=db.Column(db.String(100),db.ForeignKey('dict.id'),nullable=False)
    confidence=db.Column(db.Float)
