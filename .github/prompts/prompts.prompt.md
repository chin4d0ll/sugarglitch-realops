# Copilot Prompts for SugarGlitch RealOps

ไฟล์นี้รวบรวม Prompts สำหรับใช้งานกับ GitHub Copilot ใน Codespace เพื่อช่วยให้การพัฒนาและปรับแต่งสคริปต์ในโปรเจกต์ **SugarGlitch RealOps** เป็นไปอย่างรวดเร็วและตรงความต้องการมากขึ้น

---

## 1. Setup & Initialization


# สร้างไฟล์ Python ใหม่และติดตั้ง dependencies เบื้องต้น
# Prompt: 
# “Generate a Python script that installs Playwright, sets up Chromium, 
# and verifies installation by launching a headless browser.”

# สร้างไฟล์ Dockerfile สำหรับรันสคริปต์ IG DM Extractor แบบ Dockerized
# Prompt:
# “Write a Dockerfile that uses Python 3.9 slim as base, installs Playwright,
# copies the project directory, runs `playwright install chromium`, and sets 
# the entrypoint to `python3 src/ultra_dm_conversation_extractor_2025.py`.”

# สร้างไฟล์ docker-compose.yml ที่เชื่อมกับ PostgreSQL และมี service สำหรับ DM extractor
# Prompt:
# “Generate a docker-compose.yml with two services: 
# 1) ‘db’: Postgres 14, environment variables POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB; 
# 2) ‘dm_extractor’: build from Dockerfile, depends_on ‘db’, linked network, mount a volume for outputs,
# and set environment variables for database URI and session file path.”


⸻

2. DM Extraction

# สร้างฟังก์ชันดึง DM แบบละเอียดพร้อม media ด้วย Instagram Private API
# Prompt:
# “Using requests library, write a function `fetch_instagram_dms(sessionid: str)` 
# that calls Instagram’s private API endpoint `/api/v1/direct_v2/inbox/`, 
# paginates through all threads, saves messages and media URLs into a JSON structure, 
# and returns the JSON data.”

# สร้างฟังก์ชันเก็บ media (รูปภาพ/วิดีโอ) ใน DM ลงโฟลเดอร์แยกตาม thread ID
# Prompt:
# “Write a Python function `download_dm_media(dm_data: dict, output_dir: str)` 
# that takes the JSON data from `fetch_instagram_dms`, iterates over each thread, 
# and downloads all media URLs to `output_dir/{thread_id}/` while preserving original filenames.”


⸻

3. Session Management & Stealth

# สร้างฟังก์ชัน load และ validate session จากไฟล์ JSON ในโฟลเดอร์ sessions/
# Prompt:
# “Generate a Python function `load_session(session_file: str) -> dict` 
# that reads a JSON file containing `sessionid` and `user_agent`, verifies that 
# the session is still valid by making a test request to `https://www.instagram.com/`, 
# and returns a dictionary with cookie and headers if valid, otherwise raises an exception.”

# สร้างฟังก์ชันสำหรับสุ่ม User-Agent และสลับ Proxy จากไฟล์ config
# Prompt:
# “Write a Python function `get_stealth_headers(proxy_list: List[str]) -> Tuple[dict, str]` 
# that picks a random proxy from `proxy_list`, randomizes a mobile User-Agent string, 
# and returns (headers_dict, proxy_url) for use in requests sessions.”


⸻

4. Brute-Force Workflow

# สร้างสคริปต์ brute-force รหัสผ่าน IG ด้วย wordlist และ proxy rotation
# Prompt:
# “Create a Python script `instagram_bruteforce.py` which:
# 1. Loads a `wordlist.txt` of passwords,
# 2. Loads a `session_example.json` containing a valid `sessionid` and `csrftoken`,
# 3. Iterates through each password, sending POST requests to 
#    `https://www.instagram.com/accounts/login/ajax/` with required headers and cookies,
# 4. Uses a rotating proxy from a given `proxy_list`,
# 5. Adds random delays (0.5–1.5s) between attempts,
# 6. Logs successes (when `authenticated”: true` in JSON response) to `found_credentials.json`,
# 7. Stops when a valid password is found or when the list is exhausted.”

