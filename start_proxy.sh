#!/bin/bash
# start_proxy.sh - Start Bright Data Proxy Manager with SG config and web auth

set -e



# === Bright Data Proxy Manager (LPM) via npm ===
if ! command -v luminati &> /dev/null; then
  echo "[INFO] luminati (LPM) not found. Installing via npm..."
  npm install -g @luminati-io/luminati-proxy || { echo '[ERROR] npm install failed!'; exit 1; }
fi

echo "[INFO] Starting Bright Data Proxy Manager (LPM) via luminati ..."
luminati \
  --config proxy_config.json \
  --www 22999 \
  --lpm_auth admin:changeme123 \
  --daemon
