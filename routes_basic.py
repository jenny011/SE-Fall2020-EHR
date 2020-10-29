from operator import ne
from flask import Flask, render_template, redirect, url_for, request, json, jsonify, session
from flask_login.utils import logout_user
from flask_login import login_user, logout_user, current_user
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash
# from ehr.forms import LoginForm, RegisterForm
from SE_Fall2020_EHR import app, db, login
from SE_Fall2020_EHR.models import *
import sys

@login.user_loader
def load_user(user_id): # haven't decided which identifier to use. ID or Email?
	return User.query.get(user_id)

#???? json.dumps or jsonify ????
#---------------------Home----------------------
#---------------------Home----------------------
@app.route('/')
def home():
	return render_template('WeCare.html')

# @app.route('/goToLogin')
# def goToLogin():
# 	return render_template('login.html')

#-------------------Register--------------------
#-------------------Register--------------------

@app.route('/register', methods=['POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for(f'{user.role}+Home'))
	role = request.form['role']
	first_name = request.form['firstName']
	last_name = request.form['lastName']
	id = request.form['id']
	phone = request.form['phone']
	email = request.form['email']
	password = request.form['password']
	# try:
		# get pre-registered doctor/nurse
	if role == "doctor":
		doctor = Doctor.query.get(id)
		if not doctor:
			return ""
	elif role == "nurse":
		nurse = Nurse.query.get(id)
		if not nurse:
			return ""
	# generate random unique user_id and create new user
	user_id = str(uuid4())
	user = User(user_id=user_id, first_name=first_name, last_name=last_name, role=role, email=email, phone=phone, password_hash=generate_password_hash(password))
	db.session.add(user)
	db.session.commit()
	# update corresponding table
	if role == "patient":
		patient = Patient(national_id=id, user_id=user_id)
		db.session.add(patient)
		db.session.commit()
	elif role == "doctor":
		doctor.user_id = user_id
	elif role == "nurse":
		nurse.user_id = user_id
	return redirect(url_for('login'))
	# except:
	# 	db.session.rollback()
	# 	print('error')
	# 	return "error"


	# another possible style of coding
	# form = RegisterForm()
	# if form.validate_on_submit():
	# 	flash(f'Register for a {form.role.data} with id: {form.id.data}')
	# 	user = User(
	# 				id=form.id.data,
	# 				email=form.email.data,
	# 				role=form.role.data,
	# 				first_name = form.first_name.data,
	# 				last_name = form.last_name.data,
	# 				phone = form.phone.data
	# 			)
	# 	user.set_password(form.password.data)
	# 	db.session.add(user)
	# 	db.session.commit()
	# 	flash("Welcome to the family!")
	# 	return redirect(url_for('login'))
	# return render_template('register.html', form=form)


#--------------------Login---------------------
#--------------------Login---------------------
#login_required
#authentication

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		if not current_user.is_authenticated:
			email = request.form['email']
			password = request.form['password']
			# try:
			user = User.query.one(id)
			match = user.check_password(password)
			if not match:
				return redirect(url_for('login'))
			login_user(user)
			# except:
				# return redirect(url_for('login'))
		return redirect(url_for(f'{user.role}+Home'))

	# return render_template('/login.html', form=form)

	# form = LoginForm()
	# if form.validate_on_submit():
	# 	flash(f'Login for a {form.role.data} with id: {form.id.data}')
	# 	user = User.query.filter_by(id=form.id.data).first()
	# 	if not user or not user.check_password(form.password.data):
	# 		flash("Invalid ID or unmatched Password")
	# 		return redirect(url_for('login'))
	#
	# 	# session['role_type'] = form.role.data
	# 	login_user(user) # current_user becomes user
	# 	return redirect(url_for(f'{user.role}+Home'))


#--------------------Logout---------------------
#--------------------Logout---------------------

@app.route('/logout', methods=['POST'])
def logout():
	logout_user()
	return redirect(url_for('/'))