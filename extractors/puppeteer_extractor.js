#!/usr/bin/env node
/**
 * 🎭 PUPPETEER INSTAGRAM EXTRACTOR
 * ===============================
 * Advanced browser automation for Instagram data extraction
 * Target: alx.trading profile
 */

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

class PuppeteerInstagramExtractor {
    constructor() {
        this.targetUsername = 'alx.trading';
        this.targetUserId = '4976283726';
        this.sessionId = '4976283726%3A1JgRzA56Q8e8Qs%3A12';
        this.dsUserId = '4976283726';
        this.outputDir = process.argv[2] || 'puppeteer_extraction';
        this.browser = null;
        this.page = null;
        
        console.log('🎭 PUPPETEER INSTAGRAM EXTRACTOR INITIALIZED');
        console.log(`📁 Output Directory: ${this.outputDir}`);
        console.log(`🎯 Target: ${this.targetUsername} (ID: ${this.targetUserId})`);
    }

    async init() {
        // Create output directory
        await fs.mkdir(this.outputDir, { recursive: true });
        await fs.mkdir(path.join(this.outputDir, 'screenshots'), { recursive: true });
        await fs.mkdir(path.join(this.outputDir, 'data'), { recursive: true });
        
        // Launch browser
        this.browser = await puppeteer.launch({
            headless: false, // Set to false for debugging
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        });
        
        this.page = await this.browser.newPage();
        
        // Set viewport and user agent
        await this.page.setViewport({ width: 1920, height: 1080 });
        await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
        
        console.log('✅ Browser launched successfully');
    }

    async setupSession() {
        console.log('🔧 Setting up Instagram session...');
        
        // Navigate to Instagram
        await this.page.goto('https://www.instagram.com/', { waitUntil: 'networkidle2' });
        
        // Set cookies
        await this.page.setCookie(
            {
                name: 'sessionid',
                value: this.sessionId,
                domain: '.instagram.com',
                path: '/',
                secure: true,
                sameSite: 'Lax'
            },
            {
                name: 'ds_user_id',
                value: this.dsUserId,
                domain: '.instagram.com',
                path: '/',
                secure: true,
                sameSite: 'Lax'
            },
            {
                name: 'csrftoken',
                value: 'missing',
                domain: '.instagram.com',
                path: '/',
                secure: true,
                sameSite: 'Lax'
            }
        );
        
        // Refresh to apply cookies
        await this.page.reload({ waitUntil: 'networkidle2' });
        
        // Navigate to target profile
        await this.page.goto(`https://www.instagram.com/${this.targetUsername}/`, { waitUntil: 'networkidle2' });
        
        // Take screenshot for verification
        await this.page.screenshot({ 
            path: path.join(this.outputDir, 'screenshots', 'profile_loaded.png'),
            fullPage: true 
        });
        
        console.log('✅ Session setup complete');
    }

    async extractProfileInfo() {
        console.log('📊 Extracting profile information...');
        
        try {
            const profileData = await this.page.evaluate(() => {
                const data = {};
                
                // Extract from meta tags
                const metaTags = document.querySelectorAll('meta');
                metaTags.forEach(tag => {
                    if (tag.getAttribute('property') === 'og:description') {
                        data.description = tag.getAttribute('content');
                    }
                    if (tag.getAttribute('property') === 'og:image') {
                        data.profilePicture = tag.getAttribute('content');
                    }
                });
                
                // Extract from page text
                const statsElements = document.querySelectorAll('a[href*="/followers/"], a[href*="/following/"]');
                statsElements.forEach(el => {
                    const text = el.textContent;
                    if (el.href.includes('followers')) {
                        data.followersCount = text;
                    }
                    if (el.href.includes('following')) {
                        data.followingCount = text;
                    }
                });
                
                // Extract posts count
                const postsElement = document.querySelector('div:-webkit-any-link');
                if (postsElement) {
                    const postsText = postsElement.textContent;
                    if (postsText && postsText.includes('posts')) {
                        data.postsCount = postsText;
                    }
                }
                
                // Extract bio
                const bioElement = document.querySelector('div[dir="auto"]');
                if (bioElement) {
                    data.bio = bioElement.textContent;
                }
                
                // Extract verification status
                data.isVerified = document.querySelector('svg[aria-label="Verified"]') !== null;
                
                // Extract profile picture high-res
                const profileImg = document.querySelector('img[alt*="profile picture"]');
                if (profileImg) {
                    data.profilePictureHD = profileImg.src;
                }
                
                return data;
            });
            
            // Save profile data
            await fs.writeFile(
                path.join(this.outputDir, 'data', 'profile_info.json'),
                JSON.stringify(profileData, null, 2)
            );
            
            console.log('✅ Profile information extracted');
            return profileData;
            
        } catch (error) {
            console.error('❌ Error extracting profile info:', error);
            return null;
        }
    }

