#!/bin/bash

# Define variables
VENV_DIR="venv"
APP_FILE="app"
HOST="0.0.0.0"
PORT="5000"
WORKERS=2

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating virtual environment..."
activate () {
    . $PWD/$VENV_DIR/bin/activate
}
activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Set the environment variable for GPU usage
export USE_GPU=False

# Run the app using Gunicorn
echo "Starting the app with Gunicorn..."
gunicorn --workers=$WORKERS --bind $HOST:$PORT $APP_FILE:app
