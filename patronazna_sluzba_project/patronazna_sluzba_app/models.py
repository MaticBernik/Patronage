from django.db import models
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings

'''class Osebe(models.Model):
	emso = models.CharField(max_length=13, null=False, primary_key=True)#raje integer?
	ime = models.CharField(max_length=100, null=False)
	priimek = models.CharField(max_length=100, null=False)
	naslov = models.CharField(max_length=100, null=False)
	telefon = models.CharField(max_length=15, null=False) #+368

class Registrirani_uporabniki(models.Model):
	email = models.CharField(max_length=13, null=False, unique=True) #primary_key=True 
	geslo = 
	emso = models.ForeignKey(Osebe, on_delete=models.CASCADE)

class Pacienti(models.Model):
	sifra_okolisa = models.IntegerField()
	datum_rojstva = models.DateTimeField()
	st_zdravstvene_kartice = 
	email = models.ForeignKey(Registrirani_uporabnik,on_delete=models.CASCADE) 

class Zdravstveno_osebje(models.Model):
	sifra
	sifra_izvajalca
	email = models.ForeignKey(Registrirani_uporabnik,on_delete=models.CASCADE)	

class Sorodstvena_razmerja(models.Model):
	email = models.ForeignKey(Registrirani_uporabnik,on_delete=models.CASCADE)	
	emso
	vrsta_razmerja

class Funkcije(models.Model):
	email = models.ForeignKey(Registrirani_uporabnik,on_delete=models.CASCADE)
	funkcija
'''

class Zdravnik(models.Model):
	uporabniski_profil = models.ForeignKey(User,on_delete=models.CASCADE)
	sifra_zdravnika = models.IntegerField() #koliko mestna?
	telefonska_st = models.CharField(max_length=15, null=False) #+368
	#sifra_izvajalca_ZS
	def __str__(self):
		return self.sifra_zdravnika+' '+self.uporabniski_profil.firstName+''+self.uporabniski_profil.lastName

class Vodja_PS(models.Model):
	uporabniski_profil = models.ForeignKey(User, on_delete=models.CASCADE)
	sifra_vodje_PS = models.IntegerField()
	telefonska_st = models.CharField(max_length=15, null=False)
	#sifra_izvajalca_ZS

class Patronazna_sestra(models.Model):
	uporabniski_profil = models.ForeignKey(User, on_delete=models.CASCADE)
	sifra_patronazne_sestre = models.IntegerField()
	telefonska_st = models.CharField(max_length=15, null=False)
	#sifra_izvajalca_ZS

class Sodelavec_ZD(models.Model):
	uporabniski_profil = models.ForeignKey(User, on_delete=models.CASCADE)
	sifra_sodelavca = models.IntegerField()
	telefonska_st = models.CharField(max_length=15, null=False)
	#sifra_izvajalca_ZS

'''class Izvajalec_ZS(models.Model):
	st_izvajalca = models.IntegerField(primary_key=True)
	sifra_nadrejenega
	sifra_osnovni
	sifra_podrejeni
	sifra_lokacije
	naziv_organizacije
	dodatni_naziv
	naslov
	posta
	sifra_VZD
	naziv_VZD
	sifra_pravnega_statusa_izvajalca
	opis_pravnega_statusa_izvajalca
	sifra_tipa_izvajalca
	opis_tipa_izvajalca
	sifra_obcine
	ime_obcine
	sifra_ZZV
	izvajalec_samo1X
	stevilo_vrstic_VZDjev'''

#class Okolis(models.Model):


class Pacient(models.Model):
	uporabniski_profil = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)#pacient je lahko registriran (lahko pa tudi ne v primeru skrbnistva)
	telefonska_st = models.CharField(max_length=15, null=False)
	#sifra_okolisa
	naslov = models.CharField(max_length=100, null=False)
	datum_rojstva = models.DateTimeField(default=datetime.now() + timedelta(days=14))
	spol


class Kontaktna_oseba(models.Model):
	ime = models.CharField(max_length=100, null=False)
	priimek = models.CharField(max_length=100, null=False)
	naslov = models.CharField(max_length=100, null=False)
	telefon = models.CharField(max_length=15, null=False)  # +368

class Sorodstveno_razmerje(models.Model):
