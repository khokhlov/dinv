# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('securities', '0002_auto_20170216_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='board',
            options={'verbose_name': '\u0420\u0435\u0436\u0438\u043c \u0442\u043e\u0440\u0433\u043e\u0432', 'verbose_name_plural': '\u0420\u0435\u0436\u0438\u043c\u044b \u0442\u043e\u0440\u0433\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='share',
            options={'verbose_name': '\u0410\u043a\u0446\u0438\u044f', 'verbose_name_plural': '\u0410\u043a\u0446\u0438\u0438'},
        ),
        migrations.AlterModelOptions(
            name='sharehistory',
            options={'verbose_name': '\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0430\u043a\u0446\u0438\u0438', 'verbose_name_plural': '\u0418\u0441\u0442\u043e\u0440\u0438\u0438 \u0430\u043a\u0446\u0438\u0439'},
        ),
        migrations.AddField(
            model_name='share',
            name='dividend_flag',
            field=models.BooleanField(default=False, help_text='\u0414\u0438\u0432\u0438\u0434\u0435\u043d\u0434\u043d\u0430\u044f \u0430\u043a\u0446\u0438\u044f', verbose_name='\u0414\u0438\u0432\u0438\u0434\u0435\u043d\u0434\u043d\u0430\u044f'),
        ),
    ]
