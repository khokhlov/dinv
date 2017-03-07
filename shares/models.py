#coding: utf-8

from __future__ import unicode_literals

import datetime
import csv
from decimal import Decimal
from django.db import models
import django
from django.db.models.signals import post_save, post_delete
from django.db import transaction

from dinv.utils import daterange
from securities.models import ShareHistory, Share
from securities.models import AbstractSecurityItem, AbstractItemTransaction, AbstractItemHistory, AbstractItemIncome

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'):unicode(value, 'utf-8') for key, value in row.iteritems()}


class ShareTransaction(AbstractItemTransaction):
    share_item = models.ForeignKey('ShareItem',
                              verbose_name = u'Актив',
                              related_name = 'transactions',
                              help_text = u'Сделка по какому активу')

    @property
    def sec_item(self): return self.share_item

    @staticmethod
    def create(share_item, action, volume, price, date, comment, key = None):
        s = ShareTransaction()
        s.share_item = share_item
        s.action = action
        s.volume = volume
        s.price = price
        s.date = date
        s.comment = comment
        s.key = key
        s.save()
        return s


    @staticmethod
    @transaction.atomic
    def load_csv(path, portfolio, cols):
        reader = UnicodeDictReader(open(path, 'r'), delimiter=str(u','), quotechar=str(u'"'))
        for row in reader:
            sec_id = row[cols['sec_id']]
            s = None
            try:
                s = Share.objects.filter(sec_id = sec_id)[0]
            except:
                print 'Share key error:', sec_id
            share_item = ShareItem.get_or_create(portfolio, s)
            
            # сначала проверяем ключ
            key = row[cols['key']]
            if ShareTransaction.objects.filter(share_item = share_item).filter(key = key).count() > 0:
                print 'Skip transaction with key:', key
                continue
            
            action = ShareTransaction.TYPE_SELL
            if row[cols['action']] == cols['action_buy']:
                action = ShareTransaction.TYPE_BUY
            print row[cols['date']]
            date = datetime.datetime.strptime(row[cols['date']], "%d.%m.%Y %H:%M:%S")
            volume = int(row[cols['volume']])
            price = Decimal(row[cols['price']].replace(',', '.'))
            print ShareTransaction.create(share_item, action, volume, price, date, '', key)

class ShareItemHistory(AbstractItemHistory):
    class Meta:
        unique_together = ('share_item', 'date')
        ordering = ['-date', ]
        verbose_name = u'История пакета акций'
        verbose_name_plural = u'Истории пакетов акций'

    
    @property
    def sec_item(self): return self.share_item
    
    share_item = models.ForeignKey('ShareItem',
                              verbose_name = u'Актив',
                              related_name = 'history',
                              help_text = u'История актива')
        
    @staticmethod
    def get(share_item, date):
        return ShareItemHistory.objects.filter(share_item = share_item, date = date).all()[0]
    
    @staticmethod
    def has(share_item, date):
        return ShareItemHistory.objects.filter(share_item = share_item, date = date).count() > 0
    
    @staticmethod
    def update(share_item, date, create = False):
        if not create and not ShareHistory.has(share_item.share, date):
            return None

        sih = ShareItemHistory()
        if not create and ShareItemHistory.has(share_item, date):
            sih = ShareItemHistory.get(share_item, date)
        else:
            sih.share_item = share_item
            sih.date = date
        sih.legal_close_price = ShareHistory.get(share_item.share, date).legal_close_price
        sih.volume, sih.avg_price = share_item.get_volume_and_price(date)
        sih.save()
        return sih
    
    @staticmethod
    def create(share_item, date):
        return ShareItemHistory.update(share_item, date, True)

class ShareItemDividend(AbstractItemIncome):
    class Meta:
        ordering = ['-dividend__date_registry_close', ]
        unique_together = ('share_item', 'dividend')
        verbose_name = u'Выплаченный дивиденд'
        verbose_name_plural = u'Выплаченные дивиденды'
    
    @property
    def sec_item(self): return self.share_item
    
    share_item = models.ForeignKey('ShareItem',
                              verbose_name = u'Актив',
                              related_name = 'dividends',
                              help_text = u'История дивидендов')
                              
    dividend = models.ForeignKey('securities.DividendHistory',
                              verbose_name = u'Дивиденд')
    
    @staticmethod
    def has(share_item, dividend):
        return ShareItemDividend.objects.filter(share_item = share_item).filter(dividend = dividend).count() > 0
    
    @staticmethod
    def get(share_item, dividend):
        return ShareItemDividend.objects.filter(share_item = share_item).filter(dividend = dividend)[0]


