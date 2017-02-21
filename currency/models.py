#coding: utf-8
from __future__ import unicode_literals

from django.db import models

class Currency(models.Model):
    class Meta:
        verbose_name = u'Валюта'
        verbose_name_plural = u'Валюты'
        
    code = models.CharField(max_length = 1024,
                            verbose_name = u'Код',
                            help_text  = u'Код валюты, не более 1024-х символов')
    
    short_name = models.CharField(max_length = 1024,
                            verbose_name = u'Краткое название',
                            help_text  = u'Краткое название, не более 1024-х символов')
    
    name = models.CharField(max_length = 1024,
                            verbose_name = u'Название',
                            help_text  = u'Название, не более 1024-х символов')
    
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u'%s' % self.code
    
    @staticmethod
    def get(code):
        return Currency.objects.filter(code = code)[0]


class CurrencyRate(models.Model):
    class Meta:
        verbose_name = u'Курс валюты'
        verbose_name_plural = u'Курсы валют'
        ordering = ['-date']
    
    currency1 = models.ForeignKey('Currency',
                              related_name = 'rates1',
                              verbose_name = u'Валюта 1')
    
    currency2 = models.ForeignKey('Currency',
                              related_name = 'rates2',
                              verbose_name = u'Валюта 2')
    
    rate = models.DecimalField(max_digits=35,
                               decimal_places=15,
                               verbose_name = u'Курс',
                               help_text = u'Курс валюты 1 в цене 2 (за сколько валюты 2 можно купить одну валюту 1)')
    
    date = models.DateField(verbose_name = u'Дата',
                            help_text = u'На какую дату курс')
    
    def __unicode__(self):
        return u'%s-%s(%s)' % (self.currency1, self.currency2, self.rate)
    
    @staticmethod
    def get(c1, c2, date):
        return CurrencyRate.objects.filter(currency1 = c1).filter(currency2 = c2).filter(date = date).all()[0]
    
    @staticmethod
    def has(c1, c2, date):
        return CurrencyRate.objects.filter(currency1 = c1).filter(currency2 = c2).filter(date = date).count() > 0
    
    @staticmethod
    def update(c1, c2, rate, date, create = False):
        dh = CurrencyRate()
        if not create and CurrencyRate.has(c1, c2, date):
            dh = CurrencyRate.get(c1, c2, date)
        else:
            dh.currency1 = c1
            dh.currency2 = c2
            dh.date = date
        dh.rate = rate
        dh.save()
        return dh
