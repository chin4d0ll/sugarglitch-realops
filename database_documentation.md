# Instagram Database Documentation

## Database Information
- **File**: extracted_project/Python/instagram_deep_data_alx.trading.db
- **Size**: 40,960 bytes
- **Total Tables**: 8
- **Total Records**: 0

## Tables Overview

### profile_data
- **Records**: 0
- **Columns**: 13

**Schema**:
- `id` (INTEGER)
- `username` (TEXT)
- `full_name` (TEXT)
- `biography` (TEXT)
- `external_url` (TEXT)
- `follower_count` (INTEGER)
- `following_count` (INTEGER)
- `post_count` (INTEGER)
- `is_verified` (BOOLEAN)
- `is_private` (BOOLEAN)
- `is_business` (BOOLEAN)
- `profile_pic_url` (TEXT)
- `extracted_at` (TEXT)

### posts
- **Records**: 0
- **Columns**: 12

**Schema**:
- `id` (INTEGER)
- `post_id` (TEXT)
- `shortcode` (TEXT)
- `caption` (TEXT)
- `likes_count` (INTEGER)
- `comments_count` (INTEGER)
- `timestamp` (TEXT)
- `media_urls` (TEXT)
- `hashtags` (TEXT)
- `mentions` (TEXT)
- `location` (TEXT)
- `extracted_at` (TEXT)

### followers
- **Records**: 0
- **Columns**: 8

**Schema**:
- `id` (INTEGER)
- `username` (TEXT)
- `full_name` (TEXT)
- `profile_pic_url` (TEXT)
- `is_verified` (BOOLEAN)
- `follower_count` (INTEGER)
- `following_count` (INTEGER)
- `extracted_at` (TEXT)

### following
- **Records**: 0
- **Columns**: 8

**Schema**:
- `id` (INTEGER)
- `username` (TEXT)
- `full_name` (TEXT)
- `profile_pic_url` (TEXT)
- `is_verified` (BOOLEAN)
- `follower_count` (INTEGER)
- `following_count` (INTEGER)
- `extracted_at` (TEXT)

### stories
- **Records**: 0
- **Columns**: 6

**Schema**:
- `id` (INTEGER)
- `story_id` (TEXT)
- `media_url` (TEXT)
- `timestamp` (TEXT)
- `views_count` (INTEGER)
- `extracted_at` (TEXT)

### direct_messages
- **Records**: 0
- **Columns**: 7

**Schema**:
- `id` (INTEGER)
- `thread_id` (TEXT)
- `participant` (TEXT)
- `message_text` (TEXT)
- `timestamp` (TEXT)
- `message_type` (TEXT)
- `extracted_at` (TEXT)

### comments
- **Records**: 0
- **Columns**: 8

**Schema**:
- `id` (INTEGER)
- `post_id` (TEXT)
- `comment_id` (TEXT)
- `username` (TEXT)
- `comment_text` (TEXT)
- `likes_count` (INTEGER)
- `timestamp` (TEXT)
- `extracted_at` (TEXT)

### activity_log
- **Records**: 0
- **Columns**: 6

**Schema**:
- `id` (INTEGER)
- `activity_type` (TEXT)
- `target_user` (TEXT)
- `target_post` (TEXT)
- `timestamp` (TEXT)
- `extracted_at` (TEXT)

