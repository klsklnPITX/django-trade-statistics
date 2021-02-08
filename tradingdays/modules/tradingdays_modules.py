import pandas as pd


def parse_csv_file(csv_file):
    df = pd.read_csv(csv_file)

    filtered_df = df.filter(["Open Date", "Close Date", "Profit"], axis=1)
    filtered_df.dropna(inplace=True)

    per_day_df = filtered_df[["Close Date", "Profit"]]
    per_day_df["Close Date"] = pd.to_datetime(per_day_df["Close Date"]).dt.date
    per_day_df = per_day_df.groupby(["Close Date"], as_index=False).agg({'Profit': 'sum'}).reset_index()
    per_day_df["Profit"] = per_day_df["Profit"].round(2)

    for index, row in per_day_df.iterrows():
        print(row["Close Date"], row["Profit"])
