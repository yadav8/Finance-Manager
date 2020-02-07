from app import db, login
from datetime import datetime
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Creating a user_loader function for the flask_login extension
# to be able to load a user from our DB
@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(UserMixin, db.Model):
	# Users DB fields
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	# User DB relationships
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	# Converts plaintext password to hash
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	# Checks input plaintext password against hashed password
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)   


class Post(db.Model):
	# Posts DB fields
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)