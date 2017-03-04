# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securities', '0008_auto_20170304_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='bondhistory',
            name='yield_close',
            field=models.DecimalField(blank=True, decimal_places=15, help_text='\u0414\u043e\u0445\u043e\u0434\u043d\u043e\u0441\u0442\u044c \u043f\u043e \u0446\u0435\u043d\u0435 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0441\u0434\u0435\u043b\u043a\u0438, % \u0433\u043e\u0434\u043e\u0432\u044b\u0445', max_digits=35, null=True, verbose_name='\u0414\u043e\u0445\u043e\u0434\u043d\u043e\u0441\u0442\u044c, % \u0433\u043e\u0434\u043e\u0432\u044b\u0445 - \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0441\u0434\u0435\u043b\u043a\u0438'),
        ),
    ]