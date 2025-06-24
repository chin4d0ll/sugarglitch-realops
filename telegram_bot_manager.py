#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 Telegram Bot Manager & Control Panel
ระบบจัดการ Telegram bots หลายตัวพร้อมกัน

✨ Features:
- จัดการหลาย Telegram sessions
- Control panel สำหรับควบคุม bots
- ตรวจสอบสถานะและสถิติ
- Auto restart เมื่อ bot crash
- บันทึก logs แยกตาม bot
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional
import signal
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
import time

# สร้าง console สำหรับ rich
console = Console()

class TelegramBotManager:
    def __init__(self, config_file='bot_config.json'):
        """
        Bot Manager สำหรับจัดการ Telegram bots
        
        Args:
            config_file (str): ไฟล์ config สำหรับ bots
        """
        self.config_file = config_file
        self.bots = {}  # เก็บข้อมูล bots
        self.processes = {}  # เก็บ process ของแต่ละ bot
        self.stats = {
            'total_bots': 0,
            'running_bots': 0,
            'crashed_bots': 0,
            'total_uptime': 0,
            'last_update': datetime.now()
        }
        self.is_monitoring = False
        
        # ตั้งค่า logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BotManager')
        
        # โหลด config
        self.load_config()
        
        # จัดการ signal สำหรับ graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """จัดการ signal สำหรับหยุดการทำงาน"""
        console.print("\n[yellow]กำลังหยุดการทำงาน...[/yellow]")
        asyncio.create_task(self.stop_all_bots())
        sys.exit(0)
    
    def load_config(self):
        """โหลด configuration จากไฟล์"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.bots = config.get('bots', {})
                    self.logger.info(f"โหลด config แล้ว: {len(self.bots)} bots")
            else:
                self.create_default_config()
        except Exception as e:
            self.logger.error(f"โหลด config ไม่ได้: {e}")
            self.create_default_config()
    
    def create_default_config(self):
        """สร้าง config เริ่มต้น"""
        default_config = {
            "bots": {
                "bomber": {
                    "name": "Message Bomber",
                    "script": "telegram_bomber.py",
                    "description": "ส่งข้อความแบบต่อเนื่อง",
                    "auto_restart": True,
                    "restart_delay": 30,
                    "max_restarts": 5,
                    "enabled": False
                },
                "scraper": {
                    "name": "Member Scraper", 
                    "script": "telegram_scraper.py",
                    "description": "ดึงข้อมูลสมาชิกกลุ่ม",
                    "auto_restart": True,
                    "restart_delay": 60,
                    "max_restarts": 3,
                    "enabled": False
                },
                "forwarder": {
                    "name": "Auto Forwarder",
                    "script": "telegram_forwarder.py", 
                    "description": "Forward ข้อความอัตโนมัติ",
                    "auto_restart": True,
                    "restart_delay": 10,
                    "max_restarts": 10,
                    "enabled": True
                }
            },
            "global_settings": {
                "log_level": "INFO",
                "max_log_size": "10MB",
                "backup_logs": True,
                "monitoring_interval": 5
            }
        }
        
        self.bots = default_config['bots']
        self.save_config()
        console.print("[green]สร้าง config เริ่มต้นแล้ว[/green]")
    
    def save_config(self):
        """บันทึก configuration"""
        try:
            config = {
                'bots': self.bots,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
            self.logger.info("บันทึก config แล้ว")
            
        except Exception as e:
            self.logger.error(f"บันทึก config ไม่ได้: {e}")
    
    def add_bot(self, bot_id: str, name: str, script: str, description: str = "", **options):
        """เพิ่ม bot ใหม่"""
        self.bots[bot_id] = {
            'name': name,
            'script': script,
            'description': description,
            'auto_restart': options.get('auto_restart', True),
            'restart_delay': options.get('restart_delay', 30),
            'max_restarts': options.get('max_restarts', 5),
            'enabled': options.get('enabled', False),
            'restart_count': 0,
            'last_started': None,
            'last_stopped': None,
            'total_runtime': 0
        }
        
        self.save_config()
        console.print(f"[green]เพิ่ม bot '{name}' แล้ว[/green]")
    
    def remove_bot(self, bot_id: str):
        """ลบ bot"""
        if bot_id in self.bots:
            # หยุด bot ก่อนลบ
            if bot_id in self.processes:
                asyncio.create_task(self.stop_bot(bot_id))
            
            del self.bots[bot_id]
            self.save_config()
            console.print(f"[red]ลบ bot '{bot_id}' แล้ว[/red]")
        else:
            console.print(f"[yellow]ไม่พบ bot '{bot_id}'[/yellow]")
    
    async def start_bot(self, bot_id: str) -> bool:
        """เริ่ม bot"""
        if bot_id not in self.bots:
            console.print(f"[red]ไม่พบ bot '{bot_id}'[/red]")
            return False
        
        bot = self.bots[bot_id]
        
        # ตรวจสอบว่า bot กำลังทำงานอยู่หรือไม่
        if bot_id in self.processes:
            if self.processes[bot_id].poll() is None:
                console.print(f"[yellow]Bot '{bot['name']}' กำลังทำงานอยู่แล้ว[/yellow]")
                return True
            else:
                # Process หยุดแล้ว ลบออกจาก dict
                del self.processes[bot_id]
        
        try:
            # ตรวจสอบว่าไฟล์ script มีอยู่หรือไม่
            if not os.path.exists(bot['script']):
                console.print(f"[red]ไม่พบไฟล์ {bot['script']}[/red]")
                return False
            
            # เริ่ม process
            process = subprocess.Popen(
                [sys.executable, bot['script']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes[bot_id] = process
            bot['last_started'] = datetime.now().isoformat()
            bot['restart_count'] = 0
            
            console.print(f"[green]เริ่ม bot '{bot['name']}' แล้ว (PID: {process.pid})[/green]")
            self.logger.info(f"Started bot {bot_id} with PID {process.pid}")
            
            return True
            
        except Exception as e:
            console.print(f"[red]เริ่ม bot '{bot['name']}' ไม่ได้: {e}[/red]")
            self.logger.error(f"Failed to start bot {bot_id}: {e}")
            return False
    
    async def stop_bot(self, bot_id: str) -> bool:
        """หยุด bot"""
        if bot_id not in self.processes:
            console.print(f"[yellow]Bot '{bot_id}' ไม่ได้ทำงานอยู่[/yellow]")
            return True
        
        try:
            process = self.processes[bot_id]
            bot = self.bots[bot_id]
            
            # ส่ง SIGTERM ก่อน
            process.terminate()
            
            # รอ 5 วินาที
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # ถ้ายังไม่หยุด ใช้ SIGKILL
                process.kill()
                process.wait()
            
            # คำนวณ runtime
            if bot.get('last_started'):
                start_time = datetime.fromisoformat(bot['last_started'])
                runtime = (datetime.now() - start_time).total_seconds()
                bot['total_runtime'] = bot.get('total_runtime', 0) + runtime
            
            bot['last_stopped'] = datetime.now().isoformat()
            del self.processes[bot_id]
            
            console.print(f"[red]หยุด bot '{bot['name']}' แล้ว[/red]")
            self.logger.info(f"Stopped bot {bot_id}")
            
            return True
            
        except Exception as e:
            console.print(f"[red]หยุด bot '{bot_id}' ไม่ได้: {e}[/red]")
            self.logger.error(f"Failed to stop bot {bot_id}: {e}")
            return False
    
    async def restart_bot(self, bot_id: str) -> bool:
        """เริ่ม bot ใหม่"""
        console.print(f"[yellow]กำลัง restart bot '{bot_id}'...[/yellow]")
        
        # หยุดก่อน
        await self.stop_bot(bot_id)
        
        # รอสักครู่
        await asyncio.sleep(2)
        
        # เริ่มใหม่
        return await self.start_bot(bot_id)
    
    async def start_all_bots(self):
        """เริ่ม bots ทั้งหมดที่ enabled"""
        console.print("[blue]กำลังเริ่ม bots ทั้งหมด...[/blue]")
        
        for bot_id, bot in self.bots.items():
            if bot.get('enabled', False):
                await self.start_bot(bot_id)
                await asyncio.sleep(1)  # หน่วงเล็กน้อยระหว่าง bot
    
    async def stop_all_bots(self):
        """หยุด bots ทั้งหมด"""
        console.print("[red]กำลังหยุด bots ทั้งหมด...[/red]")
        
        for bot_id in list(self.processes.keys()):
            await self.stop_bot(bot_id)
    
    def get_bot_status(self, bot_id: str) -> str:
        """ดูสถานะ bot"""
        if bot_id not in self.bots:
            return "ไม่พบ"
        
        if bot_id not in self.processes:
            return "หยุด"
        
        process = self.processes[bot_id]
        if process.poll() is None:
            return "ทำงาน"
        else:
            return "crash"
    
    def get_bot_info(self, bot_id: str) -> Dict:
        """ดูข้อมูล bot"""
        if bot_id not in self.bots:
            return {}
        
        bot = self.bots[bot_id].copy()
        bot['status'] = self.get_bot_status(bot_id)
        
        if bot_id in self.processes:
            process = self.processes[bot_id]
            bot['pid'] = process.pid
            
            # ดูการใช้ทรัพยากร
            try:
                p = psutil.Process(process.pid)
                bot['cpu_percent'] = p.cpu_percent()
                bot['memory_mb'] = p.memory_info().rss / 1024 / 1024
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                bot['cpu_percent'] = 0
                bot['memory_mb'] = 0
        
        return bot
    
    async def monitor_bots(self):
        """ตรวจสอบและ auto restart bots"""
        self.is_monitoring = True
        console.print("[blue]เริ่มการตรวจสอบ bots...[/blue]")
        
        while self.is_monitoring:
            try:
                for bot_id, bot in self.bots.items():
                    if not bot.get('enabled', False):
                        continue
                    
                    status = self.get_bot_status(bot_id)
                    
                    # ถ้า bot crash และมี auto_restart
                    if status == "crash" and bot.get('auto_restart', False):
                        restart_count = bot.get('restart_count', 0)
                        max_restarts = bot.get('max_restarts', 5)
                        
                        if restart_count < max_restarts:
                            console.print(f"[yellow]Bot '{bot['name']}' crash, กำลัง restart... ({restart_count+1}/{max_restarts})[/yellow]")
                            
                            # รอตาม restart_delay
                            delay = bot.get('restart_delay', 30)
                            await asyncio.sleep(delay)
                            
                            # restart
                            if await self.restart_bot(bot_id):
                                bot['restart_count'] = restart_count + 1
                            
                        else:
                            console.print(f"[red]Bot '{bot['name']}' restart เกินขีดจำกัดแล้ว[/red]")
                            bot['enabled'] = False
                            self.save_config()
                
                # อัพเดท stats
                self._update_stats()
                
                # รอก่อนตรวจสอบรอบถัดไป
                await asyncio.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Monitor error: {e}")
                await asyncio.sleep(10)
    
    def _update_stats(self):
        """อัพเดทสถิติ"""
        self.stats['total_bots'] = len(self.bots)
        self.stats['running_bots'] = sum(1 for bot_id in self.bots if self.get_bot_status(bot_id) == "ทำงาน")
        self.stats['crashed_bots'] = sum(1 for bot_id in self.bots if self.get_bot_status(bot_id) == "crash")
        self.stats['last_update'] = datetime.now()
    
    def create_status_table(self) -> Table:
        """สร้างตาราง status สำหรับแสดงผล"""
        table = Table(title="🤖 Telegram Bot Manager Status")
        
        table.add_column("Bot ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("PID", style="yellow")
        table.add_column("CPU %", style="blue")
        table.add_column("Memory MB", style="red")
        table.add_column("Restarts", style="white")
        
        for bot_id, bot in self.bots.items():
            info = self.get_bot_info(bot_id)
            
            # สีตาม status
            if info['status'] == "ทำงาน":
                status_color = "[green]🟢 ทำงาน[/green]"
            elif info['status'] == "crash":
                status_color = "[red]🔴 crash[/red]"
            else:
                status_color = "[gray]⚫ หยุด[/gray]"
            
            table.add_row(
                bot_id,
                info.get('name', ''),
                status_color,
                str(info.get('pid', '-')),
                f"{info.get('cpu_percent', 0):.1f}",
                f"{info.get('memory_mb', 0):.1f}",
                str(info.get('restart_count', 0))
            )
        
        return table
    
    async def run_dashboard(self):
        """เรียก dashboard แบบ real-time"""
        console.print("[blue]กำลังเริ่ม Real-time Dashboard...[/blue]")
        
        # เริ่ม monitoring ใน background
        monitor_task = asyncio.create_task(self.monitor_bots())
        
        try:
            with Live(self.create_status_table(), refresh_per_second=1) as live:
                while True:
                    live.update(self.create_status_table())
                    await asyncio.sleep(1)
                    
        except KeyboardInterrupt:
            console.print("\n[yellow]หยุด dashboard...[/yellow]")
        finally:
            self.is_monitoring = False
            monitor_task.cancel()
    
    def show_help(self):
        """แสดงคำสั่งที่ใช้ได้"""
        help_text = """
