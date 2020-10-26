from ehr import app
from ehr.models import *

#-------------------Homepages--------------------
#-------------------Homepages--------------------

@app.route('/doctorHome', methods=['POST'])
def doctorHome():
	
	try:

		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]

@app.route('/nurseHome', methods=['POST'])
def nurseHome():
	try:

		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]

@app.route('/patientHome', methods=['POST'])
def patientHome():
	try:

		return redirect(url_for('/login'))
	except:
		return sys.exc_info()[0]
