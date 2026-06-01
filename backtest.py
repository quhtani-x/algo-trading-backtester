import numpy as np
# DISCLAIMER , some  comments has been added by Ai as my code didnt have much comments and i told the Ai to explain the code , also remove dead commented code

# ALGO TRADING BACKTESTER.
# tests a moving-average crossover strategy on price data and shows how much
# money you'd have made vs just holding. buy when the fast average crosses above
# the slow one, sell when it crosses back down. plots the price + trades + the
# equity curve so you can SEE if the strategy actually works.
#
# it makes its own fake-but-realistic price data so it runs with no downloads.


def fake_prices(days=500, seed=7):
    # random walk with a slight upward drift, looks like a real chart
    rng = np.random.default_rng(seed)
    returns = rng.normal(0.0005, 0.02, days)
    return 100 * np.exp(np.cumsum(returns))


def moving_average(x, n):
    # simple moving average
    return np.convolve(x, np.ones(n) / n, mode="valid")


def backtest(prices, fast=20, slow=50, cash=10000):
    fast_ma = moving_average(prices, fast)
    slow_ma = moving_average(prices, slow)
    # line them up (slow ma is shorter)
    offset = slow - fast
    fast_ma = fast_ma[offset:]
    idx = np.arange(slow - 1, len(prices))

    holding = False
    shares = 0
    equity = []
    buys, sells = [], []

    for i in range(len(idx)):
        price = prices[idx[i]]
        # crossover signals
        if not holding and fast_ma[i] > slow_ma[i]:
            shares = cash / price       # go all in
            cash = 0
            holding = True
            buys.append((idx[i], price))
        elif holding and fast_ma[i] < slow_ma[i]:
            cash = shares * price        # sell everything
            shares = 0
            holding = False
            sells.append((idx[i], price))
        equity.append(cash + shares * price)

    final = equity[-1]
    hold_final = 10000 / prices[slow - 1] * prices[-1]  # buy & hold benchmark
    return idx, np.array(equity), buys, sells, final, hold_final


def main():
    prices = fake_prices()
    idx, equity, buys, sells, final, hold_final = backtest(prices)

    print(f"strategy final:  ${final:,.0f}")
    print(f"buy & hold:      ${hold_final:,.0f}")
    print(f"trades taken:    {len(buys)} buys, {len(sells)} sells")

    # ---- charts ---- (import here so the logic above runs without matplotlib)
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    ax1.plot(prices, color="#888", label="price")
    if buys:
        ax1.scatter(*zip(*buys), marker="^", color="green", s=80, label="buy")
    if sells:
        ax1.scatter(*zip(*sells), marker="v", color="red", s=80, label="sell")
    ax1.set_title("price + trades (MA crossover)")
    ax1.legend()

    ax2.plot(idx, equity, color="#2a9d8f", label="strategy")
    ax2.axhline(10000, color="#ccc", linestyle="--", label="start ($10k)")
    ax2.set_title("equity curve")
    ax2.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
