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
			return jsonify({'result': 'success'})
			#return redirect(url_for('/login'))
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
			return jsonify({'result': 'success'})
			#return redirect(url_for('/login'))
		except:
			return sys.exc_info()[0]
	elif role == "Patient":
		id = request.form['ID']
		address = request.form['address']
		newPatient = Patient(id, password, name, email, phone, address)
		try:
			db.session.add(newPatient)
			db.session.commit()
			return jsonify({'result': 'success'})
			#return redirect(url_for('/login'))
		except:
			return sys.exc_info()[0]

#--------------------Login---------------------
#--------------------Login---------------------

@app.route('/login', methods=['POST'])
def login():
	role = request.form['role']
	email = request.form['email']
	password = request.form['password']
	try:
		results = None
		if role == "Doctor":
			results = Doctor.query().filter_by(email='', password='').one()
			return jsonify({'name': results[0].name})
		elif role == "Nurse":
			results = Nurse.query().filter_by(email='', password='').one()
			return jsonify({'name': results[0].name})
		elif role == "Patient":
			results = Patient.query().filter_by(email='', password='').one()
			return jsonify({'name': results[0].name})
	except:
		return render_template('login.html', error='login failed')
