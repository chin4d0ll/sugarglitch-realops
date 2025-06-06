#!/bin/bash

# SugarGlitch RealOps - Main DM Extractor Script
# This script runs the main dm_extractor.py from the src directory

echo "🚀 Starting SugarGlitch RealOps DM Extractor..."

# Change to project root
cd "$(dirname "$0")"

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install requirements if needed
if [ -f "src/requirements.txt" ]; then
    echo "📋 Installing requirements..."
    pip install -r src/requirements.txt
fi

# Run the main extractor
echo "🎯 Running DM Extractor..."
python3 src/dm_extractor.py "$@"

echo "✅ DM Extraction completed!"