from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Administrators(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(256), unique = True)
    Password = db.Column(db.String(256))

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    TName = db.Column(db.String(256), unique = True)
    School = db.Column(db.String(256))
    Score = db.Column(db.Integer)
    seedRank = db.Column(db.Integer)
    members = db.relationship('Competitors')

class Competitors(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    CName = db.Column(db.String(256))
    TID = db.Column(db.Integer, db.ForeignKey('teams.id'))

class Match(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    T1id = db.Column(db.Integer)
    T2id = db.Column(db.Integer)
    T1Name = db.Column(db.String(256))
    T2Name = db.Column(db.String(256))
    T1Score = db.Column(db.Integer)
    T2Score = db.Column(db.Integer)
    Ended = db.Column(db.Integer)
    Winner = db.Column(db.String(256))