# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0010_auto_20170220_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharetransaction',
            name='key',
            field=models.CharField(blank=True, help_text='\u0423\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u0441\u0434\u0435\u043b\u043a\u0438 \u0434\u043b\u044f \u0430\u0432\u0442\u043e\u043f\u0430\u0440\u0441\u0438\u043d\u0433\u0430', max_length=1024, null=True, verbose_name='\u041a\u043b\u044e\u0447 \u0441\u0434\u0435\u043b\u043a\u0438'),
        ),
    ]
