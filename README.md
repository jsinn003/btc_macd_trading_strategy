# BTC Algorithmic Trading Research Pipeline

This project implements a complete end-to-end algorithmic trading research pipeline for Bitcoin (BTCUSDC), covering data ingestion, indicator computation, signal generation, risk management, backtesting, and performance evaluation.

The goal of the project is **not** to optimize a single indicator, but to build a reusable and realistic framework for evaluating trading ideas under real-world constraints such as execution costs and market noise.

## Data

Market data is not included in this repository.
BTCUSDC minute-level OHLCV data is sourced from Binance Futures and can be downloaded using:
python btc_download.py
The raw data is then cleaned and prepared for research using:
python clean_data.py

## Project Overview
The pipeline supports:
- Minute-level OHLCV data ingestion
- Multi-timeframe signal generation
- Indicator computation (MACD, EMA, ATR)
- Risk-based position sizing
- Trade simulation
- Transaction costs (fees & slippage)
- Performance metrics (return, drawdown, Sharpe)
- Strategy diagnostics (win rate, holding time, exit reasons)
The system is modular by design: signals, execution, and risk logic are intentionally separated to allow clean experimentation.

## Strategy Implemented
### Base Strategy
- **Signal**: MACD crossover
- **Signal timeframe**: 15m / 30m / 1h (tested)
- **Execution timeframe**: 1-minute
- **Filter**: Trend regime filter using EMA-200 on signal timeframe
- **Risk model**:
  - ATR-based stop-loss
  - Fixed fraction risk per trade
  - No leverage (1x)

### Execution Assumptions
- Market (taker) execution
- Configurable fees and slippage
- Conservative stop execution logic

## Key Findings
- Naive 1-minute MACD massively overtrades and is destroyed by transaction costs.
- Multi-timeframe signals significantly reduce noise and trade frequency.
- Trend filtering (EMA-200) materially improves trade quality.
- Despite structural improvements, MACD crossover strategies on BTC **do not generate sufficient alpha to overcome realistic trading costs** in this setup.
- Increasing signal timeframe reduces trade frequency but eventually degrades signal quality.

## Project Structure

```text
.
├── macd_strategy/
│   ├── macd.py               # MACD & EMA indicators
│   └── signal_generation.py  # Signal logic
├── btc_download.py        	  # BTC raw data download
├── clean_data.py        	  # BTC raw data cleaning
├── position_sizing.py        # ATR & position sizing
├── trade_simulation.py       # Event-driven backtest engine
├── backtest.py               # Performance metrics
├── loader.py                 # Data loading & cleaning
├── utils.py                  # Resampling utilities
├── run.py                    # Main research pipeline
├── btc_usdc_data/            # Local OHLCV data (not tracked)
└── README.md