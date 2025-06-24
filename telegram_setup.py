#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 Telegram Setup & Configuration Tool
เครื่องมือตั้งค่าและกำหนดค่า Telegram automation อย่างละเอียด

✨ Features:
- ตั้งค่า API credentials
- ทดสอบการเชื่อมต่อ
- สร้าง session files
- ตรวจสอบ permissions
- Export/Import configurations
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import PhoneNumberInvalidError, ApiIdInvalidError
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging

console = Console()

class TelegramSetup:
    def __init__(self):
        """ตั้งค่าเริ่มต้นสำหรับ Telegram Setup"""
        self.config = {}
        self.config_file = 'telegram_config.json'
        self.session_dir = 'telegram_sessions'
        
        # สร้างโฟลเดอร์สำหรับ sessions
        Path(self.session_dir).mkdir(exist_ok=True)
        
        # ปิด logging ของ telethon
        logging.getLogger('telethon').setLevel(logging.WARNING)
    
    def load_config(self):
        """โหลด configuration ที่มีอยู่"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                return True
        except Exception as e:
            console.print(f"[red]โหลด config ไม่ได้: {e}[/red]")
        return False
    
    def save_config(self):
        """บันทึก configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            console.print(f"[red]บันทึก config ไม่ได้: {e}[/red]")
            return False
    
    def get_api_credentials(self):
        """รับ API credentials จากผู้ใช้"""
        console.print(Panel.fit(
            "[bold blue]🔑 ตั้งค่า Telegram API Credentials[/bold blue]\n\n"
            "1. ไปที่ https://my.telegram.org\n"
            "2. ล็อกอินด้วยเบอร์โทรของคุณ\n"
            "3. ไป 'API Development tools'\n"
            "4. สร้าง app ใหม่หรือใช้ที่มีอยู่\n"
            "5. คัดลอก API ID และ API Hash",
            title="📋 วิธีรับ API Credentials"
        ))
        
        # ถ้ามี config เก่า แสดงให้ดู
        if 'api_id' in self.config:
            console.print(f"\n[yellow]พบ API ID เก่า: {self.config['api_id']}[/yellow]")
            if not Confirm.ask("ต้องการใช้ API ID เก่าไหม?"):
                self.config.pop('api_id', None)
                self.config.pop('api_hash', None)
        
        # รับ API ID
        if 'api_id' not in self.config:
            while True:
                api_id = Prompt.ask("\n[cyan]ใส่ API ID")
                try:
                    api_id = int(api_id)
                    self.config['api_id'] = api_id
                    break
                except ValueError:
                    console.print("[red]API ID ต้องเป็นตัวเลขเท่านั้น[/red]")
        
        # รับ API Hash
        if 'api_hash' not in self.config:
            api_hash = Prompt.ask("[cyan]ใส่ API Hash", password=True)
            self.config['api_hash'] = api_hash
        
        console.print("[green]✅ ตั้งค่า API Credentials เรียบร้อย[/green]")
        return True
    
    def get_phone_numbers(self):
        """รับเบอร์โทรสำหรับ accounts"""
        console.print(Panel.fit(
            "[bold blue]📱 ตั้งค่าเบอร์โทรศัพท์[/bold blue]\n\n"
            "ใส่เบอร์โทรศัพท์ที่ลงทะเบียน Telegram แล้ว\n"
            "รูปแบบ: +66812345678 (ใส่รหัสประเทศด้วย)",
            title="📞 Phone Numbers"
        ))
        
        accounts = self.config.get('accounts', {})
        
        # แสดง accounts ที่มีอยู่
        if accounts:
            console.print("\n[yellow]📋 Accounts ที่มีอยู่:[/yellow]")
            table = Table()
            table.add_column("ชื่อ", style="cyan")
            table.add_column("เบอร์โทร", style="white")
            table.add_column("สถานะ", style="green")
            
            for name, info in accounts.items():
                status = "✅ พร้อมใช้" if info.get('session_exists') else "❌ ยังไม่ล็อกอิน"
                table.add_row(name, info.get('phone', ''), status)
            
            console.print(table)
        
        # เพิ่ม account ใหม่
        while True:
            if not Confirm.ask("\nต้องการเพิ่มเบอร์โทรใหม่ไหม?"):
                break
            
            name = Prompt.ask("[cyan]ชื่อ account (เช่น main, backup)")
            
            if name in accounts:
                if not Confirm.ask(f"Account '{name}' มีอยู่แล้ว ต้องการแทนที่ไหม?"):
                    continue
            
            phone = Prompt.ask("[cyan]เบอร์โทรศัพท์ (เช่น +66812345678)")
            
            # ตรวจสอบรูปแบบเบอร์โทร
            if not phone.startswith('+'):
                console.print("[red]เบอร์โทรต้องขึ้นต้นด้วย + และรหัสประเทศ[/red]")
                continue
            
            accounts[name] = {
                'phone': phone,
                'session_exists': False,
                'last_login': None
            }
            
            console.print(f"[green]✅ เพิ่มเบอร์ {phone} ในชื่อ '{name}' แล้ว[/green]")
        
        self.config['accounts'] = accounts
        
        if not accounts:
            console.print("[red]❌ ต้องมีอย่างน้อย 1 เบอร์โทร[/red]")
            return False
        
        return True
    
    async def test_connection(self, account_name):
        """ทดสอบการเชื่อมต่อและสร้าง session"""
        if account_name not in self.config.get('accounts', {}):
            console.print(f"[red]ไม่พบ account '{account_name}'[/red]")
            return False
        
        account = self.config['accounts'][account_name]
        api_id = self.config['api_id']
        api_hash = self.config['api_hash']
        phone = account['phone']
        
        session_file = os.path.join(self.session_dir, f"{account_name}_session")
        
        console.print(f"\n[blue]🔗 กำลังทดสอบการเชื่อมต่อสำหรับ {account_name}...[/blue]")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("กำลังเชื่อมต่อ...", total=None)
                
                client = TelegramClient(session_file, api_id, api_hash)
                
                try:
                    await client.start(phone=phone)
                    progress.update(task, description="เชื่อมต่อสำเร็จ!")
                    
                    # ดึงข้อมูลผู้ใช้
                    me = await client.get_me()
                    
                    console.print(f"[green]✅ เชื่อมต่อสำเร็จ![/green]")
                    console.print(f"[cyan]👤 ชื่อ: {me.first_name} {me.last_name or ''}[/cyan]")
                    console.print(f"[cyan]🆔 Username: @{me.username or 'ไม่มี'}[/cyan]")
                    console.print(f"[cyan]📞 เบอร์: {me.phone}[/cyan]")
                    
                    # อัพเดทข้อมูล account
                    account['session_exists'] = True
                    account['last_login'] = datetime.now().isoformat()
                    account['user_info'] = {
                        'id': me.id,
                        'first_name': me.first_name,
                        'last_name': me.last_name,
                        'username': me.username,
                        'phone': me.phone
                    }
                    
                    return True
                    
                except PhoneNumberInvalidError:
                    console.print("[red]❌ เบอร์โทรไม่ถูกต้อง[/red]")
                except ApiIdInvalidError:
                    console.print("[red]❌ API ID หรือ API Hash ไม่ถูกต้อง[/red]")
                except Exception as e:
                    console.print(f"[red]❌ เชื่อมต่อไม่ได้: {e}[/red]")
                finally:
                    await client.disconnect()
                    
        except Exception as e:
            console.print(f"[red]❌ เกิดข้อผิดพลาด: {e}[/red]")
            
        return False
    
    async def test_all_connections(self):
        """ทดสอบการเชื่อมต่อทุก account"""
        accounts = self.config.get('accounts', {})
        
        if not accounts:
            console.print("[red]❌ ไม่มี accounts ให้ทดสอบ[/red]")
            return False
        
        console.print(f"\n[blue]🧪 ทดสอบการเชื่อมต่อ {len(accounts)} accounts...[/blue]")
        
        results = {}
        for account_name in accounts:
            result = await self.test_connection(account_name)
            results[account_name] = result
            
            # หน่วงเวลาระหว่าง account
            if len(accounts) > 1:
                await asyncio.sleep(2)
        
        # แสดงผลรวม
        console.print(f"\n[bold]📊 ผลการทดสอบ:[/bold]")
        table = Table()
        table.add_column("Account", style="cyan")
        table.add_column("เบอร์โทร", style="white")
        table.add_column("สถานะ", style="green")
        
        for account_name, success in results.items():
            phone = accounts[account_name]['phone']
            status = "✅ สำเร็จ" if success else "❌ ไม่สำเร็จ"
            table.add_row(account_name, phone, status)
        
        console.print(table)
        
        successful = sum(1 for success in results.values() if success)
        console.print(f"\n[green]✅ ทดสอบสำเร็จ: {successful}/{len(accounts)} accounts[/green]")
        
        return successful > 0
    
    def check_permissions(self):
        """ตรวจสอบ permissions และไฟล์ที่จำเป็น"""
        console.print("\n[blue]🔍 ตรวจสอบ permissions และไฟล์...[/blue]")
        
        checks = []
        
        # ตรวจสอบการเขียนไฟล์
        try:
            test_file = 'test_write.tmp'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            checks.append(("เขียนไฟล์", True, "สามารถเขียนไฟล์ได้"))
        except Exception as e:
            checks.append(("เขียนไฟล์", False, f"ไม่สามารถเขียนไฟล์: {e}"))
        
        # ตรวจสอบโฟลเดอร์ sessions
        try:
            os.makedirs(self.session_dir, exist_ok=True)
            checks.append(("โฟลเดอร์ sessions", True, f"โฟลเดอร์ {self.session_dir} พร้อมใช้"))
        except Exception as e:
            checks.append(("โฟลเดอร์ sessions", False, f"สร้างโฟลเดอร์ไม่ได้: {e}"))
        
        # ตรวจสอบ Python version
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            checks.append(("Python version", True, f"Python {version.major}.{version.minor} รองรับ"))
        else:
            checks.append(("Python version", False, f"Python {version.major}.{version.minor} ต่ำเกินไป (ต้อง 3.7+)"))
        
        # ตรวจสอบ Telethon
        try:
            import telethon
            checks.append(("Telethon", True, f"Telethon {telethon.__version__} พร้อมใช้"))
        except ImportError:
            checks.append(("Telethon", False, "ติดตั้ง Telethon ด้วย: pip install telethon"))
        
        # แสดงผล
        table = Table(title="🔍 System Checks")
        table.add_column("รายการ", style="cyan")
        table.add_column("สถานะ", style="white")
        table.add_column("รายละเอียด", style="gray")
        
        all_passed = True
        for check_name, passed, detail in checks:
            status = "✅ ผ่าน" if passed else "❌ ไม่ผ่าน"
            if not passed:
                all_passed = False
            table.add_row(check_name, status, detail)
        
        console.print(table)
        
        if all_passed:
            console.print("[green]✅ ตรวจสอบทุกรายการผ่านแล้ว![/green]")
        else:
            console.print("[red]❌ มีปัญหาบางรายการ กรุณาแก้ไขก่อนใช้งาน[/red]")
        
        return all_passed
    
    def generate_example_scripts(self):
        """สร้างไฟล์ตัวอย่างการใช้งาน"""
        console.print("\n[blue]📝 สร้างไฟล์ตัวอย่าง...[/blue]")
        
        examples_dir = 'telegram_examples'
        os.makedirs(examples_dir, exist_ok=True)
        
        # ตัวอย่าง 1: การส่งข้อความ
        example_send = '''#!/usr/bin/env python3
"""ตัวอย่างการส่งข้อความ"""
import asyncio
from telethon import TelegramClient

async def main():
    # โหลด config
    import json
    with open('telegram_config.json', 'r') as f:
        config = json.load(f)
    
    # เลือก account แรก
    account_name = list(config['accounts'].keys())[0]
    account = config['accounts'][account_name]
    
    # สร้าง client
    client = TelegramClient(
        f'telegram_sessions/{account_name}_session',
        config['api_id'],
        config['api_hash']
    )
    
    await client.start()
    
    # ส่งข้อความให้ตัวเอง
    await client.send_message('me', 'สวัสดีจาก Telegram Bot! 🚀')
    print("✅ ส่งข้อความแล้ว!")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        # ตัวอย่าง 2: การดึงข้อมูลกลุ่ม
        example_group = '''#!/usr/bin/env python3
