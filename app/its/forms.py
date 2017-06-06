# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, RadioField, validators,DateField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department
from datetime import datetime

import time

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description',)
    submit = SubmitField('Submit')

class EquipmentForm(FlaskForm):
    """
    Form for admin to add or edit a equipment
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    serialnumber = StringField('Serial Number')
    modelnumber = StringField('Model Number')
    location = StringField('Location')
    status = StringField('Status')
    type = RadioField('Type', choices=[('Amplifier','Amplifier'),('Encoder','Encoder'),('Camera','Camera'),
                                       ('Receiver','Receiver'),('Other','Other')],validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')

class ReportsForm(FlaskForm):

    date = StringField('Date',render_kw={"placeholder": "2016-09-26"},validators=[validators.DataRequired()])
    company = StringField('Client')
    service_provided = StringField('Service Provided')
    location = StringField('Location')
    space = StringField('Space')
    time_gmt_s = StringField('S Time GMT')
    time_gmt_e = StringField('E Time GMT')
    extension = StringField('Extension')
    actual_s_time = StringField('Actual S Time')
    actual_e_time = StringField('Actual E Time')
    duration = StringField('Duration')
    engineer = StringField('Engineer')
    reference = StringField('Reference No.')
    guest = StringField('Guest')
    transport_company = StringField('Transport Company')
    transport_kind = StringField('Transport Kind')
    note = StringField('Note')
    extrafees = StringField('Extra Fees')
    type = RadioField('Type', choices=[('Office','Office'),('SNG','SNG'),('ENG','ENG')])
    submit = SubmitField('Submit')


class LivesForm(FlaskForm):

    date = DateField('Date',format="%Y-%m-%d", default=datetime.today,validators=[validators.DataRequired()])
    company = StringField('Client')
    service_provided = StringField('Service Provided')
    sat = StringField('Satellite info')
    ul = StringField('Uplink')
    dl = StringField('Downlink')
    sr = StringField('Symbol Rate')
    fec = StringField('FEC')
    mod = StringField('Modulation')
    access = StringField('Sat Access')
    reference = StringField('Reference')
    time_gmt_s = StringField('S Time GMT')
    time_gmt_e = StringField('E Time GMT')
    reg_code = StringField('Reg Code')
    location = RadioField('Type', choices=[('Maspero','Maspero'),('Agoza','Agoza'),('Street','Street')])
    submit = SubmitField('Submit')

class FreelancersForm(FlaskForm):

    job = RadioField('Job', choices=[('Camera Man','Camera Man'),('Sound Engineer','Sound Engineer'),('Assistant','Assistant'),('Other','Other')])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    hire_rate = StringField('Hiring Rate')
    tel = StringField('Telephone No.')
    submit = SubmitField('Submit')


class TransportsForm(FlaskForm):

    date = StringField('Date',render_kw={"placeholder": "2016-09-26"},validators=[validators.DataRequired()])
    company = StringField('Client')
    reference = StringField('Reference')
    guest_counter = SelectField(
        'Number of Guests',
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    guest1 = StringField('Guest1')
    city1 = StringField('City1')

    guest2 = StringField('Guest2')
    city2 = StringField('City2')

    guest3 = StringField('Guest3')
    city3 = StringField('City3')

    guest4 = StringField('Guest4')
    city4 = StringField('City4')

    guest5 = StringField('Guest5')
    city5 = StringField('City5')

    guest6 = StringField('Guest6')
    city6 = StringField('City6')

    guest7 = StringField('Guest7')
    city7 = StringField('City7')

    guest8 = StringField('Guest8')
    city8 = StringField('City8')

    guest9 = StringField('Guest9')
    city9 = StringField('City9')

    guest10 = StringField('Guest10')
    city10 = StringField('City10')

    note = StringField('Note')
    submit = SubmitField('Submit')

class StudiosForm(FlaskForm):
    showname = SelectField('Show Name', choices=[('Al Youm', 'Al Youm'), ('Best of Al Youm', 'Best of Al Youm'),
                                                ('Kalam Masry', 'Kalam Masry'),
                                                ('Dispute or Differences', 'Dispute or Differences'),
                                                ('Other', 'Other')])
    date = StringField('Date',render_kw={"placeholder": "2016-09-26"},validators=[validators.DataRequired()])
    company = StringField('Client')
    reference = StringField('Reference No.')
    time_gmt_s = StringField('S Time GMT')
    time_gmt_e = StringField('E Time GMT')
    guest_counter = SelectField(
        'Number of Guests',
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                 ('9', '9'), ('10', '10')])
    guest1 = StringField('Guest1')
    guest2 = StringField('Guest2')
    guest3 = StringField('Guest3')
    guest4 = StringField('Guest4')
    guest5 = StringField('Guest5')
    guest6 = StringField('Guest6')
    guest7 = StringField('Guest7')
    guest8 = StringField('Guest8')
    guest9 = StringField('Guest9')
    guest10 = StringField('Guest10')

    note = StringField('Note')
    submit = SubmitField('Submit')

class NotesForm(FlaskForm):
    """
    Form to add or edit a lives
    """

    note = StringField('Note')
    actual_s_time = StringField('Actual S')
    actual_e_time = StringField('Actual E')
    submit = SubmitField('Submit')


class SngordersForm(FlaskForm):

    date = StringField('Date',render_kw={"placeholder": "2016-09-26"},validators=[validators.DataRequired()])
    company = StringField('Client')
    engineer = StringField('Engineer')
    location = StringField('Location')
    reference = StringField('Reference No.')
    time_gmt_s = StringField('S Time GMT')
    time_gmt_e = StringField('E Time GMT')
    cameraman = StringField('Camera Man')
    tech = StringField('Technician')
    driver = StringField('Driver')
    camera = StringField('Camera')
    car = StringField('Car')
    note = StringField('Note')
    submit = SubmitField('Submit')


class GuestsForm(FlaskForm):

    job = StringField('Job')
    title = StringField('Title')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    tel = StringField('Telephone No.')
    address = StringField('Address')
    submit = SubmitField('Submit')
