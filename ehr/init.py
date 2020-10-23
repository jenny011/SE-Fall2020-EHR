from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# dialect + connector
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/wecare"
db = SQLAlchemy(app)

# import building blocks
import routes_basic, models

if __name__ == '__main__':
	print("starting ehr system...")
	app.run(debug=True)