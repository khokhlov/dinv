from django.contrib import admin

from django.contrib import admin

from .models import *


class ShareItemAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'share', 'volume', 'avg_price', ]
    list_filter = ('portfolio', )

class ShareTransactionAdmin(admin.ModelAdmin):
    list_display = ['share_item', 'action', 'volume', 'price', 'date', 'comment',]

class ShareItemHistoryAdmin(admin.ModelAdmin):
    list_display = ['share_item', 'date', 'volume', 'avg_price', 'legal_close_price', 'balance']
    list_filter = ('share_item', )


class ShareItemDividendAdmin(admin.ModelAdmin):
    list_display = ['share_item', 'dividend', 'price_no_tax', 'price', 'tax', 'percent', 'checked']
    list_filter = ('share_item', 'checked')

admin.site.register(ShareItem, ShareItemAdmin)

admin.site.register(ShareTransaction, ShareTransactionAdmin)

admin.site.register(ShareItemHistory, ShareItemHistoryAdmin)

admin.site.register(ShareItemDividend, ShareItemDividendAdmin)

