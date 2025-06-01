#!/usr/bin/env python3
"""
🔗💾 SMART DATA INTEGRATION & ANALYSIS SYSTEM 2025 💾🔗
======================================================
- Integrate all existing Instagram data files
- Cross-reference target information
- Extract hidden conversation data
- Smart data fusion and correlation
- Comprehensive intelligence compilation

ระบบรวมข้อมูลและวิเคราะห์อัจฉริยะ!

Created by: น้องจิน (chin4d0ll) ♥️
For: Advanced Instagram Intelligence Operations
"""

import asyncio
import json
import sqlite3
import gzip
import pickle
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")

class SmartDataIntegrationSystem:
    """🔗 ระบบรวมข้อมูลอัจฉริยะ"""
    
    def __init__(self):
        self.workspace_path = Path(".")
        self.targets = ["whatilove1728", "alx.trading", "alx_trading"]
        
        self.integrated_data = {
            'targets': {},
            'conversations': {},
            'media': {},
            'relationships': {},
            'timeline': [],
            'intelligence': {}
        }
        
        self.processing_stats = {
            'files_processed': 0,
            'data_points_extracted': 0,
            'conversations_found': 0,
            'media_items_found': 0,
            'relationships_mapped': 0
        }
        
        self.log("🔗 Smart Data Integration System initialized")
    
    def log(self, message: str, level: str = "INFO"):
        """📝 Enhanced logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_codes = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m", 
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "RESET": "\033[0m"
        }
        
        colored_message = f"{color_codes.get(level, '')}{timestamp} - {message}{color_codes['RESET']}"
        print(colored_message)
    
    async def discover_data_files(self) -> Dict[str, List[Path]]:
        """🔍 Discover all data files by category"""
        self.log("🔍 Discovering data files in workspace...")
        
        file_categories = {
            'json_data': [],
            'database_files': [],
            'session_files': [],
            'extraction_results': [],
            'reports': [],
            'media_files': []
        }
        
        # Define patterns for each category
        patterns = {
            'json_data': ['*.json', '!*session*.json', '!*cookie*.json'],
            'database_files': ['*.db', '*.sqlite', '*.sqlite3'],
            'session_files': ['*session*.json', '*cookie*.json', '*auth*.json'],
            'extraction_results': ['*extract*.json', '*dm*.json', '*result*.json'],
            'reports': ['*.md', '*.txt', '*.log'],
            'media_files': ['*.jpg', '*.jpeg', '*.png', '*.mp4', '*.gif']
        }
        
        for category, category_patterns in patterns.items():
            for pattern in category_patterns:
                if pattern.startswith('!'):
                    # Exclude pattern - skip for now
                    continue
                    
                files = list(self.workspace_path.glob(pattern))
                
                # Filter out excluded patterns
                exclude_patterns = [p[1:] for p in category_patterns if p.startswith('!')]
                if exclude_patterns and category == 'json_data':
                    filtered_files = []
                    for f in files:
                        exclude = False
                        for exclude_pattern in exclude_patterns:
                            if f.match(exclude_pattern):
                                exclude = True
                                break
                        if not exclude:
                            filtered_files.append(f)
                    files = filtered_files
                
                file_categories[category].extend(files)
                
                if files:
                    self.log(f"📁 Found {len(files)} {category.replace('_', ' ')} files")
        
        return file_categories
    
    async def extract_target_data(self, file_path: Path) -> Optional[Dict]:
        """🎯 Extract target-specific data from files"""
        try:
            file_content = None
            target_data = {
                'source_file': str(file_path),
                'file_size': file_path.stat().st_size,
                'modified_time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'target_users': [],
                'conversations': [],
                'media_items': [],
                'user_profiles': {},
                'raw_data': {}
            }
            
            # Read file content based on type
            if file_path.suffix == '.json':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to parse JSON
                    try:
                        file_content = json.loads(content)
                    except json.JSONDecodeError:
                        # Try to repair and parse
                        repaired_content = await self.repair_json_content(content)
                        if repaired_content:
                            file_content = json.loads(repaired_content)
                        else:
                            self.log(f"⚠️ Could not parse JSON in {file_path.name}", "WARNING")
                            return None
                            
                except Exception as e:
                    self.log(f"❌ Error reading {file_path.name}: {e}", "ERROR")
                    return None
            
            elif file_path.suffix in ['.db', '.sqlite', '.sqlite3']:
                try:
                    file_content = await self.extract_database_data(file_path)
                except Exception as e:
                    self.log(f"❌ Error reading database {file_path.name}: {e}", "ERROR")
                    return None
            
            else:
                # Skip non-JSON, non-database files for now
                return None
            
            if not file_content:
                return None
            
            target_data['raw_data'] = file_content
            
            # Extract target users
            content_str = str(file_content).lower()
            for target in self.targets:
                if target.lower() in content_str:
                    target_data['target_users'].append(target)
            
            # Extract conversations and messages
            conversations = await self.extract_conversations_from_data(file_content)
            if conversations:
                target_data['conversations'] = conversations
                self.processing_stats['conversations_found'] += len(conversations)
            
            # Extract media items
            media_items = await self.extract_media_from_data(file_content)
            if media_items:
                target_data['media_items'] = media_items
                self.processing_stats['media_items_found'] += len(media_items)
            
            # Extract user profiles
            user_profiles = await self.extract_user_profiles_from_data(file_content)
            if user_profiles:
                target_data['user_profiles'] = user_profiles
            
            self.processing_stats['data_points_extracted'] += 1
            return target_data if target_data['target_users'] else None
            
        except Exception as e:
            self.log(f"💥 Error extracting target data from {file_path}: {e}", "ERROR")
            return None
    
    async def repair_json_content(self, content: str) -> Optional[str]:
        """🔧 Repair corrupted JSON content"""
        try:
            # Common repair strategies
            repairs = [
                lambda x: re.sub(r',(\s*[}\]])', r'\1', x),  # Remove trailing commas
                lambda x: re.sub(r'(\w+):', r'"\1":', x),    # Quote unquoted keys
                lambda x: x.replace("'", '"'),               # Single to double quotes
                lambda x: re.sub(r'[\x00-\x1f\x7f]', '', x), # Remove control chars
                lambda x: x[x.find('{'):x.rfind('}')+1] if '{' in x and '}' in x else x
            ]
            
            for repair_func in repairs:
                try:
                    repaired = repair_func(content)
                    json.loads(repaired)  # Test if valid
                    return repaired
                except:
                    continue
            
            return None
            
        except Exception:
            return None
    
    async def extract_database_data(self, db_path: Path) -> Dict:
        """🗄️ Extract data from database files"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            database_data = {'tables': {}}
            
            for table_name, in tables:
                try:
                    # Get table schema
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    # Get table data (limit to prevent memory issues)
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1000")
                    rows = cursor.fetchall()
                    
                    table_data = []
                    for row in rows:
                        row_dict = dict(zip(columns, row))
                        table_data.append(row_dict)
                    
                    database_data['tables'][table_name] = {
                        'columns': columns,
                        'data': table_data,
                        'row_count': len(table_data)
                    }
                    
                except Exception as e:
                    self.log(f"⚠️ Error reading table {table_name}: {e}", "WARNING")
            
            conn.close()
            return database_data
            
        except Exception as e:
            self.log(f"❌ Database extraction error: {e}", "ERROR")
            return {}
    
    async def extract_conversations_from_data(self, data: Any) -> List[Dict]:
        """💬 Extract conversation data from any data structure"""
        conversations = []
        
        def recursive_search(obj, path=""):
            if isinstance(obj, dict):
                # Look for conversation indicators
                if any(key in str(obj).lower() for key in ['message', 'dm', 'conversation', 'thread']):
                    if any(key in obj for key in ['text', 'content', 'body', 'message']):
                        conversation = {
                            'source_path': path,
                            'timestamp': obj.get('timestamp') or obj.get('created_time') or obj.get('date'),
                            'participants': [],
                            'messages': []
                        }
                        
                        # Extract participants
                        for key in ['participants', 'users', 'members']:
                            if key in obj:
                                conversation['participants'] = obj[key]
                                break
                        
                        # Extract messages
                        message_keys = ['messages', 'items', 'thread_items', 'data']
                        for key in message_keys:
                            if key in obj and isinstance(obj[key], list):
                                conversation['messages'] = obj[key]
                                break
                        
                        if conversation['messages'] or any(key in obj for key in ['text', 'content']):
                            conversations.append(conversation)
                
                # Recursively search nested objects
                for key, value in obj.items():
                    recursive_search(value, f"{path}.{key}" if path else key)
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_search(item, f"{path}[{i}]" if path else f"[{i}]")
        
        recursive_search(data)
        return conversations
    
    async def extract_media_from_data(self, data: Any) -> List[Dict]:
        """🖼️ Extract media items from data"""
        media_items = []
        
        def find_media(obj, path=""):
            if isinstance(obj, dict):
                # Look for media indicators
                if any(key in obj for key in ['url', 'src', 'image_url', 'video_url', 'media_url']):
                    media_item = {
                        'source_path': path,
                        'type': 'unknown',
                        'url': None,
                        'dimensions': {},
                        'caption': obj.get('caption') or obj.get('alt_text')
                    }
                    
                    # Determine media type and URL
                    for url_key in ['url', 'src', 'image_url', 'video_url', 'media_url']:
                        if url_key in obj:
                            media_item['url'] = obj[url_key]
                            if 'image' in url_key or any(ext in str(obj[url_key]).lower() for ext in ['.jpg', '.png', '.jpeg', '.gif']):
                                media_item['type'] = 'image'
                            elif 'video' in url_key or any(ext in str(obj[url_key]).lower() for ext in ['.mp4', '.mov', '.avi']):
                                media_item['type'] = 'video'
                            break
                    
                    # Extract dimensions
                    for dim_key in ['width', 'height']:
                        if dim_key in obj:
                            media_item['dimensions'][dim_key] = obj[dim_key]
                    
                    if media_item['url']:
                        media_items.append(media_item)
                
                # Recursive search
                for key, value in obj.items():
                    find_media(value, f"{path}.{key}" if path else key)
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_media(item, f"{path}[{i}]" if path else f"[{i}]")
        
        find_media(data)
        return media_items
    
    async def extract_user_profiles_from_data(self, data: Any) -> Dict:
        """👤 Extract user profile information"""
        profiles = {}
        
        def find_profiles(obj, path=""):
            if isinstance(obj, dict):
                # Look for profile indicators
                if any(key in obj for key in ['username', 'user_id', 'profile', 'account']):
                    profile = {}
                    
                    # Extract common profile fields
                    profile_fields = {
                        'username': ['username', 'user', 'account_name'],
                        'user_id': ['user_id', 'id', 'pk'],
                        'full_name': ['full_name', 'name', 'display_name'],
                        'bio': ['bio', 'biography', 'description'],
                        'follower_count': ['follower_count', 'followers'],
                        'following_count': ['following_count', 'following'],
                        'profile_pic_url': ['profile_pic_url', 'avatar', 'profile_picture'],
                        'is_verified': ['is_verified', 'verified'],
                        'is_private': ['is_private', 'private']
                    }
                    
                    for field, keys in profile_fields.items():
                        for key in keys:
                            if key in obj:
                                profile[field] = obj[key]
                                break
                    
                    if profile and profile.get('username'):
                        profiles[profile['username']] = profile
                
                # Recursive search
                for key, value in obj.items():
                    find_profiles(value, f"{path}.{key}" if path else key)
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    find_profiles(item, f"{path}[{i}]" if path else f"[{i}]")
        
        find_profiles(data)
        return profiles
    
    async def integrate_target_data(self, target_data_list: List[Dict]):
        """🔗 Integrate data for each target"""
        self.log("🔗 Integrating target data...")
        
        # Group data by target
        target_groups = defaultdict(list)
        for data in target_data_list:
            for target in data['target_users']:
                target_groups[target].append(data)
        
        # Process each target
        for target, target_files in target_groups.items():
            self.log(f"🎯 Processing target: {target}")
            
            integrated_target = {
                'username': target,
                'data_sources': [d['source_file'] for d in target_files],
                'conversations': [],
                'media_items': [],
                'profile_data': {},
                'timeline': [],
                'relationships': set(),
                'statistics': {
                    'total_conversations': 0,
                    'total_messages': 0,
                    'total_media': 0,
                    'date_range': {'earliest': None, 'latest': None}
                }
            }
            
            # Combine conversations
            all_conversations = []
            for file_data in target_files:
                all_conversations.extend(file_data['conversations'])
            
            # Deduplicate and sort conversations
            unique_conversations = {}
            for conv in all_conversations:
                # Create a simple hash for deduplication
                conv_hash = hash(str(conv.get('messages', [])[:3]))  # Use first 3 messages for identity
                if conv_hash not in unique_conversations:
                    unique_conversations[conv_hash] = conv
            
            integrated_target['conversations'] = list(unique_conversations.values())
            integrated_target['statistics']['total_conversations'] = len(integrated_target['conversations'])
            
            # Count total messages
            total_messages = sum(len(conv.get('messages', [])) for conv in integrated_target['conversations'])
            integrated_target['statistics']['total_messages'] = total_messages
            
            # Combine media items
            all_media = []
            for file_data in target_files:
                all_media.extend(file_data['media_items'])
            
            # Deduplicate media
            unique_media = {}
            for media in all_media:
                media_url = media.get('url', '')
                if media_url and media_url not in unique_media:
                    unique_media[media_url] = media
            
            integrated_target['media_items'] = list(unique_media.values())
            integrated_target['statistics']['total_media'] = len(integrated_target['media_items'])
            
            # Combine profile data
            for file_data in target_files:
                for username, profile in file_data['user_profiles'].items():
                    if username not in integrated_target['profile_data']:
                        integrated_target['profile_data'][username] = profile
                    else:
                        # Merge profile data
                        existing = integrated_target['profile_data'][username]
                        for key, value in profile.items():
                            if value and (key not in existing or not existing[key]):
                                existing[key] = value
            
            # Extract relationships
            for conv in integrated_target['conversations']:
                participants = conv.get('participants', [])
                for participant in participants:
                    if isinstance(participant, str):
                        integrated_target['relationships'].add(participant)
                    elif isinstance(participant, dict) and 'username' in participant:
                        integrated_target['relationships'].add(participant['username'])
            
            # Convert set to list for JSON serialization
            integrated_target['relationships'] = list(integrated_target['relationships'])
            self.processing_stats['relationships_mapped'] += len(integrated_target['relationships'])
            
            # Store integrated data
            self.integrated_data['targets'][target] = integrated_target
            
            self.log(f"✅ Integrated data for {target}: {total_messages} messages, {len(integrated_target['media_items'])} media, {len(integrated_target['relationships'])} relationships")
    
    async def generate_intelligence_summary(self) -> Dict:
        """🧠 Generate intelligence summary from integrated data"""
        self.log("🧠 Generating intelligence summary...")
        
        intelligence = {
            'timestamp': datetime.now().isoformat(),
            'targets_analyzed': list(self.integrated_data['targets'].keys()),
            'cross_target_analysis': {},
            'relationship_network': {},
            'communication_patterns': {},
            'content_analysis': {},
            'temporal_analysis': {}
        }
        
        # Cross-target relationship analysis
        all_relationships = set()
        target_relationships = {}
        
        for target, data in self.integrated_data['targets'].items():
            target_relationships[target] = set(data['relationships'])
            all_relationships.update(data['relationships'])
        
        # Find common connections
        if len(self.integrated_data['targets']) > 1:
            target_names = list(self.integrated_data['targets'].keys())
            for i, target1 in enumerate(target_names):
                for target2 in target_names[i+1:]:
                    common = target_relationships[target1] & target_relationships[target2]
                    if common:
                        intelligence['cross_target_analysis'][f"{target1}_vs_{target2}"] = {
                            'common_connections': list(common),
                            'unique_to_target1': list(target_relationships[target1] - target_relationships[target2]),
                            'unique_to_target2': list(target_relationships[target2] - target_relationships[target1])
                        }
        
        # Communication volume analysis
        for target, data in self.integrated_data['targets'].items():
            intelligence['communication_patterns'][target] = {
                'total_conversations': data['statistics']['total_conversations'],
                'total_messages': data['statistics']['total_messages'],
                'avg_messages_per_conversation': data['statistics']['total_messages'] / max(1, data['statistics']['total_conversations']),
                'unique_connections': len(data['relationships']),
                'media_sharing_frequency': data['statistics']['total_media']
            }
        
        self.integrated_data['intelligence'] = intelligence
        return intelligence
    
    async def save_integrated_data(self):
        """💾 Save integrated data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save main integrated data
        main_file = f"integrated_data_{timestamp}.json"
        with open(main_file, 'w', encoding='utf-8') as f:
            # Convert sets to lists for JSON serialization
            serializable_data = json.loads(json.dumps(self.integrated_data, default=str))
            json.dump(serializable_data, f, ensure_ascii=False, indent=2)
        
        self.log(f"💾 Integrated data saved: {main_file}")
        
        # Save individual target files
        for target, data in self.integrated_data['targets'].items():
            target_file = f"integrated_{target}_{timestamp}.json"
            with open(target_file, 'w', encoding='utf-8') as f:
                serializable_target_data = json.loads(json.dumps(data, default=str))
                json.dump(serializable_target_data, f, ensure_ascii=False, indent=2)
            
            self.log(f"💾 Target data saved: {target_file}")
        
        # Generate comprehensive report
        await self.generate_integration_report(timestamp)
    
    async def generate_integration_report(self, timestamp: str):
        """📋 Generate comprehensive integration report"""
        report_file = f"data_integration_report_{timestamp}.md"
        
        intelligence = self.integrated_data.get('intelligence', {})
        
        report_content = f"""# 🔗 SMART DATA INTEGRATION REPORT 2025
