#!/bin/bash
# Quick Penetration Testing Environment Status
# สถานะสิ่งแวดล้อมการเจาะระบบแบบเร็ว

echo "🎯 SUGARGLITCH REALOPS - PENETRATION TESTING STATUS"
echo "=================================================="
echo "Date: $(date)"
echo ""

# Database Status
echo "📊 DATABASE STATUS:"
if [ -f "alx_trading_database.sqlite" ]; then
    echo "✅ Database: alx_trading_database.sqlite exists"
    python3 -c "
import sqlite3
conn = sqlite3.connect('alx_trading_database.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM deep_profiles')
profiles = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM real_contacts')
contacts = cursor.fetchone()[0]
print(f'✅ Deep Profiles: {profiles} records')
print(f'✅ Real Contacts: {contacts} records')
conn.close()
"
else
    echo "❌ Database not found"
fi

echo ""

# Tools Status
echo "🛠️  ESSENTIAL TOOLS:"
tools=("curl" "wget" "whois" "python3" "git")
for tool in "${tools[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "✅ $tool: Available"
    else
        echo "❌ $tool: Missing"
    fi
done

echo ""

# Scripts Status
echo "🐍 CUSTOM SCRIPTS:"
scripts=("recon.py" "realops.py" "view_deep_profile.py" "quick_insert_profile.py")
for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ $script: Ready"
    else
        echo "❌ $script: Missing"
    fi
done

echo ""

# Environment Setup
echo "🔧 ENVIRONMENT:"
if [ -f "hacker_aliases.sh" ]; then
    echo "✅ Hacker aliases available"
fi
if [ -f "setup_hacker_env.sh" ]; then
    echo "✅ Environment setup script ready"
fi
if [ -f "targets.txt" ]; then
    echo "✅ Target list configured"
fi

echo ""
echo "🚀 QUICK START COMMANDS:"
echo "1. Load aliases: source hacker_aliases.sh"
echo "2. Start recon: python3 recon.py"
echo "3. View profiles: python3 view_deep_profile.py"
echo "4. Operations menu: python3 realops.py"
echo ""
echo "⚡ Environment is configured for penetration testing operations!"
echo "Ready to proceed with reconnaissance and data extraction."
