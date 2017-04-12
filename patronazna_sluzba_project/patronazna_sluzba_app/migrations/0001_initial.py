# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 09:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='Pacient',
            fields=[
                ('uporabniski_profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('st_kartice', models.IntegerField(default=-1)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('naslov', models.CharField(max_length=100)),
                ('spol', models.CharField(choices=[('M', 'Moski'), ('Z', 'Zenska')], default='', max_length=1)),
                ('datum_rojstva', models.DateTimeField()),
                ('kontakt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Kontaktna_oseba')),
                ('skrbnistvo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Pacient')),
            ],
        ),
        migrations.CreateModel(
            name='Patronazna_sestra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_patronazne_sestre', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sodelavec_ZD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_sodelavca', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sorodstveno_razmerje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip_razmerja', models.CharField(max_length=100)),
                ('kontaktna_oseba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Kontaktna_oseba')),
                ('pacient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patronazna_sluzba_app.Pacient')),
            ],
        ),
        migrations.CreateModel(
            name='Vodja_PS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_vodje_PS', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zdravnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sifra_zdravnika', models.IntegerField(unique=True)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
