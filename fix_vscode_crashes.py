#!/usr/bin/env python3
"""
VSCode Remote Extension Crash Fix Script
Addresses memory pressure and resource issues causing frequent crashes
"""

import os
import subprocess
import json
import shutil
import time
from pathlib import Path

class VSCodeCrashFixer:
    def __init__(self):
        self.vscode_remote_dir = Path.home() / ".vscode-remote"
        self.vscode_server_dir = Path.home() / ".vscode-server"
        self.codespace_dir = Path("/workspaces/sugarglitch-realops")
        
    def check_system_resources(self):
        """Check current system resource usage"""
        print("=== SYSTEM RESOURCE CHECK ===")
        
        # Memory check
        try:
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            print("Memory Usage:")
            print(result.stdout)
        except Exception as e:
            print(f"Error checking memory: {e}")
        
        # Disk check
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            print("\nDisk Usage:")
            print(result.stdout)
        except Exception as e:
            print(f"Error checking disk: {e}")
        
        # Process check
        try:
            result = subprocess.run(['ps', 'aux', '--sort=-%mem'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            print("\nTop Memory Consumers:")
            for line in lines[:10]:
                if 'vscode' in line.lower() or 'python' in line.lower():
                    print(line)
        except Exception as e:
            print(f"Error checking processes: {e}")
    
    def clean_vscode_cache(self):
        """Clean VSCode cache and temporary files"""
        print("\n=== CLEANING VSCODE CACHE ===")
        
        cache_dirs = [
            self.vscode_remote_dir / "data" / "logs",
            self.vscode_remote_dir / "data" / "CachedExtensions",
            self.vscode_remote_dir / "data" / "CachedExtensionVSIXs",
            self.vscode_remote_dir / "extensionsCache",
            self.vscode_server_dir / "data" / "logs" if self.vscode_server_dir.exists() else None,
        ]
        
        for cache_dir in cache_dirs:
            if cache_dir and cache_dir.exists():
                try:
                    print(f"Cleaning: {cache_dir}")
                    shutil.rmtree(cache_dir)
                    print(f"✓ Cleaned {cache_dir}")
                except Exception as e:
                    print(f"✗ Failed to clean {cache_dir}: {e}")
    
    def optimize_vscode_settings(self):
        """Create optimized VSCode settings for Codespaces"""
        print("\n=== OPTIMIZING VSCODE SETTINGS ===")
        
        # Create .vscode directory if it doesn't exist
        vscode_dir = self.codespace_dir / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        # Optimized settings for memory-constrained environments
        settings = {
            # Memory optimization
            "python.analysis.memory.keepLibraryAst": False,
            "python.analysis.memory.keepLibraryLocalVariables": False,
            "python.analysis.indexing": False,
            "python.analysis.packageIndexDepths": [
                {"name": "", "depth": 1}
            ],
            
            # Disable heavy features
            "python.analysis.autoImportCompletions": False,
            "python.analysis.completeFunctionParens": False,
            "python.analysis.inlayHints.variableTypes": False,
            "python.analysis.inlayHints.functionReturnTypes": False,
            "python.analysis.inlayHints.callArgumentNames": False,
            
            # File watching optimization
            "files.watcherExclude": {
                "**/.git/**": True,
                "**/node_modules/**": True,
                "**/__pycache__/**": True,
                "**/logs/**": True,
                "**/temp/**": True,
                "**/backups/**": True,
                "**/data/**": True,
                "**/results/**": True,
                "**/extracted_project/**": True,
                "**/hijacked_sessions/**": True,
                "**/sessions/**": True,
                "**/sessions_fresh/**": True
            },
            
            # Search optimization
            "search.exclude": {
                "**/.git": True,
                "**/node_modules": True,
                "**/__pycache__": True,
                "**/logs": True,
                "**/temp": True,
                "**/backups": True,
                "**/data": True,
                "**/results": True
            },
            
            # Editor optimization
            "editor.suggest.showStatusBar": False,
            "editor.hover.delay": 1000,
            "editor.quickSuggestions": {
                "other": False,
                "comments": False,
                "strings": False
            },
            
            # Extension optimization
            "extensions.autoCheckUpdates": False,
            "extensions.autoUpdate": False,
            
            # Terminal optimization
            "terminal.integrated.scrollback": 1000,
            
            # Git optimization
            "git.autorefresh": False,
            "git.decorations.enabled": False,
            
            # Telemetry
            "telemetry.telemetryLevel": "off"
        }
        
        settings_file = vscode_dir / "settings.json"
        try:
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print(f"✓ Created optimized settings: {settings_file}")
        except Exception as e:
            print(f"✗ Failed to create settings: {e}")
    
    def create_launch_config(self):
        """Create optimized launch configuration"""
        print("\n=== CREATING LAUNCH CONFIG ===")
        
        vscode_dir = self.codespace_dir / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Current File (Optimized)",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "justMyCode": True,
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}",
                        "PYTHONUNBUFFERED": "1"
                    }
                }
            ]
        }
        
        launch_file = vscode_dir / "launch.json"
        try:
            with open(launch_file, 'w') as f:
                json.dump(launch_config, f, indent=2)
            print(f"✓ Created launch config: {launch_file}")
        except Exception as e:
            print(f"✗ Failed to create launch config: {e}")
    
    def clean_project_cache(self):
        """Clean project-specific cache and temporary files"""
        print("\n=== CLEANING PROJECT CACHE ===")
        
        cache_patterns = [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            ".pytest_cache",
            ".coverage",
            "logs/*.log",
            "temp/*",
        ]
        
        for pattern in cache_patterns:
            try:
                if pattern.startswith("*."):
                    # File pattern
                    result = subprocess.run(['find', str(self.codespace_dir), '-name', pattern, '-delete'], 
                                          capture_output=True, text=True)
                elif pattern.endswith("/*"):
                    # Directory contents
                    dir_path = self.codespace_dir / pattern[:-2]
                    if dir_path.exists():
                        for item in dir_path.iterdir():
                            if item.is_file():
                                item.unlink()
                        print(f"✓ Cleaned contents of {dir_path}")
                else:
                    # Directory
                    result = subprocess.run(['find', str(self.codespace_dir), '-name', pattern, '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'], 
                                          capture_output=True, text=True)
                    print(f"✓ Cleaned {pattern} directories")
            except Exception as e:
                print(f"✗ Failed to clean {pattern}: {e}")
    
    def kill_heavy_processes(self):
        """Kill heavy VSCode processes that might be causing issues"""
        print("\n=== MANAGING HEAVY PROCESSES ===")
        
        try:
            # Get process list
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            heavy_processes = []
            for line in lines:
                if 'extensionHost' in line and '%MEM' in line:
                    continue  # Skip header
                if 'extensionHost' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        pid = parts[1]
                        mem_percent = float(parts[3])
                        if mem_percent > 3.0:  # More than 3% memory
                            heavy_processes.append((pid, mem_percent))
            
            print(f"Found {len(heavy_processes)} heavy extension processes")
            
            # Kill the heaviest processes (keep at least one)
            if len(heavy_processes) > 2:
                heavy_processes.sort(key=lambda x: x[1], reverse=True)
                for pid, mem_percent in heavy_processes[1:]:  # Keep the first one
                    try:
                        subprocess.run(['kill', '-TERM', pid], check=True)
                        print(f"✓ Terminated process {pid} (using {mem_percent}% memory)")
                        time.sleep(1)
                    except Exception as e:
                        print(f"✗ Failed to terminate process {pid}: {e}")
        
        except Exception as e:
            print(f"Error managing processes: {e}")
    
    def create_monitoring_script(self):
        """Create a script to monitor system resources"""
        print("\n=== CREATING MONITORING SCRIPT ===")
        
        monitor_script = '''#!/bin/bash
# VSCode Resource Monitor
echo "=== VSCode Resource Monitor ==="
echo "Memory Usage:"
free -h
echo ""
echo "Disk Usage:"
df -h | grep -E '(Filesystem|overlay|/dev/root)'
echo ""
echo "VSCode Processes:"
ps aux --sort=-%mem | grep -E '(vscode|extensionHost|Pylance)' | head -5
echo ""
echo "Last 5 VSCode crashes (if any):"
journalctl --user -u vscode-server --since "1 hour ago" | tail -5 2>/dev/null || echo "No crash logs found"
'''
        
        monitor_file = self.codespace_dir / "monitor_resources.sh"
        try:
            with open(monitor_file, 'w') as f:
                f.write(monitor_script)
            os.chmod(monitor_file, 0o755)
            print(f"✓ Created monitoring script: {monitor_file}")
            print("  Run with: ./monitor_resources.sh")
        except Exception as e:
            print(f"✗ Failed to create monitoring script: {e}")
    
    def run_full_optimization(self):
        """Run all optimization steps"""
        print("🔧 VSCode Remote Extension Crash Fix")
        print("=" * 50)
        
        self.check_system_resources()
        self.clean_vscode_cache()
        self.clean_project_cache()
        self.optimize_vscode_settings()
        self.create_launch_config()
        self.create_monitoring_script()
        self.kill_heavy_processes()
        
        print("\n" + "=" * 50)
        print("✅ OPTIMIZATION COMPLETE!")
        print("\n📋 NEXT STEPS:")
        print("1. Restart VSCode (Ctrl+Shift+P -> 'Developer: Reload Window')")
        print("2. If crashes persist, restart the entire Codespace")
        print("3. Use ./monitor_resources.sh to track resource usage")
        print("4. Consider upgrading to a larger Codespace if issues continue")
        print("\n💡 PREVENTION TIPS:")
        print("- Close unused tabs and terminals")
        print("- Avoid opening too many files simultaneously")
        print("- Use 'Files: Save All' frequently")
        print("- Run this script weekly to maintain performance")

if __name__ == "__main__":
    fixer = VSCodeCrashFixer()
    fixer.run_full_optimization()
