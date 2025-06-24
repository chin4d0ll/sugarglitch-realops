#!/bin/bash

# ตั้งค่า environment variables
export GIT_COMMITTER_EMAIL="developer@example.com"
export GIT_COMMITTER_NAME="Developer"
export GIT_AUTHOR_EMAIL="developer@example.com"
export GIT_AUTHOR_NAME="Developer"

# ตรวจสอบว่ามีข้อความ commit หรือไม่
if [ -z "$1" ]; then
    echo "กรุณาระบุข้อความ commit"
    echo "ใช้งาน: ./easy_commit.sh \"ข้อความ commit\""
    exit 1
fi

# Add ไฟล์ทั้งหมดและ commit
git add .
git commit -m "$1" --no-gpg-sign --no-verify

echo "Commit เสร็จสิ้น!"
