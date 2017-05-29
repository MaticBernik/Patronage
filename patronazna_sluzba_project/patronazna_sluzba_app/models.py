# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from annoying.fields import AutoOneToOneField #,signals  ;;   pip install django-annoying
from django.db.models import signals



# SOME VALIDATORS 
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
numeric_only = RegexValidator(r'^[0-9]*$', 'Dovoljena zgolj stevilska vrednost.')
min_len_12 = MinLengthValidator(12, "Stevilka kartica je dolzine 12 znakov.")
max_len_12 = MaxLengthValidator(12, "Stevilka kartica je dolzine 12 znakov.")

class Posta(models.Model):
    postna_st = models.IntegerField(primary_key=True)
    naziv_poste = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.postna_st+' '+self.naziv_poste


class Okolis(models.Model):
    class Meta:
        unique_together = (('posta', 'ime'),)
    #sifra_okolisa = models.IntegerField(primary_key=True)  # Zacasno..
    posta = models.ForeignKey(Posta)
    ime = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.ime

'''class Izvajalec_ZS(models.Model):
    #V izvorni tabeli so Izvajalci naprej deljeni na oddelke - vendar to nas tu ne zanima??
    class Meta:
        unique_together = (('st_izvajalca', 'sifra_VZD'),)

    st_izvajalca = models.IntegerField(primary_key=True)
    sifra_nadrejenega = models.IntegerField(null=True)
    sifra_osnovni = models.IntegerField(null=True)
    sifra_podrejeni = models.IntegerField(null=True)
    sifra_lokacije = models.IntegerField(null=False)
    naziv_organizacije = models.CharField(max_length=100, null=False)
    dodatni_naziv = models.CharField(max_length=100, null=True)
    naslov = models.CharField(max_length=100, null=False)
    posta = models.ForeignKey(Posta, null=True)
    sifra_VZD = models.IntegerField(null=False)
    naziv_VZD = models.CharField(max_length=100, null=False)
    sifra_pravnega_statusa_izvajalca = models.IntegerField(null=False)
    opis_pravnega_statusa_izvajalca = models.CharField(max_length=100, null=False)
    sifra_tipa_izvajalca = models.IntegerField(null=False)
    opis_tipa_izvajalca = models.CharField(max_length=100, null=False)
    sifra_obcine = models.IntegerField(null=False)
    ime_obcine = models.CharField(max_length=100, null=False)
    sifra_ZZV = models.IntegerField(null=False)
    izvajalec_samo1X = models.BooleanField(null=False, default=False)
    stevilo_vrstic_VZDjev = models.IntegerField(null=False)'''




'''def create_Uporabnik(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        Uporabnik.objects.create(thing=instance)

signals.post_save.connect(create_Uporabnik, sender=User, weak=False, dispatch_uid='models.create_Uporabnik')'''

class Izvajalec_ZS(models.Model):
    st_izvajalca = models.IntegerField(primary_key=True)
    #st_izvajalca = models.DecimalField(max_digits=5,decimal_places=0,primary_key=True)
    naziv = models.CharField(max_length=100, null=False)
    naslov = models.CharField(max_length=100, null=False)
    posta = models.ForeignKey(Posta, null=True)


class Zdravnik(models.Model):
    #uporabniski_profil = models.ForeignKey(User,on_delete=models.CASCADE)
    uporabniski_profil = models.OneToOneField(User)
    sifra_zdravnika = models.IntegerField(unique=True,null=False) #koliko mestna?
    telefonska_st = models.CharField(max_length=15, null=False) #+368
    sifra_izvajalca_ZS = models.ForeignKey(Izvajalec_ZS, null=True)
    #sifra_izvajalca_ZS = models.DecimalField(max_digits=5,decimal_places=0)
    def __str__(self):
        return str(self.sifra_zdravnika)+' '+self.uporabniski_profil.first_name+' '+self.uporabniski_profil.last_name


class Vodja_PS(models.Model):
    #uporabniski_profil = models.ForeignKey(User, on_delete=models.CASCADE)
    uporabniski_profil = models.OneToOneField(User)
    sifra_vodje_PS = models.IntegerField(unique=True,null=False)
    #sifra_vodje_PS = models.DecimalField(max_digits=5,decimal_places=0)
    telefonska_st = models.CharField(max_length=15, null=False)
    sifra_izvajalca_ZS = models.ForeignKey(Izvajalec_ZS, null=True)
    def __str__(self):
        return str(self.sifra_vodje_PS)+' '+self.uporabniski_profil.first_name+' '+self.uporabniski_profil.last_name


