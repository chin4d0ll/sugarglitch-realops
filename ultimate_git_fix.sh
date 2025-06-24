#!/bin/bash
# 🔧 Ultimate Git Fix Script - แก้ไขปัญหา commit ทุกแบบ!

echo "🔧 Ultimate Git Fix - แก้ไขปัญหา commit"
echo "========================================"

echo "📋 Step 1: ลบการตั้งค่า GPG ทั้งหมด"
git config --global --unset commit.gpgsign 2>/dev/null
git config --global --unset tag.gpgsign 2>/dev/null  
git config --global --unset user.signingkey 2>/dev/null
git config --global --unset gpg.program 2>/dev/null
git config --local --unset commit.gpgsign 2>/dev/null
git config --local --unset tag.gpgsign 2>/dev/null
git config --local --unset user.signingkey 2>/dev/null
git config --local --unset gpg.program 2>/dev/null

echo "✅ ลบการตั้งค่า GPG แล้ว"

echo "📋 Step 2: ตั้งค่า Git อย่างชัดเจน"
git config --global user.name "chin4d0ll"
git config --global user.email "beamr.1232@gmail.com"
git config --global commit.gpgsign false
git config --global tag.gpgsign false

echo "✅ ตั้งค่า Git แล้ว"

echo "📋 Step 3: ตั้งค่าสำหรับ Codespaces"
export GIT_COMMITTER_NAME="chin4d0ll"
export GIT_COMMITTER_EMAIL="beamr.1232@gmail.com"
export GIT_AUTHOR_NAME="chin4d0ll"
export GIT_AUTHOR_EMAIL="beamr.1232@gmail.com"

echo "✅ ตั้งค่า environment variables"

echo "📋 Step 4: ทดสอบ commit"
echo "test commit $(date)" > git_fix_test.txt
git add git_fix_test.txt

if git commit -m "🔧 Test commit after ultimate fix"; then
    echo "🎉 Commit สำเร็จ!"
    rm git_fix_test.txt
    git add git_fix_test.txt
    git commit -m "🧹 Clean up test file"
    echo "✅ Git พร้อมใช้งานแล้ว!"
else
    echo "❌ ยังมีปัญหา - ลองดูขั้นตอนถัดไป"
fi

echo ""
echo "📝 การตั้งค่าปัจจุบัน:"
echo "Username: $(git config user.name)"
echo "Email: $(git config user.email)" 
echo "GPG Signing: $(git config commit.gpgsign)"

echo ""
echo "💡 หากยังมีปัญหา ให้รัน:"
echo "export GIT_AUTHOR_NAME='chin4d0ll'"
echo "export GIT_AUTHOR_EMAIL='beamr.1232@gmail.com'"
echo "export GIT_COMMITTER_NAME='chin4d0ll'"
echo "export GIT_COMMITTER_EMAIL='beamr.1232@gmail.com'"
echo ""
echo "แล้วลอง commit อีกครั้ง"
