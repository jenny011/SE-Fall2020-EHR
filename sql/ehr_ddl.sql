--Hospital
create table hospital (
	id varchar(20),
	name varchar(100) NOT NULL,
	phone varchar(20),
	address text NOT NULL,
	description longtext,
	primary key (id)
);

--Department
create table department (
	id varchar(20) NOT NULL,
	hospital_id varchar(20),
	name varchar(100) NOT NULL,
	phone varchar(20),
	address text,
	description longtext,
	foreign key (hospital_id) references hospital(id)
);

--Doctor
create table doctor (
	id varchar(20),
	department_id varchar(20),
	password text NOT NULL,
	name varchar(100) NOT NULL,
	phone varchar(20),
	address text,
	primary key (id),
	foreign key (department_id) references department(id)
);

--Nurse

--Patient

--Time slot
create table time_slot (
	time_slot_id varchar(20),
	doctor_id varchar(20),
	date date NOT NULL,
	time time NOT NULL,
	n_total int NOT NULL,
	n_booked int DEFAULT 0 ,
	primary key( time_slot_id),
	foreign key (doctor_id) references doctor(doctor_id)
);
--Application-Appointment
create table application (
	appt_id varchar(20),
	time_slot_id varchar(20),
	doctor_id varchar(20),
	approver_id varchar(20),
	patient_id varchar(20),
	timestamp timestamp,
	symptoms text,
	status enum(approved, rejected, pending, ended) NOT NULL,
	reject_reason text NOT NULL,
	primary key(appt_id),
	foreign key(time_slot_id) references time_slot(time_slot_id),
	foreign key(doctor_id) references doctor(doctor_id),
	foreign key(approver_id) references nurse(nurse_id),
	foreign key(patient_id) references patient(patient_id)
);
--Medical record
create table medical_record (
	mc_id varchar(20),
	patient_id varchar(20),
	appt_id varchar(20),
	nurse_id varchar(20),
	body_temperature float,
	body_pressure int,
	heart_rate int,
	weight float,
	state enum(conscious, coma),

	primary key(record)
	foreign key(appt_id) references application(appt_id),
	foreign key(nurse_id) references nurse(nurse_id),
	foreign key(patient_id) references patient(patient_id)
);
--Prescription
create table prescription (
	prescription_id varchar(20),
	mc_id varchar(20),
	medicine text,
	dose text,
	comment text,

	primary key(prescription_id),
	foreign key(mc_id) references(medical_record(mc_id))
);
--Lab repot

--Lab report type
