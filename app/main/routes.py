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
	user = {'username': 'Sumit'}
	transactions = [
		{
			'user': {'username': 'test1'},
			'amount': '$100'
		},
		{
			'user': {'username': 'test1'},
			'amount': '$200'
		}
	]
	return render_template('index.html', title='Home Page', transactions=transactions)



@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	if(username != current_user.username):
		flash("You don't have access to that page")
		return redirect(url_for('main.index'))
	user = User.query.filter_by(username=username).first_or_404()
	
	# Mock data for testing
	transactions = [
		{'user': user, 'amount': '$5'},
		{'user': user, 'amount': '$10'}
	]

	return render_template('user.html', user=user, transactions=transactions)


@bp.route('/delete_user')
@login_required
def delete_user():
	username = current_user.username
	db.session.delete(current_user)
	db.session.commit()
	flash("User {} successfully deleted".format(username))
	return redirect(url_for('auth.login'))


@bp.route('/add_account')
@login_required
def add_account():
	flash("Account add pressed")
	return redirect(url_for('main.user',username=current_user.username))
