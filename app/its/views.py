from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from forms import DepartmentForm, EmployeeAssignForm ,EquipmentForm, ReportsForm, LivesForm, FreelancersForm, TransportsForm, StudiosForm, NotesForm, SngordersForm, GuestsForm
from ..models import Department, Employee, Equipment, Reports, Lives, Freelancers, Transports, Studios, Sngorders, Guests
from . import its
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

@its.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    departments = Department.query.order_by(Department.name)

    return render_template('its/departments/departments.html',
                            departments=departments, title="Departments")



@its.route('/departments/add', methods=['GET', 'POST'])
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

    employees = Employee.query.filter(Employee.department_id==id).order_by(Employee.first_name)
    return render_template('its/departments/sub.html',Department=Department,
                        employees=employees, title='Employees')


# Employee Views
@its.route('/employees')
@login_required
def list_employees():

    employees = Employee.query.filter(Employee.first_name!=None).order_by(Employee.department_id)
    return render_template('its/employees/employees.html',
                        employees=employees, title='Employees')



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

    equipment = Equipment.query.order_by(Equipment.type)

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
            equipment = Equipment(name=form.name.data,description=form.description.data, serialnumber=form.serialnumber.data,
                                  modelnumber=form.modelnumber.data, location=form.location.data, status=form.status.data, type=form.type.data)
            # add equipment to the database
            db.session.add(equipment)
            db.session.commit()
            flash('You have successfully added a new equipment.')

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
            equipment.modelnumber = form.modelnumber.data
            equipment.location = form.location.data
            equipment.status = form.status.data
            equipment.type = form.type.data
            db.session.commit()
            flash('You have successfully edited the equipment.')

            # redirect to the equipment page
            return redirect(url_for('its.list_equipment'))

        form.name.data = equipment.name
        form.description.data = equipment.description
        form.serialnumber.data = equipment.serialnumber
        form.modelnumber.data = equipment.modelnumber
        form.location.data = equipment.location
        form.status.data = equipment.status
        form.type.data = equipment.type
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

#sub equipment
@its.route('/equipment/sub/<type>', methods=['GET', 'POST'])
@login_required
def list_equipment_type(type):
    """
    List sub equipment
    """

    equipment = Equipment.query.filter(Equipment.type == type).order_by(Equipment.name)
    return render_template('its/equipment/sub.html', Equipment=Equipment,
                           equipment=equipment, title='Store', type=type)


#Satdisk Reports

# Reports Views

@its.route('/reports')
@login_required
def list_reports():
    """
    List Monthly Reports.
    """
    sng = False
    eng = False
    office = False
    reports = Reports.query.order_by(Reports.time_gmt_s)
    return render_template('its/reports/reports.html',
                           reports=reports, sng=sng, eng=eng, office=office,current_user=current_user, title='Reports')

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
            reports = Reports(company=form.company.data, service_provided=form.service_provided.data,
                              location=form.location.data, space=form.space.data, time_gmt_s=form.time_gmt_s.data, time_gmt_e=form.time_gmt_e.data,
                              extension = form.extension.data,actual_s_time=form.actual_s_time.data,
                              actual_e_time=form.actual_e_time.data,duration=form.duration.data,engineer=form.engineer.data,
                              reference=form.reference.data, guest=form.guest.data, transport_company=form.transport_company.data,
                              transport_kind=form.transport_kind.data, note=form.note.data, date=form.date.data,
                              extrafees=form.extrafees.data, type=form.type.data)


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
            reports.company = form.company.data
            reports.service_provided = form.service_provided.data
            reports.location = form.location.data
            reports.space = form.space.data
            reports.time_gmt_s = form.time_gmt_s.data
            reports.time_gmt_e = form.time_gmt_e.data
            reports.extension = form.extension.data
            reports.actual_s_time = form.actual_s_time.data
            reports.actual_e_time = form.actual_e_time.data
            reports.duration = form.duration.data
            reports.engineer = form.engineer.data
            reports.reference = form.reference.data
            reports.guest = form.guest.data
            reports.transport_company = form.transport_company.data
            reports.transport_kind = form.transport_kind.data
            reports.note = form.note.data
            reports.extrafees = form.extrafees.data
            reports.date = form.date.data
            reports.type = form.type.data
            db.session.commit()
            flash('You have successfully edited the report.')

            # redirect to the reports page
            return redirect(url_for('its.list_reports'))

        form.company.data = reports.company
        form.service_provided.data = reports.service_provided
        form.location.data = reports.location
        form.space.data = reports.space
        form.time_gmt_s.data = reports.time_gmt_s
        form.time_gmt_e.data = reports.time_gmt_e
        form.extension.data = reports.extension
        form.actual_s_time.data = reports.actual_s_time
        form.actual_e_time.data = reports.actual_e_time
        form.duration.data = reports.duration
        form.engineer.data = reports.engineer
        form.reference.data = reports.reference
        form.guest.data = reports.guest
        form.transport_company.data = reports.transport_company
        form.transport_kind.data = reports.transport_kind
        form.note.data = reports.note
        form.extrafees.data = reports.extrafees
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
#@its.route("/export", methods=['GET'])
#def doexport():
 #   return excel.make_response_from_tables(db.session, [Reports], "xls")


