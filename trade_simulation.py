from dataclasses import dataclass
import pandas as pd
import numpy as np
from position_sizing import position_size
from typing import Optional, List

@dataclass
class Trade:
    entry_time: pd.Timestamp
    exit_time: Optional[pd.Timestamp]
    entry_price: float
    exit_price: Optional[float]
    qty: float
    pnl: Optional[float]
    reason: Optional[str]

def backtest_macd(
    df: pd.DataFrame,
    initial_equity=10_000.0,
    fee_bps=4.0,
    slippage_bps=1.0,
    risk_per_trade=0.01,
    atr_mult=2.0,
    max_leverage=1.0
):
    equity = initial_equity
    position_qty = 0.0
    entry_price = None
    stop_price = None
    trades: List[Trade] = []
    equity_curve = []
    fee_rate = fee_bps / 10_000.0
    slip_rate = slippage_bps / 10_000.0
    for t, row in df.iterrows():
        o, h, l, c = float(row["Open"]), float(row["High"]), float(row["Low"]), float(row["Close"])
        sig = int(row["signal"])
        atr = float(row["atr"]) if "atr" in df.columns else np.nan
        if position_qty > 0:
            if stop_price is not None and l <= stop_price:
                exit_px = stop_price * (1 - slip_rate)
                cost = exit_px * position_qty * fee_rate
                pnl = (exit_px - entry_price) * position_qty - cost
                equity += pnl
                trades[-1].exit_time = t
                trades[-1].exit_price = exit_px
                trades[-1].pnl = pnl
                trades[-1].reason = "stop"
                position_qty = 0.0
                entry_price = None
                stop_price = None
            elif sig == -1:
                exit_px = o * (1 - slip_rate)
                cost = exit_px * position_qty * fee_rate
                pnl = (exit_px - entry_price) * position_qty - cost
                equity += pnl
                trades[-1].exit_time = t
                trades[-1].exit_price = exit_px
                trades[-1].pnl = pnl
                trades[-1].reason = "signal_exit"
                position_qty = 0.0
                entry_price = None
                stop_price = None
        if position_qty == 0 and sig == 1:
            entry_px = o * (1 + slip_rate)
            qty = position_size(
                equity=equity,
                entry_price=entry_px,
                atr=atr,
                risk_per_trade=risk_per_trade,
                atr_mult=atr_mult,
                max_leverage=max_leverage
            )
            if qty > 0:
                cost = entry_px * qty * fee_rate
                equity -= cost
                position_qty = qty
                entry_price = entry_px
                stop_price = entry_px - atr_mult * atr if (atr is not None and not np.isnan(atr)) else None
                trades.append(Trade(entry_time=t, exit_time=None, entry_price=entry_px, exit_price=None, qty=qty, pnl=None, reason=None))
        unreal = 0.0
        if position_qty > 0 and entry_price is not None:
            unreal = (c - entry_price) * position_qty
        equity_curve.append((t, equity + unreal))
    eq = pd.DataFrame(equity_curve, columns=["time", "equity"]).set_index("time")
    return eq, trades