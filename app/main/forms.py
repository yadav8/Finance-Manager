from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import Form, StringField, PasswordField, BooleanField, DateField, \
	SubmitField, DecimalField, RadioField, SelectField, FieldList, FormField
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


class AddTransactionForm(FlaskForm):
	transaction_name = StringField('Transaction Name', validators=[DataRequired()])
	transaction_type = RadioField('Transaction Type', \
		choices=[('Income','Income'), ('Expense','Expense')], default='Expense')
	amount = DecimalField('Amount (USD)', places=2)
	recurring = RadioField('One-Time Transaction?', \
		choices=[('False','Yes'), ('True','No')], default='False')
	how_often = SelectField('Repeats', \
		choices=[('Weekly','Weekly'), ('Monthly','Monthly'), ('Yearly','Yearly')])
	enddate = DateField('Recurring End (YYYY-MM-DD)', default=datetime.utcnow)
	note = StringField('Notes (Optional)')
	submit = SubmitField('Submit Transaction')