"""ตัวอย่างการดึงข้อมูลกลุ่ม"""
import asyncio
from telethon import TelegramClient

async def main():
    # โหลด config
    import json
    with open('telegram_config.json', 'r') as f:
        config = json.load(f)
    
    account_name = list(config['accounts'].keys())[0]
    account = config['accounts'][account_name]
    
    client = TelegramClient(
        f'telegram_sessions/{account_name}_session',
        config['api_id'],
        config['api_hash']
    )
    
    await client.start()
    
    # ดึงรายการ dialogs (แชท/กลุ่มทั้งหมด)
    async for dialog in client.iter_dialogs():
        print(f"📂 {dialog.name} (ID: {dialog.id})")
        if dialog.is_group:
            print(f"   👥 กลุ่ม - สมาชิก: {dialog.entity.participants_count or 'ไม่ทราบ'}")
        elif dialog.is_channel:
            print(f"   📢 ช่อง")
        else:
            print(f"   👤 แชทส่วนตัว")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        # บันทึกไฟล์ตัวอย่าง
        examples = [
            ('send_message_example.py', example_send),
            ('list_groups_example.py', example_group)
        ]
        
        for filename, content in examples:
            filepath = os.path.join(examples_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            console.print(f"📝 สร้าง {filepath}")
        
        console.print(f"[green]✅ สร้างไฟล์ตัวอย่างใน {examples_dir}/ แล้ว[/green]")
    
    def export_config(self, filename=None):
        """Export configuration สำหรับ backup"""
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"telegram_config_backup_{timestamp}.json"
        
        try:
            # ลบข้อมูล sensitive ออก
            export_config = self.config.copy()
            if 'api_hash' in export_config:
                export_config['api_hash'] = '***HIDDEN***'
            
            for account in export_config.get('accounts', {}).values():
                if 'user_info' in account:
                    account['user_info'] = {k: v for k, v in account['user_info'].items() 
                                          if k not in ['phone', 'id']}
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_config, f, ensure_ascii=False, indent=2)
            
            console.print(f"[green]📤 Export config ไป {filename} แล้ว[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Export ไม่ได้: {e}[/red]")
            return False

