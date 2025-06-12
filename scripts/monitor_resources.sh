#!/bin/bash
# VSCode Resource Monitor
echo "=== VSCode Resource Monitor ==="
echo "Memory Usage:"
free -h
echo ""
echo "Disk Usage:"
df -h | grep -E '(Filesystem|overlay|/dev/root)'
echo ""
echo "VSCode Processes:"
ps aux --sort=-%mem | grep -E '(vscode|extensionHost|Pylance)' | head -5
echo ""
echo "Last 5 VSCode crashes (if any):"
journalctl --user -u vscode-server --since "1 hour ago" | tail -5 2>/dev/null || echo "No crash logs found"
