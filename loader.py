import pandas as pd

def load_data(path="btc_usdc_data/full_btc_usdc_data_clean.csv"):
    df = pd.read_csv(path)
    df["Open time"] = pd.to_datetime(df["Open time"], utc=True)
    df = df.sort_values("Open time").set_index("Open time")
    cols = ["Open", "High", "Low", "Close", "Volume"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="raise")
    return df[cols]