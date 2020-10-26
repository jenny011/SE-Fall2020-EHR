from ehr import app
from ehr.models import *

#-------------------Homepages--------------------
#-------------------Homepages--------------------

@app.route('/doctorHome', methods=['POST'])
def doctorHome():

	try:
		db.session.add(newDoctor)
		db.session.commit()
		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]

@app.route('/nurseHome', methods=['POST'])
def nurseHome():
	try:
		db.session.add(newNurse)
		db.session.commit()
		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]

@app.route('/patientHome', methods=['POST'])
def patientHome():
	try:
		db.session.add(newPatient)
		db.session.commit()
		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]
