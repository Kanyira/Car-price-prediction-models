#!/bin/bash

# Run the FastAPI server
echo "Starting Car Price Prediction API..."
echo "API will be available at: http://localhost:8000"
echo "API docs will be available at: http://localhost:8000/docs"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
