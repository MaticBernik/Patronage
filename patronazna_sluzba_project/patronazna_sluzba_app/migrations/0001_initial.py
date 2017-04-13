# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delovni_nalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum_prvega_obiska', models.DateTimeField(null=True)),
                ('st_obiskov', models.IntegerField()),
                ('cas_obiskov_tip', models.CharField(max_length=10, choices=[(b'Interval', b'Casovni interval med zaporednima obiskoma v dnevih'), (b'Obdobje', b'Stevilo dni, v katerih mora biti obisk opravljen')])),
                ('cas_obiskov_dolzina', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Izvajalec_ZS',
            fields=[
                ('st_izvajalca', models.IntegerField(serialize=False, primary_key=True)),
                ('naziv', models.CharField(max_length=100)),
                ('naslov', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kontaktna_oseba',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ime', models.CharField(max_length=100)),
                ('priimek', models.CharField(max_length=100)),
                ('naslov', models.CharField(max_length=100)),
                ('telefon', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Material_DN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delovni_nalog', models.ForeignKey(to='patronazna_sluzba_app.Delovni_nalog', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meritev',
            fields=[
                ('sifra', models.IntegerField(serialize=False, primary_key=True)),
                ('opis', models.CharField(max_length=500)),
                ('porocilo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Okolis',
            fields=[
                ('sifra_okolisa', models.IntegerField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pacient',
            fields=[
                ('uporabniski_profil', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('st_kartice', models.IntegerField(default=-1)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('naslov', models.CharField(max_length=100)),
                ('spol', models.CharField(max_length=1, choices=[(b'M', b'Moski'), (b'Z', b'Zenska')])),
                ('datum_rojstva', models.DateTimeField()),
                ('ime', models.CharField(max_length=100)),
                ('priimek', models.CharField(max_length=100)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('kontakt', models.ForeignKey(to='patronazna_sluzba_app.Kontaktna_oseba', null=True)),
                ('okolis', models.ForeignKey(to='patronazna_sluzba_app.Okolis', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pacient_DN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delovni_nalog', models.ForeignKey(to='patronazna_sluzba_app.Delovni_nalog')),
                ('pacient', models.ForeignKey(to='patronazna_sluzba_app.Pacient', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patronazna_sestra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_patronazne_sestre', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('okolis', models.OneToOneField(to='patronazna_sluzba_app.Okolis')),
                ('sifra_izvajalca_ZS', models.ForeignKey(to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posta',
            fields=[
                ('postna_st', models.IntegerField(serialize=False, primary_key=True)),
                ('naziv_poste', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sodelavec_ZD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_sodelavca', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('sifra_izvajalca_ZS', models.ForeignKey(to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sorodstveno_razmerje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tip_razmerja', models.CharField(max_length=100)),
                ('kontaktna_oseba', models.ForeignKey(to='patronazna_sluzba_app.Kontaktna_oseba')),
                ('pacient', models.ForeignKey(to='patronazna_sluzba_app.Pacient')),
            ],
        ),
        migrations.CreateModel(
            name='Vodja_PS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_vodje_PS', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('sifra_izvajalca_ZS', models.ForeignKey(to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vrsta_obiska',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ime', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Zdravilo',
            fields=[
                ('nacionalna_sifra', models.IntegerField(serialize=False, primary_key=True)),
                ('ime', models.CharField(max_length=100, null=True)),
                ('poimenovanje', models.CharField(max_length=100)),
                ('kratko_poimenovanje', models.CharField(max_length=100, null=True)),
                ('oznaka_EAN', models.IntegerField()),
                ('oglasevanje_dovoljeno', models.BooleanField(default=False)),
                ('originator', models.BooleanField(default=False)),
                ('slovenski_naziv_farmacevtske_oblike', models.CharField(max_length=100, null=True)),
                ('kolicina_osnovne_enote_za_aplikacijo', models.IntegerField(default=-1)),
                ('oznaka_osnovne_enote_za_aplikacijo', models.CharField(max_length=100, null=True)),
                ('pakiranje', models.CharField(max_length=100, null=True)),
                ('sifra_pravnega_statusa', models.IntegerField()),
                ('naziv_pravnega_statusa', models.CharField(max_length=100, null=True)),
                ('naziv_poti_uporabe', models.CharField(max_length=100, null=True)),
                ('sifra_rezima_izdaje', models.IntegerField()),
                ('oznaka_rezima_izdaje', models.CharField(max_length=100, null=True)),
                ('naziv_rezima_izdaje', models.CharField(max_length=100, null=True)),
                ('sifra_prisotnosti_na_trgu', models.IntegerField(null=True)),
                ('izdaja_na_posebni_zdravniski_recept', models.CharField(max_length=100, null=True)),
                ('trigonik_absolutna_prepoved_upravljanja_vozil', models.CharField(max_length=100, null=True)),
                ('trigonik_relativna_prepoved_upravljanja_vozil', models.CharField(max_length=100, null=True)),
                ('omejena_kolicina_enkratne_izdaje', models.CharField(max_length=100, null=True)),
                ('oznaka_vrste_postopka', models.CharField(max_length=100, null=True)),
                ('oznaka_ATC', models.CharField(max_length=100, null=True)),
                ('vir_podatka', models.CharField(max_length=100, null=True)),
                ('slovenski_opis_ATC', models.CharField(max_length=100, null=True)),
                ('latinski_opis_ATC', models.CharField(max_length=100, null=True)),
                ('angleski_opis_ATC', models.CharField(max_length=100, null=True)),
                ('aktivno_zdravilo', models.BooleanField(default=False)),
                ('sifra_liste', models.IntegerField()),
                ('oznaka_liste', models.CharField(max_length=100, null=True)),
                ('opis_omejitve_predpisovanja', models.CharField(max_length=100, null=True)),
                ('velja_od', models.CharField(max_length=100, null=True)),
                ('sifra_iz_seznama_B', models.IntegerField(null=True)),
                ('oznaka_iz_seznama_B', models.CharField(max_length=100, null=True)),
                ('opis_omejitve_predpisovanja_B', models.CharField(max_length=100, null=True)),
                ('velja_od_B', models.DateTimeField(null=True)),
                ('sifra_iz_seznama_A', models.IntegerField(null=True)),
                ('oznaka_iz_seznama_A', models.CharField(max_length=100, null=True)),
                ('opis_omejitve_predpisovanja_A', models.CharField(max_length=100, null=True)),
                ('velja_od_A', models.DateTimeField(null=True)),
                ('cena_na_debelo_regulirana', models.FloatField(null=True)),
                ('datum_veljavnosti_regulirane_cene', models.DateTimeField(null=True)),
                ('tip_regulirane_cene', models.CharField(max_length=100, null=True)),
                ('predviden_datum_konca_veljavnosti_regulirane_cene', models.DateTimeField(null=True)),
                ('vrsta_zdravila', models.CharField(max_length=100, null=True)),
                ('dogovorjena_cena', models.FloatField(null=True)),
                ('datum_veljavnosti_dogovorjene_cene', models.DateTimeField(null=True)),
                ('tip_dogovorjene_cene', models.CharField(max_length=100, null=True)),
                ('sifra_skupine_MZZ', models.IntegerField(null=True)),
                ('opis_skupine_MZZ', models.CharField(max_length=100, null=True)),
                ('najvisja_priznana_vrednost_zdravila_v_eur', models.FloatField(null=True)),
                ('datum_veljavnosti_NPV_zdravila', models.DateTimeField(null=True)),
                ('najvisja_priznana_vrednost_za_zivila', models.CharField(max_length=100, null=True)),
                ('datum_veljavnosti_NPV_zivila', models.DateTimeField(null=True)),
                ('primerno_za_INN_predpisovanje', models.CharField(max_length=100, null=True)),
                ('sifra_vrste_postopka', models.IntegerField(null=True)),
                ('naziv_vrste_postopka', models.CharField(max_length=100, null=True)),
                ('stevilka_dovoljenja', models.CharField(max_length=100, null=True)),
                ('datum_dovoljenja', models.DateTimeField(null=True)),
                ('datum_veljavnosti_dovoljenja', models.DateTimeField(null=True)),
                ('stevilka_uradnega_lista_objave', models.CharField(max_length=100, null=True)),
                ('datum_uradnega_lista_objave', models.DateTimeField(null=True)),
                ('datum_prenehanja_trzenja_zdravila', models.DateTimeField(null=True)),
                ('sifra_imetnika_dovoljenja', models.IntegerField(null=True)),
                ('naziv_imetnika_dovoljenja', models.CharField(max_length=100, null=True)),
                ('kolicina_za_preracun_DDO', models.IntegerField(null=True)),
                ('DDO', models.FloatField(null=True)),
                ('oznaka_merske_enote', models.CharField(max_length=100, null=True)),
                ('spletna_povezava_na_EMA', models.CharField(max_length=100, null=True)),
                ('spremljanje_varnosti', models.BooleanField(default=False)),
                ('sif_razp_zdr', models.CharField(max_length=100, null=True)),
                ('razpolozljivost_zdravila', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zdravilo_DN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delovni_nalog', models.ForeignKey(to='patronazna_sluzba_app.Delovni_nalog', null=True)),
                ('zdravilo', models.ForeignKey(to='patronazna_sluzba_app.Zdravilo', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zdravnik',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_zdravnika', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('sifra_izvajalca_ZS', models.ForeignKey(to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pacient',
            name='posta',
            field=models.ForeignKey(to='patronazna_sluzba_app.Posta', null=True),
        ),
        migrations.AddField(
            model_name='pacient',
            name='skrbnistvo',
            field=models.ForeignKey(to='patronazna_sluzba_app.Pacient', null=True),
        ),
        migrations.AddField(
            model_name='izvajalec_zs',
            name='posta',
            field=models.ForeignKey(to='patronazna_sluzba_app.Posta', null=True),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='izvajalec_zs',
            field=models.ForeignKey(to='patronazna_sluzba_app.Izvajalec_ZS'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='vodja_PS',
            field=models.ForeignKey(to='patronazna_sluzba_app.Vodja_PS'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='vrsta_obiska',
            field=models.ForeignKey(to='patronazna_sluzba_app.Vrsta_obiska'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='zdravnik',
            field=models.ForeignKey(to='patronazna_sluzba_app.Zdravnik'),
        ),
    ]