🎮 Telegram Bot Manager Commands:

📊 ดูสถานะ:
  status                 - แสดงสถานะ bots ทั้งหมด
  info <bot_id>         - ดูข้อมูลละเอียด bot
  dashboard             - เปิด real-time dashboard

🚀 ควบคุม bots:
  start <bot_id>        - เริ่ม bot
  stop <bot_id>         - หยุด bot  
  restart <bot_id>      - restart bot
  start-all             - เริ่ม bots ทั้งหมด
  stop-all              - หยุด bots ทั้งหมด

⚙️ จัดการ:
  add <id> <name> <script> - เพิ่ม bot ใหม่
  remove <bot_id>       - ลบ bot
  enable <bot_id>       - เปิดใช้ bot
  disable <bot_id>      - ปิดใช้ bot

📁 ไฟล์:
  save                  - บันทึก config
  reload                - โหลด config ใหม่
  
❓ อื่นๆ:
  help                  - แสดงความช่วยเหลือ
  quit/exit             - ออกจากโปรแกรม
        """
        console.print(help_text)

# Interactive CLI
async def interactive_cli():
    """CLI แบบ interactive สำหรับจัดการ bots"""
    manager = TelegramBotManager()
    
    console.print(Panel.fit("🎮 Telegram Bot Manager", style="bold blue"))
    console.print("พิมพ์ 'help' เพื่อดูคำสั่งที่ใช้ได้")
    
    while True:
        try:
            command = console.input("\n[bold cyan]bot-manager>[/bold cyan] ").strip().lower()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0]
            
            if cmd in ['quit', 'exit', 'q']:
                await manager.stop_all_bots()
                console.print("[green]ขอบคุณที่ใช้งาน![/green]")
                break
            
            elif cmd == 'help':
                manager.show_help()
            
            elif cmd == 'status':
                console.print(manager.create_status_table())
            
            elif cmd == 'dashboard':
                await manager.run_dashboard()
            
            elif cmd == 'start':
                if len(parts) > 1:
                    await manager.start_bot(parts[1])
                else:
                    console.print("[red]ใส่ bot_id ด้วย: start <bot_id>[/red]")
            
            elif cmd == 'stop':
                if len(parts) > 1:
                    await manager.stop_bot(parts[1])
                else:
                    console.print("[red]ใส่ bot_id ด้วย: stop <bot_id>[/red]")
            
            elif cmd == 'restart':
                if len(parts) > 1:
                    await manager.restart_bot(parts[1])
                else:
                    console.print("[red]ใส่ bot_id ด้วย: restart <bot_id>[/red]")
            
            elif cmd == 'start-all':
                await manager.start_all_bots()
            
            elif cmd == 'stop-all':
                await manager.stop_all_bots()
            
            elif cmd == 'info':
                if len(parts) > 1:
                    info = manager.get_bot_info(parts[1])
                    if info:
                        table = Table(title=f"ข้อมูล Bot: {parts[1]}")
                        table.add_column("Property", style="cyan")
                        table.add_column("Value", style="white")
                        
                        for key, value in info.items():
                            table.add_row(str(key), str(value))
                        
                        console.print(table)
                    else:
                        console.print(f"[red]ไม่พบ bot '{parts[1]}'[/red]")
                else:
                    console.print("[red]ใส่ bot_id ด้วย: info <bot_id>[/red]")
            
            elif cmd == 'add':
                if len(parts) >= 4:
                    manager.add_bot(parts[1], parts[2], parts[3])
                else:
                    console.print("[red]ใช้: add <bot_id> <name> <script>[/red]")
            
            elif cmd == 'remove':
                if len(parts) > 1:
                    manager.remove_bot(parts[1])
                else:
                    console.print("[red]ใส่ bot_id ด้วย: remove <bot_id>[/red]")
            
            elif cmd == 'enable':
                if len(parts) > 1 and parts[1] in manager.bots:
                    manager.bots[parts[1]]['enabled'] = True
                    manager.save_config()
                    console.print(f"[green]เปิดใช้ bot '{parts[1]}' แล้ว[/green]")
                else:
                    console.print("[red]ใส่ bot_id ที่ถูกต้อง[/red]")
            
            elif cmd == 'disable':
                if len(parts) > 1 and parts[1] in manager.bots:
                    manager.bots[parts[1]]['enabled'] = False
                    await manager.stop_bot(parts[1])
                    manager.save_config()
                    console.print(f"[red]ปิดใช้ bot '{parts[1]}' แล้ว[/red]")
                else:
                    console.print("[red]ใส่ bot_id ที่ถูกต้อง[/red]")
            
            elif cmd == 'save':
                manager.save_config()
                console.print("[green]บันทึก config แล้ว[/green]")
            
            elif cmd == 'reload':
                manager.load_config()
                console.print("[green]โหลด config ใหม่แล้ว[/green]")
            
            else:
                console.print(f"[red]ไม่รู้จักคำสั่ง '{cmd}' พิมพ์ 'help' เพื่อดูคำสั่งที่ใช้ได้[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]กด Ctrl+C อีกครั้งเพื่อออก หรือพิมพ์ 'quit'[/yellow]")
        except Exception as e:
            console.print(f"[red]เกิดข้อผิดพลาด: {e}[/red]")

# รันโปรแกรม
if __name__ == "__main__":
    try:
        asyncio.run(interactive_cli())
    except KeyboardInterrupt:
        console.print("\n[green]ขอบคุณที่ใช้งาน Bot Manager![/green]")
    except Exception as e:
        console.print(f"[red]เกิดข้อผิดพลาด: {e}[/red]")
