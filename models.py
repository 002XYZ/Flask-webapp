from . import db # . means importing from the current package
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.String(10010))
    date=db.Column(db.DateTime(timezone=True),default=func.now()) # stores date and time of
                                        # the note written, by default becomes the current time
    user_id=db.Column(db.Integer,db.ForeignKey('user.id')) # references id in user table
                                                    # and makes a 1 user to many notes relationship

class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    first_Name=db.Column(db.String(140))
    notes=db.relationship('Note') # references to Note table,makes sure that a 
                        # specific user gets access to all notes that person created
