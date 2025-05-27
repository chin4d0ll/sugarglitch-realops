#!/usr/bin/env python3
"""
Memory Optimization Script for SugarGlitch RealOps
Reduces RAM usage by optimizing VS Code, Python processes, and system resources
"""

import psutil
import os
import subprocess
import gc
import sys
from pathlib import Path
import json

class MemoryOptimizer:
    def __init__(self):
        self.initial_memory = self.get_memory_info()
        print(f"🔧 Memory Optimizer Starting - Initial RAM Usage: {self.initial_memory['used_gb']:.1f}GB / {self.initial_memory['total_gb']:.1f}GB")
    
    def get_memory_info(self):
        """Get current memory information"""
        memory = psutil.virtual_memory()
        return {
            'total_gb': memory.total / (1024**3),
            'used_gb': memory.used / (1024**3),
            'available_gb': memory.available / (1024**3),
            'percent': memory.percent
        }
    
    def optimize_vscode_settings(self):
        """Optimize VS Code settings for lower memory usage"""
        print("⚙️ Optimizing VS Code settings...")
        
        vscode_settings_dir = Path.home() / ".vscode-remote" / "data" / "Machine"
        settings_file = vscode_settings_dir / "settings.json"
        
        # Create optimized settings
        optimized_settings = {
            "files.watcherExclude": {
                "**/.git/objects/**": True,
                "**/.git/subtree-cache/**": True,
                "**/node_modules/**": True,
                "**/.hg/store/**": True,
                "**/logs/**": True,
                "**/temp/**": True,
                "**/__pycache__/**": True,
                "**/.pytest_cache/**": True,
                "**/venv/**": True,
                "**/env/**": True
            },
            "search.exclude": {
                "**/node_modules": True,
                "**/bower_components": True,
                "**/.git": True,
                "**/.DS_Store": True,
                "**/logs": True,
                "**/temp": True,
                "**/__pycache__": True,
                "**/.pytest_cache": True
            },
            "python.analysis.memory.keepLibraryAst": False,
            "python.analysis.memory.keepLibraryLocalVariables": False,
            "extensions.autoUpdate": False,
            "extensions.autoCheckUpdates": False,
            "workbench.enableExperiments": False,
            "telemetry.telemetryLevel": "off",
            "typescript.preferences.includePackageJsonAutoImports": "off",
            "typescript.suggest.autoImports": False,
            "javascript.suggest.autoImports": False,
            "editor.codeLens": False,
            "editor.minimap.enabled": False,
            "workbench.iconTheme": None,
            "git.decorations.enabled": False,
            "git.autoRepositoryDetection": False
        }
        
        try:
            # Read existing settings
            existing_settings = {}
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    existing_settings = json.load(f)
            
            # Merge with optimized settings
            existing_settings.update(optimized_settings)
            
            # Write back
            settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(settings_file, 'w') as f:
                json.dump(existing_settings, f, indent=2)
                
            print("✅ VS Code settings optimized for lower memory usage")
        except Exception as e:
            print(f"⚠️ Could not optimize VS Code settings: {e}")
    
    def clean_python_cache(self):
        """Clean Python cache files"""
        print("🧹 Cleaning Python cache...")
        
        cache_patterns = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo", 
            "**/.pytest_cache",
            "**/pip-log.txt",
            "**/pip-delete-this-directory.txt"
        ]
        
        workspace_root = Path("/workspaces/sugarglitch-realops")
        cleaned_count = 0
        
        for pattern in cache_patterns:
            for path in workspace_root.rglob(pattern):
                try:
                    if path.is_file():
                        path.unlink()
                        cleaned_count += 1
                    elif path.is_dir():
                        import shutil
                        shutil.rmtree(path)
                        cleaned_count += 1
                except Exception as e:
                    continue
        
        print(f"✅ Cleaned {cleaned_count} Python cache files/directories")
    
    def optimize_node_memory(self):
        """Optimize Node.js memory usage"""
        print("🟢 Optimizing Node.js processes...")
        
        # Kill old Node processes that are using too much memory
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
            try:
                if proc.info['name'] and 'node' in proc.info['name'].lower():
                    memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    
                    # Kill Node processes using more than 500MB
                    if memory_mb > 500:
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if 'tsserver' not in cmdline and 'pylance' not in cmdline:
                            proc.terminate()
                            killed_count += 1
                            print(f"  Terminated high-memory Node process: {memory_mb:.1f}MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if killed_count > 0:
            print(f"✅ Terminated {killed_count} high-memory Node processes")
        else:
            print("✅ No high-memory Node processes found")
    
    def force_garbage_collection(self):
        """Force Python garbage collection"""
        print("🗑️ Forcing garbage collection...")
        
        # Python garbage collection
        collected = gc.collect()
        print(f"✅ Collected {collected} garbage objects")
        
        # System memory cleanup
        try:
            subprocess.run(['sync'], check=False)
            subprocess.run(['sudo', 'sysctl', '-w', 'vm.drop_caches=1'], 
                         check=False, capture_output=True)
        except:
            pass
    
    def set_memory_limits(self):
        """Set memory limits for processes"""
        print("⚖️ Setting memory limits...")
        
        # Set Node.js memory limit
        os.environ['NODE_OPTIONS'] = '--max-old-space-size=1024'
        
        # Set Python memory limit (if using uvloop or similar)
        os.environ['PYTHONMALLOC'] = 'pymalloc_debug'
        
        print("✅ Memory limits configured")
    
    def optimize_extension_host(self):
        """Optimize VS Code extension host"""
        print("🔌 Optimizing extension host...")
        
        try:
            # Kill extension hosts using too much memory
            killed = 0
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cmdline']):
                try:
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if 'extensionHost' in cmdline:
                            memory_mb = proc.info['memory_info'].rss / (1024 * 1024)
                            if memory_mb > 1000:  # Kill if using more than 1GB
                                proc.terminate()
                                killed += 1
                                print(f"  Terminated extension host using {memory_mb:.1f}MB")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if killed > 0:
                print(f"✅ Terminated {killed} high-memory extension hosts")
            else:
                print("✅ Extension hosts are within memory limits")
                
        except Exception as e:
            print(f"⚠️ Extension host optimization failed: {e}")
    
    def run_optimization(self):
        """Run full memory optimization"""
        print("🚀 Starting comprehensive memory optimization...\n")
        
        self.set_memory_limits()
        self.clean_python_cache()
        self.optimize_node_memory()
        self.optimize_extension_host()
        self.force_garbage_collection()
        self.optimize_vscode_settings()
        
        # Final memory check
        final_memory = self.get_memory_info()
        memory_saved = self.initial_memory['used_gb'] - final_memory['used_gb']
        
        print(f"\n📊 Memory Optimization Complete!")
        print(f"Initial: {self.initial_memory['used_gb']:.1f}GB / {self.initial_memory['total_gb']:.1f}GB ({self.initial_memory['percent']:.1f}%)")
        print(f"Final:   {final_memory['used_gb']:.1f}GB / {final_memory['total_gb']:.1f}GB ({final_memory['percent']:.1f}%)")
        
        if memory_saved > 0:
            print(f"💾 Memory Saved: {memory_saved:.1f}GB")
        else:
            print(f"⚠️ Memory usage increased by {abs(memory_saved):.1f}GB")
        
        return final_memory

if __name__ == "__main__":
    optimizer = MemoryOptimizer()
    optimizer.run_optimization()
