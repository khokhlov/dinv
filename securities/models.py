#coding: utf-8
from __future__ import unicode_literals

from django.db import models
import django
import datetime
from dinv.utils import daterange
from dinv.utils import UnicodeDictReader
from decimal import Decimal


class Board(models.Model):
    class Meta:
        verbose_name = u'Режим торгов'
        verbose_name_plural = u'Режимы торгов'
        
    board_id = models.CharField(max_length = 128,
                                unique = True,
                                verbose_name = u'Код режима',
                                help_text = u'Идентификатор режима торгов')
    
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return u'%s' % self.board_id

class AbstractSecurity(models.Model):
    class Meta:
        abstract = True
    
    sec_id = models.CharField(max_length = 128,
                              null = True,
                              blank = True,
                              verbose_name = u'Код инструмента',
                              help_text = u'Идентификатор финансового инструмента')
    
    board = models.ForeignKey('Board',
                              on_delete = models.CASCADE,
                              null = True,
                              blank = True,
                              verbose_name = u'Режим торгов')
    
    short_name = models.CharField(max_length = 1024,
                              null = True,
                              blank = True,
                              verbose_name = u'Наименование',
                              help_text = u'Краткое наименование')
    
    isin = models.CharField(max_length = 128,
                            null = True,
                            blank = True,
                            verbose_name = u'ISIN код',
                            help_text = u'ISIN код')
    
    face_value = models.DecimalField(max_digits=35,
                                     decimal_places=15,
                                     null = True,
                                     blank = True,
                                     verbose_name = u'Номинал',
                                     help_text = u'Номинальная стоимость')
    
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.short_name, self.sec_id)
    
    def has_history(self, date):
        return self.history.filter(trade_date = date).count() > 0
                                     

class AbstractHistory(models.Model):
    class Meta:
        abstract = True
        ordering = ['-trade_date', ]
    
    trade_date = models.DateField(verbose_name = u'Дата торгов')
    
    num_trades = models.IntegerField(null = True,
                                     blank = True,
                                     verbose_name = u'Сделок, шт.',
                                     help_text = u'Количество сделок за день, штук')
    
    value = models.DecimalField(max_digits=35,
                                decimal_places=15,
                                null = True,
                                blank = True,
                                verbose_name = u'Объем',
                                help_text = u'Объем сделок в валюте ценной бумаги')
    
    open = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Первая',
                               help_text = u'Цена предторгового периода/Цена аукциона открытия')
    
    low = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Минимум',
                               help_text = u'Цена сделки минимальная')
    
    high = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Максимум',
                               help_text = u'Максимальная цена сделки')
    
    close = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Последняя',
                               help_text = u'Цена последней сделки')
    
    legal_close_price = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Закрытия',
                               help_text = u'Цена закрытия')
    
    war_price = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Срвзв. цена',
                               help_text = u'Средневзвешенная цена')

class Share(AbstractSecurity):
    class Meta:
        verbose_name = u'Акция'
        verbose_name_plural = u'Акции'
    
    dividend_flag = models.BooleanField(default = False,
                                        verbose_name = u'Дивидендная',
                                        help_text = u'Дивидендная акция')

class DividendHistory(models.Model):
    class Meta:
        verbose_name = u'Дивидендная выплата'
        verbose_name_plural = u'Дивидендные выплаты'
        unique_together = ('share', 'date_registry_close')
        ordering = ['-date_registry_close']
    
    share = models.ForeignKey('Share',
                              related_name = 'dividends',
                              verbose_name = u'Акция')
    
    forecast_flag = models.BooleanField(verbose_name = u'Прогноз',
                                        help_text = u'Прогноз дивидендной выплаты')
    
    date_registry_close = models.DateField(verbose_name = u'Дата закрытия реестра')
    
    date_payment = models.DateField(verbose_name = u'Дата выплаты')
    
    dividend = models.DecimalField(max_digits=35,
                                decimal_places=15,
                               null = True,
                               blank = True,
                               verbose_name = u'Дивиденд',
                               help_text = u'Размер выплаты дивиденда на одну акцию')
    
    profit_percent = models.DecimalField(max_digits=10,
                                decimal_places=5,
                               null = True,
                               blank = True,
                               verbose_name = u'Процент от прибыли',
                               help_text = u'Какой процент от прибыли компании был выплачен в качестве дивидендов')
    
    def __unicode__(self):
        return u'%s - %s (%s)' % (self.share, self.date_registry_close, self.dividend)
    
    @staticmethod
    def get(share, date):
        return DividendHistory.objects.filter(share = share, date_registry_close = date).all()[0]
    
    @staticmethod
    def has(share, date):
        return DividendHistory.objects.filter(share = share, date_registry_close = date).count() > 0
    
    @staticmethod
    def update(share, date_registry_close, date_payment, dividend, profit, forecast, create = False):
        dh = DividendHistory()
        if not create and DividendHistory.has(share, date_registry_close):
            dh = DividendHistory.get(share, date_registry_close)
        else:
            dh.share = share
            dh.date_registry_close = date_registry_close
        dh.date_payment = date_payment
        dh.dividend = dividend
        dh.profit_percent = profit
        dh.forecast_flag = forecast
        dh.save()
        return dh

