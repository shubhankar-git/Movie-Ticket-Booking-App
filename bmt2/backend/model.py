import os
from flask import Flask
from flask_login import LoginManager, UserMixin

from datetime import datetime


from flask_security import  UserMixin, RoleMixin
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SECURITY_PASSWORD_SALT'] = 'your_salt_value_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
mm = Marshmallow(app)
jwt = JWTManager(app)

login_manager = LoginManager(app)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )
# Define the user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_booked = db.Column(db.DateTime)

    def __init__(self, username, email, password,last_booked):
        self.username = username
        self.email = email
        self.password = password
       
        self.last_booked=last_booked
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    place = db.Column(db.String(255))
    capacity = db.Column(db.Integer)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.Float)
    genres = db.Column(db.String(255))
    ticket_price = db.Column(db.Float)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
  

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    shows_backref = db.relationship('Show', backref='bookings')

    def __init__(self, user_id, show_id, num_tickets, total_price,shows):
        self.user_id = user_id
        self.show_id = show_id
        self.num_tickets = num_tickets
        self.total_price = total_price
        self.shows=shows


class CsvEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, theatre_id, filename, content):
        self.theatre_id = theatre_id
        self.filename = filename
        self.content = content