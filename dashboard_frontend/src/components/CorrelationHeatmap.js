import React from 'react';
import './CorrelationHeatmap.css';

const CorrelationHeatmap = ({ data }) => {
  const { symbols, matrix } = data;

  const getColor = (value) => {
    // Normalize value from -1 to 1 to 0 to 1
    const normalized = (value + 1) / 2;
    // Red to white to green gradient
    if (normalized < 0.5) {
      // Red to white
      const intensity = normalized * 2;
      return `rgb(255, ${Math.round(255 * intensity)}, ${Math.round(255 * intensity)})`;
    } else {
      // White to green
      const intensity = (normalized - 0.5) * 2;
      return `rgb(${Math.round(255 * (1 - intensity))}, 255, ${Math.round(255 * (1 - intensity))})`;
    }
  };

  return (
    <div className="correlation-heatmap">
      <table>
        <thead>
          <tr>
            <th></th>
            {symbols.map(symbol => (
              <th key={symbol}>{symbol}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {symbols.map((symbol, i) => (
            <tr key={symbol}>
              <td className="row-label">{symbol}</td>
              {matrix[i].map((value, j) => (
                <td
                  key={j}
                  className="cell"
                  style={{ backgroundColor: getColor(value) }}
                  title={`${symbol} vs ${symbols[j]}: ${value.toFixed(3)}`}
                >
                  {value.toFixed(2)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CorrelationHeatmap;