class ShareItem(AbstractSecurityItem):
    class Meta:
        unique_together = ('share', 'portfolio')
        verbose_name = u'Пакет акций'
        verbose_name_plural = u'Пакеты акций'

    TransactionModel = ShareTransaction
    HistoryModel = ShareItemHistory
    IncomeModel = ShareItemDividend

    @property
    def sec(self): return self.share

    @property
    def income(self): return self.dividends


    share = models.ForeignKey('securities.Share',
                              verbose_name = u'Акция')
    
    portfolio = models.ForeignKey('portfolio.Portfolio',
                                  related_name = 'shares',
                                  verbose_name = u'Портфель')

    def update_dividends(self, date = django.utils.timezone.now().date() - datetime.timedelta(1)):
        date_max = datetime.datetime.combine(date, datetime.datetime.max.time())
        date_min = datetime.datetime.combine(self.first_transaction().date.date(), datetime.datetime.min.time())
        ds = self.share.dividends.filter(date_registry_close__lte = date_max).filter(date_registry_close__gte = date_min)
        for d in ds:
            sid = ShareItemDividend()
            sid.share_item = self
            sid.dividend = d
            sid.checked = False
            if ShareItemDividend.has(self, d):
                sid = ShareItemDividend.get(self, d)
            if sid.checked:
                continue
            sid.price_no_tax = d.dividend * self.volume
            sid.percent = Decimal(sid.price() / self.last_history_date(d.date_registry_close).price() * Decimal(100.0))
            sid.save()
    
    @staticmethod
    def get(portfolio, share):
        return ShareItem.objects.filter(portfolio = portfolio).filter(share = share)[0]
    
    @staticmethod
    def has(portfolio, share):
        return ShareItem.objects.filter(portfolio = portfolio).filter(share = share).count() > 0
    
    @staticmethod
    def get_or_create(portfolio, share):
        if ShareItem.has(portfolio, share):
            return ShareItem.get(portfolio, share)
        s = ShareItem()
        s.portfolio = portfolio
        s.share = share
        s.volume = 0
        s.avg_price = Decimal("0")
        s.save()
        return s



"""
class ShareItem(models.Model):
    class Meta:
        unique_together = ('share', 'portfolio')
        verbose_name = u'Пакет акций'
        verbose_name_plural = u'Пакеты акций'

    
    
    
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество акций')
    
    avg_price = models.DecimalField(max_digits=35,
                                    decimal_places=15,
                                    verbose_name = u'Средняя',
                                    help_text = u'Средняя цена')
    
    @staticmethod
    def get(portfolio, share):
        return ShareItem.objects.filter(portfolio = portfolio).filter(share = share)[0]
    
    @staticmethod
    def has(portfolio, share):
        return ShareItem.objects.filter(portfolio = portfolio).filter(share = share).count() > 0
    
    @staticmethod
    def get_or_create(portfolio, share):
        if ShareItem.has(portfolio, share):
            return ShareItem.get(portfolio, share)
        s = ShareItem()
        s.portfolio = portfolio
        s.share = share
        s.volume = 0
        s.avg_price = Decimal("0")
        s.save()
        return s
    
    def __unicode__(self):
        return u'%s (%s)' % (self.portfolio, self.share)
    
    def percent(self):
        return self.balance() / self.price() * Decimal(100.0)
        
    def price(self):
        return self.avg_price * self.volume
    
    def balance(self):
        return self.last_history().price() - self.price()
    
    def get_volume_and_price(self, date):
        volume = 0
        volume_plus = 0
        price = Decimal()
        for t in self.transactions.filter(date__lte = datetime.datetime.combine(date, datetime.datetime.max.time())):
            if t.action == ShareTransaction.TYPE_BUY:
                volume += t.volume
                volume_plus += t.volume
                price  += t.total_price()
            else:
                volume -= t.volume
        avg_price = 0
        if volume_plus > 0:
            avg_price = price / volume_plus
        else:
            avg_price = 0
        return volume, avg_price
    
    def update_from_transactions(self):
        self.volume, self.avg_price = self.get_volume_and_price(django.utils.timezone.now().date())
        self.save()
    
    def first_transaction(self):
        return self.transactions.order_by('date').all()[0]
    
    def last_history(self):
        return self.history.latest('date')
    
    def last_history_date(self, date):
        return self.history.filter(date__lte = date).order_by('-date')[0]
    
    def update_history(self, date = django.utils.timezone.now().date() - datetime.timedelta(1)):
        first_date = self.first_transaction().date.date()
        for d in daterange(first_date, date):
            print 'Updating date %s' % d
            print ShareItemHistory.update(self, d)
    
    
    def update_dividends(self, date = django.utils.timezone.now().date() - datetime.timedelta(1)):
        date_max = datetime.datetime.combine(date, datetime.datetime.max.time())
        date_min = datetime.datetime.combine(self.first_transaction().date.date(), datetime.datetime.min.time())
        ds = self.share.dividends.filter(date_registry_close__lte = date_max).filter(date_registry_close__gte = date_min)
        for d in ds:
            sid = ShareItemDividend()
            sid.share_item = self
            sid.dividend = d
            sid.checked = False
            if ShareItemDividend.has(self, d):
                sid = ShareItemDividend.get(self, d)
            if sid.checked:
                continue
            sid.price_no_tax = d.dividend * self.volume
            sid.percent = Decimal(sid.price() / self.last_history_date(d.date_registry_close).price() * Decimal(100.0))
            sid.save()
   
    def price_all_dividends(self):
        price = Decimal(0)
        for d in self.dividends.all():
            price += d.price()
        return price
    
    def dividend_yield(self):
        return self.price_all_dividends() / self.price() * Decimal(100.0)
    
    def balance_with_dividends(self):
        return self.balance() + self.price_all_dividends()
    
    def percent_with_dividends(self):
        return self.balance_with_dividends() / self.price() * Decimal(100.0)
            
"""
    

