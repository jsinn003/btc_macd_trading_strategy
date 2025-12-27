from macd_strategy.macd import add_macd, add_ema
from macd_strategy.signal_generation import generate_signals
from position_sizing import add_atr
from trade_simulation import backtest_macd
from backtest import compute_metrics
from loader import load_data
from utils import resample_ohlcv


def run_pipeline(path: str):
    df_1m = load_data(path)
    df_15m = resample_ohlcv(df_1m, "15m")
    df_15m = add_macd(df_15m, fast=12, slow=26, signal=9)
    df_15m = add_ema(df_15m, span=200)
    df_15m = generate_signals(df_15m)
    df_15m.loc[df_15m["Close"] <= df_15m["ema_200"], "signal"] = 0
    df_1m["signal"] = (
        df_15m["signal"]
        .reindex(df_1m.index, method="ffill")
        .fillna(0)
        .astype(int)
    )
    df_1m = add_atr(df_1m, n=14)
    equity_curve, trades = backtest_macd(
        df_1m,
        initial_equity=10_000.0,
        fee_bps=4.0,
        slippage_bps=1.0,
        risk_per_trade=0.01,
        atr_mult=4.0,
        max_leverage=1.0
    )
    metrics = compute_metrics(equity_curve)
    print(metrics)
    print(f"Trades: {len(trades)}")

    # diagnostics
    reasons = {}
    for tr in trades:
        if tr.reason is not None:
            reasons[tr.reason] = reasons.get(tr.reason, 0) + 1
    print("Exit reasons:", reasons)
    durations = [
        (tr.exit_time - tr.entry_time).total_seconds() / 60
        for tr in trades
        if tr.exit_time is not None
    ]
    if durations:
        print("Avg holding (min):", sum(durations) / len(durations))
        print("Median holding (min):", sorted(durations)[len(durations)//2])
    pnls = [tr.pnl for tr in trades if tr.pnl is not None]
    if pnls:
        print("Avg pnl per trade:", sum(pnls) / len(pnls))
        print("Win rate:", sum(p > 0 for p in pnls) / len(pnls))
    return df_1m, equity_curve, trades

df, eq, trades = run_pipeline("btc_usdc_data/full_btc_usdc_data_clean.csv")