# สร้างฟังก์ชันตรวจสอบว่า account เปิด 2FA หรือไม่
# Prompt:
# “Write a Python function `check_two_factor(username: str) -> bool` that sends a POST to 
# `https://www.instagram.com/accounts/check_two_factor/` or simulates the login flow to detect if 
# the username requires a 2FA code, and returns True if 2FA is enabled, otherwise False.”


⸻

5. Database Integration & Reporting

# สร้างไฟล์ schema.sql สำหรับสร้างตาราง DM ใน PostgreSQL
# Prompt:
# “Generate a SQL file `schema.sql` with:
# 1. Table `users` (columns: id SERIAL PRIMARY KEY, username TEXT UNIQUE, full_name TEXT, last_seen TIMESTAMP),
# 2. Table `threads` (columns: id SERIAL PRIMARY KEY, thread_id TEXT UNIQUE, created_at TIMESTAMP),
# 3. Table `messages` (columns: id SERIAL PRIMARY KEY, thread_id INTEGER REFERENCES threads(id), 
#    sender_username TEXT, message_text TEXT, timestamp TIMESTAMP, media_url TEXT),
# 4. Ensure proper indexes on `thread_id` and `sender_username`.”

# สร้างฟังก์ชันบันทึก DM ลงใน PostgreSQL
# Prompt:
# “Write a Python function `save_dms_to_db(dms: dict, db_uri: str)` that:
# 1. Connects to PostgreSQL using SQLAlchemy or psycopg2,
# 2. Iterates through threads in `dms`, inserts or updates `threads` table,
# 3. Inserts each message into `messages` table,
# 4. Creates/updates sender information in `users` table,
# 5. Commits all changes and handles errors gracefully.”

# สร้างสคริปต์รายงานสถิติเบื้องต้นจาก DB แล้ว export เป็น CSV/Excel
# Prompt:
# “Generate a Python script `report_generator.py` that:
# 1. Connects to PostgreSQL using SQLAlchemy,
# 2. Queries number of threads, number of messages per thread, top 5 active senders,
# 3. Exports these results into `report_summary.csv` and `report_summary.xlsx` using pandas.”


⸻

6. Alerting & Webhook Integration

# สร้างฟังก์ชันส่ง Discord Webhook เมื่อเจอข้อความใหม่ใน DM
# Prompt:
# “Write a Python function `notify_discord(new_messages: List[dict], webhook_url: str)` 
# that formats each new DM as Discord embed fields (sender + snippet + timestamp) and 
# sends a POST request to `webhook_url` with the payload following Discord’s JSON schema.”

# สร้างฟังก์ชันเช็ค session หมดอายุ และแจ้ง LINE Notify ถ้าหมดอายุ
# Prompt:
# “Write a Python function `check_session_and_notify(session_info: dict, line_token: str)` that:
# 1. Makes a test request to `https://www.instagram.com/direct/inbox/` using session_info cookies/headers,
# 2. If response indicates login challenge or 401, sends a POST to LINE Notify API with a custom message,
# 3. Returns True if session still valid, otherwise False.”


⸻

7. Advanced Tools & Customization

# สร้างฟังก์ชันสลับ Proxy Pool อัตโนมัติระหว่างงาน Recon/Exploit
# Prompt:
# “Generate a Python class `ProxyRotator` that:
# 1. Loads a JSON array of proxy URLs from `config/proxies/proxy_config.json`,
# 2. Provides a method `get_next_proxy()` returning the next proxy in a round-robin fashion,
# 3. Has a health-check method `validate_proxy(proxy: str) -> bool` that tests a simple request (e.g., to https://httpbin.org/ip) and returns True if low latency (< 500ms), False otherwise.”

