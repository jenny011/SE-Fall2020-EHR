from inspect import indentsize
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from ehr import db
from flask import session
from flask_login import UserMixin # UserMixin conains four useful login function 
								  # [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins]
from ehr import login
import enum
from sqlalchemy import Enum

@login.user_loader
def load_user(identifier): # haven't decided which identifier to use. ID or Email?
	role_type = session.get('role_type')
	if role_type == "Doctor":
		return Doctor.query.get(identifier) 
	elif role_type == 'Nurse':
		return Nurse.query.get(identifier)
	elif role_type == 'Patient':
		return Patient.query.get(identifier)

class Hospital(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	phone = db.Column(db.String(20))
	address = db.Column(db.Text(), nullable=False)
	description = db.Column(db.Text())
	#one-to-many relationship
	departments = db.relationship('Department', backref='hospital', lazy=True)

	def __repr__(self):
		return f'Hospital < id: {self.id}, name: {self.name}, \
			phone: {self.phone}, address: {self.address}, description: {self.description} >'


class Department(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	phone = db.Column(db.String(20))
	address = db.Column(db.Text())
	description = db.Column(db.Text())
	#foreign key
	hospital_id = db.Column(db.String(20), \
		db.ForeignKey('hospital.id'), nullable=False)
	#one-to-many relationship
	doctors = db.relationship('Doctor', backref='department', lazy=True)
	nurses = db.relationship('Nurse', backref='department', lazy=True)

	def __repr__(self):
		return f'Department < id: {self.id}, name: {self.first_name + self.last_name}, \
			phone: {self.phone}, address: {self.address}, description: {self.description}\
				hospital_id: {self.hospital_id} >'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

# Enum Type example reference :
# https://stackoverflow.com/questions/58049679/can-i-have-array-enum-column-with-flask-sqlalchemy
class RoleEnum(enum.Enum):
	doctor = "doctor"
	nurse = "nurse"
	patient = "patient"
	admin = "admin"

class User(UserMixin, db.Model):
	id = db.Column(db.String(20), primary_key=True)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	role = db.Column(db.Enum(RoleEnum), nullable=False) # should we set a default role? default=RoleEnum.patient
	password_hash = db.Column(db.String(120))
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(20))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Doctor(db.Model):

	#foreign key
	license_id = license_id = db.Column(db.String(20),
							            db.ForeignKey('user.id'), 
										primary_key=True)

	department_id = db.Column(db.String(20),\
		db.ForeignKey('department.id'), nullable=False)
	hospital_id = db.Column(db.String(20),\
		db.ForeignKey("hospital.id"), nullable=False)
	
	#one-to-many relationship
	time_slots = db.relationship('Time_slot', backref='doctor', lazy=True)
	applications = db.relationship('Application', backref='doctor', lazy=True)


	def __repr__(self):
		return f'Doctor < license_id: {self.license_id} >'


class Nurse(db.Model):
	
	#foreign key
	department_id = db.Column(db.String(20), \
		db.ForeignKey('department.id'), nullable=False)
	license_id = db.Column(db.String(20),
				           db.ForeignKey('user.id'), 
						   primary_key=True)
	#one-to-many relationship
	applications = db.relationship('Application', backref='nurse', lazy=True)
	medical_records = db.relationship('Medical_record', backref='nurse', lazy=True)
	lab_reports = db.relationship('Lab_report', backref='nurse', lazy=True)

	def __repr__(self):
		return f'Nurse < id: {self.license_id} >'

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class GenderEnum(enum.Enum):
	male = 'male'
	female = 'female'

class Patient(db.Model):

	age = db.Column(db.SmallInteger())
	gender = db.Column(db.Enum(GenderEnum))
	blood_type = db.Column(db.String(10))
	allergies = db.Column(db.Text())

	# foreign key
	id = db.Column(db.String(20), db.ForeignKey('user.id'), primary_key=True)
	#one-to-many relationship
	applications = db.relationship('Application', backref='patient', lazy=True)
	medical_records = db.relationship('Medical_record', backref='patient', lazy=True)
	lab_reports = db.relationship('Lab_report', backref='patient', lazy=True)
		

	def __repr__(self):
		return f'Patient < id: {self.id} >'

class Time_slot(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	slot_date = db.Column(db.DateTime(), nullable=False)
	slot_time = db.Column(db.DateTime(), nullable=False)
	n_total = db.Column(db.Integer(), nullable=False)
	n_booked = db.Column(db.Integer())
	#foreign key
	doctor_id = db.Column(db.String(20), \
		db.ForeignKey('doctor.license_id'), nullable=False)
	#one-to-many relationship
	applications = db.relationship('Application', backref='time_slot', lazy=True)

	def __repr__(self):
		return f'Time_slot < id: {self.id}, slot_date: {self.slot_date}, \
			slot_time: {self.slot_time}, n_total: {self.n_total}, n_booked: {self.n_booked}, \
				doctor_id: {self.doctor_id} >'
		
class Application(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	app_timestamp = db.Column(db.TIMESTAMP())
	symptomps = db.Column(db.Text())
	status = db.Column(db.Enum('approved', 'rejected', 'pending', 'finished'), nullable=False)
	reject_reason = db.Column(db.Text())
	#foreign key
	time_slot_id = db.Column(db.String(20), \
		db.ForeignKey('time_slot.id'), nullable=False)
	doctor_id = db.Column(db.String(20), \
		db.ForeignKey('doctor.license_id'), nullable=False)
	approver_id = db.Column(db.String(20), \
		db.ForeignKey('nurse.id'), nullable=False)
	patient_id = db.Column(db.String(20), \
		db.ForeignKey('patient.id'), nullable=False)
	#one-to-one relationship
	medical_record = db.relationship('Medical_record', backref='application', uselist=False ,lazy=True)

	def __repr__(self):
		return f'Application < id: {self.id}, app_timestamp: {self.app_timestamp}, \
			status: {self.status}, time_slot_id: {self.time_slot_id}, approver_id: {self.approver_id}, \
				doctor_id: {self.doctor_id}, patient_id: {self.patient_id} >'

class Medical_record(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	body_temperature = db.Column(db.Float(1))
	body_pressure = db.Column(db.Float(1))
	heart_rate = db.Column(db.Integer())
	weight = db.Column(db.Float(1))
	state = db.Column(db.Enum('conscious', 'coma'), default="conscious")
	#foreign key
	patient_id = db.Column(db.String(20), \
		db.ForeignKey('patient.id'), nullable=False)
	appt_id = db.Column(db.String(20), \
		db.ForeignKey('application.id'), nullable=False)
	nurse_id = db.Column(db.String(20), \
		db.ForeignKey('nurse.id'), nullable=False)
	#one-to-many relationship
	lab_reports = db.relationship('Lab_report', backref='medical_record', lazy=True)
	prescription = db.relationship('Prescription', backref='medical_record', lazy=True)

	def __repr__(self):
		return f'Medical_record < id: {self.id}, appt_id: {self.appt_id}, \
			nurse_id: {self.nurse_id}, patient_id: {self.patient_id} >'

class Prescription(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	medicine = db.Column(db.Text())
	dose = db.Column(db.Text())
	comments = db.Column(db.Text())
	#foreign key
	mc_id = db.Column(db.String(20), \
		db.ForeignKey('medical_record.id'), nullable=False)

	def __repr__(self):
		return f'Prescription < id: {self.id}, mc_id: {self.mc_id} >'

class Lab_report_type(db.Model):
	type = db.Column(db.String(50), primary_key=True)
	description = db.Column(db.Text())
	#one-to-many relationship, one report type might contains sereval reports.
	lab_reports = db.relationship('Lab_report', backref='lab_report_type', lazy=True)
	def __repr__(self):
		return f'Lab_report_type < type: {self.type}, number of lab reports: {len(self.lab_reports)} >'

class Lab_report(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	file = db.Column(db.LargeBinary())
	comments = db.Column(db.Text())
	#foreign key
	type = db.Column(db.String(20), \
		db.ForeignKey('lab_report_type.type'), nullable=False)
	mc_id = db.Column(db.String(20), \
		db.ForeignKey('medical_record.id'), nullable=False)
	uploader_id = db.Column(db.String(20), \
		db.ForeignKey('nurse.id'), nullable=False)
	patient_id = db.Column(db.String(20), \
		db.ForeignKey('patient.id'), nullable=False)

	def __repr__(self):
		return f'Lab_report < id: {self.id}, (report_)type: {len(self.type)},\
			mc_id: {self.mc_id}, uploader_id: {self.uploader_id},\
				patient_id: {self.patient_id} >'
