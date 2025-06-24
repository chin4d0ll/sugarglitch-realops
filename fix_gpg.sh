#!/bin/bash

# ลบการตั้งค่า GPG ทั้งหมด
git config --global --unset commit.gpgsign
git config --global --unset user.signingkey
git config --global gpg.program ""

# ตั้งค่าให้ไม่ใช้ GPG
git config --global commit.gpgsign false

# ตรวจสอบผล
echo "==== ข้อมูลการตั้งค่า Git ====="
git config --global --list

# ลองทำ commit ไฟล์
echo "# Next Level Applications" > next_level_applications.py
git add next_level_applications.py
git commit -m "Add next level applications file" --no-verify

echo "==== เสร็จสิ้น! ====="
