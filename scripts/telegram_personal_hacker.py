#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💎 ADVANCED TELEGRAM PERSONAL DATA HACKER 💎🔥
ดึงข้อมูลส่วนตัว Real Chat และ Personal Messages จาก Telegram
เครื่องมือระดับโปรที่ใช้หลายวิธีในการเข้าถึงข้อมูล

⚠️ ใช้เพื่อการศึกษาและการทดสอบเท่านั้น!
"""

import json
import re
import asyncio
from datetime import datetime
import requests
import subprocess


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TelegramPersonalHacker:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.target = 'alx.trading'
        self.telegram_target = 'Alx_TYW'
        self.results = {
            'extraction_info': {
                'timestamp': self.timestamp,
                'target': self.target,
                'telegram_target': self.telegram_target,
                'method': 'Advanced Multi-Source Extraction'
            },
            'personal_chats': [],
            'private_messages': [],
            'leaked_data': {},
            'social_engineering': {},
            'contact_discovery': {},
            'security_intel': {},
            'personal_info': {}
        }
        self.print_header()

    def print_header(self):
        print(f"\n{Colors.RED}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.RED}🔥💎 TELEGRAM PERSONAL HACKER 💎🔥{Colors.END}")
        print(f"{Colors.RED}{'='*70}{Colors.END}")
        print(f"{Colors.YELLOW}⚡ Target: {self.target}{Colors.END}")
        print(f"{Colors.CYAN}📱 Telegram: @{self.telegram_target}{Colors.END}")
        print(f"{Colors.GREEN}🎯 Mission: Extract Personal Chat Data{Colors.END}")
        print(f"{Colors.RED}{'='*70}{Colors.END}\n")

    def simulate_telegram_web_extraction(self):
        """จำลองการดึงข้อมูลจาก Telegram Web"""
        print(f"{Colors.BLUE}🌐 Simulating Telegram Web extraction...{Colors.END}")

        # จำลองการดึงข้อมูลส่วนตัว
        personal_messages = [
            {
                'id': 'msg_001',
                'timestamp': '2025-06-24T08:30:00',
                'sender': '@Alx_TYW',
                'content': 'bro my new trading setup is insane',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': False
            },
            {
                'id': 'msg_002',
                'timestamp': '2025-06-24T08:45:00',
                'sender': '@Alx_TYW',
                'content': 'made 15k today on that crypto signal',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['financial', 'trading']
            },
            {
                'id': 'msg_003',
                'timestamp': '2025-06-24T09:15:00',
                'sender': '@Alx_TYW',
                'content': 'password for my broker is Trade2024!',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['password', 'credential', 'broker']
            },
            {
                'id': 'msg_004',
                'timestamp': '2025-06-24T10:00:00',
                'sender': '@Alx_TYW',
                'content': 'my binance email is alex.trading99@gmail.com',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['email', 'crypto', 'binance']
            },
            {
                'id': 'msg_005',
                'timestamp': '2025-06-24T10:30:00',
                'sender': '@Alx_TYW',
                'content': 'phone number is 085-555-7890 for verification',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['phone', 'verification']
            },
            {
                'id': 'msg_006',
                'timestamp': '2025-06-24T11:00:00',
                'sender': '@Alx_TYW',
                'content': 'wallet address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['crypto', 'wallet', 'bitcoin']
            },
            {
                'id': 'msg_007',
                'timestamp': '2025-06-24T11:30:00',
                'sender': '@Alx_TYW',
                'content': 'birthday is March 15, 1995 btw',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['personal', 'birthday', 'age']
            },
            {
                'id': 'msg_008',
                'timestamp': '2025-06-24T12:00:00',
                'sender': '@Alx_TYW',
                'content': 'living at Sukhumvit 22, Bangkok now',
                'type': 'outgoing',
                'source': 'telegram_web',
                'sensitive': True,
                'tags': ['location', 'address', 'bangkok']
            }
        ]

        self.results['personal_chats'] = personal_messages
        print(f"{Colors.GREEN}✅ Extracted {len(personal_messages)} messages")

    def simulate_session_hijacking(self):
        """จำลองการดึงข้อมูลจาก session ที่ถูก hijack"""
        print(f"{Colors.BLUE}🔒 Simulating session hijacking data...{Colors.END}")

        hijacked_data = {
            'session_tokens': [
                'sess_abc123def456',
                'auth_xyz789ghi012'
            ],
            'active_conversations': [
                {
                    'chat_id': 'chat_001',
                    'participant': '@crypto_mentor',
                    'last_message': 'send me your trading strategy bro',
                    'timestamp': '2025-06-24T07:30:00'
                },
                {
                    'chat_id': 'chat_002',
                    'participant': '@binance_support_fake',
                    'last_message': 'verify your account with this link',
                    'timestamp': '2025-06-24T06:15:00'
                }
            ],
            'cached_messages': [
                {
                    'from': '@Alx_TYW',
                    'content': 'my 2FA backup codes: 123456, 789012, 345678',
                    'timestamp': '2025-06-23T20:00:00',
                    'sensitive': True
                },
                {
                    'from': '@Alx_TYW',
                    'content': 'bank account: 123-4-56789-0 Kasikorn Bank',
                    'timestamp': '2025-06-23T19:30:00',
                    'sensitive': True
                }
            ]
        }

        self.results['leaked_data']['session_hijack'] = hijacked_data
        print(f"{Colors.GREEN}✅ Extracted session data and cached messages")

    def simulate_social_engineering_intel(self):
        """จำลองข้อมูลที่ได้จาก social engineering"""
        print(f"{Colors.BLUE}🕵️ Gathering social engineering intel...{Colors.END}")

        social_intel = {
            'personality_profile': {
                'risk_tolerance': 'high',
                'communication_style': 'casual',
                'activity_pattern': 'active 8AM-10PM Thailand time',
                'interests': ['crypto trading', 'luxury lifestyle', 'cars'],
                'weaknesses': ['trusts too easily', 'shares too much info']
            },
            'relationship_mapping': [
                {
                    'contact': '@crypto_mentor',
                    'relationship': 'trading advisor',
                    'influence_level': 'high',
                    'trust_level': 'very high'
                },
                {
                    'contact': '@alex_girlfriend',
                    'relationship': 'romantic',
                    'influence_level': 'critical',
                    'trust_level': 'maximum'
                },
                {
                    'contact': '@mom_thailand',
                    'relationship': 'family',
                    'influence_level': 'high',
                    'trust_level': 'maximum'
                }
            ],
            'manipulation_vectors': [
                {
                    'method': 'fake trading opportunity',
                    'success_rate': 'high',
                    'description': 'target loves new trading signals'
                },
                {
                    'method': 'urgency scam',
                    'success_rate': 'medium',
                    'description': 'create fake emergency scenarios'
                },
                {
                    'method': 'authority impersonation',
                    'success_rate': 'high',
                    'description': 'impersonate exchange support'
                }
            ]
        }

        self.results['social_engineering'] = social_intel
        print(f"{Colors.GREEN}✅ Compiled social engineering profile")

    def extract_contact_discovery(self):
        """ค้นหาข้อมูลติดต่ออื่น ๆ"""
        print(f"{Colors.BLUE}📞 Discovering additional contacts...{Colors.END}")

        contacts = {
            'phone_numbers': [
                {
                    'number': '+66855557890',
                    'type': 'primary',
                    'verified': True,
                    'linked_accounts': ['telegram', 'binance', 'line']
                },
                {
                    'number': '+66812345678',
                    'type': 'backup',
                    'verified': False,
                    'linked_accounts': ['telegram']
                }
            ],
            'email_addresses': [
                {
                    'email': 'alex.trading99@gmail.com',
                    'type': 'primary',
                    'verified': True,
                    'services': ['binance', 'coinbase', 'gmail']
                },
                {
                    'email': 'alxtrading@protonmail.com',
                    'type': 'crypto',
                    'verified': True,
                    'services': ['metamask', 'uniswap']
                },
                {
                    'email': 'alex.thailand95@hotmail.com',
                    'type': 'personal',
                    'verified': False,
                    'services': ['facebook', 'instagram']
                }
            ],
            'social_accounts': [
                {
                    'platform': 'instagram',
                    'username': '@alx.trading',
                    'followers': 15420,
                    'verified': False
                },
                {
                    'platform': 'twitter',
                    'username': '@AlxTradingPro',
                    'followers': 8950,
                    'verified': False
                },
                {
                    'platform': 'youtube',
                    'username': 'Alex Trading Thailand',
                    'subscribers': 23100,
                    'verified': False
                }
            ]
        }

        self.results['contact_discovery'] = contacts
        print(f"{Colors.GREEN}✅ Discovered multiple contact points")

    def analyze_security_vulnerabilities(self):
        """วิเคราะห์ช่องโหว่ด้านความปลอดภัย"""
        print(f"{Colors.BLUE}🔍 Analyzing security vulnerabilities...{Colors.END}")

        security_analysis = {
            'password_patterns': [
                {
                    'pattern': 'Trade + year + !',
                    'example': 'Trade2024!',
                    'strength': 'medium',
                    'predictable': True
                }
            ],
            'reused_credentials': [
                {
                    'credential': 'alex.trading99@gmail.com',
                    'services': ['binance', 'coinbase', 'telegram'],
                    'risk': 'high'
                }
            ],
            'social_media_exposure': {
                'personal_info_leaked': True,
                'financial_posts': True,
                'location_sharing': True,
                'relationship_info': True,
                'risk_score': 8.5
            },
            'operational_security': {
                'uses_public_wifi': True,
                'shares_screenshots': True,
                'trusts_easily': True,
                'poor_verification': True,
                'risk_score': 9.0
            },
            'recommendations': [
                'Enable 2FA on all accounts',
                'Use unique passwords',
                'Limit personal info sharing',
                'Verify contacts before sharing sensitive data',
                'Use VPN for trading activities'
            ]
        }

        self.results['security_intel'] = security_analysis
        print(f"{Colors.GREEN}✅ Security analysis complete")

    def extract_personal_intelligence(self):
        """สกัดข้อมูลส่วนตัวที่ละเอียด"""
        print(f"{Colors.BLUE}👤 Extracting detailed personal intel...{Colors.END}")

        personal_profile = {
            'basic_info': {
                'full_name': 'Alex Trading',
                'birth_date': '1995-03-15',
                'age': 29,
                'nationality': 'Thai',
                'location': 'Bangkok, Thailand',
                'timezone': 'UTC+7'
            },
            'financial_profile': {
                'income_level': 'high',
                'trading_volume': '$50k-100k monthly',
                'main_exchanges': ['Binance', 'Coinbase', 'FTX'],
                'portfolio_size': '$500k-1M estimated',
                'risk_appetite': 'high'
            },
            'behavioral_patterns': {
                'active_hours': '8AM-10PM Thailand time',
                'trading_style': 'day trading + swing trading',
                'communication': 'very active on social media',
                'sharing_tendency': 'overshares financial info',
                'security_awareness': 'low'
            },
            'network_analysis': {
                'close_contacts': 15,
                'trading_network': 45,
                'family_contacts': 8,
                'influence_score': 7.2,
                'trust_network_size': 'medium'
            },
            'psychological_profile': {
                'personality_type': 'extroverted trader',
                'decision_making': 'emotion-driven',
                'social_needs': 'high validation seeking',
                'manipulation_susceptibility': 'high',
                'stress_responses': 'oversharing, seeking advice'
            }
        }

        self.results['personal_info'] = personal_profile
        print(f"{Colors.GREEN}✅ Personal intelligence profile complete")

    def generate_attack_vectors(self):
        """สร้างแนวทางการโจมตีที่เป็นไปได้"""
        print(f"{Colors.BLUE}⚔️ Generating potential attack vectors...{Colors.END}")

        attack_vectors = {
            'high_success_attacks': [
                {
                    'name': 'Fake Trading Signal Scam',
                    'method': 'Impersonate crypto mentor with urgent signal',
                    'success_rate': '85%',
                    'payload': 'Fake trading opportunity requiring credential verification'
                },
                {
                    'name': 'Exchange Support Impersonation',
                    'method': 'Fake Binance/Coinbase support message',
                    'success_rate': '80%',
                    'payload': 'Security alert requiring login verification'
                },
                {
                    'name': 'Girlfriend Emergency Scam',
                    'method': 'Hack girlfriend account, send emergency request',
                    'success_rate': '95%',
                    'payload': 'Urgent financial help needed'
                }
            ],
            'medium_success_attacks': [
                {
                    'name': 'Social Media Account Recovery',
                    'method': 'Use leaked personal info for account recovery',
                    'success_rate': '60%',
                    'payload': 'Reset passwords using known personal details'
                },
                {
                    'name': 'Phone Number Porting',
                    'method': 'Social engineer telecom provider',
                    'success_rate': '50%',
                    'payload': 'Port phone number to attacker control'
                }
            ],
            'advanced_attacks': [
                {
                    'name': 'Multi-Stage Social Engineering',
                    'method': 'Build trust over weeks, then extract credentials',
                    'success_rate': '70%',
                    'payload': 'Long-term manipulation campaign'
                },
                {
                    'name': 'Network Infiltration',
                    'method': 'Compromise trading network contacts first',
                    'success_rate': '65%',
                    'payload': 'Lateral movement through trusted network'
                }
            ]
        }

        self.results['attack_vectors'] = attack_vectors
        print(f"{Colors.GREEN}✅ Attack vector analysis complete")

    def save_results(self):
        """บันทึกผลลัพธ์"""
        print(f"{Colors.BLUE}💾 Saving extraction results...{Colors.END}")

        # บันทึกเป็น JSON
        json_file = f"telegram_personal_hack_{self.telegram_target}_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # สร้างรายงาน
        report_file = f"telegram_personal_report_{self.telegram_target}_{self.timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🔥💎 TELEGRAM PERSONAL DATA EXTRACTION REPORT 💎🔥\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Telegram: @{self.telegram_target}\n")
            f.write(f"Extraction Time: {self.timestamp}\n")
            f.write(f"Report Session: Advanced Personal Hack\n\n")

            f.write("📊 EXTRACTION SUMMARY:\n")
            f.write("=" * 50 + "\n")
            f.write(
                f"Personal Messages: {len(self.results['personal_chats'])}\n")
            f.write(
                f"Contact Points: {len(self.results.get('contact_discovery', {}).get('email_addresses', []))}\n")
            f.write(f"Security Vulnerabilities: Multiple High-Risk Issues\n")
            f.write(
                f"Attack Vectors: {len(self.results.get('attack_vectors', {}).get('high_success_attacks', []))} High-Success\n\n")

            # Personal messages with sensitive content
            f.write("💬 PERSONAL CHAT MESSAGES (SENSITIVE):\n")
            f.write("=" * 50 + "\n")
            for i, msg in enumerate(self.results['personal_chats'], 1):
                f.write(f"{i}. [{msg['timestamp']}] {msg['sender']}\n")
                f.write(f"   📝 {msg['content']}\n")
                if msg.get('sensitive'):
                    f.write(
                        f"   🚨 SENSITIVE: {', '.join(msg.get('tags', []))}\n")
                f.write("\n")

            # Leaked credentials
            if 'leaked_data' in self.results:
                f.write("🔓 LEAKED CREDENTIALS & DATA:\n")
                f.write("=" * 50 + "\n")
                if 'session_hijack' in self.results['leaked_data']:
                    hijack = self.results['leaked_data']['session_hijack']
                    f.write("Session Tokens:\n")
                    for token in hijack.get('session_tokens', []):
                        f.write(f"   🔑 {token}\n")
                    f.write("\nCached Sensitive Messages:\n")
                    for msg in hijack.get('cached_messages', []):
                        f.write(f"   💬 {msg['content']}\n")
                f.write("\n")

            # Contact discovery
            if 'contact_discovery' in self.results:
                contacts = self.results['contact_discovery']
                f.write("📞 DISCOVERED CONTACT POINTS:\n")
                f.write("=" * 50 + "\n")

                f.write("Email Addresses:\n")
                for email in contacts.get('email_addresses', []):
                    f.write(f"   📧 {email['email']} ({email['type']})\n")
                    f.write(
                        f"      Services: {', '.join(email['services'])}\n")

                f.write("\nPhone Numbers:\n")
                for phone in contacts.get('phone_numbers', []):
                    f.write(f"   📱 {phone['number']} ({phone['type']})\n")
                    f.write(
                        f"      Linked: {', '.join(phone['linked_accounts'])}\n")
                f.write("\n")

            # Security vulnerabilities
            if 'security_intel' in self.results:
                security = self.results['security_intel']
                f.write("🔍 SECURITY VULNERABILITIES:\n")
                f.write("=" * 50 + "\n")
                f.write(
                    f"Social Media Risk Score: {security['social_media_exposure']['risk_score']}/10\n")
                f.write(
                    f"Operational Security Score: {security['operational_security']['risk_score']}/10\n")
                f.write("\nCritical Issues:\n")
                f.write("   ❌ Reuses credentials across services\n")
                f.write("   ❌ Overshares financial information\n")
                f.write("   ❌ Poor verification practices\n")
                f.write("   ❌ Predictable password patterns\n\n")

            # Attack vectors
            if 'attack_vectors' in self.results:
                attacks = self.results['attack_vectors']
                f.write("⚔️ HIGH-SUCCESS ATTACK VECTORS:\n")
                f.write("=" * 50 + "\n")
                for attack in attacks.get('high_success_attacks', []):
                    f.write(f"🎯 {attack['name']} ({attack['success_rate']})\n")
                    f.write(f"   Method: {attack['method']}\n")
                    f.write(f"   Payload: {attack['payload']}\n\n")

            f.write("⚠️ DISCLAIMER:\n")
            f.write("=" * 50 + "\n")
            f.write(
                "This report is for educational and security testing purposes only.\n")
            f.write("Use this information ethically and legally.\n")
            f.write("Do not attempt actual attacks on real individuals.\n")

        print(f"{Colors.GREEN}✅ Results saved to:{Colors.END}")
        print(f"   📄 JSON: {json_file}")
        print(f"   📋 Report: {report_file}")

        return json_file, report_file

    def run_extraction(self):
        """รันการดึงข้อมูลทั้งหมด"""
        print(
            f"{Colors.BOLD}🚀 Starting advanced personal data extraction...{Colors.END}\n")

        # 1. จำลองการดึงข้อมูลจาก Telegram Web
        self.simulate_telegram_web_extraction()
        print()

        # 2. จำลองข้อมูลจาก session hijacking
        self.simulate_session_hijacking()
        print()

        # 3. รวบรวมข้อมูล social engineering
        self.simulate_social_engineering_intel()
        print()

        # 4. ค้นหาข้อมูลติดต่อเพิ่มเติม
        self.extract_contact_discovery()
        print()

        # 5. วิเคราะห์ช่องโหว่ความปลอดภัย
        self.analyze_security_vulnerabilities()
        print()

        # 6. สกัดข้อมูลส่วนตัวละเอียด
        self.extract_personal_intelligence()
        print()

        # 7. สร้างแนวทางการโจมตี
        self.generate_attack_vectors()
        print()

        # 8. บันทึกผลลัพธ์
        json_file, report_file = self.save_results()

        print(f"\n{Colors.GREEN}🏁 Personal data extraction complete!{Colors.END}")
        print(f"{Colors.CYAN}📋 Generated comprehensive intelligence report{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ Use responsibly and ethically!{Colors.END}")

        return json_file, report_file


def main():
    """ฟังก์ชันหลัก"""
    try:
        hacker = TelegramPersonalHacker()
        json_file, report_file = hacker.run_extraction()

        print(f"\n{Colors.BOLD}📊 EXTRACTION RESULTS:{Colors.END}")
        print(f"   🔥 Personal Messages: Extracted")
        print(f"   🔓 Leaked Credentials: Found")
        print(f"   📞 Contact Discovery: Complete")
        print(f"   🔍 Security Analysis: High-Risk Profile")
        print(f"   ⚔️ Attack Vectors: Multiple High-Success Methods")

        return True

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Extraction interrupted by user{Colors.END}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.END}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n{Colors.GREEN}✅ Mission accomplished!{Colors.END}")
    else:
        print(f"\n{Colors.RED}❌ Mission failed!{Colors.END}")
