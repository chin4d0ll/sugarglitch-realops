#!/bin/bash
# REALOPS - Essential Setup
# Focus: Real work, real tools, no fluff

echo "=== REALOPS SETUP ==="

# Essential aliases only
cat >> ~/.bashrc << 'EOF'

# === REALOPS ALIASES ===
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias recon='python3 /workspaces/sugarglitch-realops/realops.py'
alias db='sqlite3 /workspaces/sugarglitch-realops/alx_trading_database.sqlite'
alias scan='nmap -sS -O'
alias quick='ping -c 3'
alias grep='grep --color=auto'
alias ports='netstat -tulpn'

# Custom prompt
PS1='\[\033[01;32m\]\u@REALOPS\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
EOF

# Create essential directories
mkdir -p /workspaces/sugarglitch-realops/{data,results,logs}

# Make realops executable
chmod +x /workspaces/sugarglitch-realops/realops.py

# Install essential Python packages
pip3 install --user requests beautifulsoup4 sqlite3 2>/dev/null

echo "=== REALOPS READY ==="
echo "Commands:"
echo "  recon    - Main operations interface"
echo "  db       - Direct database access"
echo "  scan     - Network scanning"
echo "  quick    - Quick ping test"
echo ""
echo "Run: source ~/.bashrc"
echo "Then: recon"
