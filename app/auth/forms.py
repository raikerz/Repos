# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,DateField,IntegerField,FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

from ..models import Employee

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    hire_date = StringField('Hired From',render_kw={"placeholder": "2016-09-26"}, validators=[Optional()])
    salary = IntegerField('Salary', validators=[Optional()])
    tel = StringField('Telephone No.')
    submit = SubmitField('Submit')



class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')