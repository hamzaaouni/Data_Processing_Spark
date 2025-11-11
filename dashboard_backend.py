# ============================================================================
# FLASK BACKEND API FOR SPARK STREAMING LAB DASHBOARD
# ============================================================================
# Run: python dashboard_backend.py
# API will be available at http://localhost:5000

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()
STOCK_STREAM_DIR = SCRIPT_DIR / "stock_stream"

def load_stock_data():
    """Load and process all stock data from batch files"""
    all_data = []
    
    batch_files = sorted(STOCK_STREAM_DIR.glob("batch_*.json"))
    
    for batch_file in batch_files:
        try:
            with open(batch_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        if data.get('symbol') != 'INIT':
                            all_data.append(data)
        except Exception as e:
            print(f"Warning: Could not read {batch_file}: {e}")
    
    if not all_data:
        return None
    
    df = pd.DataFrame(all_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Calculate metrics
    df['price_change'] = df.groupby('symbol')['price'].diff()
    df['price_change_pct'] = df.groupby('symbol')['price'].pct_change() * 100
    df['volatility'] = df.groupby('symbol')['price_change_pct'].rolling(window=5, min_periods=1).std().reset_index(0, drop=True)
    
    return df

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Dashboard API is running"})

@app.route('/api/data/overview', methods=['GET'])
def get_overview():
    """Get overview statistics"""
    df = load_stock_data()
    if df is None:
        return jsonify({"error": "No data available"}), 404
    
    overview = {
        "total_records": len(df),
        "date_range": {
            "start": df['timestamp'].min().isoformat(),
            "end": df['timestamp'].max().isoformat()
        },
        "symbols": df['symbol'].unique().tolist(),
        "summary": {}
    }
    
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        overview["summary"][symbol] = {
            "avg_price": float(symbol_data['price'].mean()),
            "min_price": float(symbol_data['price'].min()),
            "max_price": float(symbol_data['price'].max()),
            "current_price": float(symbol_data['price'].iloc[-1]),
            "total_volume": int(symbol_data['volume'].sum()),
            "avg_volatility": float(symbol_data['volatility'].mean()),
            "price_change_pct": float(symbol_data['price_change_pct'].iloc[-1]) if not pd.isna(symbol_data['price_change_pct'].iloc[-1]) else 0.0
        }
    
    return jsonify(overview)

@app.route('/api/data/prices', methods=['GET'])
def get_prices():
    """Get price time series data"""
    df = load_stock_data()
    if df is None:
        return jsonify({"error": "No data available"}), 404
    
    result = {}
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        result[symbol] = {
            "timestamps": symbol_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            "prices": symbol_data['price'].tolist(),
            "volumes": symbol_data['volume'].tolist()
        }
    
    return jsonify(result)

@app.route('/api/data/volatility', methods=['GET'])
def get_volatility():
    """Get volatility data"""
    df = load_stock_data()
    if df is None:
        return jsonify({"error": "No data available"}), 404
    
    result = {}
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        result[symbol] = {
            "timestamps": symbol_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            "volatility": symbol_data['volatility'].fillna(0).tolist(),
            "avg_volatility": float(symbol_data['volatility'].mean())
        }
    
    return jsonify(result)

@app.route('/api/data/correlation', methods=['GET'])
def get_correlation():
    """Get correlation matrix"""
    df = load_stock_data()
    if df is None:
        return jsonify({"error": "No data available"}), 404
    
    price_pivot = df.pivot_table(index='timestamp', columns='symbol', values='price', aggfunc='mean')
    correlation_matrix = price_pivot.corr()
    
    return jsonify({
        "symbols": correlation_matrix.columns.tolist(),
        "matrix": correlation_matrix.values.tolist()
    })

@app.route('/api/data/var', methods=['GET'])
def get_var():
    """Get Value at Risk data"""
    df = load_stock_data()
    if df is None:
        return jsonify({"error": "No data available"}), 404
    
    var_data = []
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        avg_price = symbol_data['price'].mean()
        volatility = symbol_data['volatility'].mean()
        var_95 = 1.645 * volatility * avg_price / 100
        
        var_data.append({
            "symbol": symbol,
            "avg_price": float(avg_price),
            "volatility": float(volatility),
            "var_95": float(var_95),
            "var_pct": float(1.645 * volatility)
        })
    
    # Sort by VaR descending
    var_data.sort(key=lambda x: x['var_95'], reverse=True)
    
    return jsonify(var_data)

@app.route('/api/data/volume', methods=['GET'])
def get_volume():
    """Get volume statistics"""
    df = load_stock_data()
    if df is None:
        return jsonify({"error": "No data available"}), 404
    
    result = {}
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        result[symbol] = {
            "total_volume": int(symbol_data['volume'].sum()),
            "avg_volume": float(symbol_data['volume'].mean()),
            "max_volume": int(symbol_data['volume'].max()),
            "min_volume": int(symbol_data['volume'].min())
        }
    
    return jsonify(result)

if __name__ == '__main__':
    print("="*70)
    print("SPARK STREAMING LAB - DASHBOARD API")
    print("="*70)
    print("Starting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("API endpoints:")
    print("  - GET /api/health")
    print("  - GET /api/data/overview")
    print("  - GET /api/data/prices")
    print("  - GET /api/data/volatility")
    print("  - GET /api/data/correlation")
    print("  - GET /api/data/var")
    print("  - GET /api/data/volume")
    print("="*70)
    app.run(debug=True, host='0.0.0.0', port=5000)

