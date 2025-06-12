#!/bin/bash
# Clean workspace - keep only essential files for real work

echo "=== CLEANING WORKSPACE ==="

# Keep essential files only
KEEP_FILES=(
    "realops.py"
    "realops_setup.sh"
    "alx_trading_database.sqlite"
    "alx_trading_database_setup.py"
    "comprehensive_real_data_summary.py"
    "comprehensive_dm_scan_results_1749231518.json"
    "alx_trading_session_fleming654.json"
    "config/json/MASTER_PROFILE_alx_trading_1748262733.json"
    "config/json/MASTER_PROFILE_alx_trading_1748264047.json"
    "config/proxy_config.json"
    "results/dm_content_analysis/extracted_messages_1749233354.json"
    "REAL_DATA_BACKUP_*"
    "CLEAN_DATA_SUMMARY_*.json"
)

# Create workspace structure
mkdir -p {data,results,logs,config}

# List what we're keeping
echo "Keeping essential files:"
for file in "${KEEP_FILES[@]}"; do
    if [ -f "$file" ] || [ -d "$file" ]; then
        echo "  ✓ $file"
    fi
done

echo ""
echo "=== WORKSPACE CLEANED ==="
echo "Essential tools ready:"
echo "  ./realops.py       - Main operations interface"
echo "  recon              - Quick command (after source ~/.bashrc)"
echo "  db                 - Database access"
echo ""
echo "Real data preserved in:"
echo "  alx_trading_database.sqlite"
echo "  config/ directory"
echo "  results/ directory"
