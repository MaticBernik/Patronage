#!/usr/bin/python
import sqlite3
import csv
from datetime import datetime
import os
import hashlib
import uuid
from django.utils.crypto import (pbkdf2, get_random_string)
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return "sha256"+'$1$'+salt+"$"+hashlib.sha256(salt+ password).hexdigest()

'''def hash_password(password):
	algorithm = "pbkdf2_sha256"
	iterations = 10000
	salt = 'p9Tkr6uqxKtf'
	digest = hashlib.sha256
	hash = pbkdf2(password, salt, iterations, digest=digest)
	hash = hash.encode('base64').strip()
	return "%s$%d$%s$%s" % (algorithm, iterations, salt, hash)'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
#db_path = os.path.join(BASE_DIR, "db.sqlite3")
conn = sqlite3.connect("../patronazna_sluzba_project/db.sqlite3")
print("***Connection to DB successful",os.getcwd())

#Patients
with open("testni_pacienti.csv","r", encoding="Windows-1251") as patients_file:
	patients_reader = csv.reader(patients_file, delimiter=';')
	next(patients_reader, None) #skip header
	for line in patients_reader:
		print(line)
		passwd=hash_password(line[9])
		if line[0]=="da":
			conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",(line[5],line[5],line[1],line[2],passwd,True,False,False,datetime.now()));
			cursor = conn.execute("select id from auth_user where username = '"+line[5]+"';")
			id=int(cursor.fetchall()[0][0])
			conn.execute("INSERT INTO patronazna_sluzba_app_pacient (ime,priimek,naslov,st_kartice,email,telefonska_st,spol,datum_rojstva,uporabniski_profil_id) VALUES (?,?,?,?,?,?,?,?,?)", (line[1], line[2], line[3], int(line[4]), line[5], line[6], line[7], datetime.strptime(line[8], '%d.%m.%Y'), id));
		else:
			conn.execute("INSERT INTO patronazna_sluzba_app_pacient (ime,priimek,naslov,st_kartice,email,telefonska_st,spol,datum_rojstva) VALUES (?,?,?,?,?,?,?,?)", (line[1], line[2], line[3], int(line[4]), line[5], line[6], line[7], datetime.strptime(line[8], '%d.%m.%Y')));

#Medical staff
with open("testno_zdravnisko_osebje.csv","r", encoding="Windows-1251") as staff_file:
	staff_reader = csv.reader(staff_file, delimiter=';')
	next(staff_reader, None)  # skip header
	for line in staff_reader:
		print(line)
		conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",	(line[4], line[4], line[1], line[2], line[7], True, False, True, datetime.now()));
		cursor = conn.execute("select id from auth_user where username = '" + line[4] + "';")
		id = int(cursor.fetchall()[0][0])
		if line[0]=="zdravnik":
			conn.execute("INSERT INTO patronazna_sluzba_app_zdravnik (sifra_zdravnika,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id) VALUES (?,?,?,?)", (line[3], line[5], line[6], id));
		elif line[0]=="vodja":
			conn.execute("INSERT INTO patronazna_sluzba_app_vodja_ps (sifra_vodje_ps,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id) VALUES (?,?,?,?)", (line[3], line[5], line[6], id));
		elif line[0]=="sestra":
			conn.execute("INSERT INTO patronazna_sluzba_app_patronazna_sestra (sifra_patronazne_sestre,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id,okolis_id) VALUES (?,?,?,?,?)", (line[3], line[5], line[6], id, 99));
		else: # line[0]=="sodelavec":
			conn.execute("INSERT INTO patronazna_sluzba_app_sodelavec_zd (sifra_sodelavca,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id) VALUES (?,?,?,?)", (line[3], line[5], line[6], id));

#zdravnik;Joze;Dolenc;99999;joze.dolenc@mail.si;051 111 111;00100;geslo

#Drugs
with open("vsa_zdravila.csv","r", encoding="Windows-1251") as drugs_file:
	drugs_reader = csv.reader(drugs_file, delimiter=';')
	#next(drugs_reader, None)  # skip header
	#for line in drugs_reader:
		#print(line)


conn.commit()
conn.close()