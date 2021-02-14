from django.db.models import Sum, Func, Avg
from django.db import models

from accounts.models import Account, Withdrawal, Deposit, TradingDay

from itertools import accumulate
import pandas as pd


ALLOWED_EXTENSIONS = ["csv"]


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

        data_decimal = list((TradingDay.objects
                             .filter(user=self.user)
                             .filter(account=self.account)
                             .values_list("profit")
                             .order_by("date_created")))
        dates = list((TradingDay.objects
                      .filter(user=self.user)
                      .filter(account=self.account)
                      .values_list("date_created")
                      .order_by("date_created")))

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
        Get account's monthly profit with their month and year
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

    def get_yearly_profit(self):
        """
        Get account's yearly profit with corresponding year.
        Returns dictionary {year: profit}.
        """

        data = (TradingDay.objects
                .filter(user=self.user)
                .filter(account=self.account)
                .annotate(year=Year("date_created"))
                .values("year")
                .annotate(total=Sum("profit"))
                .order_by("year"))

        data_dict = {}
        for year in data:
            try:
                total = round(float(year["total"]), 2)
            except:
                total = 0
            data_dict[year["year"]] = total

        return data_dict

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

    def get_tradingday_count(self):
        """
        Get count of account's trading days.
        Returns int count
        """
        data = (TradingDay.objects
                .filter(user=self.user)
                .filter(account=self.account)
                .count())
        return data

    def get_accumulated_profit(self, trading_day_count, trading_day_profit):
        """
        Get accumulated account's profit per day.
        Takes trading day count (Get from get_tradingday_count() method.
        Takes trading day profit (Get from get_daily_profit_chart_data() method).
        Returns accumulated profit per day and current day count value.
        """
        accumulated_profit = []
        profits = accumulate(trading_day_profit)
        for n in profits:
            accumulated_profit.append(round(n, 2))

        tradingday_count = []
        for i in range(1, trading_day_count+1):
            tradingday_count.append(i)

        return accumulated_profit, tradingday_count

    def get_profit_percent(self, profit, deposits):
        """
        Get account's profit in percent.
        Take profit and deposits from get_account_main_statistics() method.
        Returns float profit percent.
        """
        try:
            return round((profit / deposits) * 100, 2)
        except ZeroDivisionError:
            return 0

    def parse_csv_file(self, csv_file):
        """
        Takes a csv file from myfxbook and parses its content.
        Sums up daily profit, deposit and withdrawal with its date
        and passes it to selected account's trading days model and Deposit/Withdrawal models.
        """

        df = pd.read_csv(csv_file)

        # Profits
        filtered_df = df.filter(["Open Date", "Close Date", "Profit"], axis=1)
        filtered_df.dropna(inplace=True)

        profits_per_day_df = filtered_df[["Close Date", "Profit"]]
        profits_per_day_df["Close Date"] = pd.to_datetime(profits_per_day_df["Close Date"]).dt.date
        profits_per_day_df = profits_per_day_df.groupby(["Close Date"], as_index=False).agg({'Profit': 'sum'}).reset_index()
        profits_per_day_df["Profit"] = profits_per_day_df["Profit"].round(2)

        # Deposits
        deposits_per_day_df = self.get_deposits_withdrawals_from_df(df, "Deposit")

        # Withdrawals
        withdrawals_per_day_df = self.get_deposits_withdrawals_from_df(df, "Withdrawal")

        account_instance = Account.objects.get(pk=self.account)

        # Save to model

        # Profits
        for index, row in profits_per_day_df.iterrows():
            TradingDay.objects.create(
                user=self.user,
                account=account_instance,
                date_created=row["Close Date"],
                profit=row["Profit"],
                note="Automatically added through uploaded csv."
            )

        # Deposits
        for index, row in deposits_per_day_df.iterrows():
            Deposit.objects.create(
                account=account_instance,
                amount=row["Profit"],
                date=row["Open Date"]
            )

        # Withdrawals
        for index, row in withdrawals_per_day_df.iterrows():
            Withdrawal.objects.create(
                account=account_instance,
                amount=row["Profit"],
                date=row["Open Date"]
            )

    def get_deposits_withdrawals_from_df(self, df, action):
        """
        Get deposits and withdrawals from csv file.
        Provide "action" kwarg as:
        * "Deposit"
        * "Withdrawal"
        Returns df with deposits or withdrawals
        """

        new_df = df[(df.Action == action)]
        new_df = new_df[["Open Date", "Profit"]]
        new_df["Open Date"] = pd.to_datetime(new_df["Open Date"]).dt.date
        new_df = new_df.groupby(["Open Date"], as_index=False).agg({'Profit': 'sum'}).reset_index()
        new_df["Profit"] = new_df["Profit"].abs()
        return new_df

    @staticmethod
    def allowed_file(filename):
        """
        Checks wether the file has an allowed fiel extension.
        Returns True or False.
        """

        return '.' in str(filename) and \
            str(filename).rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def delete_previous_account_data(self):
        """
        Delete tradingdays, withdrawals, deposits from current account.
        Used in upload csv view.
        Take request and account as parameter
        """
        user = self.user
        account = self.account

        (TradingDay.objects
         .filter(user=user)
         .filter(account=account)
         .delete())
        (Withdrawal.objects
         .filter(account=account)
         .delete())

        (Deposit.objects
         .filter(account=account)
         .delete())

    def calculate_yearly_tax(self, yearly_profit):
        """
        Calculatees account's yearly tax expenses.
        Uses German capital gains tax and German regulations.

        Takes yearly profit dictionary from get_yearly_profit() method.
        """
        freibetrag = 801
        cap_gains_tax_rate = 0.25
        soli = 0.055
        kirchensteuer = 0.08

        result_dict = {}

        for year, profit in yearly_profit.items():
            if profit <= freibetrag:
                result_dict[year] = {
                    "profit": profit,
                    "profit_after_deduction": "-",
                    "cap_gains_deduction": "-",
                    "soli_deduction": "-",
                    "kirche_deduction": "-",
                    "tax_sum": "-",
                    "net_profit": profit,
                    "tax_ratio_profit": "-",
                    "tax_ratio_profit_with_freibetrag": "-",
                    "cap_gains_tax_rate": cap_gains_tax_rate * 100,
                    "soli_rate": soli * 100,
                    "kirchensteuer_rate": kirchensteuer * 100,
                    "freibetrag_euro": 801
                }
            else:
                profit_after_decuction = profit - freibetrag
                cap_gains_tax_deduction = profit_after_decuction * cap_gains_tax_rate
                soli_deduction = cap_gains_tax_deduction * soli
                kirche_deduction = cap_gains_tax_deduction * kirchensteuer
                tax_sum = cap_gains_tax_deduction + soli_deduction + kirche_deduction
                net_profit = profit - tax_sum

                tax_ratio_profit = round(tax_sum / profit, 2)
                tax_ratio_profit_with_freibetrag = round(tax_sum / profit_after_decuction, 2)

                result_dict[year] = {
                    "profit": profit,
                    "profit_after_deduction": round(profit_after_decuction, 2),
                    "cap_gains_deduction": round(cap_gains_tax_deduction, 2),
                    "soli_deduction": round(soli_deduction, 2),
                    "kirche_deduction": round(kirche_deduction, 2),
                    "tax_sum": round(tax_sum, 2),
                    "net_profit": round(net_profit, 2),
                    "tax_ratio_profit": round(tax_ratio_profit * 100, 2),
                    "tax_ratio_profit_with_freibetrag": round(tax_ratio_profit_with_freibetrag * 100, 2),
                    "cap_gains_tax_rate": cap_gains_tax_rate * 100,
                    "soli_rate": soli * 100,
                    "kirchensteuer_rate": kirchensteuer * 100,
                    "freibetrag_euro": 801

                }

        return result_dict
