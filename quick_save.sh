#!/bin/bash
# 🔥💾 QUICK SAVE COMMANDS FOR SUGARGLITCH REALOPS 💾🔥
# =====================================================
# คำสั่งลัดสำหรับ save, commit และ push
#
# Usage:
#   ./quick_save.sh              # Auto commit & push
#   ./quick_save.sh "message"    # Custom message
#   ./quick_save.sh --local      # Local commit only
#   ./quick_save.sh --help       # Show help

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🔥💾 SUGARGLITCH REALOPS QUICK SAVE${NC}"
echo "=================================="

# Check arguments
case "$1" in
    "--help"|"-h")
        echo -e "${BLUE}📖 Usage:${NC}"
        echo "  ./quick_save.sh              # Auto commit & push"
        echo "  ./quick_save.sh \"message\"    # Custom message"
        echo "  ./quick_save.sh --local      # Local commit only"
        echo "  ./quick_save.sh --help       # Show this help"
        exit 0
        ;;
    "--local")
        echo -e "${YELLOW}📍 Local commit only mode${NC}"
        python3 smart_auto_commit.py --local-only
        ;;
    "")
        echo -e "${GREEN}🚀 Auto commit & push mode${NC}"
        python3 smart_auto_commit.py
        ;;
    *)
        echo -e "${BLUE}💬 Custom message mode${NC}"
        python3 smart_auto_commit.py -m "$1"
        ;;
esac

echo ""
echo -e "${GREEN}✅ Quick save completed!${NC}"
