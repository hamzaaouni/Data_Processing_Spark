# Spark Streaming Lab - Interactive Dashboard

A modern, interactive web dashboard for visualizing Spark streaming lab results in real-time.

## Features

- 📊 **Real-time Price Trends** - Interactive line charts showing stock price movements
- 📈 **Volatility Analysis** - Visualize volatility patterns across stocks
- 💹 **Volume Analysis** - Trading volume statistics and trends
- 🔗 **Correlation Matrix** - Interactive heatmap showing stock price correlations
- 💰 **Value at Risk (VaR)** - Risk analysis with 95% confidence intervals
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ and npm (for frontend)
- Data from Spark streaming lab (batch files in `stock_stream/` directory)

## Installation

### 1. Install Backend Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```powershell
cd dashboard_frontend
npm install
cd ..
```

## Running the Dashboard

### Option 1: Run Both Services (Recommended)

**Terminal 1 - Backend:**
```powershell
python dashboard_backend.py
```

**Terminal 2 - Frontend:**
```powershell
cd dashboard_frontend
npm start
```

The dashboard will automatically open at `http://localhost:3000`

### Option 2: Run in Docker

If you prefer to run everything in Docker, you can modify the docker-compose.yml to include the dashboard services.

## API Endpoints

The backend API runs on `http://localhost:5000` and provides:

- `GET /api/health` - Health check
- `GET /api/data/overview` - Overview statistics
- `GET /api/data/prices` - Price time series data
- `GET /api/data/volatility` - Volatility data
- `GET /api/data/correlation` - Correlation matrix
- `GET /api/data/var` - Value at Risk data
- `GET /api/data/volume` - Volume statistics

## Dashboard Components

1. **Overview Cards** - Quick stats for each stock symbol
2. **Price Trends Chart** - Multi-line chart showing price movements
3. **Volatility Chart** - Bar chart comparing volatility across stocks
4. **Volume Chart** - Trading volume comparison
5. **VaR Chart** - Risk analysis visualization
6. **Correlation Heatmap** - Interactive correlation matrix

## Troubleshooting

### Backend won't start
- Make sure port 5000 is not in use
- Check that `stock_stream/` directory contains batch files
- Verify Python dependencies are installed

### Frontend won't connect
- Ensure backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify API health endpoint: `http://localhost:5000/api/health`

### No data displayed
- Run the Spark lab first to generate data: `python lab7.py` or `.\run-docker.ps1`
- Check that batch files exist in `stock_stream/` directory

## Development

### Backend Development
- Backend uses Flask with CORS enabled
- API endpoints are in `dashboard_backend.py`
- Data is loaded from `stock_stream/` directory

### Frontend Development
- Frontend uses React with Recharts for visualizations
- Components are in `dashboard_frontend/src/components/`
- Styling uses CSS modules

## Technologies Used

- **Backend**: Flask, Pandas, NumPy
- **Frontend**: React, Recharts, Axios
- **Visualization**: Recharts (built on D3.js)

## License

This project is part of the Spark Streaming Lab coursework.

