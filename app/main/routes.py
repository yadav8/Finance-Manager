from app import db
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, \
	current_app, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp
from app.main.forms import *
from app.models import User, Account


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
	# Mock data for testing
	user = {'first_name': 'Sumit'}
	transactions = [
		{
			'user': {'first_name': 'test1'},
			'amount': '$100'
		},
		{
			'user': {'first_name': 'test1'},
			'amount': '$200'
		}
	]
	return render_template('index.html', title='Home Page', transactions=transactions)



@bp.route('/profile', methods=['GET'])
@login_required
def profile():

	# Mock data for testing
	accounts = current_user.accounts.all()

	return render_template('user.html', user=current_user, accounts=accounts)


@bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
	name = current_user.first_name + ' ' + current_user.last_name
	db.session.delete(current_user)
	db.session.commit()
	flash("User {} successfully deleted".format(name))
	return redirect(url_for('auth.login'))


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
				user_id=current_user.user_id, institution=form.institution.data)
			db.session.add(new_account)
			db.session.commit()
			flash("Account {} succesfully added to profile".format(new_account.account_name))
			return redirect(url_for('main.profile'))

	return render_template('add_account.html', form=form)
