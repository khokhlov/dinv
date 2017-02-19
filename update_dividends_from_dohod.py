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
import lxml.html

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinv.settings")
django.setup()

from securities.models import Share, DividendHistory


DOHOD_URL_SHARE = 'http://www.dohod.ru/ik/analytics/dividend/%s'

for s in Share.objects.filter(dividend_flag = True).all():
    print 'Update share %s' %s
    url = DOHOD_URL_SHARE % (s.sec_id.lower())
    data = urllib.urlopen(url).read()
    doc = lxml.html.document_fromstring(data)
    trs = doc.find_class('content-table')[1]
    for t in trs:
        td = t.findall("td")
        if len(td) == 4:
            drc = td[0].text.strip().split()
            forecast = False
            if len(drc) > 1:
                forecast = True
            date_registry_close = datetime.datetime.strptime(drc[0].strip(), "%d.%m.%Y").date()
            date_payment = datetime.datetime.strptime(td[1].text.strip(), "%d.%m.%Y").date()
            dividend = Decimal(td[2].text.strip())
            
            
            profit = None
            try:
                profit = Decimal(td[3].text.strip('%%'))
            except:
                pass
            if DividendHistory.has(s, date_registry_close):
                if not DividendHistory.get(s, date_registry_close).forecast_flag:
                    continue
            print DividendHistory.update(s, date_registry_close, date_payment, dividend, profit, forecast)
            
    
