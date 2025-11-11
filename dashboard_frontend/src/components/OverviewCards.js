import React from 'react';
import './OverviewCards.css';

const OverviewCards = ({ overview }) => {
  const symbols = overview.symbols || [];
  const summary = overview.summary || {};

  const getPriceChangeColor = (change) => {
    if (change > 0) return 'positive';
    if (change < 0) return 'negative';
    return 'neutral';
  };

  const formatPrice = (price) => {
    return `$${price.toFixed(2)}`;
  };

  return (
    <div className="overview-cards">
      {symbols.map(symbol => {
        const data = summary[symbol];
        if (!data) return null;

        return (
          <div key={symbol} className="overview-card">
            <div className="card-header">
              <h3>{symbol}</h3>
              <span className={`price-change ${getPriceChangeColor(data.price_change_pct)}`}>
                {data.price_change_pct >= 0 ? '↑' : '↓'} {Math.abs(data.price_change_pct).toFixed(2)}%
              </span>
            </div>
            <div className="card-body">
              <div className="metric">
                <span className="metric-label">Current Price</span>
                <span className="metric-value">{formatPrice(data.current_price)}</span>
              </div>
              <div className="metric-row">
                <div className="metric">
                  <span className="metric-label">Avg Price</span>
                  <span className="metric-value-small">{formatPrice(data.avg_price)}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Volatility</span>
                  <span className="metric-value-small">{data.avg_volatility.toFixed(2)}%</span>
                </div>
              </div>
              <div className="metric-row">
                <div className="metric">
                  <span className="metric-label">Min</span>
                  <span className="metric-value-small">{formatPrice(data.min_price)}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Max</span>
                  <span className="metric-value-small">{formatPrice(data.max_price)}</span>
                </div>
              </div>
              <div className="metric">
                <span className="metric-label">Total Volume</span>
                <span className="metric-value-small">{data.total_volume.toLocaleString()}</span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default OverviewCards;

