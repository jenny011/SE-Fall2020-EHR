from ehr import app
from ehr.models import *

#???? json.dumps or jsonify ????
#---------------------Home----------------------
#---------------------Home----------------------
@app.route('/')
def home():
	return render_template('WeCare.html')


#-------------------Register--------------------
#-------------------Register--------------------

@app.route('/register', methods=['POST'])
def register():
	role = request.form['registerRole']
	password = request.form['password']
	name = request.form['legalName']
	email = request.form['email']
	phone = request.form['phone']
	if role == "Doctor":
		license_id = request.form['license_id']
		try:
			doctor = Doctor.query().get(license_id)
			doctor.password = password
			doctor.name = name
			doctor.email = email
			doctor.phone = phone
			db.session.commit()
			return render_template('doctorHome', data=data)
			#return jsonify({'result': 'success'})
		except:
			return sys.exc_info()[0]
	elif role == "Nurse":
		license_id = request.form['license_id']
		try:
			nurse = Nurse.query().get(license_id)
			nurse.password = password
			nurse.name = name
			nurse.email = email
			nurse.phone = phone
			db.session.commit()
			return render_template('nurseHome', data=data)
			#return jsonify({'result': 'success'})
		except:
			return sys.exc_info()[0]
	elif role == "Patient":
		id = request.form['ID']
		address = request.form['address']
		newPatient = Patient(id, password, name, email, phone, address)
		try:
			db.session.add(newPatient)
			db.session.commit()
			return render_template('patientHome', data=data)
			#return jsonify({'result': 'success'})
		except:
			return sys.exc_info()[0]

#--------------------Login---------------------
#--------------------Login---------------------
#login_required
#authentication

@app.route('/login', methods=['POST'])
def login():
	role = request.form['role']
	id = request.form['id']
	password = request.form['password']
	user = None
	try:
		if role == "Doctor":
			user = Doctor.query().filter_by(id='', password='').one()
		elif role == "Nurse":
			user = Nurse.query().filter_by(id='', password='').one()
		elif role == "Patient":
			user = Patient.query().filter_by(id='', password='').one()
		if user:
			session['id'] = id
		return render_template('patientHome', data=data)
	except:
		return sys.exc_info()[0]
		

#--------------------Logout---------------------
#--------------------Logout---------------------

@app.route('/logout', methods=['POST'])
def logout():
	role = request.form['role']
	id = request.form['id']
	password = request.form['password']
	user = None
	try:
		if role == "Doctor":
			user = Doctor.query().filter_by(id='', password='').one()
		elif role == "Nurse":
			user = Nurse.query().filter_by(id='', password='').one()
		elif role == "Patient":
			user = Patient.query().filter_by(id='', password='').one()
		if user:
			session['id'] = id
		return jsonify({'name': user[0].name})
	except:
		return sys.exc_info()[0]
