#!/bin/bash

# Navigate to script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "Please enter your AI_BUILDER_TOKEN:"
    read -s TOKEN
    echo "AI_BUILDER_TOKEN=$TOKEN" > .env
    echo ".env file created!"
fi

# Load environment variables
export $(cat .env | xargs)

# Run the application
echo "Starting English Editor server..."
echo "Open http://localhost:8000 in your browser"
python app.py

