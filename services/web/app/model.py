from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy(app)


class Role(enum.Enum):
    admin = "admin"
    client = "client"
    coach = "coach"
    health_professional = "health_professional"

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    years = db.Column(db.Integer)
    birthday = db.Column(db.Date())
    weight = db.Column(db.Float)
    height = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    role = db.Column(db.Enum(Role), nullable=False)
    user_zone = relationship("UserZone")

class Zone(db.Model):
    __tablename__ = 'zone'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_zone = relationship("UserZone")

class UserZone(db.Model):
    __tablename__ = 'user_zone'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))