## Generated: {datetime.now().isoformat()}

---

## 📊 INTEGRATION SUMMARY

- **Files Processed**: {self.processing_stats['files_processed']}
- **Data Points Extracted**: {self.processing_stats['data_points_extracted']}
- **Conversations Found**: {self.processing_stats['conversations_found']}
- **Media Items Found**: {self.processing_stats['media_items_found']}
- **Relationships Mapped**: {self.processing_stats['relationships_mapped']}

---

## 🎯 TARGET ANALYSIS

"""
        
        for target, data in self.integrated_data['targets'].items():
            stats = data['statistics']
            report_content += f"""### {target}
- **Data Sources**: {len(data['data_sources'])} files
- **Conversations**: {stats['total_conversations']}
- **Messages**: {stats['total_messages']}
- **Media Items**: {stats['total_media']}
- **Unique Connections**: {len(data['relationships'])}
- **Average Messages per Conversation**: {stats['total_messages'] / max(1, stats['total_conversations']):.1f}

#### Connections:
{chr(10).join([f"- {conn}" for conn in data['relationships'][:10]])}
{'- ...' if len(data['relationships']) > 10 else ''}

"""
        
        if intelligence.get('cross_target_analysis'):
            report_content += """---

## 🔗 CROSS-TARGET ANALYSIS

