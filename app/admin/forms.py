# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, RadioField, validators,DateField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department
from datetime import datetime

import  time

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EquipmentForm(FlaskForm):
    """
    Form for admin to add or edit a equipment
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    serialnumber = StringField('Serial Number')
    location = StringField('Location')
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')

class ReportsForm(FlaskForm):
    """
    Form for admin to add or edit a reports
    """
    number = StringField('Number')
    company = StringField('Company')
    service_provided = StringField('Service Provided')
    location = StringField('Location')
    time_gmt_s = StringField('S Time GMT')
    time_gmt_e = StringField('E Time GMT')
    engineer = StringField('Engineer')
    reference = StringField('Reference No.')
    guest = StringField('Guest')
    transport_company = StringField('Transport Company')
    transport_kind = StringField('Transport Kind')
    note = StringField('Note')
    date = StringField('Date',render_kw={"placeholder": "2016-09-26"},validators=[validators.DataRequired()])
    type = RadioField('Type', choices=[('Office','Office'),('SNG','SNG'),('ENG','ENG')])
    submit = SubmitField('Submit')


class LivesForm(FlaskForm):
    """
    Form to add or edit a lives
    """

    company = StringField('Company')
    service_provided = StringField('Service Provided')
    sat = StringField('Satellite info')
    ul = StringField('Uplink')
    dl = StringField('Downlink')
    sr = StringField('Symbol Rate')
    fec = StringField('FEC')
    mod = StringField('Modulation')
    access = StringField('Sat Access')
    time_gmt_s = StringField('S Time GMT')
    time_gmt_e = StringField('E Time GMT')
    location = RadioField('Type', choices=[('Maspero','Maspero'),('Agoza','Agoza'),('Street','Street')])
    date = DateField('Date',format="%Y-%m-%d", default=datetime.today,validators=[validators.DataRequired()])
    submit = SubmitField('Submit')