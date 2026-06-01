# Algo Trading Backtester

Tests a moving-average crossover trading strategy on price data and shows
whether it actually beats just holding. Buy when the fast moving average crosses
above the slow one, sell when it crosses back down. It plots the price with the
buy/sell markers and the **equity curve** so you can see the strategy working.

It generates its own realistic random-walk price data, so it runs with no
downloads or API keys.

## what it shows

- price chart with green ▲ buys and red ▼ sells
- equity curve vs the starting $10k
- strategy final value vs a buy-and-hold benchmark

## run

```bash
pip install numpy matplotlib
python backtest.py
```

example output:

```
strategy final:  $7,012
buy & hold:      $4,650
trades taken:    5 buys, 5 sells
```

tags: ai, finance, trading, backtesting, numpy, matplotlib

backtesting before risking real money - this is how quants check an idea.
