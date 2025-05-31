#!/usr/bin/env python3
"""
🕵️💀 ADVANCED INSTAGRAM OSINT TOOLKIT 2025 💀🕵️
================================================
- Deep Social Media Cross-Reference
- Advanced Search Engine Mining
- Reverse Image Search
- Username Pattern Analysis
- Digital Footprint Mapping
- Social Network Analysis

Created by: น้องจิน (chin4d0ll) ♥️
For: Educational & Security Research Only!
"""

import asyncio
import aiohttp
import json
import time
import random
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import base64
import warnings
warnings.filterwarnings("ignore")

class AdvancedInstagramOSINT:
    """Advanced OSINT Toolkit สำหรับ Instagram"""
    
    def __init__(self):
        self.session = None
        self.results_cache = {}
        self.search_engines = self._init_search_engines()
        self.social_platforms = self._init_social_platforms()
        self.username_patterns = self._init_username_patterns()
        
        print("🕵️ Advanced Instagram OSINT Toolkit ถูกสร้างแล้ว!")
        
    def _init_search_engines(self) -> Dict[str, Dict[str, str]]:
        """Search Engines สำหรับ OSINT"""
        return {
            "google": {
                "url": "https://www.google.com/search",
                "params": {"q": "", "num": "20", "hl": "en"},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "bing": {
                "url": "https://www.bing.com/search",
                "params": {"q": "", "count": "20"},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "duckduckgo": {
                "url": "https://duckduckgo.com/html/",
                "params": {"q": "", "kl": "us-en"},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "yandex": {
                "url": "https://yandex.com/search/",
                "params": {"text": "", "lr": "213"},
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        }
        
    def _init_social_platforms(self) -> Dict[str, Dict[str, str]]:
        """Social Media Platforms สำหรับค้นหา"""
        return {
            "twitter": {
                "search_url": "https://twitter.com/search",
                "profile_url": "https://twitter.com/{}",
                "api_patterns": [
                    "https://api.twitter.com/1.1/users/show.json?screen_name={}",
                    "https://twitter.com/i/api/graphql/*/UserByScreenName"
                ]
            },
            "facebook": {
                "search_url": "https://www.facebook.com/search/people/",
                "profile_url": "https://www.facebook.com/{}",
                "api_patterns": [
                    "https://graph.facebook.com/{}",
                    "https://www.facebook.com/api/graphql/"
                ]
            },
            "tiktok": {
                "search_url": "https://www.tiktok.com/search/user",
                "profile_url": "https://www.tiktok.com/@{}",
                "api_patterns": [
                    "https://www.tiktok.com/api/user/detail/",
                    "https://m.tiktok.com/api/user/detail/"
                ]
            },
            "linkedin": {
                "search_url": "https://www.linkedin.com/search/results/people/",
                "profile_url": "https://www.linkedin.com/in/{}",
                "api_patterns": [
                    "https://www.linkedin.com/voyager/api/search/dash/clusters"
                ]
            },
            "youtube": {
                "search_url": "https://www.youtube.com/results",
                "profile_url": "https://www.youtube.com/@{}",
                "api_patterns": [
                    "https://www.googleapis.com/youtube/v3/channels",
                    "https://www.youtube.com/youtubei/v1/search"
                ]
            },
            "snapchat": {
                "search_url": "https://www.snapchat.com/add/{}",
                "profile_url": "https://www.snapchat.com/add/{}",
                "api_patterns": []
            },
            "pinterest": {
                "search_url": "https://www.pinterest.com/search/people/",
                "profile_url": "https://www.pinterest.com/{}",
                "api_patterns": [
                    "https://www.pinterest.com/resource/UserResource/get/"
                ]
            },
            "reddit": {
                "search_url": "https://www.reddit.com/search/",
                "profile_url": "https://www.reddit.com/user/{}",
                "api_patterns": [
                    "https://www.reddit.com/api/username_available.json",
                    "https://www.reddit.com/user/{}/about.json"
                ]
            },
            "discord": {
                "search_url": "",
                "profile_url": "",
                "api_patterns": [
                    "https://discord.com/api/v10/users/@me"
                ]
            },
            "telegram": {
                "search_url": "https://t.me/{}",
                "profile_url": "https://t.me/{}",
                "api_patterns": [
                    "https://api.telegram.org/bot{}/getChat"
                ]
            }
        }
        
    def _init_username_patterns(self) -> List[str]:
        """รูปแบบ Username ที่น่าจะใช้"""
        return [
            "{}",  # username เดิม
            "{}_",  # เติม underscore
            "_{}", 
            "{}1", "{}2", "{}3",  # เติมตัวเลข
            "{}123", "{}2024", "{}2025",
            "{}.official", "{}.real", "{}.me",  # เติม suffix
            "the{}", "real{}", "official{}",  # เติม prefix
            "{}gram", "{}ig", "{}insta",  # Instagram specific
            "{}_ig", "{}_insta", "{}_gram"
        ]
        
    async def initialize_session(self):
        """เริ่มต้น Session"""
        connector = aiohttp.TCPConnector(
            limit=50,
            limit_per_host=20,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        
        print("🕵️ OSINT Session เริ่มต้นแล้ว!")
        
    async def search_engine_reconnaissance(self, target: str) -> Dict[str, Any]:
        """ค้นหาข้อมูลจาก Search Engines"""
        print(f"🔍 เริ่ม Search Engine Reconnaissance: {target}")
        
        results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "search_engines": {},
            "total_results": 0,
            "instagram_references": [],
            "other_social_media": [],
            "potential_leads": []
        }
        
        # สร้าง Search Queries ต่างๆ
        search_queries = [
            f'"{target}" instagram',
            f'"{target}" site:instagram.com',
            f'"{target}" instagram profile',
            f'"{target}" instagram account',
            f'instagram.com/{target}',
            f'"{target}" social media',
            f'"{target}" facebook twitter',
            f'"{target}" contact information'
        ]
        
        for engine_name, engine_config in self.search_engines.items():
            print(f"  🌐 ค้นหาใน {engine_name.upper()}...")
            
            engine_results = {
                "engine": engine_name,
                "queries_performed": [],
                "results_found": [],
                "error": None
            }
            
            try:
                for query in search_queries:
                    await asyncio.sleep(random.uniform(1, 3))  # Rate limiting
                    
                    query_result = await self._search_single_engine(
                        engine_config, query
                    )
                    
                    engine_results["queries_performed"].append({
                        "query": query,
                        "status": query_result.get("status", "unknown"),
                        "results_count": len(query_result.get("results", []))
                    })
                    
                    if query_result.get("results"):
                        engine_results["results_found"].extend(query_result["results"])
                        
                        # วิเคราะห์ผลลัพธ์
                        for result in query_result["results"]:
                            if "instagram.com" in result.get("url", "").lower():
                                results["instagram_references"].append({
                                    "engine": engine_name,
                                    "title": result.get("title", ""),
                                    "url": result.get("url", ""),
                                    "snippet": result.get("snippet", "")
                                })
                            elif any(social in result.get("url", "").lower() for social in ["facebook.com", "twitter.com", "tiktok.com", "linkedin.com"]):
                                results["other_social_media"].append({
                                    "engine": engine_name,
                                    "platform": self._extract_platform_from_url(result.get("url", "")),
                                    "title": result.get("title", ""),
                                    "url": result.get("url", ""),
                                    "snippet": result.get("snippet", "")
                                })
                                
                results["search_engines"][engine_name] = engine_results
                results["total_results"] += len(engine_results["results_found"])
                
            except Exception as e:
                print(f"    ❌ Error searching {engine_name}: {e}")
                engine_results["error"] = str(e)
                results["search_engines"][engine_name] = engine_results
                
        print(f"  📊 Total Results: {results['total_results']}")
        print(f"  📷 Instagram References: {len(results['instagram_references'])}")
        print(f"  🌐 Other Social Media: {len(results['other_social_media'])}")
        
        return results
        
    async def _search_single_engine(self, engine_config: Dict, query: str) -> Dict[str, Any]:
        """ค้นหาใน Search Engine เดียว"""
        try:
            headers = {
                "User-Agent": engine_config["user_agent"],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            params = engine_config["params"].copy()
            
            # Set query parameter based on engine
            if "google" in engine_config["url"]:
                params["q"] = query
            elif "bing" in engine_config["url"]:
                params["q"] = query
            elif "duckduckgo" in engine_config["url"]:
                params["q"] = query
            elif "yandex" in engine_config["url"]:
                params["text"] = query
                
            async with self.session.get(
                engine_config["url"], 
                params=params, 
                headers=headers
            ) as response:
                
                if response.status == 200:
                    text = await response.text()
                    results = self._parse_search_results(text, engine_config["url"])
                    
                    return {
                        "status": "success",
                        "results": results,
                        "query": query
                    }
                else:
                    return {
                        "status": f"error_{response.status}",
                        "results": [],
                        "query": query
                    }
                    
        except Exception as e:
            return {
                "status": "exception",
                "error": str(e),
                "results": [],
                "query": query
            }
            
    def _parse_search_results(self, html: str, search_url: str) -> List[Dict[str, str]]:
        """แยกผลลัพธ์จาก HTML ของ Search Engine"""
        results = []
        
        try:
            # Google Search Results
            if "google.com" in search_url:
                # หา title และ url
                title_pattern = r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>'
                matches = re.findall(title_pattern, html, re.DOTALL)
                
                for url, title in matches[:10]:  # เอาแค่ 10 อันแรก
                    # ทำความสะอาด title
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    if url.startswith('/url?q='):
                        url = urllib.parse.parse_qs(url.split('?', 1)[1]).get('q', [''])[0]
                        
                    if url and title:
                        results.append({
                            "title": title[:200],
                            "url": url,
                            "snippet": ""
                        })
                        
            # Bing Search Results
            elif "bing.com" in search_url:
                title_pattern = r'<h2><a href="([^"]+)"[^>]*>(.*?)</a></h2>'
                matches = re.findall(title_pattern, html, re.DOTALL)
                
                for url, title in matches[:10]:
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    if url and title:
                        results.append({
                            "title": title[:200],
                            "url": url,
                            "snippet": ""
                        })
                        
            # DuckDuckGo Results
            elif "duckduckgo.com" in search_url:
                title_pattern = r'<a rel="nofollow" href="([^"]+)"[^>]*class="result__a"[^>]*>(.*?)</a>'
                matches = re.findall(title_pattern, html, re.DOTALL)
                
                for url, title in matches[:10]:
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    if url and title:
                        results.append({
                            "title": title[:200],
                            "url": url,
                            "snippet": ""
                        })
                        
        except Exception as e:
            print(f"Error parsing search results: {e}")
            
        return results
        
    def _extract_platform_from_url(self, url: str) -> str:
        """แยก Platform จาก URL"""
        url_lower = url.lower()
        
        if "facebook.com" in url_lower:
            return "facebook"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "twitter"
        elif "tiktok.com" in url_lower:
            return "tiktok"
        elif "linkedin.com" in url_lower:
            return "linkedin"
        elif "youtube.com" in url_lower:
            return "youtube"
        elif "snapchat.com" in url_lower:
            return "snapchat"
        elif "pinterest.com" in url_lower:
            return "pinterest"
        elif "reddit.com" in url_lower:
            return "reddit"
        elif "t.me" in url_lower:
            return "telegram"
        else:
            return "unknown"
            
    async def cross_platform_username_search(self, username: str) -> Dict[str, Any]:
        """ค้นหา Username ใน Social Media Platforms ต่างๆ"""
        print(f"👥 เริ่ม Cross-Platform Username Search: {username}")
        
        results = {
            "target_username": username,
            "timestamp": datetime.now().isoformat(),
            "platforms_checked": {},
            "found_profiles": [],
            "username_variations": [],
            "total_platforms": len(self.social_platforms),
            "successful_finds": 0
        }
        
        # สร้าง Username Variations
        username_variations = []
        for pattern in self.username_patterns:
            variation = pattern.format(username)
            username_variations.append(variation)
            
        results["username_variations"] = username_variations[:20]  # เอาแค่ 20 อันแรก
        
        # ค้นหาใน Platform ต่างๆ
        for platform_name, platform_config in self.social_platforms.items():
            print(f"  🔍 ค้นหาใน {platform_name.upper()}...")
            
            platform_result = {
                "platform": platform_name,
                "profiles_found": [],
                "variations_checked": [],
                "error": None
            }
            
            try:
                # ตรวจสอบ Username หลักก่อน
                main_check = await self._check_profile_exists(
                    platform_config["profile_url"].format(username),
                    platform_name
                )
                
                if main_check["exists"]:
                    profile_data = {
                        "username": username,
                        "url": platform_config["profile_url"].format(username),
                        "platform": platform_name,
                        "confidence": "high",
                        "details": main_check.get("details", {})
                    }
                    platform_result["profiles_found"].append(profile_data)
                    results["found_profiles"].append(profile_data)
                    results["successful_finds"] += 1
                    
                platform_result["variations_checked"].append({
                    "username": username,
                    "exists": main_check["exists"],
                    "status_code": main_check.get("status_code", 0)
                })
                
                # ตรวจสอบ Variations (เอาแค่ 5 อันแรก)
                for variation in username_variations[:5]:
                    if variation != username:
                        await asyncio.sleep(random.uniform(0.5, 1.5))  # Rate limiting
                        
                        variation_check = await self._check_profile_exists(
                            platform_config["profile_url"].format(variation),
                            platform_name
                        )
                        
                        platform_result["variations_checked"].append({
                            "username": variation,
                            "exists": variation_check["exists"],
                            "status_code": variation_check.get("status_code", 0)
                        })
                        
                        if variation_check["exists"]:
                            profile_data = {
                                "username": variation,
                                "url": platform_config["profile_url"].format(variation),
                                "platform": platform_name,
                                "confidence": "medium",
                                "details": variation_check.get("details", {})
                            }
                            platform_result["profiles_found"].append(profile_data)
                            results["found_profiles"].append(profile_data)
                            results["successful_finds"] += 1
                            
                results["platforms_checked"][platform_name] = platform_result
                
            except Exception as e:
                print(f"    ❌ Error checking {platform_name}: {e}")
                platform_result["error"] = str(e)
                results["platforms_checked"][platform_name] = platform_result
                
        print(f"  📊 Profiles Found: {results['successful_finds']}")
        print(f"  🎯 Success Rate: {(results['successful_finds'] / results['total_platforms']) * 100:.1f}%")
        
        return results
        
    async def _check_profile_exists(self, profile_url: str, platform: str) -> Dict[str, Any]:
        """ตรวจสอบว่า Profile มีอยู่จริงหรือไม่"""
        try:
            headers = {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ]),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            async with self.session.get(profile_url, headers=headers) as response:
                result = {
                    "exists": False,
                    "status_code": response.status,
                    "url": profile_url,
                    "details": {}
                }
                
                # ตรวจสอบ Status Code
                if response.status == 200:
                    text = await response.text()
                    
                    # ตรวจสอบเฉพาะ Platform
                    if platform == "instagram":
                        if "Page Not Found" not in text and "Sorry, this page isn't available" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_instagram_details(text)
                            
                    elif platform == "twitter":
                        if "This account doesn't exist" not in text and "User not found" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_twitter_details(text)
                            
                    elif platform == "facebook":
                        if "Content Not Found" not in text and "Page not found" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_facebook_details(text)
                            
                    elif platform == "tiktok":
                        if "Couldn't find this account" not in text and "User not found" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_tiktok_details(text)
                            
                    elif platform == "linkedin":
                        if "Member not found" not in text and "Profile not found" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_linkedin_details(text)
                            
                    elif platform == "youtube":
                        if "This channel doesn't exist" not in text and "404 Not Found" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_youtube_details(text)
                            
                    elif platform == "reddit":
                        if "page not found" not in text.lower() and "user not found" not in text.lower():
                            result["exists"] = True
                            result["details"] = self._extract_reddit_details(text)
                            
                    elif platform == "pinterest":
                        if "Sorry, we couldn't find that page" not in text:
                            result["exists"] = True
                            result["details"] = self._extract_pinterest_details(text)
                            
                    else:
                        # สำหรับ Platforms อื่นๆ ใช้ Generic detection
                        error_indicators = [
                            "not found", "doesn't exist", "page not found", 
                            "user not found", "404", "no such user"
                        ]
                        
                        text_lower = text.lower()
                        if not any(indicator in text_lower for indicator in error_indicators):
                            result["exists"] = True
                            
                return result
                
        except Exception as e:
            return {
                "exists": False,
                "error": str(e),
                "url": profile_url
            }
            
    def _extract_instagram_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก Instagram Profile"""
        details = {}
        
        # หา Display Name
        name_match = re.search(r'"full_name":"([^"]+)"', html)
        if name_match:
            details["display_name"] = name_match.group(1)
            
        # หา Bio
        bio_match = re.search(r'"biography":"([^"]+)"', html)
        if bio_match:
            details["bio"] = bio_match.group(1)
            
        # หา Follower Count
        followers_match = re.search(r'"edge_followed_by":{"count":(\d+)}', html)
        if followers_match:
            details["followers"] = int(followers_match.group(1))
            
        # หา Following Count
        following_match = re.search(r'"edge_follow":{"count":(\d+)}', html)
        if following_match:
            details["following"] = int(following_match.group(1))
            
        # หา Posts Count
        posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)}', html)
        if posts_match:
            details["posts"] = int(posts_match.group(1))
            
        # หา Profile Picture
        profile_pic_match = re.search(r'"profile_pic_url_hd":"([^"]+)"', html)
        if profile_pic_match:
            details["profile_picture"] = profile_pic_match.group(1)
            
        return details
        
    def _extract_twitter_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก Twitter Profile"""
        details = {}
        
        # Basic Twitter profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    def _extract_facebook_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก Facebook Profile"""
        details = {}
        
        # Basic Facebook profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    def _extract_tiktok_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก TikTok Profile"""
        details = {}
        
        # Basic TikTok profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    def _extract_linkedin_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก LinkedIn Profile"""
        details = {}
        
        # Basic LinkedIn profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    def _extract_youtube_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก YouTube Profile"""
        details = {}
        
        # Basic YouTube profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    def _extract_reddit_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก Reddit Profile"""
        details = {}
        
        # Basic Reddit profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    def _extract_pinterest_details(self, html: str) -> Dict[str, Any]:
        """แยกรายละเอียดจาก Pinterest Profile"""
        details = {}
        
        # Basic Pinterest profile extraction
        name_match = re.search(r'<title>([^<]+)</title>', html)
        if name_match:
            details["title"] = name_match.group(1)
            
        return details
        
    async def comprehensive_osint_scan(self, target: str) -> Dict[str, Any]:
        """สแกน OSINT แบบครอบคลุม"""
        print(f"🕵️ เริ่ม Comprehensive OSINT Scan: {target}")
        
        start_time = time.time()
        
        results = {
            "target": target,
            "scan_timestamp": datetime.now().isoformat(),
            "scan_duration": 0,
            "search_engine_results": {},
            "cross_platform_results": {},
            "summary": {
                "total_instagram_references": 0,
                "total_social_profiles_found": 0,
                "total_search_results": 0,
                "confidence_score": 0
            }
        }
        
        try:
            # 1. Search Engine Reconnaissance
            search_results = await self.search_engine_reconnaissance(target)
            results["search_engine_results"] = search_results
            results["summary"]["total_instagram_references"] = len(search_results.get("instagram_references", []))
            results["summary"]["total_search_results"] = search_results.get("total_results", 0)
            
            # 2. Cross-Platform Username Search
            platform_results = await self.cross_platform_username_search(target)
            results["cross_platform_results"] = platform_results
            results["summary"]["total_social_profiles_found"] = platform_results.get("successful_finds", 0)
            
            # 3. คำนวณ Confidence Score
            confidence = 0
            if results["summary"]["total_instagram_references"] > 0:
                confidence += 30
            if results["summary"]["total_social_profiles_found"] > 0:
                confidence += 40
            if results["summary"]["total_search_results"] > 10:
                confidence += 20
            if results["summary"]["total_social_profiles_found"] > 3:
                confidence += 10
                
            results["summary"]["confidence_score"] = min(confidence, 100)
            
            results["scan_duration"] = time.time() - start_time
            
            print(f"✅ OSINT Scan Complete!")
            print(f"📊 Instagram References: {results['summary']['total_instagram_references']}")
            print(f"👥 Social Profiles Found: {results['summary']['total_social_profiles_found']}")
            print(f"🔍 Total Search Results: {results['summary']['total_search_results']}")
            print(f"🎯 Confidence Score: {results['summary']['confidence_score']}%")
            print(f"⏱️ Duration: {results['scan_duration']:.2f} seconds")
            
        except Exception as e:
            print(f"❌ Error in OSINT scan: {e}")
            results["error"] = str(e)
            
        return results
        
    async def save_osint_results(self, results: Dict[str, Any], filename: str = None):
        """บันทึกผลลัพธ์ OSINT"""
        if not filename:
            timestamp = int(time.time())
            target = results.get("target", "unknown")
            filename = f"osint_results_{target}_{timestamp}.json"
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        # สร้างรายงานสรุป
        summary_file = filename.replace('.json', '_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"🕵️ OSINT INVESTIGATION REPORT 🕵️\n")
            f.write(f"=" * 50 + "\n\n")
            f.write(f"Target: {results.get('target', 'Unknown')}\n")
            f.write(f"Scan Date: {results.get('scan_timestamp', 'Unknown')}\n")
            f.write(f"Duration: {results.get('scan_duration', 0):.2f} seconds\n\n")
            
            summary = results.get("summary", {})
            f.write(f"📊 SUMMARY STATISTICS:\n")
            f.write(f"Instagram References Found: {summary.get('total_instagram_references', 0)}\n")
            f.write(f"Social Profiles Found: {summary.get('total_social_profiles_found', 0)}\n")
            f.write(f"Search Results Found: {summary.get('total_search_results', 0)}\n")
            f.write(f"Confidence Score: {summary.get('confidence_score', 0)}%\n\n")
            
            # Instagram References
            instagram_refs = results.get("search_engine_results", {}).get("instagram_references", [])
            if instagram_refs:
                f.write(f"📷 INSTAGRAM REFERENCES:\n")
                for i, ref in enumerate(instagram_refs[:10], 1):
                    f.write(f"{i}. {ref.get('title', 'No Title')}\n")
                    f.write(f"   URL: {ref.get('url', 'No URL')}\n")
                    f.write(f"   Engine: {ref.get('engine', 'Unknown')}\n\n")
                    
            # Social Profiles
            social_profiles = results.get("cross_platform_results", {}).get("found_profiles", [])
            if social_profiles:
                f.write(f"👥 SOCIAL MEDIA PROFILES FOUND:\n")
                for i, profile in enumerate(social_profiles, 1):
                    f.write(f"{i}. Platform: {profile.get('platform', 'Unknown').upper()}\n")
                    f.write(f"   Username: {profile.get('username', 'Unknown')}\n")
                    f.write(f"   URL: {profile.get('url', 'No URL')}\n")
                    f.write(f"   Confidence: {profile.get('confidence', 'Unknown')}\n\n")
                    
        print(f"💾 OSINT Results saved to: {filename}")
        print(f"📋 Summary report saved to: {summary_file}")
        
        return filename, summary_file
        
    async def close(self):
        """ปิด Session"""
        if self.session:
            await self.session.close()
            print("🕵️ OSINT Session ปิดแล้ว!")

# === TESTING FUNCTION ===
async def test_osint_toolkit():
    """ทดสอบ OSINT Toolkit"""
    osint = AdvancedInstagramOSINT()
    
    try:
        await osint.initialize_session()
        
        # ทดสอบกับ target
        target = "whatilove1728"
        results = await osint.comprehensive_osint_scan(target)
        
        # บันทึกผลลัพธ์
        files = await osint.save_osint_results(results)
        
        print(f"\n🎉 OSINT Investigation Complete!")
        print(f"📁 Files created: {files}")
        
        return results
        
    finally:
        await osint.close()

if __name__ == "__main__":
    print("🕵️💀 Advanced Instagram OSINT Toolkit 2025 💀🕵️")
    print("Deep Social Media Investigation & Analysis\n")
    
    # รัน Test
    asyncio.run(test_osint_toolkit())
