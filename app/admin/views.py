from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from forms import DepartmentForm, EmployeeAssignForm,EquipmentForm,ReportsForm,LivesForm
from ..models import Department, Employee, Equipment, Reports, Lives
from . import admin
from .. import db
from datetime import datetime
import flask_excel as excel
import pyexcel.ext.xls, pyexcel.ext.xlsx



now = datetime.now().strftime("%Y-%m-%d")
def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

def check_heng():
    """
    prevent non-heng from accessing this page
    """
    if not current_user.is_heng:
        abort(403)

def check_acc():
    """
    prevent non-acc from accessing this page
    """
    if not current_user.is_acc:
        abort(403)


# Department Views



@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    if current_user.is_admin == True or current_user.is_acc == True:

        add_department = True

        form = DepartmentForm()
        if form.validate_on_submit():
            department = Department(name=form.name.data,
                                description=form.description.data)
            try:
                # add department to the database
                db.session.add(department)
                db.session.commit()
                flash('You have successfully added a new department.')
            except:
                # in case department name already exists
                flash('Error: department name already exists.')

            # redirect to departments page
            return redirect(url_for('its.list_departments'))

        # load department template
        return render_template('its/departments/department.html', action="Add",
                            add_department=add_department, form=form,
                            title="Add Department")
    else:
        abort(403)


#Edit Departments

@its.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    if current_user.is_admin == True or current_user.is_acc == True:

        add_department = False

        department = Department.query.get_or_404(id)
        form = DepartmentForm(obj=department)
        if form.validate_on_submit():
            department.name = form.name.data
            department.description = form.description.data
            db.session.commit()
            flash('You have successfully edited the department.')

            # redirect to the departments page
            return redirect(url_for('its.list_departments'))

        form.description.data = department.description
        form.name.data = department.name
        return render_template('its/departments/department.html', action="Edit",
                            add_department=add_department, form=form,
                            department=department, title="Edit Department")
    else:
        abort(403)

#Delete Department

@its.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    if current_user.is_admin == True or current_user.is_acc == True:

        department = Department.query.get_or_404(id)
        db.session.delete(department)
        db.session.commit()
        flash('You have successfully deleted the department.')

        # redirect to the departments page
        return redirect(url_for('its.list_departments'))

        return render_template(title="Delete Department")
    else:
        abort(403)

@its.route('/departments/sub/<int:id>', methods=['GET', 'POST'])
@login_required
def list_employees_dep(id):
    """
    List sub departments
    """

    employees = Employee.query.filter(Employee.department_id==id)
    return render_template('its/departments/sub.html',Department=Department,
                           employees=employees, title='Employees')

# Employee Views
@its.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    if current_user.is_admin == True or current_user.is_acc == True:

        employees = Employee.query.filter(Employee.first_name!=None)
        return render_template('its/employees/employees.html',
                            employees=employees, title='Employees')
    else:
        abort(403)


@its.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    if current_user.is_admin == True or current_user.is_acc == True:

        employee = Employee.query.get_or_404(id)

        # prevent admin from being assigned a department or role
        if employee.is_admin:
            abort(403)

        form = EmployeeAssignForm(obj=employee)
        if form.validate_on_submit():
            employee.department = form.department.data
            db.session.add(employee)
            db.session.commit()
            flash('You have successfully assigned a department .')

            # redirect to the roles page
            return redirect(url_for('its.list_employees'))

        return render_template('its/employees/employee.html',
                            employee=employee, form=form,
                            title='Assign Employee')
    else:
        abort(403)

