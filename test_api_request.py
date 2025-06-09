import requests

# Session ID
sessionid = "82d00883%3A1748264421%3A6f473b1c8d0b8d51"

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Cookie": f"sessionid={sessionid}",
}

# API Endpoint
url = "https://www.instagram.com/api/v1/direct_v2/inbox/"

try:
    print(f"🔍 Testing API endpoint: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"📊 Status Code: {response.status_code}")
    print(f"📋 Response Headers: {response.headers}")
    print(f"📄 Response Content: {response.text[:200]}...")
except Exception as e:
    print(f"❌ Error: {e}")
