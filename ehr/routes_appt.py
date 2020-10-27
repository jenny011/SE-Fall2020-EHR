from ehr import app
from ehr.models import *
from date import datetime

#--------------------Time slot and appointment---------------------
#--------------------Time slot and appointment---------------------

@app.route('/doctorTimeslot', methods=['GET','POST'])
def doctorTimeslot():
	try:
		return jsonify({'name': results[0].name})
	except:
		return 


@app.route('/appointmentApp', methods=['POST'])
def appointmentApp():
	symptoms = request.form['symptoms']
	doctor_id = request.form['doctor_id']
	slot_id = request.form['slot_id']
	patient_id = session[]
	try:
		id =
		timestamp = datetime.now()
		newApp = Application(id, timestamp, symptoms, 'pending', None, slot_id, doctor_id, None, patient_id)
		db.session.add(newApp)
		db.commit()
		return 'submitted'
	except:
		return render_template('application.html', error='application failed')

@app.route('/applicationProcess', methods=['POST'])
def applicationProcess():
	app_id = request.form['app_id']
	response = request.form['response']
	reason = request.form['reject_reason']
	try:
		return
	except:
		return render_template('applicationProcess.html', error='applicationProcess failed')

@app.route('/selectHospital')
def selectHospital():
	
