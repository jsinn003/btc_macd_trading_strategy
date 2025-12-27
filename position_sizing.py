import pandas as pd
import numpy as np

def add_atr(df: pd.DataFrame, n=14) -> pd.DataFrame:
    out = df.copy()
    high, low, close = out["High"], out["Low"], out["Close"]
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    out["atr"] = tr.rolling(n).mean()
    return out

def position_size(equity, entry_price, atr, risk_per_trade=0.01, atr_mult=2.0, max_leverage=1.0):
    if atr is None or np.isnan(atr) or atr <= 0:
        return 0.0
    stop_dist = atr_mult * atr
    risk_dollars = risk_per_trade * equity
    qty = risk_dollars / stop_dist
    max_qty = (equity * max_leverage) / entry_price
    return float(min(qty, max_qty))