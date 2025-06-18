import instaloader
from instagrapi import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import httpx
import time

# --- Instaloader: ดึงข้อมูล profile และ media ---


def fetch_profile(username):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    print(f"[instaloader] Username: {profile.username}")
    print(f"[instaloader] Bio: {profile.biography}")
    print(f"[instaloader] Followers: {profile.followers}")
    print(f"[instaloader] Profile Pic: {profile.profile_pic_url}")
    # โหลด media ล่าสุด
    for post in profile.get_posts():
        print(f"[instaloader] Post: {post.url}")
        break

# --- Instagrapi: ดึง media ล่าสุด ---


def fetch_media_instagrapi(username):
    cl = Client()
    cl.login("your_username", "your_password")  # ใส่ account ทดสอบ
    user_id = cl.user_id_from_username(username)
    medias = cl.user_medias(user_id, 5)
    for m in medias:
        print(
            f"[instagrapi] Media: {m.dict().get('thumbnail_url', m.dict().get('url'))}")

# --- Selenium: Automation เข้า IG ---


def selenium_automation(username):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://www.instagram.com/{username}/"
    driver.get(url)
    print(f"[selenium] Page title: {driver.title}")
    driver.quit()

# --- httpx + BeautifulSoup: ดึงข้อมูล profile ---


def fetch_with_httpx(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = httpx.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("title").text if soup.find("title") else ""
    print(f"[httpx] Title: {title}")


if __name__ == "__main__":
    test_user = "instagram"  # เปลี่ยนเป็น username ที่ต้องการ
    print("\n--- Instaloader ---")
    fetch_profile(test_user)
    print("\n--- Instagrapi ---")
    # fetch_media_instagrapi(test_user)  # ต้องใส่ username/password
    print("\n--- Selenium ---")
    selenium_automation(test_user)
    print("\n--- httpx + BeautifulSoup ---")
    fetch_with_httpx(test_user)
