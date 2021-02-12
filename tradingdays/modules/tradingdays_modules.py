import pandas as pd

from tradingdays.models import TradingDay
from accounts.models import Account, Withdrawal, Deposit


ALLOWED_EXTENSIONS = ["csv"]


def parse_csv_file(csv_file, account, user):
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
    deposits_per_day_df = get_deposits_withdrawals_from_df(df, "Deposit")

    # Withdrawals
    withdrawals_per_day_df = get_deposits_withdrawals_from_df(df, "Withdrawal")

    account_instance = Account.objects.get(pk=account)

    # Save to model

    # Profits
    for index, row in profits_per_day_df.iterrows():
        TradingDay.objects.create(
            user=user,
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


def get_deposits_withdrawals_from_df(df, action):
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


def allowed_file(filename):
    """
    Checks wether the file has an allowed fiel extension.
    Returns True or False.
    """

    return '.' in str(filename) and \
           str(filename).rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_previous_account_data(request, account):
    """
    Delete tradingdays, withdrawals, deposits from current account.
    Used in upload csv view.
    Take request and account as parameter
    """
    user = request.user

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
