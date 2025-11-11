import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';
import PriceChart from './PriceChart';
import VolatilityChart from './VolatilityChart';
import VolumeChart from './VolumeChart';
import CorrelationHeatmap from './CorrelationHeatmap';
import VarChart from './VarChart';
import OverviewCards from './OverviewCards';

const API_BASE_URL = 'http://localhost:5000/api';

const Dashboard = () => {
  const [overview, setOverview] = useState(null);
  const [prices, setPrices] = useState(null);
  const [volatility, setVolatility] = useState(null);
  const [correlation, setCorrelation] = useState(null);
  const [varData, setVarData] = useState(null);
  const [volume, setVolume] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, pricesRes, volatilityRes, correlationRes, varRes, volumeRes] = 
          await Promise.all([
            axios.get(`${API_BASE_URL}/data/overview`),
            axios.get(`${API_BASE_URL}/data/prices`),
            axios.get(`${API_BASE_URL}/data/volatility`),
            axios.get(`${API_BASE_URL}/data/correlation`),
            axios.get(`${API_BASE_URL}/data/var`),
            axios.get(`${API_BASE_URL}/data/volume`)
          ]);

        setOverview(overviewRes.data);
        setPrices(pricesRes.data);
        setVolatility(volatilityRes.data);
        setCorrelation(correlationRes.data);
        setVarData(varRes.data);
        setVolume(volumeRes.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>📊 Spark Streaming Lab Dashboard</h1>
        <p className="subtitle">Real-time Stock Market Analysis</p>
        {overview && (
          <div className="header-info">
            <span>Records: {overview.total_records}</span>
            <span>•</span>
            <span>Symbols: {overview.symbols.join(', ')}</span>
          </div>
        )}
      </header>

      <div className="dashboard-content">
        {overview && <OverviewCards overview={overview} />}
        
        <div className="chart-grid">
          <div className="chart-card full-width">
            <h2>Price Trends</h2>
            {prices && <PriceChart data={prices} />}
          </div>

          <div className="chart-card">
            <h2>Volatility Analysis</h2>
            {volatility && <VolatilityChart data={volatility} />}
          </div>

          <div className="chart-card">
            <h2>Trading Volume</h2>
            {volume && <VolumeChart data={volume} />}
          </div>

          <div className="chart-card">
            <h2>Value at Risk (95%)</h2>
            {varData && <VarChart data={varData} />}
          </div>

          <div className="chart-card full-width">
            <h2>Price Correlation Matrix</h2>
            {correlation && <CorrelationHeatmap data={correlation} />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

