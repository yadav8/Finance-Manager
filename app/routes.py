from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
	# Mock data
	user = {'username': 'Sumit'}
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	# If we already have a logged in user in session, take client to index
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	# Otherwise, load login form
	form = LoginForm()

	# Next page after login
	next_page = request.args.get('next')
	if not next_page or url_parse(next_page).netloc != '':
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