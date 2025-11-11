import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const VarChart = ({ data }) => {
  const chartData = data.map(item => ({
    symbol: item.symbol,
    var95: parseFloat(item.var_95.toFixed(2)),
    varPct: parseFloat(item.var_pct.toFixed(2))
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="symbol" stroke="#666" />
        <YAxis 
          stroke="#666"
          label={{ value: 'VaR ($)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '1px solid #ccc' }}
          formatter={(value) => `$${value.toFixed(2)}`}
        />
        <Legend />
        <Bar dataKey="var95" fill="#fa709a" name="VaR (95%)" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default VarChart;

