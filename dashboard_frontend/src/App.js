import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check API health
    fetch(`${API_BASE_URL}/health`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          setLoading(false);
        } else {
          setError('API is not responding correctly');
          setLoading(false);
        }
      })
      .catch(err => {
        setError('Cannot connect to API. Make sure the backend is running on http://localhost:5000');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <p className="error-hint">
          Please run: <code>python dashboard_backend.py</code>
        </p>
      </div>
    );
  }

  return (
    <div className="App">
      <Dashboard />
    </div>
  );
}

export default App;

