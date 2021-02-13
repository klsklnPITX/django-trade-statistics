from django.contrib import admin

from .models import Account, Withdrawal, Deposit, TradingDay

admin.site.register(Account)
admin.site.register(Withdrawal)
admin.site.register(Deposit)
admin.site.register(TradingDay)
