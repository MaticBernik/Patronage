#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
conn.text_factory = str
print("***Connection to DB successful",os.getcwd())

#Patients
with open("testni_pacienti.csv","r") as patients_file: #encoding="utf8"
	patients_reader = csv.reader(patients_file, delimiter=';')
	next(patients_reader, None) #skip header
	for line in patients_reader:
		print(line)
		#passwd=hash_password(line[9])
		passwd="pbkdf2_sha256$30000$5tP0aYJfzJu2$KPakIfFZwRVWnzc8H08kFF67XMvKh1Kjbm5JqN1ucBs=" #workaround --> geslo123
		if line[0]=="da":
			conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",(line[5],line[5],line[1],line[2],passwd,True,False,False,datetime.now()));
			cursor = conn.execute("select id from auth_user where username = '"+line[5]+"';")
			id=int(cursor.fetchall()[0][0])
			conn.execute("INSERT INTO patronazna_sluzba_app_pacient (ime,priimek,naslov,st_kartice,email,telefonska_st,spol,datum_rojstva,uporabniski_profil_id) VALUES (?,?,?,?,?,?,?,?,?)", (line[1], line[2], line[3], int(line[4]), line[5], line[6], line[7], datetime.strptime(line[8], '%d.%m.%Y'), id));
		else:
			conn.execute("INSERT INTO patronazna_sluzba_app_pacient (ime,priimek,naslov,st_kartice,email,telefonska_st,spol,datum_rojstva) VALUES (?,?,?,?,?,?,?,?)", (line[1], line[2], line[3], int(line[4]), line[5], line[6], line[7], datetime.strptime(line[8], '%d.%m.%Y')));

#Medical staff
with open("testno_zdravnisko_osebje.csv","r") as staff_file: #encoding="utf8"
	staff_reader = csv.reader(staff_file, delimiter=';')
	next(staff_reader, None)  # skip header
	for line in staff_reader:
		print(line)
		conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",	(line[4], line[4], line[1], line[2], passwd, True, False, True, datetime.now()));
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

#Poste
with open("seznam_post.csv", "r") as poste_file:  #encoding="utf8"
	poste_reader = csv.reader(poste_file, delimiter=';')
	# skip header
	next(poste_reader, None)
	for line in poste_reader:
		print(line)
		conn.execute("INSERT INTO patronazna_sluzba_app_posta (postna_st, naziv_poste) VALUES (?,?)", (line[0], line[1]));

