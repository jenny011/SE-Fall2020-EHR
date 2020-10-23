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

--Application

--Medical record

--Prescription

--Lab repot

--Lab report type
