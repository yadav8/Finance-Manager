from app import db
from flask import render_template, flash, redirect, url_for, request, \
	current_app, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.main import bp
from app.main.forms import *
from app.models import User, Post

@bp.route('/')
@bp.route('/index')
@login_required
def index():
	# Mock data for testing
	user = {'username': 'Sumit'}
	posts = [
		{
			'author': {'username': 'test1'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'test1'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template('index.html', title='Home Page', posts=posts)



@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	if(username != current_user.username):
		flash("You don't have access to that page")
		return redirect(url_for('main.index'))
	user = User.query.filter_by(username=username).first_or_404()
	
	# Mock data for testing
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	
	form = DeleteProfileForm()

	# Validating user registration
	if form.validate_on_submit():
		username = current_user.username
		db.session.delete(current_user)
		db.session.commit()
		flash("User {} successfully deleted".format(username))
		return redirect(url_for('auth.login'))


	return render_template('user.html', user=user, posts=posts, form=form)