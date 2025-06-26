import pandas as pd

def simulate_trades(df: pd.DataFrame, initial_capital: float = 10000.0):
    capital = initial_capital
    position = 0
    trade_log = []
    equity_curve = []

    for idx, row in df.iterrows():
        price = row['close']
        ema = row.get('EMA_20', None)
        rsi = row.get('RSI_14', None)

        if pd.isna(price) or pd.isna(ema) or pd.isna(rsi):
            equity = capital if position == 0 else position * price
            equity_curve.append({
                "timestamp": idx.isoformat(),
                "equity": round(equity, 2)
            })
            continue

        # Buy condition
        if position == 0 and price > ema and rsi < 70:
            position = capital / price
            capital = 0
            trade_log.append({"type": "BUY", "price": price, "timestamp": idx.isoformat()})

        # Sell condition
        elif position > 0 and price < ema and rsi > 30:
            capital = position * price
            position = 0
            trade_log.append({"type": "SELL", "price": price, "timestamp": idx.isoformat()})

        # Update equity
        equity = capital if position == 0 else position * price
        equity_curve.append({
            "timestamp": idx.isoformat(),
            "equity": round(equity, 2)
        })

    final_equity = capital if position == 0 else position * df.iloc[-1]['close']
    profit = final_equity - initial_capital

    return {
        "final_equity": round(final_equity, 2),
        "total_profit": round(profit, 2),
        "trades": trade_log,
        "equity_curve": equity_curve
    }
