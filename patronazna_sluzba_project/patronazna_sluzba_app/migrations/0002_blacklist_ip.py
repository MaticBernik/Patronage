# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='blacklist_ip',
            fields=[
                ('naslov_ip', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('cas_vpisa', models.DateTimeField(default=datetime.datetime(2017, 4, 13, 10, 48, 3, 124042))),
            ],
        ),
    ]