class Patronazna_sestra(models.Model):
    #uporabniski_profil = models.ForeignKey(User, on_delete=models.CASCADE)
    uporabniski_profil = models.OneToOneField(User)
    sifra_patronazne_sestre = models.IntegerField(unique=True,null=False)
    #sifra_patronazne_sestre = models.DecimalField(max_digits=5,decimal_places=0)
    telefonska_st = models.CharField(max_length=15, null=False)
    sifra_izvajalca_ZS = models.ForeignKey(Izvajalec_ZS, null=True)
    okolis = models.OneToOneField(Okolis,default=1)
    def __str__(self):
        return str(self.sifra_patronazne_sestre)+' '+self.uporabniski_profil.first_name+' '+self.uporabniski_profil.last_name


class Sodelavec_ZD(models.Model):
    #uporabniski_profil = models.ForeignKey(User, on_delete=models.CASCADE)
    uporabniski_profil = models.OneToOneField(User)
    sifra_sodelavca = models.IntegerField(unique=True,null=False)
    #sifra_sodelavca = models.DecimalField(max_digits=5,decimal_places=0)
    telefonska_st = models.CharField(max_length=15, null=False)
    sifra_izvajalca_ZS = models.ForeignKey(Izvajalec_ZS, null=True)
    def __str__(self):
        return str(self.sifra_sodelavca)+' '+self.uporabniski_profil.first_name+' '+self.uporabniski_profil.last_name


class Uporabnik(models.Model):
    #profil = models.OneToOneField(User, primary_key=True)
    profil= AutoOneToOneField(User, primary_key=True)

    def __str__(self):
        if Patronazna_sestra.objects.filter(uporabniski_profil_id=self.profil_id).exists():
            sifra=Patronazna_sestra.objects.get(uporabniski_profil_id=self.profil).sifra_patronazne_sestre
        if Vodja_PS.objects.filter(uporabniski_profil_id=self.profil).exists():
            sifra=Vodja_PS.objects.get(uporabniski_profil_id=self.profil).sifra_vodje_PS
        if Zdravnik.objects.filter(uporabniski_profil_id=self.profil).exists():
            sifra=Zdravnik.objects.get(uporabniski_profil_id=self.profil).sifra_zdravnika
        if Sodelavec_ZD.objects.filter(uporabniski_profil_id=self.profil).exists():
            sifra=Sodelavec_ZD.objects.get(uporabniski_profil_id=self.profil).sifra_sodelavca
        return str(sifra)+' '+self.profil.first_name+' '+self.profil.last_name
    def __unicode__(self):
        if Patronazna_sestra.objects.filter(uporabniski_profil_id=self.profil_id).exists():
            sifra=Patronazna_sestra.objects.get(uporabniski_profil_id=self.profil).sifra_patronazne_sestre
        if Vodja_PS.objects.filter(uporabniski_profil_id=self.profil).exists():
            sifra=Vodja_PS.objects.get(uporabniski_profil_id=self.profil).sifra_vodje_PS
        if Zdravnik.objects.filter(uporabniski_profil_id=self.profil).exists():
            sifra=Zdravnik.objects.get(uporabniski_profil_id=self.profil).sifra_zdravnika
        if Sodelavec_ZD.objects.filter(uporabniski_profil_id=self.profil).exists():
            sifra=Sodelavec_ZD.objects.get(uporabniski_profil_id=self.profil).sifra_sodelavca
        return str(sifra)+' '+self.profil.first_name+' '+self.profil.last_name

class Kontaktna_oseba(models.Model):
    ime = models.CharField(max_length=100, null=False)
    priimek = models.CharField(max_length=100, null=False)
    naslov = models.CharField(max_length=100, null=False)
    telefon = models.CharField(max_length=15, null=False)  # +368
    sorodstvo = models.ForeignKey('Sorodstveno_razmerje',null=True)


