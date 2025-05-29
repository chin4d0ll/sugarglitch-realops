#!/bin/bash
# start_proxy.sh - Start Bright Data Proxy Manager with SG config and web auth

set -e


# Remove old/broken proxy-manager if not a valid binary
if [ -f proxy-manager ]; then
  if file proxy-manager | grep -q 'HTML'; then
    echo "Found invalid proxy-manager (HTML). Removing..."
    rm -f proxy-manager
  fi
fi

# Download Proxy Manager binary if not exists or after removal
if [ ! -f proxy-manager ]; then
  echo "Downloading Proxy Manager binary..."
  curl -L -o proxy-manager "https://brightdata.com/static/lpm/luminati-proxy-latest-linux" && chmod +x proxy-manager
fi

# Start Proxy Manager with config, web auth (admin/changeme123), and web UI on 22999
./proxy-manager \
  --config proxy_config.json \
  --www 22999 \
  --lpm_auth admin:changeme123 \
  --daemon
