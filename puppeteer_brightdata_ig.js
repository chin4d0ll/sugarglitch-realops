// Puppeteer + Bright Data Scraping Browser for Instagram (bypass block, human-like)
// Requires: Node.js, puppeteer
// Usage: node puppeteer_brightdata_ig.js <target_instagram_username>

const puppeteer = require('puppeteer');

if (process.argv.length < 3) {
    console.log('Usage: node puppeteer_brightdata_ig.js <target_instagram_username>');
    process.exit(1);
}

const TARGET_USERNAME = process.argv[2];
const BRD_PROXY = 'http://brd-customer-hl_63f0835e-zone-scraping_browser1:bj0nymiw6mij@brd.superproxy.io:9515';
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36';

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            `--proxy-server=${BRD_PROXY}`,
            '--window-size=1200,800',
            '--disable-blink-features=AutomationControlled',
        ]
    });
    const page = await browser.newPage();
    await page.setUserAgent(USER_AGENT);
    await page.setViewport({ width: 1200, height: 800 });
    console.log(`[DEBUG] Navigating to https://www.instagram.com/${TARGET_USERNAME}/`);
    await page.goto(`https://www.instagram.com/${TARGET_USERNAME}/`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(5000);
    console.log('[INFO] Page title:', await page.title());
    const content = await page.content();
    console.log('[INFO] Page content snippet:', content.substring(0, 2000));
    await browser.close();
})();
