import pandas as pd

def run_process():
    df = pd.read_csv("data/raw.csv")

    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour

    df.to_csv("data/hourly.csv", index=False)

    daily = df.groupby("date").mean(numeric_only=True)
    daily.to_csv("data/processed.csv")