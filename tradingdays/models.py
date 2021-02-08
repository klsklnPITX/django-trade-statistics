from django.db import models
from django.db.models.deletion import CASCADE

import datetime

from accounts.models import Account, User


class TradingDay(models.Model):

    TIMEFRAME_CHOICES = (
        ("1M", "1M"),
        ("5M", "5M"),
        ("15M", "15M"),
        ("30M", "30M"),
        ("H1", "1H"),
        ("4H", "4H"),
    )

    user = models.ForeignKey(User, on_delete=CASCADE)
    account = models.ForeignKey(Account, on_delete=CASCADE)
    lotsize = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    timeframe = models.CharField(choices=TIMEFRAME_CHOICES, max_length=4, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date_created = models.DateField(default=datetime.date.today)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username
