from django.contrib import admin

from django.contrib import admin

from .models import *


class BondItemAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'bond', 'volume', 'avg_price', ]
    list_filter = ('portfolio', )

class BondTransactionAdmin(admin.ModelAdmin):
    list_display = ['bond_item', 'action', 'volume', 'price', 'date', 'comment',]


admin.site.register(BondItem, BondItemAdmin)

admin.site.register(BondTransaction, BondTransactionAdmin)