    async extractStories() {
        console.log('📚 Extracting stories...');
        
        try {
            // Navigate to stories
            await this.page.goto(`https://www.instagram.com/stories/${this.targetUsername}/`, { waitUntil: 'networkidle2' });
            
            // Wait for stories to load
            await this.page.waitForTimeout(3000);
            
            // Take screenshot
            await this.page.screenshot({ 
                path: path.join(this.outputDir, 'screenshots', 'stories.png'),
                fullPage: true 
            });
            
            const storiesData = await this.page.evaluate(() => {
                const stories = [];
                
                // Extract story media
                const videoElements = document.querySelectorAll('video');
                const imgElements = document.querySelectorAll('img[decoding="auto"]');
                
                videoElements.forEach((video, index) => {
                    stories.push({
                        type: 'video',
                        url: video.src,
                        index: index,
                        timestamp: Date.now()
                    });
                });
                
                imgElements.forEach((img, index) => {
                    if (img.src && img.src.includes('instagram')) {
                        stories.push({
                            type: 'image',
                            url: img.src,
                            index: index,
                            timestamp: Date.now()
                        });
                    }
                });
                
                return stories;
            });
            
            // Save stories data
            await fs.writeFile(
                path.join(this.outputDir, 'data', 'stories.json'),
                JSON.stringify(storiesData, null, 2)
            );
            
            console.log(`✅ Extracted ${storiesData.length} stories`);
            return storiesData;
            
        } catch (error) {
            console.error('❌ Error extracting stories:', error);
            return [];
        }
    }

    async extractPosts() {
        console.log('📷 Extracting posts...');
        
        try {
            // Navigate back to profile
            await this.page.goto(`https://www.instagram.com/${this.targetUsername}/`, { waitUntil: 'networkidle2' });
            
            // Scroll to load more posts
            let previousHeight = 0;
            let currentHeight = await this.page.evaluate('document.body.scrollHeight');
            
            while (previousHeight !== currentHeight) {
                previousHeight = currentHeight;
                await this.page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
                await this.page.waitForTimeout(2000);
                currentHeight = await this.page.evaluate('document.body.scrollHeight');
            }
            
            // Extract post data
            const postsData = await this.page.evaluate(() => {
                const posts = [];
                
                // Find all post links
                const postLinks = document.querySelectorAll('a[href*="/p/"]');
                
                postLinks.forEach((link, index) => {
                    const img = link.querySelector('img');
                    if (img) {
                        posts.push({
                            postUrl: link.href,
                            imageUrl: img.src,
                            alt: img.alt,
                            index: index
                        });
                    }
                });
                
                return posts;
            });
            
            // Save posts data
            await fs.writeFile(
                path.join(this.outputDir, 'data', 'posts.json'),
                JSON.stringify(postsData, null, 2)
            );
            
            console.log(`✅ Extracted ${postsData.length} posts`);
            return postsData;
            
        } catch (error) {
            console.error('❌ Error extracting posts:', error);
            return [];
        }
    }

    async extractDMs() {
        console.log('💬 Extracting DMs...');
        
        try {
            // Navigate to DMs
            await this.page.goto('https://www.instagram.com/direct/inbox/', { waitUntil: 'networkidle2' });
            
            // Wait for DMs to load
            await this.page.waitForTimeout(5000);
            
            // Take screenshot
            await this.page.screenshot({ 
                path: path.join(this.outputDir, 'screenshots', 'dms.png'),
                fullPage: true 
            });
            
            const dmsData = await this.page.evaluate(() => {
                const conversations = [];
                
                // Extract conversation list
                const convElements = document.querySelectorAll('[role="button"]');
                
                convElements.forEach((element, index) => {
                    const text = element.textContent;
                    if (text && text.trim()) {
                        conversations.push({
                            text: text.trim(),
                            index: index,
                            timestamp: Date.now()
                        });
                    }
                });
                
                return conversations;
            });
            
            // Save DMs data
            await fs.writeFile(
                path.join(this.outputDir, 'data', 'dms.json'),
                JSON.stringify(dmsData, null, 2)
            );
            
            console.log(`✅ Extracted ${dmsData.length} DM conversations`);
            return dmsData;
            
        } catch (error) {
            console.error('❌ Error extracting DMs:', error);
            return [];
        }
    }

