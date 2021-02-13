from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import AbstractUser

import datetime


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Account(models.Model):

    ACCOUNT_TYPE_CHOICES = (
        ("Live", "Live"),
        ("Demo", "Demo"),
    )

    user = models.ForeignKey(User, on_delete=CASCADE)
    broker = models.CharField(max_length=50)
    account_number = models.IntegerField()
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    leverage = models.CharField(max_length=10)
    started = models.DateField(default=datetime.date.today)
    platform = models.CharField(max_length=30)

    def __str__(self):
        return str(self.account_number)


class Withdrawal(models.Model):
    account = models.ForeignKey(Account, on_delete=CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)


class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)


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
