#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Environment Test Script
ทดสอบการติดตั้ง libraries และ environment
"""

import sys
import subprocess
import importlib
import os

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def test_import(module_name, display_name=None):
    """ทดสอบการ import module"""
    if display_name is None:
        display_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"{Colors.GREEN}✅ {display_name} - OK{Colors.END}")
        return True
    except ImportError as e:
        print(f"{Colors.RED}❌ {display_name} - FAILED: {e}{Colors.END}")
        return False

def main():
    print(f"{Colors.BLUE}{Colors.BOLD}🔧 ENVIRONMENT TEST REPORT{Colors.END}")
    print("=" * 50)
    
    # Python version
    print(f"🐍 Python Version: {sys.version}")
    print(f"📍 Python Path: {sys.executable}")
    print(f"📂 Working Directory: {os.getcwd()}")
    print()
    
    # Test basic libraries
    print("📦 Testing Basic Libraries:")
    basic_libs = [
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("json", "JSON"),
        ("re", "Regular Expressions"),
        ("datetime", "DateTime"),
        ("time", "Time"),
        ("random", "Random"),
        ("os", "OS"),
        ("sys", "System")
    ]
    
    basic_success = 0
    for module, name in basic_libs:
        if test_import(module, name):
            basic_success += 1
    
    print()
    print("🌐 Testing Web Scraping Libraries:")
    web_libs = [
        ("selenium", "Selenium"),
        ("cloudscraper", "CloudScraper"), 
        ("fake_useragent", "Fake UserAgent")
    ]
    
    web_success = 0
    for module, name in web_libs:
        if test_import(module, name):
            web_success += 1
    
    print()
    print("📱 Testing Telegram Libraries:")
    telegram_libs = [
        ("telethon", "Telethon"),
        ("pyrogram", "Pyrogram"),
        ("asyncio", "AsyncIO"),
        ("aiohttp", "AioHTTP")
    ]
    
    telegram_success = 0
    for module, name in telegram_libs:
        if test_import(module, name):
            telegram_success += 1
    
    print()
    print("📊 SUMMARY:")
    print("=" * 30)
    print(f"Basic Libraries: {basic_success}/{len(basic_libs)}")
    print(f"Web Libraries: {web_success}/{len(web_libs)}")
    print(f"Telegram Libraries: {telegram_success}/{len(telegram_libs)}")
    
    total_success = basic_success + web_success + telegram_success
    total_libs = len(basic_libs) + len(web_libs) + len(telegram_libs)
    
    if total_success == total_libs:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! Environment ready for operations!{Colors.END}")
        return True
    else:
        print(f"{Colors.YELLOW}⚠️ {total_libs - total_success} libraries failed. Some features may not work.{Colors.END}")
        return False

if __name__ == "__main__":
    main()
