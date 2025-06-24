#!/bin/bash
# Easy Commit Script
echo "🚀 Easy Git Commit"
echo "=================="

# Add all files
git add .
echo "✅ Added all files"

# Get commit message
if [ "$1" != "" ]; then
    MESSAGE="$1"
else
    echo "📝 Enter commit message:"
    read MESSAGE
fi

# Commit
git commit -m "$MESSAGE"

if [ $? -eq 0 ]; then
    echo "🎉 Commit successful!"
    echo "💫 Push to GitHub? (y/n)"
    read PUSH
    if [ "$PUSH" = "y" ] || [ "$PUSH" = "Y" ]; then
        git push
        echo "🌟 Pushed to GitHub!"
    fi
else
    echo "❌ Commit failed"
fi