#Drugs
with open("vsa_zdravila.csv","r") as drugs_file: #encoding="utf8"
	drugs_reader = csv.reader(drugs_file, delimiter=';')
	next(drugs_reader, None)  # skip header
	for line in drugs_reader:
		print(line)
		conn.execute("INSERT INTO patronazna_sluzba_app_zdravilo (nacionalna_sifra,ime, poimenovanje, kratko_poimenovanje, oznaka_EAN, oglasevanje_dovoljeno, originator, slovenski_naziv_farmacevtske_oblike, kolicina_osnovne_enote_za_aplikacijo, oznaka_osnovne_enote_za_aplikacijo,pakiranje,sifra_pravnega_statusa,naziv_pravnega_statusa,naziv_poti_uporabe,sifra_rezima_izdaje,oznaka_rezima_izdaje,naziv_rezima_izdaje,sifra_prisotnosti_na_trgu,izdaja_na_posebni_zdravniski_recept,trigonik_absolutna_prepoved_upravljanja_vozil,trigonik_relativna_prepoved_upravljanja_vozil,omejena_kolicina_enkratne_izdaje,sifra_vrste_postopka,oznaka_vrste_postopka,naziv_vrste_postopka,oznaka_ATC,vir_podatka,slovenski_opis_ATC,latinski_opis_ATC,angleski_opis_ATC,aktivno_zdravilo,sifra_liste,oznaka_liste, opis_omejitve_predpisovanja,velja_od,sifra_iz_seznama_B,oznaka_iz_seznama_B,opis_omejitve_predpisovanja_B,velja_od_B,sifra_iz_seznama_A,oznaka_iz_seznama_A,opis_omejitve_predpisovanja_A,velja_od_A,cena_na_debelo_regulirana,datum_veljavnosti_regulirane_cene,tip_regulirane_cene,predviden_datum_konca_veljavnosti_regulirane_cene,vrsta_zdravila,dogovorjena_cena,datum_veljavnosti_dogovorjene_cene,tip_dogovorjene_cene,sifra_skupine_MZZ,opis_skupine_MZZ,najvisja_priznana_vrednost_zdravila_v_eur,datum_veljavnosti_NPV_zdravila,najvisja_priznana_vrednost_za_zivila,datum_veljavnosti_NPV_zivila,primerno_za_INN_predpisovanje,sifra_vrste_postopka,naziv_vrste_postopka,stevilka_dovoljenja,datum_dovoljenja,datum_veljavnosti_dovoljenja,stevilka_uradnega_lista_objave,datum_uradnega_lista_objave,datum_prenehanja_trzenja_zdravila,sifra_imetnika_dovoljenja,naziv_imetnika_dovoljenja,kolicina_za_preracun_DDO,DDO,oznaka_merske_enote,spletna_povezava_na_EMA,spremljanje_varnosti,sif_razp_zdr,razpolozljivost_zdravila) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(line[0], line[1], line[2],line[3], line[4], line[5],line[6], line[7], line[8],line[9],line[10], line[11], line[12],line[13], line[14], line[15],line[16], line[17], line[18],line[19],line[20], line[21], line[22],line[23], line[24], line[25],line[26], line[27], line[28],line[29],line[30], line[31], line[32],line[33], line[34], line[35],line[36], line[37], line[38],line[39],line[40], line[41], line[42],line[43], line[44], line[45],line[46], line[47], line[48],line[49],line[50], line[51], line[52],line[53], line[54], line[55],line[56], line[57], line[58],line[59],line[60], line[61], line[62],line[63], line[64], line[65],line[66], line[67], line[68],line[69],line[70], line[71], line[72],line[73], line[74]));

#Izvajalci zdravstvenih storitev
with open("izvajalci_zdravstvenih_storitev.csv", "r") as izvajalci_file:  #encoding="utf8"
	izvajalci_reader = csv.reader(izvajalci_file, delimiter=';')
	next(izvajalci_reader, None)  # skip header
	last_imported=None
	for line in izvajalci_reader:
		if not last_imported or last_imported!=line[0]:
			last_imported=line[0]
			print(line)
			posta=int(line[8][:4])
			conn.execute("INSERT INTO patronazna_sluzba_app_izvajalec_zs (st_izvajalca, naziv, naslov, posta_id) VALUES (?,?,?,?)", (line[0], line[5], line[7], posta));

#Vrste obiskov
VRSTA_PREVENTIVNI = ('Obisk nosecnice', 'Obisk otrocnice', 'Obisk novorojencka', 'Obisk starostnika')
VRSTA_KURATIVNI = ("Aplikacija inekcij", "Odvzem krvi", "Kontrola zdravstvenega stanja")
with open("TPO_Aktivnosti_patronazne_sestre.csv", "r") as vrste_obiskov_file:  #encoding="utf8"
	vrste_obiskov_reader = csv.reader(vrste_obiskov_file, delimiter=';')
	next(vrste_obiskov_reader, None)  # skip header
	last_imported = None
	for line in vrste_obiskov_reader:
		if len(line) == 5 and (last_imported==None or last_imported!=line[0]):
			last_imported=line[0]
			print(line)
			ime=line[1].replace('č','c').replace('š','s')
			if ime in VRSTA_PREVENTIVNI:
				tip="Preventivni obisk"
			else:
				tip="Kurativni obisk"
			conn.execute("INSERT INTO patronazna_sluzba_app_vrsta_obiska (sifra, ime, tip) VALUES (?,?,?)", (int(line[0]), ime, tip));

#Meritve oz. Aktivnosti
with open("TPO_Aktivnosti_patronazne_sestre.csv", "r") as aktivnosti_file:  #encoding="utf8"
	aktivnosti_reader = csv.reader(aktivnosti_file, delimiter=';')
	next(aktivnosti_reader, None)  # skip header
	for line in aktivnosti_reader:
		if len(line)==5:
			print(line)
			conn.execute("INSERT INTO patronazna_sluzba_app_meritev (vrsta_obiska_id, sifra, opis, porocilo) VALUES (?,?,?,?)", (int(line[0]), int(line[2]), line[3], line[4]));

#Okrozja
imena_okrozij_lj = ["Bežigrad","Črnuče","Mislejeva","Center","Kotnikova","Aškerčeva","Moste-Polje","Polje","Fužine","Jarše","Šentvid","Šiška","LEK","Vič-Rudnik","Rudnik","Tehnološki park","SNMP"]
imena_okrozij_mb = ["Center","Teyno in Pobrežje", "Tabor"]
imena_okrozij_nm = ["Novo mesto","Šmarjeta","Šentjernej","Žužemberk","Dolenjske Toplice","Škocjan"]
imena_okrozij_sezana = ["Sežana","Hrpelje","Divača","Dutovlje","Komen","Senožeče"]
imena_okrozij_kr = ["Brnik","Cerklje","Golnik","Iskra","Jezersko","Naklo","Preddvor","Sava Kranj","Šenčur","Stražišče"]

for okrozje in imena_okrozij_lj:
	okrozje.replace('č','c').replace('š','s')
	cursor = conn.execute("select postna_st from patronazna_sluzba_app_posta where naziv_poste = '"+okrozje+"';")
	cursor=cursor.fetchall()
	if len(cursor)>0:
		id = int(cursor[0][0])
	else:
		id=1000
	conn.execute("INSERT INTO patronazna_sluzba_app_okolis (posta_id,ime) VALUES (?,?)",	(id,okrozje));
for okrozje in imena_okrozij_mb:
	okrozje.replace('č', 'c').replace('š', 's')
	cursor = conn.execute("select postna_st from patronazna_sluzba_app_posta where naziv_poste = '"+okrozje+"';")
	cursor = cursor.fetchall()
	if len(cursor) > 0:
		id = int(cursor[0][0])
	else:
		id = 2000
	conn.execute("INSERT INTO patronazna_sluzba_app_okolis (posta_id,ime) VALUES (?,?)",	(id,okrozje));
for okrozje in imena_okrozij_nm:
	okrozje.replace('č', 'c').replace('š', 's')
	cursor = conn.execute("select postna_st from patronazna_sluzba_app_posta where naziv_poste = '"+okrozje+"';")
	cursor = cursor.fetchall()
	if len(cursor) > 0:
		id = int(cursor[0][0])
	else:
		id = 8000
	conn.execute("INSERT INTO patronazna_sluzba_app_okolis (posta_id,ime) VALUES (?,?)",	(id,okrozje));
for okrozje in imena_okrozij_sezana:
	okrozje.replace('č', 'c').replace('š', 's')
	cursor = conn.execute("select postna_st from patronazna_sluzba_app_posta where naziv_poste = '"+okrozje+"';")
	cursor = cursor.fetchall()
	if len(cursor) > 0:
		id = int(cursor[0][0])
	else:
		id = 6000
	conn.execute("INSERT INTO patronazna_sluzba_app_okolis (posta_id,ime) VALUES (?,?)",	(id,okrozje));
for okrozje in imena_okrozij_kr:
	okrozje.replace('č', 'c').replace('š', 's')
	cursor = conn.execute("select postna_st from patronazna_sluzba_app_posta where naziv_poste = '"+okrozje+"';")
	cursor = cursor.fetchall()
	if len(cursor) > 0:
		id = int(cursor[0][0])
	else:
		id = 4000
	conn.execute("INSERT INTO patronazna_sluzba_app_okolis (posta_id,ime) VALUES (?,?)",	(id,okrozje));




conn.commit()
conn.close()