class Pacient(models.Model):
    SEX = (('M', 'Moski'), ('Z', 'Zenska'))

    uporabniski_profil = models.OneToOneField(User,on_delete=models.CASCADE, null=True)#pacient je lahko registriran (lahko pa tudi ne v primeru skrbnistva)
    #   Dolzino kartice sem dal na 11, tako kot imam na svoji kartici zdravstvenega zavarovanja
    #   MAX_LEN does not get used in combo with IntegerField.. "max_length=11,"
    st_kartice = models.CharField(validators=[numeric_only, min_len_12, max_len_12], max_length=12, null=False,default=-1, primary_key=True)
    telefonska_st = models.CharField(max_length=15, null=False)
    naslov = models.CharField(max_length=100, null=False)
    spol = models.CharField(max_length=1,choices=SEX,blank=False)
    skrbnistvo = models.ForeignKey('self', null=True)
    datum_rojstva = models.DateTimeField()
    kontakt = models.ForeignKey(Kontaktna_oseba, null=True)
    posta = models.ForeignKey(Posta, null=True)
    okolis = models.ForeignKey(Okolis, null=True)
    sorodstvo = models.ForeignKey('Sorodstveno_razmerje',null=True) #Kaze na skrbnika doticnega pacienta
    ime = models.CharField(max_length=100, null=False)
    priimek = models.CharField(max_length=100, null=False)
    email=models.EmailField(unique=True,null=True)

    def copy_redundant_fiends(self):
        if self.uporabniski_profil:
            self.uporabniski_profil.first_name = self.ime
            self.uporabniski_profil.last_name = self.priimek
            self.uporabniski_profil.email = self.email
            self.uporabniski_profil.username= self.email

    def __str__(self):
        return str(self.st_kartice)+' '+self.ime+' '+self.priimek+' '+self.naslov


class Sorodstveno_razmerje(models.Model):
	kontakt = models.ForeignKey(Kontaktna_oseba, on_delete=models.CASCADE)
	pacient_id = models.ForeignKey(Pacient, on_delete=models.CASCADE)
	tip_razmerja = models.CharField(max_length=100, null=False)


