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
Screensho![Screenshot (77)](https://github.com/user-attachments/assets/4c7edfd3-0639-4eaa-8860-414f3214055f)
ts:
![Screenshot (76)](https://github.com/user-attachments/assets/03e73b0c-e71b-4417-8423-c1a87a56f33d)
![Screenshot (75)](https://github.com/user-attachments/assets/8bdc5189-1165-4737-af53-093e932cb792)
![Screenshot (74)](https://github.com/user-attachments/assets/b81929e1-0070-45c0-bcd7-d2ea04232a7f)
![Screenshot (73)](https://github.com/user-attachments/assets/494fabdd-3591-4c50-82a3-3dace5f0074f)
![Screenshot (72)](https://github.com/user-attachments/assets/3f4916dd-0f10-4250-97df-cf592ce51f2c)
![Screenshot (71)](https://github.com/user-attachments/assets/ff0f877e-ba5b-4c2e-ae14-362e1961b473)
![Screenshot (70)](https://github.com/user-attachments/assets/9c2c59ea-8f07-4ed1-81bf-aba0c0618dc7)
![Screenshot (69)](https://github.com/user-attachments/assets/fbf3e318-08c5-4f9c-b58f-e50d2d25000b)
![Screenshot (68)](https://github.com/user-attachments/assets/7a3524d8-4b69-4b63-9b0d-2651c42595da)
![Screenshot (67)](https://github.com/user-attachments/assets/29b974dd-4b84-4010-b4b5-da018f578fa7)
![Screenshot (66)](https://github.com/user-attachments/assets/630b44f6-ed63-4874-8eca-682ce7ead5eb)
![Screenshot (65)](https://github.com/user-attachments/assets/9c91aad8-304b-4ec2-8c44-ffbffd37afe7)

