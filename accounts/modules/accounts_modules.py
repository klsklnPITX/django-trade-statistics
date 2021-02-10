from django.db.models import Sum, Func, Avg
from django.db import models

from accounts.models import Deposit, Withdrawal
from tradingdays.models import TradingDay


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


class AccountDataManager():
    """
    This class has all methods related to the user's current trading account calculations.
    """

    def __init__(self, user, account):
        self.user = user
        self.account = account

    def get_account_main_statistics(self):
        """
        Get accounts's sum of:
        * Profit 
        * Balance
        * Withdrawals
        * Deposits

        Returns profit, balance, withdrawal, deposits as float values.
        """
        deposits_sum = Deposit.objects.filter(account=self.account).aggregate(Sum("amount"))
        withdrawals_sum = Withdrawal.objects.filter(account=self.account).aggregate(Sum("amount"))

        profit = TradingDay.objects.filter(user=self.user).filter(account=self.account).aggregate(Sum("profit"))

        if not deposits_sum["amount__sum"]:
            deposits_sum["amount__sum"] = 0
        if not withdrawals_sum["amount__sum"]:
            withdrawals_sum["amount__sum"] = 0
        if not profit["profit__sum"]:
            profit["profit__sum"] = 0

        deposits_sum = round(float(deposits_sum["amount__sum"]), 2)
        withdrawals_sum = round(float(withdrawals_sum["amount__sum"]), 2)
        profit = round(float(profit["profit__sum"]), 2)
        balance = round(deposits_sum + profit - withdrawals_sum, 2)

        return profit, balance, withdrawals_sum, deposits_sum

    def get_daily_profit_chart_data(self):
        """
        Get accounts's daily profit with their dates for the daily profit chart.
        Returns data and label values for the js chart.
        """
        labels_daily_profit_chart = []
        data_daily_profit_chart = []

        data_decimal = list(TradingDay.objects.filter(user=self.user).filter(account=self.account).values_list("profit"))
        dates = list(TradingDay.objects.filter(user=self.user).filter(account=self.account).values_list("date_created"))

        for n in data_decimal:
            if n:
                data_daily_profit_chart.append(float(n[0]))
            else:
                data_daily_profit_chart.append(0)

        for d in dates:
            labels_daily_profit_chart.append(d[0].strftime("%d.%m.%Y"))

        return data_daily_profit_chart, labels_daily_profit_chart

    def get_monthly_profit_chart_data(self):
        """
        Get accounts's monthly profit with their month and year 
        for the monthly profit chart.
        Returns data and label values for the js chart.
        """
        data = (TradingDay.objects
                .filter(user=self.user)
                .filter(account=self.account)
                .annotate(month=Month("date_created"), year=Year("date_created"))
                .values("month", "year")
                .annotate(total=Sum("profit"))
                .order_by("year", "month"))

        labels_date = []
        data_profit = []

        for month in data:
            labels_date.append(f"{month['month']}/{month['year']}")
            if month["total"]:
                data_profit.append(round(float(month["total"]), 2))

        return data_profit, labels_date

    def get_average_daily_profit(self):
        """
        Get account's average daily profit.
        Returns float.
        """
        data = (TradingDay.objects
                .filter(user=self.user)
                .filter(account=self.account)
                .aggregate(Avg("profit")))

        if data["profit__avg"]:
            return round(float(data["profit__avg"]), 2)
        return 0
