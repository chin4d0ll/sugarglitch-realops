#!/usr/bin/env python3
"""
💖🎮 ENHANCED INSTAGRAM BYPASS - GUI VERSION 🎮💖
=================================================
Beautiful GUI interface for Enhanced Instagram Private Bypass

Features:
- User-friendly interface
- Real-time progress tracking
- Beautiful results display
- Export functionality

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 - GUI Enhanced!
For: Educational & Security Research Only!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import asyncio
import threading
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our enhanced bypass
from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass

class InstagramBypassGUI:
    """
    💖 Beautiful GUI for Instagram Enhanced Bypass
    
    Features:
    - Real-time progress updates
    - Beautiful girly theme
    - Results visualization
    - Export functionality
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💖 Enhanced Instagram Private Bypass - น้องจิน ♥️")
        self.root.geometry("900x700")
        self.root.configure(bg='#2C2F36')
        
        # Colors (girly theme)
        self.colors = {
            'bg': '#2C2F36',
            'fg': '#FFFFFF', 
            'accent': '#FF69B4',
            'success': '#90EE90',
            'warning': '#FFD700',
            'error': '#FF6B6B',
            'button': '#FF1493',
            'entry': '#3C3F47'
        }
        
        # Variables
        self.target_username = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="พร้อมแล้วค่ะ! ใส่ username แล้วกด Start! 💖")
        
        # Results storage
        self.current_results = None
        self.bypass_instance = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the beautiful GUI interface"""
        
        # Title Section
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=20, fill='x')
        
        title_label = tk.Label(
            title_frame,
            text="💀🔥 Enhanced Instagram Private Bypass 🔥💀",
            font=("Arial", 18, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="โดย น้องจิน - Super Enhanced GUI Version! ♥️",
            font=("Arial", 12),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        subtitle_label.pack()
        
        # Input Section
        input_frame = tk.Frame(self.root, bg=self.colors['bg'])
        input_frame.pack(pady=20, fill='x', padx=50)
        
        tk.Label(
            input_frame,
            text="🎯 Instagram Username (without @):",
            font=("Arial", 12, "bold"),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).pack(anchor='w')
        
        username_entry = tk.Entry(
            input_frame,
            textvariable=self.target_username,
            font=("Arial", 14),
            bg=self.colors['entry'],
            fg=self.colors['fg'],
            insertbackground=self.colors['fg']
        )
        username_entry.pack(fill='x', pady=5, ipady=8)
        
        # Buttons Section
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Start Enhanced Bypass",
            command=self.start_bypass,
            font=("Arial", 12, "bold"),
            bg=self.colors['button'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⛔ Stop",
            command=self.stop_bypass,
            font=("Arial", 12, "bold"),
            bg=self.colors['error'],
            fg='white',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=10)
        
        self.export_button = tk.Button(
            button_frame,
            text="💾 Export Results",
            command=self.export_results,
            font=("Arial", 12, "bold"),
            bg=self.colors['success'],
            fg='black',
            padx=20,
            pady=10,
            relief='flat',
            cursor='hand2',
            state='disabled'
        )
        self.export_button.pack(side='left', padx=10)
        
        # Progress Section
        progress_frame = tk.Frame(self.root, bg=self.colors['bg'])
        progress_frame.pack(pady=20, fill='x', padx=50)
        
        tk.Label(
            progress_frame,
            text="📊 Progress:",
            font=("Arial", 12, "bold"),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Arial", 10),
            fg=self.colors['warning'],
            bg=self.colors['bg'],
            wraplength=600
        )
        self.status_label.pack(anchor='w', pady=5)
        
        # Results Section
        results_frame = tk.Frame(self.root, bg=self.colors['bg'])
        results_frame.pack(pady=20, fill='both', expand=True, padx=50)
        
        tk.Label(
            results_frame,
            text="📋 Results:",
            font=("Arial", 12, "bold"),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        ).pack(anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            font=("Consolas", 10),
            bg='#1E1E1E',
            fg='#FFFFFF',
            insertbackground='white',
            wrap='word'
        )
        self.results_text.pack(fill='both', expand=True, pady=5)
        
        # Configure scrolled text colors
        self.results_text.tag_config('success', foreground='#90EE90')
        self.results_text.tag_config('warning', foreground='#FFD700')
        self.results_text.tag_config('error', foreground='#FF6B6B')
        self.results_text.tag_config('info', foreground='#87CEEB')
        self.results_text.tag_config('accent', foreground='#FF69B4')
        
    def log_message(self, message: str, tag: str = 'info'):
        """Add message to results text with proper formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.results_text.insert(tk.END, formatted_message, tag)
        self.results_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message: str):
        """Update status label"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def update_progress(self, value: float):
        """Update progress bar"""
        self.progress_var.set(value)
        self.root.update_idletasks()
        
    def start_bypass(self):
        """Start the enhanced bypass process"""
        username = self.target_username.get().strip()
        
        if not username:
            messagebox.showwarning("Warning", "กรุณาใส่ Instagram username ค่ะ! 💖")
            return
            
        # Reset UI
        self.results_text.delete('1.0', tk.END)
        self.progress_var.set(0)
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.export_button.config(state='disabled')
        
        # Start bypass in separate thread
        self.bypass_thread = threading.Thread(
            target=self.run_bypass_async,
            args=(username,),
            daemon=True
        )
        self.bypass_thread.start()
        
    def stop_bypass(self):
        """Stop the bypass process"""
        self.update_status("หยุดการทำงานแล้วค่ะ 🛑")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
    def run_bypass_async(self, username: str):
        """Run bypass in async context"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the bypass
            result = loop.run_until_complete(self.execute_bypass(username))
            
            # Update UI when done
            self.root.after(0, self.bypass_completed, result)
            
        except Exception as e:
            self.root.after(0, self.bypass_error, str(e))
            
    async def execute_bypass(self, username: str):
        """Execute the enhanced bypass with GUI updates"""
        
        self.log_message(f"🔥 เริ่ม Enhanced Instagram Private Bypass!", 'accent')
        self.log_message(f"🎯 Target: @{username}", 'info')
        self.update_status("กำลังเริ่มการ bypass... 🚀")
        self.update_progress(10)
        
        try:
            # Create bypass instance
            self.bypass_instance = SuperEnhancedInstagramBypass(username)
            
            # Override logging to update GUI
            original_girly_print = self.bypass_instance.girly_print
            def gui_girly_print(message, level="INFO", emoji="💖"):
                tag_map = {
                    "SUCCESS": "success",
                    "WARNING": "warning", 
                    "ERROR": "error",
                    "INFO": "info"
                }
                tag = tag_map.get(level, "info")
                self.root.after(0, self.log_message, f"{emoji} {message}", tag)
                
            self.bypass_instance.girly_print = gui_girly_print
            
            # Method 1: Enhanced Cache Mining
            self.update_status("📊 Method 1: Enhanced Cache Mining... 💎")
            self.update_progress(20)
            
            cache_result = await self.bypass_instance.enhanced_cache_mining()
            self.update_progress(50)
            
            # Method 2: Enhanced OSINT Gathering
            self.update_status("📊 Method 2: Enhanced OSINT Gathering... 🕵️")
            self.update_progress(60)
            
            osint_result = await self.bypass_instance.enhanced_osint_gathering()
            self.update_progress(80)
            
            # Generate report
            self.update_status("📊 Generating Final Report... 📋")
            self.update_progress(90)
            
            report = await self.bypass_instance.generate_final_report()
            self.update_progress(100)
            
            # Prepare results
            result = {
                'success': len(self.bypass_instance.success_methods) > 0,
                'extracted_data': self.bypass_instance.extracted_data,
                'results': self.bypass_instance.results,
                'report': report,
                'cache_result': cache_result,
                'osint_result': osint_result
            }
            
            return result
            
        except Exception as e:
            raise e
            
    def bypass_completed(self, result):
        """Handle bypass completion"""
        self.current_results = result
        
        if result.get('success'):
            self.log_message("🎉 Enhanced Instagram Private Bypass Complete!", 'success')
            self.log_message(f"📊 Data extracted: {len(result.get('extracted_data', {}))}", 'success')
            
            # Display summary
            summary = self.create_results_summary(result)
            self.log_message("\n" + "="*50, 'info')
            self.log_message("📋 RESULTS SUMMARY:", 'accent')
            self.log_message("="*50, 'info')
            self.log_message(summary, 'info')
            
            self.update_status("เสร็จสิ้นแล้ว! 🎉 คลิก Export เพื่อบันทึกผลลัพธ์")
            self.export_button.config(state='normal')
            
        else:
            self.log_message("💔 Bypass ไม่สำเร็จ", 'error')
            self.update_status("ไม่สำเร็จ 😢 ลองใหม่อีกครั้ง")
            
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
    def bypass_error(self, error_msg):
        """Handle bypass error"""
        self.log_message(f"❌ Error: {error_msg}", 'error')
        self.update_status(f"เกิดข้อผิดพลาด: {error_msg}")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
    def create_results_summary(self, result):
        """Create a formatted results summary"""
        extracted_data = result.get('extracted_data', {})
        results = result.get('results', {})
        
        summary = f"""
🎯 Target: @{results.get('target', 'N/A')}
⏱️ Duration: {results.get('total_duration', 'N/A')} seconds
📊 Success Rate: {results.get('success_rate', 0):.1f}%
🔍 Methods Used: {len(results.get('methods_used', []))}

📋 Extracted Data:
"""
        
        # Key profile data
        key_fields = ['username', 'full_name', 'biography', 'follower_count', 'following_count', 'posts_count', 'is_private', 'is_verified']
        
        for field in key_fields:
            if field in extracted_data:
                value = extracted_data[field]
                summary += f"  • {field.replace('_', ' ').title()}: {value}\n"
        
        # OSINT data
        osint_platforms = []
        for key in extracted_data:
            if any(platform in key.lower() for platform in ['twitter', 'tiktok', 'github', 'pinterest']):
                platform = key.split('_')[0].title()
                if platform not in osint_platforms:
                    osint_platforms.append(platform)
        
        if osint_platforms:
            summary += f"\n🕵️ OSINT Platforms Found: {', '.join(osint_platforms)}"
        
        return summary
        
    def export_results(self):
        """Export results to files"""
        if not self.current_results:
            messagebox.showwarning("Warning", "ไม่มีผลลัพธ์ให้ export ค่ะ!")
            return
            
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                title="บันทึกผลลัพธ์"
            )
            
            if filename:
                if filename.endswith('.json'):
                    # Export as JSON
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.current_results, f, indent=2, default=str)
                        
                else:
                    # Export as text
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(self.current_results.get('report', ''))
                
                messagebox.showinfo("Success", f"บันทึกผลลัพธ์แล้ว: {filename} 💾")
                self.log_message(f"💾 Exported to: {filename}", 'success')
                
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถบันทึกไฟล์ได้: {e}")
            
    def run(self):
        """Run the GUI application"""
        self.log_message("💖 Welcome to Enhanced Instagram Private Bypass GUI!", 'accent')
        self.log_message("🎯 ใส่ Instagram username แล้วกด Start เพื่อเริ่ม!", 'info')
        self.log_message("⚠️ สำหรับการศึกษาและวิจัยด้านความปลอดภัยเท่านั้น!", 'warning')
        
        self.root.mainloop()

def main():
    """Main function to run GUI"""
    try:
        app = InstagramBypassGUI()
        app.run()
    except Exception as e:
        print(f"❌ GUI Error: {e}")

if __name__ == "__main__":
    main()
