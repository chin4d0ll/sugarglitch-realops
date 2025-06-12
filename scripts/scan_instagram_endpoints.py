"""
สคริปต์นี้จะเปิด Instagram DM ใน Chrome (headless) และดึง network log เพื่อหา endpoint ที่เกี่ยวข้องกับ direct_v2 หรือ graphql
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("w3c", False)
chrome_options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True})
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--window-size=1200,800")

caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['loggingPrefs'] = {'performance': 'ALL'}
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

print("🚀 Launching Chrome and navigating to Instagram DM...")
driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
driver.get("https://www.instagram.com/direct/inbox/")

print("⏳ Waiting for network activity...")
time.sleep(15)  # รอให้หน้าเว็บโหลดและมี network activity

print("🔍 Scanning network logs for endpoints...")
logs = driver.get_log("performance")
endpoints = set()
for entry in logs:
    try:
        msg = json.loads(entry["message"])['message']
        if msg["method"] == "Network.requestWillBeSent":
            url = msg["params"]["request"]["url"]
            if any(x in url for x in ["direct_v2", "graphql", "api"]):
                endpoints.add(url)
    except Exception:
        continue

driver.quit()

print("\n📋 พบ endpoints ที่เกี่ยวข้อง:")
for ep in sorted(endpoints):
    print(ep)

with open("/workspaces/sugarglitch-realops/INSTAGRAM_ENDPOINTS_FOUND.txt", "w") as f:
    for ep in sorted(endpoints):
        f.write(ep + "\n")

print("\n✅ บันทึก endpoints ที่พบไว้ที่ INSTAGRAM_ENDPOINTS_FOUND.txt แล้ว!")
