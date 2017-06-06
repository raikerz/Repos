# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask import abort, flash, redirect, render_template, url_for

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee

def check_admins():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@auth.route('/register', methods=['GET', 'POST'])
@login_required


def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """

    if current_user.is_admin == True or current_user.is_acc == True:

        form = RegistrationForm()
        if form.validate_on_submit():
            employee = Employee(
                                first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                hire_date=form.hire_date.data,
                                salary=form.salary.data,
                                tel=form.tel.data,
                               )

            # add employee to the database
            db.session.add(employee)
            db.session.commit()
            flash('You have successfully registered an Employee!')

            # redirect to the login page
            return redirect(url_for('its.list_employees'))

        # load registration template
        return render_template('auth/register.html', form=form, title='Register')
    else:
        abort(403)


#Edit Employee

@auth.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """
    Edit a employee
    """

    if current_user.is_admin == True or current_user.is_acc == True:

        employee = Employee.query.get_or_404(id)
        if employee.is_admin !=1 and employee.is_acc !=1 and employee.is_heng !=1 and employee.is_sat !=1 \
                and employee.is_eng !=1:
            form = RegistrationForm(obj=employee)
            if form.validate_on_submit():
                employee.first_name = form.first_name.data
                employee.last_name = form.last_name.data
                employee.hire_date = form.hire_date.data
                employee.salary = form.salary.data
                employee.tel = form.tel.data
                db.session.commit()
                flash('You have successfully edited the employee.')

                # redirect to the employee page
                return redirect(url_for('its.list_employees'))

            form.first_name.data = employee.first_name
            form.last_name.data = employee.last_name
            form.hire_date.data = employee.hire_date
            form.salary.data = employee.salary
            form.tel.data = employee.tel

            return render_template('auth/employee.html', action="Edit", form=form,
                                employee=employee, title="Edit Employee")
        else:
            abort(403)
    else:
        abort(403)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(username=form.username.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            if employee.is_admin==1 or employee.is_acc==1 or employee.is_heng==1 or employee.is_sat==1 or employee.is_eng==1 or employee.is_mos==1:
                # log employee in
                login_user(employee)
                # redirect to the appropriate dashboard page
                if employee.is_admin:
                    return redirect(url_for('home.admin_dashboard'))
                else:
                    return redirect(url_for('home.dashboard'))

            # when login details are incorrect
        else:
            flash('Invalid username or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))