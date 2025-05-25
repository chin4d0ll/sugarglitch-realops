#!/usr/bin/env python3
"""
📊 INSTAGRAM CHAT ANALYTICS & PATTERN ANALYSIS
Advanced analysis of extracted chat data
Target: alx.trading conversations
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import re
from collections import Counter, defaultdict
import sqlite3
import sys
import os

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class ChatAnalytics:
    def __init__(self, username="alx.trading"):
        self.username = username
        self.chat_data = None
        self.analysis_results = {
            "conversation_stats": {},
            "message_patterns": {},
            "contact_analysis": {},
            "behavioral_insights": {},
            "risk_indicators": {},
            "network_connections": {}
        }
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def load_chat_data(self):
        """Load chat data from various sources"""
        try:
            safe_print("📚 Loading chat data for analysis...")
            
            # Try to load from JSON files
            import glob
            chat_files = glob.glob(f"instagram_chats_{self.username}_*.json")
            
            if chat_files:
                latest_file = max(chat_files, key=os.path.getctime)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.chat_data = json.load(f)
                safe_print(f"✅ Loaded chat data from: {latest_file}")
                return True
            
            # Try to load from database
            db_file = f"instagram_chats_{self.username}.db"
            if os.path.exists(db_file):
                self.load_from_database(db_file)
                safe_print(f"✅ Loaded chat data from database: {db_file}")
                return True
            
            safe_print("❌ No chat data found!")
            return False
            
        except Exception as e:
            safe_print(f"❌ Failed to load chat data: {e}")
            return False
    
    def load_from_database(self, db_file):
        """Load chat data from SQLite database"""
        try:
            conn = sqlite3.connect(db_file)
            
            # Load conversations
            conversations_df = pd.read_sql_query("SELECT * FROM conversations", conn)
            conversations = conversations_df.to_dict('records')
            
            # Load messages
            messages_df = pd.read_sql_query("SELECT * FROM messages", conn)
            messages = messages_df.to_dict('records')
            
            self.chat_data = {
                "conversations": conversations,
                "direct_messages": messages,
                "chat_metadata": {
                    "total_conversations": len(conversations),
                    "total_messages": len(messages)
                }
            }
            
            conn.close()
            
        except Exception as e:
            safe_print(f"⚠️ Database loading error: {e}")
    
    def analyze_conversation_patterns(self):
        """Analyze conversation patterns and statistics"""
        try:
            safe_print("🔍 Analyzing conversation patterns...")
            
            if not self.chat_data or not self.chat_data.get("conversations"):
                safe_print("⚠️ No conversation data available")
                return False
            
            conversations = self.chat_data["conversations"]
            messages = self.chat_data.get("direct_messages", [])
            
            # Basic statistics
            stats = {
                "total_conversations": len(conversations),
                "total_messages": len(messages),
                "active_conversations": len([c for c in conversations if c.get("extracted", False)]),
                "conversation_names": [c.get("name", "Unknown") for c in conversations]
            }
            
            # Message distribution by conversation
            message_distribution = defaultdict(int)
            for msg in messages:
                conversation = msg.get("conversation", "Unknown")
                message_distribution[conversation] += 1
            
            stats["message_distribution"] = dict(message_distribution)
            stats["most_active_conversations"] = sorted(message_distribution.items(), 
                                                      key=lambda x: x[1], reverse=True)[:5]
            
            self.analysis_results["conversation_stats"] = stats
            
            safe_print(f"✅ Analyzed {stats['total_conversations']} conversations")
            safe_print(f"📊 Total messages: {stats['total_messages']}")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Conversation analysis failed: {e}")
            return False
    
    def analyze_message_content(self):
        """Analyze message content and patterns"""
        try:
            safe_print("📝 Analyzing message content...")
            
            messages = self.chat_data.get("direct_messages", [])
            if not messages:
                safe_print("⚠️ No message data available")
                return False
            
            # Extract text content
            message_texts = [msg.get("text", "") for msg in messages if msg.get("text")]
            
            # Content analysis
            content_analysis = {
                "total_characters": sum(len(text) for text in message_texts),
                "average_message_length": sum(len(text) for text in message_texts) / len(message_texts) if message_texts else 0,
                "longest_message": max(message_texts, key=len) if message_texts else "",
                "shortest_message": min(message_texts, key=len) if message_texts else ""
            }
            
            # Word frequency analysis
            all_words = []
            for text in message_texts:
                words = re.findall(r'\b\w+\b', text.lower())
                all_words.extend(words)
            
            word_freq = Counter(all_words)
            content_analysis["most_common_words"] = word_freq.most_common(20)
            content_analysis["unique_words"] = len(set(all_words))
            content_analysis["total_words"] = len(all_words)
            
            # Pattern detection
            patterns = {
                "urls": len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' '.join(message_texts))),
                "emails": len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' '.join(message_texts))),
                "phone_numbers": len(re.findall(r'\b\d{3}-\d{3}-\d{4}\b|\b\d{10}\b', ' '.join(message_texts))),
                "mentions": len(re.findall(r'@\w+', ' '.join(message_texts)))
            }
            
            content_analysis["patterns"] = patterns
            
            self.analysis_results["message_patterns"] = content_analysis
            
            safe_print(f"✅ Analyzed {len(message_texts)} messages")
            safe_print(f"📊 Average message length: {content_analysis['average_message_length']:.1f} characters")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Message content analysis failed: {e}")
            return False
    
    def analyze_behavioral_patterns(self):
        """Analyze behavioral patterns and insights"""
        try:
            safe_print("🧠 Analyzing behavioral patterns...")
            
            conversations = self.chat_data.get("conversations", [])
            messages = self.chat_data.get("direct_messages", [])
            
            # Contact analysis
            contact_patterns = {
                "unique_contacts": len(set(c.get("name", "Unknown") for c in conversations)),
                "contact_names": [c.get("name", "Unknown") for c in conversations],
                "most_contacted": None
            }
            
            # Message frequency by contact
            contact_frequency = defaultdict(int)
            for msg in messages:
                conversation = msg.get("conversation", "Unknown")
                contact_frequency[conversation] += 1
            
            if contact_frequency:
                most_contacted = max(contact_frequency.items(), key=lambda x: x[1])
                contact_patterns["most_contacted"] = most_contacted
            
            # Risk indicators
            risk_indicators = {
                "suspicious_patterns": [],
                "risk_score": 0,
                "flagged_conversations": []
            }
            
            # Check for suspicious patterns
            all_text = ' '.join([msg.get("text", "") for msg in messages])
            
            suspicious_keywords = ['password', 'login', 'hack', 'access', 'credentials', 'account', 'verify', 'urgent']
            for keyword in suspicious_keywords:
                if keyword.lower() in all_text.lower():
                    risk_indicators["suspicious_patterns"].append(keyword)
                    risk_indicators["risk_score"] += 1
            
            # Behavioral insights
            insights = {
                "communication_style": "active" if len(messages) > 50 else "moderate" if len(messages) > 10 else "limited",
                "network_size": len(conversations),
                "engagement_level": "high" if len(messages) / max(len(conversations), 1) > 10 else "moderate"
            }
            
            self.analysis_results["contact_analysis"] = contact_patterns
            self.analysis_results["risk_indicators"] = risk_indicators
            self.analysis_results["behavioral_insights"] = insights
            
            safe_print(f"✅ Behavioral analysis completed")
            safe_print(f"🎯 Risk score: {risk_indicators['risk_score']}")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Behavioral analysis failed: {e}")
            return False
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        try:
            safe_print("📋 Generating analytics report...")
            
            report_file = f"chat_analytics_report_{self.username}_{self.timestamp}.json"
            
            # Compile full report
            full_report = {
                "target": self.username,
                "analysis_timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_conversations": self.analysis_results.get("conversation_stats", {}).get("total_conversations", 0),
                    "total_messages": self.analysis_results.get("conversation_stats", {}).get("total_messages", 0),
                    "risk_score": self.analysis_results.get("risk_indicators", {}).get("risk_score", 0),
                    "network_size": self.analysis_results.get("behavioral_insights", {}).get("network_size", 0)
                },
                "detailed_analysis": self.analysis_results
            }
            
            # Save report
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(full_report, f, indent=2, ensure_ascii=False)
            
            safe_print(f"✅ Analytics report saved: {report_file}")
            
            # Print summary
            safe_print("\n" + "="*50)
            safe_print("📊 CHAT ANALYTICS SUMMARY")
            safe_print("="*50)
            
            summary = full_report["summary"]
            for key, value in summary.items():
                safe_print(f"{key.replace('_', ' ').title()}: {value}")
            
            # Print top insights
            if "most_active_conversations" in self.analysis_results.get("conversation_stats", {}):
                safe_print("\n🔥 Most Active Conversations:")
                for conv, count in self.analysis_results["conversation_stats"]["most_active_conversations"]:
                    safe_print(f"  • {conv}: {count} messages")
            
            if "most_common_words" in self.analysis_results.get("message_patterns", {}):
                safe_print("\n💬 Most Common Words:")
                for word, count in self.analysis_results["message_patterns"]["most_common_words"][:5]:
                    safe_print(f"  • {word}: {count}")
            
            safe_print("="*50)
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Report generation failed: {e}")
            return False
    
    def run_full_analysis(self):
        """Run complete chat analytics workflow"""
        try:
            safe_print("🚀 STARTING CHAT ANALYTICS")
            safe_print("=" * 50)
            safe_print(f"🎯 Target: {self.username}")
            safe_print(f"⏰ Timestamp: {self.timestamp}")
            safe_print("=" * 50)
            
            # Load data
            if not self.load_chat_data():
                safe_print("❌ Failed to load chat data!")
                return False
            
            # Run analyses
            self.analyze_conversation_patterns()
            self.analyze_message_content()
            self.analyze_behavioral_patterns()
            
            # Generate report
            if not self.generate_analytics_report():
                safe_print("❌ Failed to generate report!")
                return False
            
            safe_print("🎉 CHAT ANALYTICS COMPLETED!")
            return True
            
        except Exception as e:
            safe_print(f"❌ Analytics workflow failed: {e}")
            return False

def main():
    """Main execution"""
    analytics = ChatAnalytics()
    success = analytics.run_full_analysis()
    
    if success:
        safe_print("✅ Chat analytics completed successfully!")
        sys.exit(0)
    else:
        safe_print("❌ Chat analytics failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
