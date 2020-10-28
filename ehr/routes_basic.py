from operator import ne
from flask.helpers import url_for
from flask_login.utils import logout_user
from ehr import app
from ehr.models import *
from flask import render_template, request, redirect, flash, session
from flask_login import login_user, logout_user
from ehr.forms import LoginForm, RegisterForm
from ehr import app, db

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

	# role = request.form['registerRole']
	# password = request.form['password']
	# name = request.form['legalName']
	# email = request.form['email']
	# phone = request.form['phone']
	# if role == "Doctor":
	# 	license_id = request.form['license_id']
	# 	try:
	# 		doctor = Doctor.query().get(license_id)
	# 		doctor.password = password
	# 		doctor.name = name
	# 		doctor.email = email
	# 		doctor.phone = phone
	# 		db.session.commit()
	# 		return render_template('doctorHome', data=data)
	# 		#return jsonify({'result': 'success'})
	# 	except:
	# 		return sys.exc_info()[0]

	# elif role == "Nurse":
	# 	license_id = request.form['license_id']
	# 	try:
	# 		nurse = Nurse.query().get(license_id)
	# 		nurse.password = password
	# 		nurse.name = name
	# 		nurse.email = email
	# 		nurse.phone = phone
	# 		db.session.commit()
	# 		return render_template('nurseHome', data=data)
	# 		#return jsonify({'result': 'success'})
	# 	except:
	# 		return sys.exc_info()[0]

	# elif role == "Patient":
	# 	id = request.form['ID']
	# 	address = request.form['address']
	# 	newPatient = Patient(id, password, name, email, phone, address)
	# 	try:
	# 		db.session.add(newPatient)
	# 		db.session.commit()
	# 		return render_template('patientHome', data=data)
	# 		#return jsonify({'result': 'success'})
	# 	except:
	# 		return sys.exc_info()[0]


	# another possible style of coding
	form = RegisterForm()
	if form.validate_on_submit():
		flash(f'Register for a {form.role.data} with id: {form.id.data}')
		user = User(	
					id=form.id.data, 
					email=form.email.data, 
					role=form.role.data,
					first_name = form.first_name.data,
					last_name = form.last_name.data,
					phone = form.phone.data				
				)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Welcome to the family!")
		return redirect(url_for('login'))
	return render_template('register.html', form=form)
		
		
#--------------------Login---------------------
#--------------------Login---------------------

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		flash(f'Login for a {form.role.data} with id: {form.id.data}')
		## Since we have a whole table(总表), we no longer need to specify which role table to query.
		## Instead, we only need to query the User Table.
		# user_role = form.role.data
		# if user_role == "doctor":
		# 	user = Doctor.query.filter_by(id = form.id.data).first()
		# elif user_role == 'nurse':
		# 	user = Nurse.query.filter_by(id = form.id.data).first()
		# elif user_role == 'patient':
		# 	user = Patient.query.filter_by(id=form.id.data).first()
		# else:
		# 	user = None
		user = User.query.filter_by(id=form.id.data).first()
		if not user or not user.check_password(form.password.data):
			flash("Invalid ID or unmatched Password")
			return redirect(url_for('login'))
		
		# session['role_type'] = form.role.data
		login_user(user) # current_user becomes user
		return redirect(url_for(f'{user.role}+Home'))

	return render_template('/login.html', form=form)
		

#--------------------Logout---------------------
#--------------------Logout---------------------

@app.route('/logout', methods=['POST'])
def logout():
	logout_user()
	return redirect(url_for('login'))
