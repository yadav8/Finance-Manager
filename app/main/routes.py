from app import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
	current_app, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp
from app.main.forms import *
from app.models import User


@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
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



@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

	# Mock data for testing
	transactions = [
		{'user': current_user, 'amount': '$5'},
		{'user': current_user, 'amount': '$10'}
	]

	return render_template('user.html', user=current_user, transactions=transactions)


@bp.route('/delete_user')
@login_required
def delete_user():
	name = current_user.first_name + ' ' + current_user.last_name
	db.session.delete(current_user)
	db.session.commit()
	flash("User {} successfully deleted".format(name))
	return redirect(url_for('auth.login'))


@bp.route('/add_account')
@login_required
def add_account():
	form = AddAccountForm()

	if form.validate_on_submit():
		flash("yay")

	return redirect(url_for('main.profile'))
