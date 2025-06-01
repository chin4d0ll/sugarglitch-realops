#!/bin/bash
# 🔄💾 SugarGlitch Backup Manager 💾🔄
# Simple script to manage database backups

BASEDIR="/workspaces/sugarglitch-realops"
export PYTHONPATH="$BASEDIR"

# Colors
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

echo -e "${BLUE}💾🔥 SUGARGLITCH BACKUP MANAGER 🔥💾${NC}"
echo "========================================"

case "$1" in
    create)
        echo -e "${GREEN}Creating backup...${NC}"
        python3 "$BASEDIR/database_backup_system.py" backup
        ;;
        
    status)
        echo -e "${BLUE}Checking backup status...${NC}"
        python3 "$BASEDIR/database_backup_system.py" status
        ;;
        
    daemon)
        echo -e "${GREEN}Starting backup daemon in background...${NC}"
        nohup python3 "$BASEDIR/database_backup_system.py" daemon > "$BASEDIR/logs/backup_daemon.log" 2>&1 &
        echo -e "${GREEN}✓ Daemon started! (PID: $!)${NC}"
        ;;
        
    restore)
        echo -e "${YELLOW}Restoring latest backup...${NC}"
        
        # Find latest backup
        LATEST_BACKUP=$(find "$BASEDIR/backups/database/" -name "*.db" -type f -printf "%T+ %p\n" | sort -r | head -n 1 | cut -d' ' -f2-)
        
        if [ -z "$LATEST_BACKUP" ]; then
            echo -e "${RED}❌ No backup found!${NC}"
            exit 1
        fi
        
        echo -e "${YELLOW}Found backup: $(basename "$LATEST_BACKUP")${NC}"
        echo -e "${YELLOW}⚠️ This will replace the current database. Continue? (y/n)${NC}"
        read -r confirm
        
        if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
            cp "$LATEST_BACKUP" "$BASEDIR/databases/sugarglitch_realops_master.db"
            echo -e "${GREEN}✓ Database restored successfully!${NC}"
        else
            echo -e "${YELLOW}Restore canceled.${NC}"
        fi
        ;;
        
    list)
        echo -e "${BLUE}Available backups:${NC}"
        find "$BASEDIR/backups/database/" -name "*.db" -type f -printf "%T+ %p\n" | sort -r | head -n 10 | while read -r line; do
            file=$(echo "$line" | cut -d' ' -f2-)
            date=$(echo "$line" | cut -d' ' -f1)
            size=$(du -h "$file" | cut -f1)
            echo -e "${YELLOW}$(basename "$file")${NC} [${BLUE}$date${NC}] ${GREEN}$size${NC}"
        done
        ;;
        
    *)
        echo -e "Usage: ${YELLOW}$0 <command>${NC}"
        echo "Commands:"
        echo -e "  ${GREEN}create${NC}   - Create new backup"
        echo -e "  ${GREEN}status${NC}   - Check backup status"
        echo -e "  ${GREEN}daemon${NC}   - Start backup daemon"
        echo -e "  ${GREEN}restore${NC}  - Restore latest backup"
        echo -e "  ${GREEN}list${NC}     - List available backups"
        ;;
esac

echo ""
echo -e "${BLUE}Created by: น้องจิน (chin4d0ll) ♥️${NC}"
