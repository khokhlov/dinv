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
from dinv.utils import UnicodeDictReader
from securities.models import BondHistory, AbstractSecurityItem, AbstractItemTransaction

class BondTransaction(AbstractItemTransaction):
    bond_item = models.ForeignKey('BondItem',
                              verbose_name = u'Актив',
                              related_name = 'transactions',
                              help_text = u'Сделка по какому активу')

    @property
    def sec_item(self): return self.bond_item

    @staticmethod
    @transaction.atomic
    def load_csv(path, portfolio, cols):
        reader = UnicodeDictReader(open(path, 'r'), delimiter=str(u','), quotechar=str(u'"'))
        for row in reader:
            sec_id = row[cols['sec_id']]
            s = None
            try:
                s = Bond.objects.filter(sec_id = sec_id)[0]
            except:
                print 'Bond key error:', sec_id
            bond_item = BondItem.get_or_create(portfolio, s)
            
            # сначала проверяем ключ
            key = row[cols['key']]
            if BondTransaction.objects.filter(bond_item = bond_item).filter(key = key).count() > 0:
                print 'Skip transaction with key:', key
                continue
            
            action = BondTransaction.TYPE_SELL
            if row[cols['action']] == cols['action_buy']:
                action = BondTransaction.TYPE_BUY
            print row[cols['date']]
            date = datetime.datetime.strptime(row[cols['date']], "%d.%m.%Y %H:%M:%S")
            volume = int(row[cols['volume']])
            price = Decimal(row[cols['price']].replace(',', '.')) / s.face_value
            print BondTransaction.create(bond_item, action, volume, price, date, '', key)


class BondItem(AbstractSecurityItem):
	class Meta:
		unique_together = ('bond', 'portfolio')
		verbose_name = u'Пакет облигаций'
		verbose_name_plural = u'Пакеты облигаций'

	TransactionModel = BondTransaction

	@property
	def sec(self): return self.bond

	bond = models.ForeignKey('securities.Bond',
                              verbose_name = u'Облигация')
    
	portfolio = models.ForeignKey('portfolio.Portfolio',
                                  related_name = 'bonds',
                                  verbose_name = u'Портфель')



"""
class BondItem(models.Model):
    class Meta:
        unique_together = ('bond', 'portfolio')
        verbose_name = u'Пакет облигаций'
        verbose_name_plural = u'Пакеты облигаций'

    bond = models.ForeignKey('securities.Bond',
                              verbose_name = u'Облигация')
    
    portfolio = models.ForeignKey('portfolio.Portfolio',
                                  related_name = 'bonds',
                                  verbose_name = u'Портфель')
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество акций')
    
    avg_price = models.DecimalField(max_digits=35,
                                    decimal_places=15,
                                    verbose_name = u'Средняя, %',
                                    help_text = u'Средняя цена, %')
    
    @staticmethod
    def get(portfolio, bond):
        return BondItem.objects.filter(portfolio = portfolio).filter(bond = bond)[0]
    
    @staticmethod
    def has(portfolio, bond):
        return BondItem.objects.filter(portfolio = portfolio).filter(bond = bond).count() > 0
    
    @staticmethod
    def get_or_create(portfolio, bond):
        if BondItem.has(portfolio, bond):
            return BondItem.get(portfolio, bond)
        s = BondItem()
        s.portfolio = portfolio
        s.bond = bond
        s.volume = 0
        s.avg_price = Decimal("0")
        s.save()
        return s
    
    def __unicode__(self):
        return u'%s (%s)' % (self.portfolio, self.bond)
    
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
            if t.action == BondTransaction.TYPE_BUY:
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
            print BondItemHistory.update(self, d)
  """

