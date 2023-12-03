from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from paysheet_pack.models import Company
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, HiddenField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    company_name = StringField('Company Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')

    def validate_company_name(self, company_name):
        company = Company.query.filter_by(company_name=company_name.data).first()
        if company:
            raise ValidationError('That company name is taken. Please choose a different one')

    def validate_email(self, email):
        company = Company.query.filter_by(email=email.data).first()
        if company:
            raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    company_name = StringField('company_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_company_name(self, company_name):
        if company_name.data != current_user.company_name:
            company = Company.query.filter_by(company_name=company_name.data).first()
            if company:
                raise ValidationError('That company_name is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            company = Company.query.filter_by(email=email.data).first()
            if company:
                raise ValidationError('That email is taken. Please choose a different one.')
            
class TaxtableForm(FlaskForm):
    id = StringField('Row Id')
    min_pay = StringField('Min Pay', validators=[DataRequired()])
    max_pay = StringField('Max Pay', validators=[DataRequired()])
    tax_rate = StringField('Tax Rate', validators=[DataRequired()])
    tax_deduction = StringField('Tax Deduction', validators=[DataRequired()])
    pension = StringField('Pension', validators=[DataRequired()])
    save_and_new = HiddenField('Save and New')
    submit = SubmitField('Submit')

class NewemployeForm(FlaskForm):
    emp_name = StringField('Employee Name*', validators=[DataRequired()]) 
    position = StringField('Position*', validators=[DataRequired()])
    phone = StringField('Phone Number*', validators=[DataRequired()])
    basic_salary = StringField('Basic Salary*', validators=[DataRequired()])
    emp_status = StringField('Employee Status', validators=[DataRequired()])
    overtime = StringField('Over Time(If It has else leave empty)')
    allowance = StringField('Allowance(If It has else leave empty)')
    other_deduction = StringField('Other Deduction(If It has else leave empty)')
    submit = SubmitField('Create')

class OvertimetableForm(FlaskForm):
    id = StringField('Row Id')
    in_time = StringField('In Time')
    out_time = StringField('Out Time')
    other = StringField('Holiday or Weekend Day')
    ov_rate = FloatField('Overtime Rate', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeListForm(FlaskForm):
    emp_name = StringField('Employee Name', validators=[DataRequired()]) 
    position = StringField('Position', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    basic_salary = FloatField('Basic Salary', validators=[DataRequired()])
    emp_id = IntegerField('Employee Id', validators=[DataRequired()])
    company_id = IntegerField('Company Id ', validators=[DataRequired()])
    growth_earning = FloatField('Growth Earning', validators=[DataRequired()])
    overtime = FloatField('Over Time')
    allowance = FloatField('Other Allowance', validators=[DataRequired()])
    tax = FloatField('Tax', validators=[DataRequired()])
    pension = FloatField('Pension', validators=[DataRequired()])
    other_deduction = FloatField('Other Deduction', validators=[DataRequired()])
    total_deduction = StringField('Total Deduction', validators=[DataRequired()])
    emp_status = StringField('Employee Status', validators=[DataRequired()])
    in_time = StringField('Overtime (in time)')
    out_time = StringField('Overtime (out time)')
    other = StringField('Overtime (Holiday or Weekend)')
    duration = StringField('Overtime (Duration)')
    net_pay = FloatField('Net Pay', validators=[DataRequired()])
    transportation_allowance = FloatField('Transportation Allowance', validators=[DataRequired()])
    submit = SubmitField('Done')