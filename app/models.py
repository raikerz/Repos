# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#from app import db, login_manager, wa
from config import app_config

from app import *
enable_search = True

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    hire_date = db.Column(db.String(60), index=True)
    salary = db.Column(db.Integer, index=True)
    tel = db.Column(db.String(60), index=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_heng = db.Column(db.Boolean, default=False)
    is_acc = db.Column(db.Boolean, default=False)
    is_sat = db.Column(db.Boolean, default=False)
    is_eng = db.Column(db.Boolean, default=False)
    is_mos = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Equipment(db.Model):
    """
    Create a Equipment table
    """

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False)
    description = db.Column(db.String(200))
    serialnumber = db.Column(db.String(50), unique=False)
    modelnumber = db.Column(db.String(50), unique=False)
    location = db.Column(db.String(30))
    type = db.Column(db.String(30))
    status = db.Column(db.String(300))

    def __repr__(self):
        return '<Equipment: {}>'.format(self.name)

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Reports(db.Model):
    """
    Create a Reports table
    """

    __tablename__ = 'reports'
    __searchable__ = ['date', 'reference', 'company', 'service_provided']

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(30), unique=False)
    service_provided = db.Column(db.String(30), unique=False)
    location = db.Column(db.String(30), unique=False)
    space = db.Column(db.String(50), unique=False)
    time_gmt_s = db.Column(db.String(30), unique=False)
    time_gmt_e = db.Column(db.String(30), unique=False)
    extension = db.Column(db.String(30), unique=False)
    actual_s_time = db.Column(db.String(30), unique=False)
    actual_e_time = db.Column(db.String(30), unique=False)
    duration = db.Column(db.String(30), unique=False)
    engineer = db.Column(db.String(30), unique=False)
    reference = db.Column(db.String(40), unique=False)
    guest = db.Column(db.String(30), unique=False)
    transport_company = db.Column(db.String(30), unique=False)
    transport_kind = db.Column(db.String(50), unique=False)
    note = db.Column(db.String(400), unique=False)
    extrafees = db.Column(db.String(200), unique=False)
    date = db.Column(db.String(30), unique=False)
    type = db.Column(db.String(30), unique=False)

    def __repr__(self):
        return '<Reports: {}>'.format(self.name)


class Lives (db.Model):
    """
    Create a Lives table
    """
    __tablename__ = 'lives'
    __searchable__ = [ 'reference', 'company', 'service_provided']

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(30), unique=False)
    service_provided = db.Column(db.String(30), unique=False)
    sat = db.Column(db.String(50), unique=False)
    ul = db.Column(db.String(30), unique=False)
    dl = db.Column(db.String(30), unique=False)
    sr = db.Column(db.String(30), unique=False)
    fec = db.Column(db.String(30), unique=False)
    mod = db.Column(db.String(30), unique=False)
    access = db.Column(db.String(30), unique=False)
    reference = db.Column(db.String(40), unique=False)
    time_gmt_s = db.Column(db.String(30), unique=False)
    time_gmt_e = db.Column(db.String(30), unique=False)
    location = db.Column(db.String(30), unique=False)
    reg_code = db.Column(db.String(10), unique=False)
    date = db.Column(db.Date)
    note = db.Column(db.String(200), unique=False)
    actual_s_time = db.Column(db.String(30), unique=False)
    actual_e_time = db.Column(db.String(30), unique=False)
    flag = db.Column(db.Boolean)


    def __repr__(self):
        return '<Lives: {}>'.format(self.name)



class Freelancers (db.Model):
    """
    Create a Freelancers table
    """
    __tablename__ = 'freelancers'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(20), index=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    hire_rate = db.Column(db.String(10), index=True)
    tel = db.Column(db.String(30), index=True)

    def __repr__(self):
        return '<Freelancers: {}>'.format(self.first_name)


