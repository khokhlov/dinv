from django.contrib import admin

from .models import *

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'short_name', 'name', ]

class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ['currency1', 'currency2', 'rate', 'date']

admin.site.register(Currency, CurrencyAdmin)

admin.site.register(CurrencyRate, CurrencyRateAdmin)