@its.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete a employees from the database
    """
    if current_user.is_admin == True or current_user.is_acc == True:

        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        flash('You have successfully deleted the employee.')

        # redirect to the departments page
        return redirect(url_for('its.list_employees'))

        return render_template(title="Delete Employee")
    else:
        abort(403)
# Equipment Views

@its.route('/equipment', methods=['GET', 'POST'])
@login_required
def list_equipment():
    """
    List all equipment
    """
    #check_admin()

    equipment = Equipment.query.all()

    return render_template('its/equipment/equipments.html',
                           equipment=equipment, title="Equipment")
# Equipment Add

@its.route('/equipment/add', methods=['GET', 'POST'])
@login_required
def add_equipment():
    """
    Add a equipment to the database
    """
    if current_user.is_admin==True or current_user.is_heng==True:

        add_equipment = True

        form = EquipmentForm()
        if form.validate_on_submit():
            equipment = Equipment(name=form.name.data,description=form.description.data, serialnumber=form.serialnumber.data, location=form.location.data)

            try:
                # add equipment to the database
                db.session.add(equipment)
                db.session.commit()
                flash('You have successfully added a new equipment.')
            except:
                # in case equipment name already exists
                flash('Error: serialnumber name already exists.')

            # redirect to equipment page
            return redirect(url_for('its.list_equipment'))

        # load equipment template
        return render_template('its/equipment/equipment.html', action="Add",
                            add_equipment=add_equipment, form=form,
                            title="Add Equipment")
    else:
        abort(403)


# Equipment Edit

@its.route('/equipment/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_equipment(id):
    """
    Edit a equipment
    """
    if current_user.is_admin == True or current_user.is_heng == True:

        add_equipment = False

        equipment = Equipment.query.get_or_404(id)
        form = EquipmentForm(obj=equipment)
        if form.validate_on_submit():
            equipment.name = form.name.data
            equipment.description = form.description.data
            equipment.serialnumber = form.serialnumber.data
            equipment.location = form.location.data
            db.session.commit()
            flash('You have successfully edited the equipment.')

            # redirect to the equipment page
            return redirect(url_for('its.list_equipment'))

        form.name.data = equipment.name
        form.description.data = equipment.description
        form.serialnumber.data = equipment.serialnumber
        form.location.data = equipment.location
        return render_template('its/equipment/equipment.html', action="Edit",
                            add_equipment=add_equipment, form=form,
                            equipment=equipment, title="Edit Equipment")
    else:
        abort(403)
# Equipment Delete

@its.route('/equipment/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_equipment(id):
    """
    Delete a equipment from the database
    """
    if current_user.is_admin == True or current_user.is_heng == True:

        equipment = Equipment.query.get_or_404(id)
        db.session.delete(equipment)
        db.session.commit()
        flash('You have successfully deleted the equipment.')

        # redirect to the equipment page
        return redirect(url_for('its.list_equipment'))

        return render_template(title="Delete Equipment")
    else:
        abort(403)

#Satdisk Reports

# Reports Views

@its.route('/reports')
@login_required
def list_reports():
    """
    List Monthly Reports.
    """
    reports = Reports.query.all()
    return render_template('its/reports/reports.html',
                           reports=reports, title='Reports')
#Reports Add
@its.route('/reports/add', methods=['GET', 'POST'])
@login_required
def add_reports():
    """
    Add a reports to the database
    """
    if current_user.is_admin==True or current_user.is_sat==True:

        add_reports = True

        form = ReportsForm()
        if form.validate_on_submit():
            reports = Reports(number=form.number.data,company=form.company.data, service_provided=form.service_provided.data,
                              location=form.location.data, time_gmt_s=form.time_gmt_s.data, time_gmt_e=form.time_gmt_e.data, engineer=form.engineer.data,
                              reference=form.reference.data, guest=form.guest.data, transport_company=form.transport_company.data,
                              transport_kind=form.transport_kind.data, note=form.note.data, date=form.date.data, type=form.type.data)


            # add report to the database
            db.session.add(reports)
            db.session.commit()
            flash('You have successfully added a new report.')


            # redirect to repots page
            return redirect(url_for('its.list_reports'))

        # load reports template
        return render_template('its/reports/report.html', action="Add",
                            add_reports=add_reports, form=form,
                            title="Add Reports")
    else:
        abort(403)

@its.route('/reports/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reports(id):
    """
    Edit a reports
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        add_reports = False

        reports = Reports.query.get_or_404(id)
        form = ReportsForm(obj=reports)
        if form.validate_on_submit():
            reports.number = form.number.data
            reports.company = form.company.data
            reports.service_provided = form.service_provided.data
            reports.location = form.location.data
            reports.time_gmt_s = form.time_gmt_s.data
            reports.time_gmt_e = form.time_gmt_e.data
            reports.engineer = form.engineer.data
            reports.reference = form.reference.data
            reports.guest = form.guest.data
            reports.transport_company = form.transport_company.data
            reports.transport_kind = form.transport_kind.data
            reports.note = form.note.data
            reports.date = form.date.data
            reports.type = form.type.data
            db.session.commit()
            flash('You have successfully edited the report.')

            # redirect to the reports page
            return redirect(url_for('its.list_reports'))

        form.number.data = reports.number
        form.company.data =  reports.company
        form.service_provided.data = reports.service_provided
        form.location.data = reports.location
        form.time_gmt_s.data = reports.time_gmt_s
        form.time_gmt_e.data = reports.time_gmt_e
        form.engineer.data = reports.engineer
        form.reference.data = reports.reference
        form.guest.data = reports.guest
        form.transport_company.data = reports.transport_company
        form.transport_kind.data = reports.transport_kind
        form.note.data = reports.note
        form.date.data = reports.date
        form.type.data = reports.type
        return render_template('its/reports/report.html', action="Edit",
                            add_reports=add_reports, form=form,
                               reports=reports, title="Edit Reports")
    else:
        abort(403)
