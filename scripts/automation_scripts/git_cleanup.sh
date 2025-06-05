#!/bin/bash
"""
Git Cleanup Script - จัดการ source control
"""

echo "🔄 Git Cleanup and Organization Script"
echo "=================================="

# Add all recovered files
echo "📁 Adding recovered files..."
git add .

# Check current status
echo "📊 Current git status:"
git status --short | wc -l

echo "✅ All files staged for commit"
echo ""
echo "To commit these changes, run:"
echo "git commit -m 'File recovery and reorganization complete'"
echo ""
echo "To see detailed status:"
echo "git status"
