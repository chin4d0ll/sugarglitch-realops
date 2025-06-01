#!/usr/bin/env python3
"""
💀📱 Instagram DM Extractor - Simple GUI Version 💀📱
====================================================
เครื่องมือดึง DMs พร้อม GUI ใช้ง่าย
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import asyncio
import json
import threading
from datetime import datetime
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False

class InstagramDMExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💀📱 Instagram DM Extractor 💀📱")
        self.root.geometry("600x500")
        self.root.configure(bg='#1a1a1a')
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#ff69b4', background='#1a1a1a')
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#ffffff', background='#1a1a1a')
        self.style.configure('Info.TLabel', font=('Arial', 10), foreground='#cccccc', background='#1a1a1a')
        
        self.setup_ui()
        
        # Check if instagrapi is available
        if not INSTAGRAPI_AVAILABLE:
            messagebox.showerror("Error", "instagrapi not installed!\nPlease run: pip install instagrapi")
            
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title
        title_label = ttk.Label(self.root, text="💀📱 Instagram DM Extractor 💀📱", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Login section
        login_frame = ttk.LabelFrame(main_frame, text="🔐 Instagram Login", padding=10)
        login_frame.pack(fill='x', pady=5)
        
        ttk.Label(login_frame, text="Username:", style='Heading.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30, font=('Arial', 11))
        self.username_entry.grid(row=0, column=1, pady=5, padx=10, columnspan=2, sticky='ew')
        
        ttk.Label(login_frame, text="Password:", style='Heading.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        
        # Password frame for entry + show/hide button
        password_frame = ttk.Frame(login_frame)
        password_frame.grid(row=1, column=1, pady=5, padx=10, columnspan=2, sticky='ew')
        
        self.password_entry = ttk.Entry(password_frame, width=25, show='*', font=('Arial', 11))
        self.password_entry.pack(side='left', fill='x', expand=True)
        
        # Show/Hide password button
        self.show_password_var = tk.BooleanVar()
        self.show_password_btn = ttk.Button(password_frame, text="👁️", width=3, 
                                          command=self.toggle_password_visibility)
        self.show_password_btn.pack(side='right', padx=(5, 0))
        
        # Password strength indicator
        self.password_strength_var = tk.StringVar()
        self.password_strength_label = ttk.Label(login_frame, textvariable=self.password_strength_var, 
                                               font=('Arial', 9), foreground='#888888')
        self.password_strength_label.grid(row=2, column=1, sticky='w', padx=10)
        
        # Bind password entry to check strength
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Extraction Options", padding=10)
        options_frame.pack(fill='x', pady=5)
        
        ttk.Label(options_frame, text="Target User (optional):", style='Heading.TLabel').grid(row=0, column=0, sticky='w', pady=5)
        self.target_entry = ttk.Entry(options_frame, width=30)
        self.target_entry.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(options_frame, text="Max Conversations:", style='Heading.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.max_conv_var = tk.StringVar(value="20")
        max_conv_spin = ttk.Spinbox(options_frame, from_=1, to=100, textvariable=self.max_conv_var, width=10)
        max_conv_spin.grid(row=1, column=1, sticky='w', pady=5, padx=10)
        
        ttk.Label(options_frame, text="Messages per conversation:", style='Heading.TLabel').grid(row=2, column=0, sticky='w', pady=5)
        self.max_msg_var = tk.StringVar(value="100")
        max_msg_spin = ttk.Spinbox(options_frame, from_=10, to=1000, textvariable=self.max_msg_var, width=10)
        max_msg_spin.grid(row=2, column=1, sticky='w', pady=5, padx=10)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        self.extract_btn = ttk.Button(button_frame, text="🚀 Extract DMs", command=self.start_extraction)
        self.extract_btn.pack(side='left', padx=5)
        
        self.save_btn = ttk.Button(button_frame, text="💾 Save Results", command=self.save_results, state='disabled')
        self.save_btn.pack(side='left', padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ Clear Log", command=self.clear_log)
        self.clear_btn.pack(side='left', padx=5)
        
        self.help_btn = ttk.Button(button_frame, text="❓ ช่วยเหลือ", command=self.show_help)
        self.help_btn.pack(side='left', padx=5)
        
        self.test_btn = ttk.Button(button_frame, text="🧪 ทดสอบการเชื่อมต่อ", command=self.test_connection)
        self.test_btn.pack(side='left', padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="📝 Extraction Log", padding=5)
        log_frame.pack(fill='both', expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, height=15, bg='#2d2d2d', fg='#ffffff', font=('Consolas', 9))
        log_scroll = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scroll.pack(side='right', fill='y')
        
        # Results storage
        self.results = None
        
        # Load saved credentials
        self.load_credentials()
        
        # Load saved credentials
        self.load_credentials()
        
    def log(self, message, level='info'):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {
            'info': '💙',
            'success': '✅', 
            'error': '❌',
            'working': '⚡',
            'found': '🔍'
        }
        icon = icons.get(level, '💙')
        log_message = f"[{timestamp}] {icon} {message}\n"
        
        # Update UI from main thread
        self.root.after(0, self._update_log, log_message)
        
    def _update_log(self, message):
        """Update log text widget"""
        self.log_text.insert('end', message)
        self.log_text.see('end')
        self.root.update()
        
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete('1.0', 'end')
        
    def start_extraction(self):
        """Start DM extraction in background thread"""
        if not INSTAGRAPI_AVAILABLE:
            messagebox.showerror("ข้อผิดพลาด", "instagrapi ไม่ได้ติดตั้ง!\nกรุณารัน: pip install instagrapi")
            return
        
        # Validate credentials first
        if not self.validate_credentials():
            return
            
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Ask to save credentials
        self.save_credentials()
        
        # Show confirmation dialog with security warning
        confirm_message = f"""🔐 ยืนยันการเข้าสู่ระบบ

