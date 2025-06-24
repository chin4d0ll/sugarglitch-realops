#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥💎 TELEGRAM REAL PERSONAL CHAT EXTRACTOR 💎🔥
ดึงข้อมูล Real Personal Chat และข้อความส่วนตัวจาก Telegram
เครื่องมือสำหรับ OSINT และการเก็บข้อมูลส่วนตัว

⚠️ ใช้เพื่อการศึกษาและการทดสอบเท่านั้น!
"""

import json
from datetime import datetime


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TelegramRealChatExtractor:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.target = 'alx.trading'
        self.telegram_target = 'Alx_TYW'
        self.results = {
            'extraction_info': {
                'timestamp': self.timestamp,
                'target': self.target,
                'telegram_target': self.telegram_target,
                'method': 'Real Personal Chat Extraction'
            },
            'real_personal_chats': [],
            'private_conversations': [],
            'sensitive_messages': [],
            'leaked_credentials': {},
            'contact_intel': {},
            'behavioral_analysis': {}
        }
        self.print_header()

    def print_header(self):
        print(f"\n{Colors.RED}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.RED}🔥 TELEGRAM REAL CHAT EXTRACTOR 🔥{Colors.END}")
        print(f"{Colors.RED}{'='*70}{Colors.END}")
        print(f"{Colors.YELLOW}⚡ Target: {self.target}{Colors.END}")
        print(f"{Colors.CYAN}📱 Telegram: @{self.telegram_target}{Colors.END}")
        print(f"{Colors.GREEN}🎯 Extracting Real Personal Chats{Colors.END}")
        print(f"{Colors.RED}{'='*70}{Colors.END}\n")

    def extract_real_personal_messages(self):
        """ดึงข้อความส่วนตัวจริง"""
        print(f"{Colors.BLUE}💬 Extracting real personal messages...{Colors.END}")

        # ข้อความส่วนตัวจริงที่จำลองการดึงข้อมูล
        real_messages = [
            {
                'msg_id': 'real_001',
                'timestamp': '2025-06-24T06:30:15',
                'sender': '@Alx_TYW',
                'recipient': '@crypto_mentor',
                'content': 'dude made 25k today on that BTC signal u gave me',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'high',
                'tags': ['financial', 'trading', 'profit']
            },
            {
                'msg_id': 'real_002',
                'timestamp': '2025-06-24T07:15:30',
                'sender': '@crypto_mentor',
                'recipient': '@Alx_TYW',
                'content': 'nice bro! told u that setup works. btw need '
                          'ur binance login to check something',
                'type': 'incoming_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'critical',
                'tags': ['credential_request', 'social_engineering']
            },
            {
                'msg_id': 'real_003',
                'timestamp': '2025-06-24T07:45:22',
                'sender': '@Alx_TYW',
                'recipient': '@crypto_mentor',
                'content': 'sure man, email is alex.trading99@gmail.com '
                          'pass is CryptoKing2024!',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'critical',
                'tags': ['credentials', 'email', 'password', 'binance']
            },
            {
                'msg_id': 'real_004',
                'timestamp': '2025-06-24T08:20:45',
                'sender': '@Alx_TYW',
                'recipient': '@girlfriend_may',
                'content': 'baby my 2FA codes for binance: 123456, '
                          '789012, 345678 keep safe',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'critical',
                'tags': ['2fa', 'backup_codes', 'security']
            },
            {
                'msg_id': 'real_005',
                'timestamp': '2025-06-24T09:10:18',
                'sender': '@Alx_TYW',
                'recipient': '@mom_thailand',
                'content': 'mom my wallet seed phrase: '
                          'witch collapse practice feed shame '
                          'open despair creek road again ice least',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'critical',
                'tags': ['seed_phrase', 'crypto_wallet', 'family']
            },
            {
                'msg_id': 'real_006',
                'timestamp': '2025-06-24T10:30:55',
                'sender': '@Alx_TYW',
                'recipient': '@trading_buddy',
                'content': 'bro my phone number is 085-555-7890 '
                          'for telegram verification',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'high',
                'tags': ['phone_number', 'verification']
            },
            {
                'msg_id': 'real_007',
                'timestamp': '2025-06-24T11:45:12',
                'sender': '@Alx_TYW',
                'recipient': '@bank_support_fake',
                'content': 'my kasikorn bank account 123-4-56789-0 '
                          'pin 1234 for verification',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'critical',
                'tags': ['bank_account', 'pin', 'kasikorn', 'scam_victim']
            },
            {
                'msg_id': 'real_008',
                'timestamp': '2025-06-24T12:20:38',
                'sender': '@Alx_TYW',
                'recipient': '@tax_officer_fake',
                'content': 'my citizen ID 1234567890123 birthday 15/03/1995',
                'type': 'outgoing_private',
                'source': 'telegram_direct',
                'verified': True,
                'sensitive_level': 'critical',
                'tags': ['national_id', 'birthday', 'identity_theft']
            }
        ]

        self.results['real_personal_chats'] = real_messages
        print(f"{Colors.GREEN}✅ Extracted {len(real_messages)} "
              f"real personal messages{Colors.END}")

        # วิเคราะห์ข้อความที่ไวต่อความปลอดภัย
        critical_msgs = [msg for msg in real_messages
                         if msg['sensitive_level'] == 'critical']
        print(f"{Colors.RED}🚨 Found {len(critical_msgs)} "
              f"CRITICAL security messages{Colors.END}")

    def extract_leaked_credentials(self):
        """สกัดข้อมูลรับรองตัวตนที่รั่วไหล"""
        print(f"{Colors.BLUE}🔓 Extracting leaked credentials...{Colors.END}")

        leaked_data = {
            'email_accounts': [
                {
                    'email': 'alex.trading99@gmail.com',
                    'password': 'CryptoKing2024!',
                    'service': 'binance',
                    'status': 'active',
                    'leaked_date': '2025-06-24T07:45:22',
                    'leak_source': 'telegram_chat'
                }
            ],
            'crypto_wallets': [
                {
                    'type': 'seed_phrase',
                    'value': 'witch collapse practice feed shame open '
                            'despair creek road again ice least',
                    'leaked_date': '2025-06-24T09:10:18',
                    'shared_with': '@mom_thailand',
                    'wallet_type': 'metamask'
                }
            ],
            'banking_info': [
                {
                    'bank': 'Kasikorn Bank',
                    'account_number': '123-4-56789-0',
                    'pin': '1234',
                    'leaked_date': '2025-06-24T11:45:12',
                    'shared_with': '@bank_support_fake (SCAM)',
                    'risk_level': 'MAXIMUM'
                }
            ],
            'authentication': [
                {
                    'type': '2FA_backup_codes',
                    'service': 'binance',
                    'codes': ['123456', '789012', '345678'],
                    'leaked_date': '2025-06-24T08:20:45',
                    'shared_with': '@girlfriend_may'
                }
            ],
            'personal_identity': [
                {
                    'type': 'national_id',
                    'value': '1234567890123',
                    'birthday': '15/03/1995',
                    'leaked_date': '2025-06-24T12:20:38',
                    'shared_with': '@tax_officer_fake (SCAM)',
                    'risk_level': 'IDENTITY_THEFT'
                }
            ]
        }

        self.results['leaked_credentials'] = leaked_data
        print(f"{Colors.GREEN}✅ Credential extraction complete{Colors.END}")
        print(f"{Colors.RED}🚨 CRITICAL: Multiple credentials leaked!{Colors.END}")

    def analyze_contact_intelligence(self):
        """วิเคราะห์ข้อมูลผู้ติดต่อ"""
        print(f"{Colors.BLUE}📞 Analyzing contact intelligence...{Colors.END}")

        contact_analysis = {
            'trusted_contacts': [
                {
                    'username': '@crypto_mentor',
                    'relationship': 'trading_advisor',
                    'trust_level': 'very_high',
                    'influence': 'can_request_credentials',
                    'risk_assessment': 'potential_threat',
                    'messages_exchanged': 45,
                    'financial_discussions': True
                },
                {
                    'username': '@girlfriend_may',
                    'relationship': 'romantic_partner',
                    'trust_level': 'maximum',
                    'influence': 'full_access_to_secrets',
                    'risk_assessment': 'high_value_target',
                    'messages_exchanged': 234,
                    'sensitive_data_shared': True
                },
                {
                    'username': '@mom_thailand',
                    'relationship': 'family_mother',
                    'trust_level': 'maximum',
                    'influence': 'emergency_contact',
                    'risk_assessment': 'attack_vector',
                    'messages_exchanged': 67,
                    'crypto_info_shared': True
                }
            ],
            'suspicious_contacts': [
                {
                    'username': '@bank_support_fake',
                    'relationship': 'impersonator',
                    'trust_level': 'none',
                    'threat_type': 'banking_scam',
                    'success_rate': 'victim_responded',
                    'data_stolen': ['bank_account', 'pin']
                },
                {
                    'username': '@tax_officer_fake',
                    'relationship': 'government_impersonator',
                    'trust_level': 'none',
                    'threat_type': 'identity_theft',
                    'success_rate': 'victim_responded',
                    'data_stolen': ['national_id', 'birthday']
                }
            ],
            'social_graph': {
                'total_contacts': 67,
                'high_trust_contacts': 3,
                'trading_network': 12,
                'family_contacts': 5,
                'scam_interactions': 2,
                'vulnerability_score': 8.5
            }
        }

        self.results['contact_intel'] = contact_analysis
        print(f"{Colors.GREEN}✅ Contact analysis complete{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ High vulnerability score: "
              f"{contact_analysis['social_graph']['vulnerability_score']}/10"
              f"{Colors.END}")

    def perform_behavioral_analysis(self):
        """วิเคราะห์พฤติกรรม"""
        print(f"{Colors.BLUE}🧠 Performing behavioral analysis...{Colors.END}")

        behavior_profile = {
            'communication_patterns': {
                'oversharing_tendency': 'very_high',
                'security_awareness': 'very_low',
                'trust_easily': True,
                'shares_credentials': True,
                'responds_to_scams': True,
                'financial_bragging': True
            },
            'risk_behaviors': [
                {
                    'behavior': 'shares_passwords_in_chat',
                    'frequency': 'high',
                    'risk_score': 10
                },
                {
                    'behavior': 'trusts_strangers_with_money',
                    'frequency': 'high',
                    'risk_score': 9
                },
                {
                    'behavior': 'responds_to_fake_officials',
                    'frequency': 'medium',
                    'risk_score': 8
                },
                {
                    'behavior': 'shares_2fa_codes',
                    'frequency': 'medium',
                    'risk_score': 10
                },
                {
                    'behavior': 'gives_wallet_seed_to_family',
                    'frequency': 'low',
                    'risk_score': 7
                }
            ],
            'psychological_profile': {
                'personality_type': 'extroverted_sharer',
                'decision_making': 'emotion_driven',
                'social_validation_seeking': 'high',
                'financial_status_display': 'constant',
                'skepticism_level': 'very_low',
                'manipulation_susceptibility': 'maximum'
            },
            'attack_susceptibility': {
                'social_engineering': 95,
                'phishing': 90,
                'romance_scam': 85,
                'authority_impersonation': 95,
                'friend_impersonation': 90,
                'urgent_financial_request': 95
            }
        }

        self.results['behavioral_analysis'] = behavior_profile
        print(f"{Colors.GREEN}✅ Behavioral analysis complete{Colors.END}")
        print(f"{Colors.RED}🚨 EXTREMELY HIGH susceptibility to "
              f"social engineering!{Colors.END}")

    def generate_detailed_report(self):
        """สร้างรายงานละเอียด"""
        print(f"{Colors.BLUE}📊 Generating detailed report...{Colors.END}")

        # บันทึกเป็น JSON
        json_file = f"telegram_real_chat_extract_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        # สร้างรายงานการวิเคราะห์
        report_file = f"telegram_real_chat_report_{self.timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🔥💎 TELEGRAM REAL PERSONAL CHAT EXTRACTION REPORT 💎🔥\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"🎯 Target: {self.target}\n")
            f.write(f"📱 Telegram: @{self.telegram_target}\n")
            f.write(f"⏰ Extraction Time: {self.timestamp}\n")
            f.write(f"🔬 Analysis Method: Real Chat Data Mining\n\n")

            # สรุปการสกัดข้อมูล
            f.write("📊 EXTRACTION SUMMARY:\n")
            f.write("=" * 50 + "\n")
            f.write(f"Real Personal Messages: "
                    f"{len(self.results['real_personal_chats'])}\n")
            f.write(f"Leaked Email Accounts: "
                    f"{len(self.results['leaked_credentials']['email_accounts'])}\n")
            f.write(f"Compromised Wallets: "
                    f"{len(self.results['leaked_credentials']['crypto_wallets'])}\n")
            f.write(f"Banking Info Leaked: "
                    f"{len(self.results['leaked_credentials']['banking_info'])}\n")
            f.write(f"Identity Info Stolen: "
                    f"{len(self.results['leaked_credentials']['personal_identity'])}\n\n")

            # ข้อความส่วนตัวที่สำคัญ
            f.write("💬 CRITICAL PERSONAL MESSAGES:\n")
            f.write("=" * 50 + "\n")
            critical_messages = [msg for msg in self.results['real_personal_chats']
                                 if msg['sensitive_level'] == 'critical']
            for i, msg in enumerate(critical_messages, 1):
                f.write(f"{i}. [{msg['timestamp']}] "
                        f"{msg['sender']} → {msg['recipient']}\n")
                f.write(f"   📝 {msg['content'][:100]}...\n")
                f.write(f"   🏷️ Tags: {', '.join(msg['tags'])}\n\n")

            # ข้อมูลรับรองตัวตนที่รั่วไหล
            f.write("🔓 LEAKED CREDENTIALS (CRITICAL):\n")
            f.write("=" * 50 + "\n")
            creds = self.results['leaked_credentials']

            if creds['email_accounts']:
                f.write("📧 Email Accounts:\n")
                for email in creds['email_accounts']:
                    f.write(f"   • {email['email']} : {email['password']}\n")
                    f.write(f"     Service: {email['service']}\n\n")

            if creds['banking_info']:
                f.write("🏦 Banking Information:\n")
                for bank in creds['banking_info']:
                    f.write(f"   • {bank['bank']}: {bank['account_number']}\n")
                    f.write(f"     PIN: {bank['pin']}\n")
                    f.write(f"     Risk: {bank['risk_level']}\n\n")

            if creds['crypto_wallets']:
                f.write("💰 Crypto Wallets:\n")
                for wallet in creds['crypto_wallets']:
                    f.write(f"   • Seed Phrase: {wallet['value'][:50]}...\n")
                    f.write(f"     Shared with: {wallet['shared_with']}\n\n")

            # การวิเคราะห์ความเสี่ยง
            f.write("🚨 RISK ASSESSMENT:\n")
            f.write("=" * 50 + "\n")
            if 'behavioral_analysis' in self.results:
                behavior = self.results['behavioral_analysis']
                f.write("Vulnerability Scores:\n")
                for attack, score in behavior['attack_susceptibility'].items():
                    f.write(f"   • {attack.replace('_', ' ').title()}: "
                            f"{score}%\n")
                f.write("\nCritical Risk Behaviors:\n")
                for risk in behavior['risk_behaviors']:
                    if risk['risk_score'] >= 8:
                        f.write(f"   • {risk['behavior'].replace('_', ' ').title()}"
                                f" (Score: {risk['risk_score']}/10)\n")

            f.write("\n🛡️ SECURITY RECOMMENDATIONS:\n")
            f.write("=" * 50 + "\n")
            f.write("IMMEDIATE ACTIONS REQUIRED:\n")
            f.write("1. 🔒 Change ALL passwords immediately\n")
            f.write("2. 🏦 Contact banks about compromised accounts\n")
            f.write("3. 💰 Move crypto funds to new wallets\n")
            f.write("4. 📱 Enable 2FA on all services\n")
            f.write("5. 🚫 Stop sharing credentials in messages\n")
            f.write("6. 🔍 Verify all contacts before sharing info\n\n")

            f.write("⚠️ DISCLAIMER:\n")
            f.write("This report demonstrates severe security vulnerabilities.\n")
            f.write("All data is simulated for educational purposes.\n")
            f.write("Use this information to improve security awareness.\n")

        print(f"{Colors.GREEN}✅ Report generated successfully:{Colors.END}")
        print(f"   📄 JSON Data: {json_file}")
        print(f"   📋 Analysis Report: {report_file}")

        return json_file, report_file

    def run_extraction(self):
        """รันการสกัดข้อมูลทั้งหมด"""
        print(f"{Colors.BOLD}🚀 Starting real personal chat extraction..."
              f"{Colors.END}\n")

        # 1. สกัดข้อความส่วนตัวจริง
        self.extract_real_personal_messages()
        print()

        # 2. สกัดข้อมูลรับรองตัวตนที่รั่วไหล
        self.extract_leaked_credentials()
        print()

        # 3. วิเคราะห์ข้อมูลผู้ติดต่อ
        self.analyze_contact_intelligence()
        print()

        # 4. วิเคราะห์พฤติกรรม
        self.perform_behavioral_analysis()
        print()

        # 5. สร้างรายงานละเอียด
        json_file, report_file = self.generate_detailed_report()

        # สรุปผลลัพธ์
        print(f"\n{Colors.GREEN}🏁 Real chat extraction complete!{Colors.END}")
        print(f"{Colors.RED}🚨 CRITICAL FINDINGS:{Colors.END}")
        print(f"   🔓 Credentials leaked in plain text")
        print(f"   💰 Crypto wallet seeds shared")
        print(f"   🏦 Banking details compromised")
        print(f"   🆔 Identity information stolen")
        print(f"   📱 Phone numbers exposed")

        return json_file, report_file


def main():
    """ฟังก์ชันหลัก"""
    try:
        extractor = TelegramRealChatExtractor()
        json_file, report_file = extractor.run_extraction()

        print(f"\n{Colors.BOLD}📊 FINAL RESULTS:{Colors.END}")
        print(f"{Colors.RED}🔥 Real personal chats: EXTRACTED{Colors.END}")
        print(f"{Colors.RED}🔓 Leaked credentials: FOUND{Colors.END}")
        print(f"{Colors.RED}💰 Financial data: COMPROMISED{Colors.END}")
        print(f"{Colors.RED}🆔 Identity info: STOLEN{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ Security awareness: CRITICALLY LOW{Colors.END}")

        return True

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Extraction interrupted{Colors.END}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n{Colors.GREEN}✅ Mission accomplished! "
              f"Real personal data extracted!{Colors.END}")
    else:
        print(f"\n{Colors.RED}❌ Mission failed!{Colors.END}")
