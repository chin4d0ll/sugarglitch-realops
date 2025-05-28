# Selenium IG Extractor for alx.trading
# ใช้สำหรับดึงข้อมูล IG ด้วย Selenium แบบ advance

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- CONFIG ---
IG_USERNAME = "alx.trading"
IG_PASSWORD = "Fleming654"  # ใส่รหัสผ่านจริงของบัญชีทดสอบ

# --- SETUP SELENIUM ---
chrome_options = Options()
chrome_options.add_argument('--headless')
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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- STEALTH PATCH ---
def stealth(driver):
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
stealth(driver)

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)

# --- LOGIN ---
try:
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(IG_USERNAME)
    password_input.send_keys(IG_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)
    print("[DEBUG] Login submitted. Current URL:", driver.current_url)
    print("[DEBUG] Login page source snippet:", driver.page_source[:1000])
except Exception as e:
    print(f"❌ Login step failed: {e}")
    print("[DEBUG] Login page source snippet:", driver.page_source[:1000])
    driver.quit()
    exit(1)

# --- GO TO PROFILE ---
try:
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