class ShareHistory(AbstractHistory):
    class Meta:
        unique_together = ('trade_date', 'share')
        verbose_name = u'История акции'
        verbose_name_plural = u'Истории акций'

    share = models.ForeignKey('Share',
                              related_name = 'history',
                              verbose_name = u'Акция')
    
    def __unicode__(self):
        return u'%s %s' % (self.trade_date, self.share)
    
    @staticmethod
    def get(share, date):
        return ShareHistory.objects.filter(share = share).filter(trade_date = date)[0]
    
    @staticmethod
    def has(share, date):
        return ShareHistory.objects.filter(share = share).filter(trade_date = date).count() > 0


class Bond(AbstractSecurity):
    class Meta:
        verbose_name = u'Облигация'
        verbose_name_plural = u'Облигации'
    
class BondHistory(AbstractHistory):
    class Meta:
        unique_together = ('trade_date', 'bond')
        verbose_name = u'История облигации'
        verbose_name_plural = u'Истории облигаций'

    bond = models.ForeignKey('Bond',
                              related_name = 'history',
                              verbose_name = u'Облигация')

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

    
    def __unicode__(self):
        return u'%s %s' % (self.trade_date, self.bond)
    
    @staticmethod
    def get(bond, date):
        return BondHistory.objects.filter(bond = bond).filter(trade_date = date)[0]
    
    @staticmethod
    def has(bond, date):
        return BondHistory.objects.filter(bond = bond).filter(trade_date = date).count() > 0



class AbstractSecurityItem(models.Model):
    class Meta:
        verbose_name = u'Пакет бумаг'
        verbose_name_plural = u'Пакеты бумаг'
        abstract = True

    HistoryModel = None
    TransactionModel = None
    ThisModel = None
    IncomeModel = None

    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество бумаг')
    
    avg_price = models.DecimalField(max_digits=35,
                                    decimal_places=15,
                                    verbose_name = u'Средняя',
                                    help_text = u'Средняя цена')
    
    def __unicode__(self):
        return u'%s (%s)' % (self.portfolio, self.sec)
    
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
            if t.action == self.TransactionModel.TYPE_BUY:
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
            print self.HistoryModel.update(self, d)
    
    def price_all_income(self):
        price = Decimal(0)
        for d in self.income.all():
            price += d.price()
        return price
    
    def income_yield(self):
        return self.price_all_income() / self.price() * Decimal(100.0)
    
    def balance_with_income(self):
        return self.balance() + self.price_all_income()
    
    def percent_with_income(self):
        return self.balance_with_income() / self.price() * Decimal(100.0)

class AbstractItemTransaction(models.Model):
    class Meta:
        ordering = ['-date', ]
        verbose_name = u'Сделка'
        verbose_name_plural = u'Сделки'
        abstract = True
        
    TYPE_SELL = 0
    TYPE_BUY  = 1
    
    TYPE = (
        (TYPE_SELL, u'Продажа'),
        (TYPE_BUY,  u'Покупка')
        )
        
    action = models.IntegerField(choices = TYPE,
                               verbose_name = u'Действие',
                               help_text = u'Действие по кативу: покупка/продажа'
                               )
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество бумаг')
    
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
    
class AbstractItemHistory(models.Model):
    class Meta:
        ordering = ['-date', ]
        verbose_name = u'История пакета бумаг'
        verbose_name_plural = u'Истории пакетов бумаг'
        abstract = True
    
    volume = models.IntegerField(verbose_name = u'Количество',
                                help_text = u'Количество бумаг')
    
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
        return u'%s - %s - %s' % (self.sec_item, self.date, self.price())
    

class AbstractItemIncome(models.Model):
    class Meta:
        verbose_name = u'Выплаченный доход'
        verbose_name_plural = u'Выплаченные доходы'
        abstract = True
        
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
                                  help_text = u'Подтверждение получения на счет')
    
    percent = models.DecimalField(max_digits=35,
                                decimal_places=15,
                                blank = True,
                               null = True,
                               verbose_name = u'Доходность, %',
                               help_text = u'Доходность на дату выплаты с учетом налога, %')
    
    def price(self):
        return self.price_no_tax * (Decimal(100.0) - self.tax) / Decimal(100.0)
    
    