class Zdravilo(models.Model):
    nacionalna_sifra = models.IntegerField(primary_key=True)
    ime = models.CharField(max_length=100, null=True)
    poimenovanje = models.CharField(max_length=100, null=False)
    kratko_poimenovanje = models.CharField(max_length=100, null=True)
    oznaka_EAN = models.IntegerField()
    oglasevanje_dovoljeno = models.BooleanField(default=False,null=False)
    originator = models.BooleanField(default=False,null=False)
    slovenski_naziv_farmacevtske_oblike = models.CharField(max_length=100, null=True)
    kolicina_osnovne_enote_za_aplikacijo = models.IntegerField(null=False,default=-1)
    oznaka_osnovne_enote_za_aplikacijo = models.CharField(max_length=100, null=True)
    pakiranje = models.CharField(max_length=100, null=True)
    sifra_pravnega_statusa = models.IntegerField(null=False)
    naziv_pravnega_statusa = models.CharField(max_length=100, null=True)
    naziv_poti_uporabe = models.CharField(max_length=100, null=True)
    sifra_rezima_izdaje = models.IntegerField(null=False)
    oznaka_rezima_izdaje = models.CharField(max_length=100, null=True)
    naziv_rezima_izdaje = models.CharField(max_length=100, null=True)
    sifra_prisotnosti_na_trgu = models.IntegerField(null=True)
    izdaja_na_posebni_zdravniski_recept = models.CharField(max_length=100, null=True)
    trigonik_absolutna_prepoved_upravljanja_vozil = models.CharField(max_length=100, null=True)
    trigonik_relativna_prepoved_upravljanja_vozil = models.CharField(max_length=100, null=True)
    omejena_kolicina_enkratne_izdaje = models.CharField(max_length=100, null=True)
    sifra_vrste_postopka = models.IntegerField(null=True)
    oznaka_vrste_postopka = models.CharField(max_length=100, null=True)
    naziv_vrste_postopka = models.CharField(max_length=100, null=True)
    oznaka_ATC = models.CharField(max_length=100, null=True)
    vir_podatka = models.CharField(max_length=100, null=True)
    slovenski_opis_ATC = models.CharField(max_length=100, null=True)
    latinski_opis_ATC = models.CharField(max_length=100, null=True)
    angleski_opis_ATC = models.CharField(max_length=100, null=True)
    aktivno_zdravilo = models.BooleanField(default=False)
    sifra_liste = models.IntegerField(null=False)
    oznaka_liste = models.CharField(max_length=100, null=True)
    opis_omejitve_predpisovanja = models.CharField(max_length=100, null=True)
    velja_od = models.CharField(max_length=100, null=True) #models.DateTimeField(null=True)
    sifra_iz_seznama_B = models.IntegerField(null=True)
    oznaka_iz_seznama_B = models.CharField(max_length=100, null=True)
    opis_omejitve_predpisovanja_B = models.CharField(max_length=100, null=True)
    velja_od_B = models.DateTimeField(null=True)
    sifra_iz_seznama_A = models.IntegerField(null=True)
    oznaka_iz_seznama_A = models.CharField(max_length=100, null=True)
    opis_omejitve_predpisovanja_A = models.CharField(max_length=100, null=True)#models.DateTimeField(null=True)
    velja_od_A = models.DateTimeField(null=True)
    cena_na_debelo_regulirana = models.FloatField(null=True)
    datum_veljavnosti_regulirane_cene = models.DateTimeField(null=True)
    tip_regulirane_cene = models.CharField(max_length=100, null=True)
    predviden_datum_konca_veljavnosti_regulirane_cene = models.DateTimeField(null=True)
    vrsta_zdravila = models.CharField(max_length=100, null=True)
    dogovorjena_cena = models.FloatField(null=True)
    datum_veljavnosti_dogovorjene_cene = models.DateTimeField(null=True)
    tip_dogovorjene_cene = models.CharField(max_length=100, null=True)
    sifra_skupine_MZZ = models.IntegerField(null=True)
    opis_skupine_MZZ = models.CharField(max_length=100, null=True)
    najvisja_priznana_vrednost_zdravila_v_eur = models.FloatField(null=True)
    datum_veljavnosti_NPV_zdravila = models.DateTimeField(null=True)
    najvisja_priznana_vrednost_za_zivila = models.CharField(max_length=100, null=True)
    datum_veljavnosti_NPV_zivila = models.DateTimeField(null=True)
    primerno_za_INN_predpisovanje = models.CharField(max_length=100, null=True)
    sifra_vrste_postopka = models.IntegerField(null=True)
    naziv_vrste_postopka = models.CharField(max_length=100, null=True)
    stevilka_dovoljenja = models.CharField(max_length=100, null=True)
    datum_dovoljenja = models.DateTimeField(null=True)
    datum_veljavnosti_dovoljenja = models.DateTimeField(null=True)
    stevilka_uradnega_lista_objave = models.CharField(max_length=100, null=True)
    datum_uradnega_lista_objave = models.DateTimeField(null=True)
    datum_prenehanja_trzenja_zdravila = models.DateTimeField(null=True)
    sifra_imetnika_dovoljenja = models.IntegerField(null=True)
    naziv_imetnika_dovoljenja = models.CharField(max_length=100, null=True)
    kolicina_za_preracun_DDO = models.IntegerField(null=True)
    DDO = models.FloatField(null=True)
    oznaka_merske_enote = models.CharField(max_length=100, null=True)
    spletna_povezava_na_EMA = models.CharField(max_length=100, null=True)
    spremljanje_varnosti = models.BooleanField(default=False)
    sif_razp_zdr = models.CharField(max_length=100, null=True)
    razpolozljivost_zdravila = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.ime
    def __str__(self):
        return self.ime


class Vrsta_obiska(models.Model):
    TIP_OBISKA = (('P', 'Preventivni obisk'), ('K', 'Kurativni obisk'))
    VRSTA_PREVENTIVNI = (('N', 'Obisk nosecnice'), ('O', 'Obisk otrocnice in novorojencka'), ('S', 'Obisk starostnika')) #('R', 'Obisk novorojencka')
    VRSTA_KURATIVNI = (('I', "Aplikacija inekcij"), ('K', "Odvzem krvi"), ('Z', "Kontrola zdravstvenega stanja"))
    IME_STORITVE = (('I', "Aplikacija inekcij"), ('K', "Odvzem krvi"), ('Z', "Kontrola zdravstvenega stanja"), ('N', 'Obisk nosecnice'), ('O', 'Obisk otrocnice in novorojencka'), ('S', 'Obisk starostnika'))

    sifra = models.IntegerField(primary_key=True)
    ime = models.CharField(choices=IME_STORITVE, max_length=10, blank=False, null=False)
    tip = models.CharField(choices=TIP_OBISKA, max_length=10, null=True)

    def save(self):
        preventivni=[x[0] for x in self.VRSTA_PREVENTIVNI]
        if self.ime in preventivni:
            self.tip=self.TIP_OBISKA[0]
        else:
            self.tip=self.TIP_OBISKA[1]

    def __unicode__(self):
        return str(self.sifra)+" "+self.ime

    def __str__(self):
        return str(self.sifra) + " " + self.ime


