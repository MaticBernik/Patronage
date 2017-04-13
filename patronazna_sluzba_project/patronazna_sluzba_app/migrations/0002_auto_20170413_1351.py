# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patronazna_sluzba_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delovni_nalog',
            name='cas_obiskov_tip',
            field=models.CharField(choices=[('Interval', 'Casovni interval med zaporednima obiskoma v dnevih'), ('Obdobje', 'Stevilo dni, v katerih mora biti obisk opravljen')], max_length=10),
        ),
        migrations.AlterField(
            model_name='pacient',
            name='spol',
            field=models.CharField(choices=[('M', 'Moski'), ('Z', 'Zenska')], max_length=1),
        ),
    ]
