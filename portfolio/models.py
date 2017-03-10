#coding: utf-8
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal

class Portfolio(models.Model):
    class Meta:
        verbose_name = u'Инвестиционный портфель'
        verbose_name_plural = u'Инвестиционные портфели'
        
    name = models.CharField(max_length = 1024,
                            verbose_name = u'Портфель',
                            help_text  = u'Название портфеля, не более 1024 символа')
    
    created_date = models.DateTimeField(auto_now_add = True)
    
    modified_date = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u'%s' % self.name
    
    def shares_price_balance(self):
        p = Decimal(0)
        b = Decimal(0)
        for s in self.shares.all():
            p += s.last_history().price()
            b += s.balance()
        return p, b
    
    def shares_price(self):
        return self.shares_price_balance()[0]
    
    def shares_balance(self):
        return self.shares_price_balance()[1]
    
    def shares_yield(self):
        return self.shares_balance() / self.shares_price() * Decimal(100.0)
    
    def shares_dividends(self):
        d = Decimal(0)
        for s in self.shares.all():
            d += s.price_all_income()
        return d
    
    def shares_balance_dividends(self):
        return self.shares_balance() + self.shares_dividends()
    
    def shares_yield_dividends(self):
        return self.shares_balance_dividends() / self.shares_price() * Decimal(100.0)
    
    
    def shares_info(self):
        sp = self.shares_price()
        ret = {
            'shares_price': sp,
            'shares_balance': self.shares_balance(),
            'shares_yield': self.shares_yield(),
            'shares': [],
            }
        
        for s in self.shares.all():
            s.portion = s.last_history().price() / sp * Decimal(100.0)
            ret['shares'].append(s)
        return ret
    
    """BONDS"""
    def bonds_price_balance(self):
        p = Decimal(0)
        b = Decimal(0)
        for s in self.bonds.all():
            p += s.last_history().price()
            b += s.balance()
        return p, b
    
    def bonds_price(self):
        return self.bonds_price_balance()[0]
    
    def bonds_balance(self):
        return self.bonds_price_balance()[1]
    
    def bonds_yield(self):
        return self.bonds_balance() / self.bonds_price() * Decimal(100.0)
    
    def bonds_coupons(self):
        d = Decimal(0)
        for s in self.bonds.all():
            d += s.price_all_income()
        return d
    
    def bonds_yield_coupons(self):
        return self.bonds_coupons() / self.bonds_price() * Decimal(100.0)
    
    def bonds_cost(self):
        p = Decimal(0)
        for s in self.bonds.all():
            p += s.last_history().cost()
        return p
    
    
    