@its.route('/reports/search')
@login_required
def search_reports():
    reports = Reports.query.order_by(Reports.date).whoosh_search(request.args.get('query'))
    #reports = Reports.query.filter(Reports.reference==request.args.get('query')).all()
    #column_names = ['number','company', 'service_provided','location', 'time_gmt_s','time_gmt_e', 'engineer','reference', 'guest','transport_company', 'transport_kind','note', 'date','type']
    #if request.args.get('x'):
        #s = Reports.query.filter(Reports.reference=='ww').all()
        #return excel.make_response_from_query_sets(s,column_names, "xls")
        #<a href="{{ url_for('its.search_reports', x='true') }}" class="btn btn-default btn-lg">
    return render_template('its/reports/search.html',
                           reports=reports,current_user=current_user, title='Reports')

@its.route('/reports/sng')
@login_required
def list_reports_s():
    """
    List Monthly Reports
    """
    sng = True
    eng = False
    office = False
    reports = Reports.query.filter(Reports.type=="SNG").order_by(Reports.time_gmt_s)
    return render_template('its/reports/reports.html',
                           reports=reports, sng=sng, eng=eng, office=office,current_user=current_user, title='Reports')

@its.route('/reports/eng')
@login_required
def list_reports_e():
    """
    List Monthly Reports
    """
    sng = False
    eng = True
    office = False
    reports = Reports.query.filter(Reports.type=="ENG").order_by(Reports.time_gmt_s)
    return render_template('its/reports/reports.html',
                           reports=reports, sng=sng, eng=eng, office=office,current_user=current_user, title='Reports')

@its.route('/reports/office')
@login_required
def list_reports_o():
    """
    List Monthly Reports
    """
    sng = False
    eng = False
    office = True
    reports = Reports.query.filter(Reports.type=="Office").order_by(Reports.time_gmt_s)
    return render_template('its/reports/reports.html',
                           reports=reports, sng=sng, eng=eng, office=office,current_user=current_user, title='Reports')

@its.route('/lives')
@login_required
def list_lives():
    """
    List Daily Lives
    """
    lives = Lives.query.filter(Lives.date== now).order_by(Lives.time_gmt_s)
    return render_template('its/lives/lives.html',
                   lives=lives, title='Lives')

@its.route('/lives/archive')
@login_required
def list_archived_lives():
    """
    List Archived Lives
    """
    lives = Lives.query.order_by(Lives.date)
    return render_template('its/lives/archive.html',
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
                          access=form.access.data, reference=form.reference.data, time_gmt_s=form.time_gmt_s.data, time_gmt_e=form.time_gmt_e.data,
                          location=form.location.data, reg_code=form.reg_code.data, date=form.date.data)

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
            lives.access = form.access.data
            lives.reference = form.reference.data
            lives.time_gmt_s = form.time_gmt_s.data
            lives.time_gmt_e = form.time_gmt_e.data
            lives.location = form.location.data
            lives.reg_code = form.reg_code.data
            lives.date = form.date.data
            db.session.commit()
            flash('You have successfully edited the live.')

            # redirect to the reports page
            return redirect(url_for('its.list_lives'))

        form.company.data = lives.company
        form.service_provided.data = lives.service_provided
        form.sat.data = lives.sat
        form.ul.data = lives.ul
        form.dl.data = lives.dl
        form.sr.data = lives.sr
        form.fec.data = lives.fec
        form.mod.data = lives.mod
        form.access.data = lives.access
        form.reference.data = lives.reference
        form.time_gmt_s.data = lives.time_gmt_s
        form.time_gmt_e.data = lives.time_gmt_e
        form.location.data = lives.location
        form.reg_code.data = lives.reg_code
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

