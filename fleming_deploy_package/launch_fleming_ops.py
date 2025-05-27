#!/usr/bin/env python3
"""
Fleming Operations Launcher
Main entry point for Instagram extraction operations
"""

import os
import sys
import json
from pathlib import Path

# Ensure we're in the right directory
script_dir = Path(__file__).parent
os.chdir(script_dir)

def setup_environment():
    """Setup environment and install dependencies"""
    print("🔧 Setting up environment...")
    
    # Install requirements
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed")

def load_config():
    """Load configuration"""
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json not found!")
        print("Please update config.json with your credentials")
        return None
    
    with open(config_file, 'r') as f:
        return json.load(f)

def main():
    """Main launcher"""
    print("🚀 Fleming Operations Launcher")
    print("="*50)
    
    # Setup
    setup_environment()
    
    # Load config
    config = load_config()
    if not config:
        return
    
    # Check for updated passwords
    primary_password = config["accounts"]["primary"]["password"]
    if primary_password == "UPDATE_PASSWORD_HERE":
        print("❌ Please update passwords in config.json first!")
        return
    
    print(f"🎯 Target: {config['accounts']['primary']['username']}")
    
    # Import and run extractor
    try:
        from master_production_extractor_2025 import MasterProductionExtractor
        
        extractor = MasterProductionExtractor()
        # Update credentials from config
        extractor.username = config["accounts"]["primary"]["username"]
        extractor.passwords = config["accounts"]["primary"]["backup_passwords"]
        
        results = extractor.run_complete_extraction()
        
        if results["success"]:
            print("🎉 EXTRACTION SUCCESSFUL!")
            summary = results["summary"]
            print(f"📥 DM Threads: {summary['dm_threads']}")
            print(f"💬 Messages: {summary['total_messages']}")
            print(f"📖 Stories: {summary['total_stories']}")
            print(f"📸 Posts: {summary['total_posts']}")
        else:
            print(f"❌ Extraction failed: {results.get('error', 'Unknown error')}")
            
    except ImportError:
        print("❌ Extractor module not found!")
        print("Make sure all files are in the same directory")

if __name__ == "__main__":
    main()
