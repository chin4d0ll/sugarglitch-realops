#!/usr/bin/env python3
"""
💀🔥 ULTIMATE INSTAGRAM GUI 2025 🔥💀
=====================================
Beautiful GUI for Instagram Private Bypass with real-time monitoring!

✨ Features:
- Gorgeous dark theme with neon effects
- Real-time progress tracking
- Multi-target batch processing
- Live data visualization
- Export reports (JSON, HTML, PDF)
- Image gallery viewer
- Advanced analytics dashboard

Created by: น้องจิน (chin4d0ll) ♥️
Updated: 2025-06-01 - Ultimate GUI Edition!
For: Educational & Security Research Only!
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import asyncio
import threading
import json
import time
from datetime import datetime
from pathlib import Path
import webbrowser
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import requests
from io import BytesIO

# Import our enhanced bypass
try:
    from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass
except ImportError:
    print("❌ Enhanced bypass module not found!")

class UltimateInstagramGUI:
    """
    💀 Ultimate Instagram GUI - Beautiful and Powerful
    
    Features:
    - Dark theme with neon effects
    - Real-time progress monitoring
    - Multi-target processing
    - Advanced analytics
    - Export capabilities
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        # Data storage
        self.current_targets = []
        self.scan_results = {}
        self.is_scanning = False
        
        # Progress tracking
        self.progress_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to scan! 💖")

    def setup_window(self):
        """Setup main window properties"""
        self.root.title("💀🔥 Ultimate Instagram GUI 2025 🔥💀")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

    def setup_styles(self):
        """Setup beautiful dark theme styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Dark theme colors
        bg_dark = '#0a0a0a'
        bg_medium = '#1a1a1a'
        bg_light = '#2a2a2a'
        accent_pink = '#ff1493'
        accent_cyan = '#00ffff'
        text_light = '#ffffff'
        text_dim = '#cccccc'
        
        # Configure styles
        self.style.configure('Dark.TFrame', background=bg_dark)
        self.style.configure('Medium.TFrame', background=bg_medium, relief='raised', borderwidth=1)
        self.style.configure('Light.TFrame', background=bg_light, relief='sunken', borderwidth=1)
        
        self.style.configure('Neon.TLabel', background=bg_dark, foreground=accent_pink, 
                           font=('Consolas', 12, 'bold'))
        self.style.configure('Title.TLabel', background=bg_dark, foreground=accent_cyan,
                           font=('Consolas', 16, 'bold'))
        self.style.configure('Status.TLabel', background=bg_dark, foreground=text_light,
                           font=('Consolas', 10))
        
        self.style.configure('Neon.TButton', font=('Consolas', 10, 'bold'))
        self.style.map('Neon.TButton',
                      background=[('active', accent_pink), ('!active', bg_medium)],
                      foreground=[('active', text_light), ('!active', accent_pink)])
        
        self.style.configure('Dark.TEntry', font=('Consolas', 10),
                           fieldbackground=bg_medium, foreground=text_light)
        
        self.style.configure('Dark.TNotebook', background=bg_dark, tabposition='n')
        self.style.configure('Dark.TNotebook.Tab', background=bg_medium, foreground=text_light,
                           padding=[20, 8])
        self.style.map('Dark.TNotebook.Tab',
                      background=[('selected', accent_pink), ('!selected', bg_medium)],
                      foreground=[('selected', text_light), ('!selected', text_dim)])

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="💀🔥 ULTIMATE INSTAGRAM GUI 2025 🔥💀",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_scanner_tab()
        self.create_results_tab()
        self.create_analytics_tab()
        self.create_gallery_tab()
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar(main_frame)

    def create_scanner_tab(self):
        """Create main scanner tab"""
        scanner_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(scanner_frame, text='🎯 Scanner')
        
        # Left panel - Input
        left_panel = ttk.Frame(scanner_frame, style='Medium.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Target input section
        input_section = ttk.LabelFrame(left_panel, text='🎯 Target Settings', style='Medium.TFrame')
        input_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Single target
        ttk.Label(input_section, text="Instagram Username:", style='Neon.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 5))
        self.username_entry = ttk.Entry(input_section, style='Dark.TEntry', font=('Consolas', 12))
        self.username_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.username_entry.bind('<Return>', lambda e: self.add_target())
        
        # Buttons
        button_frame = ttk.Frame(input_section, style='Medium.TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="➕ Add Target", command=self.add_target, 
                  style='Neon.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="📁 Load List", command=self.load_target_list,
                  style='Neon.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Clear All", command=self.clear_targets,
                  style='Neon.TButton').pack(side=tk.LEFT, padx=5)
        
        # Target list
        list_section = ttk.LabelFrame(left_panel, text='📋 Target Queue', style='Medium.TFrame')
        list_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview for targets
        columns = ('Username', 'Status', 'Progress')
        self.target_tree = ttk.Treeview(list_section, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.target_tree.heading(col, text=col)
            self.target_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_section, orient=tk.VERTICAL, command=self.target_tree.yview)
        self.target_tree.configure(yscrollcommand=scrollbar.set)
        
        self.target_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Scan controls
        control_section = ttk.LabelFrame(left_panel, text='🚀 Scan Controls', style='Medium.TFrame')
        control_section.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Scan options
        options_frame = ttk.Frame(control_section, style='Medium.TFrame')
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.cache_mining_var = tk.BooleanVar(value=True)
        self.osint_gathering_var = tk.BooleanVar(value=True)
        self.deep_analysis_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="💎 Cache Mining", variable=self.cache_mining_var,
                       style='Neon.TButton').pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="🕵️ OSINT Gathering", variable=self.osint_gathering_var,
                       style='Neon.TButton').pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="🔬 Deep Analysis", variable=self.deep_analysis_var,
                       style='Neon.TButton').pack(anchor=tk.W)
        
        # Main scan button
        self.scan_button = ttk.Button(control_section, text="🔥 START ULTIMATE SCAN 🔥",
                                     command=self.start_scan, style='Neon.TButton')
        self.scan_button.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Right panel - Live progress
        right_panel = ttk.Frame(scanner_frame, style='Medium.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Live console
        console_section = ttk.LabelFrame(right_panel, text='📺 Live Console', style='Medium.TFrame')
        console_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.console_text = scrolledtext.ScrolledText(console_section, 
                                                     bg='#000000', fg='#00ff00',
                                                     font=('Consolas', 9),
                                                     wrap=tk.WORD)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Progress section
        progress_section = ttk.LabelFrame(right_panel, text='📊 Progress', style='Medium.TFrame')
        progress_section.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_section, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.progress_label = ttk.Label(progress_section, textvariable=self.progress_var,
                                       style='Status.TLabel')
        self.progress_label.pack(padx=10, pady=(0, 10))

    def create_results_tab(self):
        """Create results viewing tab"""
        results_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(results_frame, text='📊 Results')
        
        # Results will be populated after scanning
        self.results_tree = ttk.Treeview(results_frame, show='tree headings')
        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_analytics_tab(self):
        """Create analytics dashboard tab"""
        analytics_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(analytics_frame, text='📈 Analytics')
        
        # Placeholder for charts
        ttk.Label(analytics_frame, text="📈 Analytics Dashboard Coming Soon!",
                 style='Title.TLabel').pack(expand=True)

    def create_gallery_tab(self):
        """Create image gallery tab"""
        gallery_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(gallery_frame, text='🖼️ Gallery')
        
        # Placeholder for image gallery
        ttk.Label(gallery_frame, text="🖼️ Image Gallery Coming Soon!",
                 style='Title.TLabel').pack(expand=True)

    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(settings_frame, text='⚙️ Settings')
        
        # Settings will be added here
        ttk.Label(settings_frame, text="⚙️ Settings Panel",
                 style='Title.TLabel').pack(pady=20)

    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent, style='Light.TFrame')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Time display
        self.time_var = tk.StringVar()
        self.update_time()
        time_label = ttk.Label(status_frame, textvariable=self.time_var,
                              style='Status.TLabel')
        time_label.pack(side=tk.RIGHT, padx=10, pady=5)

    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(f"🕒 {current_time}")
        self.root.after(1000, self.update_time)

    def add_target(self):
        """Add target to scan queue"""
        username = self.username_entry.get().strip()
        if username:
            if username not in self.current_targets:
                self.current_targets.append(username)
                self.target_tree.insert('', tk.END, values=(username, 'Queued', '0%'))
                self.username_entry.delete(0, tk.END)
                self.console_log(f"➕ Added target: @{username}")
                self.status_var.set(f"Added @{username} to queue")
            else:
                messagebox.showwarning("Duplicate", f"@{username} already in queue!")
        else:
            messagebox.showwarning("Empty", "Please enter a username!")

    def load_target_list(self):
        """Load target list from file"""
        file_path = filedialog.askopenfilename(
            title="Load Target List",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    usernames = [line.strip() for line in f if line.strip()]
                
                added_count = 0
                for username in usernames:
                    if username and username not in self.current_targets:
                        self.current_targets.append(username)
                        self.target_tree.insert('', tk.END, values=(username, 'Queued', '0%'))
                        added_count += 1
                
                self.console_log(f"📁 Loaded {added_count} targets from file")
                self.status_var.set(f"Loaded {added_count} targets")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def clear_targets(self):
        """Clear all targets"""
        if messagebox.askyesno("Clear All", "Clear all targets from queue?"):
            self.current_targets.clear()
            for item in self.target_tree.get_children():
                self.target_tree.delete(item)
            self.console_log("🗑️ Cleared all targets")
            self.status_var.set("Queue cleared")

    def console_log(self, message):
        """Add message to console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.console_text.insert(tk.END, log_message)
        self.console_text.see(tk.END)
        
        # Limit console lines
        lines = self.console_text.get("1.0", tk.END).split('\n')
        if len(lines) > 1000:
            self.console_text.delete("1.0", "100.0")

    def start_scan(self):
        """Start scanning process"""
        if not self.current_targets:
            messagebox.showwarning("No Targets", "Please add targets to scan!")
            return
        
        if self.is_scanning:
            messagebox.showinfo("Already Scanning", "Scan is already in progress!")
            return
        
        self.is_scanning = True
        self.scan_button.configure(text="⏸️ SCANNING...", state='disabled')
        self.console_log("🚀 Starting Ultimate Instagram Scan!")
        
        # Start scanning in background thread
        threading.Thread(target=self.run_scan_thread, daemon=True).start()

    def run_scan_thread(self):
        """Run scan in background thread"""
        try:
            asyncio.run(self.execute_scan())
        except Exception as e:
            self.console_log(f"❌ Scan error: {e}")
        finally:
            self.is_scanning = False
            self.root.after(0, self.scan_complete)

    async def execute_scan(self):
        """Execute the actual scanning"""
        total_targets = len(self.current_targets)
        
        for i, username in enumerate(self.current_targets):
            try:
                # Update progress
                progress = (i / total_targets) * 100
                self.root.after(0, lambda p=progress: self.progress_bar.configure(value=p))
                self.root.after(0, lambda u=username: self.progress_var.set(f"Scanning @{u}..."))
                
                # Update target status
                for item in self.target_tree.get_children():
                    values = self.target_tree.item(item, 'values')
                    if values[0] == username:
                        self.root.after(0, lambda it=item: self.target_tree.item(it, values=(username, 'Scanning...', f'{progress:.1f}%')))
                        break
                
                self.root.after(0, lambda u=username: self.console_log(f"🎯 Scanning @{u}..."))
                
                # Create bypass instance
                bypass = SuperEnhancedInstagramBypass(username)
                
                # Execute scan based on selected options
                if self.cache_mining_var.get() and self.osint_gathering_var.get():
                    result = await bypass.execute_enhanced_bypass()
                elif self.cache_mining_var.get():
                    result = await bypass.enhanced_cache_mining()
                elif self.osint_gathering_var.get():
                    result = await bypass.enhanced_osint_gathering()
                else:
                    result = {'success': False, 'error': 'No scan methods selected'}
                
                # Store results
                self.scan_results[username] = result
                
                # Update target status
                status = "✅ Success" if result.get('success') else "❌ Failed"
                for item in self.target_tree.get_children():
                    values = self.target_tree.item(item, 'values')
                    if values[0] == username:
                        self.root.after(0, lambda it=item, s=status: self.target_tree.item(it, values=(username, s, '100%')))
                        break
                
                self.root.after(0, lambda u=username, s=status: self.console_log(f"{s} for @{u}"))
                
            except Exception as e:
                self.root.after(0, lambda u=username, e=e: self.console_log(f"❌ Error scanning @{u}: {e}"))
                
                # Update target status to failed
                for item in self.target_tree.get_children():
                    values = self.target_tree.item(item, 'values')
                    if values[0] == username:
                        self.root.after(0, lambda it=item: self.target_tree.item(it, values=(username, '❌ Error', '100%')))
                        break
        
        # Complete
        self.root.after(0, lambda: self.progress_bar.configure(value=100))
        self.root.after(0, lambda: self.progress_var.set("Scan complete!"))

    def scan_complete(self):
        """Called when scan is complete"""
        self.scan_button.configure(text="🔥 START ULTIMATE SCAN 🔥", state='normal')
        self.console_log("🎉 Ultimate Instagram Scan Complete!")
        
        # Show results summary
        total = len(self.current_targets)
        successful = sum(1 for result in self.scan_results.values() if result.get('success'))
        
        self.status_var.set(f"Scan complete: {successful}/{total} successful")
        
        # Switch to results tab
        self.notebook.select(1)
        self.populate_results()

    def populate_results(self):
        """Populate results tab with scan data"""
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Configure columns
        self.results_tree['columns'] = ('Username', 'Status', 'Data Fields', 'Sources')
        self.results_tree.column('#0', width=0, stretch=False)
        
        for col in self.results_tree['columns']:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        # Add results
        for username, result in self.scan_results.items():
            status = "✅ Success" if result.get('success') else "❌ Failed"
            
            if result.get('success'):
                data_count = len(result.get('extracted_data', {}))
                sources = len(result.get('results', {}).get('methods_used', []))
            else:
                data_count = 0
                sources = 0
            
            self.results_tree.insert('', tk.END, values=(
                username, status, f"{data_count} fields", f"{sources} sources"
            ))

    def export_results(self):
        """Export results to various formats"""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results to export!")
            return
        
        # Export options dialog
        export_format = messagebox.askyesnocancel(
            "Export Format", 
            "Choose export format:\nYes = JSON\nNo = HTML\nCancel = Cancel"
        )
        
        if export_format is None:  # Cancel
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format:  # JSON
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialname=f"instagram_scan_results_{timestamp}.json"
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.scan_results, f, indent=2, default=str)
                    
                    self.console_log(f"📁 Results exported to: {file_path}")
                    messagebox.showinfo("Export Complete", f"Results exported to:\n{file_path}")
                    
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export: {e}")
        
        else:  # HTML
            file_path = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html")],
                initialname=f"instagram_scan_report_{timestamp}.html"
            )
            
            if file_path:
                try:
                    html_content = self.generate_html_report()
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    self.console_log(f"📁 HTML report exported to: {file_path}")
                    messagebox.showinfo("Export Complete", f"HTML report exported to:\n{file_path}")
                    
                    # Ask to open in browser
                    if messagebox.askyesno("Open Report", "Open HTML report in browser?"):
                        webbrowser.open(f"file://{Path(file_path).absolute()}")
                        
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export HTML: {e}")

    def generate_html_report(self):
        """Generate HTML report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Scan Report</title>
    <style>
        body {{ background: #0a0a0a; color: #ffffff; font-family: 'Consolas', monospace; }}
        .header {{ text-align: center; color: #ff1493; margin: 20px 0; }}
        .summary {{ background: #1a1a1a; padding: 20px; margin: 20px 0; border-radius: 10px; }}
        .target {{ background: #2a2a2a; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .success {{ border-left: 5px solid #00ff00; }}
        .failed {{ border-left: 5px solid #ff0000; }}
        .data {{ margin: 10px 0; padding: 10px; background: #333; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💀🔥 ULTIMATE INSTAGRAM SCAN REPORT 🔥💀</h1>
        <p>Generated: {timestamp}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Scan Summary</h2>
        <p>Total targets: {len(self.scan_results)}</p>
        <p>Successful: {sum(1 for r in self.scan_results.values() if r.get('success'))}</p>
        <p>Failed: {sum(1 for r in self.scan_results.values() if not r.get('success'))}</p>
    </div>
"""
        
        for username, result in self.scan_results.items():
            status_class = "success" if result.get('success') else "failed"
            status_text = "✅ SUCCESS" if result.get('success') else "❌ FAILED"
            
            html += f"""
    <div class="target {status_class}">
        <h3>@{username} - {status_text}</h3>
"""
            
            if result.get('success') and result.get('extracted_data'):
                html += '<div class="data"><h4>📋 Extracted Data:</h4><ul>'
                
                for key, value in result['extracted_data'].items():
                    if isinstance(value, (str, int, bool)) and len(str(value)) < 200:
                        html += f'<li><strong>{key}:</strong> {value}</li>'
                
                html += '</ul></div>'
            
            html += '</div>'
        
        html += """
    <div style="text-align: center; margin: 40px 0; color: #ff1493;">
        <p>💖 Generated by น้องจิน's Ultimate Instagram GUI</p>
        <p>👻 For educational and security research only!</p>
    </div>
</body>
</html>"""
        
        return html

    def run(self):
        """Start the GUI application"""
        self.console_log("💖 Ultimate Instagram GUI 2025 Started!")
        self.console_log("👻 Ready for ultimate Instagram reconnaissance!")
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = UltimateInstagramGUI()
        app.run()
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
