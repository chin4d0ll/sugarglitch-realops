const puppeteer = require('puppeteer-core');

async function run(){
    const BROWSER_WS = "wss://brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95@brd.superproxy.io:9222";
    try {
        console.log('Connecting to Browser API...');
        const browser = await puppeteer.connect({
            browserWSEndpoint: BROWSER_WS,
        });
        const page = await browser.newPage();
        await page.goto('https://www.example.com');
        // CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Browser API's automatic CAPTCHA solver
        // const client = await page.createCDPSession();
        // console.log('Waiting captcha to solve...');
        // const { status } = await client.send('Captcha.waitForSolve', {
        //   detectTimeout: 10000,
        // });
        // console.log('Captcha solve status:', status);
        const html = await page.content();
        console.log(html);
        await browser.close();
    } catch (error) {
        console.log(error)
    }
}

run()
