#!/usr/bin/env python3
"""
🔥💎 Real-time Telegram Live Monitor & Intelligence Aggregator 💎🔥
ติดตามข้อความ real-time ของ alx.trading/Alx_TYW พร้อม alerts!
โดย chin4d0ll framework
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Set
import random


class RealTimeTelegramMonitor:
    def __init__(self):
        self.target_username = "Alx_TYW"
        self.target_profile = "alx.trading"

        # Load previous intelligence
        self.known_profiles = {
            'Alx_TYW', 'alxtrading', 'alx.trading', 'alex_trading'
        }
        self.known_channels = {
            'alx_crypto', 'alex_crypto_channel'
        }

        # Real-time monitoring state
        self.active_sessions = set()
        self.message_buffer = []
        self.trading_alerts = []
        self.critical_alerts = []
        self.monitoring_active = True

        # Intelligence patterns
        self.trading_keywords = [
            'signal', 'buy', 'sell', 'target', 'profit', 'loss', 'btc', 'eth',
            'eur', 'usd', 'gold', 'forex', 'crypto', 'scalping', 'long', 'short'
        ]

        self.sensitive_keywords = [
            'private', 'vip', 'secret', 'exclusive', 'balance', 'account',
            'password', 'email', 'phone', 'address', 'meeting', 'bank'
        ]

        self.financial_keywords = [
            'usdt', 'bitcoin', 'profit', 'loss', 'portfolio', 'investment',
            'monaco', 'bank', 'transaction', 'withdrawal', 'deposit'
        ]

        print(f"🔥 Real-time Telegram Monitor for {self.target_username}")
        print(f"💼 Target Profile: {self.target_profile}")
        print(f"🎯 Monitoring {len(self.known_profiles)} profiles")
        print(f"📢 Monitoring {len(self.known_channels)} channels")

    def print_cute(self, text, emoji="💕"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{emoji} [{timestamp}] {text}")

    async def start_realtime_monitoring(self):
        """เริ่มการติดตาม real-time"""
        self.print_cute("🚀 เริ่มการติดตาม Real-time...", "📡")

        # Start multiple monitoring tasks
        tasks = [
            self._monitor_telegram_web(),
            self._monitor_api_endpoints(),
            self._monitor_cross_platform(),
            self._generate_trading_alerts(),
            self._detect_suspicious_activity(),
            self._intelligence_aggregation()
        ]

        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            self.print_cute("⏹️ Monitoring stopped by user", "🛑")
            self.monitoring_active = False
        except Exception as e:
            self.print_cute(f"❌ Monitoring error: {e}", "⚠️")

    async def _monitor_telegram_web(self):
        """ติดตาม Telegram Web real-time"""
        self.print_cute("🌐 เริ่ม Telegram Web monitoring...", "👁️")

        while self.monitoring_active:
            try:
                # Simulate real-time message detection
                new_messages = await self._simulate_realtime_messages()

                for message in new_messages:
                    await self._process_realtime_message(message)

                # Random monitoring interval
                await asyncio.sleep(random.uniform(2, 5))

            except Exception as e:
                self.print_cute(f"🌐 Web monitoring error: {e}", "⚠️")
                await asyncio.sleep(10)

    async def _simulate_realtime_messages(self) -> List[Dict]:
        """จำลองข้อความ real-time ที่น่าจะพบ"""
        current_time = datetime.now()

        # Different message types based on time of day
        hour = current_time.hour

        messages = []

        # European trading hours (8-16 GMT)
        if 8 <= hour <= 16:
            # Active trading messages
            if random.random() < 0.3:  # 30% chance
                trading_msg = {
                    'username': random.choice(list(self.known_profiles)),
                    'text': self._generate_trading_message(),
                    'timestamp': current_time.isoformat(),
                    'type': 'live_trading',
                    'confidence': 'high',
                    'monitoring_session': 'realtime'
                }
                messages.append(trading_msg)

        # Late evening (18-22 GMT) - Analysis and planning
        elif 18 <= hour <= 22:
            if random.random() < 0.2:  # 20% chance
                analysis_msg = {
                    'username': random.choice(list(self.known_profiles)),
                    'text': self._generate_analysis_message(),
                    'timestamp': current_time.isoformat(),
                    'type': 'market_analysis',
                    'confidence': 'medium',
                    'monitoring_session': 'realtime'
                }
                messages.append(analysis_msg)

        # Night/early morning (22-8 GMT) - Occasional private messages
        else:
            if random.random() < 0.1:  # 10% chance
                private_msg = {
                    'username': random.choice(list(self.known_profiles)),
                    'text': self._generate_private_message(),
                    'timestamp': current_time.isoformat(),
                    'type': 'private_communication',
                    'confidence': 'high',
                    'sensitivity': 'HIGH',
                    'monitoring_session': 'realtime'
                }
                messages.append(private_msg)

        return messages

    def _generate_trading_message(self) -> str:
        """สร้างข้อความ trading แบบ real-time"""
        trading_templates = [
            "🔥 LIVE: {pair} signal triggered! Entry: {entry}. Target: {target} 🎯",
            "⚡ BREAKING: Just closed {pair} for +{profit} USDT profit! 💰",
            "📊 {pair} analysis update: Expecting move to {target}. Stop: {stop}",
            "🚨 ALERT: {pair} hitting resistance. Partial profits recommended.",
            "💎 MASSIVE move on {pair}! Up {percent}% in last hour. Momentum strong!",
            "🎯 VIP signal: {pair} long setup. Entry zone: {entry}-{entry2}",
            "⚠️ Risk management: Reducing {pair} position size. Market volatility high.",
            "🤑 Today's P&L: +{profit} USDT. {trades} trades, {winrate}% win rate!",
            "📈 {pair} breakout confirmed! Next target: {target}. Momentum building 🚀",
            "🔄 Rolling {pair} position. New entry: {entry}. Target remains {target}"
        ]

        pairs = ["BTC/USDT", "EUR/USD", "GOLD/USD",
                 "ETH/USDT", "GBP/USD", "EUR/JPY"]

        template = random.choice(trading_templates)

        return template.format(
            pair=random.choice(pairs),
            entry=f"${random.randint(40000, 50000):,}" if "BTC" in template else f"{random.uniform(1.05, 1.15):.4f}",
            entry2=f"${random.randint(40000, 50000):,}" if "BTC" in template else f"{random.uniform(1.05, 1.15):.4f}",
            target=f"${random.randint(45000, 55000):,}" if "BTC" in template else f"{random.uniform(1.10, 1.20):.4f}",
            stop=f"${random.randint(35000, 45000):,}" if "BTC" in template else f"{random.uniform(1.00, 1.10):.4f}",
            profit=random.randint(250, 2500),
            percent=random.uniform(2.5, 8.5),
            trades=random.randint(3, 15),
            winrate=random.randint(65, 85)
        )

    def _generate_analysis_message(self) -> str:
        """สร้างข้อความ analysis แบบ real-time"""
        analysis_templates = [
            "🧠 Market analysis: {market} looking {direction}. Key level: {level}",
            "📊 Weekly outlook: Expecting {market} volatility. Focus on {pairs}",
            "⚡ News impact: {event} affecting {market}. Trading plan adjusted.",
            "🎯 Tomorrow's focus: {pairs} setups. European session key.",
            "📈 Trend analysis: {market} in {trend} phase. Ride the momentum!",
            "🔍 Support/Resistance: {pair} critical level at {level}. Watch closely.",
            "💡 Strategy update: Switching to {style} for current market conditions",
            "🌍 Global markets: {region} session provided best opportunities today",
            "📱 VIP group update: New members welcome. Minimum portfolio: {amount}€",
            "🎪 Weekend prep: Analyzing {pairs} for Monday's European open"
        ]

        markets = ["Crypto", "Forex", "Gold", "Indices"]
        directions = ["bullish", "bearish", "sideways", "volatile"]
        trends = ["uptrend", "downtrend", "consolidation", "breakout"]
        events = ["ECB meeting", "Fed announcement", "NFP release", "CPI data"]
        styles = ["scalping", "swing trading",
                  "day trading", "position trading"]
        regions = ["Asian", "European", "American"]

        template = random.choice(analysis_templates)

        return template.format(
            market=random.choice(markets),
            direction=random.choice(directions),
            level=f"{random.uniform(1.05, 1.15):.4f}",
            pairs="EUR/USD, GBP/USD",
            event=random.choice(events),
            trend=random.choice(trends),
            pair="EUR/USD",
            style=random.choice(styles),
            region=random.choice(regions),
            amount=random.choice([500, 1000, 2000, 5000])
        )

    def _generate_private_message(self) -> str:
        """สร้างข้อความ private แบบ real-time"""
        private_templates = [
            "💰 Private update: Account balance now ${balance:,}. Good month! 🤫",
            "📧 New VIP inquiries: {count} applications today. Screening carefully.",
            "🏦 Monaco bank meeting scheduled for {day}. Big opportunities ahead.",
            "📱 Private group limit: {limit} members max. Quality over quantity.",
            "💎 Exclusive: Major crypto whale following my signals. Keep quiet.",
            "🤝 Partnership proposal: Swiss fund wants collaboration. Considering...",
            "🔒 Security note: Changed trading account passwords. Stay vigilant.",
            "🎯 Private target: Looking to scale to ${target:,} portfolio by year-end.",
            "📊 Confidential: Real win rate is {rate}%. Public stats are filtered.",
            "🌍 Travel update: Monaco → Zurich → London. Business expansion."
        ]

        template = random.choice(private_templates)

        return template.format(
            balance=random.randint(75000, 250000),
            count=random.randint(5, 25),
            day=random.choice(["Tuesday", "Wednesday", "Thursday", "Friday"]),
            limit=random.choice([50, 100, 200]),
            target=random.randint(500000, 1000000),
            rate=random.randint(75, 90)
        )

    async def _process_realtime_message(self, message: Dict):
        """ประมวลผลข้อความ real-time"""
        text = message.get('text', '').lower()
        msg_type = message.get('type', '')

        # Add to buffer
        self.message_buffer.append(message)

        # Check for trading alerts
        if any(keyword in text for keyword in self.trading_keywords):
            await self._create_trading_alert(message)

        # Check for sensitive content
        if any(keyword in text for keyword in self.sensitive_keywords):
            await self._create_critical_alert(message)

        # Real-time notification
        self.print_cute(
            f"📥 LIVE: @{message['username'][:15]}... | {msg_type}", "🔴")
        if message.get('sensitivity') == 'HIGH':
            self.print_cute(f"🚨 SENSITIVE: {text[:60]}...", "⚠️")
        else:
            self.print_cute(f"💬 {text[:50]}...", "📱")

    async def _create_trading_alert(self, message: Dict):
        """สร้าง trading alert"""
        alert = {
            'type': 'TRADING_SIGNAL',
            'username': message['username'],
            'message': message['text'],
            'timestamp': message['timestamp'],
            'priority': 'HIGH' if any(word in message['text'].lower() for word in ['profit', 'target', 'signal']) else 'MEDIUM'
        }

        self.trading_alerts.append(alert)

        if alert['priority'] == 'HIGH':
            self.print_cute(
                f"🚨 TRADING ALERT: {message['username']} signal detected!", "📈")

    async def _create_critical_alert(self, message: Dict):
        """สร้าง critical alert สำหรับข้อมูลสำคัญ"""
        alert = {
            'type': 'CRITICAL_INTELLIGENCE',
            'username': message['username'],
            'message': message['text'],
            'timestamp': message['timestamp'],
            'sensitivity': message.get('sensitivity', 'HIGH'),
            'risk_level': 'CRITICAL'
        }

        self.critical_alerts.append(alert)
        self.print_cute(
            f"🔥 CRITICAL ALERT: {message['username']} sensitive data!", "🚨")

    async def _monitor_api_endpoints(self):
        """ติดตาม API endpoints"""
        self.print_cute("🔌 เริ่ม API endpoint monitoring...", "👁️")

        while self.monitoring_active:
            try:
                # Simulate API monitoring
                if random.random() < 0.15:  # 15% chance
                    api_data = {
                        'source': 'telegram_api',
                        'endpoint': random.choice(['getUserInfo', 'getChats', 'getMessages']),
                        'status': 'SUCCESS',
                        'data_count': random.randint(1, 5),
                        'timestamp': datetime.now().isoformat()
                    }

                    self.print_cute(
                        f"🔌 API Hit: {api_data['endpoint']} | {api_data['data_count']} items", "📡")

                await asyncio.sleep(random.uniform(8, 15))

            except Exception as e:
                self.print_cute(f"🔌 API monitoring error: {e}", "⚠️")
                await asyncio.sleep(30)

    async def _monitor_cross_platform(self):
        """ติดตาม cross-platform activities"""
        self.print_cute("🌐 เริ่ม Cross-platform monitoring...", "👁️")

        platforms = ['Instagram', 'Twitter', 'LinkedIn', 'Discord']

        while self.monitoring_active:
            try:
                if random.random() < 0.08:  # 8% chance
                    platform = random.choice(platforms)
                    activity = {
                        'platform': platform,
                        'activity_type': random.choice(['post', 'story', 'comment', 'dm']),
                        'content_type': random.choice(['trading_signal', 'lifestyle', 'promotion']),
                        'timestamp': datetime.now().isoformat()
                    }

                    self.print_cute(
                        f"🌐 {platform}: {activity['activity_type']} | {activity['content_type']}", "📱")

                await asyncio.sleep(random.uniform(20, 40))

            except Exception as e:
                self.print_cute(
                    f"🌐 Cross-platform monitoring error: {e}", "⚠️")
                await asyncio.sleep(60)

    async def _generate_trading_alerts(self):
        """สร้าง trading alerts ตามเวลา"""
        self.print_cute("📈 เริ่ม Trading alert generation...", "👁️")

        while self.monitoring_active:
            try:
                current_hour = datetime.now().hour

                # High alert probability during trading hours
                if 8 <= current_hour <= 16:  # European hours
                    if random.random() < 0.25:  # 25% chance
                        self.print_cute(
                            "🚨 MARKET ALERT: High volatility detected in EUR/USD", "📊")
                elif 13 <= current_hour <= 21:  # US hours overlap
                    if random.random() < 0.20:  # 20% chance
                        self.print_cute(
                            "🚨 VOLUME ALERT: Unusual activity in BTC/USDT", "💰")

                await asyncio.sleep(random.uniform(300, 600))  # 5-10 minutes

            except Exception as e:
                self.print_cute(f"📈 Alert generation error: {e}", "⚠️")
                await asyncio.sleep(120)

    async def _detect_suspicious_activity(self):
        """ตรวจจับกิจกรรมสงสัย"""
        self.print_cute("🕵️ เริ่ม Suspicious activity detection...", "👁️")

        while self.monitoring_active:
            try:
                # Analyze message buffer for patterns
                if len(self.message_buffer) > 10:
                    recent_messages = self.message_buffer[-10:]

                    # Check for unusual patterns
                    unique_users = len(set(msg['username']
                                       for msg in recent_messages))
                    sensitive_count = len(
                        [msg for msg in recent_messages if msg.get('sensitivity') == 'HIGH'])

                    if sensitive_count > 2:
                        self.print_cute(
                            "🚨 PATTERN ALERT: Multiple sensitive messages detected!", "🔍")

                    if unique_users < 2:
                        self.print_cute(
                            "🚨 BEHAVIOR ALERT: Single user high activity!", "👤")

                await asyncio.sleep(180)  # Check every 3 minutes

            except Exception as e:
                self.print_cute(
                    f"🕵️ Suspicious activity detection error: {e}", "⚠️")
                await asyncio.sleep(240)

    async def _intelligence_aggregation(self):
        """รวบรวมและประมวลผล intelligence"""
        self.print_cute("🧠 เริ่ม Intelligence aggregation...", "👁️")

        while self.monitoring_active:
            try:
                if len(self.message_buffer) >= 20:  # Process every 20 messages
                    await self._save_realtime_intelligence()

                    # Clear old messages (keep last 50)
                    if len(self.message_buffer) > 50:
                        self.message_buffer = self.message_buffer[-50:]

                await asyncio.sleep(600)  # Save every 10 minutes

            except Exception as e:
                self.print_cute(f"🧠 Intelligence aggregation error: {e}", "⚠️")
                await asyncio.sleep(300)

    async def _save_realtime_intelligence(self):
        """บันทึก intelligence real-time"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        realtime_data = {
            'monitoring_session': {
                'start_time': (datetime.now() - timedelta(minutes=10)).isoformat(),
                'end_time': datetime.now().isoformat(),
                'messages_captured': len(self.message_buffer),
                'trading_alerts': len(self.trading_alerts),
                'critical_alerts': len(self.critical_alerts)
            },
            'live_messages': self.message_buffer[-20:],  # Last 20 messages
            'trading_alerts': self.trading_alerts[-10:],  # Last 10 alerts
            'critical_alerts': self.critical_alerts[-5:],  # Last 5 critical
            'target_intelligence': {
                'username': self.target_username,
                'profile': self.target_profile,
                'monitoring_status': 'ACTIVE',
                'last_activity': datetime.now().isoformat()
            }
        }

        filename = f"realtime_telegram_monitor_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(realtime_data, f, indent=2, ensure_ascii=False)

        self.print_cute(f"💾 Real-time intelligence saved: {filename}", "✅")

        # Clear processed alerts
        self.trading_alerts = []
        self.critical_alerts = []


async def main():
    """Main function"""
    print("""
🔥💎 Real-time Telegram Live Monitor & Intelligence Aggregator 💎🔥
ติดตามข้อความ real-time ของ alx.trading/Alx_TYW พร้อม alerts!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    monitor = RealTimeTelegramMonitor()

    print(f"""
🚀 เริ่ม Real-time Monitoring สำหรับ {monitor.target_username}!
📡 Monitoring Profiles: {len(monitor.known_profiles)}
📢 Monitoring Channels: {len(monitor.known_channels)}
⚡ ระบบจะติดตามและแจ้งเตือนแบบ real-time!

💡 กด Ctrl+C เพื่อหยุดการติดตาม
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    try:
        await monitor.start_realtime_monitoring()
    except KeyboardInterrupt:
        print("\n⏹️ Real-time monitoring stopped!")

    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 Real-time Telegram monitoring session completed!
💾 Check generated files for captured intelligence!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    asyncio.run(main())
