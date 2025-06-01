#!/usr/bin/env python3
"""
Master Codebase Improvement Script
Non-destructive enhancement of existing code while preserving all sensitive data
"""

import os
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
import subprocess
import sys

# Import our utility modules
sys.path.append('/workspaces/sugarglitch-realops')
from utils.error_handler import safe_execution, safe_print
from utils.config_manager import ConfigManager
from utils.session_validator import SessionBatchValidator

class CodebaseImprover:
    def __init__(self):
        self.root_dir = Path("/workspaces/sugarglitch-realops")
        self.backup_dir = self.root_dir / "backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.improved_dir = self.root_dir / "improved_code"
        self.config_manager = ConfigManager()
        self.session_validator = SessionBatchValidator()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.root_dir / 'improvement_log.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    @safe_execution
    def create_backup(self):
        """Create backup of current state before improvements"""
        safe_print(f"🔄 Creating backup in {self.backup_dir}")
        
        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup all Python files
        python_files = list(self.root_dir.glob("*.py"))
        for py_file in python_files:
            shutil.copy2(py_file, self.backup_dir / py_file.name)
            
        # Backup JSON configs
        json_files = list(self.root_dir.glob("*.json"))
        for json_file in json_files:
            shutil.copy2(json_file, self.backup_dir / json_file.name)
            
        safe_print(f"✅ Backup created with {len(python_files)} Python files and {len(json_files)} JSON files")
        return True

    @safe_execution
    def enhance_python_files(self):
        """Enhance existing Python files with error handling and logging"""
        safe_print("🔧 Enhancing Python files with improved error handling...")
        
        # Create improved code directory
        self.improved_dir.mkdir(exist_ok=True)
        
        python_files = list(self.root_dir.glob("*.py"))
        enhanced_count = 0
        
        for py_file in python_files:
            if py_file.name in ['improve_codebase.py', '__init__.py']:
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add imports if not present
                enhanced_content = self._add_error_handling_imports(content)
                enhanced_content = self._wrap_main_function(enhanced_content)
                enhanced_content = self._add_logging_setup(enhanced_content)
                
                # Save enhanced version
                enhanced_file = self.improved_dir / py_file.name
                with open(enhanced_file, 'w', encoding='utf-8') as f:
                    f.write(enhanced_content)
                    
                enhanced_count += 1
                safe_print(f"✅ Enhanced {py_file.name}")
                
            except Exception as e:
                safe_print(f"⚠️ Could not enhance {py_file.name}: {e}")
                
        safe_print(f"🎉 Enhanced {enhanced_count} Python files")
        return enhanced_count

    def _add_error_handling_imports(self, content):
        """Add error handling imports to the file"""
        if "from utils.error_handler import" not in content:
            import_line = "from utils.error_handler import safe_execution, safe_print\n"
            if "import" in content:
                # Add after existing imports
                lines = content.split('\n')
                import_inserted = False
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        continue
                    else:
                        lines.insert(i, import_line)
                        import_inserted = True
                        break
                if import_inserted:
                    content = '\n'.join(lines)
                else:
                    content = import_line + content
            else:
                content = import_line + content
        return content

    def _wrap_main_function(self, content):
        """Wrap main function with error handling"""
        if "def main(" in content and "@safe_execution" not in content:
            content = content.replace("def main(", "@safe_execution\ndef main(")
        return content

    def _add_logging_setup(self, content):
        """Add logging setup to the file"""
        if "logging.basicConfig" not in content:
            logging_setup = '''
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
'''
            if "import" in content:
                content = content.replace("import logging", logging_setup.strip())
            else:
                content = logging_setup + content
        return content

    @safe_execution
    def validate_all_sessions(self):
        """Validate all session files in the workspace"""
        safe_print("🔍 Validating all session files...")
        
        json_files = list(self.root_dir.glob("*.json"))
        session_files = [f for f in json_files if any(keyword in f.name.lower() 
                        for keyword in ['session', 'extraction', 'intelligence', 'report'])]
        
        validation_results = self.session_validator.validate_batch(
            [str(f) for f in session_files]
        )
        
        # Save validation report
        report_file = self.root_dir / f"session_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(validation_results, f, indent=2)
            
        safe_print(f"✅ Session validation complete. Report saved to {report_file.name}")
        return validation_results

    @safe_execution
    def consolidate_configurations(self):
        """Consolidate all configuration files"""
        safe_print("📋 Consolidating configuration files...")
        
        json_files = list(self.root_dir.glob("*.json"))
        config_files = [f for f in json_files if any(keyword in f.name.lower() 
                       for keyword in ['config', 'setup', 'proxy'])]
        
        consolidated_configs = {}
        for config_file in config_files:
            try:
                config_data = self.config_manager.load_config(str(config_file))
                consolidated_configs[config_file.name] = config_data
                safe_print(f"✅ Loaded config: {config_file.name}")
            except Exception as e:
                safe_print(f"⚠️ Could not load {config_file.name}: {e}")
        
        # Save consolidated config
        consolidated_file = self.root_dir / f"consolidated_configs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(consolidated_file, 'w') as f:
            json.dump(consolidated_configs, f, indent=2)
            
        safe_print(f"✅ Configuration consolidation complete. Saved to {consolidated_file.name}")
        return consolidated_configs

    @safe_execution
    def create_requirements_analysis(self):
        """Analyze and optimize requirements.txt"""
        safe_print("📦 Analyzing requirements.txt...")
        
        req_file = self.root_dir / "requirements.txt"
        if not req_file.exists():
            safe_print("⚠️ requirements.txt not found")
            return False
            
        with open(req_file, 'r') as f:
            requirements = f.read().splitlines()
        
        # Remove duplicates and sort
        unique_requirements = sorted(list(set(req.strip() for req in requirements if req.strip())))
        
        # Save optimized requirements
        optimized_req_file = self.root_dir / "requirements_optimized.txt"
        with open(optimized_req_file, 'w') as f:
            f.write('\n'.join(unique_requirements))
            
        safe_print(f"✅ Optimized requirements: {len(requirements)} → {len(unique_requirements)} packages")
        return True

    @safe_execution
    def create_project_structure_report(self):
        """Create comprehensive project structure report"""
        safe_print("📊 Creating project structure report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "python_files": 0,
            "json_files": 0,
            "database_files": 0,
            "log_files": 0,
            "image_files": 0,
            "directories": [],
            "file_categories": {}
        }
        
        for item in self.root_dir.iterdir():
            if item.is_file():
                report["total_files"] += 1
                ext = item.suffix.lower()
                
                if ext == '.py':
                    report["python_files"] += 1
                elif ext == '.json':
                    report["json_files"] += 1
                elif ext in ['.db', '.sqlite']:
                    report["database_files"] += 1
                elif ext in ['.log', '.txt']:
                    report["log_files"] += 1
                elif ext in ['.png', '.jpg', '.jpeg']:
                    report["image_files"] += 1
                    
                category = report["file_categories"].get(ext, 0)
                report["file_categories"][ext] = category + 1
                
            elif item.is_dir() and not item.name.startswith('.'):
                report["directories"].append(item.name)
        
        # Save structure report
        structure_report_file = self.root_dir / f"project_structure_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(structure_report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        safe_print(f"✅ Project structure report saved to {structure_report_file.name}")
        return report

    @safe_execution
    def run_improvement_pipeline(self):
        """Run the complete improvement pipeline"""
        safe_print("🚀 Starting codebase improvement pipeline...")
        safe_print("="*60)
        
        results = {}
        
        # Step 1: Create backup
        safe_print("Step 1: Creating backup...")
        results['backup'] = self.create_backup()
        
        # Step 2: Enhance Python files
        safe_print("\nStep 2: Enhancing Python files...")
        results['enhanced_files'] = self.enhance_python_files()
        
        # Step 3: Validate sessions
        safe_print("\nStep 3: Validating session files...")
        results['session_validation'] = self.validate_all_sessions()
        
        # Step 4: Consolidate configs
        safe_print("\nStep 4: Consolidating configurations...")
        results['config_consolidation'] = self.consolidate_configurations()
        
        # Step 5: Optimize requirements
        safe_print("\nStep 5: Optimizing requirements...")
        results['requirements_optimization'] = self.create_requirements_analysis()
        
        # Step 6: Create structure report
        safe_print("\nStep 6: Creating project structure report...")
        results['structure_report'] = self.create_project_structure_report()
        
        # Save final results
        final_report = self.root_dir / f"improvement_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(final_report, 'w') as f:
            json.dump(results, f, indent=2, default=str)
            
        safe_print("="*60)
        safe_print("🎉 Codebase improvement pipeline completed!")
        safe_print(f"📊 Final report saved to {final_report.name}")
        safe_print("="*60)
        
        return results


def main():
    """Main execution function"""
    safe_print("🔧 Sugarglitch RealOps - Codebase Improvement Tool")
    safe_print("="*60)
    safe_print("This tool will improve your codebase while preserving ALL sensitive data")
    safe_print("="*60)
    
    improver = CodebaseImprover()
    results = improver.run_improvement_pipeline()
    
    if results:
        safe_print("\n✅ All improvements completed successfully!")
        safe_print("📁 Check the following directories:")
        safe_print(f"   - backups/: Original files backup")
        safe_print(f"   - improved_code/: Enhanced Python files")
        safe_print(f"   - Root directory: Validation and analysis reports")
    else:
        safe_print("\n⚠️ Some improvements may have failed. Check the logs.")


if __name__ == "__main__":
    main()
