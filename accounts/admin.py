from django.contrib import admin

from .models import Account, Withdrawal, Deposit

admin.site.register(Account)
admin.site.register(Withdrawal)
admin.site.register(Deposit)
