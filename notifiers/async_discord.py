#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔔 ASYNC DISCORD WEBHOOK NOTIFIER
High-performance async notification system with rate limiting and retry logic
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from pathlib import Path
import logging
from enum import Enum

# Rich imports
try:
    from rich.console import Console
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


class NotificationLevel(Enum):
    """📊 Notification priority levels"""
    LOW = "🔵"
    MEDIUM = "🟡"
    HIGH = "🟠"
    CRITICAL = "🔴"
    SUCCESS = "🟢"


@dataclass
class DiscordEmbed:
    """🎨 Discord embed structure"""
    title: str
    description: str = ""
    color: int = 0x00ff00  # Green by default
    fields: List[Dict[str, Union[str, bool]]] = field(default_factory=list)
    footer: Optional[Dict[str, str]] = None
    thumbnail: Optional[Dict[str, str]] = None
    timestamp: Optional[str] = None

    def add_field(self, name: str, value: str, inline: bool = False) -> None:
        """Add field to embed"""
        self.fields.append({
            "name": name[:256],  # Discord limit
            "value": value[:1024],  # Discord limit
            "inline": inline
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert to Discord API format"""
        embed_dict = {
            "title": self.title[:256],
            "description": self.description[:4096],
            "color": self.color,
            "fields": self.fields,
            "timestamp": self.timestamp or datetime.utcnow().isoformat()
        }

        if self.footer:
            embed_dict["footer"] = self.footer
        if self.thumbnail:
            embed_dict["thumbnail"] = self.thumbnail

        return embed_dict


@dataclass
class NotificationTemplate:
    """📝 Reusable notification templates"""
    name: str
    title_template: str
    description_template: str
    color: int
    level: NotificationLevel

    def render(self, **kwargs) -> DiscordEmbed:
        """Render template with variables"""
        title = self.title_template.format(**kwargs)
        description = self.description_template.format(**kwargs)

        embed = DiscordEmbed(
            title=title,
            description=description,
            color=self.color
        )

        # Add timestamp and level
        embed.add_field("Level", self.level.value, inline=True)
        embed.add_field("Time", datetime.now().strftime(
            "%H:%M:%S"), inline=True)

        return embed


class AsyncDiscordNotifier:
    """🚀 High-performance async Discord webhook notifier"""

    def __init__(
        self,
        webhook_url: str,
        max_concurrent: int = 10,
        rate_limit_calls: int = 5,
        rate_limit_period: int = 5,
        retry_attempts: int = 3,
        timeout: int = 30
    ):
        self.webhook_url = webhook_url
        self.max_concurrent = max_concurrent
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        self.retry_attempts = retry_attempts
        self.timeout = timeout

        # Rate limiting
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limiter = self._create_rate_limiter()

        # Session management
        self.session: Optional[aiohttp.ClientSession] = None

        # Metrics
        self.sent_notifications = 0
        self.failed_notifications = 0
        self.rate_limited_count = 0

        # Templates
        self.templates: Dict[str, NotificationTemplate] = {}
        self._load_default_templates()

    def _create_rate_limiter(self):
        """Create token bucket rate limiter"""
        async def rate_limit():
            # Simple token bucket implementation
            if not hasattr(self, '_tokens'):
                self._tokens = self.rate_limit_calls
                self._last_refill = time.time()

            now = time.time()
            elapsed = now - self._last_refill

            # Refill tokens
            self._tokens = min(
                self.rate_limit_calls,
                self._tokens + elapsed *
                (self.rate_limit_calls / self.rate_limit_period)
            )
            self._last_refill = now

            if self._tokens >= 1:
                self._tokens -= 1
                return

            # Wait for next token
            wait_time = (1 - self._tokens) * \
                (self.rate_limit_period / self.rate_limit_calls)
            await asyncio.sleep(wait_time)
            self._tokens = 0

        return rate_limit

    def _load_default_templates(self):
        """Load default notification templates"""
        self.templates.update({
            "attack_start": NotificationTemplate(
                name="attack_start",
                title_template="🚀 Attack Started: {target}",
                description_template="Started {attack_type} attack on target: {target}\nThreads: {threads}\nEstimated time: {estimated_time}",
                color=0x0099ff,
                level=NotificationLevel.MEDIUM
            ),
            "attack_success": NotificationTemplate(
                name="attack_success",
                title_template="✅ Attack Successful: {target}",
                description_template="Successfully compromised target: {target}\nMethod: {method}\nCredentials: {credentials}\nTime taken: {time_taken}",
                color=0x00ff00,
                level=NotificationLevel.SUCCESS
            ),
            "attack_failed": NotificationTemplate(
                name="attack_failed",
                title_template="❌ Attack Failed: {target}",
                description_template="Attack failed on target: {target}\nReason: {reason}\nAttempts made: {attempts}",
                color=0xff0000,
                level=NotificationLevel.HIGH
            ),
            "data_extracted": NotificationTemplate(
                name="data_extracted",
                title_template="📊 Data Extracted: {target}",
                description_template="Successfully extracted data from: {target}\nData type: {data_type}\nRecords: {record_count}\nSize: {data_size}",
                color=0x00ff99,
                level=NotificationLevel.SUCCESS
            ),
            "rate_limited": NotificationTemplate(
                name="rate_limited",
                title_template="⏱️ Rate Limited: {target}",
                description_template="Rate limited while attacking: {target}\nStatus: {status_code}\nWait time: {wait_time}s",
                color=0xffaa00,
                level=NotificationLevel.MEDIUM
            ),
            "system_error": NotificationTemplate(
                name="system_error",
                title_template="🚨 System Error",
                description_template="Critical system error occurred:\n```{error}```\nComponent: {component}",
                color=0xff0000,
                level=NotificationLevel.CRITICAL
            )
        })

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self) -> None:
        """Initialize async session"""
        if self.session and not self.session.closed:
            return

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)

    async def close(self) -> None:
        """Close async session"""
        if self.session and not self.session.closed:
            await self.session.close()
            await asyncio.sleep(0.1)  # Allow cleanup

    async def send_notification(
        self,
        content: str = "",
        embed: Optional[DiscordEmbed] = None,
        username: str = "SugarGlitch RealOps",
        avatar_url: str = ""
    ) -> bool:
        """Send notification to Discord webhook"""
        if not self.session:
            await self.start()

        async with self.semaphore:
            await self.rate_limiter()

            payload = {
                "username": username,
                "content": content[:2000] if content else "",  # Discord limit
                "avatar_url": avatar_url
            }

            if embed:
                payload["embeds"] = [embed.to_dict()]

            for attempt in range(self.retry_attempts):
                try:
                    async with self.session.post(
                        self.webhook_url,
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    ) as response:

                        if response.status == 204:  # Success
                            self.sent_notifications += 1
                            return True
                        elif response.status == 429:  # Rate limited
                            self.rate_limited_count += 1
                            retry_after = int(
                                response.headers.get("Retry-After", 5))
                            await asyncio.sleep(retry_after)
                            continue
                        else:
                            logging.warning(
                                f"Discord webhook failed: {response.status}")

                except asyncio.TimeoutError:
                    logging.warning(
                        f"Discord webhook timeout (attempt {attempt + 1})")
                except Exception as e:
                    logging.error(f"Discord webhook error: {e}")

                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

            self.failed_notifications += 1
            return False

    async def send_template(self, template_name: str, **kwargs) -> bool:
        """Send notification using template"""
        if template_name not in self.templates:
            logging.error(f"Template '{template_name}' not found")
            return False

        template = self.templates[template_name]
        embed = template.render(**kwargs)

        return await self.send_notification(embed=embed)

    async def send_attack_start(self, target: str, attack_type: str, threads: int, estimated_time: str) -> bool:
        """Send attack start notification"""
        return await self.send_template(
            "attack_start",
            target=target,
            attack_type=attack_type,
            threads=threads,
            estimated_time=estimated_time
        )

    async def send_attack_success(self, target: str, method: str, credentials: str, time_taken: str) -> bool:
        """Send attack success notification"""
        return await self.send_template(
            "attack_success",
            target=target,
            method=method,
            credentials=credentials,
            time_taken=time_taken
        )

    async def send_attack_failed(self, target: str, reason: str, attempts: int) -> bool:
        """Send attack failed notification"""
        return await self.send_template(
            "attack_failed",
            target=target,
            reason=reason,
            attempts=attempts
        )

    async def send_data_extracted(self, target: str, data_type: str, record_count: int, data_size: str) -> bool:
        """Send data extraction notification"""
        return await self.send_template(
            "data_extracted",
            target=target,
            data_type=data_type,
            record_count=record_count,
            data_size=data_size
        )

    async def send_rate_limited(self, target: str, status_code: int, wait_time: int) -> bool:
        """Send rate limit notification"""
        return await self.send_template(
            "rate_limited",
            target=target,
            status_code=status_code,
            wait_time=wait_time
        )

    async def send_system_error(self, error: str, component: str) -> bool:
        """Send system error notification"""
        return await self.send_template(
            "system_error",
            error=str(error)[:1000],  # Truncate long errors
            component=component
        )

    async def send_batch(self, notifications: List[Dict[str, Any]]) -> List[bool]:
        """Send multiple notifications concurrently"""
        tasks = []

        for notification in notifications:
            if "template" in notification:
                task = self.send_template(**notification)
            else:
                task = self.send_notification(**notification)
            tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)

    def get_stats(self) -> Dict[str, Any]:
        """Get notification statistics"""
        total = self.sent_notifications + self.failed_notifications
        success_rate = (self.sent_notifications / max(total, 1)) * 100

        return {
            "sent_notifications": self.sent_notifications,
            "failed_notifications": self.failed_notifications,
            "success_rate": success_rate,
            "rate_limited_count": self.rate_limited_count,
            "total_notifications": total
        }

    async def test_webhook(self) -> bool:
        """Test webhook connection"""
        embed = DiscordEmbed(
            title="🧪 Webhook Test",
            description="Testing Discord webhook connection from SugarGlitch RealOps",
            color=0x0099ff
        )
        embed.add_field("Status", "✅ Connected", inline=True)
        embed.add_field("Time", datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), inline=True)

        result = await self.send_notification(embed=embed)

        if RICH_AVAILABLE and console:
            if result:
                console.print(
                    "[green]✅ Discord webhook test successful![/green]")
            else:
                console.print("[red]❌ Discord webhook test failed![/red]")
        else:
            print(f"Webhook test: {'✅ Success' if result else '❌ Failed'}")

        return result


# Convenience function for quick notifications
async def send_quick_notification(
    webhook_url: str,
    title: str,
    description: str,
    level: NotificationLevel = NotificationLevel.MEDIUM,
    **kwargs
) -> bool:
    """Send a quick notification without setting up full notifier"""

    color_map = {
        NotificationLevel.LOW: 0x0099ff,
        NotificationLevel.MEDIUM: 0xffaa00,
        NotificationLevel.HIGH: 0xff6600,
        NotificationLevel.CRITICAL: 0xff0000,
        NotificationLevel.SUCCESS: 0x00ff00
    }

    embed = DiscordEmbed(
        title=f"{level.value} {title}",
        description=description,
        color=color_map[level]
    )

    # Add extra fields
    for key, value in kwargs.items():
        embed.add_field(key.replace("_", " ").title(), str(value), inline=True)

    async with AsyncDiscordNotifier(webhook_url) as notifier:
        return await notifier.send_notification(embed=embed)


# Export main components
__all__ = [
    'AsyncDiscordNotifier',
    'DiscordEmbed',
    'NotificationLevel',
    'NotificationTemplate',
    'send_quick_notification'
]
