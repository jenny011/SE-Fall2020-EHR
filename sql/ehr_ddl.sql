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
	hospital_id varchar(20) REFERENCES hospital(id) 
	ON UPDATE CASCADE ON DELETE CASCADE,
	name varchar(100) NOT NULL,
	phone varchar(20),
	address text,
	description longtext,
	primary key (id)	
);

--Doctor
create table doctor (
	id varchar(20),
	department_id varchar(20) REFERENCES department(id)
	ON UPDATE CASCADE ON DELETE SET NULL,
	hospital_id varchar(20) REFERENCES hospital(id) 
	ON UPDATE CASCADE ON DELETE SET NULL,
	password text NOT NULL,
	name varchar(100) NOT NULL,
	email varchar(100) UNIQUE NOT NULL,
	phone varchar(20),
	address text,
	primary key (id)
);

--Nurse
create table nurse (
	id varchar(20),
	department_id varchar(20) REFERENCES department(id)
	ON UPDATE CASCADE ON DELETE SET NULL,
	hospital_id varchar(20) REFERENCES hospital(id) 
	ON UPDATE CASCADE ON DELETE SET NULL,
	password text NOT NULL,
	name varchar(100) NOT NULL,
	email varchar(100) UNIQUE NOT NULL,
	phone varchar(20),
	address text,
	primary key (id)
);

--Patient
create table patient (
	id varchar(20),
	password text NOT NULL,
	name varchar(100) NOT NULL,
	email varchar(100) UNIQUE NOT NULL,
	phone varchar(20),
	address text,
	age tinyint UNSIGNED,
	gender enum('male', 'female'),
	blood type enum('A', 'B', 'O', 'AB', 'RH+', 'RH-', 'other'),
	allergies text,
	primary key (id)
);

--Time slot

--Application

--Medical record

--Prescription

--Lab repot
create table lab_report (
	id varchar(20),
	type text REFERENCES lab_report_type(id)
	ON UPDATE CASCADE,
	medical_record_id varchar(20) REFERENCES medical_record(id)
	ON UPDATE CASCADE,
	uploader_id varchar(20) REFERENCES nurse(id)
	ON UPDATE CASCADE,
	patient_id varchar(20) REFERENCES patient(id)
	ON UPDATE CASCADE,
	file longblob,
	comments longtext,
	primary key (id)
);

--Lab report type
create table lab_report_type (
	type text,
	description longtext,
	primary key (type)
);
