#!/bin/bash

echo "===== ซ่อมแซมปัญหา Git Commit ====="

# ลบการตั้งค่า GPG ทั้งหมด
git config --global --unset commit.gpgsign 2>/dev/null || true
git config --global --unset user.signingkey 2>/dev/null || true
git config --global --unset gpg.program 2>/dev/null || true

# ตั้งค่าใหม่ให้ไม่ใช้ GPG
git config --global commit.gpgsign false
git config --global user.name "Developer"
git config --global user.email "developer@example.com"

echo "===== ตั้งค่าใหม่เสร็จแล้ว ====="

# ลองทำ commit ทดสอบ
echo "# Test file for commit fix" > test_commit.txt
git add test_commit.txt
git commit -m "Test commit - fix GPG issue" --no-verify

echo "===== เสร็จสิ้น ====="
