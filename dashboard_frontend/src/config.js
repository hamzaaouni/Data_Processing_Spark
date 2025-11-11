// API Configuration
// Automatically detects if running on same machine or network

const getApiBaseUrl = () => {
  // Check if we have an environment variable set
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // If accessing from another device on network, use the hostname
  // This will work when accessing via http://192.168.6.92:3000
  const hostname = window.location.hostname;
  
  // If it's localhost or 127.0.0.1, use localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:5000/api';
  }
  
  // Otherwise, use the same hostname with port 5000
  // This works when accessing via network IP like http://192.168.6.92:3000
  return `http://${hostname}:5000/api`;
};

export const API_BASE_URL = getApiBaseUrl();

// For debugging
console.log('API Base URL:', API_BASE_URL);
console.log('Current hostname:', window.location.hostname);

