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

@app.route('/registerDoctor', methods=['POST'])
def registerDoctor():
	name = request.form['name']
	email = request.form['email']
	phone = request.form['phone']
	address = request.form['address']
	department_id = request.form['department_id']
	id = ?
	newDoctor = Doctor(id, name, email, phone, address, department_id)
	try:
		db.session.add(newDoctor)
		db.session.commit()
		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]

@app.route('/registerNurse', methods=['POST'])
def registerNurse():
	name = request.form['name']
	email = request.form['email']
	phone = request.form['phone']
	address = request.form['address']
	department_id = request.form['department_id']
	id = ?
	newNurse = Nurse(id, name, email, phone, address, department_id)
	try:
		db.session.add(newNurse)
		db.session.commit()
		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]

@app.route('/registerPatient', methods=['POST'])
def registerPatient():
	name = request.form['name']
	national_id = request.form['national_id']
	email = request.form['email']
	phone = request.form['phone']
	address = request.form['address']
	age = request.form['age']
	gender = request.form['gender']
	id = ?
	newPatient = Patient(id, name, national_id, email, phone, address, age, gender)
	try:
		db.session.add(newPatient)
		db.session.commit()
		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]


#--------------------Login---------------------
#--------------------Login---------------------

@app.route('/loginDoctor', methods=['POST'])
def loginDoctor():
	email = request.form['email']
	password = request.form['password']
	try:
		results = Doctor.query().filter_by(email='', password='').one()
		return jsonify({'name': results[0].name})
	except:
		return render_template('login.html', error='login failed')

@app.route('/loginNurse', methods=['POST'])
def loginNurse():
	email = request.form['email']
	password = request.form['password']
	try:
		results = Nurse.query().filter_by(email='', password='').one()
		return jsonify({'name': results[0].name})
	except:
		return render_template('login.html', error='login failed')

@app.route('/loginPatient', methods=['POST'])
def loginPatient():
	email = request.form['email']
	password = request.form['password']
	try:
		results = Patient.query().filter_by(email='', password='').one()
		return jsonify({'name': results[0].name})
	except:
		return render_template('login.html', error='login failed')
