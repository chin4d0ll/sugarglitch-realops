import asyncio
from playwright.async_api import async_playwright
from utils.error_handler import safe_execution, safe_print


AUTH = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
SBR_WS_CDP = f'wss://{AUTH}@brd.superproxy.io:9222'

async def run(pw):
    print('Connecting to Browser API...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        print('Connected! Navigating to webpage')
        await page.goto('https://www.example.com')
        
        # More info at https://playwright.dev/python/docs/screenshots
        await page.screenshot(path='screenshot.png', full_page=True)
        
        print("Screenshot saved as 'screenshot.png'")
        html = await page.content()
        print(html)
    finally:
        await browser.close()

async @safe_execution
def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
