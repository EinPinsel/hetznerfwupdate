#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file with your Hetzner credentials"
fi

echo "Setup complete! Don't forget to:"
echo "1. Edit the .env file with your credentials"
echo "2. Activate the virtual environment with 'source venv/bin/activate' when working on the project" 