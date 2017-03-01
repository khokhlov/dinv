from django.contrib import admin

# Register your models here.

from .models import *

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'shares_price', 'shares_balance', ]

admin.site.register(Portfolio, PortfolioAdmin)