Username: {username}
Password: {'*' * len(password)}

⚠️ คำเตือนความปลอดภัย:
• ใช้ข้อมูลของคุณเองเท่านั้น
• ปิด 2FA ชั่วคราวหากเปิดใช้งาน
• ระวัง rate limiting จาก Instagram
• ใช้เพื่อการศึกษาเท่านั้น

ต้องการดำเนินการต่อหรือไม่?"""
        
        if not messagebox.askyesno("ยืนยันการดำเนินการ", confirm_message):
            return
        
        # Disable extract button and start progress
        self.extract_btn.config(state='disabled', text='🔄 กำลังดำเนินการ...')
        self.progress.start()
        
        # Start extraction in background
        thread = threading.Thread(target=self.run_extraction, args=(username, password))
        thread.daemon = True
        thread.start()
        
    def run_extraction(self, username, password):
        """Run extraction in background thread"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run extraction
            self.results = loop.run_until_complete(self._extract_dms(username, password))
            
            # Update UI
            self.root.after(0, self._extraction_complete)
            
        except Exception as e:
            self.root.after(0, self._extraction_error, str(e))
            
    async def _extract_dms(self, username, password):
        """Extract DMs using instagrapi"""
        target_user = self.target_entry.get().strip() or None
        max_conversations = int(self.max_conv_var.get())
        max_messages = int(self.max_msg_var.get())
        
        self.log(f"🚀 Starting DM extraction for {username}", 'working')
        
        # Initialize client
        client = Client()
        client.delay_range = [1, 3]
        
        # Login
        try:
            self.log("🔐 Logging in...", 'working')
            client.login(username, password)
            self.log("✅ Login successful!", 'success')
        except ChallengeRequired:
            self.log("🚨 Challenge required - manual verification needed", 'error')
            return None
        except PleaseWaitFewMinutes:
            self.log("⏰ Rate limited - please try again later", 'error')
            return None
        except Exception as e:
            self.log(f"❌ Login failed: {str(e)}", 'error')
            return None
            
        dm_data = {
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'target_user': target_user,
            'conversations': [],
            'total_messages': 0
        }
        
        try:
            # Get threads
            self.log("📥 Fetching conversations...", 'working')
            threads = client.direct_threads()
            self.log(f"Found {len(threads)} conversations", 'found')
            
            # Process conversations
            for i, thread in enumerate(threads[:max_conversations], 1):
                try:
                    self.log(f"💬 Processing conversation {i}/{min(len(threads), max_conversations)}", 'working')
                    
                    conversation = {
                        'thread_id': thread.id,
                        'participants': [],
                        'messages': [],
                        'message_count': 0
                    }
                    
                    # Get participants
                    for user in thread.users:
                        conversation['participants'].append({
                            'username': user.username,
                            'full_name': user.full_name,
                            'user_id': str(user.pk)
                        })
                    
                    # Check target user filter
                    if target_user:
                        usernames = [p['username'] for p in conversation['participants']]
                        if target_user not in usernames:
                            continue
                    
                    # Get messages
                    messages = client.direct_messages(thread.id, amount=max_messages)
                    
                    for msg in messages:
                        message = {
                            'message_id': msg.id,
                            'sender_id': str(msg.user_id),
                            'timestamp': msg.timestamp.isoformat(),
                            'text': msg.text or '',
                            'message_type': msg.item_type
                        }
                        conversation['messages'].append(message)
                    
                    conversation['message_count'] = len(conversation['messages'])
                    dm_data['conversations'].append(conversation)
                    dm_data['total_messages'] += conversation['message_count']
                    
                    self.log(f"✅ Extracted {conversation['message_count']} messages", 'success')
                    
                    # Small delay
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    self.log(f"❌ Error processing conversation: {str(e)}", 'error')
                    continue
            
            # Logout
            try:
                client.logout()
                self.log("🚪 Logged out successfully", 'success')
            except:
                pass
                
            self.log(f"🎉 Extraction complete! {dm_data['total_messages']} messages from {len(dm_data['conversations'])} conversations", 'success')
            return dm_data
            
        except Exception as e:
            self.log(f"💔 Extraction failed: {str(e)}", 'error')
            return None
            
    def _extraction_complete(self):
        """Called when extraction completes"""
        self.progress.stop()
        self.extract_btn.config(state='normal', text='🚀 Extract DMs')
        
        if self.results:
            self.save_btn.config(state='normal')
            success_message = f"""✅ การดึงข้อมูล DM เสร็จสิ้น!

📊 สรุปผลลัพธ์:
💬 ข้อความทั้งหมด: {self.results['total_messages']} ข้อความ
🗣️ การสนทนา: {len(self.results['conversations'])} การสนทนา
👥 ผู้ใช้ที่พบ: {len(set(p['username'] for conv in self.results['conversations'] for p in conv['participants']))} คน

💾 คลิก "Save Results" เพื่อบันทึกข้อมูล"""
            messagebox.showinfo("สำเร็จ!", success_message)
        else:
            messagebox.showerror("ข้อผิดพลาด", "การดึงข้อมูลล้มเหลว - ตรวจสอบ log สำหรับรายละเอียด")
            
    def _extraction_error(self, error):
        """Called when extraction fails"""
        self.progress.stop()
        self.extract_btn.config(state='normal', text='🚀 Extract DMs')
        self.log(f"💔 ข้อผิดพลาดในการดึงข้อมูล: {error}", 'error')
        
        error_message = f"""❌ การดึงข้อมูลล้มเหลว

ข้อผิดพลาด: {error}

🔧 วิธีแก้ไขที่แนะนำ:
• ตรวจสอบ username และ password
• ปิด 2FA ชั่วคราว
• ลองอีกครั้งหลังจาก 5-10 นาที
• ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
• ดูรายละเอียดใน log"""
        
        messagebox.showerror("ข้อผิดพลาด", error_message)
        
    def save_results(self):
        """Save results to file"""
        if not self.results:
            messagebox.showerror("Error", "No results to save!")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"instagram_dms_{self.results['username']}_{timestamp}.json"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialname=default_filename
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, indent=2, ensure_ascii=False)
                self.log(f"💾 Results saved to: {filename}", 'success')
                messagebox.showinfo("Success", f"Results saved to:\n{filename}")
            except Exception as e:
                self.log(f"❌ Save failed: {str(e)}", 'error')
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show='')
            self.show_password_btn.config(text='🙈')
            self.show_password_var.set(False)
        else:
            self.password_entry.config(show='*')
            self.show_password_btn.config(text='👁️')
            self.show_password_var.set(True)
    
    def check_password_strength(self, event=None):
        """Check password strength and provide feedback"""
        password = self.password_entry.get()
        
        if not password:
            self.password_strength_var.set("")
            return
        
        strength_score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            strength_score += 1
        else:
            feedback.append("ต้องมีอย่างน้อย 8 ตัวอักษร")
        
        # Has uppercase
        if any(c.isupper() for c in password):
            strength_score += 1
        else:
            feedback.append("ควรมีตัวพิมพ์ใหญ่")
        
        # Has lowercase  
        if any(c.islower() for c in password):
            strength_score += 1
        else:
            feedback.append("ควรมีตัวพิมพ์เล็ก")
        
        # Has numbers
        if any(c.isdigit() for c in password):
            strength_score += 1
        else:
            feedback.append("ควรมีตัวเลข")
        
        # Has special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            strength_score += 1
        else:
            feedback.append("ควรมีอักขระพิเศษ")
        
        # Set strength indicator
        if strength_score <= 2:
            strength_text = "🔴 อ่อน"
            color = '#ff4444'
        elif strength_score <= 3:
            strength_text = "🟡 ปานกลาง"
            color = '#ffaa00'
        elif strength_score <= 4:
            strength_text = "🟢 ดี"
            color = '#44ff44'
        else:
            strength_text = "💚 แข็งแกร่ง"
            color = '#00ff00'
        
        if feedback:
            strength_text += f" ({', '.join(feedback[:2])})"
        
        self.password_strength_var.set(strength_text)
        self.password_strength_label.config(foreground=color)
    
    def validate_credentials(self):
        """Validate user credentials before extraction"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        errors = []
        
        if not username:
            errors.append("กรุณาใส่ username")
        elif len(username) < 3:
            errors.append("Username สั้นเกินไป")
        
        if not password:
            errors.append("กรุณาใส่รหัสผ่าน")
        elif len(password) < 6:
            errors.append("รหัสผ่านสั้นเกินไป (ต้องมีอย่างน้อย 6 ตัวอักษร)")
        
        if errors:
            error_message = "ข้อมูลไม่ถูกต้อง:\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("ข้อผิดพลาด", error_message)
            return False
        
        return True

    def save_credentials(self):
        """Save credentials for future use (optional)"""
        username = self.username_entry.get().strip()
        if username and messagebox.askyesno("บันทึกข้อมูล", "ต้องการบันทึก username สำหรับใช้ครั้งต่อไปหรือไม่?"):
            try:
                config_file = Path.home() / ".instagram_dm_extractor_config.json"
                config = {"last_username": username}
                with open(config_file, 'w') as f:
                    json.dump(config, f)
                self.log("💾 บันทึก username แล้ว", 'success')
            except Exception as e:
                self.log(f"❌ ไม่สามารถบันทึกข้อมูลได้: {e}", 'error')
    
    def load_credentials(self):
        """Load saved credentials"""
        try:
            config_file = Path.home() / ".instagram_dm_extractor_config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    last_username = config.get("last_username", "")
                    if last_username:
                        self.username_entry.insert(0, last_username)
                        self.log("💡 โหลด username ที่บันทึกไว้แล้ว", 'info')
        except Exception as e:
            self.log(f"⚠️ ไม่สามารถโหลดข้อมูลได้: {e}", 'info')

    def show_help(self):
        """Show help dialog"""
        help_text = """💀📱 Instagram DM Extractor - คู่มือการใช้งาน

