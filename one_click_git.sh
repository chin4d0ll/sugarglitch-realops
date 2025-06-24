#!/bin/bash
# 🚀 One-Click Git Commit & Push Tool
# ใช้งานง่าย กดปุ่มเดียวเท่านั้น!

# สีสำหรับ output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 One-Click Git Tool${NC}"
echo "======================="

# Function to show status
show_status() {
    echo -e "${YELLOW}📊 Git Status:${NC}"
    git status --porcelain
    echo ""
}

# Function to add all files
add_files() {
    echo -e "${BLUE}📁 Adding all files...${NC}"
    git add .
    echo -e "${GREEN}✅ Files added${NC}"
}

# Function to commit
commit_files() {
    # Auto-generate commit message with timestamp
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    DEFAULT_MSG="🔧 Auto commit - $TIMESTAMP"
    
    echo -e "${BLUE}💬 Commit message options:${NC}"
    echo "1. Use default: $DEFAULT_MSG"
    echo "2. Enter custom message"
    echo "3. Quick templates"
    echo ""
    
    read -p "Choose (1/2/3) or press Enter for default: " choice
    
    case $choice in
        2)
            echo "Enter your commit message:"
            read -p "> " COMMIT_MSG
            ;;
        3)
            echo "Quick templates:"
            echo "a) 🐛 Bug fix"
            echo "b) ✨ New feature" 
            echo "c) 📝 Update docs"
            echo "d) 🔧 Maintenance"
            echo "e) 🎨 UI/Style changes"
            read -p "Choose template (a/b/c/d/e): " template
            case $template in
                a) COMMIT_MSG="🐛 Bug fix - $TIMESTAMP" ;;
                b) COMMIT_MSG="✨ New feature - $TIMESTAMP" ;;
                c) COMMIT_MSG="📝 Update docs - $TIMESTAMP" ;;
                d) COMMIT_MSG="🔧 Maintenance - $TIMESTAMP" ;;
                e) COMMIT_MSG="🎨 UI/Style changes - $TIMESTAMP" ;;
                *) COMMIT_MSG="$DEFAULT_MSG" ;;
            esac
            ;;
        *)
            COMMIT_MSG="$DEFAULT_MSG"
            ;;
    esac
    
    echo -e "${BLUE}📝 Committing with message: $COMMIT_MSG${NC}"
    
    if git commit -m "$COMMIT_MSG"; then
        echo -e "${GREEN}✅ Commit successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Commit failed!${NC}"
        return 1
    fi
}

# Function to push
push_files() {
    echo -e "${BLUE}🌐 Pushing to GitHub...${NC}"
    
    if git push; then
        echo -e "${GREEN}🎉 Push successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Push failed!${NC}"
        echo -e "${YELLOW}💡 Trying to set upstream...${NC}"
        
        # Try to set upstream and push
        BRANCH=$(git branch --show-current)
        if git push --set-upstream origin $BRANCH; then
            echo -e "${GREEN}🎉 Push successful after setting upstream!${NC}"
            return 0
        else
            echo -e "${RED}❌ Push still failed${NC}"
            return 1
        fi
    fi
}

# Main menu
main_menu() {
    echo -e "${YELLOW}🎯 What would you like to do?${NC}"
    echo "1. 🚀 Quick commit & push (recommended)"
    echo "2. 📊 Just show status"
    echo "3. 📁 Add files only"
    echo "4. 💬 Commit only (no push)"
    echo "5. 🌐 Push only"
    echo "6. ⚙️  Fix Git config"
    echo "7. 🆘 Emergency: Reset & fix everything"
    echo ""
    
    read -p "Choose option (1-7) or press Enter for option 1: " option
    
    case $option in
        2)
            show_status
            ;;
        3)
            show_status
            add_files
            ;;
        4)
            show_status
            add_files
            commit_files
            ;;
        5)
            push_files
            ;;
        6)
            fix_git_config
            ;;
        7)
            emergency_fix
            ;;
        *)
            # Default: Quick commit & push
            echo -e "${BLUE}🚀 Starting quick commit & push...${NC}"
            show_status
            
            # Check if there are changes
            if [ -z "$(git status --porcelain)" ]; then
                echo -e "${YELLOW}📭 No changes to commit${NC}"
                exit 0
            fi
            
            add_files
            if commit_files; then
                push_files
            fi
            ;;
    esac
}

# Fix Git config function
fix_git_config() {
    echo -e "${BLUE}⚙️ Fixing Git configuration...${NC}"
    
    git config --global user.name "chin4d0ll"
    git config --global user.email "beamr.1232@gmail.com"
    git config --global commit.gpgsign false
    git config --global tag.gpgsign false
    
    # Set environment variables
    export GIT_AUTHOR_NAME="chin4d0ll"
    export GIT_AUTHOR_EMAIL="beamr.1232@gmail.com"
    export GIT_COMMITTER_NAME="chin4d0ll" 
    export GIT_COMMITTER_EMAIL="beamr.1232@gmail.com"
    
    echo -e "${GREEN}✅ Git config fixed!${NC}"
    echo "Username: $(git config user.name)"
    echo "Email: $(git config user.email)"
}

# Emergency fix function
emergency_fix() {
    echo -e "${RED}🆘 EMERGENCY FIX MODE${NC}"
    echo "This will reset Git settings and fix common issues"
    read -p "Continue? (y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}🔧 Running emergency fixes...${NC}"
        
        # Reset Git config
        git config --global --unset commit.gpgsign 2>/dev/null
        git config --global --unset tag.gpgsign 2>/dev/null
        git config --global --unset user.signingkey 2>/dev/null
        git config --global --unset gpg.program 2>/dev/null
        
        # Set fresh config
        fix_git_config
        
        # Clean up any problematic files
        rm -f .git/COMMIT_EDITMSG 2>/dev/null
        rm -f .git/index.lock 2>/dev/null
        
        echo -e "${GREEN}🎉 Emergency fix completed!${NC}"
        echo -e "${YELLOW}💡 Try committing again${NC}"
    else
        echo -e "${YELLOW}Emergency fix cancelled${NC}"
    fi
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a Git repository!${NC}"
    echo -e "${YELLOW}💡 Initialize git with: git init${NC}"
    exit 1
fi

# Run main menu
main_menu

echo ""
echo -e "${BLUE}🏁 Git tool finished!${NC}"
