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

DATE_FROM = date(2016, 10, 1)
DATE_TO = date.today()-timedelta(1)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

if len(sys.argv) > 1:
    si = ShareItem.objects.get(pk = sys.argv[1])
    print 'Updating %s' % si
    si.update_history()
    si.update_dividends()
else:
    for si in ShareItem.objects.all():
        print 'Updating %s' % si
        si.update_history()
        si.update_dividends()

