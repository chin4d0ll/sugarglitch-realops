#!/bin/bash

# SugarGlitch RealOps Setup Script
# Automated setup for development environment

set -e

echo "🚀 Setting up SugarGlitch RealOps..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p {config/sessions,data/{uploads,sessions,extractions,operations,intelligence,attacks,telegram},logs,backups,temp}

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found, skipping Python dependencies"
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    npm install
else
    echo "⚠️ package.json not found, skipping Node.js dependencies"
fi

# Set up environment variables
echo "🔧 Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from example"
    echo "📝 Please edit .env file with your actual configuration"
else
    echo "✅ .env file already exists"
fi

# Set permissions
echo "🔒 Setting permissions..."
chmod +x *.sh 2>/dev/null || true
chmod 755 scripts/* 2>/dev/null || true

# Initialize database (if needed)
echo "🗄️ Checking database..."
if [ -f "databases/simple_db.py" ]; then
    python3 databases/simple_db.py
    echo "✅ Database initialized"
fi

# Run memory optimization
echo "🔧 Optimizing memory..."
if [ -f "optimize_memory.sh" ]; then
    ./optimize_memory.sh
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Quick Start:"
echo "1. Edit .env file with your configuration"
echo "2. Run: python3 simple_main.py (for lightweight version)"
echo "3. Run: python3 main.py (for full version)"
echo ""
echo "For more information, see:"
echo "- README.md"
echo "- QUICKSTART.md"
echo "- SETUP_TH.md"
