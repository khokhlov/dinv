# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 17:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securities', '0004_auto_20170217_2220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dividendhistory',
            options={'ordering': ['-date_registry_close'], 'verbose_name': '\u0414\u0438\u0432\u0438\u0434\u0435\u043d\u0434\u043d\u0430\u044f \u0432\u044b\u043f\u043b\u0430\u0442\u0430', 'verbose_name_plural': '\u0414\u0438\u0432\u0438\u0434\u0435\u043d\u0434\u043d\u044b\u0435 \u0432\u044b\u043f\u043b\u0430\u0442\u044b'},
        ),
    ]
