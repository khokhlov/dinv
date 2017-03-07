# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0005_auto_20170306_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='bondtransaction',
            name='accint',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='\u041d\u0430\u043a\u043e\u043f\u043b\u0435\u043d\u043d\u044b\u0439 \u043a\u0443\u043f\u043e\u043d\u043d\u044b\u0439 \u0434\u043e\u0445\u043e\u0434 (\u041d\u041a\u0414), \u043f\u043e \u043e\u0434\u043d\u043e\u0439 \u0446\u0435\u043d\u043d\u043e\u0439 \u0431\u0443\u043c\u0430\u0433\u0435', max_digits=35, null=True, verbose_name='\u041d\u041a\u0414'),
        ),
    ]
