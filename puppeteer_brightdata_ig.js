// Puppeteer + Bright Data Scraping Browser for Instagram (bypass block, human-like)
// Requires: Node.js, puppeteer
// Usage: node puppeteer_brightdata_ig.js <target_instagram_username> <wsEndpoint>

const puppeteer = require('puppeteer');


if (process.argv.length < 4) {
    console.log('Usage: node puppeteer_brightdata_ig.js <target_instagram_username> <wsEndpoint>');
    console.log('Example wsEndpoint: ws://127.0.0.1:9515/devtools/browser/<id>');
    process.exit(1);
}

const TARGET_USERNAME = process.argv[2];
const WS_ENDPOINT = process.argv[3];
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36';


(async () => {
    // Connect to Bright Data Scraping Browser via WebSocket endpoint
    const browser = await puppeteer.connect({
        browserWSEndpoint: WS_ENDPOINT,
        defaultViewport: { width: 1200, height: 800 },
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
    await browser.disconnect();
})();
