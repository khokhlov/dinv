# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 14:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portfolio', '0002_auto_20170217_2137'),
        ('currency', '0002_currencyrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(0, '\u041f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (1, '\u0421\u043f\u0438\u0441\u0430\u043d\u0438\u0435')], help_text='\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435: \u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435/\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435', verbose_name='\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435')),
                ('volume', models.DecimalField(decimal_places=15, help_text='\u0421\u0443\u043c\u043c\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u0432 \u0432\u0430\u043b\u044e\u0442\u0435 \u0441\u0447\u0435\u0442\u0430', max_digits=35, verbose_name='\u0421\u0443\u043c\u043c\u0430')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='\u0414\u0430\u0442\u0430 \u0441\u0434\u0435\u043b\u043a\u0438', verbose_name='\u0414\u0430\u0442\u0430')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': '\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435 \u043f\u043e \u0441\u0447\u0435\u0442\u0443',
                'verbose_name_plural': '\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043f\u043e \u0441\u0447\u0435\u0442\u0443',
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435, \u043d\u0435 \u0431\u043e\u043b\u0435\u0435 1024-\u0445 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432', max_length=1024, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('volume', models.DecimalField(decimal_places=15, help_text='\u0421\u0443\u043c\u043c\u0430 \u0432 \u0432\u0430\u043b\u044e\u0442\u0435 \u0441\u0447\u0435\u0442\u0430', max_digits=35, verbose_name='\u0421\u0443\u043c\u043c\u0430')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='currency.Currency', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='portfolio.Portfolio', verbose_name='\u041f\u043e\u0440\u0442\u0444\u0435\u043b\u044c')),
            ],
            options={
                'verbose_name': '\u0421\u0447\u0435\u0442',
                'verbose_name_plural': '\u0421\u0447\u0435\u0442\u0430',
            },
        ),
        migrations.AddField(
            model_name='accounttransaction',
            name='account',
            field=models.ForeignKey(help_text='\u041f\u043e \u043a\u0430\u043a\u043e\u043c\u0443 \u0441\u0447\u0435\u0442\u0443 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435', on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.BankAccount', verbose_name='\u0421\u0447\u0435\u0442'),
        ),
        migrations.AlterUniqueTogether(
            name='bankaccount',
            unique_together=set([('name', 'portfolio')]),
        ),
    ]
