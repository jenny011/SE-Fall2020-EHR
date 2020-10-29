from ehr import app
from ehr.models import *


#-------------------Homepages--------------------
#-------------------Homepages--------------------

@app.route('/doctorHome', methods=['POST'])
def doctorHome():
	pass
	# try:
	#
	# 	return redirect(url_for('/login'))
	# except:
	# 	return sys.exc_info()[0]

@app.route('/nurseHome', methods=['POST'])
def nurseHome():
	pass
	# try:
	# 	return redirect(url_for('/login'))
	# except:
	# 	return sys.exc_info()[0]

@app.route('/patientHome', methods=['POST'])
def patientHome():
	pass
	# try:
	# 	return redirect(url_for('/login'))
	# except:
	# 	return sys.exc_info()[0]
