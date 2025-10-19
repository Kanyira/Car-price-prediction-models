import React, { useState } from 'react';
import './CarPriceForm.css';

const CarPriceForm = ({ onSubmit, loading, onReset }) => {
  const [formData, setFormData] = useState({
    Levy: '1399',
    Manufacturer: 'LEXUS',
    Model: 'RX 450',
    Prod_year: 2010,
    Category: 'Jeep',
    Leather_interior: 'Yes',
    Fuel_type: 'Hybrid',
    Engine_volume: 3.5,
    Mileage: 186005,
    Cylinders: 6.0,
    Gear_box_type: 'Automatic',
    Drive_wheels: '4x4',
    Wheel: 'Left wheel',
    Color: 'Silver',
    Airbags: 12,
    Age: 15,
    Mileage_per_year: 12400
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: ['Prod_year', 'Age', 'Airbags'].includes(name) 
        ? parseInt(value) || 0
        : ['Engine_volume', 'Mileage', 'Cylinders', 'Mileage_per_year'].includes(name)
        ? parseFloat(value) || 0
        : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleReset = () => {
    setFormData({
      Levy: '',
      Manufacturer: '',
      Model: '',
      Prod_year: new Date().getFullYear(),
      Category: '',
      Leather_interior: 'No',
      Fuel_type: '',
      Engine_volume: 0,
      Mileage: 0,
      Cylinders: 4.0,
      Gear_box_type: '',
      Drive_wheels: '',
      Wheel: 'Left wheel',
      Color: '',
      Airbags: 0,
      Age: 0,
      Mileage_per_year: 0
    });
    onReset();
  };

  const manufacturers = ['LEXUS', 'TOYOTA', 'MERCEDES-BENZ', 'BMW', 'HYUNDAI', 'KIA', 'HONDA', 'FORD', 'CHEVROLET', 'NISSAN', 'MAZDA', 'AUDI', 'VOLKSWAGEN'];
  const categories = ['Sedan', 'Jeep', 'Hatchback', 'SUV', 'Coupe', 'Minivan', 'Pickup', 'Cabriolet', 'Limousine'];
  const fuelTypes = ['Petrol', 'Diesel', 'Hybrid', 'Electric', 'CNG', 'LPG', 'Hydrogen'];
  const gearBoxTypes = ['Automatic', 'Manual', 'Tiptronic', 'Variator'];
  const driveWheels = ['Front', 'Rear', '4x4'];
  const wheelTypes = ['Left wheel', 'Right-hand drive'];
  const colors = ['Black', 'White', 'Silver', 'Grey', 'Blue', 'Red', 'Green', 'Yellow', 'Orange', 'Brown', 'Golden', 'Beige'];

  return (
    <form onSubmit={handleSubmit} className="car-form">
      <h2>Enter Car Details</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>Levy (Tax) *</label>
          <input
            type="text"
            name="Levy"
            value={formData.Levy}
            onChange={handleChange}
            placeholder="e.g., 1399 or -"
            required
          />
          <small>Enter amount or "-" for no levy</small>
        </div>

        <div className="form-group">
          <label>Manufacturer *</label>
          <select
            name="Manufacturer"
            value={formData.Manufacturer}
            onChange={handleChange}
            required
          >
            <option value="">Select manufacturer</option>
            {manufacturers.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Model *</label>
          <input
            type="text"
            name="Model"
            value={formData.Model}
            onChange={handleChange}
            placeholder="e.g., RX 450"
            required
          />
        </div>

        <div className="form-group">
          <label>Production Year *</label>
          <input
            type="number"
            name="Prod_year"
            value={formData.Prod_year}
            onChange={handleChange}
            min="1980"
            max={new Date().getFullYear()}
            required
          />
        </div>

        <div className="form-group">
          <label>Category *</label>
          <select
            name="Category"
            value={formData.Category}
            onChange={handleChange}
            required
          >
            <option value="">Select category</option>
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Leather Interior *</label>
          <select
            name="Leather_interior"
            value={formData.Leather_interior}
            onChange={handleChange}
            required
          >
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        <div className="form-group">
          <label>Fuel Type *</label>
          <select
            name="Fuel_type"
            value={formData.Fuel_type}
            onChange={handleChange}
            required
          >
            <option value="">Select fuel type</option>
            {fuelTypes.map(f => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Engine Volume (L) *</label>
          <input
            type="number"
            name="Engine_volume"
            value={formData.Engine_volume}
            onChange={handleChange}
            step="0.1"
            min="0.5"
            max="8.0"
            required
          />
        </div>

        <div className="form-group">
          <label>Mileage (km) *</label>
          <input
            type="number"
            name="Mileage"
            value={formData.Mileage}
            onChange={handleChange}
            min="0"
            required
          />
        </div>

        <div className="form-group">
          <label>Cylinders *</label>
          <input
            type="number"
            name="Cylinders"
            value={formData.Cylinders}
            onChange={handleChange}
            step="1"
            min="2"
            max="16"
            required
          />
        </div>

        <div className="form-group">
          <label>Gear Box Type *</label>
          <select
            name="Gear_box_type"
            value={formData.Gear_box_type}
            onChange={handleChange}
            required
          >
            <option value="">Select gear box</option>
            {gearBoxTypes.map(g => <option key={g} value={g}>{g}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Drive Wheels *</label>
          <select
            name="Drive_wheels"
            value={formData.Drive_wheels}
            onChange={handleChange}
            required
          >
            <option value="">Select drive wheels</option>
            {driveWheels.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Wheel Position *</label>
          <select
            name="Wheel"
            value={formData.Wheel}
            onChange={handleChange}
            required
          >
            {wheelTypes.map(w => <option key={w} value={w}>{w}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Color *</label>
          <select
            name="Color"
            value={formData.Color}
            onChange={handleChange}
            required
          >
            <option value="">Select color</option>
            {colors.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="form-group">
          <label>Number of Airbags *</label>
          <input
            type="number"
            name="Airbags"
            value={formData.Airbags}
            onChange={handleChange}
            min="0"
            max="16"
            required
          />
        </div>

        <div className="form-group">
          <label>Age (years) *</label>
          <input
            type="number"
            name="Age"
            value={formData.Age}
            onChange={handleChange}
            min="0"
            max="50"
            required
          />
        </div>

        <div className="form-group">
          <label>Mileage per Year (optional)</label>
          <input
            type="number"
            name="Mileage_per_year"
            value={formData.Mileage_per_year}
            onChange={handleChange}
            min="0"
          />
          <small>Leave 0 for auto-calculation</small>
        </div>
      </div>

      <div className="form-actions">
        <button 
          type="button" 
          onClick={handleReset} 
          className="btn btn-secondary"
          disabled={loading}
        >
          Reset
        </button>
        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? 'Predicting...' : 'Predict Price'}
        </button>
      </div>
    </form>
  );
};

export default CarPriceForm;