class Meritev(models.Model): #Oz. bolje receno aktivnost?
    #Pove za katero vrsto obiska se meritev izvaja, in katere podatke mora vsebovati porocilo
    class Meta:
        unique_together = (('sifra', 'vrsta_obiska'),)

    vrsta_obiska = models.ForeignKey(Vrsta_obiska, null=False)
    sifra = models.IntegerField(null=False)
    opis = models.CharField(max_length=500, null=False)
    #porocilo = models.CharField(max_length=100, null=False)

class Polje_v_porocilu(models.Model):
    #Tu so opisana polja, ki se lahko pojavijo na porocilu
    ime = models.CharField(max_length=100, null=True) #ime polja oz. tip vsebine npr. Sistolični (mm Hg)
    vnosno_polje = models.CharField(max_length=100, null=True) #tip polja, ki se ga uporabi na frontendu za vnos
    mozne_vrednosti = models.CharField(max_length=100, null=True) #mozne vrednosti locene z vejico.. sicer razvidno ze iz imena

class Polje_meritev(models.Model):
    #Tabela povezuje Meritev oz. aktivnost z vsemi polji, ki jih potrebuje porocilo za to meritev
    meritev = models.ForeignKey(Meritev)  # Katera meritev naj vsebuje to polje
    polje = models.ForeignKey(Polje_v_porocilu)


class Bolezen(models.Model):
    sifra = models.CharField(max_length=6, null=False, primary_key=True)
    ime = models.CharField(max_length=100, null=False)
    opis = models.CharField(max_length=500, null=True)

class Material(models.Model):
    ime = models.CharField(max_length=100, null=False)
    proizvajalec = models.CharField(max_length=100, null=False)
    opis = models.CharField(max_length=500, null=False)
    kolicina_osnovne_enote = models.IntegerField(null=False, default=-1)
    oznaka_osnovne_enote = models.CharField(max_length=100, null=True)

class Delovni_nalog(models.Model):
    CAS_OBISKOV = (("Interval","Casovni interval med zaporednima obiskoma v dnevih"), ("Obdobje","Stevilo dni, v katerih mora biti obisk opravljen"))
    #OBVEZNOST = (("Obvezen","Prvi obisk se mora opraviti na tocen dan"), ("Okviren","Prvi obisk se lahko opravi v vec dnevih"))

    datum_prvega_obiska = models.DateTimeField(null=True)
    st_obiskov = models.IntegerField(null=True)
    cas_obiskov_tip = models.CharField(choices=CAS_OBISKOV, max_length=10, blank=True)
    cas_obiskov_dolzina = models.IntegerField(null=True)
    vrsta_obiska = models.ForeignKey(Vrsta_obiska, null=True)
    bolezen = models.ForeignKey(Bolezen,null=True)
    izvajalec_zs = models.ForeignKey(Izvajalec_ZS, null=True)
    zdravnik = models.ForeignKey(Zdravnik, null=True)
    vodja_PS = models.ForeignKey(Vodja_PS, null=True)
    #obveznost_obiska = models.CharField(choices=OBVEZNOST, max_length=10, blank=True)

