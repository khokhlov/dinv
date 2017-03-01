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

from securities.models import Share, ShareHistory

DATE_FROM = date(2016, 10, 1)
DATE_TO = date.today()-timedelta(1)

MOEX_URL_SHARE = 'https://moex.com/iss/history/engines/stock/markets/shares/boards/%s/securities/%s.xml?from=%s&till=%s&lang=RU'

def daterange(start_date, end_date):
    for n in range(0, int ((end_date - start_date).days + 1), 30):
        yield start_date + timedelta(n)

for s in Share.objects.all():
    print 'Update share %s' %s
    for d1 in daterange(DATE_FROM, DATE_TO):
        d2 = d1 + timedelta(30)
        print d1, d2
        url = MOEX_URL_SHARE % (s.board.board_id, s.sec_id, d1, d2)
        xml_data = urllib.urlopen(url).read()
        root = ET.fromstring(xml_data)
        for row in root.iter('row'):
            d = datetime.datetime.strptime(row.get('TRADEDATE'), "%Y-%m-%d").date()
            if not s.has_history(d):
                sh = ShareHistory()
                sh.share = s
                sh.num_trades = int(row.get('NUMTRADES'))
                sh.low = Decimal(row.get('LOW'))
                sh.value = Decimal(row.get('VALUE'))
                sh.high = Decimal(row.get('HIGH'))
                sh.open = Decimal(row.get('OPEN'))
                sh.war_price = Decimal(row.get('WAPRICE'))
                sh.legal_close_price = Decimal(row.get('LEGALCLOSEPRICE'))
                sh.trade_date = datetime.datetime.strptime(row.get('TRADEDATE'), "%Y-%m-%d").date()
                sh.save()
                    
                print sh
                    
                    # Check share
                if not s.short_name:
                    s.short_name = row.get('SHORTNAME')
                    s.save()
            else:
                print 'Skip date %s for share %s.' % (d, s)
