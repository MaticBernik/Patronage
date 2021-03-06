# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 20:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0003_auto_20170606_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_konec',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 20, 58, 59, 196815)),
        ),
        migrations.AlterField(
            model_name='nadomescanje',
            name='datum_zacetek',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 7, 20, 58, 59, 194885)),
        ),
        migrations.AlterUniqueTogether(
            name='meritev',
            unique_together=set([]),
        ),
    ]
