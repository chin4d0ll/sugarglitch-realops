# REALOPS - Essential Operations

## เอาสาระค่ะเน้นใล้งานจริง (Focus on Real Work)

### Ready to Use
```bash
source ~/.bashrc   # Load aliases
recon             # Main interface
```

### Core Tools
- **realops.py** - Main operations menu
- **Database** - Real trading data (alx.trading, whatilove1728)
- **Aliases** - recon, db, scan, quick

### Real Data
✓ alx_trading_database.sqlite - Contact database  
✓ comprehensive_dm_scan_results_1749231518.json - DM data  
✓ alx_trading_session_fleming654.json - Session data  
✓ config/json/MASTER_PROFILE_*.json - Profile data  

### Commands
```bash
recon      # Operations menu
db         # Database access
scan IP    # Port scan
quick HOST # Ping test
```

**Status**: Ready for real work  
**Focus**: Essential tools only

# วิธีการทำให้โหดในงานพัฒนา Python

## 1. ทำงานเร็วปรี๊ดดด
- ใช้ฟังก์ชันที่มีประสิทธิภาพสูง เช่น `asyncio` เพื่อจัดการงานที่ต้องรอคอย (เช่น HTTP requests) หรือ `multiprocessing` สำหรับ parallel processing
- เลือกใช้ library ที่ optimize แล้ว เช่น `numpy` สำหรับการคำนวณทางคณิตศาสตร์ หรือ `aiohttp` สำหรับ HTTP requests แบบ asynchronous
- ลดการใช้ loops ซ้อนกัน (nested loops) โดยใช้ list comprehension หรือ generator functions

ตัวอย่าง:
```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

urls = ["https://www.instagram.com", "https://www.facebook.com"]
results = asyncio.run(main(urls))
print(results)
```

## 2. ใช้เมมโมรี่น้อยๆ
- ใช้ generator เพื่อประหยัด memory แทนการเก็บข้อมูลใน list
- ลดการเก็บค่าที่ไม่จำเป็นในตัวแปร
- ใช้ library เช่น `pandas` หรือ `sqlite` สำหรับการจัดการข้อมูลขนาดใหญ่

ตัวอย่าง:
```python
def generate_numbers(limit):
    for i in range(limit):
        yield i

for number in generate_numbers(1000):
    print(number)
```

## 3. การ hack/exploit เพื่อการศึกษา
- ศึกษา API documentation อย่างละเอียด
- ใช้ tools เช่น `Burp Suite` หรือ `Wireshark` เพื่อดู traffic
- ใช้ Python libraries เช่น `requests` หรือ `socket` เพื่อส่ง HTTP requests หรือสร้าง connections

ตัวอย่าง:
```python
import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

response = requests.get("https://api.instagram.com/v1/users/self", headers=headers)
print(response.json())
```

## 4. ตั้งค่า Environment ให้เหมาะสม
### Extensions ที่แนะนำ:
- Python Development Pack:
  - ms-python.python
  - ms-python.flake8
  - ms-python.black-formatter

### Remote Development
- ติดตั้งและใช้ `Visual Studio Code` พร้อมกับ `Dev Containers` เพื่อทำงานร่วมกับ Codespaces หรือ Docker

---

## ข้อมูลเพิ่มเติมจากภาพ
ภาพที่แนบมาแสดงการใช้ session สำหรับ Instagram API และการจัดการ rate limit ด้วยคำสั่ง Python เช่น `sleep()` ในการลดความถี่ของ requests เพื่อป้องกันการถูก block

---

## References
- [Python Official Documentation](https://docs.python.org/3/)
- [Hacker's Guide to Python](https://inventwithpython.com/)

---

## วิธีหา Instagram API Endpoint ที่อัปเดตล่าสุด
1. เปิด Developer Tools (F12) ใน browser ขณะใช้งาน Instagram Web
2. ไปที่แท็บ Network แล้วกรองด้วยคำว่า `graphql` หรือ `api`
3. ส่ง DM หรือโหลดหน้า DM แล้วดู request ที่ถูกส่งออกไป
4. คัดลอก URL endpoint ที่ Instagram ใช้จริง เช่น `/api/graphql/` หรือ `/api/v1/direct_v2/inbox/`
5. ทดสอบ endpoint เหล่านั้นใน Python ด้วย requests หรือ aiohttp

**หมายเหตุ:** Instagram อาจเปลี่ยน endpoint หรือเพิ่มการป้องกันบ่อยครั้ง ควรตรวจสอบและอัปเดตสคริปต์เป็นระยะ
