# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
⚙️ CONFIGURATION INITIALIZER 2025 ⚙️
=====================================
Initialize and configure the Instagram Intelligence Platform
- Set up all configuration files
- Validate configurations
- Initialize system components
- Prepare for operations

Created by: SugarGlitch RealOps Team
Version: 2025.1.ULTIMATE
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from master_configuration_manager import master_config, get_config, set_config
except ImportError:
    print("❌ Failed to import master configuration manager")
    sys.exit(1)

class ConfigurationInitializer:
    """Initialize and configure the entire platform"""

    def __init__(self):
        self.config_manager = master_config
        self.initialization_log = []

    def log(self, message: str, level: str = "INFO"):
        """Log initialization messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.initialization_log.append(log_entry)
        print(log_entry)

    def initialize_platform(self) -> bool:
        """Initialize the entire Instagram Intelligence Platform"""
        self.log("🚀 Initializing Instagram Intelligence Platform", "START")

        success = True

        # Step 1: Validate configurations
        if not self.validate_configurations():
            success = False

        # Step 2: Initialize directories
        if not self.initialize_directories():
            success = False

        # Step 3: Setup database configuration
        if not self.setup_database_config():
            success = False

        # Step 4: Configure proxy system
        if not self.configure_proxy_system():
            success = False

        # Step 5: Setup session management
        if not self.setup_session_management():
            success = False

        # Step 6: Initialize monitoring
        if not self.initialize_monitoring():
            success = False

        # Step 7: Configure security settings
        if not self.configure_security():
            success = False

        # Step 8: Setup logging
        if not self.setup_logging():
            success = False

        # Step 9: Generate initialization report
        self.generate_initialization_report()

        status = "✅ SUCCESS" if success else "❌ FAILED"
        self.log(f"Platform initialization completed: {status}", "RESULT")

        return success

    def validate_configurations(self) -> bool:
        """Validate all configuration files"""
        self.log("🔍 Validating configurations...", "STEP")

        validation = self.config_manager.validate_all_configurations()

        if validation["overall_valid"]:
            self.log("✅ All configurations are valid", "SUCCESS")
            return True
        else:
            self.log("❌ Configuration validation failed", "ERROR")

            for config_name, result in validation.items():
                if config_name != "overall_valid" and not result["valid"]:
                    self.log(f"  ❌ {config_name}: {result['errors']}", "ERROR")

            return False

    def initialize_directories(self) -> bool:
        """Initialize required directories"""
        self.log("📁 Initializing directories...", "STEP")

        directories = [
            "databases",
            "logs",
            "intelligence",
            "encrypted_cache",
            "elite_results",
            "elite_logs",
            "sessions",
            "backups",
            "temp"
        ]

        try:
            for directory in directories:
                dir_path = Path(directory)
                dir_path.mkdir(exist_ok=True, mode=0o755)

                if directory in ["encrypted_cache", "elite_logs", "sessions"]:
                    # Secure permissions for sensitive directories
                    os.chmod(dir_path, 0o700)

                self.log(f"  📁 Created/verified: {directory}", "INFO")

            self.log("✅ Directory initialization completed", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"❌ Directory initialization failed: {e}", "ERROR")
            return False

    def setup_database_config(self) -> bool:
        """Setup database configuration"""
        self.log("🗄️ Setting up database configuration...", "STEP")

        try:
            db_enabled = get_config("master.database.enabled", True)
            db_path = get_config("master.database.path", "databases/")
            main_db = get_config("master.database.main_db", "instagram_intelligence_2025.db")

            # Ensure database directory exists
            Path(db_path).mkdir(exist_ok=True)

            # Set runtime database configuration
            set_config("system.database.runtime_path", str(Path(db_path) / main_db))
            set_config("system.database.initialized", True)
            set_config("system.database.initialization_time", datetime.now().isoformat())

            self.log(f"  🗄️ Database path: {db_path}", "INFO")
            self.log(f"  🗄️ Main database: {main_db}", "INFO")
            self.log(f"  🗄️ Database enabled: {db_enabled}", "INFO")

            self.log("✅ Database configuration completed", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"❌ Database configuration failed: {e}", "ERROR")
            return False

    def configure_proxy_system(self) -> bool:
        """Configure proxy system"""
        self.log("🌐 Configuring proxy system...", "STEP")

        try:
            proxy_enabled = get_config("proxy.enabled", False)
            proxy_host = get_config("proxy.primary_proxy.host", "")
            proxy_port = get_config("proxy.primary_proxy.port", "")

            if proxy_enabled and proxy_host and proxy_port:
                # Test proxy configuration
                self.log(f"  🌐 Proxy host: {proxy_host}:{proxy_port}", "INFO")
                self.log(f"  🌐 Proxy rotation: {get_config('proxy.rotation.enabled', False)}", "INFO")
                self.log(f"  🌐 Proxy validation: {get_config('proxy.validation.enabled', False)}", "INFO")

                # Set runtime proxy status
                set_config("system.proxy.configured", True)
                set_config("system.proxy.last_check", datetime.now().isoformat())

                self.log("✅ Proxy system configured", "SUCCESS")
            else:
                self.log("⚠️ Proxy system disabled or incomplete configuration", "WARNING")

            return True

        except Exception as e:
            self.log(f"❌ Proxy configuration failed: {e}", "ERROR")
            return False

    def setup_session_management(self) -> bool:
        """Setup session management system"""
        self.log("🔐 Setting up session management...", "STEP")

        try:
            session_enabled = get_config("session.session_management.enabled", False)
            session_dir = get_config("session.storage.directory", "config/sessions/")

            # Ensure session directory exists
            Path(session_dir).mkdir(parents=True, exist_ok=True)

            # Check for existing sessions
            active_sessions = get_config("session.active_sessions", {})
            session_count = len(active_sessions)

            self.log(f"  🔐 Session management: {session_enabled}", "INFO")
            self.log(f"  🔐 Session directory: {session_dir}", "INFO")
            self.log(f"  🔐 Active sessions: {session_count}", "INFO")

            # Set runtime session status
            set_config("system.sessions.configured", True)
            set_config("system.sessions.count", session_count)
            set_config("system.sessions.last_check", datetime.now().isoformat())

            self.log("✅ Session management configured", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"❌ Session management setup failed: {e}", "ERROR")
            return False

    def initialize_monitoring(self) -> bool:
        """Initialize monitoring system"""
        self.log("📊 Initializing monitoring system...", "STEP")

        try:
            monitoring_enabled = get_config("monitoring.monitoring.enabled", False)
            dashboard_enabled = get_config("monitoring.monitoring.dashboard_enabled", False)
            real_time = get_config("monitoring.monitoring.real_time", False)

            self.log(f"  📊 Monitoring: {monitoring_enabled}", "INFO")
            self.log(f"  📊 Dashboard: {dashboard_enabled}", "INFO")
            self.log(f"  📊 Real-time: {real_time}", "INFO")

            # Set runtime monitoring status
            set_config("system.monitoring.initialized", True)
            set_config("system.monitoring.start_time", datetime.now().isoformat())

            if monitoring_enabled:
                self.log("✅ Monitoring system initialized", "SUCCESS")
            else:
                self.log("⚠️ Monitoring system disabled", "WARNING")

            return True

        except Exception as e:
            self.log(f"❌ Monitoring initialization failed: {e}", "ERROR")
            return False

    def configure_security(self) -> bool:
        """Configure security settings"""
        self.log("🛡️ Configuring security settings...", "STEP")

        try:
            encryption_enabled = get_config("master.security.encryption.enabled", False)
            stealth_enabled = get_config("master.security.stealth.enabled", False)
            opsec_enabled = get_config("master.security.operational_security.log_sanitization", False)

            self.log(f"  🛡️ Encryption: {encryption_enabled}", "INFO")
            self.log(f"  🛡️ Stealth mode: {stealth_enabled}", "INFO")
            self.log(f"  🛡️ OpSec: {opsec_enabled}", "INFO")

            # Set runtime security status
            set_config("system.security.configured", True)
            set_config("system.security.encryption_ready", encryption_enabled)
            set_config("system.security.stealth_mode", stealth_enabled)

            self.log("✅ Security configuration completed", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"❌ Security configuration failed: {e}", "ERROR")
            return False

    def setup_logging(self) -> bool:
        """Setup logging system"""
        self.log("📝 Setting up logging system...", "STEP")

        try:
            log_enabled = get_config("system.logging.enabled", True)
            log_level = get_config("system.logging.level", "INFO")
            file_enabled = get_config("system.logging.handlers.file.enabled", True)

            # Ensure logs directory exists
            Path("logs").mkdir(exist_ok=True)

            self.log(f"  📝 Logging: {log_enabled}", "INFO")
            self.log(f"  📝 Log level: {log_level}", "INFO")
            self.log(f"  📝 File logging: {file_enabled}", "INFO")

            # Set runtime logging status
            set_config("system.logging.initialized", True)
            set_config("system.logging.start_time", datetime.now().isoformat())

            self.log("✅ Logging system configured", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"❌ Logging setup failed: {e}", "ERROR")
            return False

    def generate_initialization_report(self):
        """Generate initialization report"""
        report_path = f"config/initialization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report = {
            "initialization_timestamp": datetime.now().isoformat(),
            "platform_name": get_config("master.app.name", "Unknown"),
            "platform_version": get_config("master.app.version", "Unknown"),
            "initialization_log": self.initialization_log,
            "configuration_status": self.config_manager.get_configuration_status(),
            "validation_results": self.config_manager.validate_all_configurations(),
            "system_readiness": {
                "database_ready": get_config("system.database.initialized", False),
                "proxy_ready": get_config("system.proxy.configured", False),
                "sessions_ready": get_config("system.sessions.configured", False),
                "monitoring_ready": get_config("system.monitoring.initialized", False),
                "security_ready": get_config("system.security.configured", False),
                "logging_ready": get_config("system.logging.initialized", False)
            }
        }

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            self.log(f"📋 Initialization report saved: {report_path}", "INFO")

        except Exception as e:
            self.log(f"❌ Failed to save initialization report: {e}", "ERROR")

    def display_platform_status(self):
        """Display comprehensive platform status"""
        print("\n" + "="*60)
        print("🎯 INSTAGRAM INTELLIGENCE PLATFORM STATUS")
        print("="*60)

        app_name = get_config("master.app.name", "Unknown")
        app_version = get_config("master.app.version", "Unknown")

        print(f"📱 Platform: {app_name}")
        print(f"🔢 Version: {app_version}")
        print(f"⏰ Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n🔧 SYSTEM COMPONENTS:")
        print("-" * 30)

        components = [
            ("Database", get_config("system.database.initialized", False)),
            ("Proxy System", get_config("system.proxy.configured", False)),
            ("Session Management", get_config("system.sessions.configured", False)),
            ("Monitoring", get_config("system.monitoring.initialized", False)),
            ("Security", get_config("system.security.configured", False)),
            ("Logging", get_config("system.logging.initialized", False))
        ]

        for component, status in components:
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component}")

        print("\n📊 CONFIGURATION STATUS:")
        print("-" * 30)

        configs = [
            ("Master Config", "master"),
            ("Proxy Config", "proxy"),
            ("Session Config", "session"),
            ("Monitoring Config", "monitoring"),
            ("Bypass Config", "bypass"),
            ("System Config", "system")
        ]

        for name, config_key in configs:
            enabled = self.config_manager._get_enabled_status(config_key, self.config_manager.configs.get(config_key, {}))
            status_icon = "✅" if enabled else "⚠️"
            print(f"  {status_icon} {name}")

        print("\n🎯 READY FOR OPERATIONS!")
        print("="*60)

def main():
    """Main initialization function"""
    print("⚙️ CONFIGURATION INITIALIZER 2025 ⚙️")
    print("="*50)

    initializer = ConfigurationInitializer()

    # Initialize the platform
    success = initializer.initialize_platform()

    if success:
        print("\n✅ PLATFORM INITIALIZATION COMPLETED SUCCESSFULLY!")
        initializer.display_platform_status()

        # Export configurations for backup
        export_path = master_config.export_configurations()
        if export_path:
            print(f"\n💾 Configuration backup saved: {export_path}")

        return 0
    else:
        print("\n❌ PLATFORM INITIALIZATION FAILED!")
        print("Please check the logs and fix any configuration issues.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
