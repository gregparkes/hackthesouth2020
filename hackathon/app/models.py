from app import db

class Dict(db.Model):
    labelname = db.Column(db.String(100), primary_key=True)
    displaylabelname = db.Column(db.String(100))
    

class Image(db.Model):
    imageid = db.Column(db.String(50), primary_key=True)
    subset=db.Column(db.String(50))
    originalurl=db.Column(db.String(100))
    originallandingurl = db.Column(db.String(100))
    originalsize = db.Column(db.String(50))
    originalmd5 = db.Column(db.String(100))
    thumbnail300kurl = db.Column(db.String(100))


class Label(db.Model):
    imageid= db.Column(db.String(50),db.ForeignKey('image.imageid'),primary_key=True,nullable=False)
    source = db.Column(db.String(50),primary_key=True,nullable=False)
    labelname=db.Column(db.String(100),db.ForeignKey('dict.labelname'),primary_key=True,nullable=False)
    confidence=db.Column(db.Float)
 