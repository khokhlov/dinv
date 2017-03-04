# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('securities', '0006_auto_20170303_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_id', models.CharField(blank=True, help_text='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u0444\u0438\u043d\u0430\u043d\u0441\u043e\u0432\u043e\u0433\u043e \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430', max_length=128, null=True, verbose_name='\u041a\u043e\u0434 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430')),
                ('short_name', models.CharField(blank=True, help_text='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435', max_length=1024, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('isin', models.CharField(blank=True, help_text='ISIN \u043a\u043e\u0434', max_length=128, null=True, verbose_name='ISIN \u043a\u043e\u0434')),
                ('face_value', models.DecimalField(blank=True, decimal_places=15, help_text='\u041d\u043e\u043c\u0438\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', max_digits=35, null=True, verbose_name='\u041d\u043e\u043c\u0438\u043d\u0430\u043b')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='securities.Board', verbose_name='\u0420\u0435\u0436\u0438\u043c \u0442\u043e\u0440\u0433\u043e\u0432')),
            ],
            options={
                'verbose_name': '\u041e\u0431\u043b\u0430\u0433\u0430\u0446\u0438\u044f',
                'verbose_name_plural': '\u041e\u0431\u043b\u0438\u0433\u0430\u0446\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='BondHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0442\u043e\u0440\u0433\u043e\u0432')),
                ('num_trades', models.IntegerField(blank=True, help_text='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0434\u0435\u043b\u043e\u043a \u0437\u0430 \u0434\u0435\u043d\u044c, \u0448\u0442\u0443\u043a', null=True, verbose_name='\u0421\u0434\u0435\u043b\u043e\u043a, \u0448\u0442.')),
                ('value', models.DecimalField(blank=True, decimal_places=15, help_text='\u041e\u0431\u044a\u0435\u043c \u0441\u0434\u0435\u043b\u043e\u043a \u0432 \u0432\u0430\u043b\u044e\u0442\u0435 \u0446\u0435\u043d\u043d\u043e\u0439 \u0431\u0443\u043c\u0430\u0433\u0438', max_digits=35, null=True, verbose_name='\u041e\u0431\u044a\u0435\u043c')),
                ('open', models.DecimalField(blank=True, decimal_places=15, help_text='\u0426\u0435\u043d\u0430 \u043f\u0440\u0435\u0434\u0442\u043e\u0440\u0433\u043e\u0432\u043e\u0433\u043e \u043f\u0435\u0440\u0438\u043e\u0434\u0430/\u0426\u0435\u043d\u0430 \u0430\u0443\u043a\u0446\u0438\u043e\u043d\u0430 \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044f', max_digits=35, null=True, verbose_name='\u041f\u0435\u0440\u0432\u0430\u044f')),
                ('low', models.DecimalField(blank=True, decimal_places=15, help_text='\u0426\u0435\u043d\u0430 \u0441\u0434\u0435\u043b\u043a\u0438 \u043c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f', max_digits=35, null=True, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0443\u043c')),
                ('high', models.DecimalField(blank=True, decimal_places=15, help_text='\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0446\u0435\u043d\u0430 \u0441\u0434\u0435\u043b\u043a\u0438', max_digits=35, null=True, verbose_name='\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c')),
                ('close', models.DecimalField(blank=True, decimal_places=15, help_text='\u0426\u0435\u043d\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0441\u0434\u0435\u043b\u043a\u0438', max_digits=35, null=True, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f')),
                ('legal_close_price', models.DecimalField(blank=True, decimal_places=15, help_text='\u0426\u0435\u043d\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f', max_digits=35, null=True, verbose_name='\u0417\u0430\u043a\u0440\u044b\u0442\u0438\u044f')),
                ('war_price', models.DecimalField(blank=True, decimal_places=15, help_text='\u0421\u0440\u0435\u0434\u043d\u0435\u0432\u0437\u0432\u0435\u0448\u0435\u043d\u043d\u0430\u044f \u0446\u0435\u043d\u0430', max_digits=35, null=True, verbose_name='\u0421\u0440\u0432\u0437\u0432. \u0446\u0435\u043d\u0430')),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='securities.Bond', verbose_name='\u041e\u0431\u043b\u0438\u0433\u0430\u0446\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u043e\u0431\u043b\u0438\u0433\u0430\u0446\u0438\u0438',
                'verbose_name_plural': '\u0418\u0441\u0442\u043e\u0440\u0438\u0438 \u043e\u0431\u043b\u0438\u0433\u0430\u0446\u0438\u0439',
            },
        ),
        migrations.AlterUniqueTogether(
            name='bondhistory',
            unique_together=set([('trade_date', 'bond')]),
        ),
    ]