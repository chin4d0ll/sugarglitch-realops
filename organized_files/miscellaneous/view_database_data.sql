-- Query ข้อมูลจากฐานข้อมูล Advanced DM Database
-- ไฟล์: advanced_dm_database_1748742706.sqlite

-- แสดงข้อมูลทั้งหมดจาก extraction_sessions
SELECT '=== EXTRACTION SESSIONS ===' as section;
SELECT * FROM extraction_sessions;

-- แสดงข้อมูลทั้งหมดจาก dm_threads  
SELECT '=== DM THREADS ===' as section;
SELECT * FROM dm_threads;

-- แสดงข้อมูลทั้งหมดจาก dm_messages
SELECT '=== DM MESSAGES ===' as section;
SELECT * FROM dm_messages ORDER BY timestamp;

-- สรุปสถิติ
SELECT '=== SUMMARY STATISTICS ===' as section;
SELECT 
    'Total Sessions' as metric, 
    COUNT(*) as count 
FROM extraction_sessions
UNION ALL
SELECT 
    'Total Threads' as metric, 
    COUNT(*) as count 
FROM dm_threads
UNION ALL
SELECT 
    'Total Messages' as metric, 
    COUNT(*) as count 
FROM dm_messages;
