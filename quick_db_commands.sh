#!/bin/bash
# 🔍 Quick Database Commands - คำสั่งดูข้อมูลเร็วๆ

echo "🗄️ Quick Database Viewer Commands"
echo "================================"

DB_FILE="project_realops.db"

echo "📊 1. ดูตารางทั้งหมด:"
echo "sqlite3 $DB_FILE \"SELECT name FROM sqlite_master WHERE type='table';\""

echo ""
echo "🎯 2. ดู Targets ล่าสุด:"
echo "sqlite3 $DB_FILE \"SELECT id, name, type, target_value, status, created_at FROM targets ORDER BY created_at DESC LIMIT 10;\""

echo ""
echo "📋 3. ดู Operation Logs ล่าสุด:"
echo "sqlite3 $DB_FILE \"SELECT operation_type, message, created_at FROM operation_logs ORDER BY created_at DESC LIMIT 10;\""

echo ""
echo "📈 4. ดูสถิติ Operations:"
echo "sqlite3 $DB_FILE \"SELECT operation_type, COUNT(*) as count FROM operation_logs GROUP BY operation_type ORDER BY count DESC;\""

echo ""
echo "⏰ 5. ดูกิจกรรมวันนี้:"
echo "sqlite3 $DB_FILE \"SELECT operation_type, message, created_at FROM operation_logs WHERE date(created_at) = date('now') ORDER BY created_at DESC;\""

echo ""
echo "🔍 6. ค้นหาใน logs (แทน 'keyword' ด้วยคำที่ต้องการ):"
echo "sqlite3 $DB_FILE \"SELECT * FROM operation_logs WHERE message LIKE '%keyword%' ORDER BY created_at DESC;\""

echo ""
echo "📊 7. ดูอัตราความสำเร็จ:"
echo "sqlite3 $DB_FILE \"SELECT CASE WHEN message LIKE '%success%' OR message LIKE '%completed%' THEN 'Success' WHEN message LIKE '%failed%' OR message LIKE '%error%' THEN 'Failed' ELSE 'Other' END as result, COUNT(*) FROM operation_logs GROUP BY result;\""

echo ""
echo "🎯 8. ดู Targets ที่ Active:"
echo "sqlite3 $DB_FILE \"SELECT * FROM targets WHERE status = 'active';\""

echo ""
echo "🚀 รันคำสั่งโดยตรง:"
echo "sqlite3 $DB_FILE"
