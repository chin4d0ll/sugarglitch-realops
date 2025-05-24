const puppeteer = require('puppeteer-core');

async function connectToBrowser() {
    const BROWSER_WS = "wss://brd-customer-hl_a3b13c04-zone-scraping_browser:hl_a3b13c04@brd.superproxy.io:9222";
    try {
        console.log('🌸 กำลังเชื่อมต่อ BrightData Browser API...');
        const browser = await puppeteer.connect({
            browserWSEndpoint: BROWSER_WS,
        });
        
        console.log('✅ เชื่อมต่อ Browser API สำเร็จ!');
        return browser;
    } catch (error) {
        console.log('❌ เชื่อมต่อ Browser API ล้มเหลว:', error.message);
        return null;
    }
}

async function testInstagramAccess() {
    const browser = await connectToBrowser();
    if (!browser) return false;
    
    try {
        const page = await browser.newPage();
        
        // ตั้งค่า User-Agent ให้เหมือนมือถือ
        await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1');
        
        console.log('🔄 กำลังเข้าถึง Instagram...');
        await page.goto('https://www.instagram.com/', { waitUntil: 'networkidle2' });
        
        const title = await page.title();
        console.log('✅ เข้าถึง Instagram สำเร็จ!');
        console.log('📄 Title:', title);
        
        await browser.close();
        return true;
    } catch (error) {
        console.log('❌ ไม่สามารถเข้าถึง Instagram:', error.message);
        await browser.close();
        return false;
    }
}

async function extractInstagramData(sessionId) {
    const browser = await connectToBrowser();
    if (!browser) return null;
    
    try {
        const page = await browser.newPage();
        
        // ตั้งค่า User-Agent
        await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1');
        
        // ตั้งค่า session cookie
        await page.setCookie({
            name: 'sessionid',
            value: sessionId,
            domain: '.instagram.com',
            path: '/',
            httpOnly: true,
            secure: true
        });
        
        console.log('🔄 กำลังเข้าถึง Instagram DMs...');
        await page.goto('https://www.instagram.com/direct/inbox/', { waitUntil: 'networkidle2' });
        
        // รอให้หน้าโหลดและตรวจสอบว่า login สำเร็จ
        await page.waitForTimeout(3000);
        
        const currentUrl = page.url();
        if (currentUrl.includes('/accounts/login/')) {
            console.log('❌ Session ID ไม่ถูกต้องหรือหมดอายุ');
            await browser.close();
            return null;
        }
        
        console.log('✅ เข้าสู่ระบบสำเร็จ!');
        
        // ดึงข้อมูล DMs (ตัวอย่างง่ายๆ)
        const dms = await page.evaluate(() => {
            // โค้ดสำหรับดึงข้อมูล DMs จากหน้าเว็บ
            // นี่เป็นตัวอย่างง่ายๆ อาจต้องปรับแต่งตาม UI ของ Instagram
            const conversations = [];
            const elements = document.querySelectorAll('[role="button"]');
            
            elements.forEach((el, index) => {
                if (index < 5) { // ดึงแค่ 5 รายการแรก
                    const text = el.textContent || el.innerText;
                    if (text && text.length > 0) {
                        conversations.push({
                            user: `User_${index + 1}`,
                            last_message: text.substring(0, 100)
                        });
                    }
                }
            });
            
            return conversations;
        });
        
        console.log(`✅ ดึงข้อมูล DMs สำเร็จ! จำนวน ${dms.length} รายการ`);
        
        await browser.close();
        return dms;
        
    } catch (error) {
        console.log('❌ เกิดข้อผิดพลาดในการดึงข้อมูล:', error.message);
        await browser.close();
        return null;
    }
}

// Export functions สำหรับใช้จาก Python
module.exports = {
    connectToBrowser,
    testInstagramAccess,
    extractInstagramData
};

// รันทดสอบถ้าไฟล์นี้ถูกเรียกโดยตรง
if (require.main === module) {
    async function main() {
        console.log('🌸 SugarGlitch Browser API Tester');
        console.log('='.repeat(50));
        
        // ทดสอบการเชื่อมต่อ
        await testInstagramAccess();
        
        console.log('='.repeat(50));
        console.log('💡 หากต้องการดึงข้อมูลจริง ให้ใส่ session ID ใน session.json แล้วรัน main.py');
    }
    
    main().catch(console.error);
}
