#!/bin/bash

# SugarGlitch RealOps - Project Structure Organizer
# Organizes the project for better production clarity

echo "🔥 SugarGlitch RealOps - Project Organization 🔥"
echo "================================================"

# Create new folder structure
mkdir -p core config docs sessions scripts devcontainer data

echo "📁 Created project structure folders..."

# Move core application files
echo "🎯 Moving core application files..."
if [ -f "main.py" ]; then cp main.py core/; fi
if [ -f "runner.py" ]; then cp runner.py core/; fi
if [ -f "verify_env.py" ]; then cp verify_env.py core/; fi
if [ -f "verify_production.py" ]; then cp verify_production.py core/; fi
if [ -f "environment_test.py" ]; then cp environment_test.py core/; fi

# Move configuration files
echo "⚙️  Moving configuration files..."
if [ -f ".env" ]; then cp .env config/; fi
if [ -f ".env.example" ]; then cp .env.example config/; fi
if [ -f ".env.template" ]; then cp .env.template config/; fi
if [ -f "config.json" ]; then cp config.json config/; fi

# Move documentation
echo "📚 Moving documentation..."
find . -maxdepth 1 -name "*.md" -exec cp {} docs/ \; 2>/dev/null || true
find . -maxdepth 1 -name "*.pdf" -exec cp {} docs/ \; 2>/dev/null || true

# Move session data
echo "🔐 Moving session data..."
if [ -d "hijacked_sessions" ]; then cp -r hijacked_sessions sessions/; fi
if [ -f "session-alx.trading" ]; then cp session-alx.trading sessions/; fi
find . -maxdepth 1 -name "*session*" -type f -exec cp {} sessions/ \; 2>/dev/null || true

# Move Python scripts (excluding core)
echo "🐍 Moving Python scripts..."
find . -maxdepth 1 -name "*.py" \
  ! -name "main.py" \
  ! -name "runner.py" \
  ! -name "verify_env.py" \
  ! -name "verify_production.py" \
  ! -name "environment_test.py" \
  -exec cp {} scripts/ \; 2>/dev/null || true

# Move data files
echo "📊 Moving data files..."
find . -maxdepth 1 \( \
  -name "*.json" -o \
  -name "*.txt" -o \
  -name "*.html" -o \
  -name "*.csv" -o \
  -name "*.png" -o \
  -name "*.log" -o \
  -name "*.xml" \
\) -exec cp {} data/ \; 2>/dev/null || true

# Move devcontainer and setup files
echo "🛠️  Moving devcontainer files..."
if [ -d ".devcontainer" ]; then cp -r .devcontainer devcontainer/; fi
if [ -d ".vscode" ]; then cp -r .vscode devcontainer/; fi
find . -maxdepth 1 -name "*.sh" -exec cp {} devcontainer/ \; 2>/dev/null || true

# Set permissions
echo "🔒 Setting permissions..."
chmod +x core/*.py 2>/dev/null || true
chmod +x scripts/*.py 2>/dev/null || true
chmod +x devcontainer/*.sh 2>/dev/null || true

# Create README for each folder
echo "📝 Creating folder documentation..."

cat > core/README.md << 'EOF'
# Core Application Files

This folder contains the main application entry points and core functionality:

- `main.py` - Main application with module system
- `runner.py` - Interactive application runner
- `verify_env.py` - Environment verification
- `verify_production.py` - Production readiness check
- `environment_test.py` - Comprehensive environment testing

## Usage
```bash
cd core
python main.py --list
python runner.py --interactive
```
EOF

cat > config/README.md << 'EOF'
# Configuration Files

This folder contains all configuration files:

- `.env` - Environment variables (production)
- `.env.example` - Example environment configuration
- `.env.template` - Environment template
- `config.json` - Application configuration (if exists)

## Usage
Copy `.env.example` to `.env` and configure your settings.
EOF

cat > docs/README.md << 'EOF'
# Documentation

This folder contains all project documentation including:

- README files
- Markdown documentation
- PDF manuals
- Project guides

## Key Documents
- Project setup guides
- API documentation
- Security procedures
- Troubleshooting guides
EOF

cat > sessions/README.md << 'EOF'
# Session Data

This folder contains session-related files:

- Session tokens
- Hijacked session data
- Session validation outputs
- JSON session data

⚠️ **WARNING**: This folder may contain sensitive data. Handle with care.
EOF

cat > scripts/README.md << 'EOF'
# Utility Scripts

This folder contains all utility scripts and tools:

- Instagram extractors
- Penetration testing tools
- Data analysis scripts
- Automation utilities

## Categories
- Social media tools
- Network reconnaissance
- Data extraction
- Security testing
EOF

cat > devcontainer/README.md << 'EOF'
# Development Container

This folder contains development environment setup:

- `.devcontainer/` - VS Code dev container configuration
- `.vscode/` - VS Code workspace settings
- Shell scripts for environment setup

## Usage
This folder is used by VS Code for containerized development.
EOF

echo ""
echo "✅ Project organization complete!"
echo ""
echo "📊 New Structure:"
echo "├── core/          - Main application files"
echo "├── config/        - Configuration files"
echo "├── docs/          - Documentation"
echo "├── sessions/      - Session data"
echo "├── scripts/       - Utility scripts"
echo "├── devcontainer/  - Development setup"
echo "├── data/          - Data files (JSON, TXT, etc.)"
echo "└── requirements.txt"
echo ""
echo "🚀 Ready for production deployment!"
