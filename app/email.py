from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	Thread(target=send_async_email, args=(app, msg)).start()

# Sending email in a new thread because we don't
# need it to be syncronous and slow down the app
def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_password_request_email(user):
	token = user.get_password_reset_token()

	subject = "Finance Manager - Password reset"
	sender = app.config['ADMINS'][0]
	recipients = [user.email]
	text_body = render_template('email/reset_password_email.txt', user=user, token=token)
	html_body = render_template('email/reset_password_email.html', user=user, token=token)

	send_email(subject, sender, recipients, text_body, html_body)