"""
            for comparison, analysis in intelligence['cross_target_analysis'].items():
                report_content += f"""### {comparison.replace('_vs_', ' vs ')}
- **Common Connections**: {len(analysis['common_connections'])}
- **Unique to Target 1**: {len(analysis['unique_to_target1'])}
- **Unique to Target 2**: {len(analysis['unique_to_target2'])}

#### Common Connections:
{chr(10).join([f"- {conn}" for conn in analysis['common_connections'][:5]])}

"""
        
        report_content += """---

## 📁 FILES GENERATED

- Main integrated data: `integrated_data_[timestamp].json`
- Individual target files: `integrated_[target]_[timestamp].json`
- This report: `data_integration_report_[timestamp].md`

---

*Generated by Smart Data Integration System 2025*  
*Created by: น้องจิน (chin4d0ll) ♥️*
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.log(f"📋 Integration report generated: {report_file}")
    
    async def execute_smart_integration(self) -> Dict:
        """🚀 Execute complete smart data integration"""
        self.log("🚀 Starting smart data integration", "SUCCESS")
        self.log("=" * 60)
        
        start_time = time.time()
        
        # Discover data files
        file_categories = await self.discover_data_files()
        
        # Process relevant files
        target_data_list = []
        
        for category, files in file_categories.items():
            if category in ['json_data', 'database_files', 'extraction_results']:
                self.log(f"📁 Processing {category}: {len(files)} files")
                
                for file_path in files:
                    self.processing_stats['files_processed'] += 1
                    self.log(f"🔍 Processing: {file_path.name}")
                    
                    try:
                        target_data = await self.extract_target_data(file_path)
                        if target_data:
                            target_data_list.append(target_data)
                            self.log(f"✅ Data extracted from {file_path.name}")
                        else:
                            self.log(f"⚠️ No target data found in {file_path.name}")
                    except Exception as e:
                        self.log(f"❌ Error processing {file_path.name}: {e}", "ERROR")
        
        if not target_data_list:
            self.log("⚠️ No target data extracted from any files", "WARNING")
            return self.processing_stats
        
        # Integrate target data
        await self.integrate_target_data(target_data_list)
        
        # Generate intelligence summary
        await self.generate_intelligence_summary()
        
        # Save results
        await self.save_integrated_data()
        
        execution_time = time.time() - start_time
        self.log("\n" + "=" * 60)
        self.log("🏁 SMART DATA INTEGRATION COMPLETED", "SUCCESS")
        self.log(f"⏱️ Execution Time: {execution_time:.2f} seconds")
        self.log(f"🎯 Targets Integrated: {len(self.integrated_data['targets'])}")
        self.log(f"💬 Total Conversations: {sum(len(t['conversations']) for t in self.integrated_data['targets'].values())}")
        self.log(f"🔗 Total Relationships: {sum(len(t['relationships']) for t in self.integrated_data['targets'].values())}")
        self.log("=" * 60)
        
        return self.processing_stats

async def main():
    """🚀 Main execution function"""
    print("""
🔗💾 SMART DATA INTEGRATION SYSTEM 2025 💾🔗
============================================
Integrating and analyzing Instagram data...
    """)
    
    integration_system = SmartDataIntegrationSystem()
    results = await integration_system.execute_smart_integration()
    
    if results['data_points_extracted'] > 0:
        print(f"\n🎉 Successfully integrated {results['data_points_extracted']} data points! 🎉")
    else:
        print("\n⚠️ No data could be integrated. Check the report for details.")

if __name__ == "__main__":
    asyncio.run(main())
