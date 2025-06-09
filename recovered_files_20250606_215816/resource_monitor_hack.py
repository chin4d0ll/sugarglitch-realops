# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import os
import time
import subprocess
import threading

def get_cpu_mem_hack():
    """
    แฮกดู CPU และ Memory แบบ low-level, OS-agnostic (Linux-centric),
    เน้นเร็วสุดๆ ไม่ใช้ lib ใหญ่ๆ
    """
    # ใช้ shell command แบบแฮกๆ ช่วยรีดข้อมูล
    cpu = subprocess.getoutput("grep 'cpu ' /proc/stat")
    mem = subprocess.getoutput("free | grep Mem")

    # CPU: คำนวณ % การใช้งานแบบแฮก
    cpu_fields = list(map(int, cpu.strip().split()[1:]))
    idle1, total1 = cpu_fields[3], sum(cpu_fields)
    time.sleep(0.1) # รอเพื่อจับ delta
    cpu2 = subprocess.getoutput("grep 'cpu ' /proc/stat")
    cpu_fields2 = list(map(int, cpu2.strip().split()[1:]))
    idle2, total2 = cpu_fields2[3], sum(cpu_fields2)
    cpu_usage = 100.0 * (1 - (idle2 - idle1) / (total2 - total1 + 0.1))

    # Memory: แฮกดู usage
    mem_fields = list(map(int, mem.strip().split()[1:]))
    mem_total, mem_used = mem_fields[0], mem_fields[1]
    mem_usage = 100.0 * mem_used / (mem_total + 0.1)

    return cpu_usage, mem_usage

def monitor(interval=1.0):
    """
    แสดงผล resource ทุก ๆ interval วินาที (default: 1 วิ)
    """
    print("เริ่มการ monitor แบบ hacky! (Ctrl+C เพื่อหยุด)")
    try:
        while True:
            cpu, mem = get_cpu_mem_hack()
            print(f"💻 CPU Usage: {cpu:.2f}% | 🧠 Memory Usage: {mem:.2f}%")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("จบการ monitor แล้วค่ะ")

if __name__ == "__main__":
    monitor(0.5)