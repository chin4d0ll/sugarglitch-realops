#!/bin/bash

echo "===== เริ่มการเคลียร์แคชโปรเจกต์ ====="

# เคลียร์ Python cache
echo "🧹 ลบ Python cache files..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# เคลียร์ Node.js cache (ถ้ามี)
echo "🧹 ลบ Node.js cache files..."
rm -rf node_modules 2>/dev/null || true
rm -f package-lock.json 2>/dev/null || true
rm -f yarn.lock 2>/dev/null || true

# เคลียร์ temporary files
echo "🧹 ลบไฟล์ชั่วคราว..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true

# เคลียร์ log files
echo "🧹 ลบไฟล์ log..."
find . -name "*.log" -delete 2>/dev/null || true

# เคลียร์ backup files
echo "🧹 ลบไฟล์สำรอง..."
find . -name "*.bak" -delete 2>/dev/null || true
find . -name "*.backup" -delete 2>/dev/null || true

# เคลียร์ VS Code cache
echo "🧹 ลบ VS Code cache..."
rm -rf .vscode/.ropeproject 2>/dev/null || true

# เคลียร์ Git cache (soft clean)
echo "🧹 ทำความสะอาด Git cache..."
git gc --prune=now 2>/dev/null || true

# เคลียร์ Docker cache (ถ้าใช้)
echo "🧹 ลบ Docker cache..."
rm -rf .dockerignore 2>/dev/null || true

# สร้าง .gitignore ใหม่ถ้ายังไม่มี
if [ ! -f .gitignore ]; then
    echo "📝 สร้าง .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
*.bak
*.backup

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
EOF
fi

echo "✅ เคลียร์แคชเสร็จสิ้น!"
echo "📊 ขนาดโปรเจกต์ปัจจุบัน:"
du -sh . 2>/dev/null || echo "ไม่สามารถคำนวณขนาดได้"

echo ""
echo "🚀 โปรเจกต์ได้รับการทำความสะอาดแล้ว!"
