# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 05:34
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bolezen',
            fields=[
                ('sifra', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('ime', models.CharField(max_length=100)),
                ('opis', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delovni_nalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_prvega_obiska', models.DateTimeField(null=True)),
                ('st_obiskov', models.IntegerField(null=True)),
                ('cas_obiskov_tip', models.CharField(blank=True, choices=[(b'Interval', b'Casovni interval med zaporednima obiskoma v dnevih'), (b'Obdobje', b'Stevilo dni, v katerih mora biti obisk opravljen')], max_length=10)),
                ('cas_obiskov_dolzina', models.IntegerField(null=True)),
                ('bolezen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Bolezen')),
            ],
        ),
        migrations.CreateModel(
            name='Izvajalec_ZS',
            fields=[
                ('st_izvajalca', models.IntegerField(primary_key=True, serialize=False)),
                ('naziv', models.CharField(max_length=100)),
                ('naslov', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kontaktna_oseba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=100)),
                ('priimek', models.CharField(max_length=100)),
                ('naslov', models.CharField(max_length=100)),
                ('telefon', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=100)),
                ('proizvajalec', models.CharField(max_length=100)),
                ('opis', models.CharField(max_length=500)),
                ('kolicina_osnovne_enote', models.IntegerField(default=-1)),
                ('oznaka_osnovne_enote', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material_DN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.IntegerField(default=1)),
                ('delovni_nalog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Delovni_nalog')),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Material')),
            ],
        ),
        migrations.CreateModel(
            name='Meritev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra', models.IntegerField()),
                ('opis', models.CharField(max_length=500)),
                ('porocilo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nadomescanje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_zacetek', models.DateTimeField(default=datetime.datetime(2017, 5, 12, 7, 34, 18, 477404))),
                ('datum_konec', models.DateTimeField(default=datetime.datetime(2017, 5, 13, 7, 34, 18, 477431))),
            ],
        ),
        migrations.CreateModel(
            name='Obisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField(null=True)),
                ('obvezen_obisk', models.BooleanField(default=0)),
                ('delovni_nalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Delovni_nalog')),
            ],
        ),
        migrations.CreateModel(
            name='Okolis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pacient',
            fields=[
                ('st_kartice', models.CharField(default=-1, max_length=12, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(b'^[0-9]*$', b'Dovoljena zgolj stevilska vrednost.'), django.core.validators.MinLengthValidator(12, b'Stevilka kartica je dolzine 12 znakov.'), django.core.validators.MaxLengthValidator(12, b'Stevilka kartica je dolzine 12 znakov.')])),
                ('telefonska_st', models.CharField(max_length=15)),
                ('naslov', models.CharField(max_length=100)),
                ('spol', models.CharField(choices=[(b'M', b'Moski'), (b'Z', b'Zenska')], max_length=1)),
                ('datum_rojstva', models.DateTimeField()),
                ('ime', models.CharField(max_length=100)),
                ('priimek', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('kontakt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Kontaktna_oseba')),
                ('okolis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Okolis')),
            ],
        ),
        migrations.CreateModel(
            name='Pacient_DN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delovni_nalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Delovni_nalog')),
                ('pacient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Pacient')),
            ],
        ),
        migrations.CreateModel(
            name='Patronazna_sestra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_patronazne_sestre', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('okolis', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Okolis')),
                ('sifra_izvajalca_ZS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateTimeField(default=datetime.datetime(2017, 5, 13, 7, 34, 18, 475488))),
                ('planirani_obisk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Obisk')),
            ],
        ),
        migrations.CreateModel(
            name='Posta',
            fields=[
                ('postna_st', models.IntegerField(primary_key=True, serialize=False)),
                ('naziv_poste', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sodelavec_ZD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_sodelavca', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('sifra_izvajalca_ZS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sorodstveno_razmerje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip_razmerja', models.CharField(max_length=100)),
                ('kontakt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Kontaktna_oseba')),
                ('pacient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Pacient')),
            ],
        ),
        migrations.CreateModel(
            name='Vodja_PS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_vodje_PS', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('sifra_izvajalca_ZS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vrsta_obiska',
            fields=[
                ('sifra', models.IntegerField(primary_key=True, serialize=False)),
                ('ime', models.CharField(choices=[(b'I', b'Aplikacija inekcij'), (b'K', b'Odvzem krvi'), (b'Z', b'Kontrola zdravstvenega stanja'), (b'N', b'Obisk nosecnice'), (b'O', b'Obisk otrocnice in novorojencka'), (b'S', b'Obisk starostnika')], max_length=10)),
                ('tip', models.CharField(choices=[(b'P', b'Preventivni obisk'), (b'K', b'Kurativni obisk')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zdravilo',
            fields=[
                ('nacionalna_sifra', models.IntegerField(primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.IntegerField(default=1)),
                ('delovni_nalog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Delovni_nalog')),
                ('zdravilo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Zdravilo')),
            ],
        ),
        migrations.CreateModel(
            name='Zdravnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_zdravnika', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('sifra_izvajalca_ZS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Izvajalec_ZS')),
                ('uporabniski_profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pacient',
            name='posta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Posta'),
        ),
        migrations.AddField(
            model_name='pacient',
            name='skrbnistvo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Pacient'),
        ),
        migrations.AddField(
            model_name='pacient',
            name='sorodstvo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Sorodstveno_razmerje'),
        ),
        migrations.AddField(
            model_name='pacient',
            name='uporabniski_profil',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='okolis',
            name='posta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Posta'),
        ),
        migrations.AddField(
            model_name='obisk',
            name='p_sestra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Patronazna_sestra'),
        ),
        migrations.AddField(
            model_name='nadomescanje',
            name='nadomestna_sestra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Patronazna_sestra'),
        ),
        migrations.AddField(
            model_name='nadomescanje',
            name='sestra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nadomescanje_requests_created', to='patronazna_sluzba_app.Patronazna_sestra'),
        ),
        migrations.AddField(
            model_name='meritev',
            name='vrsta_obiska',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Vrsta_obiska'),
        ),
        migrations.AddField(
            model_name='kontaktna_oseba',
            name='sorodstvo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Sorodstveno_razmerje'),
        ),
        migrations.AddField(
            model_name='izvajalec_zs',
            name='posta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Posta'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='izvajalec_zs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Izvajalec_ZS'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='vodja_PS',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Vodja_PS'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='vrsta_obiska',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Vrsta_obiska'),
        ),
        migrations.AddField(
            model_name='delovni_nalog',
            name='zdravnik',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Zdravnik'),
        ),
        migrations.AlterUniqueTogether(
            name='okolis',
            unique_together=set([('posta', 'ime')]),
        ),
        migrations.AlterUniqueTogether(
            name='nadomescanje',
            unique_together=set([('sestra', 'datum_zacetek', 'datum_konec')]),
        ),
        migrations.AlterUniqueTogether(
            name='meritev',
            unique_together=set([('sifra', 'vrsta_obiska')]),
        ),
    ]
