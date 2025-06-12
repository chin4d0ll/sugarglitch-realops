#!/usr/bin/env python3
"""
🔗 SECLISTS INTEGRATION MANAGER
==============================

This script helps you download, manage, and integrate SecLists wordlists
into your existing penetration testing framework.

Features:
✅ Automatic SecLists download and setup
✅ Wordlist categorization and organization
✅ Integration with your existing scripts
✅ Memory-efficient wordlist processing
✅ Custom wordlist generation
"""

import os
import subprocess
import json
import logging
from pathlib import Path
from typing import List, Dict, Generator
import requests
import zipfile
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecListsManager:
    """Manage SecLists wordlists for penetration testing"""
    
    def __init__(self, base_dir: str = "wordlists"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.seclists_dir = self.base_dir / "SecLists"
        
    def download_seclists(self, method: str = "git") -> bool:
        """Download SecLists repository"""
        logger.info("📥 Downloading SecLists repository...")
        
        try:
            if method == "git" and self._check_git():
                return self._download_with_git()
            else:
                return self._download_with_wget()
        except Exception as e:
            logger.error(f"❌ Failed to download SecLists: {e}")
            return False
    
    def _check_git(self) -> bool:
        """Check if git is available"""
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _download_with_git(self) -> bool:
        """Download using git clone"""
        try:
            if self.seclists_dir.exists():
                logger.info("🔄 SecLists already exists, updating...")
                subprocess.run(['git', 'pull'], cwd=self.seclists_dir, check=True)
            else:
                subprocess.run([
                    'git', 'clone', 
                    'https://github.com/danielmiessler/SecLists.git',
                    str(self.seclists_dir)
                ], check=True)
            
            logger.info("✅ SecLists downloaded successfully via git")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Git download failed: {e}")
            return False
    
    def _download_with_wget(self) -> bool:
        """Download using wget/requests as fallback"""
        try:
            url = "https://github.com/danielmiessler/SecLists/archive/refs/heads/master.zip"
            logger.info("📥 Downloading SecLists via HTTP...")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            # Extract ZIP
            with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.base_dir)
            
            # Rename extracted folder
            extracted_dir = self.base_dir / "SecLists-master"
            if extracted_dir.exists():
                if self.seclists_dir.exists():
                    import shutil
                    shutil.rmtree(self.seclists_dir)
                extracted_dir.rename(self.seclists_dir)
            
            # Cleanup
            os.unlink(tmp_file_path)
            
            logger.info("✅ SecLists downloaded successfully via HTTP")
            return True
            
        except Exception as e:
            logger.error(f"❌ HTTP download failed: {e}")
            return False
    
    def get_wordlist_categories(self) -> Dict[str, List[str]]:
        """Get available wordlist categories"""
        if not self.seclists_dir.exists():
            logger.warning("⚠️ SecLists not found. Run download_seclists() first.")
            return {}
        
        categories = {}
        
        # Common wordlist directories in SecLists
        category_paths = {
            'Discovery': ['Discovery/Web-Content', 'Discovery/DNS'],
            'Fuzzing': ['Fuzzing'],
            'Passwords': ['Passwords'],
            'Usernames': ['Usernames'],
            'Web-Shells': ['Web-Shells'],
            'Payloads': ['Payloads'],
            'Miscellaneous': ['Miscellaneous']
        }
        
        for category, paths in category_paths.items():
            category_files = []
            for path in paths:
                full_path = self.seclists_dir / path
                if full_path.exists():
                    for file_path in full_path.rglob('*.txt'):
                        category_files.append(str(file_path.relative_to(self.seclists_dir)))
            categories[category] = category_files
        
        return categories
    
    def get_recommended_wordlists(self) -> Dict[str, str]:
        """Get recommended wordlists for common tasks"""
        return {
            # Directory/File Discovery
            'common_directories': 'Discovery/Web-Content/common.txt',
            'big_directories': 'Discovery/Web-Content/big.txt',
            'directory_list_medium': 'Discovery/Web-Content/directory-list-2.3-medium.txt',
            'raft_directories': 'Discovery/Web-Content/raft-medium-directories.txt',
            
            # File Discovery
            'common_files': 'Discovery/Web-Content/common.txt',
            'raft_files': 'Discovery/Web-Content/raft-medium-files.txt',
            'common_extensions': 'Discovery/Web-Content/web-extensions.txt',
            
            # Subdomain Discovery
            'subdomains_top1million': 'Discovery/DNS/subdomains-top1million-5000.txt',
            'fierce_hostlist': 'Discovery/DNS/fierce-hostlist.txt',
            
            # Password Lists
            'rockyou': 'Passwords/Leaked-Databases/rockyou.txt',
            'common_passwords': 'Passwords/Common-Credentials/10-million-password-list-top-100.txt',
            'darkweb2017': 'Passwords/Leaked-Databases/darkweb2017-top100.txt',
            
            # Username Lists
            'common_usernames': 'Usernames/Names/names.txt',
            'xato_usernames': 'Usernames/xato-net-10-million-usernames.txt',
            
            # Fuzzing
            'fuzz_common': 'Fuzzing/fuzz-Bo0oM.txt',
            'special_chars': 'Fuzzing/special-chars.txt',
            
            # Web Parameters
            'burp_params': 'Discovery/Web-Content/burp-parameter-names.txt',
            'common_params': 'Discovery/Web-Content/common-api-endpoints-mazen160.txt'
        }
    
    def load_wordlist(self, wordlist_path: str, max_lines: int = None) -> Generator[str, None, None]:
        """Load wordlist with memory-efficient generator"""
        full_path = self.seclists_dir / wordlist_path
        
        if not full_path.exists():
            logger.warning(f"⚠️ Wordlist not found: {wordlist_path}")
            return
        
        logger.info(f"📖 Loading wordlist: {wordlist_path}")
        
        try:
            line_count = 0
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        yield line
                        line_count += 1
                        if max_lines and line_count >= max_lines:
                            break
                            
            logger.info(f"✅ Loaded {line_count} entries from {wordlist_path}")
            
        except Exception as e:
            logger.error(f"❌ Error loading wordlist {wordlist_path}: {e}")
    
    def create_custom_wordlist(self, output_file: str, sources: List[str], 
                             max_per_source: int = 1000, 
                             remove_duplicates: bool = True) -> bool:
        """Create custom wordlist from multiple sources"""
        logger.info(f"🔧 Creating custom wordlist: {output_file}")
        
        all_words = set() if remove_duplicates else []
        
        for source in sources:
            logger.info(f"📥 Processing source: {source}")
            
            for word in self.load_wordlist(source, max_per_source):
                if remove_duplicates:
                    all_words.add(word)
                else:
                    all_words.append(word)
        
        # Write custom wordlist
        output_path = self.base_dir / output_file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if remove_duplicates:
                    for word in sorted(all_words):
                        f.write(f"{word}\n")
                else:
                    for word in all_words:
                        f.write(f"{word}\n")
            
            word_count = len(all_words)
            logger.info(f"✅ Custom wordlist created: {output_path} ({word_count} entries)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create custom wordlist: {e}")
            return False
    
    def get_wordlist_stats(self, wordlist_path: str) -> Dict[str, int]:
        """Get statistics about a wordlist"""
        full_path = self.seclists_dir / wordlist_path
        
        if not full_path.exists():
            return {'error': 'File not found'}
        
        stats = {
            'total_lines': 0,
            'non_empty_lines': 0,
            'comment_lines': 0,
            'max_length': 0,
            'min_length': float('inf'),
            'avg_length': 0
        }
        
        total_length = 0
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    stats['total_lines'] += 1
                    line = line.strip()
                    
                    if line:
                        stats['non_empty_lines'] += 1
                        if line.startswith('#'):
                            stats['comment_lines'] += 1
                        else:
                            length = len(line)
                            stats['max_length'] = max(stats['max_length'], length)
                            stats['min_length'] = min(stats['min_length'], length)
                            total_length += length
            
            effective_lines = stats['non_empty_lines'] - stats['comment_lines']
            if effective_lines > 0:
                stats['avg_length'] = total_length / effective_lines
            else:
                stats['avg_length'] = 0
                
            if stats['min_length'] == float('inf'):
                stats['min_length'] = 0
                
        except Exception as e:
            logger.error(f"❌ Error analyzing wordlist: {e}")
            return {'error': str(e)}
        
        return stats

