#!/usr/bin/env python3
"""
💬 QUICK INSTAGRAM CHAT DEMO
Demo chat extraction and analysis
Shows potential chat data structure
"""

import json
import sys
import os
from datetime import datetime
import random

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        sys.exit(1)

class QuickChatDemo:
    def __init__(self):
        self.demo_data = {
            "conversations": [
                {"name": "john_trader", "timestamp": "2025-05-25T10:30:00", "extracted": True, "message_count": 45},
                {"name": "crypto_expert", "timestamp": "2025-05-25T09:15:00", "extracted": True, "message_count": 32},
                {"name": "investment_buddy", "timestamp": "2025-05-25T08:45:00", "extracted": True, "message_count": 67},
                {"name": "forex_mentor", "timestamp": "2025-05-24T22:30:00", "extracted": True, "message_count": 28},
                {"name": "trading_group", "timestamp": "2025-05-24T20:15:00", "extracted": True, "message_count": 89}
            ],
            "direct_messages": [
                {"conversation": "john_trader", "text": "Hey, did you see the market movement today?", "timestamp": "2025-05-25T10:30:00", "type": "received"},
                {"conversation": "john_trader", "text": "Yeah, incredible! Bitcoin is up 5%", "timestamp": "2025-05-25T10:31:00", "type": "sent"},
                {"conversation": "crypto_expert", "text": "Check out this new trading strategy", "timestamp": "2025-05-25T09:15:00", "type": "received"},
                {"conversation": "crypto_expert", "text": "Looks promising, let me analyze it", "timestamp": "2025-05-25T09:16:00", "type": "sent"},
                {"conversation": "investment_buddy", "text": "Portfolio update: +12% this week", "timestamp": "2025-05-25T08:45:00", "type": "received"},
                {"conversation": "forex_mentor", "text": "EUR/USD looking bullish", "timestamp": "2025-05-24T22:30:00", "type": "received"},
                {"conversation": "trading_group", "text": "Anyone trading TSLA options?", "timestamp": "2025-05-24T20:15:00", "type": "received"}
            ],
            "chat_metadata": {
                "total_conversations": 5,
                "total_messages": 271,
                "extraction_timestamp": datetime.now().isoformat(),
                "target_account": "alx.trading"
            }
        }
    
    def display_chat_overview(self):
        """Display chat overview"""
        safe_print("💬 INSTAGRAM CHAT OVERVIEW - alx.trading")
        safe_print("=" * 50)
        
        metadata = self.demo_data["chat_metadata"]
        safe_print(f"📊 Total Conversations: {metadata['total_conversations']}")
        safe_print(f"📝 Total Messages: {metadata['total_messages']}")
        safe_print(f"🎯 Target Account: {metadata['target_account']}")
        safe_print(f"⏰ Last Updated: {metadata['extraction_timestamp'][:19]}")
        safe_print()
        
        safe_print("🔥 ACTIVE CONVERSATIONS:")
        for conv in self.demo_data["conversations"]:
            status = "✅" if conv["extracted"] else "⏳"
            safe_print(f"{status} {conv['name']}: {conv['message_count']} messages")
        
        safe_print()
    
    def display_recent_messages(self):
        """Display recent messages"""
        safe_print("📱 RECENT MESSAGES:")
        safe_print("-" * 30)
        
        for msg in self.demo_data["direct_messages"]:
            direction = "→" if msg["type"] == "sent" else "←"
            safe_print(f"{direction} {msg['conversation']}: {msg['text']}")
            safe_print(f"   {msg['timestamp'][11:16]}")
            safe_print()
    
    def analyze_chat_patterns(self):
        """Analyze chat patterns"""
        safe_print("🔍 CHAT PATTERN ANALYSIS:")
        safe_print("-" * 30)
        
        # Contact analysis
        contacts = [conv["name"] for conv in self.demo_data["conversations"]]
        safe_print(f"📞 Unique Contacts: {len(contacts)}")
        
        # Message distribution
        msg_counts = [conv["message_count"] for conv in self.demo_data["conversations"]]
        avg_messages = sum(msg_counts) / len(msg_counts)
        safe_print(f"📊 Average Messages per Contact: {avg_messages:.1f}")
        
        most_active = max(self.demo_data["conversations"], key=lambda x: x["message_count"])
        safe_print(f"🔥 Most Active Contact: {most_active['name']} ({most_active['message_count']} messages)")
        
        # Keywords analysis
        all_text = " ".join([msg["text"] for msg in self.demo_data["direct_messages"]])
        trading_keywords = ["trading", "bitcoin", "market", "crypto", "portfolio", "investment", "forex"]
        found_keywords = [word for word in trading_keywords if word.lower() in all_text.lower()]
        
        safe_print(f"💰 Trading Keywords Found: {', '.join(found_keywords)}")
        safe_print()
    
    def generate_chat_intelligence(self):
        """Generate intelligence insights"""
        safe_print("🕵️ INTELLIGENCE INSIGHTS:")
        safe_print("-" * 30)
        
        insights = [
            "• Target shows active trading community engagement",
            "• High frequency communication about financial markets",
            "• Multiple contacts with trading/investment expertise",
            "• Regular discussion of cryptocurrency and forex",
            "• Portfolio performance tracking behavior observed",
            "• Active participation in trading groups",
            "• Strong network of financial advisors and mentors"
        ]
        
        for insight in insights:
            safe_print(insight)
        
        safe_print()
        
        # Risk assessment
        safe_print("⚠️ RISK ASSESSMENT:")
        safe_print("• Communication Style: Professional/Financial")
        safe_print("• Network Type: Trading/Investment Community") 
        safe_print("• Activity Level: High (271 total messages)")
        safe_print("• Risk Score: Medium (Financial discussions)")
        safe_print()
    
    def save_demo_data(self):
        """Save demo data to file"""
        filename = f"demo_chat_data_alx.trading_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.demo_data, f, indent=2, ensure_ascii=False)
        
        safe_print(f"💾 Demo data saved to: {filename}")
    
    def run_demo(self):
        """Run complete demo"""
        safe_print("🚀 INSTAGRAM CHAT ANALYSIS DEMO")
        safe_print("=" * 50)
        safe_print("📋 Demonstrating chat extraction capabilities")
        safe_print("🎯 Target: alx.trading account")
        safe_print("=" * 50)
        safe_print()
        
        self.display_chat_overview()
        self.display_recent_messages()
        self.analyze_chat_patterns()
        self.generate_chat_intelligence()
        self.save_demo_data()
        
        safe_print("✅ Chat analysis demo completed!")
        safe_print("🔄 Ready for live extraction with real Instagram data")

def main():
    demo = QuickChatDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
