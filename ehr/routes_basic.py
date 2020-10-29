from operator import ne
from flask import Flask, render_template, redirect, url_for, request, json, jsonify, session
from flask.helpers import flash
# from flask_login.utils import logout_user
from flask_login import login_user, logout_user, current_user
from uuid import uuid4
# from ehr.forms import LoginForm, RegisterForm
from ehr import app, db, login
from ehr.models import *

@login.user_loader
def load_user(user_id): # user_id != national_id != license_id
	return User.query.get(user_id)

#---------------------Home----------------------
#---------------------Home----------------------
@app.route('/')
def home():
	return render_template('WeCare.html')

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
	id = request.form['id']
	first_name = request.form['firstName']
	last_name = request.form['lastName']
	email = request.form['email']
	phone = request.form['phone']
	password = request.form['password']

	try:
		# get pre-registered doctor/nurse
		if role == "doctor":
			doctor = Doctor.query.get(id)
			if not doctor:
				return {"error": "No pre-registered by admin"}
			# if already owned a user_id, prevent them from obtaining a new one
			elif doctor and doctor.user_id:
				return {"error": 'Already registered!'}
		elif role == "nurse":
			nurse = Nurse.query.get(id)
			if not nurse:
				return {"error": "No pre-registered by admin"}
			# if already owned a user_id, prevent them from obtaining a new one
			elif nurse and nurse.user_id:
				return {"error": 'Already registered!'}
		elif role == "patient":
			patient = Patient.query.get(id)
			# if already exist, prevent from register again
			if patient:
				return {"error": 'Already registered!'}

		# generate random unique user_id and create new user
		user_id = uuid4()
		user = User(user_id, first_name, last_name, role, email, phone)
		user.set_password(password)

		# update corresponding table
		if role == "patient":
			patient = Patient(id, user_id)
			db.session.add(patient)
		elif role == "doctor" or role == 'nurse':
			# update pre-registered info
			eval(role).user_id = user_id

		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	except:
		db.session.rollback()
		print(sys.exc_info()[0])
		return sys.exc_info()[0]

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
			password = request.form['password']
			try:
				user = User.query.one(id)
				if not user or not user.check_password(password):
					flash("Unregistered ID or wrong password")
					return redirect(url_for('login'))
				login_user(user)
			except:
				flash("Unknown error, sorry!")
				return redirect(url_for('login'))
		return redirect(url_for(f'{current_user.role}+Home'))

#--------------------Logout---------------------
#--------------------Logout---------------------

@app.route('/logout', methods=['POST'])
def logout():
	"""
	logout the system
	"""
	logout_user()
	return redirect(url_for('home'))
