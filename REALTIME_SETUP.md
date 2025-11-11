# 🔄 Real-Time Dashboard Setup

## Overview

The dashboard now supports **real-time data updates every 10 seconds**. New data is automatically fetched, processed, and displayed.

## How It Works

1. **Data Producer** generates new batch files every 10 seconds
2. **Backend API** reads the latest data from batch files
3. **Frontend Dashboard** automatically refreshes every 10 seconds
4. **Charts update** in real-time with new data

## Setup Instructions

### Step 1: Start the Real-Time Producer

**Open a NEW PowerShell window** and run:

```powershell
python realtime_producer.py
```

You'll see:
```
======================================================================
REAL-TIME STOCK DATA PRODUCER
======================================================================
Generating new data every 10 seconds...
Output directory: D:\M2\Big Data 2\lab7\stock_stream
Symbols: AAPL, GOOGL, MSFT, AMZN, TSLA
======================================================================
Press Ctrl+C to stop

[10:30:15] Batch 58 - AAPL: $182.45, GOOGL: $141.23, MSFT: $371.89, AMZN: $146.12, TSLA: $238.76
[10:30:25] Batch 59 - AAPL: $183.12, GOOGL: $140.89, MSFT: $370.45, AMZN: $145.67, TSLA: $239.23
...
```

**Keep this running!** This continuously generates new data.

### Step 2: Start the Backend API

**In another PowerShell window:**

```powershell
python dashboard_backend.py
```

**Keep this running!** The backend reads new batch files as they're created.

### Step 3: Start the Frontend Dashboard

**In another PowerShell window:**

```powershell
cd dashboard_frontend
npm start
```

The dashboard will:
- Open automatically at `http://localhost:3000`
- Show a **"Live Data"** indicator with pulsing dot
- **Auto-refresh every 10 seconds** with new data
- Display **"Last Update"** timestamp in the header

## What You'll See

### Real-Time Updates

- **Overview Cards**: Prices update every 10 seconds
- **Price Trends Chart**: New data points appear automatically
- **Volatility Chart**: Updates with latest volatility calculations
- **Volume Chart**: Shows latest trading volumes
- **Correlation Heatmap**: Updates as prices change
- **VaR Chart**: Risk metrics update in real-time

### Visual Indicators

- **Pulsing green dot**: Shows dashboard is live
- **"Last Update" timestamp**: Shows when data was last refreshed
- **Smooth chart animations**: Charts animate when new data arrives

## Running All Services

You need **3 PowerShell windows**:

1. **Window 1**: `python realtime_producer.py` (generates data)
2. **Window 2**: `python dashboard_backend.py` (serves API)
3. **Window 3**: `cd dashboard_frontend && npm start` (dashboard UI)

## Stopping Services

Press `Ctrl+C` in each window to stop:
1. Stop producer (Window 1)
2. Stop backend (Window 2)
3. Stop frontend (Window 3)

## Data Flow

```
Real-Time Producer (every 10s)
    │
    ├─▶ Generates batch_N.json
    │   (5 stock ticks: AAPL, GOOGL, MSFT, AMZN, TSLA)
    │
    ▼
Backend API (reads on request)
    │
    ├─▶ Loads all batch files
    ├─▶ Calculates metrics (volatility, changes, etc.)
    │
    ▼
Frontend Dashboard (every 10s)
    │
    ├─▶ Fetches data from API
    ├─▶ Updates all charts
    └─▶ Shows "Last Update" timestamp
```

## Customization

### Change Update Interval

**Frontend (dashboard refresh):**
Edit `dashboard_frontend/src/components/Dashboard.js`:
```javascript
const interval = setInterval(fetchData, 10000); // Change 10000 to desired ms
```

**Producer (data generation):**
Edit `realtime_producer.py`:
```python
producer.run(interval=10)  # Change 10 to desired seconds
```

### Start Prices

Edit `realtime_producer.py` to change initial prices:
```python
self.prices = {
    'AAPL': 180.0,   # Change these values
    'GOOGL': 140.0,
    'MSFT': 370.0,
    'AMZN': 145.0,
    'TSLA': 240.0
}
```

## Troubleshooting

### No data appearing
- Make sure producer is running
- Check `stock_stream/` folder has new `batch_*.json` files
- Verify backend is reading files (check backend terminal)

### Charts not updating
- Check browser console (F12) for errors
- Verify frontend refresh interval is 10 seconds
- Make sure all 3 services are running

### Producer not generating files
- Check file permissions on `stock_stream/` folder
- Verify Python has write access
- Check for errors in producer terminal

## Performance Notes

- **Producer**: Very lightweight, minimal CPU usage
- **Backend**: Processes all batch files on each request (may slow with 1000+ files)
- **Frontend**: Smooth updates, React handles re-rendering efficiently

For long-running sessions, consider periodically cleaning old batch files.

