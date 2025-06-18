import instaloader
import httpx
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# --- Instaloader Example ---


def fetch_with_instaloader(username):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    print(f"[instaloader] Username: {profile.username}")
    print(f"[instaloader] Bio: {profile.biography}")
    print(f"[instaloader] Followers: {profile.followers}")
    print(f"[instaloader] Profile Pic: {profile.profile_pic_url}")

# --- httpx + BeautifulSoup Example ---


def fetch_with_httpx(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = httpx.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("title").text
    print(f"[httpx] Title: {title}")
    # (For real scraping, parse JSON in <script> tags)

# --- Selenium Example ---


def fetch_with_selenium(username):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://www.instagram.com/{username}/"
    driver.get(url)
    print(f"[selenium] Page title: {driver.title}")
    driver.quit()


if __name__ == "__main__":
    test_user = "instagram"  # เปลี่ยนเป็น username ที่ต้องการ
    print("\n--- Instaloader ---")
    fetch_with_instaloader(test_user)
    print("\n--- httpx + BeautifulSoup ---")
    fetch_with_httpx(test_user)
    print("\n--- Selenium ---")
    fetch_with_selenium(test_user)
