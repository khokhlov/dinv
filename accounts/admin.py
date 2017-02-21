from django.contrib import admin

# Register your models here.
from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'portfolio', 'currency', 'volume', ]
    list_filter = ('portfolio', )

class AccountTransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'action', 'volume', 'date', 'comment',]

admin.site.register(BankAccount, AccountAdmin)

admin.site.register(AccountTransaction, AccountTransactionAdmin)