@its.route('/lives/search')
@login_required
def search_lives():
    lives = Lives.query.order_by(Lives.date).whoosh_search(request.args.get('query'))
    return render_template('its/lives/search.html',
                           lives=lives, title='Lives')

@its.route('/lives/note/<int:id>', methods=['GET', 'POST'])
@login_required
def eng_lives(id):
    if current_user.is_admin == True or current_user.is_eng == True:

        lives = Lives.query.get_or_404(id)
        form = NotesForm(obj=lives)
        if form.validate_on_submit():
            lives.note = form.note.data
            db.session.commit()
            flash('You have successfully edited the live note.')

            # redirect to the reports page
            return redirect(url_for('its.list_lives'))

        form.note.data = lives.note
        return render_template('its/lives/eng.html', action="Eng Edit", form=form,
                               lives=lives, title="Eng Edit Lives")
    else:
        abort(403)

@its.route('/freelancers')
@login_required
def list_freelancers():
    """
    List freelancers.
    """

    freelancers = Freelancers.query.order_by(Freelancers.job)
    return render_template('its/freelancers/freelancers.html',
                           freelancers=freelancers,current_user=current_user, title='Freelancers')


@its.route('/freelancers/add', methods=['GET', 'POST'])
@login_required
def add_freelancers():
    """
    Add a freelancers to the database
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        add_freelancers = True

        form = FreelancersForm()
        if form.validate_on_submit():
            freelancers = Freelancers(job=form.job.data, first_name=form.first_name.data,
                                          last_name=form.last_name.data, hire_rate=form.hire_rate.data, tel=form.tel.data)

            # add freelancers to the database
            db.session.add(freelancers)
            db.session.commit()
            flash('You have successfully added a new freelancer.')

            # redirect to lives page
            return redirect(url_for('its.list_freelancers'))

        # load lives template
        return render_template('its/freelancers/freelancer.html', action="Add",
                               add_freelancers=add_freelancers, form=form,
                               title="Add Freelancers")
    else:
        abort(403)


@its.route('/freelancers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_freelancers(id):
    """
    Edit a freelancers
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        add_freelancers = False

        freelancers = Freelancers.query.get_or_404(id)
        form = FreelancersForm(obj=freelancers)
        if form.validate_on_submit():
            freelancers.job = form.job.data
            freelancers.first_name = form.first_name.data
            freelancers.last_name = form.last_name.data
            freelancers.hire_rate = form.hire_rate.data
            freelancers.tel = form.tel.data
            db.session.commit()
            flash('You have successfully edited the freelancer data.')

            # redirect to the reports page
            return redirect(url_for('its.list_freelancers'))

        form.job.data = freelancers.job
        form.first_name.data = freelancers.first_name
        form.last_name.data = freelancers.last_name
        form.hire_rate.data = freelancers.hire_rate
        form.tel.data = freelancers.tel
        return render_template('its/freelancers/freelancer.html', action="Edit",
                            add_freelancers=add_freelancers, form=form, id=id,
                               freelancers=freelancers, title="Edit Freelancers")
    else:
        abort(403)


