from django.contrib import admin

from .models import Account, Withdrawal, Deposit, TradingDay, User

admin.site.register(Account)
admin.site.register(Withdrawal)
admin.site.register(Deposit)
admin.site.register(TradingDay)
admin.site.register(User)
