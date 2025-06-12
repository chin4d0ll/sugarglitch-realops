#!/bin/bash

# Docker build and run script for sugarglitch-realops

echo "🐳 Building Docker image..."
docker build -t sugarglitch-realops:latest .

echo "✅ Build completed!"
echo ""
echo "🚀 To run the container:"
echo "docker run --rm -it sugarglitch-realops:latest"
echo ""
echo "🔧 To run with custom command:"
echo "docker run --rm -it sugarglitch-realops:latest tools/your_script.py"
echo ""
echo "📁 To run with volume mount for data persistence:"
echo "docker run --rm -it -v \$(pwd)/data:/app/data sugarglitch-realops:latest"
