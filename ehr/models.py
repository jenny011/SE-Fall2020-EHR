# from __main__ import db
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
		return "Hospital < id: {0}, name: {1}, \
			phone: {2}, address: {3}, description: {4} >"\
			.format(self.id, self.name, self.phone, self.address, self.description)


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


class Doctor(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(20))
	address = db.Column(db.Text())
	#foreign key
	department_id = db.Column(db.String(20), \
		db.ForeignKey('department.id'), nullable=False)
	#one-to-many relationship
	time_slots = db.relationship('Time_slot', backref='doctor', lazy=True)
	applications = db.relationship('Application', backref='doctor', lazy=True)


class Nurse(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(20))
	address = db.Column(db.Text())
	#foreign key
	department_id = db.Column(db.String(20), \
		db.ForeignKey('department.id'), nullable=False)
	#one-to-many relationship
	applications = db.relationship('Application', backref='nurse', lazy=True)
	medical_records = db.relationship('Medical_record', backref='nurse', lazy=True)
	lab_reports = db.relationship('Lab_report', backref='nurse', lazy=True)


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
	#one-to-many relationship
	medical_records = db.relationship('Medical_record', backref='application', lazy=True)


class Medical_record(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	body_temperature = db.Column(db.Float(1))
	body_pressure = db.Column(db.Float(1))
	heart_rate = db.Column(db.Integer())
	weight = db.Column(db.Float(1))
	state = db.Column(db.Enum('conscious', 'coma'))
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


class Prescription(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	medicine = db.Column(db.Text())
	dose = db.Column(db.Text())
	comments = db.Column(db.Text())
	#foreign key
	mc_id = db.Column(db.String(20), \
		db.ForeignKey('medical_record.id'), nullable=False)


class Lab_report_type(db.Model):

	type = db.Column(db.String(50), primary_key=True)
	description = db.Column(db.Text())
	#one-to-many relationship
	lab_reports = db.relationship('Lab_report', backref='lab_report_type', lazy=True)


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