def update_from_transactions(sender, instance, **kwargs):
    instance.share_item.update_from_transactions()
    
post_save.connect(update_from_transactions, sender = ShareTransaction)
post_delete.connect(update_from_transactions, sender = ShareTransaction)

"""
class ShareItemDividend(models.Model):
    class Meta:
        ordering = ['-dividend__date_registry_close', ]
        unique_together = ('share_item', 'dividend')
        verbose_name = u'Выплаченный дивиденд'
        verbose_name_plural = u'Выплаченные дивиденды'
        
    share_item = models.ForeignKey('ShareItem',
                              verbose_name = u'Актив',
                              related_name = 'dividends',
                              help_text = u'История дивидендов')
                              
    dividend = models.ForeignKey('securities.DividendHistory',
                              verbose_name = u'Дивиденд')
    
    price_no_tax = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               verbose_name = u'Сумма выплат',
                               help_text = u'Сумма выплат без налога')
                               
    tax = models.DecimalField(default = Decimal("13"),
                                max_digits=35,
                                decimal_places=15,
                               verbose_name = u'НДФЛ, %',
                               help_text = u'Величина налога')
    
    checked = models.BooleanField(default = False,
                                  verbose_name = u'Подтверждена',
                                  help_text = u'Подтверждение получения дивидендов на счет')
    
    percent = models.DecimalField(max_digits=35,
                                decimal_places=15,
                                blank = True,
                               null = True,
                               verbose_name = u'Доходность, %',
                               help_text = u'Доходность на дату выплаты с учетом налога, %')
    
    def price(self):
        return self.price_no_tax * (Decimal(100.0) - self.tax) / Decimal(100.0)
    
    
    @staticmethod
    def has(share_item, dividend):
        return ShareItemDividend.objects.filter(share_item = share_item).filter(dividend = dividend).count() > 0
    
    @staticmethod
    def get(share_item, dividend):
        return ShareItemDividend.objects.filter(share_item = share_item).filter(dividend = dividend)[0]
"""    
                              
"""
class ShareItemHistory(models.Model):
    class Meta:
        ordering = ['-date', ]
        unique_together = ('share_item', 'date')
        verbose_name = u'История пакета акций'
        verbose_name_plural = u'Истории пакетов акций'
    
    share_item = models.ForeignKey('ShareItem',
                              verbose_name = u'Актив',
                              related_name = 'history',
                              help_text = u'История актива')
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество акций')
    
    legal_close_price = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               verbose_name = u'Закрытия',
                               help_text = u'Цена закрытия')
    
    avg_price = models.DecimalField(max_digits=35,
                                    decimal_places=15,
                                    verbose_name = u'Средняя',
                                    help_text = u'Средняя цена')
    
    date = models.DateField(verbose_name = u'Дата торгов')
    
    def price(self):
        return self.legal_close_price * self.volume
    
    def buy_price(self):
        return self.avg_price * self.volume
    
    def balance(self):
        return self.price() - self.buy_price()
    
    def __unicode__(self):
        return u'%s - %s - %s' % (self.share_item, self.date, self.price())
    
    @staticmethod
    def get(share_item, date):
        return ShareItemHistory.objects.filter(share_item = share_item, date = date).all()[0]
    
    @staticmethod
    def has(share_item, date):
        return ShareItemHistory.objects.filter(share_item = share_item, date = date).count() > 0
    
    @staticmethod
    def update(share_item, date, create = False):
        if not create and not ShareHistory.has(share_item.share, date):
            return None

        sih = ShareItemHistory()
        if not create and ShareItemHistory.has(share_item, date):
            sih = ShareItemHistory.get(share_item, date)
        else:
            sih.share_item = share_item
            sih.date = date
        sih.legal_close_price = ShareHistory.get(share_item.share, date).legal_close_price
        sih.volume, sih.avg_price = share_item.get_volume_and_price(date)
        sih.save()
        return sih
    
    @staticmethod
    def create(share_item, date):
        return ShareItemHistory.update(share_item, date, True)
"""