class Obisk(models.Model):
    delovni_nalog = models.ForeignKey(Delovni_nalog,null=False, on_delete=models.CASCADE)
    datum = models.DateTimeField(null=True)
    p_sestra = models.ForeignKey(Patronazna_sestra, null=True) #lahko jih je vec, ocitno -.-"
    obvezen_obisk = models.BooleanField(default=0) #    0 == NEOBVEZEN; 1 == OBVEZEN - ce je 1 pomeni da se ne sme spremenit datuma v prihodnje
    opravljen = models.BooleanField(null=False, default=0)

    def meritve(self):
        #Metoda vrne polja, ki jih mora vsebovati porocilo o obisku
        delovni_nalog = Delovni_nalog.objects.get(id=self.delovni_nalog)
        vrsta_obiska = Vrsta_obiska.objects.get(sifra=delovni_nalog.vrsta_obiska)
        meritve=Meritev.objects.filter(vrsta_obiska=vrsta_obiska)
        return meritve

    def porocilo(self):
        #Metoda vrne polja, ki jih mora vsebovati porocilo o obisku
        delovni_nalog = Delovni_nalog.objects.get(id=self.delovni_nalog.id)
        vrsta_obiska = Vrsta_obiska.objects.get(sifra=delovni_nalog.vrsta_obiska.sifra)
        meritve=Meritev.objects.filter(vrsta_obiska=vrsta_obiska)
        meritve=[x.id for x in meritve]
        polja=Polje_meritev.objects.filter(meritev_id__in=meritve)
        # return [x.polje_id for x in polja]
        return [(x.polje_id,Meritev.objects.get(id=x.meritev_id).opis) for x in polja]


class Pacient_DN(models.Model):
    delovni_nalog = models.ForeignKey(Delovni_nalog, null=False, on_delete=models.CASCADE)
    pacient = models.ForeignKey(Pacient, null=True)

class Porocilo_o_obisku(models.Model):
    obisk=models.ForeignKey(Obisk)
    polje=models.ForeignKey(Polje_v_porocilu)
    vrednost=models.CharField(max_length=100, null=False) #zal ne vem kako bi resil drugace, kot da so vse vrednosti znotraj porocila nizi znakov (kar bo dovolj za izpis), potem pa se typecasta glede na tip polja
    pacient = models.ForeignKey(Pacient) # Pri obisku otročnice in novorojenčka(ov) je treba vnesti podatke za vsakega pacienta posebej.

    def save(self, *args, **kwargs):
        if not self.pacient:
            self.pacient = Pacient_DN.objects.get(delovni_nalog_id=self.obisk.delovni_nalog)
        super(Porocilo_o_obisku, self).save(*args, **kwargs)

class Plan(models.Model):
    #Pripadajoca sestra, ki planira obisk je ze dolocena z izbiro obiska
    #V primeru, da sestra1 nadomesca sestro2, se ji pac prikazejo tudi obiski, ki jih planira sestra2,
    #zaradi cesar se vnosi v tej tabeli ne bodo spreminjali..
    planirani_obisk = models.ForeignKey(Obisk) #Obisk, ki ga sestra planera
    datum = models.DateTimeField(null=False,default=datetime.now()+timedelta(days=1)) #Kdaj bo sestra obisk opravila

    def remove_expired(self):
        #Iz plana je potrebno izbrisati pretecene zastavljene obiske
        if datetime.now() >= self.datum:
            self.delete()

    def nurse(self):
        #Metoda vrne sestro, kateri plan pripada
        delovni_nalog = Obisk.objects.get(id=self.planirani_obisk)
        pacient = Pacient_DN.objects.get(delovni_nalog_id=delovni_nalog).pacient
        okolis = pacient.okolis
        sestra = Patronazna_sestra.objects.get(okolis_id=okolis)
        return sestra


class Material_DN(models.Model):
    material = models.ForeignKey(Material, null=True)
    delovni_nalog = models.ForeignKey(Delovni_nalog, null=True, on_delete=models.CASCADE)
    kolicina = models.IntegerField(null=False, default=1)


class Zdravilo_DN(models.Model):
    zdravilo = models.ForeignKey(Zdravilo, null=True)
    delovni_nalog = models.ForeignKey(Delovni_nalog, null=True, on_delete=models.CASCADE)
    kolicina = models.IntegerField( null=False, default=1)

class Nadomescanje(models.Model):
    class Meta:
        unique_together = (('sestra', 'datum_zacetek','datum_konec'),)

    #vodja = models.ForeignKey(Vodja_PS,null=False) #vodja PS, ki je dodal nadomescanje
    sestra = models.ForeignKey(Patronazna_sestra,related_name='%(class)s_requests_created', null=False)
    datum_zacetek = models.DateTimeField(null=False,default=datetime.now())
    datum_konec = models.DateTimeField(null=False,default=datetime.now()+timedelta(days=1))
    nadomestna_sestra = models.ForeignKey(Patronazna_sestra, null=False)
    veljavno = models.BooleanField(null=False, default=0)