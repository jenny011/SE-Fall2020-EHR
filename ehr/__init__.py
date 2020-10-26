from flask import Flask, render_template, redirect, url_for, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# dialect + connector
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/wecare"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
	print("starting ehr system...")
	app.run(debug=True)

# import building blocks
from ehr import routes_basic, models

