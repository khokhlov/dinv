# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 18:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0005_auto_20170216_2132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shareitem',
            options={'verbose_name': '\u041f\u0430\u043a\u0435\u0442 \u0430\u043a\u0446\u0438\u0439', 'verbose_name_plural': '\u041f\u0430\u043a\u0435\u0442\u044b \u0430\u043a\u0446\u0438\u0439'},
        ),
        migrations.AlterModelOptions(
            name='shareitemhistory',
            options={'ordering': ['-date'], 'verbose_name': '\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u043f\u0430\u043a\u0435\u0442\u0430 \u0430\u043a\u0446\u0438\u0439', 'verbose_name_plural': '\u0418\u0441\u0442\u043e\u0440\u0438\u0438 \u043f\u0430\u043a\u0435\u0442\u043e\u0432 \u0430\u043a\u0446\u0438\u0439'},
        ),
        migrations.AlterModelOptions(
            name='sharetransaction',
            options={'ordering': ['-date'], 'verbose_name': '\u0421\u0434\u0435\u043b\u043a\u0430', 'verbose_name_plural': '\u0421\u0434\u0435\u043b\u043a\u0438'},
        ),
    ]
