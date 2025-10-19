# Car Price Predictor - Frontend

React-based frontend for the Car Price Prediction API.

## 🚀 Quick Start

### Development Mode

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

### Production Build

```bash
# Create production build
npm run build

# The build folder will contain optimized production files
```

## 🔧 Configuration

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

For production, update the API URL to your deployed backend.

## 📦 Docker

Build and run with Docker:

```bash
docker build -t car-price-frontend .
docker run -p 3000:80 car-price-frontend
```

## 🎨 Features

- Modern, responsive UI
- Real-time form validation
- Dropdown selectors for consistent data entry
- Loading states and error handling
- Mobile-friendly design

## 🛠️ Built With

- React 18
- Axios for API calls
- CSS3 with modern animations
