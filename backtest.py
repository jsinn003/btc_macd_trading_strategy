import pandas as pd
import numpy as np

def compute_metrics(equity_curve: pd.DataFrame) -> dict:
    rets = equity_curve["equity"].pct_change().dropna()
    total_return = equity_curve["equity"].iloc[-1] / equity_curve["equity"].iloc[0] - 1
    peak = equity_curve["equity"].cummax()
    dd = equity_curve["equity"] / peak - 1
    max_dd = dd.min()
    sharpe = np.nan
    if rets.std() > 0:
        sharpe = (rets.mean() / rets.std()) * np.sqrt(365 * 24 * 60)
    return {"total_return": float(total_return), "max_drawdown": float(max_dd), "sharpe": float(sharpe)}