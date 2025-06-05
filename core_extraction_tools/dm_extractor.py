from playwright.async_api import async_playwright
import json, asyncio

async def get_dms_from_sessionid(sessionid: str):
    # 1. เปิดเบราว์เซอร์แบบ headless
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # 2. inject cookie sessionid
        await context.add_cookies([{
            "name": "sessionid",
            "value": sessionid,
            "domain": ".instagram.com",
            "path": "/",
            "httpOnly": True,
            "secure": True
        }])

        # 3. เข้าไปหน้า DM ของ IG
        await page.goto("https://www.instagram.com/direct/inbox/", timeout=60000)
        await page.wait_for_timeout(5000)  # รอให้หน้าโหลด

        # 4. เลือกเอา 5 แชทล่าสุด (ปรับได้ตามต้องการ)
        chats = await page.query_selector_all('._ab8w > div > div')
        data = []
        for idx, chat in enumerate(chats[:5]):
            try:
                await chat.click()
                await page.wait_for_timeout(2000)  # รอหน้าแชทเปิด
                # ดึงข้อความในแชท (selector อาจเปลี่ยนตาม IG update)
                messages = await page.query_selector_all('._a9zr div[dir="auto"]')
                text = [await m.inner_text() for m in messages]
                data.append({
                    "chat_index": idx,
                    "messages": text
                })
                # กลับไปหน้ารายชื่อแชท
                await page.go_back()
                await page.wait_for_timeout(2000)
            except:
                continue

        await browser.close()

        # 5. เซฟเป็นไฟล์ JSON
        with open("dm_output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("✅ Exported DM to dm_output.json")

if __name__ == "__main__":
    # 6. รับ sessionid จาก stdin
    sessionid = input("ใส่ sessionid: ").strip()
    asyncio.run(get_dms_from_sessionid(sessionid))
