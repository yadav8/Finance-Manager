from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, DeleteProfileForm
from app.models import User, Post

@app.route('/')
@app.route('/index')
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



@app.route('/login', methods=['GET', 'POST'])
def login():
	# If we already have a logged in user in session, take client to index
	if current_user.is_authenticated:
		return redirect(url_for('index'))	
	form = LoginForm()	# Otherwise, load login form

	# Next page after login
	next_page = request.args.get('next')
	if not next_page or url_parse(next_page).netloc != '':
		# The netloc != '' means that next_page is redirecting
		# to a different domain. We don't want that for security reasons
		next_page = url_for('index')

	# Validating user login
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		# Invalid login
		if not (user and user.check_password(form.password.data)):
			flash("Invalid username or password")
			return redirect(next_page)
		# Valid login
		login_user(user, remember=form.remember_me.data)
		flash("User {} successfully logged in".format(user.username))
		
		return redirect(next_page)

	return render_template('login.html', title='Sign in', form = form)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
	# If we already have a logged in user in session, take client to index
	if current_user.is_authenticated:
		return redirect(url_for('index'))	
	form = RegistrationForm()	# Otherwise, load registration form

	# Validating user registration
	if form.validate_on_submit():
		# Add user to db
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		# Succesfully added new user
		flash("Congratulations, user {} successfully created".format(user.username))
		return redirect(url_for('login'))
	
	return render_template('register.html', title='Register', form = form)



@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	if(username != current_user.username):
		flash("You don't have access to that page")
		return redirect(url_for('index'))
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
		return redirect(url_for('login'))


	return render_template('user.html', user=user, posts=posts, form=form)