class Transports(db.Model):


    __tablename__ = 'transports'
    __searchable__ = ['date', 'reference', 'company']

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), unique=False)
    company = db.Column(db.String(20), unique=False)
    reference = db.Column(db.String(20), unique=False)
    guest_counter = db.Column(db.String(3), unique=False)
    guest1 = db.Column(db.String(30), unique=False)
    guest2 = db.Column(db.String(30), unique=False)
    guest3 = db.Column(db.String(30), unique=False)
    guest4 = db.Column(db.String(30), unique=False)
    guest5 = db.Column(db.String(30), unique=False)
    guest6 = db.Column(db.String(30), unique=False)
    guest7 = db.Column(db.String(30), unique=False)
    guest8 = db.Column(db.String(30), unique=False)
    guest9 = db.Column(db.String(30), unique=False)
    guest10 = db.Column(db.String(30), unique=False)
    city1 = db.Column(db.String(20), unique=False)
    city2 = db.Column(db.String(20), unique=False)
    city3 = db.Column(db.String(20), unique=False)
    city4 = db.Column(db.String(20), unique=False)
    city5 = db.Column(db.String(20), unique=False)
    city6 = db.Column(db.String(20), unique=False)
    city7 = db.Column(db.String(20), unique=False)
    city8 = db.Column(db.String(20), unique=False)
    city9 = db.Column(db.String(20), unique=False)
    city10 = db.Column(db.String(20), unique=False)
    note = db.Column(db.String(400), unique=False)

    def __repr__(self):
        return '<Transports: {}>'.format(self.name)


class Studios(db.Model):


    __tablename__ = 'studios'
    __searchable__ = ['date', 'reference', 'company','showname']

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), unique=False)
    company = db.Column(db.String(20), unique=False)
    showname = db.Column(db.String(20), unique=False)
    reference = db.Column(db.String(20), unique=False)
    time_gmt_s = db.Column(db.String(30), unique=False)
    time_gmt_e = db.Column(db.String(30), unique=False)
    guest_counter = db.Column(db.String(3), unique=False)
    guest1 = db.Column(db.String(30), unique=False)
    guest2 = db.Column(db.String(30), unique=False)
    guest3 = db.Column(db.String(30), unique=False)
    guest4 = db.Column(db.String(30), unique=False)
    guest5 = db.Column(db.String(30), unique=False)
    guest6 = db.Column(db.String(30), unique=False)
    guest7 = db.Column(db.String(30), unique=False)
    guest8 = db.Column(db.String(30), unique=False)
    guest9 = db.Column(db.String(30), unique=False)
    guest10 = db.Column(db.String(30), unique=False)
    note = db.Column(db.String(400), unique=False)

    def __repr__(self):
        return '<Studios: {}>'.format(self.name)

class Sngorders(db.Model):


    __tablename__ = 'sngorders'
    __searchable__ = ['date', 'reference', 'company']

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), unique=False)
    company = db.Column(db.String(20), unique=False)
    engineer = db.Column(db.String(30), unique=False)
    location = db.Column(db.String(30), unique=False)
    reference = db.Column(db.String(20), unique=False)
    time_gmt_s = db.Column(db.String(30), unique=False)
    time_gmt_e = db.Column(db.String(30), unique=False)
    cameraman = db.Column(db.String(50), unique=False)
    tech = db.Column(db.String(50), unique=False)
    driver = db.Column(db.String(50), unique=False)
    camera = db.Column(db.String(50), unique=False)
    car = db.Column(db.String(30), unique=False)
    note = db.Column(db.String(400), unique=False)

    def __repr__(self):
        return '<Sngorders: {}>'.format(self.name)


class Guests (db.Model):

    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(150), index=True)
    title = db.Column(db.String(50), index=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(20), index=True)
    tel = db.Column(db.String(30), index=True)
    address = db.Column(db.String(300), index=True)


    def __repr__(self):
        return '<Guests: {}>'.format(self.first_name)
