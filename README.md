# backtesting-platform
Backtesting Platform (Full-Stack)
A full-stack backtesting platform that allows users to simulate trading strategies on historical data using technical indicators such as EMA, RSI, and MACD. The platform includes real-time WebSocket updates, a performance dashboard, and a visual strategy builder.
🚀 Features
✅ Backend (FastAPI)
OHLCV data ingestion from CSV
REST API for backtesting
WebSocket endpoint for real-time simulation logs
Supports indicators:
EMA (Exponential Moving Average)
RSI (Relative Strength Index)
MACD (Moving Average Convergence Divergence)
Risk management parameters:
Stop Loss
Take Profit
Performance metrics:
PnL
Sharpe Ratio
Win Rate
Max Drawdown (%, $)
CAGR
Volatility
Trade Count
Avg Trade Duration
Largest Win / Loss
🎨 Frontend (React + Bootstrap)
Visual Strategy Builder (form-based)
PnL Bar Chart using react-chartjs-2
Detailed backtest result summary table
Live WebSocket log view for trades
🧱 Tech Stack
LayerTechnologyBackendFastAPI, Python, PandasFrontendReact, Bootstrap 5ChartsChart.jsWebSocketFastAPI WebSocketDataCSV (BTC-1d sample data)📁 Folder Structure
project/
├── backend/
│   └── main.py
│   └── data/BTC-1d.csv
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StrategyBuilder.js
│   │   │   ├── BacktestResult.js
│   │   │   ├── PnlBarChart.js
│   │   │   ├── BacktestLogs.js
│   │   ├── pages/Backtest.js
│   │   └── services/api.js
│   └── public/
⚙️ Setup Instructions
📦 Backend (FastAPI)
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install fastapi uvicorn pandas numpy
uvicorn main:app --reload
Make sure BTC-1d.csv is located inside the data/ folder.

🌐 Frontend (React)
cd frontend
npm install
npm start
Runs the app at http://localhost:3000.

Ensure the backend is running on http://localhost:8000.
🔌 API Endpoints
REST: POST /backtest
{
  "indicator": "EMA",
  "period": 14,
  "startDate": "2025-05-01",
  "endDate": "2025-06-20",
  "stopLoss": 2,
  "takeProfit": 5
}
WebSocket: /ws/backtest
Sends back entry/exit logs in real time
📊 Example Output
{
  "pnl": -2060.24,
  "sharpe": -0.88,
  "winRate": 50.0,
  "tradeCount": 2,
  "maxDrawdown": 2.19,
  "maxDrawdownDollar": 2195.64,
  "cagr": -25.34,
  "volatility": 1165.52,
  "largestWin": 135.40,
  "largestLoss": -2195.64,
  "avgTradeDuration": 2.5,
  "trades": [ ... ]
}
🧪 Testing Tips
Try changing indicator to RSI or MACD.
Vary stopLoss and takeProfit to simulate tighter/looser risk settings.
📘 Credits
Designed & implemented by Goutham
Built with ❤️ using FastAPI + React
📦 To-Do (Optional Enhancements)
Visual drag-and-drop logic builder
Multi-asset portfolio simulation
Export results as CSV or image
