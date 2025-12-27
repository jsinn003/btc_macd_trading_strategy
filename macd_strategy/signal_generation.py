import pandas as pd

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    cross_up = (
        (out["macd"] > out["macd_signal"]) &
        (out["macd"].shift(1) <= out["macd_signal"].shift(1))
    )
    cross_down = (
        (out["macd"] < out["macd_signal"]) &
        (out["macd"].shift(1) >= out["macd_signal"].shift(1))
    )
    out["signal_raw"] = 0
    out.loc[cross_up, "signal_raw"] = 1
    out.loc[cross_down, "signal_raw"] = -1
    out["signal"] = out["signal_raw"].shift(1).fillna(0).astype(int)
    return out