from flask_login import UserMixin
from . import db
from flask import Flask
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    info=db.Column(db.String(1000))
    #billing_address_id = db.Column(db.Integer, db.ForeignKey("Fut.id"))
    #billing_address = relationship("Fut", foreign_keys="user.billing_address_id")
    fmember=db.relationship("Fut",backref="user")

class Fut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calinfo = db.Column(db.String(1000))
    fame = db.Column(db.String(1000))
    #ret=db.column(db.Integer, db.ForeignKey("user.id"))
    #owner_id = db.column(db.Integer,db.Foreignkey("user.id"))
    #name = db.Column(db.String(1000))
    #feet=db.Column(db.String(1000))
    #inches=db.Column(db.String(1000))
   # gender=db.Column(db.String(1000))
    #activelevel=gender=db.Column(db.String(1000))

