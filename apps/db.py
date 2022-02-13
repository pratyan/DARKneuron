import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text


import sqlite3 
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()
# DB  Functions

# Patients-------------------------------------------------------------------------------------------------------------------------
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,doctorname TEXT)')

def add_userdata(username,password,doctorname):
	c.execute('INSERT INTO userstable(username,password,doctorname) VALUES (?,?,?)',(username,password,doctorname))
	conn.commit()

def update_userdoctor(doctorname,username):
	c.execute('UPDATE userstable SET doctorname = ? WHERE username = ?',(doctorname,username))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def get_doctorname(username):
	c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
	data = c.fetchall()
	return data[0][2]
#-----------------------------------------------------------------------------------------------------------------------------------------------



#Doctor----------------------------------------------------------------------------------------------------------------------------------------------
def create_doctortable():
	c.execute('CREATE TABLE IF NOT EXISTS doctorstable(username TEXT,password TEXT,specialization TEXT,patientname TEXT)')


def add_doctordata(username,password,specialization,patientname):
    c.execute('INSERT INTO doctorstable(username,password,specialization,patientname) VALUES (?,?,?,?)',(username,password,specialization,patientname))
    conn.commit()

def update_doctorpatient(patientname,username):
	c.execute('UPDATE doctorstable SET patientname = ? WHERE username = ?',(patientname,username))
	conn.commit()


def login_doctor(username,password,specialization):
    c.execute('SELECT * FROM doctorstable WHERE username =? AND password = ? AND specialization = ?',(username,password,specialization))
    data = c.fetchall()
    return data

def get_patientname(username):
	c.execute('SELECT * FROM doctorstable WHERE username = ?',(username,))
	data = c.fetchall()
	return data[0][3]
#-----------------------------------------------------------------------------------------------------------------------------------


#Appointments---------------------------------------------------------------------------------------------
def create_appointmenttable():
	c.execute('CREATE TABLE IF NOT EXISTS appointmentstable(doctorname TEXT,patientname TEXT,date TEXT,time TEXT)')

def add_appointment(doctorname,patientname,date,time):
	c.execute('INSERT INTO appointmentstable(doctorname,patientname,date,time) VALUES (?,?,?,?)',(doctorname,patientname,date,time))
	conn.commit()

def get_appointment_patient(patientname):
	c.execute('SELECT * FROM appointmentstable WHERE patientname = ?',(patientname,))
	data = c.fetchall()
	return data[0][2],data[0][3]

def get_appointment_doctor(doctorname):
	c.execute('SELECT * FROM appointmentstable WHERE patientname = ?',(doctorname,))
	data = c.fetchall()
	return data[0][2],data[0][3]
#---------------------------------------------------------------------------------------------------------------------


def view_all_doctors():
	c.execute('SELECT * FROM doctorstable')
	data = c.fetchall()
	return data
