from paysheet_pack import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Company.query.get(int(user_id))

class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    employees = db.relationship('Employeeinfo', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.company_name}', '{self.email}', '{self.image_file}')"

class Employeeinfo(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), default=None)
    id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company_id = db.Column(db.Integer,nullable=False)
    phone = db.Column(db.Integer)
    growth_earning = db.Column(db.Float, nullable=True, default=0.0)
    basic_salary = db.Column(db.Float, nullable=True, default=0.0)
    overtime = db.Column(db.Float, nullable=True, default=0.0)
    in_time = db.Column(db.String(50), nullable=True, default=0.0)
    out_time = db.Column(db.String(50), nullable=True, default=0.0)
    other = db.Column(db.String(50), nullable=True, default=0.0)
    duration = db.Column(db.String(50), nullable=True, default=0.0)
    emp_status = db.Column(db.String(50), nullable=True, default=0.0)
    allowance = db.Column(db.Float, nullable=True, default=0.0)
    transportation_allowance = db.Column(db.Float, nullable=True, default=0.0)
    tax = db.Column(db.Float, nullable=True, default=0.0)
    pension = db.Column(db.Float, nullable=True, default=0.0)
    other_deduction = db.Column(db.Float, nullable=True, default=0.0)
    total_deduction = db.Column(db.Float, nullable=True, default=0.0)
    net_pay = db.Column(db.Float, default=None)

class TaxEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    min_pay = db.Column(db.Float, nullable=True, default=None)
    max_pay = db.Column(db.Float, nullable=True, default=None)
    tax_rate = db.Column(db.Float, nullable=True, default=None)
    tax_deduction = db.Column(db.Float, nullable=True, default=0.0)
    pension = db.Column(db.Float, nullable=True, default=None)
    employee_id = db.Column(db.Integer, db.ForeignKey('employeeinfo.emp_id'), nullable=False)

    def __repr__(self):
        return f"<TaxEntry id={self.id}, Min Pay={self.min_pay}, Max Pay={self.max_pay}, Tax Rate={self.tax_rate}, Pension={self.pension}>"
    
class OvertimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_time = db.Column(db.Float, nullable=True, default=0.0)
    out_time = db.Column(db.Float, nullable=True, default=0.0)
    other = db.Column(db.String(50), nullable=True, default=0.0)
    ov_rate = db.Column(db.Float, nullable=True, default=0.0)
    employee_id = db.Column(db.Integer, db.ForeignKey('employeeinfo.emp_id'), nullable=False)

    def __repr__(self):
        return f"<TaxEntry id={self.id}, In Time={self.in_time}, Out Time={self.out_time}, Overtime Rate={self.ov_rate}>"

