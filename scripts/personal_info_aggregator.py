#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Personal Information Aggregator
รวมข้อมูลส่วนตัวทั้งหมดจากโปรเจกต์และจัดหมวดหมู่
"""

import json
import os
import re
import glob
from pathlib import Path
from datetime import datetime
import chardet

# เพิ่ม imports สำหรับ PDF parsing
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    try:
        from pdfminer.high_level import extract_text
        from pdfminer.layout import LAParams
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False

class PersonalInfoAggregator:
    """Class สำหรับรวมข้อมูลส่วนตัวจากไฟล์ต่างๆ"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / "data"
        self.results = {
            "targets": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "total_files_processed": 0,
                "data_sources": []
            }
        }
        
        # Patterns สำหรับ regex extraction
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'(?:\+66|0)(?:\d{1,2}[-.\s]?\d{3}[-.\s]?\d{4}|\d{8,9})',
            "ig_id": r'"id":\s*"(\d+)"',
            "username": r'(?:@|username["\':]\s*["\']?)([a-zA-Z0-9._]{1,30})',
            "session": r'sessionid["\':=]\s*["\']?([a-zA-Z0-9%_-]{20,})',
            "location": r'(?:location|address|city)["\':]\s*["\']([^"\']+)',
            "password": r'(?:password|pass)["\':=]\s*["\']([^"\']{4,})'
        }
        
        # Target usernames ที่รู้จัก
        self.known_targets = ["alx.trading", "whatilove1728", "alx_trading"]
        
    def detect_encoding(self, file_path):
        """ตรวจสอบ encoding ของไฟล์"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # อ่าน 10KB แรก
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
        except:
            return 'utf-8'
    
    def read_text_file(self, file_path):
        """อ่านไฟล์ text โดย auto-detect encoding"""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            return ""
    
    def read_pdf_file(self, file_path):
        """อ่านไฟล์ PDF"""
        if not PDF_AVAILABLE:
            print(f"⚠️  PDF libraries not available for {file_path}")
            return ""
            
        try:
            # Try PyMuPDF first
            if 'fitz' in globals():
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text
            else:
                # Use pdfminer
                return extract_text(file_path, laparams=LAParams())
        except Exception as e:
            print(f"⚠️  Error reading PDF {file_path}: {e}")
            return ""
    
    def read_json_file(self, file_path):
        """อ่านไฟล์ JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading JSON {file_path}: {e}")
            return {}
    
    def read_html_file(self, file_path):
        """อ่านไฟล์ HTML"""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
                # Remove HTML tags for easier text processing
                import re
                text = re.sub(r'<[^>]+>', ' ', content)
                return text
        except Exception as e:
            print(f"⚠️  Error reading HTML {file_path}: {e}")
            return ""
    
    def extract_patterns(self, text, target_info=None):
        """Extract patterns จาก text"""
        extracted = {}
        
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if pattern_name in ['email', 'phone', 'location']:
                    extracted[pattern_name] = list(set(matches))  # Remove duplicates
                else:
                    extracted[pattern_name] = matches[0] if matches else None
        
        return extracted
    
    def find_target_in_text(self, text):
        """หา target username ในข้อความ"""
        text_lower = text.lower()
        for target in self.known_targets:
            if target.lower() in text_lower:
                return target.replace('_', '.')  # Normalize format
        return None
    
    def process_file(self, file_path):
        """ประมวลผลไฟล์แต่ละไฟล์"""
        # Silent processing to avoid broken pipe
        file_ext = Path(file_path).suffix.lower()
        content = ""
        
        if file_ext == '.json':
            data = self.read_json_file(file_path)
            content = json.dumps(data, indent=2) if data else ""
        elif file_ext == '.pdf':
            content = self.read_pdf_file(file_path)
        elif file_ext in ['.html', '.htm']:
            content = self.read_html_file(file_path)
        elif file_ext in ['.txt', '.md', '.py']:
            content = self.read_text_file(file_path)
        else:
            return None
        
        if not content:
            return None
        
        # Extract information
        extracted = self.extract_patterns(content)
        target_username = self.find_target_in_text(content)
        
        if extracted or target_username:
            result = {
                "source_file": str(file_path),
                "target_username": target_username,
                "extracted_data": extracted,
                "file_type": file_ext,
                "processed_at": datetime.now().isoformat()
            }
            return result
        
        return None
    
    def find_all_relevant_files(self):
        """หาไฟล์ทั้งหมดที่เกี่ยวข้อง"""
        patterns = [
            "**/*personal*",
            "**/*breach*", 
            "**/*chat*",
            "**/*alx*",
            "**/*whatilove*",
            "**/*dual_account*",
            "**/*sensitive*",
            "**/*.json",
            "**/*.txt",
            "**/*.pdf",
            "**/*.html",
            "data/**/*",
            "results/**/*",
            "reports/**/*",
            "intelligence/**/*",
            "extractions/**/*"
        ]
        
        files = set()
        for pattern in patterns:
            files.update(self.project_root.glob(pattern))
        
        # Filter only files (not directories)
        return [f for f in files if f.is_file()]
    
    def aggregate_target_data(self, file_results):
        """รวมข้อมูลของแต่ละ target"""
        targets = {}
        
        for result in file_results:
            if not result or not result.get('target_username'):
                continue
                
            username = result['target_username']
            if username not in targets:
                targets[username] = {
                    "username": username,
                    "email": [],
                    "phone": [],
                    "ig_id": None,
                    "sessions": [],
                    "location_history": [],
                    "breaches": [],
                    "chat_patterns": [],
                    "aliases": [],
                    "linked_accounts": [],
                    "flags": [],
                    "sources": []
                }
            
            target = targets[username]
            extracted = result.get('extracted_data', {})
            
            # Aggregate data
            if 'email' in extracted:
                target['email'].extend(extracted['email'])
            if 'phone' in extracted:
                target['phone'].extend(extracted['phone'])
            if 'ig_id' in extracted and extracted['ig_id']:
                target['ig_id'] = extracted['ig_id']
            if 'session' in extracted and extracted['session']:
                target['sessions'].append(extracted['session'])
            if 'location' in extracted:
                target['location_history'].extend(extracted['location'])
            if 'password' in extracted and extracted['password']:
                target['flags'].append("password_known")
            
            # Add source file
            target['sources'].append(result['source_file'])
        
        # Clean up and deduplicate
        for username, target in targets.items():
            target['email'] = list(set(target['email']))
            target['phone'] = list(set(target['phone']))
            target['sessions'] = list(set(target['sessions']))
            target['location_history'] = list(set(target['location_history']))
            target['flags'] = list(set(target['flags']))
            target['sources'] = list(set(target['sources']))
            
            # Add flags
            if len(target['email']) > 0 or len(target['phone']) > 0:
                target['flags'].append("high_value_target")
            if len(target['sessions']) > 0:
                target['flags'].append("session_available")
                
        return list(targets.values())
    
    def run(self):
        """รันการรวมข้อมูล"""
        print("🔥🔥🔥 SugarGlitch RealOps - Personal Info Aggregator 🔥🔥🔥")
        print("=" * 70)
        print(f"📅 Started: {datetime.now()}")
        print()
        
        # Find all relevant files
        print("🔍 Scanning for relevant files...")
        files = self.find_all_relevant_files()
        print(f"📁 Found {len(files)} files to process")
        print()
        
        # Process each file
        file_results = []
        processed_count = 0
        
        for file_path in files:
            try:
                result = self.process_file(file_path)
                if result:
                    file_results.append(result)
                processed_count += 1
                
                # Only show progress every 50 files to avoid spam
                if processed_count % 50 == 0:
                    print(f"⏳ Processed {processed_count}/{len(files)} files...")
                    
            except Exception as e:
                # Silent error handling to avoid broken pipe
                continue
        
        print(f"✅ Processed {processed_count} files total")
        print(f"📊 Found data in {len(file_results)} files")
        print()
        
        # Aggregate target data
        print("🧩 Aggregating target data...")
        targets = self.aggregate_target_data(file_results)
        
        # Update results
        self.results['targets'] = targets
        self.results['metadata']['total_files_processed'] = processed_count
        self.results['metadata']['data_sources'] = [r['source_file'] for r in file_results]
        
        # Save results
        output_file = self.data_dir / "realops_targets.json"
        self.data_dir.mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {output_file}")
        print()
        
        # Summary
        print("📋 AGGREGATION SUMMARY:")
        print("=" * 30)
        print(f"🎯 Total Targets: {len(targets)}")
        for target in targets:
            print(f"👤 {target['username']}:")
            print(f"   📧 Emails: {len(target['email'])}")
            print(f"   📱 Phones: {len(target['phone'])}")
            print(f"   🔐 Sessions: {len(target['sessions'])}")
            print(f"   🏷️  Flags: {', '.join(target['flags'])}")
            print()
        
        return output_file

def main():
    """Main function"""
    aggregator = PersonalInfoAggregator()
    output_file = aggregator.run()
    
    print("🚀 Personal information aggregation complete!")
    print(f"📄 Results saved to: {output_file}")
    
    # Show how to import in other modules
    print("\n💡 To use in other modules:")
    print("```python")
    print("import json")
    print("with open('data/realops_targets.json', 'r') as f:")
    print("    targets = json.load(f)")
    print("    for target in targets['targets']:")
    print("        print(f'Target: {target[\"username\"]}'')")
    print("```")

if __name__ == "__main__":
    main()
