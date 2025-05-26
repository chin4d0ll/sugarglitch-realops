-- Database Overview Queries
-- Generated automatically for Instagram Deep Data DB
-- Database: extracted_project/Python/instagram_deep_data_alx.trading.db
-- Total Records: 0

-- Show all tables and their record counts
SELECT 'profile_data' as table_name, COUNT(*) as record_count FROM profile_data
UNION ALL
SELECT 'posts' as table_name, COUNT(*) as record_count FROM posts
UNION ALL
SELECT 'followers' as table_name, COUNT(*) as record_count FROM followers
UNION ALL
SELECT 'following' as table_name, COUNT(*) as record_count FROM following
UNION ALL
SELECT 'stories' as table_name, COUNT(*) as record_count FROM stories
UNION ALL
SELECT 'direct_messages' as table_name, COUNT(*) as record_count FROM direct_messages
UNION ALL
SELECT 'comments' as table_name, COUNT(*) as record_count FROM comments
UNION ALL
SELECT 'activity_log' as table_name, COUNT(*) as record_count FROM activity_log
;

-- Sample queries for each table:

-- profile_data table sample
SELECT * FROM profile_data LIMIT 10;

-- Unique usernames in profile_data
SELECT DISTINCT username FROM profile_data LIMIT 10;

-- posts table sample
SELECT * FROM posts LIMIT 10;

-- Recent records from posts
SELECT * FROM posts ORDER BY timestamp DESC LIMIT 5;

-- followers table sample
SELECT * FROM followers LIMIT 10;

-- Unique usernames in followers
SELECT DISTINCT username FROM followers LIMIT 10;

-- following table sample
SELECT * FROM following LIMIT 10;

-- Unique usernames in following
SELECT DISTINCT username FROM following LIMIT 10;

-- stories table sample
SELECT * FROM stories LIMIT 10;

-- Recent records from stories
SELECT * FROM stories ORDER BY timestamp DESC LIMIT 5;

-- direct_messages table sample
SELECT * FROM direct_messages LIMIT 10;

-- Recent records from direct_messages
SELECT * FROM direct_messages ORDER BY timestamp DESC LIMIT 5;

-- comments table sample
SELECT * FROM comments LIMIT 10;

-- Recent records from comments
SELECT * FROM comments ORDER BY timestamp DESC LIMIT 5;

-- Unique usernames in comments
SELECT DISTINCT username FROM comments LIMIT 10;

-- activity_log table sample
SELECT * FROM activity_log LIMIT 10;

-- Recent records from activity_log
SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT 5;