def create_integration_examples():
    """Create example scripts showing how to integrate SecLists"""
    
    # Example 1: Directory brute forcer with SecLists
    dir_bruteforcer = '''#!/usr/bin/env python3
"""
Directory Brute Forcer with SecLists Integration
"""
import asyncio
import aiohttp
from seclists_manager import SecListsManager

async def bruteforce_directories(target_url, wordlist_name='common_directories'):
    manager = SecListsManager()
    recommended = manager.get_recommended_wordlists()
    
    if wordlist_name not in recommended:
        print(f"❌ Wordlist {wordlist_name} not found")
        return
    
    wordlist_path = recommended[wordlist_name]
    print(f"🔍 Using wordlist: {wordlist_path}")
    
    async with aiohttp.ClientSession() as session:
        for directory in manager.load_wordlist(wordlist_path, max_lines=1000):
            url = f"{target_url.rstrip('/')}/{directory}/"
            try:
                async with session.get(url, timeout=5) as response:
                    if response.status in [200, 301, 302, 403]:
                        print(f"✅ Found: {url} [{response.status}]")
            except:
                pass

if __name__ == "__main__":
    target = input("Enter target URL: ")
    asyncio.run(bruteforce_directories(target))
'''
    
    with open('/workspaces/sugarglitch-realops/seclists_directory_bruteforcer.py', 'w') as f:
        f.write(dir_bruteforcer)
    
    # Example 2: Password list processor
    password_processor = '''#!/usr/bin/env python3
"""
Password List Processor with SecLists
"""
from seclists_manager import SecListsManager

def process_passwords(wordlist_name='common_passwords', target_service='ssh'):
    manager = SecListsManager()
    recommended = manager.get_recommended_wordlists()
    
    if wordlist_name not in recommended:
        print(f"❌ Wordlist {wordlist_name} not found")
        return
    
    wordlist_path = recommended[wordlist_name]
    print(f"🔐 Processing passwords from: {wordlist_path}")
    
    # Get wordlist stats
    stats = manager.get_wordlist_stats(wordlist_path)
    print(f"📊 Wordlist stats: {stats}")
    
    # Process passwords (example: filter by length)
    filtered_passwords = []
    for password in manager.load_wordlist(wordlist_path, max_lines=10000):
        if 6 <= len(password) <= 12:  # Common password length requirements
            filtered_passwords.append(password)
    
    print(f"✅ Filtered {len(filtered_passwords)} passwords for {target_service}")
    
    # Save filtered list
    output_file = f"filtered_passwords_{target_service}.txt"
    with open(output_file, 'w') as f:
        for pwd in filtered_passwords:
            f.write(f"{pwd}\\n")
    
    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    process_passwords()
'''
    
    with open('/workspaces/sugarglitch-realops/seclists_password_processor.py', 'w') as f:
        f.write(password_processor)

