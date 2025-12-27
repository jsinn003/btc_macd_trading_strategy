import pandas as pd

def add_macd(df: pd.DataFrame, fast=12, slow=26, signal=9) -> pd.DataFrame:
    close = df["Close"]
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal
    out = df.copy()
    out["macd"] = macd
    out["macd_signal"] = macd_signal
    out["macd_hist"] = macd_hist
    return out

def add_ema(df: pd.DataFrame, span: int = 200) -> pd.DataFrame:
    out = df.copy()
    out[f"ema_{span}"] = out["Close"].ewm(span=span, adjust=False).mean()
    return out