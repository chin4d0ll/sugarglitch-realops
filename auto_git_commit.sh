#!/bin/bash
# 🔥 Auto Git Commit & Push Script
# จัดการ Git ให้เสร็จในครั้งเดียว

echo "🔥 Auto Git Manager - Starting..."

# ตั้งค่า Git config ถ้ายังไม่มี
if [ -z "$(git config user.email)" ]; then
    echo "⚙️ Setting up git config..."
    git config user.email "developer@sugarglitch.com"
    git config user.name "SugarGlitch Developer"
fi

# สร้าง .gitignore ที่ดี
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/settings.json
.vscode/launch.json
.vscode/extensions.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Dependencies
node_modules/
.npm
.yarn-integrity

# Coverage directory used by tools like istanbul
coverage/
*.cover
.hypothesis/
.pytest_cache/

# Temporary files
*.tmp
*.temp
.cache/

# Large files that shouldn't be in repo
*.zip
*.tar.gz
*.rar
*.7z

# Sensitive data
*.env
.env.local
.env.production
config/secrets.json
passwords/
sessions/
extracted_personal_info/
bruteforce_personal_data.zip

# Build outputs
dist/
build/
*.egg-info/

# Database
*.db
*.sqlite
*.sqlite3

# Docker
.dockerignore
EOF
fi

# แสดงสถานะปัจจุบัน
echo "📊 Current git status:"
git status --short

# เพิ่มไฟล์ทั้งหมด (ยกเว้นที่อยู่ใน .gitignore)
echo "➕ Adding all files..."
git add .

# สร้าง commit message ที่มีความหมาย
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
BRANCH=$(git branch --show-current)
CHANGED_FILES=$(git diff --cached --name-only | wc -l)

COMMIT_MSG="🚀 Auto-commit: Updated $CHANGED_FILES files on $TIMESTAMP

- Updated vmess hunter tools
- Added new configurations
- Improved project structure
- Enhanced documentation

Branch: $BRANCH
Auto-generated commit"

# Commit
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"

# ตรวจสอบว่ามี remote origin หรือไม่
if git remote get-url origin >/dev/null 2>&1; then
    echo "🚀 Pushing to remote..."
    
    # ลองทำ push ปกติก่อน
    if git push origin $BRANCH 2>/dev/null; then
        echo "✅ Successfully pushed to origin/$BRANCH"
    else
        echo "⚠️ Normal push failed, trying force push..."
        # ถ้า push ไม่ได้ ให้ force push (ระวัง!)
        git push --force-with-lease origin $BRANCH
        if [ $? -eq 0 ]; then
            echo "✅ Force push successful"
        else
            echo "❌ Push failed completely. Manual intervention needed."
            echo "🔧 Try: git pull --rebase origin $BRANCH && git push"
        fi
    fi
else
    echo "⚠️ No remote origin found. Skipping push."
    echo "💡 To add remote: git remote add origin <your-repo-url>"
fi

# แสดงสถานะสุดท้าย
echo "📈 Final status:"
git status
echo ""
echo "🎉 Git operations completed!"
echo "📝 Last commit: $(git log -1 --oneline)"