"""
class BondTransaction(models.Model):
    class Meta:
        ordering = ['-date', ]
        verbose_name = u'Сделка'
        verbose_name_plural = u'Сделки'
        
    TYPE_SELL = 0
    TYPE_BUY  = 1
    
    TYPE = (
        (TYPE_SELL, u'Продажа'),
        (TYPE_BUY,  u'Покупка')
        )
    
    bond_item = models.ForeignKey('BondItem',
                              verbose_name = u'Актив',
                              related_name = 'transactions',
                              help_text = u'Сделка по какому активу')
    
    action = models.IntegerField(choices = TYPE,
                               verbose_name = u'Действие',
                               help_text = u'Действие по кативу: покупка/продажа'
                               )
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество облигаций')
    
    price = models.DecimalField(max_digits=35,
                                decimal_places=15,
                                verbose_name = u'Цена',
                                help_text = u'Цена одной ценной бумаги')
    
    date = models.DateTimeField(default = django.utils.timezone.now,
                                verbose_name = u'Дата',
                                help_text = u'Дата сделки')
    
    comment = models.TextField(blank = True,
                               null = True,
                               verbose_name = u'Комментарий')
    
    key = models.CharField(max_length = 1024,
                              null = True,
                              blank = True,
                              verbose_name = u'Ключ сделки',
                              help_text = u'Уникальный номер сделки для автопарсинга')
    
    def total_price(self):
        return self.price * self.volume
    
    @staticmethod
    def create(bond_item, action, volume, price, date, comment, key = None):
        s = BondTransaction()
        s.bond_item = bond_item
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
                s = Bond.objects.filter(sec_id = sec_id)[0]
            except:
                print 'Bond key error:', sec_id
            bond_item = BondItem.get_or_create(portfolio, s)
            
            # сначала проверяем ключ
            key = row[cols['key']]
            if BondTransaction.objects.filter(bond_item = bond_item).filter(key = key).count() > 0:
                print 'Skip transaction with key:', key
                continue
            
            action = BondTransaction.TYPE_SELL
            if row[cols['action']] == cols['action_buy']:
                action = BondTransaction.TYPE_BUY
            print row[cols['date']]
            date = datetime.datetime.strptime(row[cols['date']], "%d.%m.%Y %H:%M:%S")
            volume = int(row[cols['volume']])
            price = Decimal(row[cols['price']].replace(',', '.')) / s.face_value
            print BondTransaction.create(bond_item, action, volume, price, date, '', key)
"""
def update_from_transactions(sender, instance, **kwargs):
    instance.bond_item.update_from_transactions()
    
post_save.connect(update_from_transactions, sender = BondTransaction)
post_delete.connect(update_from_transactions, sender = BondTransaction)

class BondItemHistory(models.Model):
    class Meta:
        ordering = ['-date', ]
        unique_together = ('bond_item', 'date')
        verbose_name = u'История пакета облигаций'
        verbose_name_plural = u'Истории пакетов облигаций'
    
    bond_item = models.ForeignKey('BondItem',
                              verbose_name = u'Актив',
                              related_name = 'history',
                              help_text = u'История актива')
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество облигаций')
    
    legal_close_price = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               verbose_name = u'Закрытия',
                               help_text = u'Цена закрытия')
    
    avg_price = models.DecimalField(max_digits=35,
                                    decimal_places=15,
                                    verbose_name = u'Средняя',
                                    help_text = u'Средняя цена')

    accint = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'НКД',
                               help_text = u'Накопленный купонный доход (НКД), по одной ценной бумаге')

    yield_close = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Доходность, % годовых - последней сделки',
                               help_text = u'Доходность по цене последней сделки, % годовых')
    
    date = models.DateField(verbose_name = u'Дата торгов')
    
    def price(self):
        return self.legal_close_price * self.volume * self.bond_item.bond.face_value / Decimal(100) + self.accint * self.volume
    
    def buy_price(self):
        return self.avg_price * self.volume
    
    def balance(self):
        return self.price() - self.buy_price()
    
    def __unicode__(self):
        return u'%s - %s - %s' % (self.bond_item, self.date, self.price())
    
    @staticmethod
    def get(bond_item, date):
        return BondItemHistory.objects.filter(bond_item = bond_item, date = date).all()[0]
    
    @staticmethod
    def has(bond_item, date):
        return BondItemHistory.objects.filter(bond_item = bond_item, date = date).count() > 0
    
    @staticmethod
    def update(bond_item, date, create = False):
        if not create and not BondHistory.has(bond_item.bond, date):
            return None

        sih = BondItemHistory()
        if not create and BondItemHistory.has(bond_item, date):
            sih = BondItemHistory.get(bond_item, date)
        else:
            sih.bond_item = bond_item
            sih.date = date
        bh = BondHistory.get(bond_item.bond, date)
        sih.legal_close_price = bh.legal_close_price
        sih.accint = bh.accint
        sih.yield_close = bh.yield_close
        sih.volume, sih.avg_price = bond_item.get_volume_and_price(date)
        sih.save()
        return sih
    
    @staticmethod
    def create(bond_item, date):
        return BondItemHistory.update(bond_item, date, True)
