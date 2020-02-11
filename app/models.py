from app import db, login
from datetime import datetime
from time import time
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Creating a user_loader function for the flask_login extension
# to be able to load a user from our DB
@login.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(UserMixin, db.Model):
	# Users fields
	user_id		= db.Column(db.Integer, primary_key=True)
	first_name 	= db.Column(db.String(32), index=True)
	last_name 	= db.Column(db.String(32), index=True)
	email 		= db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	last_seen 	= db.Column(db.DateTime, default=datetime.utcnow)
	networth 	= db.Column(db.Float(precision=2), nullable=True, default=0)

	# User relationships
	accounts = db.relationship('Account', backref='owner', \
		cascade='all, delete-orphan', lazy='dynamic')


	def __repr__(self):
		return '<User {} {}>'.format(self.first_name, self.last_name)


	def get_id(self):
		return self.user_id


	# Converts plaintext password to hash
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)


	# Checks input plaintext password against hashed password
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)   


	# Generates password reset token for given user which is valid for a given duration
	def get_password_reset_token(self, valid_duration=1800):
		exp_time = time() + valid_duration
		return jwt.encode(
			{
				'reset_password': self.user_id,
				'exp': exp_time
			}, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


	def get_networth(self):
		networth = 0
		for account in self.accounts.all():
			networth = networth + account.account_networth
		return networth


	@staticmethod
	def verify_password_reset_token(token):
		try:
			user_id = jwt.decode(token , current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except: return

		return User.query.get(user_id)



class Account(db.Model):
	# Account fields
	account_id		= db.Column(db.Integer, primary_key=True)
	user_id			= db.Column(db.Integer, db.ForeignKey('user.user_id'))
	account_name 	= db.Column(db.String(64))
	account_networth = db.Column(db.Float(precision=2), nullable=True, default=0)
	date_added 		= db.Column(db.DateTime, default=datetime.utcnow)
	date_modified 	= db.Column(db.DateTime, default=datetime.utcnow)
	institution 	= db.Column(db.String(64), nullable=True)


	def __repr__(self):
		return '<Account {}>'.format(self.account_name)