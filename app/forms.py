from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import IncomeOutcome, RefundStatus


"""Create forms for login and registration"""

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = StringField('Password', validators=[DataRequired()])
	submit = StringField('Login')

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = StringField('Password', validators=[DataRequired()])
	confirm_pw = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = StringField('Register')

class AddTransaction(FlaskForm):
	amount = StringField('Amount', validators=[DataRequired()])
	category = StringField('Category', validators=[DataRequired()])
	datetime = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
	kind = SelectField('Kind', choices=[(x.name, x.value) for x in IncomeOutcome], validators=[DataRequired()])
	submit = StringField('Add new transaction')

class AddRefund(FlaskForm):
	datetime = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
	amount = StringField('Amount', validators=[DataRequired()])
	status = SelectField('Status', choices = [(x.name, x.value) for x in RefundStatus], validators=[DataRequired()])
	submit = StringField('Add new refund')

class CreateSavingJar(FlaskForm):
	id = StringField('Jar name', validators=[DataRequired()])
	goal = StringField('Goal', validators=[DataRequired()])
	submit = StringField('Create new saving jar')

