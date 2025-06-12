#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Target Data Manager
Module สำหรับ import ข้อมูล targets ใช้งานใน modules อื่น
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class TargetManager:
    """Class สำหรับจัดการข้อมูล targets"""
    
    def __init__(self, data_file="data/realops_targets.json"):
        self.project_root = Path(__file__).parent
        self.data_file = self.project_root / data_file
        self.targets_data = {}
        self.load_targets()
    
    def load_targets(self):
        """โหลดข้อมูล targets จากไฟล์"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.targets_data = json.load(f)
                print(f"✅ Loaded {len(self.targets_data.get('targets', []))} targets")
            else:
                print(f"⚠️  Targets file not found: {self.data_file}")
                self.targets_data = {"targets": [], "metadata": {}}
        except Exception as e:
            print(f"❌ Error loading targets: {e}")
            self.targets_data = {"targets": [], "metadata": {}}
    
    def get_all_targets(self) -> List[Dict]:
        """ดึงข้อมูล targets ทั้งหมด"""
        return self.targets_data.get("targets", [])
    
    def get_target_by_username(self, username: str) -> Optional[Dict]:
        """ดึงข้อมูล target ตาม username"""
        for target in self.targets_data.get("targets", []):
            if target.get("username") == username:
                return target
        return None
    
    def get_high_value_targets(self) -> List[Dict]:
        """ดึงเฉพาะ high value targets"""
        return [
            target for target in self.targets_data.get("targets", [])
            if "high_value_target" in target.get("flags", [])
        ]
    
    def get_targets_with_sessions(self) -> List[Dict]:
        """ดึง targets ที่มี session data"""
        return [
            target for target in self.targets_data.get("targets", [])
            if target.get("sessions") and len(target["sessions"]) > 0
        ]
    
    def get_targets_with_passwords(self) -> List[Dict]:
        """ดึง targets ที่รู้ password"""
        return [
            target for target in self.targets_data.get("targets", [])
            if "password_known" in target.get("flags", [])
        ]
    
    def get_contact_info(self, username: str) -> Dict:
        """ดึงข้อมูลติดต่อของ target"""
        target = self.get_target_by_username(username)
        if target:
            return {
                "email": target.get("email", []),
                "phone": target.get("phone", []),
                "aliases": target.get("aliases", [])
            }
        return {"email": [], "phone": [], "aliases": []}
    
    def list_targets_summary(self):
        """แสดงสรุปข้อมูล targets"""
        targets = self.get_all_targets()
        print("\n🎯 TARGETS SUMMARY:")
        print("=" * 40)
        
        for target in targets:
            print(f"👤 {target['username']}:")
            print(f"   📧 Emails: {len(target.get('email', []))}")
            print(f"   📱 Phones: {len(target.get('phone', []))}")
            print(f"   🔐 Sessions: {len(target.get('sessions', []))}")
            print(f"   🏷️  Flags: {', '.join(target.get('flags', []))}")
            
            # Show critical info
            if target.get('business_info', {}).get('password'):
                print(f"   🔑 Password: {target['business_info']['password']}")
            if target.get('email'):
                print(f"   📧 Primary Email: {target['email'][0]}")
            if target.get('phone'):
                print(f"   📱 Primary Phone: {target['phone'][0]}")
            print()
    
    def export_for_module(self, target_username: str) -> Dict:
        """Export ข้อมูลสำหรับใช้ใน module อื่น"""
        target = self.get_target_by_username(target_username)
        if not target:
            return {}
        
        # Format for easy use in penetration modules
        return {
            "username": target["username"],
            "credentials": {
                "password": target.get("business_info", {}).get("password"),
                "emails": target.get("email", []),
                "phones": target.get("phone", [])
            },
            "sessions": target.get("sessions", []),
            "aliases": target.get("aliases", []),
            "flags": target.get("flags", []),
            "is_high_value": "high_value_target" in target.get("flags", []),
            "has_password": "password_known" in target.get("flags", []),
            "business_info": target.get("business_info", {})
        }


# Global instance สำหรับ import ง่าย
target_manager = TargetManager()


# Convenience functions
def get_all_targets():
    """Quick access to all targets"""
    return target_manager.get_all_targets()


def get_target(username):
    """Quick access to specific target"""
    return target_manager.get_target_by_username(username)


def get_high_value_targets():
    """Quick access to high value targets"""
    return target_manager.get_high_value_targets()


def get_credentials(username):
    """Quick access to credentials"""
    export_data = target_manager.export_for_module(username)
    return export_data.get("credentials", {})


def show_targets():
    """Quick display of targets"""
    target_manager.list_targets_summary()


# Example usage
if __name__ == "__main__":
    print("🔥 SugarGlitch RealOps - Target Manager Demo")
    print("=" * 50)
    
    # Show all targets
    target_manager.list_targets_summary()
    
    # Demo specific target access
    print("🎯 Demo: ALX Trading Access")
    print("-" * 30)
    alx_data = target_manager.export_for_module("alx.trading")
    if alx_data:
        print(f"Username: {alx_data['username']}")
        print(f"Password: {alx_data['credentials']['password']}")
        print(f"Email: {alx_data['credentials']['emails']}")
        print(f"Phone: {alx_data['credentials']['phones']}")
        print(f"High Value: {alx_data['is_high_value']}")
        print(f"Session Files: {len(alx_data['sessions'])}")
    
    print("\n💡 Usage in other modules:")
    print("from target_manager import get_target, get_credentials")
    print("target = get_target('alx.trading')")
    print("creds = get_credentials('alx.trading')")
    print("high_value = get_high_value_targets()")
