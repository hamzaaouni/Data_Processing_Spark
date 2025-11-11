# 🚀 Quick Start Guide - Dashboard

## ✅ Step 1: Install Frontend Dependencies (First Time Only)

```powershell
cd dashboard_frontend
npm install
cd ..
```

**This only needs to be done once!** It will take 2-3 minutes.

## ✅ Step 2: Start the Dashboard

You need **TWO PowerShell windows**:

### Window 1 - Backend API
```powershell
python dashboard_backend.py
```

Wait until you see:
```
API will be available at: http://localhost:5000
```

### Window 2 - Frontend Dashboard  
```powershell
cd dashboard_frontend
npm start
```

Your browser will automatically open at `http://localhost:3000` 🎉

---

## 📋 What You'll See

- **Overview Cards** - Quick stats for each stock (AAPL, GOOGL, MSFT, AMZN, TSLA)
- **Price Trends** - Interactive line chart showing price movements
- **Volatility Chart** - Bar chart comparing volatility
- **Volume Chart** - Trading volume statistics  
- **VaR Chart** - Value at Risk analysis
- **Correlation Heatmap** - Interactive correlation matrix

## 🛑 To Stop

Press `Ctrl+C` in both windows, then close your browser.

---

## ❓ Troubleshooting

**"Cannot connect to API"**
- Make sure Window 1 (backend) is running
- Check `http://localhost:5000/api/health` in your browser

**"No data available"**
- Run the Spark lab first: `python lab7.py` or `.\run-docker.ps1`
- Make sure `stock_stream/` folder has `batch_*.json` files

**Frontend won't start**
- Delete `dashboard_frontend\node_modules` folder
- Run `cd dashboard_frontend && npm install` again

