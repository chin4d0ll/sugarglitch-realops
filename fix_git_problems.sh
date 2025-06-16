#!/bin/bash
# 🔧 Git Problem Fixer - แก้ปัญหา Git ทุกแบบ

echo "🔧 Git Problem Fixer - Starting diagnosis..."

# ฟังก์ชันตรวจสอบและแก้ปัญหา
fix_git_config() {
    echo "⚙️ Fixing Git configuration..."
    
    # ตั้งค่า user ถ้ายังไม่มี
    if [ -z "$(git config user.email)" ]; then
        git config user.email "developer@sugarglitch.com"
        git config user.name "SugarGlitch Developer"
        echo "✅ Set git user config"
    fi
    
    # ตั้งค่าอื่น ๆ ที่สำคัญ
    git config push.default simple
    git config pull.rebase false
    git config core.autocrlf false
    git config init.defaultBranch main
    echo "✅ Updated git settings"
}

fix_staging_issues() {
    echo "🔄 Fixing staging issues..."
    
    # ตรวจสอบ staged files
    STAGED_COUNT=$(git diff --cached --name-only | wc -l)
    
    if [ $STAGED_COUNT -gt 0 ]; then
        echo "📝 Found $STAGED_COUNT staged files"
        
        # ถาม user ว่าจะทำอะไร
        echo "Choose an action:"
        echo "1) Commit all staged files"
        echo "2) Unstage all files"
        echo "3) Show staged files"
        echo "4) Continue without changes"
        
        read -p "Enter choice (1-4): " choice
        
        case $choice in
            1)
                TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
                git commit -m "🔄 Auto-fix commit: Staged files cleanup $TIMESTAMP"
                echo "✅ Committed staged files"
                ;;
            2)
                git reset HEAD
                echo "✅ Unstaged all files"
                ;;
            3)
                echo "📋 Staged files:"
                git diff --cached --name-only
                ;;
            4)
                echo "⏭️ Skipping staged files"
                ;;
            *)
                echo "❌ Invalid choice"
                ;;
        esac
    else
        echo "✅ No staging issues found"
    fi
}

fix_branch_issues() {
    echo "🌿 Checking branch issues..."
    
    CURRENT_BRANCH=$(git branch --show-current)
    echo "📍 Current branch: $CURRENT_BRANCH"
    
    # ตรวจสอบ remote tracking
    if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
        echo "⚠️ No upstream branch set"
        if git ls-remote --heads origin $CURRENT_BRANCH >/dev/null 2>&1; then
            git branch --set-upstream-to=origin/$CURRENT_BRANCH $CURRENT_BRANCH
            echo "✅ Set upstream to origin/$CURRENT_BRANCH"
        else
            echo "💡 Run: git push -u origin $CURRENT_BRANCH"
        fi
    else
        echo "✅ Upstream branch is set"
    fi
}

fix_merge_conflicts() {
    echo "⚔️ Checking for merge conflicts..."
    
    if git status | grep -q "Unmerged paths"; then
        echo "🚨 Merge conflicts detected!"
        echo "📋 Conflicted files:"
        git status --short | grep "^UU"
        
        echo "🔧 Suggested actions:"
        echo "1. Edit conflicted files manually"
        echo "2. Use: git mergetool"
        echo "3. Abort merge: git merge --abort"
        echo "4. Continue after resolving: git commit"
    else
        echo "✅ No merge conflicts"
    fi
}

fix_remote_issues() {
    echo "🌐 Checking remote configuration..."
    
    if git remote get-url origin >/dev/null 2>&1; then
        REMOTE_URL=$(git remote get-url origin)
        echo "📡 Remote origin: $REMOTE_URL"
        
        # ทดสอบ connection
        if git ls-remote origin >/dev/null 2>&1; then
            echo "✅ Remote connection OK"
        else
            echo "❌ Cannot connect to remote"
            echo "🔧 Try: git remote set-url origin <correct-url>"
        fi
    else
        echo "⚠️ No remote origin configured"
        echo "💡 Add remote: git remote add origin <repo-url>"
    fi
}

create_gitignore() {
    if [ ! -f .gitignore ]; then
        echo "📝 Creating comprehensive .gitignore..."
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
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated
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

# Sensitive files
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

# Generated outputs
vmess_output/
free_internet_*/
free_configs/
working_vmess_*/
EOF
        echo "✅ Created .gitignore"
    else
        echo "✅ .gitignore already exists"
    fi
}

# เรียกใช้ฟังก์ชันทั้งหมด
main() {
    echo "🔍 Running complete Git diagnosis..."
    echo "=" x 50
    
    fix_git_config
    echo ""
    
    create_gitignore
    echo ""
    
    fix_staging_issues
    echo ""
    
    fix_branch_issues
    echo ""
    
    fix_merge_conflicts
    echo ""
    
    fix_remote_issues
    echo ""
    
    echo "=" x 50
    echo "🎉 Git diagnosis completed!"
    echo ""
    echo "📊 Current status:"
    git status --short
    echo ""
    echo "🚀 Ready to use Git normally!"
    echo ""
    echo "💡 Quick commands:"
    echo "   ./auto_git_commit.sh  - Auto commit & push"
    echo "   git add . && git commit -m 'message' && git push"
}

# รันฟังก์ชันหลัก
main