# Reports Delete

@its.route('/reports/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_reports(id):
    """
    Delete a reports from the database
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        reports = Reports.query.get_or_404(id)
        db.session.delete(reports)
        db.session.commit()
        flash('You have successfully deleted the report.')

        # redirect to the reports page
        return redirect(url_for('its.list_reports'))

        return render_template(title="Delete Reports")
    else:
        abort(403)


#test new tech
@its.route("/export", methods=['GET'])
def doexport():
    return excel.make_response_from_tables(db.session, [Reports], "xls")


@its.route('/reports/search')
@login_required
def search_reports():
    reports = Reports.query.whoosh_search(request.args.get('query')).all()
    if request.args.get('x'):
        return excel.make_response_from_array(reports, "xls")
    return render_template('its/reports/search.html',
                           reports=reports, title='Search')

@its.route('/reports/sng')
@login_required
def list_reports_s():
    """
    List Monthly Reports
    """
    reports = Reports.query.filter(Reports.type=="SNG")
    return render_template('its/reports/sng.html',
                           reports=reports, title='Reports')

@its.route('/reports/eng')
@login_required
def list_reports_e():
    """
    List Monthly Reports
    """
    reports = Reports.query.filter(Reports.type=="ENG")
    return render_template('its/reports/eng.html',
                           reports=reports, title='Reports')

@its.route('/reports/office')
@login_required
def list_reports_o():
    """
    List Monthly Reports
    """
    reports = Reports.query.filter(Reports.type=="Office")
    return render_template('its/reports/office.html',
                           reports=reports, title='Reports')

@its.route('/lives')
@login_required
def list_lives():
    """
    List Daily Lives
    """
    lives = Lives.query.filter(Lives.date== now )
    return render_template('its/lives/lives.html',
                   lives=lives, title='Lives')

@its.route('/lives/add', methods=['GET', 'POST'])
@login_required
def add_lives():
    """
    Add a lives to the database
    """
    if current_user.is_admin==True or current_user.is_sat==True:

        add_lives = True

        form = LivesForm()
        if form.validate_on_submit():
            lives = Lives(company=form.company.data, service_provided=form.service_provided.data,sat=form.sat.data
                          , ul=form.ul.data, dl=form.dl.data, sr=form.sr.data, fec=form.fec.data, mod=form.mod.data,
                          access=form.access.data, time_gmt_s=form.time_gmt_s.data, time_gmt_e=form.time_gmt_e.data,
                          location=form.location.data, date=form.date.data)

            # add live to the database
            db.session.add(lives)
            db.session.commit()
            flash('You have successfully added a new live.')

            # redirect to lives page
            return redirect(url_for('its.list_lives'))

        # load lives template
        return render_template('its/lives/live.html', action="Add",
                            add_lives=add_lives, form=form,
                            title="Add Lives")
    else:
        abort(403)


@its.route('/lives/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lives(id):
    """
    Edit a lives
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        add_lives = False

        lives = Lives.query.get_or_404(id)
        form = LivesForm(obj=lives)
        if form.validate_on_submit():
            lives.company = form.company.data
            lives.service_provided = form.service_provided.data
            lives.sat = form.sat.data
            lives.ul = form.ul.data
            lives.dl = form.dl.data
            lives.sr = form.sr.data
            lives.fec = form.fec.data
            lives.mod = form.mod.data
            lives.access = form.access.date
            lives.time_gmt_s = form.time_gmt_s.data
            lives.time_gmt_e = form.time_gmt_e.data
            lives.location = form.location.data
            lives.date = form.date.data
            db.session.commit()
            flash('You have successfully edited the live.')

            # redirect to the reports page
            return redirect(url_for('its.list_lives'))

        form.company.data =  lives.company
        form.service_provided.data = lives.service_provided
        form.sat.data = lives.sat
        form.ul.data = lives.ul
        form.dl.data = lives.dl
        form.sr.data = lives.sr
        form.fec.data = lives.fec
        form.mod.data = lives.mod
        form.access.data = lives.access
        form.time_gmt_s.data = lives.time_gmt_s
        form.time_gmt_e.data = lives.time_gmt_e
        form.location.data = lives.location
        form.date.data = lives.date
        return render_template('its/lives/live.html', action="Edit",
                            add_lives=add_lives, form=form,
                               lives=lives, title="Edit Lives")
    else:
        abort(403)
# Lives Delet

@its.route('/lives/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_lives(id):
    """
    Delete a lives from the database
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        lives = Lives.query.get_or_404(id)
        db.session.delete(lives)
        db.session.commit()
        flash('You have successfully deleted the live.')

        # redirect to the lives page
        return redirect(url_for('its.list_lives'))

        return render_template(title="Delete Lives")
    else:
        abort(403)


