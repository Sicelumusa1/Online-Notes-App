from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import secrets

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    keywords = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    notes = db.relationship('Note')