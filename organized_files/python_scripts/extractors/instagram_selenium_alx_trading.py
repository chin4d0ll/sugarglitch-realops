# Selenium IG Extractor for alx.trading
# ใช้สำหรับดึงข้อมูล IG ด้วย Selenium แบบ advance


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys
import json



# --- CONFIG ---
# Allow username as command-line argument
if len(sys.argv) > 1:
    IG_USERNAME = sys.argv[1]
else:
    IG_USERNAME = "alx.trading"  # Default

# --- COOKIES ---
COOKIES = {
    "sessionid": "82d00883%3A1748264421%3A6f473b1c8d0b8d51",
    "csrftoken": "8474a9868a2759304d6bc7c2810437ff",
    "rur": "VLL"
}



# --- SETUP SELENIUM ---
import tempfile
chrome_options = Options()
chrome_options.add_argument('--headless')  # Enable headless mode for server/CI
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--window-size=1200,800')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
# Use a unique temporary user data dir to avoid session errors
tmp_user_data_dir = tempfile.mkdtemp(prefix="selenium_chrome_profile_")
chrome_options.add_argument(f'--user-data-dir={tmp_user_data_dir}')

# --- PROXY SETUP ---
proxy_path = os.path.join(os.path.dirname(__file__), 'proxy_config_new.json')
proxy = None
if os.path.exists(proxy_path):
    with open(proxy_path, 'r') as f:
        proxies = json.load(f)
        if proxies and isinstance(proxies, list):
            proxy = proxies[0]  # Use the first proxy
if proxy:
    proxy_str = proxy.get('http')
    if proxy_str:
        chrome_options.add_argument(f'--proxy-server={proxy_str}')
        print(f"[DEBUG] Using proxy: {proxy_str}")
    else:
        print("[DEBUG] Proxy config found but no 'http' key.")
else:
    print("[DEBUG] No proxy config found or file missing.")

# (Removed --user-data-dir to avoid session not created error)

service = Service(ChromeDriverManager().install())

print("[DEBUG] Starting Chrome WebDriver...")
driver = webdriver.Chrome(service=service, options=chrome_options)
print("[DEBUG] WebDriver started.")


# --- STEALTH PATCH ---
def stealth(driver):
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
stealth(driver)

# --- LOAD COOKIES ---
def load_cookies_from_txt(txt_path):
    cookies = []
    if not os.path.exists(txt_path):
        print(f"[ERROR] Cookie file not found: {txt_path}")
        return cookies
    with open(txt_path, "r") as f:
        cookie_line = f.read().strip()
        for part in cookie_line.split(';'):
            if '=' in part:
                name, value = part.strip().split('=', 1)
                cookies.append({"name": name, "value": value, "domain": ".instagram.com", "path": "/"})
    return cookies

# --- INJECT COOKIES ---
print("[DEBUG] Navigating to Instagram main page for cookie injection...")
driver.get("https://www.instagram.com/")
time.sleep(3)
for name, value in COOKIES.items():
    try:
        driver.add_cookie({"name": name, "value": value, "domain": ".instagram.com"})
        print(f"[DEBUG] Injected cookie: {name}")
    except Exception as e:
        print(f"[ERROR] Failed to inject cookie {name}: {e}")
print("[DEBUG] All cookies injected. Refreshing page...")
driver.get(f"https://instagram.com/{IG_USERNAME}/")
time.sleep(5)
print("[DEBUG] Loaded profile page. Current URL:", driver.current_url)

# ตรวจสอบว่าหลุดไปหน้า login หรือเปล่า
if "login" in driver.current_url:
    print("❌ ยังโดน redirect ไป login อยู่จ้า~")
    print("[DEBUG] Profile page source snippet:", driver.page_source[:1000])
else:
    print("[DEBUG] Profile page loaded OK!")

# --- GO TO PROFILE ---
try:
    print(f"[DEBUG] Navigating to profile: https://www.instagram.com/{IG_USERNAME}/")
    driver.get(f"https://www.instagram.com/{IG_USERNAME}/")
    time.sleep(5)
    print("[DEBUG] Loaded profile page. Current URL:", driver.current_url)
    print("[DEBUG] Profile page source snippet:", driver.page_source[:2000])
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//header"))
    )
except Exception as e:
    print(f"❌ Failed to load profile page: {e}")
    print("[DEBUG] Current URL:", driver.current_url)
    print("[DEBUG] Profile page source snippet:", driver.page_source[:2000])
    driver.quit()
    exit(1)

# --- EXTRACT DATA ---
try:
    followers = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]/span | //a[contains(@href, '/followers')]/div/span"))
    )
    following = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]/span | //a[contains(@href, '/following')]/div/span"))
    )
    posts = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, '_ac2a')]"))
    )
    print(f"Followers: {followers.text}")
    print(f"Following: {following.text}")
    print(f"Posts: {posts.text}")
except Exception as e:
    print(f"❌ Data extraction failed: {e}")
    print("[DEBUG] Profile page source snippet:", driver.page_source[:2000])

# --- CLOSE ---
driver.quit()