# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-03 07:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='datum',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 4, 9, 37, 27, 517732)),
        ),
    ]
