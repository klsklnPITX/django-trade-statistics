from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


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
    lotsize = models.DecimalField(max_digits=5, decimal_places=2)
    timeframe = models.CharField(choices=TIMEFRAME_CHOICES, max_length=4)
    date_created = models.DateField(auto_now_add=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username
