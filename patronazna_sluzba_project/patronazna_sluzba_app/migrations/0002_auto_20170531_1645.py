# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 16:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delovni_nalog',
            name='aktiven',
            field=models.NullBooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_konec',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 1, 16, 45, 5, 128312)),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_zacetek',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 31, 16, 45, 5, 128287)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 1, 16, 45, 5, 126506)),
        ),
    ]