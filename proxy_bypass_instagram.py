import requests
import random
import time

PROXY_LIST = [
    "http://username:password@proxy1.example.com:8080",
    "http://username:password@proxy2.example.com:8080",
    "http://proxy3.example.com:3128",
    # เพิ่ม proxy ของคุณที่นี่
]

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    # เพิ่ม user-agent ที่นี่
]

TARGET_URL = "https://www.instagram.com/alx.trading/"

def get_with_proxy():
    for attempt in range(10):
        proxy = random.choice(PROXY_LIST)
        user_agent = random.choice(USER_AGENTS)
        proxies = {"http": proxy, "https": proxy}
        headers = {"User-Agent": user_agent}
        try:
            print(f"🌐 Attempt {attempt+1}: Proxy={proxy} | UA={user_agent[:30]}...")
            resp = requests.get(TARGET_URL, headers=headers, proxies=proxies, timeout=15)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                with open("alx_trading_proxy.html", "w", encoding="utf-8") as f:
                    f.write(resp.text)
                print("✅ Success! Saved HTML.")
                return
            elif resp.status_code == 429:
                print("⚠️ Rate limited! Retrying with new proxy...")
            else:
                print(f"❌ HTTP {resp.status_code}")
        except Exception as e:
            print(f"❌ Proxy failed: {e}")
        time.sleep(random.uniform(2, 6))
    print("❌ All proxies failed or blocked.")

if __name__ == "__main__":
    get_with_proxy()
