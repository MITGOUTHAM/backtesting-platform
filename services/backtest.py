import pandas as pd
from app.models.strategy import StrategyRequest
from app.indicators.ema import calculate_ema
from app.indicators.rsi import calculate_rsi
from app.services.simulator import simulate_trades
from app.services.metrics import (
    calculate_total_return,
    calculate_win_rate,
    calculate_avg_pnl,
    calculate_max_drawdown,
    calculate_sharpe_ratio
)

def run_backtest(request: StrategyRequest):
    file_path = f"app/data/{request.symbol}-{request.interval}.csv"

    try:
        df = pd.read_csv(file_path, sep=';')
    except FileNotFoundError:
        return {"status": "error", "message": f"File not found: {file_path}"}

    df.columns = df.columns.str.strip().str.lower()

    if 'timestamp' not in df.columns or 'close' not in df.columns:
        return {"status": "error", "message": "CSV must contain 'timestamp' and 'close' columns."}

    try:
        timestamp_col = df['timestamp'].astype(str)
        if timestamp_col.str.isnumeric().all() and timestamp_col.str.len().max() >= 10:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        else:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    except Exception as e:
        return {"status": "error", "message": f"Timestamp parsing failed: {str(e)}"}

    df = df.dropna(subset=['timestamp', 'close'])
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df = df.dropna(subset=['close'])

    df.set_index('timestamp', inplace=True)
    df = df.sort_index()

    if df.empty:
        return {"status": "error", "message": "No valid data rows after cleaning."}

    indicators_lower = [i.lower() for i in request.indicators]

    if 'ema' in indicators_lower:
        df['EMA_20'] = calculate_ema(df['close'], period=20)
    if 'rsi' in indicators_lower:
        df['RSI_14'] = calculate_rsi(df['close'], period=14)

    sim_result = simulate_trades(df, initial_capital=request.capital)
    final_equity = sim_result["final_equity"]
    trades = sim_result["trades"]
    equity_curve = sim_result["equity_curve"]
    # Prepare equity curve for frontend chart
    equity_df = equity_curve.reset_index().rename(columns={"timestamp": "date"})
    equity_curve_data = equity_df.to_dict(orient="records")


    metrics = {
        "total_return": calculate_total_return(request.capital, final_equity),
        "win_rate": calculate_win_rate(trades),
        "avg_pnl_per_trade": calculate_avg_pnl(trades),
        "max_drawdown": calculate_max_drawdown(equity_curve),
        "sharpe_ratio": calculate_sharpe_ratio(equity_curve)
    }
    equity_curve_df = sim_result["equity_curve"].reset_index()
    equity_curve_df.rename(columns={"timestamp": "date"}, inplace=True)
    equity_curve_records = equity_curve_df.to_dict(orient="records")


    return {
        "status": "success",
        "result": {
            "rows_loaded": len(df),
            "indicators_applied": request.indicators,
            "total_trades": len(trades),
            "final_equity": final_equity,
            "total_profit": final_equity - request.capital,
            "metrics": metrics,
            "trades": trades[-5:],
            #
            
        }
    }
