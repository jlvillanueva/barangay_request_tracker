from mobile_sql_alchemy import mobile_db
from modules import functions


db = mobile_db

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_salt = db.Column(db.String(250), nullable=False)
    password_key = db.Column(db.String(250), nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    middleName = db.Column(db.String(20), nullable=True)
    lastName = db.Column(db.String(20), nullable=False)
    phoneNumber = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False)