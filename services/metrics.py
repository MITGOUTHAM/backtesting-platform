import numpy as np
import pandas as pd

def calculate_total_return(initial, final):
    return round(((final - initial) / initial) * 100, 2)

def calculate_win_rate(trades):
    if not trades or len(trades) < 2:
        return 0.0

    wins = 0
    for i in range(1, len(trades), 2):
        buy = trades[i - 1]
        sell = trades[i]
        if buy["type"] == "BUY" and sell["type"] == "SELL":
            if sell["price"] > buy["price"]:
                wins += 1

    total_rounds = len(trades) // 2
    return round((wins / total_rounds) * 100, 2) if total_rounds else 0.0

def calculate_avg_pnl(trades):
    if len(trades) < 2:
        return 0.0

    pnls = []
    for i in range(1, len(trades), 2):
        buy = trades[i - 1]
        sell = trades[i]
        if buy["type"] == "BUY" and sell["type"] == "SELL":
            pnl = sell["price"] - buy["price"]
            pnls.append(pnl)

    return round(np.mean(pnls), 2) if pnls else 0.0

def calculate_max_drawdown(equity_curve):
    values = [point['equity'] for point in equity_curve]
    peak = values[0]
    max_dd = 0
    for val in values:
        peak = max(peak, val)
        dd = (peak - val) / peak
        max_dd = max(max_dd, dd)
    return round(max_dd * 100, 2)

def calculate_sharpe_ratio(equity_curve, risk_free_rate=0.0):
    values = [point['equity'] for point in equity_curve]
    returns = pd.Series(values).pct_change().dropna()
    if returns.empty:
        return 0.0
    mean_return = returns.mean()
    std_dev = returns.std()
    if std_dev == 0:
        return 0.0
    sharpe = (mean_return - risk_free_rate) / std_dev
    return round(sharpe * np.sqrt(252), 2)  # annualized
