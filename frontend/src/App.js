import React, { useState } from 'react';
import './App.css';
import CarPriceForm from './components/CarPriceForm';
import PredictionResult from './components/PredictionResult';
import axios from 'axios';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${API_URL}/predict`, formData);
      setPrediction(response.data.predicted_price);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get prediction. Please check your input and try again.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚗 Car Price Predictor</h1>
        <p>Get instant price predictions powered by machine learning</p>
      </header>
      
      <main className="App-main">
        <CarPriceForm 
          onSubmit={handlePredict} 
          loading={loading}
          onReset={handleReset}
        />
        
        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Predicting price...</p>
          </div>
        )}
        
        {error && (
          <div className="error-message">
            <span>⚠️</span>
            <p>{error}</p>
          </div>
        )}
        
        {prediction && (
          <PredictionResult price={prediction} onReset={handleReset} />
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by XGBoost Machine Learning Model</p>
      </footer>
    </div>
  );
}

export default App;
