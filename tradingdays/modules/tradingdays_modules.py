import pandas as pd

from tradingdays.models import TradingDay
from accounts.models import Account


ALLOWED_EXTENSIONS = ["csv"]


def parse_csv_file(csv_file, account, user):
    """
    Takes a csv file from myfxbook and parses its content.
    Sums up daily profit and with its date and passes it to selected account's
    trading days model.
    """

    df = pd.read_csv(csv_file)

    filtered_df = df.filter(["Open Date", "Close Date", "Profit"], axis=1)
    filtered_df.dropna(inplace=True)

    per_day_df = filtered_df[["Close Date", "Profit"]]
    per_day_df["Close Date"] = pd.to_datetime(per_day_df["Close Date"]).dt.date
    per_day_df = per_day_df.groupby(["Close Date"], as_index=False).agg({'Profit': 'sum'}).reset_index()
    per_day_df["Profit"] = per_day_df["Profit"].round(2)

    account_instance = Account.objects.get(pk=account)

    # Save to model
    for index, row in per_day_df.iterrows():
        TradingDay.objects.create(
            user=user,
            account=account_instance,
            date_created=row["Close Date"],
            profit=row["Profit"],
            note="Automatically added through uploaded csv."
        )


def allowed_file(filename):
    """
    Checks wether the file has an allowed fiel extension.
    Returns True or False.
    """

    return '.' in str(filename) and \
           str(filename).rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