    async extractFollowersFollowing() {
        console.log('👥 Extracting followers and following...');
        
        const results = { followers: [], following: [] };
        
        try {
            // Extract followers
            await this.page.goto(`https://www.instagram.com/${this.targetUsername}/followers/`, { waitUntil: 'networkidle2' });
            await this.page.waitForTimeout(3000);
            
            // Scroll in modal to load more
            for (let i = 0; i < 10; i++) {
                await this.page.evaluate(() => {
                    const modal = document.querySelector('[role="dialog"]');
                    if (modal) {
                        modal.scrollTop = modal.scrollHeight;
                    }
                });
                await this.page.waitForTimeout(1000);
            }
            
            const followers = await this.page.evaluate(() => {
                const users = [];
                const userElements = document.querySelectorAll('a[href*="/"][href!="/"]');
                
                userElements.forEach(element => {
                    const href = element.getAttribute('href');
                    if (href && href.startsWith('/') && href !== '/') {
                        const username = href.replace('/', '');
                        if (username && !username.includes('/')) {
                            users.push(username);
                        }
                    }
                });
                
                return [...new Set(users)]; // Remove duplicates
            });
            
            results.followers = followers;
            
            // Extract following
            await this.page.goto(`https://www.instagram.com/${this.targetUsername}/following/`, { waitUntil: 'networkidle2' });
            await this.page.waitForTimeout(3000);
            
            // Scroll in modal to load more
            for (let i = 0; i < 10; i++) {
                await this.page.evaluate(() => {
                    const modal = document.querySelector('[role="dialog"]');
                    if (modal) {
                        modal.scrollTop = modal.scrollHeight;
                    }
                });
                await this.page.waitForTimeout(1000);
            }
            
            const following = await this.page.evaluate(() => {
                const users = [];
                const userElements = document.querySelectorAll('a[href*="/"][href!="/"]');
                
                userElements.forEach(element => {
                    const href = element.getAttribute('href');
                    if (href && href.startsWith('/') && href !== '/') {
                        const username = href.replace('/', '');
                        if (username && !username.includes('/')) {
                            users.push(username);
                        }
                    }
                });
                
                return [...new Set(users)]; // Remove duplicates
            });
            
            results.following = following;
            
            // Save followers/following data
            await fs.writeFile(
                path.join(this.outputDir, 'data', 'followers_following.json'),
                JSON.stringify(results, null, 2)
            );
            
            console.log(`✅ Extracted ${results.followers.length} followers and ${results.following.length} following`);
            return results;
            
        } catch (error) {
            console.error('❌ Error extracting followers/following:', error);
            return results;
        }
    }

    async cleanup() {
        if (this.browser) {
            await this.browser.close();
            console.log('🧹 Browser closed');
        }
    }

    async runFullExtraction() {
        console.log('🚀 Starting full Puppeteer extraction...');
        
        try {
            await this.init();
            await this.setupSession();
            
            const results = {
                profile: await this.extractProfileInfo(),
                stories: await this.extractStories(),
                posts: await this.extractPosts(),
                dms: await this.extractDMs(),
                social: await this.extractFollowersFollowing(),
                timestamp: new Date().toISOString()
            };
            
            // Save complete results
            await fs.writeFile(
                path.join(this.outputDir, 'complete_extraction.json'),
                JSON.stringify(results, null, 2)
            );
            
            console.log('🎉 Puppeteer extraction completed successfully!');
            console.log(`📊 Results saved to: ${this.outputDir}`);
            
            return results;
            
        } catch (error) {
            console.error('💥 Extraction failed:', error);
            throw error;
        } finally {
            await this.cleanup();
        }
    }
}

// Run if called directly
if (require.main === module) {
    const extractor = new PuppeteerInstagramExtractor();
    extractor.runFullExtraction()
        .then(() => {
            console.log('✅ Extraction completed');
            process.exit(0);
        })
        .catch(error => {
            console.error('❌ Extraction failed:', error);
            process.exit(1);
        });
}

module.exports = PuppeteerInstagramExtractor;
