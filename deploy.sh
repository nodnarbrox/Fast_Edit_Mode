#!/bin/bash

# Deployment script for Fast Edit Mode Web Interface

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (ensure .env is properly configured)
export $(cat .env | xargs)

# Run database migrations (if applicable)
# flask db upgrade

# Start the application
flask run --host=0.0.0.0 --port=5000
