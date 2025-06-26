from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
import numpy as np
from datetime import datetime
from fastapi import WebSocket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Models -----------

class StrategyInput(BaseModel):
    indicator: str
    period: int
    startDate: str
    endDate: str
    stopLoss: float = 0
    takeProfit: float = 0

class Trade(BaseModel):
    entryTime: str
    exitTime: str
    entryPrice: float
    exitPrice: float
    pnl: float

class BacktestResult(BaseModel):
    pnl: float
    sharpe: float
    winRate: float
    tradeCount: int
    maxDrawdown: float
    maxDrawdownDollar: float
    cagr: float
    volatility: float
    largestWin: float
    largestLoss: float
    avgTradeDuration: float
    trades: List[Trade]

# ----------- Indicators -----------

def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line, macd_line - signal_line

# ----------- Metrics Calculation -----------

def calculate_metrics(pnls, equity_curve, trades):
    max_drawdown = 0
    max_drawdown_dollar = 0
    peak = equity_curve[0] if equity_curve else 0
    durations = []
    largest_win = max(pnls) if pnls else 0
    largest_loss = min(pnls) if pnls else 0

    for val in equity_curve:
        if val > peak:
            peak = val
        dd = (peak - val) / peak
        dd_dollar = (peak - val)
        max_drawdown = max(max_drawdown, dd)
        max_drawdown_dollar = max(max_drawdown_dollar, dd_dollar)

    for trade in trades:
        entry = datetime.strptime(trade['entryTime'], "%Y-%m-%d")
        exit = datetime.strptime(trade['exitTime'], "%Y-%m-%d")
        durations.append((exit - entry).days)

    avg_duration = round(np.mean(durations), 2) if durations else 0
    volatility = round(np.std(pnls), 2) if pnls else 0
    cagr = round((1 + (sum(pnls) / equity_curve[0])) ** (365 / len(equity_curve)) - 1, 4) if equity_curve else 0

    return max_drawdown * 100, max_drawdown_dollar, cagr * 100, volatility, largest_win, largest_loss, avg_duration

# ----------- Trade Simulation -----------

def simulate_trades(df, indicator_type, stop_loss_pct, take_profit_pct):
    trades = []
    pnl_list = []
    equity_curve = []
    wins = 0
    position = None
    capital = 100000
    equity = capital

    for i in range(1, len(df)):
        row = df.iloc[i]
        close = row['close']
        time = row.name
        signal = None

        if indicator_type == 'EMA' and not pd.isna(row.get('ema')):
            signal = 'buy' if close > row['ema'] else 'sell'
        elif indicator_type == 'RSI' and not pd.isna(row.get('rsi')):
            if row['rsi'] < 30:
                signal = 'buy'
            elif row['rsi'] > 70:
                signal = 'sell'
        elif indicator_type == 'MACD' and pd.notna(row.get('macd_line')) and pd.notna(row.get('signal_line')):
            signal = 'buy' if row['macd_line'] > row['signal_line'] else 'sell'

        if signal == 'buy' and position is None:
            position = {"entry_price": close, "entry_time": time}

        elif position:
            entry_price = position["entry_price"]
            sl = entry_price - (entry_price * stop_loss_pct / 100)
            tp = entry_price + (entry_price * take_profit_pct / 100)

            should_exit = close <= sl or close >= tp or signal == 'sell'
            if should_exit:
                pnl = close - entry_price
                equity += pnl
                pnl_list.append(pnl)
                if pnl > 0:
                    wins += 1
                trades.append({
                    "entryTime": position["entry_time"].strftime("%Y-%m-%d"),
                    "exitTime": time.strftime("%Y-%m-%d"),
                    "entryPrice": round(entry_price, 2),
                    "exitPrice": round(close, 2),
                    "pnl": round(pnl, 2)
                })
                position = None
        equity_curve.append(equity)

    total_pnl = round(sum(pnl_list), 2)
    sharpe = round(np.mean(pnl_list) / np.std(pnl_list), 2) if len(pnl_list) > 1 and np.std(pnl_list) > 0 else 0.0
    win_rate = round((wins / len(pnl_list)) * 100, 2) if pnl_list else 0.0

    mdd, mdd_dollar, cagr, vol, lwin, lloss, avg_dur = calculate_metrics(pnl_list, equity_curve, trades)

    return total_pnl, sharpe, win_rate, trades, len(trades), mdd, mdd_dollar, cagr, vol, lwin, lloss, avg_dur

# ----------- REST API -----------

@app.post("/backtest", response_model=BacktestResult)
def run_backtest(strategy: StrategyInput):
    df = pd.read_csv("data/BTC-1d.csv", delimiter=';')
    df.columns = df.columns.str.strip().str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp').sort_index()
    df = df[strategy.startDate : strategy.endDate]

    indicator = strategy.indicator.upper()
    if indicator == 'EMA':
        df['ema'] = calculate_ema(df['close'], strategy.period)
    elif indicator == 'RSI':
        df['rsi'] = calculate_rsi(df['close'], strategy.period)
    elif indicator == 'MACD':
        macd_line, signal_line, macd_hist = calculate_macd(df['close'])
        df['macd_line'], df['signal_line'], df['macd_hist'] = macd_line, signal_line, macd_hist
    else:
        raise ValueError("Unsupported indicator")

    pnl, sharpe, win_rate, trades, count, mdd, mdd_dollar, cagr, vol, lwin, lloss, avg_dur = simulate_trades(
        df, indicator, strategy.stopLoss, strategy.takeProfit)

    return {
        "pnl": pnl,
        "sharpe": sharpe,
        "winRate": win_rate,
        "tradeCount": count,
        "maxDrawdown": mdd,
        "maxDrawdownDollar": mdd_dollar,
        "cagr": cagr,
        "volatility": vol,
        "largestWin": lwin,
        "largestLoss": lloss,
        "avgTradeDuration": avg_dur,
        "trades": trades
    }

@app.websocket("/ws/backtest")
async def websocket_backtest(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            strategy = StrategyInput(**data)

            df = pd.read_csv("data/BTC-1d.csv", delimiter=';')
            df.columns = df.columns.str.strip().str.lower()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp').sort_index()
            df = df[strategy.startDate : strategy.endDate]

            indicator = strategy.indicator.upper()
            if indicator == 'EMA':
                df['ema'] = calculate_ema(df['close'], strategy.period)
            elif indicator == 'RSI':
                df['rsi'] = calculate_rsi(df['close'], strategy.period)
            elif indicator == 'MACD':
                macd_line, signal_line, macd_hist = calculate_macd(df['close'])
                df['macd_line'], df['signal_line'], df['macd_hist'] = macd_line, signal_line, macd_hist
            else:
                await websocket.send_text("❌ Unsupported indicator")
                continue

            pnl, sharpe, win_rate, trades, count, mdd, mdd_dollar, cagr, vol, lwin, lloss, avg_dur = simulate_trades(
                df, indicator, strategy.stopLoss, strategy.takeProfit)

            result = {
                "pnl": pnl,
                "sharpe": sharpe,
                "winRate": win_rate,
                "tradeCount": count,
                "maxDrawdown": mdd,
                "maxDrawdownDollar": mdd_dollar,
                "cagr": cagr,
                "volatility": vol,
                "largestWin": lwin,
                "largestLoss": lloss,
                "avgTradeDuration": avg_dur,
                "trades": trades
            }

            await websocket.send_json(result)

    except Exception as e:
        await websocket.send_text(f"❌ Error: {str(e)}")

    finally:
        await websocket.close()


