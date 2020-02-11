from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
	SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class DeleteProfileForm(FlaskForm):
	delete = SubmitField('Delete Profile')


class AddAccountRequestForm(FlaskForm):
	add_account = SubmitField('Add new account')


class AddAccountForm(FlaskForm):
	account_name = StringField('Account Name', validators=[DataRequired()])
	institution = StringField('Institution (Optional)')
	account_networth = DecimalField('Account Net Worth (USD)', places=2)
	submit = SubmitField('Add Account')