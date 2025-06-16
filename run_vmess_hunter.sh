#!/bin/bash
# 🔥 OpenTunnel Vmess Hunter - One-Click Free Internet
# 💀 Auto install dependencies and run

echo "🔥 OpenTunnel Vmess Hunter - One-Click Setup"
echo "⚡ Installing dependencies..."

# Install Python packages
pip3 install -q requests qrcode[pil] PyYAML Pillow 2>/dev/null || {
    echo "📦 Installing packages..."
    pip3 install requests qrcode[pil] PyYAML Pillow
}

echo "✅ Dependencies ready!"
echo ""

# Run the hunter
python3 ultimate_vmess_hunter.py

# Show results
latest_dir=$(ls -td free_internet_*/ 2>/dev/null | head -1)
if [ -n "$latest_dir" ]; then
    echo ""
    echo "📁 Results saved in: $latest_dir"
    echo "📱 QR codes ready to scan:"
    ls -1 "${latest_dir}"qr_*.png 2>/dev/null | head -5
    echo ""
    echo "🚀 Ready to use! Check the USAGE.txt file for instructions."
fi
