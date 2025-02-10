from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime as dt

db=SQLAlchemy()

class User(db.Model, UserMixin):
    email =db.Column(db.String(), primary_key=True)
    password =db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active =db.Column(db.Boolean, default=True)
    fullname=db.Column(db.String(), nullable=False, unique=False)

    roles = db.relationship('Role', backref='bearers', secondary='user_roles')
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False, unique= False)
    description = db.Column(db.Text, nullable=False)


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(), db.ForeignKey('user.email'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Services(db.Model):
    service_id=db.Column(db.Integer, primary_key=True)
    service_category=db.Column(db.String(), nullable=False)
    service_name=db.Column(db.String(), nullable=False, unique=True)
    description=db.Column(db.String(), nullable=False)
    base_price=db.Column(db.Float, nullable=False)


class Service_Request(db.Model):
    __tablename__='service_request'
    request_id=db.Column(db.String(), primary_key=True)
    service_id=db.Column(db.Integer, db.ForeignKey('services.service_id'))
    customer_id=db.Column(db.String(), db.ForeignKey('user.email'), nullable=False)
    professional_id=db.Column(db.String(), db.ForeignKey('user.email'), nullable=False)
    req_date=db.Column(db.DateTime, unique=False, default=dt.utcnow)
    close_date= db.Column(db.DateTime, unique=False, default=dt.utcnow)
    status=db.Column(db.String(), default='Requested')


class Professional(db.Model):
    __tablename__='professional'
    email=db.Column(db.String(), db.ForeignKey('user.email'), primary_key=True)
    service_category=db.Column(db.String(), nullable=False)
    service_name=db.Column(db.String(), nullable=False, unique=True)
    experience=db.Column(db.Integer)
    address = db.Column(db.String(), unique=True, nullable=False)
    pin_code=db.Column(db.Integer, nullable=False)
    status=db.Column(db.String(), default="Waiting for admin approval..")    


class Customer(db.Model):
    __tablename__='customer'
    email=db.Column(db.String(), db.ForeignKey('user.email'), primary_key=True)
    address=db.Column(db.String(), nullable=False, unique=True)
    contact=db.Column(db.Integer, unique=True, nullable=False)
    pin_code=db.Column(db.Integer, nullable=False)
    status=db.Column(db.String(), default='Unblock')  

    