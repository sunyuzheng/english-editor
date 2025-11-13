#!/bin/bash

# Activate virtual environment
cd "$(dirname "$0")"
source venv/bin/activate

# Check if AI_BUILDER_TOKEN is set
if [ -z "$AI_BUILDER_TOKEN" ]; then
    echo "Error: AI_BUILDER_TOKEN environment variable is not set."
    echo "Please set it before running:"
    echo "  export AI_BUILDER_TOKEN=your_token_here"
    echo "Or create a .env file with: AI_BUILDER_TOKEN=your_token_here"
    exit 1
fi

# Run the application
python app.py

