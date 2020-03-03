from app import db
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, \
	current_app, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp
from app.main.forms import *
from app.models import User, Account, Transaction, Category
import decimal

# Records last seen for a user, and resets their inactivity timer
@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		session.permanent = True
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@bp.route('/')
@bp.route('/index')
@login_required
def index():
	return redirect(url_for('main.profile'))


# Profile landing page
@bp.route('/profile')
@login_required
def profile():

	# Currently just showing accounts. Eventually want to show x number of
	# total latest transactions for the usuer
	accounts = current_user.accounts.all()

	# Recalculates total networth everytime profile loads
	current_user.networth = current_user.get_networth()
	db.session.commit()

	transactions = build_transaction_array(user=current_user)	

	return render_template('main/user.html', user=current_user, accounts=accounts, transactions=transactions)

# Builds a JSON array with all elements that the client would need to display transactions
def build_transaction_array(account=None, user=None):	
	transaction_array = []
	if user:
		for transaction in user.transaction_history.order_by(Transaction.timestamp.desc()).all():
			category = Category.query.get(transaction.category_id)
			account = Account.query.get(transaction.account_id)
			if account.institution:
				account_name = account.institution+' - '+account.account_name
			else:
				account_name = account.account_name
			transaction_array.append({'t': transaction, 'account_name': account_name, 'category_name': category.category_name})
		return transaction_array

	if account:		
		for transaction in account.transaction_history.order_by(Transaction.timestamp.desc()).all():
			category = Category.query.get(transaction.category_id)
			transaction_array.append({'t': transaction, 'category_name': category.category_name})
		return transaction_array

# Delete current user
@bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
	name = current_user.first_name + ' ' + current_user.last_name
	db.session.delete(current_user)
	db.session.commit()
	flash("User {} successfully deleted".format(name))
	return redirect(url_for('auth.login'))


# Add new account under current user
@bp.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
	form = AddAccountForm()

	if form.validate_on_submit():
		account_name_rejected = False
		for account in current_user.accounts.all():
			if account.account_name == form.account_name.data:
				flash("Account name already exists for this account")
				account_name_rejected = True
		if not account_name_rejected:
			new_account = Account(account_name=form.account_name.data, \
				user_id=current_user.user_id, institution=form.institution.data, \
				account_networth=form.account_networth.data)
			db.session.add(new_account)
			db.session.commit()
			flash("Account {} succesfully added to profile".format(new_account.account_name))
			return redirect(url_for('main.profile'))

	return render_template('main/add_account.html', form=form)


# Displays account overview
@bp.route('/account/<account_id>')
@login_required
def account(account_id):
	account = Account.query.get(account_id)
	transactions = account.transaction_history.order_by(Transaction.timestamp.desc()).all()
	transactions = build_transaction_array(account=account)
	return render_template('main/account.html', account=account, transactions=transactions)


# Delete account from user profile
@bp.route('/delete_account/<account_id>', methods=['GET', 'POST'])
@login_required
def delete_account(account_id):
	account = Account.query.get(account_id)
	db.session.delete(account)
	db.session.commit()
	return redirect(url_for('main.profile'))


# Add a transaction to a given amount
@bp.route('/add_transaction/<account_id>', methods=['GET', 'POST'])
@login_required
def add_transaction(account_id):
	account = Account.query.get(account_id)
	form = AddTransactionForm()
	form.category.choices = build_user_category_array(current_user)

	if form.validate_on_submit():
		if form.transaction_type.data=='Expense':
			amount = decimal.Decimal(0.00) - form.amount.data
		elif form.transaction_type.data=='Income':
			amount = form.amount.data

		tr = Transaction(transaction_name=form.transaction_name.data, \
			user_id=current_user.user_id, account_id=account_id, \
			amount=amount, note=form.note.data, category_id=int(form.category.data))
		if form.recurring.data=='True':
			tr.recurring = True
			tr.recurring_delay = Transaction.set_recurring_delay(form.how_often.data)
			tr.recurring_enddate = Transaction.set_recurring_enddate(form.enddate.data)
		
		account.account_networth += amount

		db.session.add(tr)
		db.session.commit()
		flash("{} succesfully added".format(tr))
		return redirect(url_for('main.account', account_id=account_id))


	return render_template('main/add_transaction.html', form=form, user_id=current_user.user_id)


def build_user_category_array(user):
	categories = user.categories.order_by(Category.category_name).all()
	choices = []
	for category in categories:
		choice = (category.category_id, category.category_name)
		choices.append(choice)
	return choices


#@bp.route('/add_transaction')


