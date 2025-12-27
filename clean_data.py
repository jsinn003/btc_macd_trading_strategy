import pandas as pd

INPUT_PATH = "btc_usdc_data/full_btc_usdc_data.csv"
OUTPUT_PATH = "btc_usdc_data/full_btc_usdc_data_clean.csv"

df = pd.read_csv(INPUT_PATH, dtype=str)
df = df[df["Open time"] != "Open time"]
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Open time"])
df["Open time"] = pd.to_datetime(df["Open time"], unit="ms", utc=True)
df["Close time"] = pd.to_datetime(df["Close time"], unit="ms", utc=True)
df = df.sort_values("Open time").reset_index(drop=True)
assert df["Open time"].is_monotonic_increasing
assert df.isna().sum().sum() == 0
df.to_csv(OUTPUT_PATH, index=False)
print(f"Rows after cleaning: {len(df)}")