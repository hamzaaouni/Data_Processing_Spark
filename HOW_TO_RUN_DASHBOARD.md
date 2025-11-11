# How to Run the Dashboard - Step by Step Guide

## Prerequisites Check

✅ **Node.js** - Already installed (v22.18.0)  
✅ **Python** - Already installed  
✅ **Pandas, Matplotlib, Seaborn** - Already installed  

## Step 1: Install Backend Dependencies

Open PowerShell in the lab7 directory and run:

```powershell
pip install flask flask-cors
```

This will install:
- Flask (web framework for the API)
- Flask-CORS (to allow React to connect to the API)

## Step 2: Install Frontend Dependencies

```powershell
cd dashboard_frontend
npm install
cd ..
```

This will install:
- React
- Recharts (for charts)
- Axios (for API calls)
- Other React dependencies

**Note:** This may take a few minutes the first time.

## Step 3: Start the Dashboard

You need **TWO terminal windows** open:

### Terminal 1 - Backend API

```powershell
python dashboard_backend.py
```

You should see:
```
======================================================================
SPARK STREAMING LAB - DASHBOARD API
======================================================================
Starting Flask server...
API will be available at: http://localhost:5000
```

**Keep this terminal open!**

### Terminal 2 - Frontend (React)

```powershell
cd dashboard_frontend
npm start
```

This will:
- Start the React development server
- Automatically open your browser at `http://localhost:3000`
- Show the dashboard with all visualizations

**Keep this terminal open too!**

## Step 4: View the Dashboard

Once both services are running:
- Backend API: `http://localhost:5000`
- Frontend Dashboard: `http://localhost:3000` (opens automatically)

The dashboard will show:
- 📊 Overview cards for each stock
- 📈 Price trends chart
- 📊 Volatility analysis
- 💹 Volume statistics
- 🔗 Correlation heatmap
- 💰 Value at Risk (VaR)

## Troubleshooting

### Backend won't start
- **Port 5000 in use?** - Close other applications using port 5000
- **No data?** - Make sure you've run the Spark lab first to generate data in `stock_stream/` folder
- **Module not found?** - Run `pip install flask flask-cors` again

### Frontend won't start
- **Port 3000 in use?** - React will ask to use a different port, say yes
- **npm install failed?** - Delete `node_modules` folder and run `npm install` again
- **Can't connect to API?** - Make sure backend is running on port 5000

### Dashboard shows "Cannot connect to API"
1. Check that `dashboard_backend.py` is running
2. Open `http://localhost:5000/api/health` in browser - should show `{"status":"ok"}`
3. Check browser console (F12) for errors

### No data displayed
- Run the Spark lab first: `python lab7.py` or `.\run-docker.ps1`
- Check that `stock_stream/` folder contains `batch_*.json` files

## Quick Commands Summary

```powershell
# Install backend dependencies
pip install flask flask-cors

# Install frontend dependencies
cd dashboard_frontend
npm install
cd ..

# Start backend (Terminal 1)
python dashboard_backend.py

# Start frontend (Terminal 2)
cd dashboard_frontend
npm start
```

## Stopping the Dashboard

- Press `Ctrl+C` in both terminals to stop the services
- Close the browser tab

## Next Steps

Once running, the dashboard will:
- Automatically refresh data every 30 seconds
- Show real-time updates if you run the Spark lab again
- Allow you to interact with all charts (hover, zoom, etc.)

Enjoy your interactive dashboard! 🎉

