from app import db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from app.auth import bp
from app.auth.forms import *
from app.auth.email import send_password_request_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
	# If we already have a logged in user in session, take client to index
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))	
	form = LoginForm()	# Otherwise, load login form

	# Next page after login
	next_page = request.args.get('next')
	if not next_page or url_parse(next_page).netloc != '':
		# The netloc != '' means that next_page is redirecting
		# to a different domain. We don't want that for security reasons
		next_page = url_for('main.index')

	# Validating user login
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# Invalid login
		if not (user and user.check_password(form.password.data)):
			flash("Invalid email or password")
			return redirect(next_page)
		# Valid login
		login_user(user, remember=form.remember_me.data)
		flash("User {} successfully logged in".format(user.first_name))
		
		return redirect(next_page)

	return render_template('auth/login.html', title='Sign in', form = form)



@bp.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('main.index'))



@bp.route('/register', methods=['GET', 'POST'])
def register():
	# If we already have a logged in user in session, take client to index
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))	
	form = RegistrationForm()	# Otherwise, load registration form

	# Validating user registration
	if form.validate_on_submit():
		# Add user to db
		first_name = form.first_name.data[0].upper() + form.first_name.data[1:]
		last_name = form.last_name.data[0].upper() + form.last_name.data[1:]
		user = User(email=form.email.data, first_name=first_name, last_name=last_name)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		# Succesfully added new user
		flash("Congratulations {}, profile successfully created".format(user.first_name))
		return redirect(url_for('auth.login'))
	
	return render_template('auth/register.html', title='Register', form = form)




@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	form = ResetPasswordRequestForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if not user:
			flash("This email does not have an account associated with it")
		else:
			send_password_request_email(user)
			flash("Password reset email has been sent to {}".format(form.email.data))
			return redirect(url_for('auth.login'))

	return render_template('auth/reset_password_request.html', form=form)



@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	user = User.verify_password_reset_token(token)
	if not user:
		return redirect(url_for('main.index'))

	form = ResetPasswordForm()

	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash("Your password has been reset")
		return redirect(url_for('auth.login'))

	return render_template('auth/reset_password.html', form=form)