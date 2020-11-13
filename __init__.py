from flask import Flask, render_template, redirect, url_for, request, json, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
# dialect + connector
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secretkey"
login = LoginManager(app)
login.login_view = 'login' # force user to login
login.login_message = "Please login first"

try:
	app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://SE:mysql@8.129.182.214:3306/wecare"
	db = SQLAlchemy(app)
except:
	app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@127.0.0.1/wecare"
	db = SQLAlchemy(app)

if __name__ == '__main__':
	print("starting ehr system...")
	app.run(debug=True, host='127.0.0.1', port=9874)

# import building blocks
from SE_Fall2020_EHR import routes_basic, models
db.create_all()
db.session.commit()
