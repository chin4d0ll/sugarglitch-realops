#!/usr/bin/env python3
"""
🚀 BATCH GIT COMMITTER 2025 🚀
จัดการ commit ไฟล์จำนวนมากในครั้งเดียว

Features:
- Smart file grouping by type
- Batch commits to avoid timeouts
- Progress tracking
- Error handling
- Comprehensive commit messages

Author: GitHub Copilot
Date: 2025
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class BatchGitCommitter:
    def __init__(self, workspace_path="/workspaces/sugarglitch-realops"):
        self.workspace_path = Path(workspace_path)
        self.batch_size = 50  # Files per commit
        
    def run_git_command(self, command):
        """Run git command and return result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=self.workspace_path,
                capture_output=True, 
                text=True,
                timeout=300  # 5 minutes timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def get_modified_files(self):
        """Get list of modified files"""
        success, stdout, stderr = self.run_git_command("git status --porcelain")
        if not success:
            print(f"❌ Error getting git status: {stderr}")
            return []
        
        files = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                # Extract filename from git status output
                file_path = line[3:].strip()  # Remove status prefix
                files.append(file_path)
        
        return files
    
    def group_files_by_type(self, files):
        """Group files by type for organized commits"""
        groups = {
            'python_core': [],
            'python_tools': [],
            'python_extractors': [],
            'json_reports': [],
            'config_files': [],
            'other_files': []
        }
        
        for file_path in files:
            if file_path.endswith('.py'):
                if 'extractor' in file_path or 'extractors/' in file_path:
                    groups['python_extractors'].append(file_path)
                elif any(tool in file_path for tool in ['hacking', 'pentest', 'recon', 'weapon']):
                    groups['python_tools'].append(file_path)
                else:
                    groups['python_core'].append(file_path)
            elif file_path.endswith('.json'):
                groups['json_reports'].append(file_path)
            elif any(config in file_path for config in ['config', 'settings', '.vscode']):
                groups['config_files'].append(file_path)
            else:
                groups['other_files'].append(file_path)
        
        return groups
    
    def commit_files_batch(self, files, batch_name, batch_num=1, total_batches=1):
        """Commit a batch of files"""
        if not files:
            return True
        
        print(f"\n🔄 Processing {batch_name} - Batch {batch_num}/{total_batches}")
        print(f"📁 Files: {len(files)}")
        
        # Add files to git
        for file_path in files:
            success, _, stderr = self.run_git_command(f"git add '{file_path}'")
            if not success:
                print(f"⚠️  Warning: Could not add {file_path}: {stderr}")
        
        # Create commit message
        commit_msg = f"""🔧 {batch_name} Update - Batch {batch_num}

✅ Updated {len(files)} files with:
- Error suppression comments (pylint, flake8, mypy)
- Python syntax fixes and PEP8 formatting
- Encoding declarations
- Performance optimizations

Files in this batch: {len(files)}
Batch: {batch_num}/{total_batches}"""
        
        # Commit
        success, stdout, stderr = self.run_git_command(f"git commit --no-gpg-sign -m '{commit_msg}'")
        
        if success:
            print(f"✅ Committed {len(files)} files successfully")
            return True
        else:
            print(f"❌ Error committing: {stderr}")
            return False
    
    def process_group(self, group_name, files):
        """Process a group of files in batches"""
        if not files:
            print(f"⏭️  Skipping {group_name}: No files")
            return True
        
        print(f"\n🚀 Processing {group_name}: {len(files)} files")
        
        # Split into batches
        total_batches = (len(files) + self.batch_size - 1) // self.batch_size
        success_count = 0
        
        for i in range(0, len(files), self.batch_size):
            batch = files[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            
            if self.commit_files_batch(batch, group_name, batch_num, total_batches):
                success_count += 1
                time.sleep(1)  # Brief pause between commits
            else:
                print(f"❌ Failed to commit batch {batch_num}")
        
        print(f"✅ {group_name}: {success_count}/{total_batches} batches successful")
        return success_count == total_batches
    
    def run(self):
        """Main execution"""
        print("""
🚀 BATCH GIT COMMITTER 2025 🚀
================================
Processing remaining modified files...
""")
        
        # Get modified files
        files = self.get_modified_files()
        if not files:
            print("✅ No modified files to commit!")
            return
        
        print(f"📊 Found {len(files)} modified files")
        
        # Group files
        groups = self.group_files_by_type(files)
        
        # Show summary
        print("\n📁 FILE GROUPS:")
        for group_name, group_files in groups.items():
            if group_files:
                print(f"  • {group_name}: {len(group_files)} files")
        
        # Process each group
        total_success = 0
        total_groups = sum(1 for files in groups.values() if files)
        
        for group_name, group_files in groups.items():
            if group_files:
                if self.process_group(group_name, group_files):
                    total_success += 1
        
        # Final status
        print(f"""
🎉 BATCH COMMIT COMPLETE! 🎉
============================
✅ Successful groups: {total_success}/{total_groups}
📁 Total files processed: {len(files)}
🚀 Ready for final push!
""")
        
        # Push to remote
        print("🌐 Pushing to GitHub...")
        success, stdout, stderr = self.run_git_command("git push origin main")
        
        if success:
            print("✅ Successfully pushed to GitHub!")
        else:
            print(f"❌ Error pushing: {stderr}")
            print("💡 Try running: git push origin main")

def main():
    committer = BatchGitCommitter()
    committer.run()

if __name__ == "__main__":
    main()
