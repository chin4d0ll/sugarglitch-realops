#!/usr/bin/env python3
"""
🔥 Quick Vmess Hunter - Get Free Internet in 30 seconds!
💀 OpenTunnel + Auto QR + Clash Config Generator
"""

import requests
import base64
import json
import qrcode
import os
from datetime import datetime

# 🔥 Working OpenTunnel endpoints (updated June 2025)
ENDPOINTS = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
]


def get_free_vmess():
    """🎯 Get working vmess configs fast"""
    print("🔥 QUICK VMESS HUNTER - Getting free configs...")

    all_vmess = []

    for url in ENDPOINTS:
        try:
            print(f"📡 Trying: {url.split('/')[-2]}/{url.split('/')[-1]}")

            headers = {"User-Agent": "v2rayNG/1.8.3"}
            r = requests.get(url, headers=headers, timeout=10)

            if r.status_code == 200:
                # Try to decode base64
                try:
                    content = base64.b64decode(r.text).decode('utf-8')
                except:
                    content = r.text

                # Extract vmess links
                for line in content.splitlines():
                    if line.strip().startswith("vmess://"):
                        all_vmess.append(line.strip())

                print(
                    f"✅ Found {len([l for l in content.splitlines() if l.strip().startswith('vmess://')])} vmess")

        except Exception as e:
            print(f"❌ Failed: {str(e)[:30]}...")

    return all_vmess[:5]  # Return best 5


def decode_vmess(vmess_url):
    """🧬 Decode vmess URL"""
    try:
        payload = vmess_url.replace("vmess://", "")
        padded = payload + '=' * (-len(payload) % 4)
        decoded = base64.b64decode(padded).decode('utf-8')
        return json.loads(decoded)
    except:
        return None


def make_qr(vmess_url, filename):
    """📸 Generate QR code"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(vmess_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return True
    except:
        return False


def generate_clash_yaml(configs):
    """⚔️ Generate Clash config"""
    clash = {
        "port": 7890,
        "socks-port": 7891,
        "allow-lan": True,
        "mode": "rule",
        "log-level": "info",
        "external-controller": "127.0.0.1:9090",
        "proxies": [],
        "proxy-groups": [
            {
                "name": "🔥 FREE",
                "type": "select",
                "proxies": ["♻️ AUTO"]
            },
            {
                "name": "♻️ AUTO",
                "type": "url-test",
                "proxies": [],
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300
            }
        ],
        "rules": [
            "DOMAIN-SUFFIX,local,DIRECT",
            "IP-CIDR,192.168.0.0/16,DIRECT",
            "IP-CIDR,10.0.0.0/8,DIRECT",
            "GEOIP,CN,DIRECT",
            "MATCH,🔥 FREE"
        ]
    }

    proxy_names = []
    for i, config in enumerate(configs, 1):
        if not config:
            continue

        name = f"Free-{i}"
        proxy_names.append(name)

        proxy = {
            "name": name,
            "type": "vmess",
            "server": config.get('add'),
            "port": int(config.get('port', 443)),
            "uuid": config.get('id'),
            "alterId": int(config.get('aid', 0)),
            "cipher": config.get('scy', 'auto'),
            "tls": config.get('tls') == 'tls'
        }

        if config.get('net') == 'ws':
            proxy["network"] = "ws"
            proxy["ws-opts"] = {
                "path": config.get('path', '/'),
                "headers": {"Host": config.get('host', config.get('add'))}
            }

        clash["proxies"].append(proxy)

    clash["proxy-groups"][0]["proxies"].extend(proxy_names)
    clash["proxy-groups"][1]["proxies"] = proxy_names

    return clash


def main():
    """🚀 Main function"""
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Starting Quick Hunt...")

    # Get vmess links
    vmess_links = get_free_vmess()

    if not vmess_links:
        print("❌ No vmess found!")
        return

    print(f"\n🎯 Processing {len(vmess_links)} configs...")

    # Create output folder
    os.makedirs("free_configs", exist_ok=True)
    os.chdir("free_configs")

    configs = []
    working_count = 0

    for i, vmess in enumerate(vmess_links, 1):
        config = decode_vmess(vmess)
        if config:
            configs.append(config)

            # Show config info
            server = config.get('add', 'N/A')
            port = config.get('port', 'N/A')
            tls = '🔒' if config.get('tls') else '🔓'

            print(f"[{i}] {server}:{port} {tls}")

            # Generate QR
            qr_file = f"qr_{i}.png"
            if make_qr(vmess, qr_file):
                working_count += 1
                print(f"    📸 QR: {qr_file}")

            # Save raw vmess
            with open(f"vmess_{i}.txt", 'w') as f:
                f.write(vmess)

    # Generate Clash config
    if configs:
        try:
            import yaml
            clash_config = generate_clash_yaml(configs)
            with open('clash.yaml', 'w') as f:
                yaml.dump(clash_config, f, default_flow_style=False)
            print(f"⚔️ Clash config: clash.yaml")
        except ImportError:
            print("⚠️ PyYAML not found, skipping Clash config")

    print(f"""
🎉 DONE! Generated {working_count} working configs
📁 Output folder: free_configs/
📸 QR codes: qr_*.png (scan with phone)
📝 Raw vmess: vmess_*.txt
⚔️ Clash: clash.yaml

🚀 Ready to use with:
   • V2rayNG: Scan QR codes
   • Clash Meta: Import clash.yaml 
   • Shadowrocket: Scan QR codes
    """)


if __name__ == "__main__":
    main()
