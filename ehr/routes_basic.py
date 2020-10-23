from __main__ import app
from models import *

#???? json.dumps or flask.jsonify ????
#---------------------Home----------------------
#---------------------Home----------------------
# used for testing for now
@app.route('/')
def test():
	results = Hospital.query.all()
	return str(results[0])


#-------------------Register--------------------
#-------------------Register--------------------

@app.route('/registerDoctor', methods=['POST'])
def registerDoctor():
	newDoctor = Doctor()
	return ''

@app.route('/registerNurse', methods=['POST'])
def registerNurse():
	newNurse = Nurse()
	return ''

@app.route('/registerPatient', methods=['POST'])
def registerPatient():
	newPatient = Patient()
	return ''


#--------------------Login---------------------
#--------------------Login---------------------

@app.route('/loginDoctor', methods=['POST'])
def loginDoctor():
	results = Doctor.query().filter_by(email='', password='').all()
	return ''

@app.route('/loginNurse', methods=['POST'])
def loginNurse():
	results = Nurse.query().filter_by(email='', password='').all()
	return ''

@app.route('/loginPatient', methods=['POST'])
def loginPatient():
	results = Patient.query().filter_by(email='', password='').all()
	return ''
