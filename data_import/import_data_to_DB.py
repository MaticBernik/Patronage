#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import csv
from datetime import datetime,timedelta
import os
import hashlib
import uuid
import random
from django.utils.crypto import (pbkdf2, get_random_string)
def hash_password(password):
	# uuid is used to generate a random number
	salt = uuid.uuid4().hex
	return "sha256"+'$1$'+salt+"$"+hashlib.sha256(salt+ password).hexdigest()
'''def hash_password(password):
	algorithm = "pbkdf2_sha256"
SSS	iterations = 10000
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
first_names=['Jana','Ana','Anja','Andreja','Zala','Lisa','Sara','Eva','Spela','Lara','Larisa','Marko','Luka','Martina','Franja','Ursa','Andrej','Jozef','Stefan','Aleksandra','Beti','Bostjan','David','Darja','Dasa','Darinka','Emanuela','Eneja','Filip','Gaja','Gabriela','Gasper','Ian','Ivan','Igor','Iztok','Ivana','Iza','Janja','Jana','Janez','Jelka','Katarina','Karmen','Karin','Katja','Laura','Lina','Matea','Martin','Maja']
last_names=['Novak','Kovac','Savic','Bohinc','Jakopin','Kozamernik','Bostjancic','Klepec','Saje','Godler','Mlakar','Mihalic','Zavec','Zajec','Petkovsek','Trubar','Begic','Bosnic','Brankovic','Cepec','Cevljar','Copatar','Kotnik','Koprivec','Koprivnikar','Jazbinsek','Jagodnik','Jagodic','Javornik','Lancic','Sebastjancic','Zalokar','Zavrsnik','Zebnik','Pozebnik','Zelenic','Hvaljnik','Hrastnik','Topoljsek','Sobotnik','Srebernik','Hlastnik']
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
#Material
with open("material.csv", "r") as material_file:  #encoding="utf8"
	material_reader = csv.reader(material_file, delimiter=';')
	next(material_reader, None)  # skip header
	for line in material_reader:
		print(line)
		conn.execute("INSERT INTO patronazna_sluzba_app_material (ime,proizvajalec,opis,kolicina_osnovne_enote,oznaka_osnovne_enote) VALUES (?,?,?,?,?)", (line[0], line[1], line[2], line[3], line[4]));
#Patients
with open("testni_pacienti.csv","r",encoding="utf8") as patients_file: #encoding="utf8"
# with open("testni_pacienti.csv","r") as patients_file: #encoding="utf8"
	patients_reader = csv.reader(patients_file, delimiter=';')
	next(patients_reader, None) #skip header
	for line in patients_reader:
		if line[0]=='#':
			continue
		print(line)
		#passwd=hash_password(line[9])
		passwd="pbkdf2_sha256$30000$5tP0aYJfzJu2$KPakIfFZwRVWnzc8H08kFF67XMvKh1Kjbm5JqN1ucBs=" #workaround --> geslo123
		if line[0]=="da":
			conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",(line[5],line[5],line[1],line[2],passwd,True,False,False,datetime.now()));
			cursor = conn.execute("select id from auth_user where username = '"+line[5]+"';")
			id=int(cursor.fetchall()[0][0])
			cursor = conn.execute("select id from patronazna_sluzba_app_okolis where posta_id = '" + line[10] + "';")
			id_okrozje = int(cursor.fetchall()[0][0])
			conn.execute("INSERT INTO patronazna_sluzba_app_pacient (ime,priimek,naslov,st_kartice,email,telefonska_st,spol,datum_rojstva,uporabniski_profil_id,okolis_id) VALUES (?,?,?,?,?,?,?,?,?,?)", (line[1], line[2], line[3], line[4], line[5], line[6], line[7], datetime.strptime(line[8], '%d.%m.%Y'), id, id_okrozje));
		else:
			conn.execute("INSERT INTO patronazna_sluzba_app_pacient (ime,priimek,naslov,st_kartice,email,telefonska_st,spol,datum_rojstva,okolis_id) VALUES (?,?,?,?,?,?,?,?,?)", (line[1], line[2], line[3], line[4], line[5], line[6], line[7], datetime.strptime(line[8], '%d.%m.%Y'), id_okrozje));
#Skrbnistvo
with open("skrbnistvo.csv","r") as skrbnistvo_file:
	skrbnistvo_reader = csv.reader(skrbnistvo_file, delimiter=';')
	next(skrbnistvo_reader, None)
	for line in skrbnistvo_reader:
		print(line)
		cursor = conn.execute("select st_kartice from patronazna_sluzba_app_pacient where st_kartice = '" + str(line[0]) + "';")
		cursor=cursor.fetchall()
		skrbnik=None
		if len(cursor)>0:
			skrbnik=cursor[0][0]
		else:
			print("Neveljavna st. kartice skrbnika")
		cursor = conn.execute("select st_kartice from patronazna_sluzba_app_pacient where st_kartice = '" + str(line[1]) + "';")
		cursor = cursor.fetchall()
		oskrbovanec = None
		if len(cursor) > 0:
			oskrbovanec = cursor[0][0]
		else:
			print("Neveljavna st. kartice oskrbovanca")
		conn.execute("UPDATE patronazna_sluzba_app_pacient set skrbnistvo_id="+str(skrbnik)+" where st_kartice='"+str(oskrbovanec)+"';")
#Medical staff
with open("testno_zdravnisko_osebje.csv","r",encoding="utf8") as staff_file: #encoding="utf8"
# with open("testno_zdravnisko_osebje.csv","r") as staff_file: #encoding="utf8"
	staff_reader = csv.reader(staff_file, delimiter=';')
	next(staff_reader, None)  # skip header
	for line in staff_reader:
		print(line)
		if line[0]=='#':
			continue
		conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",	(line[4], line[4], line[1], line[2], passwd, True, True if (line[0]=="administrator") else False, True, datetime.now()));
		cursor = conn.execute("select id from auth_user where username = '" + line[4] + "';")
		id = int(cursor.fetchall()[0][0])
		if line[0]=="zdravnik":
			conn.execute("INSERT INTO patronazna_sluzba_app_zdravnik (sifra_zdravnika,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id) VALUES (?,?,?,?)", (line[3], line[5], line[6], id));
		elif line[0]=="vodja":
			conn.execute("INSERT INTO patronazna_sluzba_app_vodja_ps (sifra_vodje_ps,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id) VALUES (?,?,?,?)", (line[3], line[5], line[6], id));
		elif line[0]=="sestra":
			cursor = conn.execute("select id from patronazna_sluzba_app_okolis where posta_id = '" + line[8] + "';")
			id_okrozje = int(cursor.fetchall()[0][0])
			conn.execute("INSERT INTO patronazna_sluzba_app_patronazna_sestra (sifra_patronazne_sestre,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id,okolis_id) VALUES (?,?,?,?,?)", (line[3], line[5], line[6], id, id_okrozje));
		elif line[0]=="sodelavec":
			conn.execute("INSERT INTO patronazna_sluzba_app_sodelavec_zd (sifra_sodelavca,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id) VALUES (?,?,?,?)", (line[3], line[5], line[6], id));
		conn.execute("INSERT INTO patronazna_sluzba_app_uporabnik (profil_id) VALUES (?)",	(id,));
#Make sure, that every area has its nurse
email_domains=['@gmail.com','@hotmail.com','@siol.net','@arnes.si']
passwd = "pbkdf2_sha256$30000$5tP0aYJfzJu2$KPakIfFZwRVWnzc8H08kFF67XMvKh1Kjbm5JqN1ucBs="  # workaround --> geslo123
cursor = conn.execute("select id,ime,posta_id from patronazna_sluzba_app_okolis;")
okolisi = cursor.fetchall()
for okolis in okolisi:
	cursor = conn.execute("select id from patronazna_sluzba_app_patronazna_sestra where okolis_id=="+str(okolis[0])+";")
	sestre = cursor.fetchall()
	if len(sestre)==0:
		while True:
			first_name=random.choice(first_names)
			last_name=random.choice(last_names)
			email=first_name+"."+last_name+random.choice(email_domains)
			cursor = conn.execute("select id from auth_user where email='"+email+"';")
			nurse = cursor.fetchall()
			if len(nurse)==0:
				break
		while True:
			sifra = random.randint(10000,99999)
			cursor = conn.execute("select id from patronazna_sluzba_app_patronazna_sestra where sifra_patronazne_sestre="+str(sifra)+";")
			nurse=cursor.fetchall()
			if len(nurse)==0:
				break
		conn.execute("INSERT INTO auth_user (username,email,first_name,last_name,password,is_active,is_superuser,is_staff,date_joined) VALUES (?,?,?,?,?,?,?,?,?)",(email, email, first_name, last_name, passwd, True, False, True, datetime.now()));
		cursor = conn.execute("select id from auth_user where username = '" + email + "';")
		id = int(cursor.fetchall()[0][0])
		conn.execute("INSERT INTO patronazna_sluzba_app_patronazna_sestra (sifra_patronazne_sestre,telefonska_st,sifra_izvajalca_ZS_id,uporabniski_profil_id,okolis_id) VALUES (?,?,?,?,?)",	(sifra, '031 111 111', line[6], id, okolis[0]));
#Poste
with open("seznam_post.csv", "r", encoding="utf8") as poste_file:  #encoding="utf8"
# with open("seznam_post.csv", "r") as poste_file:  # encoding="utf8"
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
		# conn.execute("INSERT INTO patronazna_sluzba_app_zdravilo (nacionalna_sifra,ime, poimenovanje, kratko_poimenovanje, oznaka_EAN, oglasevanje_dovoljeno, originator, slovenski_naziv_farmacevtske_oblike, kolicina_osnovne_enote_za_aplikacijo, oznaka_osnovne_enote_za_aplikacijo,pakiranje,sifra_pravnega_statusa,naziv_pravnega_statusa,naziv_poti_uporabe,sifra_rezima_izdaje,oznaka_rezima_izdaje,naziv_rezima_izdaje,sifra_prisotnosti_na_trgu,izdaja_na_posebni_zdravniski_recept,trigonik_absolutna_prepoved_upravljanja_vozil,trigonik_relativna_prepoved_upravljanja_vozil,omejena_kolicina_enkratne_izdaje,sifra_vrste_postopka,oznaka_vrste_postopka,naziv_vrste_postopka,oznaka_ATC,vir_podatka,slovenski_opis_ATC,latinski_opis_ATC,angleski_opis_ATC,aktivno_zdravilo,sifra_liste,oznaka_liste, opis_omejitve_predpisovanja,velja_od,sifra_iz_seznama_B,oznaka_iz_seznama_B,opis_omejitve_predpisovanja_B,velja_od_B,sifra_iz_seznama_A,oznaka_iz_seznama_A,opis_omejitve_predpisovanja_A,velja_od_A,cena_na_debelo_regulirana,datum_veljavnosti_regulirane_cene,tip_regulirane_cene,predviden_datum_konca_veljavnosti_regulirane_cene,vrsta_zdravila,dogovorjena_cena,datum_veljavnosti_dogovorjene_cene,tip_dogovorjene_cene,sifra_skupine_MZZ,opis_skupine_MZZ,najvisja_priznana_vrednost_zdravila_v_eur,datum_veljavnosti_NPV_zdravila,najvisja_priznana_vrednost_za_zivila,datum_veljavnosti_NPV_zivila,primerno_za_INN_predpisovanje,sifra_vrste_postopka,naziv_vrste_postopka,stevilka_dovoljenja,datum_dovoljenja,datum_veljavnosti_dovoljenja,stevilka_uradnega_lista_objave,datum_uradnega_lista_objave,datum_prenehanja_trzenja_zdravila,sifra_imetnika_dovoljenja,naziv_imetnika_dovoljenja,kolicina_za_preracun_DDO,DDO,oznaka_merske_enote,spletna_povezava_na_EMA,spremljanje_varnosti,sif_razp_zdr,razpolozljivost_zdravila) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(line[0], line[1], line[2],line[3], line[4], line[5],line[6], line[7], line[8],line[9],"", "", "",line[13], line[14], line[15],"", "", "",line[19],line[20], line[21], line[22],line[23], line[24], line[25],line[26], line[27], line[28],line[29],line[30], line[31], line[32],line[33], line[34], line[35],line[36], line[37], line[38],line[39],line[40], line[41], line[42],line[43], line[44], line[45],line[46], line[47], line[48],line[49],line[50], line[51], line[52],line[53], line[54], line[55],line[56], line[57], "","","", line[61], line[62],line[63], line[64], line[65],line[66], line[67], line[68],line[69],line[70], line[71], line[72],line[73], line[74]));
		conn.execute("INSERT INTO patronazna_sluzba_app_zdravilo (nacionalna_sifra, ime, poimenovanje, kratko_poimenovanje, oznaka_EAN, oglasevanje_dovoljeno, originator, kolicina_osnovne_enote_za_aplikacijo, sifra_pravnega_statusa, sifra_rezima_izdaje, aktivno_zdravilo, sifra_liste, spremljanje_varnosti) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(line[0], line[1], line[2],line[3], line[4], line[5], line[6], line[8], line[11], line[14], line[30], line[31], line[72]));
#Izvajalci zdravstvenih storitev
with open("izvajalci_zdravstvenih_storitev.csv", "r", encoding="utf8") as izvajalci_file:  #encoding="utf8"
# with open("izvajalci_zdravstvenih_storitev.csv", "r") as izvajalci_file:  # encoding="utf8"
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
VRSTA_PREVENTIVNI = ('Obisk nosecnice', 'Obisk otrocnice in novorojencka', 'Preventiva starostnika', 'Obisk otrocnice', 'Obisk novorojencka')
VRSTA_KURATIVNI = ("Aplikacija injekcij", "Odvzem krvi", "Kontrola zdravstvenega stanja")
with open("TPO_Aktivnosti_patronazne_sestre.csv", "r", encoding="utf8") as vrste_obiskov_file:  #encoding="utf8"
# with open("TPO_Aktivnosti_patronazne_sestre.csv", "r") as vrste_obiskov_file:  # encoding="utf8"
	vrste_obiskov_reader = csv.reader(vrste_obiskov_file, delimiter=';')
	next(vrste_obiskov_reader, None)  # skip header
	last_imported = None
	obisk_otrocnice_novorojencka_dodan = False
	for line in vrste_obiskov_reader:
		if len(line) == 5 and (last_imported==None or last_imported!=line[0]):
			last_imported=line[0]
			print(line)
			ime=line[1].replace('č','c').replace('š','s')
			if ime=='Obisk otrocnice' or ime=='Obisk novorojencka':
				if not obisk_otrocnice_novorojencka_dodan:
					conn.execute("INSERT INTO patronazna_sluzba_app_vrsta_obiska (sifra, ime, tip) VALUES (?,?,?)", (20, 'Obisk otrocnice in novorojencka', "Preventivni obisk"));
					obisk_otrocnice_novorojencka_dodan=True
			if ime in VRSTA_KURATIVNI:
				tip = "Kurativni obisk"
			else:
				tip = "Preventivni obisk"
			if int(line[0])==20:
				conn.execute("INSERT INTO patronazna_sluzba_app_vrsta_obiska (sifra, ime, tip) VALUES (?,?,?)", (80, ime, tip));
			else:
				conn.execute("INSERT INTO patronazna_sluzba_app_vrsta_obiska (sifra, ime, tip) VALUES (?,?,?)", (int(line[0]), ime, tip));
#Meritve oz. Aktivnosti
with open("TPO_Aktivnosti_patronazne_sestre.csv", "r", encoding="utf8") as aktivnosti_file:  #encoding="utf8"
# with open("TPO_Aktivnosti_patronazne_sestre.csv", "r") as aktivnosti_file:  # encoding="utf8"
	aktivnosti_reader = csv.reader(aktivnosti_file, delimiter=';')
	next(aktivnosti_reader, None)  # skip header
	for line in aktivnosti_reader:
		if len(line)==5:
			print(line)
			sifra = int(line[2]) #sifra aktivnosti
			sifra_storitve=int(line[0]) #sifra storitve oz. vrste obiska
			if sifra_storitve==30: #zdruzi sicer locena obiska otrocnice in novorojencka
				sifra_storitve=20
				sifra+=240 #offset
			#elif sifra_storitve==20:
			#	sifra_storitve=80
			meritev_id_orig=None
			conn.execute("INSERT INTO patronazna_sluzba_app_meritev (vrsta_obiska_id, sifra, opis) VALUES (?,?,?)", (sifra_storitve, sifra, str(line[3])));
			if sifra_storitve==20:
				if int(line[0])==20:
					conn.execute("INSERT INTO patronazna_sluzba_app_meritev (vrsta_obiska_id, sifra, opis) VALUES (?,?,?)", (80, int(line[2]), str(line[3])));
					cursor = conn.execute("select id from patronazna_sluzba_app_meritev where vrsta_obiska_id=" + str(80) + " and sifra=" + str(line[2]) + ";");
				else:
					conn.execute("INSERT INTO patronazna_sluzba_app_meritev (vrsta_obiska_id, sifra, opis) VALUES (?,?,?)", (int(line[0]), int(line[2]), str(line[3])));
					cursor = conn.execute("select id from patronazna_sluzba_app_meritev where vrsta_obiska_id=" + str(line[0]) + " and sifra=" + str(line[2]) + ";");
				meritev_id_orig = cursor.fetchall()[0][0]
			cursor = conn.execute("select id from patronazna_sluzba_app_meritev where vrsta_obiska_id=" + str(sifra_storitve) + " and sifra="+ str(sifra) +";");
			meritev_id = cursor.fetchall()[0][0]
			imena_polj=line[4].split(',')
			for ime in imena_polj:
				ime=ime.strip()
				if len(ime)==0:
					continue
				obvezen_vnos = False
				if '*' in ime:
					obvezen_vnos = True
					ime = ime[0 : ime.index('*') - 1]
				mozne_vrednosti=None
				if ime=="Prosti vnos" or "prosti vnos" in ime:
					vnosno_polje="CharField"
				elif '/' in ime:
					i=ime.index('/')
					if len(ime[i-2:i].strip())>1 and len(ime[i+1:i+3].strip())>1 :
						mozne_vrednosti=','.join(ime.split('/'))
						vnosno_polje='ChoiceField'
					else:
						vnosno_polje = 'DecimalField'
				elif "Datum" in ime:
					vnosno_polje="DateField"
				else:
					vnosno_polje='DecimalField'
				print("IME: ",ime,"  VNOSNO POLJE: ",vnosno_polje)
				
				enkraten_vnos=False;
				if ime=='Prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime=='Datum':
					mozne_vrednosti='*'
					#continue
				#elif ime == 'Moteno/Ni moteno':
				#elif ime == 'Nizka/Srednja/Visoka':
				elif ime == 'Sistolični (mm Hg)':
					mozne_vrednosti='0,500'
				elif ime == 'Diastolični (mm Hg)':
					mozne_vrednosti='0,500'
				elif ime == 'Udarci na minuto':
					mozne_vrednosti='0,300'
				elif ime == 'Vdihi na minuto':
					mozne_vrednosti='0,500'
				elif ime == 'st C':
					mozne_vrednosti='0,60'
				elif ime == 'kg':
					mozne_vrednosti='1,300'
				elif ime == 'Datum rojstva otroka':
					enkraten_vnos=True
					mozne_vrednosti='*'
					#continue
					'''if len(oskrbovanci)==0:
						print("Napaka!")
						continue
					pacient_id=oskrbovanci[0]
					cursor = conn.execute("select datum_rojstva from patronazna_sluzba_app_pacient where st_kartice=" + str(
					pacient_id) +";");
					datum_rojstva=datetime.strptime(cursor.fetchall()[0][0],"%Y-%m-%d %H:%M:%S")
					izbira=datum_rojstva'''
				elif ime == 'Porodna teža otroka (g)':
					enkraten_vnos=True;
					mozne_vrednosti='0,20000'
				elif ime == 'Porodna višina otroka (cm)':
					enkraten_vnos=True
					mozne_vrednosti='10,100'
				elif ime == 'g':
					mozne_vrednosti='500,50000'
				elif ime == 'cm':
					mozne_vrednosti='10,200'
				#elif ime == 'Da/Ne':
				#elif ime == 'Ni posebnosti/Mikcija/Defekacija/Napenjanje/Kolike/Polivanje/Bruhanje':
				elif ime == 'Urin: prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime == 'Blato: prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime == 'Vid: prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime == 'Vonj: prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime == 'Sluh: prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime == 'Okus: prosti vnos':
					mozne_vrednosti='*'
					#continue
				elif ime == 'Otip: prosti vnos':
					mozne_vrednosti='*'
					#continue
				#elif ime == 'Samostojen/Delno odvisen/Povsem odvisen':
				elif ime == 'Pomoč: svojci':
					mozne_vrednosti='*'
					#continue
				elif ime == 'drugi':
					mozne_vrednosti='*'
					#continue
				elif ime =='mmol/L':
					mozne_vrednosti='0,500'
				elif ime == '%':
					mozne_vrednosti='0,100'
				#elif ime == 'Da/Delno/Ne':
				
				
				cursor = conn.execute("select id from patronazna_sluzba_app_polje_v_porocilu where ime = '" + ime + "' and vnosno_polje = '" + vnosno_polje + "';");
				polje_id=cursor.fetchall()
				if len(polje_id)==0:
					if mozne_vrednosti:
						conn.execute("INSERT INTO patronazna_sluzba_app_polje_v_porocilu (ime, vnosno_polje, obvezno, mozne_vrednosti, enkraten_vnos) VALUES (?,?,?,?,?)", (ime, vnosno_polje, obvezen_vnos, mozne_vrednosti, enkraten_vnos));
					else:
						conn.execute("INSERT INTO patronazna_sluzba_app_polje_v_porocilu (ime, vnosno_polje, obvezno, enkraten_vnos) VALUES (?,?,?,?)", (ime, vnosno_polje, obvezen_vnos, enkraten_vnos));
					cursor = conn.execute("select id from patronazna_sluzba_app_polje_v_porocilu where ime='" + ime + "' and vnosno_polje='" + vnosno_polje + "';");
					polje_id = cursor.fetchall()[0][0]
				else:
					polje_id = polje_id[0][0]
				conn.execute("INSERT INTO patronazna_sluzba_app_polje_meritev (meritev_id, polje_id) VALUES (?,?)", (str(meritev_id), str(polje_id)));
				if sifra_storitve == 20:
						conn.execute("INSERT INTO patronazna_sluzba_app_polje_meritev (meritev_id, polje_id) VALUES (?,?)", (str(meritev_id_orig), str(polje_id)));
#Bolezni
with open("bolezni.csv", "r", encoding="utf8") as bolezni_file:  #encoding="utf8"
# with open("bolezni.csv", "r") as bolezni_file:  # encoding="utf8"
	bolezni_reader = csv.reader(bolezni_file, delimiter=';')
	next(bolezni_reader, None)  # skip header
	for line in bolezni_reader:
		if len(line)>2:
			conn.execute("INSERT INTO patronazna_sluzba_app_bolezen (sifra, ime, opis) VALUES (?,?,?)", (line[0], line[1], line[2]));
		else:
			conn.execute("INSERT INTO patronazna_sluzba_app_bolezen (sifra, ime) VALUES (?,?)", (line[0], line[1]));
# Metoda, ki delovnim nalogom v bazi kreira pripadajoce obiske
def kreiraj_obiske(delovni_nalog_id, interval_period, type, number_of_visits, date_current):
	# if we have interval type of visitation
	if type == 'Interval':
		for i in range(int(number_of_visits)):
			obveznost = random.choice(['Obvezen', 'Okviren'])
			date_next = date_current + timedelta(days=int(interval_period))
			weekno = date_next.weekday()
			if weekno == 6 or weekno == 0:
				date_next = date_next + timedelta(days=2)
				weekno = date_next.weekday()
			cursor = conn.execute("select pacient_id from patronazna_sluzba_app_pacient_DN where delovni_nalog_id=" + str(delovni_nalog_id) + ";");
			pacient = cursor.fetchall()[0][0]
			print(pacient)
			cursor = conn.execute("select okolis_id from patronazna_sluzba_app_pacient where st_kartice='" + pacient + "';");
			okolis = cursor.fetchall()
			print(okolis)
			okolis=okolis[0][0]
			cursor = conn.execute(
				"select id from patronazna_sluzba_app_patronazna_sestra where okolis_id=" + str(okolis) + ";")
			p_sestra = cursor.fetchall()[0][0]
			# p_sestra = Patronazna_sestra.objects.get(sifra_patronazne_sestre=request.POST['nurse_id'])
			obv = 0
			if obveznost == "Obvezen":
				obv = 1
				obveznost = "Okviren"
			opr = 0
			# visit = Obisk(delovni_nalog=work_task_f, datum=date_current, p_sestra=p_sestra, obvezen_obisk=obv)
			# visit.save()
			conn.execute(
				"INSERT INTO patronazna_sluzba_app_obisk (delovni_nalog_id, datum, obvezen_obisk, p_sestra_id, opravljen) VALUES (?,?,?,?,?)",
				(delovni_nalog_id, date_current, obv, p_sestra, opr));
			date_current = date_next
			print("Obisk shranjen (INTERVAL); datum: ", date_current)
	else:
		# space = number of days so that visits are the most balanced throughout the period
		space = int(interval_period / number_of_visits)
		for i in range(int(number_of_visits)):
			obveznost = random.choice(['Obvezen', 'Okviren'])
			#   If there are 1 or more days between visits
			if int(interval_period) >= int(number_of_visits):
				date_next = date_current + timedelta(days=int(space))
				#   check if its weekend
				weekno = date_next.weekday()
				if weekno == 6 or weekno == 0:
					date_next = date_next + timedelta(days=2)
					weekno = date_next.weekday()
				# find the appropriate nurse for the county
				# p_sestra = Patronazna_sestra.objects.get(sifra_patronazne_sestre=request.POST['nurse_id'])
				cursor = conn.execute(
					"select pacient_id from patronazna_sluzba_app_pacient_DN where delovni_nalog_id=" + str(
						delovni_nalog_id) + ";");
				pacient = cursor.fetchall()[0][0]
				cursor = conn.execute(
					"select okolis_id from patronazna_sluzba_app_pacient where st_kartice=" + str(
						pacient) + ";");
				okolis = cursor.fetchall()[0][0]
				cursor = conn.execute(
					"select id from patronazna_sluzba_app_patronazna_sestra where okolis_id=" + str(
						okolis) + ";")
				p_sestra = cursor.fetchall()[0][0]
				print("p_sestra", p_sestra)
				#   check if the first visit is mandatory on that day
				obv = 0
				if obveznost == "Obvezen":
					obv = 1
					obveznost = "Okviren"
				opr = 0
				# visit = Obisk(delovni_nalog=work_task_f, datum=date_current, p_sestra=p_sestra, obvezen_obisk=obv)
				# visit.save()
				conn.execute(
					"INSERT INTO patronazna_sluzba_app_obisk (delovni_nalog_id, datum, obvezen_obisk, p_sestra_id, opravljen) VALUES (?,?,?,?,?)",
					(delovni_nalog_id, date_current, obv, p_sestra, opr));
				date_current = date_next
				print("Obisk shranjen (OBDOBJE); datum: ", date_current)
# Pacienti na delovnih nalogih
with open("pacienti_na_DN.csv", "r", encoding="utf8") as pacientiDN_file:  #encoding="utf8"
# with open("pacienti_na_DN.csv", "r") as pacientiDN_file:  # encoding="utf8"
	pacientiDN_reader = csv.reader(pacientiDN_file, delimiter=';')
	next(pacientiDN_reader, None)  # skip header
	for line in pacientiDN_reader:
		if line[0]=='#':
			continue
		conn.execute("INSERT INTO patronazna_sluzba_app_pacient_DN (delovni_nalog_id, pacient_id) VALUES (?,?)", (int(line[0]), line[1]));
#Delovni nalogi
with open("delovni_nalogi.csv", "r", encoding="utf8") as dn_file:  #encoding="utf8"
# with open("delovni_nalogi.csv", "r") as dn_file:  # encoding="utf8"
	dn_reader = csv.reader(dn_file, delimiter=';')
	next(dn_reader, None)  # skip header
	for line in dn_reader:
			datum=datetime.strptime(line[1],"%d.%m.%Y")
			cursor = conn.execute("select id from patronazna_sluzba_app_vodja_PS where sifra_vodje_PS=" + str(line[8]) + ";")
			vodjePS = cursor.fetchall()
			if len(vodjePS) == 0:
				cursor = conn.execute("select id from patronazna_sluzba_app_zdravnik where sifra_zdravnika=" + str(line[8]) + ";")
				zdravnik=cursor.fetchall()
				conn.execute("INSERT INTO patronazna_sluzba_app_delovni_nalog (id, datum_prvega_obiska, st_obiskov, cas_obiskov_tip, cas_obiskov_dolzina, vrsta_obiska_id, bolezen_id, izvajalec_zs_id, zdravnik_id) VALUES (?,?,?,?,?,?,?,?,?)", (int(line[0]), datum, int(line[2]), line[3], int(line[4]), int(line[5]), line[6], int(line[7]), zdravnik[0][0]));
			else:
				conn.execute("INSERT INTO patronazna_sluzba_app_delovni_nalog (id, datum_prvega_obiska, st_obiskov, cas_obiskov_tip, cas_obiskov_dolzina, vrsta_obiska_id, bolezen_id, izvajalec_zs_id, vodja_PS_id) VALUES (?,?,?,?,?,?,?,?,?)", (int(line[0]), datum, int(line[2]),line[3],int(line[4]),int(line[5]),line[6],int(line[7]), vodjePS[0][0])); #int(line[8])
			kreiraj_obiske(int(line[0]), int(line[4]), line[3], int(line[2]), datum)
#Material na delovnih nalogih
with open("material_na_DN.csv", "r", encoding="utf8") as materialDN_file:  #encoding="utf8"
# with open("material_na_DN.csv", "r") as materialDN_file:  # encoding="utf8"
	materialDN_reader = csv.reader(materialDN_file, delimiter=';')
	next(materialDN_reader, None)  # skip header
	for line in materialDN_reader:
		conn.execute("INSERT INTO patronazna_sluzba_app_material_DN (delovni_nalog_id, material_id, kolicina) VALUES (?,?,?)", (int(line[0]), int(line[1]), int(line[2])));
#Zdravila na delovnih nalogih
with open("zdravila_na_DN.csv", "r", encoding="utf8") as zdravilaDN_file:  #encoding="utf8"
# with open("zdravila_na_DN.csv", "r") as zdravilaDN_file:  # encoding="utf8"
	zdravilaDN_reader = csv.reader(zdravilaDN_file, delimiter=';')
	next(zdravilaDN_reader, None)  # skip header
	for line in zdravilaDN_reader:
		conn.execute("INSERT INTO patronazna_sluzba_app_zdravilo_DN (delovni_nalog_id, zdravilo_id, kolicina) VALUES (?,?,?)", (int(line[0]), int(line[1]), int(line[2])));
#Nadomescanja
with open("nadomescanja.csv", "r", encoding="utf8") as nadomescanja_file:  #encoding="utf8"
# with open("nadomescanja.csv", "r") as nadomescanja_file:  # encoding="utf8"
	nadomescanja_reader = csv.reader(nadomescanja_file, delimiter=';')
	next(nadomescanja_reader, None)  # skip header
	for line in nadomescanja_reader:
		conn.execute("INSERT INTO patronazna_sluzba_app_nadomescanje (sestra_id, nadomestna_sestra_id, datum_zacetek, datum_konec, veljavno) VALUES (?,?,?,?,?)", (int(line[0]), int(line[1]), datetime.strptime(line[2],"%d.%m.%Y"), datetime.strptime(line[3],"%d.%m.%Y"), True if line[4]=='True' else False));
#*****za sestra2@mail.si in sestra3@mail.si se posebej dodaj nadomescanja..
'''cursor=conn.execute("select id from auth_user where username='sestra2@mail.si';")
sestra2_profil=cursor.fetchall()[0][0]
cursor = conn.execute("select id from patronazna_sluzba_app_patronazna_sestra where uporabniski_profil_id=" + str(sestra2_profil) + ";")
sestra2=cursor.fetchall()[0][0]
conn.execute("INSERT INTO patronazna_sluzba_app_nadomescanje (sestra_id, nadomestna_sestra_id, datum_zacetek, datum_konec, veljavno) VALUES (?,?,?,?,?)", (sestra2, 1, datetime.now(), datetime.now() + timedelta(days=14), True));
cursor=conn.execute("select id from auth_user where username='sestra3@mail.si';")
sestra3_profil=cursor.fetchall()[0][0]
cursor = conn.execute("select id from patronazna_sluzba_app_patronazna_sestra where uporabniski_profil_id=" + str(sestra3_profil) + ";")
sestra3=cursor.fetchall()[0][0]
conn.execute("INSERT INTO patronazna_sluzba_app_nadomescanje (sestra_id, nadomestna_sestra_id, datum_zacetek, datum_konec, veljavno) VALUES (?,?,?,?,?)", (sestra2, sestra3, datetime.now()-timedelta(days=8), datetime.now() - timedelta(days=1), True));
'''
#Obiske, ki so ze potekli oznaci kot opravljene in zanje v bazo vnesi meritve
cursor = conn.execute("select id,datum,opravljen,delovni_nalog_id,p_sestra_id from patronazna_sluzba_app_obisk;");
obiski = cursor.fetchall()

for obisk in obiski:
	#### print("----- OBISK.delovni_nalog_id = "+str(obisk[3])+" ------ ")
	id=int(obisk[0])
	datum=datetime.strptime(obisk[1],"%Y-%m-%d %H:%M:%S")
	cursor = conn.execute("select pacient_id from patronazna_sluzba_app_pacient_dn where delovni_nalog_id="+str(obisk[3])+";");
	pacienti=[x[0] for x in cursor.fetchall()]
	skrbniki=[]
	oskrbovanci=[]
	for pacient in pacienti:
		#### print("PACIENT: ",pacient)
		cursor = conn.execute("select st_kartice from patronazna_sluzba_app_pacient where st_kartice='" + str(pacient) + "' and uporabniski_profil_id is Null;");
		result = cursor.fetchall()
		if len(result)==0:
			skrbniki.append(pacient)
		else:
			oskrbovanci.append(pacient)
	#### print("SKRBNIKI: ",skrbniki)
	#### print("OSKRBOVANCI: ",oskrbovanci)

	if datetime.now() > datum:
		opravljen=True
	else:
		opravljen=False

	pacient_id = pacienti[0]
	if opravljen:
		cursor = conn.execute("update patronazna_sluzba_app_obisk set opravljen=1 where id = "+str(id)+";");

	if opravljen:
		cursor = conn.execute("select vrsta_obiska_id from patronazna_sluzba_app_delovni_nalog where id="+str(obisk[3])+";");
		delovni_nalog_vrsta_obiska = cursor.fetchall()[0][0]
		#### print("VRSTA OBISKA: ",delovni_nalog_vrsta_obiska)
		cursor = conn.execute("select id from patronazna_sluzba_app_meritev where vrsta_obiska_id="+str(delovni_nalog_vrsta_obiska)+";");
		meritve=cursor.fetchall() #HRANI VSE MERITVE ZA TO VRSTO OBISKA
		print()
		print("MERITVE ZA VRSTO OBISKA : ", delovni_nalog_vrsta_obiska, " ++++++++++++++++++++++++++++++++++++++++++++ ")
		print(meritve)
		print("=======================================================================================================")
		print()

		meritve=[x[0] for x in meritve]
		polja=[] #HRANI VSA POLJA ZA TO VRSTO OBISKA
		#meritve_id=[]
		print("meritve x0: ", meritve)
		print("=======================================================================================================")
		for meritev_id in meritve:
			cursor = conn.execute("select polje_id, meritev_id from patronazna_sluzba_app_polje_meritev where meritev_id="+str(meritev_id)+";");
			polja_tmp=cursor.fetchall()
			print()
			print()
			print("POLJA_TMP mertiev id: ", meritev_id )
			print(polja_tmp)
			print("len: ", len(polja_tmp))
			if len (polja_tmp)>0:
				for x in polja_tmp:
					polja.append((x[0],x[1]))

		print("=======================================================================================================")

		print("POLJA")
		print(polja)
					#meritve_id.append(x[1])
		#### print("STEVILO MERITEV: ",len(polja))
		'''print("***SEZNAM PRIPADAJOCIH POLJ: ")
		for polje in polja:
			#### print(polje)'''
		for vrednosti_id in polja:
			polje_id = vrednosti_id[0] #ID POLJA
			meritev_id= vrednosti_id[1] #ID MERITVE, NA KATERO SE POLJE NAVEZUJE
			cursor = conn.execute("select id,ime,vnosno_polje,obvezno,mozne_vrednosti from patronazna_sluzba_app_polje_v_porocilu where id=" + str(polje_id) + ";");
			polje_info = cursor.fetchall()[0]

		#if polje_info[3]==1: #Ustvari samo obvezna polja
			if polje_info[1]=='Prosti vnos':
				izbira = "Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1]=='Datum':
				datum_tmp=datum-timedelta(days=random.choice([1,2,3,4,5,6,7]))
			elif '/' in polje_info[1] and polje_info[1][polje_info[1].index('/')+1]!='L':
				izbira=random.choice(str(polje_info[3]).split(','))
			#elif polje_info[1] == 'Moteno/Ni moteno':
			#elif polje_info[1] == 'Nizka/Srednja/Visoka':
			elif polje_info[1] == 'Sistolični (mm Hg)':
				izbira=90+int(random.random()*200-90)
			elif polje_info[1] == 'Diastolični (mm Hg)':
				izbira = 40 + int(random.random() * 90 - 40)
			elif polje_info[1] == 'Udarci na minuto':
				izbira=45+int(random.random()*140 - 45)
			elif polje_info[1] == 'Vdihi na minuto':
				izbira = 90 + int(random.random() * 80 - 90)
			elif polje_info[1] == 'st C':
				izbira = 36 + int(random.random() * 39 - 36)
			elif polje_info[1] == 'kg':
				izbira = 45 + (random.random() * 120 - 45)
			elif polje_info[1] == 'Datum rojstva otroka':
				if len(oskrbovanci)==0:
					#### print("Napaka!")
					continue
				pacient_id=oskrbovanci[0]
				#### print("ST KARTICEE: ",pacient_id)

				'''cursor = conn.execute("select st_kartice from patronazna_sluzba_app_pacient;")
				test=cursor.fetchall()
				for t in test:
					#### print("**Pacient v bazi: ",t[0])'''

				cursor = conn.execute("select datum_rojstva from patronazna_sluzba_app_pacient where st_kartice='" + str(
				pacient_id) +"';");
				datum_rojstva=datetime.strptime(cursor.fetchall()[0][0],"%Y-%m-%d %H:%M:%S")
				izbira=datum_rojstva

			elif polje_info[1] == 'Porodna teža otroka (g)':
				if len(oskrbovanci)==0:
					#### print("Napaka!!!")
					continue
				pacient_id=oskrbovanci[0]
				izbira = 2000 + int(random.random() * 6400 - 2000)
			elif polje_info[1] == 'Porodna višina otroka (cm)':
				if len(oskrbovanci)==0:
					#### print("Napaka!!!")
					continue
				pacient_id=oskrbovanci[0]
				izbira = 40 + int(random.random() * 65 - 40)
			elif polje_info[1] == 'g':
				if len(oskrbovanci)==0:
					print("Napaka???")
					#continue
				pacient_id=oskrbovanci[0]
				izbira = 2600 + int(random.random() * 8200 - 2600)
			elif polje_info[1] == 'cm':
				if len(oskrbovanci)==0:
					print("Napaka???")
					#continue
				pacient_id=oskrbovanci[0]
				izbira = 48 + int(random.random() * 80 - 48)
			#elif polje_info[1] == 'Da/Ne':
			#elif polje_info[1] == 'Ni posebnosti/Mikcija/Defekacija/Napenjanje/Kolike/Polivanje/Bruhanje':
			elif polje_info[1] == 'Urin: prosti vnos':
				izbira = "Urin - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'Blato: prosti vnos':
				izbira = "Blato - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'Vid: prosti vnos':
				izbira = "Vid - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'Vonj: prosti vnos':
				izbira = "Vonj - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'Sluh: prosti vnos':
				izbira = "Sluh - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'Okus: prosti vnos':
				izbira = "Okus - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'Otip: prosti vnos':
				izbira = "Otip - Porocilo o pacientovem stanju. Testni vnos."
				#continue
			#elif polje_info[1] == 'Samostojen/Delno odvisen/Povsem odvisen':
			elif polje_info[1] == 'Pomoč: svojci':
				izbira = "Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] == 'drugi':
				izbira = "Porocilo o pacientovem stanju. Testni vnos."
				#continue
			elif polje_info[1] =='mmol/L':
				izbira = 50 + int(random.random() * 230 - 50)
			elif polje_info[1] == '%':
				izbira = 85 + int(random.random() * 100 - 85)
			#elif polje_info[1] == 'Da/Delno/Ne':
			else:
				izbira = "Porocilo o pacientovem stanju. Testni vnos."

			if delovni_nalog_vrsta_obiska==20:
				#print("IS MERITVE EMPTY?? ",meritve)
				cursor = conn.execute("select id,sifra,opis,vrsta_obiska_id from patronazna_sluzba_app_meritev where id=" + str(meritev_id) + ";");
				meritev_info = cursor.fetchall()
				#### print("!!!!!!!!DOLZINA VECJA OD 1: ",len(meritev_info))
				print(meritev_info)
				sifra=meritev_info[0][1]
				opis=meritev_info[0][2]
				vrsta=meritev_info[0][3]
				cursor = conn.execute("select vrsta_obiska_id from patronazna_sluzba_app_meritev where sifra=" + str(meritev_info[0][1]) + " and opis= '" + meritev_info[0][2] + "' ;");
				vrste_obiskov_vezane_na_obisk = cursor.fetchall()
				print("Na ta obisk so vezane: ",vrste_obiskov_vezane_na_obisk)

				tmp_vrste=[x[0] for x in vrste_obiskov_vezane_na_obisk]
				print("TMP VRSTE: ", tmp_vrste)
				#### print("*** Na to kombinacijo sifro storitve in opisa storitve so vezane vrste obiska: ",tmp_vrste)
				if 30 in tmp_vrste:
					#### print()
					#### print()
					#### print()
					#### print()
					print()
					print("30")
					#### print()
					#### print()
					#### print()

				if 80 in tmp_vrste:
					if len(skrbniki) > 0:
						pacient_id = skrbniki[0]
					else:
						#### print("**Manjka skrbnik")
						pacient_id = '072044444444'
				else:
					if len(oskrbovanci) > 0:
						pacient_id = oskrbovanci[0]
					else:
						#### print("**Manjka oskrbovanec")
						pacient_id = '062088888886'

				'''for meritev_info in meritveee:
					#print("Meritev info: ",meritev_info)
					if meritev_info[3]==30:
						if len(oskrbovanci)>0:
							pacient_id=oskrbovanci[0]
						else:
							#### print("**Manjka oskrbovanec")
							pacient_id='062088888886'
						break
					if meritev_info[3]==80:
						if len(skrbniki)>0:
							pacient_id=skrbniki[0]
						else:
							#### print("**Manjka skrbnik")
							pacient_id='072044444444'
						break'''

			else:
				pacient_id=skrbniki[0]

			if delovni_nalog_vrsta_obiska==20:
				if pacient_id in skrbniki:
					print()
					print("**V bazo dodajam polje za skrbnika!")
				else:
					print()
					print("**V bazo dodajam polje za oskrbovanca!")
			print("ID : ", pacient_id)
			conn.execute("INSERT INTO patronazna_sluzba_app_porocilo_o_obisku (obisk_id, pacient_id, polje_id, vrednost, meritev_id) VALUES (?,?,?,?,?)", (int(id), pacient_id, int(polje_info[0]),str(izbira), meritev_id));

conn.commit()
conn.close()