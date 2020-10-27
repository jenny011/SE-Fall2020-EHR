# from __main__ import db
from collections import UserList
from ehr import db

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
	name = db.Column(db.String(100), nullable=False)
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
		return f'Department < id: {self.id}, name: {self.name}, \
			phone: {self.phone}, address: {self.address}, description: {self.description}\
				hospital_id: {self.hospital_id} >'


class Doctor(db.Model):
	license_id = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(20))
	#foreign key
	department_id = db.Column(db.String(20), \
		db.ForeignKey('department.id'), nullable=False)
	hospital_id = db.Column(db.String(20),\
		db.ForeignKey("hospital.id"), nullable=False)
	#one-to-many relationship
	time_slots = db.relationship('Time_slot', backref='doctor', lazy=True)
	applications = db.relationship('Application', backref='doctor', lazy=True)

	def __repr__(self):
		return f'Doctor < id: {self.id}, name: {self.name}, \
			phone: {self.phone}, email: {self.email}, address: {self.address}, description: {self.description}\
				department_id: {self.department_id}, hospital_id: {self.hospital_id} >'

class Nurse(db.Model):
	license_id = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(20))
	#foreign key
	department_id = db.Column(db.String(20), \
		db.ForeignKey('department.id'), nullable=False)
	#one-to-many relationship
	applications = db.relationship('Application', backref='nurse', lazy=True)
	medical_records = db.relationship('Medical_record', backref='nurse', lazy=True)
	lab_reports = db.relationship('Lab_report', backref='nurse', lazy=True)

	def __repr__(self):
		return f'Nurse < id: {self.id}, name: {self.name}, \
			phone: {self.phone}, email: {self.email}, address: {self.address}, \
				department_id: {self.department_id}, hospital_id: {self.hospital_id} >'

class Patient(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(20))
	address = db.Column(db.Text())
	age = db.Column(db.SmallInteger())
	gender = db.Column(db.Enum('male', 'female'))
	blood_type = db.Column(db.String(10))
	allergies = db.Column(db.Text())
	#one-to-many relationship
	applications = db.relationship('Application', backref='patient', lazy=True)
	medical_records = db.relationship('Medical_record', backref='patient', lazy=True)
	lab_reports = db.relationship('Lab_report', backref='patient', lazy=True)


class Time_slot(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	slot_date = db.Column(db.DateTime(), nullable=False)
	slot_time = db.Column(db.DateTime(), nullable=False)
	n_total = db.Column(db.Integer(), nullable=False)
	n_booked = db.Column(db.Integer())
	#foreign key
	doctor_id = db.Column(db.String(20), \
		db.ForeignKey('doctor.id'), nullable=False)
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
		db.ForeignKey('doctor.id'), nullable=False)
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
