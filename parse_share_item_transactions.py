#!/usr/bin/env python
# encoding: utf-8

import codecs
import sys
import os
import csv
from datetime import date, timedelta
import datetime
import xml.etree.ElementTree as ET
import urllib
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinv.settings")
django.setup()

from shares.models import *
from portfolio.models import *

p = Portfolio.objects.get(pk = sys.argv[1])
print p

ShareTransaction.load_csv(sys.argv[2], p, {
    'sec_id': u'Код инструмента',
    'action': u'B/S',
    'action_buy': u'Покупка',
    'date': u'Дата заключения',
    'volume': u'Кол-во',
    'price': u'Цена',
    'key': u'Номер сделки',
})



