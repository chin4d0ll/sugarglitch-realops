#!/usr/bin/env python3
"""
📦 ติดตั้ง libraries ที่จำเป็น
รันคำสั่งนี้ใน terminal ก่อนนะคะ:

pip install aiohttp asyncio psutil fake-useragent requests
"""

import asyncio          # สำหรับ async programming
import aiohttp          # สำหรับ HTTP requests แบบ async
import random           # สำหรับสุ่มค่าต่างๆ
import time             # สำหรับจับเวลา
import gc               # สำหรับจัดการ memory
import psutil           # สำหรับเช็ค RAM/CPU
from itertools import cycle  # สำหรับหมุนใช้ list
import requests         # สำหรับ HTTP requests แบบธรรมดา
from fake_useragent import UserAgent  # สำหรับ fake user agent
import json             # สำหรับจัดการ JSON data
from datetime import datetime, timedelta  # สำหรับจัดการเวลา
from concurrent.futures import ThreadPoolExecutor  # สำหรับ parallel processing

def setup_environment():
    """ตรวจสอบและแสดงข้อมูลสภาพแวดล้อม"""
    print("📦 Libraries โหลดเสร็จแล้ว!")
    print(f"🕐 เวลาปัจจุบัน: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👋 สวัสดีคุณ chin4d0ll!")
    
    # ตรวจสอบ memory
    memory = psutil.virtual_memory()
    print(f"💾 Memory: {memory.percent:.1f}% ใช้แล้ว, เหลือ {memory.available/(1024**3):.2f} GB")
    
    # ตรวจสอบ CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"🖥️ CPU: {cpu_percent:.1f}% ใช้งาน")
    
    print("✅ ระบบพร้อมใช้งาน Advanced Arsenal!")

if __name__ == "__main__":
    setup_environment()
