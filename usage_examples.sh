#!/bin/bash
# 🔥 SugarGlitch RealOps - Production Usage Examples
# Real CLI execution examples for authenticated Instagram intelligence

echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "💀                SUGARGLITCH REALOPS                💀"
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "⚡ Production Usage Examples"
echo "🎯 Real-time Instagram Intelligence & Breach Analysis"
echo "⚠️  AUTHORIZED REDTEAM USE ONLY"
echo ""

# Example 1: Basic execution with specific targets
echo "📋 Example 1: Basic execution with specific targets"
echo "python run_main_realops.py --target @alx.trading --target @whatilove1728"
echo ""

# Example 2: Extended execution with custom settings
echo "📋 Example 2: Extended execution with custom timeout"
echo "python run_main_realops.py \\"
echo "  --target @alx.trading \\"
echo "  --target @whatilove1728 \\"
echo "  --timeout 7200 \\"
echo "  --export-dir ./custom_exports \\"
echo "  --verbose"
echo ""

# Example 3: Batch execution from file
echo "📋 Example 3: Batch execution from targets file"
echo "echo -e 'alx.trading\\nwhatilove1728' > targets.txt"
echo "python run_main_realops.py --targets-file targets.txt"
echo ""

# Example 4: Docker execution
echo "📋 Example 4: Docker container execution"
echo "docker run -v \$(pwd):/workspace -w /workspace \\"
echo "  -e IG_SESSIONID=\$IG_SESSIONID \\"
echo "  -e DISCORD_WEBHOOK_URL=\$DISCORD_WEBHOOK_URL \\"
echo "  python:3.11-slim \\"
echo "  python run_main_realops.py --target @alx.trading"
echo ""

# Example 5: Cron job execution
echo "📋 Example 5: Cron job (daily execution)"
echo "# Add to crontab -e"
echo "0 2 * * * cd /path/to/sugarglitch-realops && python run_main_realops.py --target @alx.trading --no-discord 2>&1 | logger -t sugarglitch"
echo ""

# Example 6: Environment variable override
echo "📋 Example 6: Environment variable override"
echo "IG_SESSIONID=\"your_real_session_44chars\" \\"
echo "TARGET_LIST=\"alx.trading,whatilove1728\" \\"
echo "DISCORD_WEBHOOK_URL=\"https://discord.com/api/webhooks/your_webhook\" \\"
echo "python run_main_realops.py"
echo ""

# Example 7: Production deployment with systemd
echo "📋 Example 7: Production systemd service"
echo "# Create /etc/systemd/system/sugarglitch-realops.service"
echo "[Unit]"
echo "Description=SugarGlitch RealOps Production Service"
echo "After=network.target"
echo ""
echo "[Service]"
echo "Type=oneshot"
echo "User=realops"
echo "WorkingDirectory=/opt/sugarglitch-realops"
echo "Environment=IG_SESSIONID=your_real_sessionid"
echo "Environment=DISCORD_WEBHOOK_URL=your_webhook_url"
echo "ExecStart=/usr/bin/python3 run_main_realops.py --target @alx.trading"
echo "StandardOutput=journal"
echo "StandardError=journal"
echo ""
echo "[Install]"
echo "WantedBy=multi-user.target"
echo ""

echo "🚨 SECURITY REMINDERS:"
echo "1. Never commit real IG_SESSIONID to version control"
echo "2. Use environment variables or .env files for secrets"
echo "3. Rotate Instagram sessions regularly"
echo "4. Monitor Discord webhooks for unauthorized access"
echo "5. Review export files for sensitive data before sharing"
echo ""

echo "🔧 SETUP CHECKLIST:"
echo "✅ 1. Get real Instagram session ID from browser dev tools"
echo "✅ 2. Create Discord webhook in target server"
echo "✅ 3. Set up proper .env file with required variables"
echo "✅ 4. Test with --verbose flag first"
echo "✅ 5. Set up log rotation for production use"
echo ""

echo "🎯 Ready to execute? Choose an example above and replace with your real values."
