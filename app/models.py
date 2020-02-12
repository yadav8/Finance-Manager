from app import db, login
from datetime import datetime, timedelta, time
from time import time
import jwt
from flask import current_app, jsonify
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
	networth 	= db.Column(db.Numeric(scale=2), nullable=True, default=0)

	# User relationships
	accounts = db.relationship('Account', backref='owner', \
		cascade='all, delete-orphan', lazy='dynamic')
	transaction_history = db.relationship('Transaction', backref='owner', \
	 	cascade='all, delete-orphan', lazy='dynamic')
	categories = db.relationship('Category', backref='owner', \
	 	cascade='all, delete-orphan', lazy='dynamic')


	def __repr__(self):
		return '<User {} {} {}>'.format(self.user_id, self.first_name, self.last_name)


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
	account_networth = db.Column(db.Numeric(scale=2), nullable=True, default=0)
	date_added 		= db.Column(db.DateTime, default=datetime.utcnow)
	date_modified 	= db.Column(db.DateTime, default=datetime.utcnow)
	institution 	= db.Column(db.String(64), nullable=True, default=None)

	# Account relationships
	transaction_history = db.relationship('Transaction', backref='account', \
	 	cascade='all, delete-orphan', lazy='dynamic')
	

	def __repr__(self):
		if self.institution:
			return '<Account {} {}>'.format(self.institution, self.account_name)
		else:
			return '<Account {}>'.format(self.account_name)


class Transaction(db.Model):
	# Transaction fields
	transaction_id	= db.Column(db.Integer, primary_key=True)
	user_id			= db.Column(db.Integer, db.ForeignKey('user.user_id'))
	account_id		= db.Column(db.Integer, db.ForeignKey('account.account_id'))
	category_id 	= db.Column(db.Integer, db.ForeignKey('category.category_id'))
	transaction_name = db.Column(db.String(40))
	amount			= db.Column(db.Numeric(scale=2))
	timestamp		= db.Column(db.DateTime, default=datetime.utcnow)
	recurring		= db.Column(db.Boolean, default=False)
	recurring_delay = db.Column(db.Interval, nullable=True, default=None)
	recurring_enddate = db.Column(db.DateTime, nullable=True, default=None)
	note 			= db.Column(db.String(120), nullable=True, default=None)
	delete_allowed	= db.Column(db.Boolean, default=True)

	def __repr__(self):
		return '<Transaction {} {}>'.format(self.transaction_name, self.amount)

	@staticmethod
	def set_recurring_delay(how_often):
		if how_often == 'Weekly':
			return timedelta(weeks=1)
		elif how_often == 'Monthly':
			return timedelta(days=30)
		elif how_often == 'Yearly':
			return timedelta(days=365)

	@staticmethod
	def set_recurring_enddate(date):
		t = datetime.min.time()
		return datetime.combine(date, t)

class Category(db.Model):
	# Category fields
	category_id 		= db.Column(db.Integer, primary_key=True)
	user_id 			= db.Column(db.Integer, db.ForeignKey('user.user_id'))
	parent_category_id	= db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True, default=None)
	category_name 		= db.Column(db.String(40))
	user_deleted 		= db.Column(db.Boolean, default=False)

	# Account relationships
	transactions = db.relationship('Transaction', backref='category', lazy='dynamic')

	def __repr__(self):
		return '<Category {}>'.format(self.category_name)


	@staticmethod
	def load_initial_categories():
		category_list = ["Rent", "Restaurants", "Groceries", "Auto", "Miscellaneous", \
			"Loan", "Clothing", "Hobbies", "Sporting Goods", "Books", "Electronics", \
			"Charity", "Gift", "Medical", "Home Improvement", "Kids"]
		return category_list
