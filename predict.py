import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def run_predict():
    df = pd.read_csv("data/processed.csv")

    df["day"] = np.arange(len(df))

    X = df[["day"]]
    y = df["temp"]

    model = RandomForestRegressor()
    model.fit(X, y)

    future = np.arange(len(df), len(df)+5).reshape(-1,1)
    pred = model.predict(future)

    pd.DataFrame({"prediction": pred}).to_csv("data/pred.csv", index=False)