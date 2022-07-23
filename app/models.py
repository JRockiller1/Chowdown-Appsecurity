# *Important
from datetime import datetime
from app import db


class Customer(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(250), nullable=False)
    cmail = db.Column(db.String(250), unique=True, nullable=False)
    cmobile = db.Column(db.Integer, unique=True, nullable=False)
    caddress = db.Column(db.String(250), nullable=False)
    cpassword = db.Column(db.String, nullable=False)

class Restadmin(db.Model):
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rname = db.Column(db.String(250), nullable=False)
    rmail = db.Column(db.String(250), unique=True, nullable=False)
    rmobile = db.Column(db.Integer,unique=True, nullable=False)
    raddress = db.Column(db.String(250), nullable=False)
    rpassword = db.Column(db.String, nullable=False)


class Diginadmin(db.Model):
    amail = db.Column(db.String(250), primary_key=True) 
    apassword = db.Column(db.String(250), nullable=False)
    

class Items(db.Model):
    iid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iname = db.Column(db.String(250), nullable=True)
    iprice = db.Column(db.Integer, nullable=False)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    idesc = db.Column(db.String(250))
    priceid = db.Column(db.String(250),nullable=False)



class Orders(db.Model):
    ohash = db.Column(db.Integer,primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, db.ForeignKey('customer.cid'), nullable=False)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    items = db.Column(db.String(250), nullable=False)
    tprice=db.Column(db.Integer, nullable=False)
    payment = db.Column(db.String(20), nullable=False)
    month1 = db.Column(db.Integer, nullable=False)
    rname = db.Column(db.String(250),nullable=False)

class Rating(db.Model):
    key = db.Column(db.Integer,primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    rstar = db.Column(db.String(250), nullable=True)
    rreview = db.Column(db.String(250), nullable=True)
    date = db.Column(db.Text)
    cname = db.Column(db.Text)

# class Data(db.Model):
#     key2 = db.Column(db.Integer,primary_key=True, autoincrement=True)
#     rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
#     month = db.Column(db.Integer, nullable=False)
#     year = db.Column(db.Integer, nullable=True)

class Promotion(db.Model):
    key3 = db.Column(db.Integer,primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    promocode = db.Column(db.String(250))
    discount = db.Column(db.Integer, nullable =False)

class charity_vote(db.Model):
    charityid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    cid = db.Column(db.Integer, db.ForeignKey('customer.cid'), nullable=False)
    organisation = db.Column(db.Text, nullable=False)
    month = db.Column(db.Integer)
db.create_all()


