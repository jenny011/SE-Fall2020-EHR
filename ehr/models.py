from __main__ import db

class Hospital(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __repr__(self):
    	return "Hospital < id: {0}, name: {1}, \
    		phone: {2}, address: {3}, description: {4} >"\
    		.format(self.id, self.name, self.phone, self.address, self.description)


class Department(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Doctor(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Nurse(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Patient(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Time_slot(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Application(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Medical_record(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Prescription(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass


class Lab_report_type(db.Model):
	type = db.Column(db.String(20), primary_key=True)
	pass


class Lab_report(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	pass

