from flask_mail import Message
from flask import current_app
from app import mail
from threading import Thread

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	app = current_app._get_current_object()
	Thread(target=send_async_email, args=(app, msg)).start()

# Sending email in a new thread because we don't
# need it to be syncronous and slow down the app
def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)