# สร้างฟังก์ชันดึงแผนภาพ timeline การโต้ตอบ DM (จำนวนข้อความต่อวัน)
# Prompt:
# “Write a Python function `generate_dm_timeline(dms: dict, output_png: str)` that:
# 1. Parses `dms` JSON to count messages per day,
# 2. Uses matplotlib to plot a line chart (x-axis: date, y-axis: message count),
# 3. Saves the chart as `output_png`. Do not specify any custom colors—use default.”


⸻

8. Utility & Maintenance

# สร้างสคริปต์ลบโฟลเดอร์ media เก่าทุก 30 วันในโฟลเดอร์ exports/
# Prompt:
# “Write a Bash script `cleanup_old_media.sh` that:
# 1. Finds all subdirectories in `exports/` older than 30 days,
# 2. Deletes them recursively,
# 3. Logs deleted folder names to `cleanup.log` with timestamp.”

# สร้าง GitHub Actions Workflow ทดสอบโค้ด DM Extractor ทุกครั้งที่ push
# Prompt:
# “Generate a `.github/workflows/ci.yml` that:
# 1. Triggers on `push` to `main`,
# 2. Sets up Python 3.9 environment,
# 3. Installs dependencies from `requirements.txt`,
# 4. Runs `python -m pytest tests/` (assume tests exist),
# 5. Caches pip dependencies for speed.”


⸻

9. Example Prompts for Custom Scenarios

# ต้องการให้ Copilot ช่วยเพิ่มฟังก์ชัน stealth: random delay + UA rotation
# Prompt:
# “Inside `src/instagram_tools/real_instagram_operations.py`, add a helper function 
# `get_stealth_session()` that returns a `requests.Session()` object configured with:
# - A random mobile User-Agent string from a predefined list
# - Optional SOCKS5 proxy from `config/proxies/proxy_config.json`
# - A method `delay()` that sleeps for a random duration between 0.5 and 1.5 seconds before each request.”

# ต้องการให้ Copilot ช่วยสร้าง function ดึง list followers แบบ paginated
# Prompt:
# “Write a Python function `fetch_followers(username: str, session: requests.Session) -> List[str]`
# that:
# 1. Calls Instagram’s private API endpoint for followers (e.g., `/api/v1/friendships/{user_id}/followers/`),
# 2. Paginates using `next_max_id` until all followers are fetched,
# 3. Returns a list of follower usernames.”

# ต้องการให้ Copilot ช่วยสร้างสคริปต์ social engineering phishing page เบื้องต้น
# Prompt:
# “Generate an HTML file `phish_login.html` that mimics Instagram’s login page styling (use official CSS links), 
# with a form posting to a PHP endpoint `steal.php`. Include hidden fields to capture CSRF token if needed.”


⸻

วิธีใช้งานไฟล์นี้
	1.	คัดลอก Prompts ที่ต้องการไปวางใน Comments หรือในโค้ดที่ต้องการให้ Copilot ช่วยเขียน
	2.	ปรับแต่ง คำสั่งให้ตรงตามชื่อโฟลเดอร์ และชื่อฟังก์ชันจริงในโปรเจกต์ของคุณ
	3.	รันใน Codespace เพื่อให้ Copilot แนะนำ code snippet อัตโนมัติ
	4.	ตรวจเช็ก & ทดสอบ ว่าโค้ดที่ได้จาก Copilot ทำงานถูกต้องก่อนใช้งานจริงเสมอ

⸻

ไฟล์นี้ถือเป็น “คีย์หลัก” สำหรับเร่งการพัฒนาใน GitHub Codespaces ร่วมกับ Copilot ให้ Dreamy ได้โค้ดรวดเร็ว ตรงโจทย์ ทุกฟีเจอร์ในโปรเจกต์ SugarGlitch RealOps! 🚀✨