def main():
    """Main function demonstrating SecLists integration"""
    print("🔗 SECLISTS INTEGRATION MANAGER")
    print("=" * 40)
    
    manager = SecListsManager()
    
    # Check if SecLists is available
    if not manager.seclists_dir.exists():
        print("📥 SecLists not found. Downloading...")
        if manager.download_seclists():
            print("✅ SecLists downloaded successfully!")
        else:
            print("❌ Failed to download SecLists")
            return
    else:
        print("✅ SecLists already available")
    
    # Show available categories
    print("\n📂 Available wordlist categories:")
    categories = manager.get_wordlist_categories()
    for category, files in categories.items():
        print(f"  {category}: {len(files)} wordlists")
    
    # Show recommended wordlists
    print("\n⭐ Recommended wordlists:")
    recommended = manager.get_recommended_wordlists()
    for name, path in list(recommended.items())[:10]:  # Show first 10
        stats = manager.get_wordlist_stats(path)
        if 'error' not in stats:
            print(f"  {name}: {stats.get('non_empty_lines', 0)} entries")
        else:
            print(f"  {name}: {stats['error']}")
    
    # Create custom wordlist example
    print("\n🔧 Creating custom wordlist example...")
    custom_sources = [
        'Discovery/Web-Content/common.txt',
        'Discovery/Web-Content/big.txt'
    ]
    
    if manager.create_custom_wordlist('custom_web_discovery.txt', custom_sources, max_per_source=500):
        print("✅ Custom wordlist created!")
    
    # Create integration examples
    print("\n📝 Creating integration examples...")
    create_integration_examples()
    print("✅ Integration examples created!")
    
    print("\n🎯 Integration complete! You can now use SecLists in your scripts.")
    print("\nNext steps:")
    print("1. Run: python seclists_directory_bruteforcer.py")
    print("2. Run: python seclists_password_processor.py")
    print("3. Integrate wordlists into your existing scripts")

if __name__ == "__main__":
    main()
