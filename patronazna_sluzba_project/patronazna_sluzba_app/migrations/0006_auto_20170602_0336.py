# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 03:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0005_auto_20170602_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_konec',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 3, 3, 36, 21, 873639)),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_zacetek',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 2, 3, 36, 21, 873617)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 3, 3, 36, 21, 872023)),
        ),
    ]
