# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 02:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0004_auto_20170601_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_konec',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 3, 2, 25, 9, 768734)),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_zacetek',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 2, 2, 25, 9, 768704)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 3, 2, 25, 9, 766911)),
        ),
        migrations.AlterUniqueTogether(
            name='porocilo_o_obisku',
            unique_together=set([]),
        ),
    ]
