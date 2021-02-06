from django.contrib import admin

from .models import User, TradingDay

admin.site.register(User)
admin.site.register(TradingDay)
