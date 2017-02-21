#coding: utf-8
from __future__ import unicode_literals

import datetime

import datetime
from decimal import Decimal
from django.db import models
import django
from django.db.models.signals import post_save, post_delete
from django.db import models

class BankAccount(models.Model):
    class Meta:
        verbose_name = u'Счет'
        verbose_name_plural = u'Счета'
        unique_together = ('name', 'portfolio')
    
    
    name = models.CharField(max_length = 1024,
                            verbose_name = u'Название',
                            help_text  = u'Название, не более 1024-х символов')
    
    currency = models.ForeignKey('currency.Currency',
                              related_name = 'accounts',
                              verbose_name = u'Валюта')
    
    portfolio = models.ForeignKey('portfolio.Portfolio',
                                  related_name = 'accounts',
                                  verbose_name = u'Портфель')
    
    volume = models.DecimalField(max_digits=35,
                                decimal_places=15,
                                verbose_name = u'Сумма',
                                help_text = u'Сумма в валюте счета')
    
    def __unicode__(self):
        return u'%s (%s)' % (self.portfolio, self.name)
    
    def get_volume_and_price(self, date):
        volume = Decimal("0")
        for t in self.transactions.filter(date__lte = datetime.datetime.combine(date, datetime.datetime.max.time())):
            if t.action == AccountTransaction.TYPE_DEBIT:
                volume += t.volume
            else:
                volume -= t.volume
        return volume
    
    def update_from_transactions(self):
        self.volume = self.get_volume_and_price(django.utils.timezone.now().date())
        self.save()

class AccountTransaction(models.Model):
    class Meta:
        ordering = ['-date', ]
        verbose_name = u'Действие по счету'
        verbose_name_plural = u'Действия по счету'
        
    TYPE_DEBIT = 0
    TYPE_CREDIR  = 1
    
    TYPE = (
        (TYPE_DEBIT, u'Пополнение'),
        (TYPE_CREDIR,  u'Списание')
        )
    
    account = models.ForeignKey('BankAccount',
                              verbose_name = u'Счет',
                              related_name = 'transactions',
                              help_text = u'По какому счету действие')
    
    action = models.IntegerField(choices = TYPE,
                               verbose_name = u'Действие',
                               help_text = u'Действие: пополнение/списание'
                               )
    
    volume = models.DecimalField(max_digits=35,
                                decimal_places=15,
                                verbose_name = u'Сумма',
                                help_text = u'Сумма действия в валюте счета')
    
    date = models.DateTimeField(default = django.utils.timezone.now,
                                verbose_name = u'Дата',
                                help_text = u'Дата сделки')
    
    comment = models.TextField(blank = True,
                               null = True,
                               verbose_name = u'Комментарий')
    
    @staticmethod
    def create(account, action, volume, price, date, comment):
        s = AccountTransaction()
        s.account = account
        s.action = action
        s.volume = volume
        s.date = date
        s.comment = comment
        s.save()
        return s

def update_from_transactions(sender, instance, **kwargs):
    instance.account.update_from_transactions()
    
post_save.connect(update_from_transactions, sender = AccountTransaction)
post_delete.connect(update_from_transactions, sender = AccountTransaction)
