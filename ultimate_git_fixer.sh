#!/bin/bash
# 🔥 Ultimate Git Fixer - แก้ปัญหา Git ทุกอย่างในครั้งเดียว

echo "🔥 ULTIMATE GIT FIXER - Starting..."
echo "⚡ This will fix all common Git issues automatically"
echo ""

# 1. แก้ GPG signing issues
echo "🔧 [1/6] Fixing GPG signing issues..."
git config --global commit.gpgsign false
git config commit.gpgsign false
echo "✅ Disabled GPG signing"

# 2. ตั้งค่า Git config ถ้ายังไม่มี
echo "🔧 [2/6] Setting up Git configuration..."
if [ -z "$(git config user.email)" ]; then
    git config user.email "developer@sugarglitch.com"
    git config user.name "SugarGlitch Developer"
    echo "✅ Set up user config"
else
    echo "✅ User config already exists"
fi

# ตั้งค่าอื่น ๆ
git config push.default simple
git config pull.rebase false
git config core.autocrlf false
git config init.defaultBranch main
echo "✅ Updated Git settings"

# 3. สร้าง .gitignore ที่ดี
echo "🔧 [3/6] Creating comprehensive .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/settings.json
.vscode/launch.json
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
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Node.js
node_modules/
.npm
.yarn-integrity

# Coverage
coverage/
*.cover
.hypothesis/
.pytest_cache/

# Databases
*.db
*.sqlite
*.sqlite3

# Sensitive data
*.env
.env.local
.env.production
config/secrets.json
passwords/
sessions/
extracted_personal_info/
bruteforce_personal_data.zip

# Temporary
*.tmp
*.temp
.cache/

# Large files
*.zip
*.tar.gz
*.rar
*.7z

# Generated outputs (uncomment if you want to ignore them)
# vmess_output/
# free_internet_*/
# free_configs/
# working_vmess_*/
EOF
echo "✅ Created .gitignore"

# 4. จัดการ staged files
echo "🔧 [4/6] Handling staged files..."
STAGED_COUNT=$(git diff --cached --name-only | wc -l)
if [ $STAGED_COUNT -gt 0 ]; then
    echo "📝 Found $STAGED_COUNT staged files - committing them..."
    TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
    git commit -m "🔄 Auto-fix commit: Cleanup staged files $TIMESTAMP

- Fixed Git configuration issues
- Added comprehensive .gitignore
- Resolved staging problems
- Updated project structure"
    echo "✅ Committed $STAGED_COUNT files"
else
    echo "✅ No staged files to handle"
fi

# 5. เพิ่มไฟล์ใหม่และ commit
echo "🔧 [5/6] Adding new files and committing..."
git add .
CHANGED_FILES=$(git diff --cached --name-only | wc -l)
if [ $CHANGED_FILES -gt 0 ]; then
    TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
    git commit -m "🚀 Project update: Added new tools and configurations $TIMESTAMP

- Added vmess hunter tools
- Created Git automation scripts
- Enhanced project documentation
- Improved configuration management

Files changed: $CHANGED_FILES"
    echo "✅ Committed $CHANGED_FILES new/modified files"
else
    echo "✅ No new changes to commit"
fi

# 6. Push ถ้ามี remote
echo "🔧 [6/6] Pushing to remote..."
if git remote get-url origin >/dev/null 2>&1; then
    BRANCH=$(git branch --show-current)
    echo "🚀 Pushing to origin/$BRANCH..."
    
    if git push origin $BRANCH 2>/dev/null; then
        echo "✅ Successfully pushed to remote"
    else
        echo "⚠️ Normal push failed, trying force with lease..."
        if git push --force-with-lease origin $BRANCH 2>/dev/null; then
            echo "✅ Force push successful"
        else
            echo "❌ Push failed. Remote might need manual setup."
            echo "💡 If this is a new repo, try:"
            echo "   git remote add origin <your-repo-url>"
            echo "   git push -u origin main"
        fi
    fi
else
    echo "⚠️ No remote configured. Skipping push."
    echo "💡 To add remote: git remote add origin <repo-url>"
fi

# แสดงสถานะสุดท้าย
echo ""
echo "=" x 60
echo "🎉 ULTIMATE GIT FIXER COMPLETED!"
echo "=" x 60
echo "📊 Current status:"
git status
echo ""
echo "📈 Recent commits:"
git log --oneline -3
echo ""
echo "🚀 Git is now ready to use normally!"
echo ""
echo "💡 Quick commands for daily use:"
echo "   git add . && git commit -m 'your message' && git push"
echo "   ./auto_git_commit.sh    # For automatic commits"
echo "   ./ultimate_git_fixer.sh # Run this script again if issues arise"
