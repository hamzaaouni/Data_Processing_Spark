import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const VolatilityChart = ({ data }) => {
  const chartData = Object.keys(data).map(symbol => ({
    symbol,
    volatility: parseFloat(data[symbol].avg_volatility.toFixed(2))
  })).sort((a, b) => b.volatility - a.volatility);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="symbol" stroke="#666" />
        <YAxis 
          stroke="#666"
          label={{ value: 'Volatility (%)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '1px solid #ccc' }}
          formatter={(value) => `${value}%`}
        />
        <Legend />
        <Bar dataKey="volatility" fill="#667eea" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default VolatilityChart;

