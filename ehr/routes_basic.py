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
	role = request.form['role']
	password = request.form['password']
	name = request.form['name']
	email = request.form['email']
	phone = request.form['phone']
	newUser = None
	if role == "Doctor":
		license_id = request.form['license_id']
		department_id = request.form['department_id']
		id = ?
		newUser = Doctor(id, password, name, license_id, email, phone, department_id)
	elif role == "Nurse":
		license_id = request.form['license_id']
		department_id = request.form['department_id']
		id = ?
		newUser = Nurse(id, password, name, license_id, email, phone, department_id)
	elif role == "Patient":
		national_id = request.form['ID']
		address = request.form['address']
		id = ?
		newUser = Patient(id, password, name, national_id, email, phone, address)
	try:
		db.session.add(newUser)
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
