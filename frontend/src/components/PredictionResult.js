import React from 'react';
import './PredictionResult.css';

const PredictionResult = ({ price, onReset }) => {
  return (
    <div className="prediction-result">
      <div className="result-card">
        <div className="result-icon">💰</div>
        <h2>Predicted Price</h2>
        <div className="price-display">
          <span className="currency">$</span>
          <span className="price">{price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
        </div>
        <p className="result-subtitle">Estimated market value based on your car's features</p>
        <button onClick={onReset} className="btn btn-new-prediction">
          Make Another Prediction
        </button>
      </div>
    </div>
  );
};

export default PredictionResult;
