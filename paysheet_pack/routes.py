import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from paysheet_pack.forms import RegistrationForm, LoginForm, UpdateAccountForm, TaxtableForm, NewemployeForm, OvertimetableForm, EmployeeListForm
from paysheet_pack.models import Company, Employeeinfo, TaxEntry, OvertimeEntry
from paysheet_pack import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        company = Company(company_name=form.company_name.data, email=form.email.data, password=hashed_password)
        db.session.add(company)
        db.session.commit()
        flash(f'For {form.company_name.data} company account created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(email=form.email.data).first()
        if company and bcrypt.check_password_hash(company.password, form.password.data):
            login_user(company, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.company_name = form.company_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.company_name.data = current_user.company_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/tax_table", methods=['GET', 'POST'])
@login_required
def tax_table():
    form = TaxtableForm()
    datas = TaxEntry.query.all()

    if form.validate_on_submit():
        if form.save_and_new.data == 'true':
            # Process and store the form data in the database
            min_pay = form.min_pay.data
            max_pay = form.max_pay.data
            tax_rate = form.tax_rate.data
            pension = form.pension.data

            # Here, you would save this data to your database (e.g., using SQLAlchemy)
            # Replace the following with your actual database model and logic
            tax_entry = TaxEntry(min_pay=min_pay, max_pay=max_pay, tax_rate=tax_rate, pension=pension)
            db.session.add(tax_entry)
            db.session.commit()

            flash('The previous tax entry added successfully add the new one', 'success')
            return redirect(url_for('tax_table'))
        else:
            min_pay = form.min_pay.data
            max_pay = form.max_pay.data
            tax_rate = form.tax_rate.data
            pension = form.pension.data

            # Here, you would save this data to your database (e.g., using SQLAlchemy)
            # Replace the following with your actual database model and logic
            tax_entry = TaxEntry(min_pay=min_pay, max_pay=max_pay, tax_rate=tax_rate, pension=pension)
            db.session.add(tax_entry)
            db.session.commit()
            flash('It is the tax rate table used for calculate your company employee income', 'success')
            return redirect(url_for('tax_table'))


    return render_template('tax_table.html', title='Tax_table', form=form, datas=datas)


@app.route("/tax_table/tax_update", methods=['GET', 'POST'])
@login_required
def tax_update():
    form = TaxtableForm()
    datas = TaxEntry.query.all()
    # Assuming 'id' is a field in your form
    entry_id = form.id.data
    data_entry = TaxEntry.query.filter_by(id=entry_id).first()

    if form.validate_on_submit():
        # Update values from the form
        data_entry.min_pay = form.min_pay.data
        data_entry.max_pay = form.max_pay.data
        data_entry.tax_deduction = form.tax_deduction.data
        data_entry.tax_rate = form.tax_rate.data
        data_entry.pension = form.pension.data

        # Commit changes to the database
        db.session.commit()

        flash('Your data successfully updated', 'success')
        return redirect(url_for('tax_update'))

    return render_template('tax_update.html', title='Tax_update', data_entry=data_entry, form=form, datas=datas)

@app.route("/overtime_table", methods=['GET', 'POST'])
@login_required
def overtime_table():
    form = OvertimetableForm()
    datas = OvertimeEntry.query.all()
    if form.validate_on_submit():
        in_time = form.in_time.data
        out_time = form.out_time.data
        other = form.other.data
        ov_rate = form.ov_rate.data

        # Process and store the form data in the database for Save and New
        ov_entry = OvertimeEntry(in_time=in_time, out_time=out_time, ov_rate=ov_rate, other=other)
        db.session.add(ov_entry)
        db.session.commit()

        flash('The previous overtime entry was added successfully. Add a new one.', 'success')
        return redirect(url_for('overtime_table'))


    return render_template('overtime_table.html', title='Over_time_table', form=form, datas=datas)



@app.route("/overtime_table/overtime_update", methods=['GET', 'POST'])
@login_required
def overtime_update():
    form = OvertimetableForm()
    datas = OvertimeEntry.query.all()
    # Assuming 'id' is a field in your form
    entry_id = form.id.data
    data_entry = OvertimeEntry.query.filter_by(id=entry_id).first()

    if form.validate_on_submit():
        # Update values from the form
        data_entry.in_time = form.in_time.data
        data_entry.out_time = form.out_time.data
        data_entry.ov_rate = form.ov_rate.data
        data_entry.other = form.other.data

        # Commit changes to the database
        db.session.commit()

        flash('Your data successfully updated', 'success')
        return redirect(url_for('overtime_table_list'))

    return render_template('overtime_update.html', title='Overtime_update', data_entry=data_entry, form=form, datas=datas)

def tax_calculate(growth_earning, basic_salary, emp_status):
    datas = TaxEntry.query.all()
    tax = 0.0
    pension = 0.0

    for data in datas:
        if data.min_pay <= growth_earning <= data.max_pay:
            # Calculate tax based on the current data entry
            tax = (growth_earning * (data.tax_rate / 100.0)) - data.tax_deduction

        if emp_status == 'permanent':
            pension = (basic_salary * (data.pension / 100.0))
        break;

    return tax, pension


def ov_calculate(basic_salary, emp_id):
    datas = Employeeinfo.query.filter_by(emp_id=emp_id).first()
    ov_data = OvertimeEntry.query.all()
    ov = 0.0

    for data in ov_data:
        # evaluate duration on working hour
        if datas.in_time == ov_data.in_time and datas.out_time == ov_data.out_time:
            ov = (basic_salary / 160) * datas.duration * data.ov_rate
            break;
        elif datas.other == 'weekend day' or datas.other == 'weekend day':
            ov = (basic_salary / 160) * datas.duration * data.ov_rate
        elif datas.other == 'holiday' or datas.other == 'holiday':
            ov = (basic_salary / 160) * datas.duration * data.ov_rate
    return ov




@app.route("/company/new_employee", methods=['GET', 'POST'])
@login_required
def new_employee():
    form = NewemployeForm()
    if form.validate_on_submit():
        emp_name = form.emp_name.data
        position = form.position.data
        company_id = current_user.id
        phone = form.phone.data
        emp_status = form.emp_status.data
        basic_salary = float(form.basic_salary.data) 

        # fake data
        transportation_allowance = 0.0
        allowance = 0.0
        overtime = 0.0
        other_deduction = 0.0
        # calculate employee info
        growth_earning = basic_salary
        tax_info = tax_calculate(growth_earning, basic_salary, emp_status)
        total_deduction = (tax_info[0]) + (tax_info[1]) + (other_deduction)
        net_pay = (growth_earning - total_deduction)

        new_employee = Employeeinfo(emp_name=emp_name, position=position, emp_status=emp_status, company_id=company_id,
                                    phone=phone, basic_salary=basic_salary, growth_earning=growth_earning,
                                    total_deduction=total_deduction, tax=tax_info[0], pension=tax_info[1], net_pay=net_pay)
        db.session.add(new_employee)
        db.session.commit()
        # Filter by phone to get the employee instance
        flash('New employee successfully added', 'success')
        return redirect(url_for('home'))
    return render_template('new_employee.html', title='New_employee', form=form)

@app.route("/company/employee_list", methods=['GET', 'POST'])
@login_required
def employee_list():
    form = EmployeeListForm()
    datas = Employeeinfo.query.filter_by(company_id=current_user.id)
    emp_id = form.emp_id.data
    if 'view' in request.form:
        datas = Employeeinfo.query.filter_by(emp_id=emp_id)
        return render_template('employee_list.html', title='Find_employee', form=form, datas=datas)
    elif 'delete' in request.form:
        employee_to_delete = Employeeinfo.query.get(emp_id)
        if employee_to_delete:
            db.session.delete(employee_to_delete)
            db.session.commit()
            flash(f'Employee with ID {emp_id} has been deleted', 'success')
        else:
            flash(f'Employee with ID {emp_id} not found', 'danger')
    elif 'update' in request.form:
        return redirect(url_for('employee_update', emp_id=emp_id))
    return render_template('employee_list.html', title='Employee_list', form=form, datas=datas)


@app.route("/company/<int:emp_id>", methods=['GET', 'POST'])
@login_required
def employee_update(emp_id):
    form = EmployeeListForm()
    data_entry = Employeeinfo.query.filter_by(emp_id=emp_id).first()
    if data_entry is None:
        flash(f'Employee with ID {emp_id} not found', 'danger')
        return redirect(url_for('employee_list'))

    if request.method == 'POST':
        data_entry.emp_name = form.emp_name.data
        data_entry.phone = form.phone.data 
        data_entry.position = form.position.data
        data_entry.emp_status = form.emp_status.data
        data_entry.basic_salary = form.basic_salary.data
        data_entry.in_time = form.in_time.data
        data_entry.out_time = form.out_time.data
        data_entry.duration = form.duration.data
        data_entry.other = form.other.data

        # initialize ov with a default value
        ov = 0.0

        # evaluate duration on working hour
        if form.in_time.data == '6' and form.out_time.data == '10':
            ov = (form.basic_salary.data / 160) * float(form.duration.data) * 1.25
        elif form.in_time.data == '10' and form.out_time.data == '6':
            ov = (form.basic_salary.data / 160) * float(form.duration.data) * 1.5
        elif form.other.data == 'holiday':
            ov = (form.basic_salary.data / 160) * float(form.duration.data) * 2.5
        elif form.other.data == 'weekend':
            ov = (form.basic_salary.data / 160) * float(form.duration.data) * 2

        data_entry.overtime = ov
        data_entry.allowance = form.allowance.data
        data_entry.other_deduction = form.other_deduction.data
        data_entry.transportation_allowance = form.transportation_allowance.data
        # calculate the net pay

        # calculate employee 1/4th of basic salary
        portion = (form.basic_salary.data * (0.25))

        taxable_allowance = 0.0

        if form.transportation_allowance.data < portion:
            pass
        elif form.transportation_allowance.data >= portion and portion <= 2200:
            taxable_allowance = (form.transportation_allowance.data - portion)
        elif portion > 2200 and form.transportation_allowance.data > 2200:
            taxable_allowance = (form.transportation_allowance.data - 2200)

        growth_earning = (data_entry.basic_salary) + (taxable_allowance) + (data_entry.overtime)
        tax_info = tax_calculate(growth_earning, data_entry.basic_salary, data_entry.emp_status)
        total_deduction = (tax_info[0]) + (tax_info[1]) + (data_entry.other_deduction)
        net_pay = (growth_earning - total_deduction)
        data_entry.growth_earning = growth_earning
        data_entry.tax = tax_info[0]
        data_entry.pension = tax_info[1]
        data_entry.total_deduction = total_deduction
        data_entry.net_pay = net_pay
        # Commit changes to the database
        db.session.commit()
        flash('Your data successfully updated', 'success')
        return redirect(url_for('employee_list'))

    form.emp_name.data = data_entry.emp_name
    form.phone.data = data_entry.phone
    form.position.data = data_entry.position
    form.emp_status.data = data_entry.emp_status
    form.basic_salary.data = data_entry.basic_salary
    form.overtime.data = data_entry.overtime
    form.in_time.data = data_entry.in_time
    form.out_time.data = data_entry.out_time
    form.duration.data = data_entry.duration
    form.other.data = data_entry.other
    form.transportation_allowance.data = data_entry.transportation_allowance
    form.allowance.data = data_entry.allowance
    form.other_deduction.data = data_entry.other_deduction  
    return render_template('employee_update.html', title='Employee_update', form=form, data_entry=data_entry)
