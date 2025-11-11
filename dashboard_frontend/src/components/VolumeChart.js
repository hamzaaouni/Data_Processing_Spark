import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const VolumeChart = ({ data }) => {
  const chartData = Object.keys(data).map(symbol => ({
    symbol,
    totalVolume: data[symbol].total_volume,
    avgVolume: Math.round(data[symbol].avg_volume)
  })).sort((a, b) => b.totalVolume - a.totalVolume);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="symbol" stroke="#666" />
        <YAxis 
          stroke="#666"
          label={{ value: 'Volume', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '1px solid #ccc' }}
          formatter={(value) => value.toLocaleString()}
        />
        <Legend />
        <Bar dataKey="totalVolume" fill="#4facfe" name="Total Volume" radius={[8, 8, 0, 0]} />
        <Bar dataKey="avgVolume" fill="#43e97b" name="Avg Volume" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default VolumeChart;

