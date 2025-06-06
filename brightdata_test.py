import requests

# กรอกข้อมูล Bright Data Proxy ของคุณที่นี่
BRIGHTDATA_PROXY = "brd.superproxy.io:22225"  # หรือ host:port ที่ Bright Data ให้มา
USERNAME = "lum-customer-<your-customer>-zone-<zone>"
PASSWORD = "<your_password>"

proxies = {
    "http": f"http://{USERNAME}:{PASSWORD}@{BRIGHTDATA_PROXY}",
    "https": f"http://{USERNAME}:{PASSWORD}@{BRIGHTDATA_PROXY}",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

url = "https://www.instagram.com/alx.trading/"

try:
    response = requests.get(url, headers=headers, proxies=proxies, timeout=20)
    print("Status:", response.status_code)
    print(response.text[:500])  # แสดงแค่ 500 ตัวอักษรแรก
except Exception as e:
    print(f"❌ Error: {e}")