@its.route('/freelancers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_freelancers(id):
    """
    Delete a freelancers from the database
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        freelancers = Freelancers.query.get_or_404(id)
        db.session.delete(freelancers)
        db.session.commit()
        flash('You have successfully deleted the freelancer.')

        return redirect(url_for('its.list_freelancers'))

        return render_template(title="Delete Freelancers")
    else:
        abort(403)

@its.route('/freelancers/sub/<job>', methods=['GET', 'POST'])
@login_required
def list_freelancers_job(job):

    freelancers = Freelancers.query.filter(Freelancers.job == job).order_by(Freelancers.first_name)
    return render_template('its/freelancers/sub.html', Freelancers=Freelancers,
                           freelancers=freelancers, title='freelancers', job=job)



@its.route('/transports')
@login_required
def list_transports():

    transports = Transports.query.all()
    return render_template('its/transports/transports.html',
                           transports=transports, title='Transports')

#Reports Add
@its.route('/transports/add', methods=['GET', 'POST'])
@login_required
def add_transports():

    if current_user.is_admin==True or current_user.is_sat==True:

        add_transports = True

        form = TransportsForm()
        if form.validate_on_submit():
            transports = Transports(date=form.date.data,company=form.company.data, reference=form.reference.data
                                    , guest_counter=form.guest_counter.data, guest1=form.guest1.data,
                                    guest2=form.guest2.data,guest3=form.guest3.data,
                                    guest4=form.guest4.data, guest5=form.guest5.data,
                                    guest6=form.guest6.data, guest7=form.guest7.data,
                                    guest8=form.guest8.data, guest9=form.guest9.data,
                                    guest10=form.guest10.data,
                                    city1=form.city1.data, city2=form.city2.data,
                                    city3=form.city3.data, city4=form.city4.data,
                                    city5=form.city5.data, city6=form.city6.data,
                                    city7=form.city7.data, city8=form.city8.data,
                                    city9=form.city9.data, city10=form.city10.data,
                                    note=form.note.data)


            db.session.add(transports)
            db.session.commit()
            flash('You have successfully added a new Transport report.')


            # redirect to repots page
            return redirect(url_for('its.list_transports'))

        # load reports template
        return render_template('its/transports/transport.html', action="Add",
                            add_transports=add_transports, form=form,
                            title="Add Transports")
    else:
        abort(403)

@its.route('/transports/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transports(id):
 
    if current_user.is_admin == True or current_user.is_sat == True:

        add_transports = False

        transports = Transports.query.get_or_404(id)
        form = TransportsForm(obj=transports)
        if form.validate_on_submit():
            transports.date = form.date.data
            transports.company = form.company.data
            transports.reference = form.reference.data
            transports.guest_counter = form.guest_counter.data
            transports.guest1 = form.guest1.data
            transports.city1 = form.city1.data
            transports.guest2 = form.guest2.data
            transports.city2 = form.city2.data
            transports.guest3 = form.guest3.data
            transports.city3 = form.city3.data
            transports.guest4 = form.guest4.data
            transports.city4 = form.city4.data
            transports.guest5 = form.guest5.data
            transports.city5 = form.city5.data
            transports.guest6 = form.guest6.data
            transports.city6 = form.city6.data
            transports.guest7 = form.guest7.data
            transports.city7 = form.city7.data
            transports.guest8 = form.guest8.data
            transports.city8 = form.city8.data
            transports.guest9 = form.guest9.data
            transports.city9 = form.city9.data
            transports.guest10 = form.guest10.data
            transports.city10 = form.city10.data
            transports.note = form.note.data
            db.session.commit()
            flash('You have successfully edited the transport.')

            # redirect to the transports page
            return redirect(url_for('its.list_transports'))
        form.date.data = transports.date
        form.company.data = transports.company
        form.reference.data = transports.reference
        form.guest_counter = transports.guest_counter
        form.guest1 = transports.guest1
        form.city1 = transports.city1
        form.guest2 = transports.guest2
        form.city2 = transports.city2
        form.guest3 = transports.guest3
        form.city3 = transports.city3
        form.guest4 = transports.guest4
        form.city4 = transports.city4
        form.guest5 = transports.guest5
        form.city5 = transports.city5
        form.guest6 = transports.guest6
        form.city6 = transports.city6
        form.guest7 = transports.guest7
        form.city7 = transports.city7
        form.guest8 = transports.guest8
        form.city8 = transports.city8
        form.guest9 = transports.guest9
        form.city9 = transports.city9
        form.guest10 = transports.guest10
        form.city10 = transports.city10
        form.note.data = transports.note
        return render_template('its/transports/transport.html', action="Edit",
                            add_transports=add_transports, form=form,
                               transports=transports, title="Edit Transports")
    else:
        abort(403)
# Transports Delete

@its.route('/transports/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_transports(id):
    """
    Delete a transports from the database
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        transports = Transports.query.get_or_404(id)
        db.session.delete(transports)
        db.session.commit()
        flash('You have successfully deleted the transport.')

        # redirect to the transports page
        return redirect(url_for('its.list_transports'))

        return render_template(title="Delete Transports")
    else:
        abort(403)


@its.route('/transports/search')
@login_required
def search_transports():
    transports = Transports.query.order_by(Transports.date).whoosh_search(request.args.get('query'))

    return render_template('its/transports/search.html',
                           transports=transports, title='Transports')

@its.route('/studios')
@login_required
def list_studios():
    alyoum = False
    best_of_alyoum = False
    kalam_masry = False
    dispute_diffrences = False
    other = False
    studios = Studios.query.order_by(Studios.time_gmt_s)
    return render_template('its/studios/studios.html',
                           studios=studios, alyoum=alyoum, best_of_alyoum=best_of_alyoum, kalam_masry=kalam_masry,
                           dispute_diffrences=dispute_diffrences, other=other, title='Studios')

#Reports Add
@its.route('/studios/add', methods=['GET', 'POST'])
@login_required
def add_studios():

    if current_user.is_admin==True or current_user.is_mos==True:

        add_studios = True

        form = StudiosForm()
        if form.validate_on_submit():
            studios = Studios(date=form.date.data, company=form.company.data, showname = form.showname.data,
                              reference=form.reference.data, time_gmt_s=form.time_gmt_s.data, time_gmt_e=form.time_gmt_e.data, 
                              note=form.note.data)

            db.session.add(studios)
            db.session.commit()
            flash('You have successfully added a new Studio report.')

            return redirect(url_for('its.list_studios'))

        # load reports template
        return render_template('its/studios/studio.html', action="Add",
                            add_studios=add_studios, form=form,
                            title="Add Studios")
    else:
        abort(403)

@its.route('/studios/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_studios(id):
   
    if current_user.is_admin == True or current_user.is_mos == True:

        add_studios = False

        studios = Studios.query.get_or_404(id)
        form = StudiosForm(obj=studios)
        if form.validate_on_submit():
            studios.date = form.date.data
            studios.company = form.company.data
            studios.showname = form.showname.data
            studios.reference = form.reference.data
            studios.time_gmt_s = form.time_gmt_s.data
            studios.time_gmt_e = form.time_gmt_e.data
            studios.note = form.note.data
            db.session.commit()
            flash('You have successfully edited the studio report.')

            # redirect to the studios page
            return redirect(url_for('its.list_studios'))

        form.date.data = studios.date
        form.company.data = studios.company
        form.showname.data = studios.showname
        form.reference.data = studios.reference
        form.time_gmt_s.data = studios.time_gmt_s
        form.time_gmt_e.data = studios.time_gmt_e
        form.note.data = studios.note
        return render_template('its/studios/studio.html', action="Edit",
                            add_studios=add_studios, form=form,
                               studios=studios, title="Edit Studios")
    else:
        abort(403)

@its.route('/studios/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_studios(id):

    if current_user.is_admin == True or current_user.is_mos == True:

        studios = Studios.query.get_or_404(id)
        db.session.delete(studios)
        db.session.commit()
        flash('You have successfully deleted the studios report.')

        return redirect(url_for('its.list_studios'))

        return render_template(title="Delete Studios")
    else:
        abort(403)




@its.route('/studios/search')
@login_required
def search_studios():
    studios = Studios.query.order_by(Studios.date).whoosh_search(request.args.get('query'))
    return render_template('its/studios/search.html',
                           studios=studios, title='Studios')

@its.route("/studios/export", methods=['GET'])
def doexport_studios():
    return excel.make_response_from_tables(db.session, [Studios], "xls")


@its.route('/studios/alyoum')
@login_required
def list_alyoum():
    alyoum = True
    best_of_alyoum = False
    kalam_masry = False
    dispute_diffrences = False
    other = False
    studios = Studios.query.filter(Studios.showname=="Al Youm").order_by(Studios.time_gmt_s)
    return render_template('its/studios/studios.html',
                           studios=studios, alyoum=alyoum, best_of_alyoum=best_of_alyoum, kalam_masry=kalam_masry,
                           dispute_diffrences=dispute_diffrences, other=other, title='Studios')


@its.route('/studios/best_of_alyoum')
@login_required
def list_best_of_alyoum():
    alyoum = False
    best_of_alyoum = True
    kalam_masry = False
    dispute_diffrences = False
    other = False
    studios = Studios.query.filter(Studios.showname=="Best of Al Youm").order_by(Studios.time_gmt_s)
    return render_template('its/studios/studios.html',
                           studios=studios, alyoum=alyoum, best_of_alyoum=best_of_alyoum, kalam_masry=kalam_masry,
                           dispute_diffrences=dispute_diffrences, other=other, title='Studios')

@its.route('/studios/kalam_masry')
@login_required
def list_kalam_masry():
    alyoum = False
    best_of_alyoum = True
    kalam_masry = True
    dispute_diffrences = False
    other = False
    studios = Studios.query.filter(Studios.showname=="Kalam Masry").order_by(Studios.time_gmt_s)
    return render_template('its/studios/studios.html',
                           studios=studios, alyoum=alyoum, best_of_alyoum=best_of_alyoum, kalam_masry=kalam_masry,
                           dispute_diffrences=dispute_diffrences, other=other, title='Studios')

@its.route('/studios/dispute_differences')
@login_required
def list_dispute_differences():
    alyoum = False
    best_of_alyoum = True
    kalam_masry = True
    dispute_diffrences = True
    other = False
    studios = Studios.query.filter(Studios.showname=="Dispute or Differences").order_by(Studios.time_gmt_s)
    return render_template('its/studios/studios.html',
                           studios=studios, alyoum=alyoum, best_of_alyoum=best_of_alyoum, kalam_masry=kalam_masry,
                           dispute_diffrences=dispute_diffrences, other=other, title='Studios')

@its.route('/studios/other')
@login_required
def list_other():
    alyoum = False
    best_of_alyoum = True
    kalam_masry = True
    dispute_diffrences = True
    other = True
    studios = Studios.query.filter(Studios.showname=="Other").order_by(Studios.time_gmt_s)
    return render_template('its/studios/studios.html',
                           studios=studios, alyoum=alyoum, best_of_alyoum=best_of_alyoum, kalam_masry=kalam_masry,
                           dispute_diffrences=dispute_diffrences, other=other, title='Studios')

@its.route('/sngorders')
@login_required
def list_sngorders():

    sngorders = Sngorders.query.order_by(Sngorders.date)
    return render_template('its/sngorders/sngorders.html', sngorders=sngorders, title='SNG Orders')

@its.route('/sngorders/add', methods=['GET', 'POST'])
@login_required
def add_sngorders():

    if current_user.is_admin==True or current_user.is_eng==True:

        add_sngorders = True

        form = SngordersForm()
        if form.validate_on_submit():
            sngorders = Sngorders(date=form.date.data, company=form.company.data, engineer=form.engineer.data,
                            location=form.location.data, reference=form.reference.data, time_gmt_s=form.time_gmt_s.data, time_gmt_e=form.time_gmt_e.data,
                            cameraman=form.cameraman.data,tech=form.tech.data, driver=form.driver.data, camera=form.camera.data,
                            car=form.car.data, note=form.note.data)

            db.session.add(sngorders)
            db.session.commit()
            flash('You have successfully added a new Sng Order.')

            return redirect(url_for('its.list_sngorders'))

        # load reports template
        return render_template('its/sngorders/sngorder.html', action="Add",
                            add_sngorders=add_sngorders, form=form,
                            title="Add Sngorders")
    else:
        abort(403)


@its.route('/sngorders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_sngorders(id):
 
    if current_user.is_admin == True or current_user.is_eng == True:

        add_sngorders = False

        sngorders = Sngorders.query.get_or_404(id)
        form = SngordersForm(obj=sngorders)
        if form.validate_on_submit():
            sngorders.date = form.date.data
            sngorders.company = form.company.data
            sngorders.engineer = form.engineer.data
            sngorders.location = form.location.data
            sngorders.reference = form.reference.data
            sngorders.time_gmt_s = form.time_gmt_s.data
            sngorders.time_gmt_e = form.time_gmt_e.data
            sngorders.cameraman = form.cameraman.data
            sngorders.tech = form.tech.data
            sngorders.driver = form.driver.data
            sngorders.camera = form.camera.data
            sngorders.car = form.car.data
            sngorders.note = form.note.data
            db.session.commit()
            flash('You have successfully edited the Sng order.')
            return redirect(url_for('its.list_sngorders'))

        form.date.data = sngorders.date
        form.company.data = sngorders.company
        form.engineer.data = sngorders.engineer
        form.location.data = sngorders.location
        form.reference.data = sngorders.reference
        form.time_gmt_s.data = sngorders.time_gmt_s
        form.time_gmt_e.data = sngorders.time_gmt_e
        form.cameraman.data = sngorders.cameraman
        form.tech.data = sngorders.tech
        form.driver.data = sngorders.driver
        form.camera.data = sngorders.camera
        form.car.data = sngorders.car
        form.note.data = sngorders.note
        return render_template('its/sngorders/sngorder.html', action="Edit",
                            add_sngorders=add_sngorders, form=form,
                               sngorders=sngorders, title="Edit Sngorders")
    else:
        abort(403)

@its.route('/sngorders/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_sngorders(id):

    if current_user.is_admin == True or current_user.is_eng == True:
        sngorders = Sngorders.query.get_or_404(id)
        db.session.delete(sngorders)
        db.session.commit()
        flash('You have successfully deleted the Sng order.')
        return redirect(url_for('its.list_sngorders'))
        return render_template(title="Delete Sngorders")
    else:
        abort(403)



@its.route('/sngorders/search')
@login_required
def search_sngorders():
    sngorders = Sngorders.query.order_by(Sngorders.date).whoosh_search(request.args.get('query'))
    return render_template('its/sngorders/search.html',
                           sngorders=sngorders, title='Sngorders')

@its.route("/sngorders/export", methods=['GET'])
def doexport_sngorders():
    return excel.make_response_from_tables(db.session, [Sngorders], "xls")


@its.route('/guests')
@login_required
def list_guests():


    guests = Guests.query.order_by(Guests.job)
    return render_template('its/guests/guests.html',
                           guests=guests, title='Guest')


@its.route('/guests/add', methods=['GET', 'POST'])
@login_required
def add_guests():

    if current_user.is_admin == True or current_user.is_sat == True:

        add_guests = True

        form = GuestsForm()
        if form.validate_on_submit():
            guests = Guests(job=form.job.data, title=form.title.data, first_name=form.first_name.data,
                                          last_name=form.last_name.data, tel=form.tel.data, address=form.address.data)

            # add guests to the database
            db.session.add(guests)
            db.session.commit()
            flash('You have successfully added a new Guest.')

            # redirect to lives page
            return redirect(url_for('its.list_guests'))

        # load lives template
        return render_template('its/guests/guest.html', action="Add",
                               add_guests=add_guests, form=form,
                               title="Add Guest")
    else:
        abort(403)


@its.route('/guests/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_guests(id):

    if current_user.is_admin == True or current_user.is_sat == True:

        add_guests = False

        guests = Guests.query.get_or_404(id)
        form = GuestsForm(obj=guests)
        if form.validate_on_submit():
            guests.job = form.job.data
            guests.title = form.title.data
            guests.first_name = form.first_name.data
            guests.last_name = form.last_name.data
            guests.tel = form.tel.data
            guests.address = form.address.data
            db.session.commit()
            flash('You have successfully edited the guest data.')

            return redirect(url_for('its.list_guests'))

        form.job.data = guests.job
        form.title.data = guests.title
        form.first_name.data = guests.first_name
        form.last_name.data = guests.last_name
        form.tel.data = guests.tel
        form.address.data = guests.address
        return render_template('its/guests/guest.html', action="Edit",
                            add_guests=add_guests, form=form, id=id,
                               guests=guests, title="Edit Guest")
    else:
        abort(403)


@its.route('/guests/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_guests(id):
    """
    Delete a guests from the database
    """
    if current_user.is_admin == True or current_user.is_sat == True:

        guests = Guests.query.get_or_404(id)
        db.session.delete(guests)
        db.session.commit()
        flash('You have successfully deleted the guest.')

        return redirect(url_for('its.list_guests'))

        return render_template(title="Delete Guest")
    else:
        abort(403)

@its.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    return render_template('its/schedule/schedule.html')

