from operator import ne
from flask import Flask, render_template, redirect, url_for, request, json, jsonify, session
from flask_login.utils import logout_user
from flask_login import login_user, logout_user, current_user
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash
# from ehr.forms import LoginForm, RegisterForm
from SE_Fall2020_EHR import app, db, login
from SE_Fall2020_EHR.models import *

@login.user_loader
def load_user(user_id): # haven't decided which identifier to use. ID or Email?
	return User.query.get(user_id)

#???? json.dumps or jsonify ????
#---------------------Home----------------------
#---------------------Home----------------------
@app.route('/')
def home():
	return render_template('index.html')

#-------------------Register--------------------
#-------------------Register--------------------

@app.route('/register', methods=['POST'])
def register():
	"""
		patient: register by (national)id
		doctor/nurse: register by (license)id
	"""
	if current_user.is_authenticated:
		return redirect(url_for(f'{current_user.role}+Home'))
	role = request.form['role']
	first_name = request.form['firstName']
	last_name = request.form['lastName']
	id = request.form['id']
	phone = request.form['phone']
	email = request.form['email']
	password = request.form['password']
	if role != "patient":
		department = request.form['department']
	# get pre-registered doctor/nurse
	user = User.query.get(id)
	if user:
		return {"error": 'Already registered!'}
	# generate random unique user_id and create new user
	user_id = str(uuid4())
	user = User(id=id, first_name=first_name, last_name=last_name, role=role, email=email, phone=phone, password_hash=generate_password_hash(password))
	db.session.add(user)
	# update corresponding table
	if role == "patient":
		patient = Patient(id=id)
		db.session.add(patient)
	elif role == "doctor":
		doctor = Doctor(id=id, department_id = department)
		db.session.add(doctor)
	elif role == "nurse":
		nurse = Nurse(id=id, department_id = department)
		db.session.add(nurse)
	db.session.commit()
	return redirect(url_for('login'))
	# except:
	# 	db.session.rollback()
	# 	print('error')
	# 	return "error"


#--------------------Login---------------------
#--------------------Login---------------------

@app.route('/login', methods=['GET','POST'])
def login():
	"""
		patient login with: national id + password
		doctor/patient login with: license id + password
	"""
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		if not current_user.is_authenticated:
			id = request.form['id']
			password = request.form['password']
			try:
				user = User.query.get(id)
				if not user or not user.check_password(password):
					flash("Unregistered ID or wrong password")
					return redirect(url_for('login'))
				login_user(user)
			except:
				flash("Unknown error, sorry!")
				return redirect(url_for('login'))
		print(type(current_user.role))
		return redirect(url_for(f'{current_user.role.value}Home'))



#--------------------Logout---------------------
#--------------------Logout---------------------

@app.route('/logout', methods=['GET','POST'])
def logout():
	print(request.method)
	logout_user()
	return redirect(url_for('home'))


#--------------------home---------------------
#--------------------home---------------------
@app.route('/patientHome', methods=['GET'])
def patientHome():
	try:
		return render_template('patientHome.html')
	except:
		return "error"
