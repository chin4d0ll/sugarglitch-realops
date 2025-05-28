# Selenium IG Extractor for alx.trading
# ใช้สำหรับดึงข้อมูล IG ด้วย Selenium แบบ advance


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# --- CONFIG ---
IG_USERNAME = "alx.trading"
IG_PASSWORD = "Fleming654"  # ใส่รหัสผ่านจริงของบัญชีทดสอบ

# --- SETUP SELENIUM ---
chrome_options = Options()
chrome_options.add_argument('--headless')  # ถ้าอยากเห็น browser จริงๆ ให้คอมเมนต์บรรทัดนี้
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--window-size=1200,800')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

# ปิด warning SSL (ถ้าเจอปัญหา SSL)
chrome_options.add_argument('--ignore-certificate-errors')


# --- START DRIVER (ใช้ webdriver-manager ดาวน์โหลด chromedriver อัตโนมัติ) ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)

# --- LOGIN ---
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(IG_USERNAME)
password_input.send_keys(IG_PASSWORD)
password_input.send_keys(Keys.RETURN)
time.sleep(5)

# --- BYPASS POPUPS ---
try:
    not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
    not_now.click()
    time.sleep(2)
except:
    pass

# --- GO TO PROFILE ---
driver.get(f"https://www.instagram.com/{alx.tradingE}/")
time.sleep(3)

# --- EXTRACT DATA ---
followers = driver.find_element(By.XPATH, "//a[contains(@href, '/followers')]/span")
following = driver.find_element(By.XPATH, "//a[contains(@href, '/following')]/span")
posts = driver.find_element(By.XPATH, "//span[contains(@class, '_ac2a')]" )

print(f"Followers: {followers.text}")
print(f"Following: {following.text}")
print(f"Posts: {posts.text}")

# --- CLOSE ---
driver.quit()
