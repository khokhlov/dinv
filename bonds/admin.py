from django.contrib import admin

from django.contrib import admin

from .models import *


class BondItemAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'bond', 'volume', 'avg_price', ]
    list_filter = ('portfolio', )

class BondTransactionAdmin(admin.ModelAdmin):
    list_display = ['bond_item', 'action', 'volume', 'price', 'date', 'comment',]

class BondItemHistoryAdmin(admin.ModelAdmin):
    list_display = ['bond_item', 'date', 'volume', 'avg_price', 'legal_close_price', 'balance']
    list_filter = ('bond_item', )

class BondItemCouponAdmin(admin.ModelAdmin):
    list_display = ['bond_item', 'date', 'price_no_tax', 'price', 'tax', 'percent', 'checked']
    list_filter = ('bond_item', 'checked')


admin.site.register(BondItem, BondItemAdmin)

admin.site.register(BondTransaction, BondTransactionAdmin)

admin.site.register(BondItemHistory, BondItemHistoryAdmin)

admin.site.register(BondItemCoupon, BondItemCouponAdmin)
