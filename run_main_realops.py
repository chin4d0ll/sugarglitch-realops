#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Production Execution Engine
🎯 Real-time Instagram Intelligence & Breach Analysis
⚠️  AUTHORIZED REDTEAM USE ONLY - NO MOCK DATA

Production-grade runner for main.py with real CLI arguments,
authenticated Instagram sessions, and live target analysis.
"""

import os
import sys
import json
import logging
import argparse
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import traceback
import time

# Production constants
PROJECT_ROOT = Path(__file__).parent.absolute()
LOGS_DIR = PROJECT_ROOT / "logs"
EXPORTS_DIR = PROJECT_ROOT / "exports"
CONFIG_DIR = PROJECT_ROOT / "config"
CORE_DIR = PROJECT_ROOT / "core"


@dataclass
class ExecutionConfig:
    """🔧 Production execution configuration"""
    targets: List[str]
    ig_sessionid: str
    discord_webhook: str
    export_dir: Path
    logs_dir: Path
    timeout: int = 3600  # 1 hour timeout


class ProductionLogger:
    """📝 Production-grade logging system"""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup dual console/file logging"""
        logger = logging.getLogger("SugarGlitchRealOps")
        logger.setLevel(logging.INFO)

        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_format = logging.Formatter(
            '🔥 %(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(
            self.log_file, mode='a', encoding='utf-8')
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        return logger

    def info(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)


class EnvironmentValidator:
    """🛡️ Production environment validation"""

    REQUIRED_ENV_VARS = [
        'IG_SESSIONID',
        'DISCORD_WEBHOOK_URL',
        'TARGET_LIST',
        'EXPORT_DIR'
    ]

    OPTIONAL_ENV_VARS = [
        'IG_USERNAME',
        'IG_PASSWORD',
        'TARGET_HOST',
        'RATE_LIMIT_DELAY',
        'MAX_RETRIES',
        'USER_AGENT'
    ]

    @classmethod
    def validate_environment(cls, logger: ProductionLogger) -> Dict[str, str]:
        """Validate all required environment variables"""
        logger.info("🔍 Validating production environment...")

        env_vars = {}
        missing_vars = []

        # Load .env file if exists
        env_file = CONFIG_DIR / ".env"
        if env_file.exists():
            logger.info(f"📁 Loading environment from: {env_file}")
            cls._load_env_file(env_file)
        else:
            logger.warning(f"⚠️  .env file not found: {env_file}")

        # Check required variables
        for var in cls.REQUIRED_ENV_VARS:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                env_vars[var] = value
                logger.info(f"✅ {var}: {'*' * min(len(value), 10)}...")

        # Check optional variables
        for var in cls.OPTIONAL_ENV_VARS:
            value = os.getenv(var)
            if value:
                env_vars[var] = value
                logger.info(f"🔧 {var}: {'*' * min(len(value), 10)}...")

        if missing_vars:
            error_msg = f"❌ Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise EnvironmentError(error_msg)

        # Validate Instagram session
        cls._validate_instagram_session(env_vars['IG_SESSIONID'], logger)

        # Validate Discord webhook
        cls._validate_discord_webhook(env_vars['DISCORD_WEBHOOK_URL'], logger)

        logger.info("✅ Environment validation successful")
        return env_vars

    @staticmethod
    def _load_env_file(env_file: Path):
        """Load environment variables from .env file"""
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key.strip()] = value

    @staticmethod
    def _validate_instagram_session(sessionid: str, logger: ProductionLogger):
        """Validate Instagram session ID"""
        if len(sessionid) < 20:
            raise ValueError("❌ Invalid IG_SESSIONID format - too short")

        # Basic format validation (Instagram sessionids are typically 44 chars)
        if not sessionid.replace('%', '').replace('3A', '').replace('3D', '').isalnum():
            logger.warning("⚠️  IG_SESSIONID format may be invalid")

        logger.info("🔐 Instagram session ID format validated")

    @staticmethod
    def _validate_discord_webhook(webhook_url: str, logger: ProductionLogger):
        """Validate Discord webhook URL"""
        if not webhook_url.startswith('https://discord.com/api/webhooks/'):
            logger.warning("⚠️  Discord webhook URL format may be invalid for production")
        else:
            logger.info("📡 Discord webhook URL validated")