🔐 การเข้าสู่ระบบ:
• ใส่ username และ password ของ Instagram
• ปิด 2FA ชั่วคราวหรือรองรับ challenge
• ระบบจะตรวจสอบความแข็งแกร่งของรหัสผ่าน

⚙️ ตัวเลือกการดึงข้อมูล:
• Target User: ระบุผู้ใช้เฉพาะ (ไม่ระบุ = ทั้งหมด)
• Max Conversations: จำนวนการสนทนาสูงสุด
• Messages per conversation: จำนวนข้อความต่อการสนทนา

🚀 การดำเนินการ:
1. ใส่ข้อมูล Instagram
2. กำหนดตัวเลือก (ถ้าต้องการ)
3. คลิก "Extract DMs"
4. รอการประมวลผล
5. บันทึกผลลัพธ์

⚠️ ข้อควรระวัง:
• ใช้ข้อมูลของคุณเองเท่านั้น
• ระวัง rate limiting
• เพื่อการศึกษาเท่านั้น
• ปฏิบัติตาม Terms of Service

🔧 การแก้ไขปัญหา:
• Login failed: ตรวจสอบ username/password
• Rate limited: รอ 5-15 นาที
• Challenge required: ยืนยันตัวตนใน Instagram app
• Connection error: ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต"""
        
        messagebox.showinfo("คู่มือการใช้งาน", help_text)
    
    def test_connection(self):
        """Test connection to Instagram"""
        if not INSTAGRAPI_AVAILABLE:
            messagebox.showerror("ข้อผิดพลาด", "instagrapi ไม่ได้ติดตั้ง!")
            return
        
        # Validate credentials first
        if not self.validate_credentials():
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        self.log("🧪 กำลังทดสอบการเชื่อมต่อ...", 'working')
        
        # Start test in background
        thread = threading.Thread(target=self._test_connection_background, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _test_connection_background(self, username, password):
        """Test connection in background"""
        try:
            # Test import
            from instagrapi import Client
            from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
            
            client = Client()
            client.delay_range = [1, 2]
            
            # Try to login
            client.login(username, password)
            
            # Try to get basic info
            user_info = client.account_info()
            
            # Logout
            client.logout()
            
            # Success
            self.root.after(0, self._test_success, user_info.username)
            
        except ChallengeRequired:
            self.root.after(0, self._test_error, "Challenge required - กรุณายืนยันตัวตนใน Instagram app")
        except PleaseWaitFewMinutes:
            self.root.after(0, self._test_error, "Rate limited - รอสักครู่แล้วลองใหม่")
        except Exception as e:
            self.root.after(0, self._test_error, f"เชื่อมต่อไม่สำเร็จ: {str(e)}")
    
    def _test_success(self, logged_username):
        """Called when test succeeds"""
        self.log(f"✅ เชื่อมต่อสำเร็จ! ยืนยันตัวตน: {logged_username}", 'success')
        messagebox.showinfo("ทดสอบสำเร็จ", f"✅ เชื่อมต่อ Instagram สำเร็จ!\n\nยืนยันตัวตน: {logged_username}\n\nพร้อมสำหรับการดึง DMs แล้ว!")
    
    def _test_error(self, error_msg):
        """Called when test fails"""
        self.log(f"❌ ทดสอบการเชื่อมต่อล้มเหลว: {error_msg}", 'error')
        messagebox.showerror("ทดสอบล้มเหลว", f"❌ การเชื่อมต่อล้มเหลว\n\n{error_msg}\n\nกรุณาตรวจสอบข้อมูลและลองใหม่")

def main():
    """Main function"""
    root = tk.Tk()
    app = InstagramDMExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
