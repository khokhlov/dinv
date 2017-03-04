from django.contrib import admin

from .models import *

class BoardAdmin(admin.ModelAdmin):
    list_display = ['board_id',]

class SecurityAdmin(admin.ModelAdmin):
    list_display = ['sec_id', 'short_name', 'board', 'isin', 'face_value', ]
    list_filter = ('board', )

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'trade_date', 'legal_close_price']

class DividendHistoryAdmin(admin.ModelAdmin):
    list_display = ['share', 'date_registry_close', 'date_payment', 'forecast_flag', 'dividend', 'profit_percent']

admin.site.register(Board, BoardAdmin)

admin.site.register(Share, SecurityAdmin)

admin.site.register(ShareHistory, HistoryAdmin)

admin.site.register(DividendHistory, DividendHistoryAdmin)

admin.site.register(Bond, SecurityAdmin)

admin.site.register(BondHistory, HistoryAdmin)