class RealOpsExecutor:
    """⚡ Main execution engine for SugarGlitch RealOps"""

    def __init__(self, config: ExecutionConfig, logger: ProductionLogger):
        self.config = config
        self.logger = logger
        self.start_time = datetime.now()
        self.results = {
            'start_time': self.start_time.isoformat(),
            'targets': config.targets,
            'status': 'running',
            'modules_executed': [],
            'exports_generated': [],
            'errors': []
        }

    def execute_production_run(self) -> Dict[str, Any]:
        """🚀 Execute full production run"""
        try:
            self.logger.info(
                "🔥 Starting SugarGlitch RealOps production execution")
            self.logger.info(f"🎯 Targets: {', '.join(self.config.targets)}")

            # Execute modules for each target
            for target in self.config.targets:
                self._execute_target_modules(target)

            # Generate final reports
            self._generate_final_reports()

            # Mark as successful
            self.results['status'] = 'success'
            self.results['end_time'] = datetime.now().isoformat()

            self.logger.info("✅ Production execution completed successfully")
            return self.results

        except Exception as e:
            self.results['status'] = 'failed'
            self.results['error'] = str(e)
            self.results['end_time'] = datetime.now().isoformat()

            error_msg = f"💥 Production execution failed: {e}"
            self.logger.error(error_msg)
            self.logger.error(traceback.format_exc())

            raise

    def _execute_target_modules(self, target: str):
        """Execute all modules for a specific target"""
        self.logger.info(f"🎯 Processing target: {target}")

        modules = [
            ('instagram-osint', f'Instagram OSINT analysis for {target}'),
            ('dm-extractor', f'DM extraction for {target}'),
            ('ig-session', f'Session analysis for {target}'),
            ('breach-analysis', f'Breach analysis for {target}'),
            ('scoring', f'Threat scoring for {target}')
        ]

        for module_name, description in modules:
            try:
                self.logger.info(f"▶️  Executing: {description}")
                result = self._execute_module(module_name, target)

                self.results['modules_executed'].append({
                    'module': module_name,
                    'target': target,
                    'status': 'success',
                    'timestamp': datetime.now().isoformat(),
                    'result': result
                })

            except Exception as e:
                error_msg = f"❌ Module {module_name} failed for {target}: {e}"
                self.logger.error(error_msg)

                self.results['modules_executed'].append({
                    'module': module_name,
                    'target': target,
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })

                self.results['errors'].append(error_msg)

    def _execute_module(self, module_name: str, target: str) -> Dict[str, Any]:
        """Execute a specific module with target"""
        cmd = [
            sys.executable,
            str(CORE_DIR / "main.py"),
            module_name
        ]

        self.logger.info(f"🔧 Command: {' '.join(cmd[:3])} [REDACTED_ARGS]")

        # Set environment variables with target and session info
        env = os.environ.copy()
        env.update({
            'IG_SESSIONID': self.config.ig_sessionid,
            'TARGET_HOST': 'www.instagram.com',
            'TARGET_USERNAME': target,
            'CURRENT_TARGET': target,
            'DISCORD_WEBHOOK_URL': self.config.discord_webhook,
            'PRODUCTION_MODE': 'true',
            'NO_MOCK_DATA': 'true',
            'EXPORT_DIR': str(self.config.export_dir)
        })

        # Execute with timeout
        start_time = time.time()
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                env=env,
                cwd=PROJECT_ROOT,
                input=target + '\n'  # Provide target as stdin input
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Module {module_name} timed out after {self.config.timeout}s")

        execution_time = time.time() - start_time

        if process.returncode != 0:
            error_msg = f"Module failed with code {process.returncode}: {process.stderr}"
            raise RuntimeError(error_msg)

        return {
            'stdout': process.stdout,
            'stderr': process.stderr,
            'return_code': process.returncode,
            'execution_time': execution_time
        }

    def _generate_final_reports(self):
        """Generate final consolidated reports"""
        self.logger.info("📊 Generating final consolidated reports...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON export
        json_file = self.config.export_dir / f"realops_report_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        self.results['exports_generated'].append(str(json_file))
        self.logger.info(f"💾 JSON report: {json_file}")

        # HTML export
        html_file = self.config.export_dir / f"realops_report_{timestamp}.html"
        self._generate_html_report(html_file)
        self.results['exports_generated'].append(str(html_file))
        self.logger.info(f"🌐 HTML report: {html_file}")

        # PDF export (if possible)
        try:
            pdf_file = self.config.export_dir / \
                f"realops_report_{timestamp}.pdf"
            self._generate_pdf_report(pdf_file, html_file)
            self.results['exports_generated'].append(str(pdf_file))
            self.logger.info(f"📄 PDF report: {pdf_file}")
        except Exception as e:
            self.logger.warning(f"⚠️  PDF generation failed: {e}")

    def _generate_html_report(self, html_file: Path):
        """Generate HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SugarGlitch RealOps - Production Report</title>
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
        .header {{ color: #ff6b6b; text-align: center; margin-bottom: 30px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #333; background: #111; }}
        .target {{ color: #ffd93d; font-weight: bold; }}
        .success {{ color: #00ff41; }}
        .error {{ color: #ff6b6b; }}
        .timestamp {{ color: #6c7b7f; font-size: 0.9em; }}
        pre {{ background: #222; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 SugarGlitch RealOps - Production Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>📊 Execution Summary</h2>
        <p><strong>Status:</strong> <span class="{self.results['status']}">{self.results['status'].upper()}</span></p>
        <p><strong>Start Time:</strong> {self.results['start_time']}</p>
        <p><strong>End Time:</strong> {self.results.get('end_time', 'In Progress')}</p>
        <p><strong>Targets:</strong> {', '.join(self.results['targets'])}</p>
        <p><strong>Modules Executed:</strong> {len(self.results['modules_executed'])}</p>
        <p><strong>Exports Generated:</strong> {len(self.results['exports_generated'])}</p>
        <p><strong>Errors:</strong> {len(self.results['errors'])}</p>
    </div>
    
    <div class="section">
        <h2>🎯 Module Execution Results</h2>
        <pre>{json.dumps(self.results['modules_executed'], indent=2)}</pre>
    </div>
    
    {"<div class='section'><h2>❌ Errors</h2><pre>" + json.dumps(self.results['errors'], indent=2) + "</pre></div>" if self.results['errors'] else ""}
    
    <div class="section">
        <h2>📁 Generated Exports</h2>
        <ul>
        {"".join(f"<li>{export}</li>" for export in self.results['exports_generated'])}
        </ul>
    </div>
</body>
</html>
        """

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _generate_pdf_report(self, pdf_file: Path, html_file: Path):
        """Generate PDF report from HTML (requires wkhtmltopdf)"""
        try:
            import subprocess
            subprocess.run([
                'wkhtmltopdf',
                '--enable-local-file-access',
                str(html_file),
                str(pdf_file)
            ], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback: use weasyprint if available
            try:
                import weasyprint
                weasyprint.HTML(filename=str(html_file)
                                ).write_pdf(str(pdf_file))
            except ImportError:
                raise RuntimeError(
                    "PDF generation requires wkhtmltopdf or weasyprint")


class DiscordNotifier:
    """📡 Discord webhook notifications"""

    def __init__(self, webhook_url: str, logger: ProductionLogger):
        self.webhook_url = webhook_url
        self.logger = logger

    def send_summary(self, results: Dict[str, Any]):
        """Send execution summary via Discord"""
        try:
            status_emoji = "✅" if results['status'] == 'success' else "❌"
            color = 0x00ff41 if results['status'] == 'success' else 0xff6b6b

            embed = {
                "title": f"{status_emoji} SugarGlitch RealOps - Execution Complete",
                "color": color,
                "timestamp": datetime.now().isoformat(),
                "fields": [
                    {
                        "name": "🎯 Targets",
                        "value": ", ".join(results['targets']),
                        "inline": True
                    },
                    {
                        "name": "📊 Status",
                        "value": results['status'].upper(),
                        "inline": True
                    },
                    {
                        "name": "🔧 Modules",
                        "value": str(len(results['modules_executed'])),
                        "inline": True
                    },
                    {
                        "name": "📁 Exports",
                        "value": str(len(results['exports_generated'])),
                        "inline": True
                    },
                    {
                        "name": "❌ Errors",
                        "value": str(len(results['errors'])),
                        "inline": True
                    },
                    {
                        "name": "⏱️ Duration",
                        "value": self._calculate_duration(results),
                        "inline": True
                    }
                ]
            }

            if results['errors']:
                embed["fields"].append({
                    "name": "🚨 Error Details",
                    "value": "\n".join(results['errors'][:5]) + ("..." if len(results['errors']) > 5 else ""),
                    "inline": False
                })

            payload = {
                "embeds": [embed],
                "username": "SugarGlitch RealOps",
                "avatar_url": "https://cdn.discordapp.com/emojis/🔥.png"
            }

            response = requests.post(
                self.webhook_url, json=payload, timeout=30)
            response.raise_for_status()

            self.logger.info("📡 Discord notification sent successfully")

        except Exception as e:
            self.logger.error(f"📡 Discord notification failed: {e}")

    def _calculate_duration(self, results: Dict[str, Any]) -> str:
        """Calculate execution duration"""
        try:
            start = datetime.fromisoformat(results['start_time'])
            end = datetime.fromisoformat(results.get(
                'end_time', datetime.now().isoformat()))
            duration = end - start

            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"

        except Exception:
            return "Unknown"


def setup_directories():
    """🗂️ Setup required directories"""
    LOGS_DIR.mkdir(exist_ok=True)
    EXPORTS_DIR.mkdir(exist_ok=True)
    (PROJECT_ROOT / "data").mkdir(exist_ok=True)
    (PROJECT_ROOT / "sessions").mkdir(exist_ok=True)


def parse_arguments() -> argparse.Namespace:
    """⚙️ Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="🔥 SugarGlitch RealOps - Production Execution Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 Examples:
  python run_main_realops.py --target @alx.trading --target @whatilove1728
  python run_main_realops.py --targets-file targets.txt --timeout 7200
  
🛡️ Environment Variables Required:
  IG_SESSIONID        - Instagram session ID (no login required)
  DISCORD_WEBHOOK_URL - Discord webhook for notifications
  TARGET_LIST         - Comma-separated target list (optional)
  EXPORT_DIR          - Export directory (default: ./exports)
        """
    )

    parser.add_argument(
        '--target',
        action='append',
        dest='targets',
        help='Target Instagram username (can be used multiple times)'
    )

    parser.add_argument(
        '--targets-file',
        help='File containing target usernames (one per line)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=3600,
        help='Execution timeout in seconds (default: 3600)'
    )

    parser.add_argument(
        '--export-dir',
        default=str(EXPORTS_DIR),
        help='Export directory (default: ./exports)'
    )

    parser.add_argument(
        '--logs-dir',
        default=str(LOGS_DIR),
        help='Logs directory (default: ./logs)'
    )

    parser.add_argument(
        '--no-discord',
        action='store_true',
        help='Disable Discord notifications'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser.parse_args()


def main():
    """🚀 Main execution function"""
    try:
        # Setup
        setup_directories()
        args = parse_arguments()

        # Setup logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Path(args.logs_dir) / f"run_{timestamp}.log"
        logger = ProductionLogger(log_file)

        logger.info("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
        logger.info("💀                SUGARGLITCH REALOPS                💀")
        logger.info("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
        logger.info("⚡ Production Execution Engine Starting")
        logger.info("🎯 Real-time Instagram Intelligence & Breach Analysis")
        logger.info("⚠️  AUTHORIZED REDTEAM USE ONLY")
        logger.info(f"📝 Logging to: {log_file}")

        # Validate environment
        env_vars = EnvironmentValidator.validate_environment(logger)

        # Parse targets
        targets = []
        if args.targets:
            targets.extend(args.targets)
        if args.targets_file:
            with open(args.targets_file, 'r') as f:
                targets.extend(line.strip() for line in f if line.strip())
        if not targets and 'TARGET_LIST' in env_vars:
            targets.extend(t.strip()
                           for t in env_vars['TARGET_LIST'].split(','))

        if not targets:
            raise ValueError(
                "❌ No targets specified. Use --target, --targets-file, or TARGET_LIST env var")

        # Clean target format
        targets = [t.lstrip('@') for t in targets]
        logger.info(
            f"🎯 Processing {len(targets)} targets: {', '.join(targets)}")

        # Create execution config
        config = ExecutionConfig(
            targets=targets,
            ig_sessionid=env_vars['IG_SESSIONID'],
            discord_webhook=env_vars['DISCORD_WEBHOOK_URL'],
            export_dir=Path(args.export_dir),
            logs_dir=Path(args.logs_dir),
            timeout=args.timeout
        )

        # Execute production run
        executor = RealOpsExecutor(config, logger)
        results = executor.execute_production_run()

        # Send Discord notification
        if not args.no_discord:
            notifier = DiscordNotifier(config.discord_webhook, logger)
            notifier.send_summary(results)

        logger.info("🎉 Production execution completed successfully")
        logger.info(
            f"📊 Results: {len(results['modules_executed'])} modules, {len(results['exports_generated'])} exports")

        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Execution interrupted by user")
        return 130

    except Exception as e:
        print(f"💥 FATAL ERROR: {e}")
        if 'logger' in locals():
            logger.error(f"💥 FATAL ERROR: {e}")
            logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
