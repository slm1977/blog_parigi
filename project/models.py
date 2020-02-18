from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Page(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    menu_title = db.Column(db.String(1000), unique=True)
    path = db.Column(db.String(1000), unique=True)
    index = db.Column(db.Integer)

    def __repr__(self):
        return "<Page: %s index:%s menu_title:%s filepath:%s>" % (self.id, self.index, self.menu_title, self.path)