# Interactive Setup
async def interactive_setup():
    """Setup แบบ interactive"""
    console.print(Panel.fit(
        "[bold blue]🚀 Telegram Automation Setup[/bold blue]\n\n"
        "ยินดีต้อนรับสู่เครื่องมือตั้งค่า Telegram automation!\n"
        "เครื่องมือนี้จะช่วยคุณตั้งค่าทุกอย่างให้พร้อมใช้งาน",
        title="🎉 Welcome"
    ))
    
    setup = TelegramSetup()
    
    # โหลด config เก่า
    has_existing = setup.load_config()
    if has_existing:
        console.print("[yellow]🔍 พบ configuration เก่า[/yellow]")
        if not Confirm.ask("ต้องการใช้ configuration เก่าไหม?"):
            setup.config = {}
    
    # ขั้นตอนที่ 1: ตรวจสอบระบบ
    console.print("\n[bold]📋 ขั้นตอนที่ 1: ตรวจสอบระบบ[/bold]")
    if not setup.check_permissions():
        if not Confirm.ask("พบปัญหาในระบบ ต้องการดำเนินการต่อไหม?"):
            return
    
    # ขั้นตอนที่ 2: ตั้งค่า API
    console.print("\n[bold]🔑 ขั้นตอนที่ 2: ตั้งค่า API Credentials[/bold]")
    if not setup.get_api_credentials():
        console.print("[red]❌ ตั้งค่า API ไม่สำเร็จ[/red]")
        return
    
    # ขั้นตอนที่ 3: ตั้งค่าเบอร์โทร
    console.print("\n[bold]📱 ขั้นตอนที่ 3: ตั้งค่าเบอร์โทรศัพท์[/bold]")
    if not setup.get_phone_numbers():
        console.print("[red]❌ ตั้งค่าเบอร์โทรไม่สำเร็จ[/red]")
        return
    
    # บันทึก config
    setup.save_config()
    
    # ขั้นตอนที่ 4: ทดสอบการเชื่อมต่อ
    console.print("\n[bold]🧪 ขั้นตอนที่ 4: ทดสอบการเชื่อมต่อ[/bold]")
    if Confirm.ask("ต้องการทดสอบการเชื่อมต่อเลยไหม?"):
        success = await setup.test_all_connections()
        if success:
            setup.save_config()
        else:
            console.print("[yellow]⚠️ การเชื่อมต่อมีปัญหา แต่ยังสามารถใช้งานได้[/yellow]")
    
    # ขั้นตอนที่ 5: สร้างไฟล์ตัวอย่าง
    console.print("\n[bold]📝 ขั้นตอนที่ 5: สร้างไฟล์ตัวอย่าง[/bold]")
    if Confirm.ask("ต้องการสร้างไฟล์ตัวอย่างการใช้งานไหม?"):
        setup.generate_example_scripts()
    
    # ขั้นตอนที่ 6: Backup
    if Confirm.ask("\nต้องการ backup configuration ไหม?"):
        setup.export_config()
    
    # สรุป
    console.print(Panel.fit(
        "[bold green]🎉 Setup เสร็จสิ้น![/bold green]\n\n"
        f"✅ API ID: {setup.config['api_id']}\n"
        f"✅ Accounts: {len(setup.config.get('accounts', {}))}\n"
        f"✅ Sessions: telegram_sessions/\n"
        f"✅ Config: {setup.config_file}\n\n"
        "[cyan]คุณสามารถเริ่มใช้งาน Telegram automation ได้แล้ว![/cyan]",
        title="🚀 Setup Complete"
    ))
    
    # แสดงคำสั่งถัดไป
    console.print("\n[bold]📋 คำสั่งที่แนะนำ:[/bold]")
    console.print("1. [cyan]python telegram_bomber.py[/cyan] - ส่งข้อความ")
    console.print("2. [cyan]python telegram_scraper.py[/cyan] - ดึงข้อมูลสมาชิก")
    console.print("3. [cyan]python telegram_forwarder.py[/cyan] - Forward ข้อความ")
    console.print("4. [cyan]python telegram_bot_manager.py[/cyan] - จัดการ bots")

# รันโปรแกรม
if __name__ == "__main__":
    try:
        asyncio.run(interactive_setup())
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️ ยกเลิกการ setup[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ เกิดข้อผิดพลาด: {e}[/red]")
