from app import db
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, \
	current_app, jsonify, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp
from app.main.forms import *
from app.models import User, Account

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
	# Mock data for testing
	transactions = [
		{
			'user': {'first_name': current_user.first_name},
			'amount': '$100'
		},
		{
			'user': {'first_name': current_user.first_name},
			'amount': '$200'
		}
	]
	return render_template('index.html', title='Home Page', transactions=transactions)


# Profile landing page
@bp.route('/profile')
@login_required
def profile():

	# Currently just showing accounts. Eventually want to show x number of
	# total latest transactions for the usuer
	accounts = current_user.accounts.all()
	current_user.networth = current_user.get_networth()
	db.session.commit()
	
	flash(current_user.networth)

	return render_template('user.html', user=current_user, accounts=accounts)


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
				account_networth=form.account_networth)
			db.session.add(new_account)
			db.session.commit()
			flash("Account {} succesfully added to profile".format(new_account.account_name))
			return redirect(url_for('main.profile'))

	return render_template('add_account.html', form=form)



#@bp.route('/delete_account', methods=['GET', 'POST'])

@bp.route('/account/<account_id>')
@login_required
def account(account_id):
	account = Account.query.get(account_id)
	flash("{} clicked".format(account.account_name))
	return redirect(url_for('main.profile'))
