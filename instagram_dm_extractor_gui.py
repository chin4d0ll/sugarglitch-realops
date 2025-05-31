#!/usr/bin/env python3
"""
💀📱 Instagram DM Extractor - Simple GUI Version 💀📱
====================================================
เครื่องมือดึง DMs พร้อม GUI ใช้งานง่าย
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
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(login_frame, text="Password:", style='Heading.TLabel').grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(login_frame, width=30, show='*')
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
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
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')\n        self.progress.pack(fill='x', pady=5)
        
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
            messagebox.showerror("Error", "instagrapi not installed!")
            return
            
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password required!")
            return
            
        # Disable extract button and start progress
        self.extract_btn.config(state='disabled')
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
        self.extract_btn.config(state='normal')
        
        if self.results:
            self.save_btn.config(state='normal')
            messagebox.showinfo("Success", f"Extraction complete!\n{self.results['total_messages']} messages extracted from {len(self.results['conversations'])} conversations")
        else:
            messagebox.showerror("Error", "Extraction failed - check log for details")
            
    def _extraction_error(self, error):
        """Called when extraction fails"""
        self.progress.stop()
        self.extract_btn.config(state='normal')
        self.log(f"💔 Extraction error: {error}", 'error')
        messagebox.showerror("Error", f"Extraction failed: {error}")
        
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

def main():
    """Main function"""
    root = tk.Tk()
    app = InstagramDMExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
