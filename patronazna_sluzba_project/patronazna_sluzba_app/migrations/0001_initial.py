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
            name='Pacient',
            fields=[
                ('uporabniski_profil', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('telefonska_st', models.CharField(max_length=15)),
                ('naslov', models.CharField(max_length=100)),
                ('datum_rojstva', models.DateTimeField()),
                ('spol', models.CharField(default=b'', max_length=1, choices=[(b'M', b'Moski'), (b'Z', b'Zenska')])),
                ('skrbnistvo', models.ForeignKey(to='patronazna_sluzba_app.Pacient')),
            ],
        ),
        migrations.CreateModel(
            name='Patronazna_sestra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_patronazne_sestre', models.IntegerField()),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sodelavec_ZD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_sodelavca', models.IntegerField()),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sorodstveno_razmerje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vodja_PS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_vodje_PS', models.IntegerField()),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zdravnik',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sifra_zdravnika', models.IntegerField()),
                ('telefonska_st', models.CharField(max_length=15)),
                ('uporabniski_profil', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
