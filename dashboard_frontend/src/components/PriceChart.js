import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PriceChart = ({ data }) => {
  // Transform data for Recharts
  const chartData = [];
  const symbols = Object.keys(data);
  
  if (symbols.length === 0) return <div>No data available</div>;
  
  // Get the first symbol to determine length
  const firstSymbol = symbols[0];
  const timestamps = data[firstSymbol].timestamps;
  
  // Create data points
  timestamps.forEach((timestamp, index) => {
    const point = { timestamp: new Date(timestamp).toLocaleTimeString() };
    symbols.forEach(symbol => {
      if (data[symbol] && data[symbol].prices[index] !== undefined) {
        point[symbol] = parseFloat(data[symbol].prices[index].toFixed(2));
      }
    });
    chartData.push(point);
  });

  const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis 
          dataKey="timestamp" 
          stroke="#666"
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis 
          stroke="#666"
          label={{ value: 'Price ($)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '1px solid #ccc' }}
          formatter={(value) => `$${value.toFixed(2)}`}
        />
        <Legend />
        {symbols.map((symbol, index) => (
          <Line
            key={symbol}
            type="monotone"
            dataKey={symbol}
            stroke={colors[index % colors.length]}
            strokeWidth={2}
            dot={{ r: 3 }}
            activeDot={{ r: 6 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;

