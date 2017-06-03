# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-03 22:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0002_auto_20170602_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='polje_v_porocilu',
            name='enkraten_vnos',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_konec',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 4, 22, 35, 41, 88906)),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_zacetek',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 3, 22, 35, 41, 88884)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 4, 22, 35, 41, 87211)),
        ),
    ]
