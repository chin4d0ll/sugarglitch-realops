# 🚀 SQL Database - Complete Setup Guide

## ✅ Setup Complete

Your SQL database system is now fully operational and integrated with your existing SugarGlitch RealOps project.

## 📊 Current Status

- **Database**: `quick_realops.db` (Ready ✅)
- **Tables**: 4 main tables created
- **Records**: Targets, proxies, and logs populated
- **Integration**: Synced with existing configs

## 🛠️ Available Tools

### Core Files

1. **`quick_db_setup.py`** - Full database setup (run once)
2. **`db_helper.py`** - Simple database helper class
3. **`database_integrator.py`** - Sync with existing data
4. **`sql_interface.py`** - Interactive SQL command line

### Quick Commands

1. **`quick_status.py`** - Show current operation status
2. **`quick_add_target.py`** - Add new targets quickly
3. **`test_quick_db.py`** - Test database functionality

## ⚡ Quick Usage Examples

### Check Status

```bash
python3 quick_status.py
```

### Add New Target

```bash
python3 quick_add_target.py "new_username" 5 "High priority target"
```

### Interactive SQL

```bash
python3 sql_interface.py
# Then use commands: stats, tables, desc targets, or direct SQL
```

### Python Integration

```python
from db_helper import DBHelper

# Connect
db = DBHelper()
db.connect()

# Add target
db.add_target("username", "instagram", 5, "Notes")

# Get targets
targets = db.get_targets("active")

# Add log
db.add_log("extraction", "username", "success", "Data extracted")

# Custom query
results = db.execute("SELECT * FROM targets WHERE priority > 3")

db.close()
```

## 📋 Database Schema

### `targets` table

- **id**: Auto-increment primary key
- **username**: Target username (unique)
- **platform**: Platform (default: instagram)
- **status**: active/pending/completed
- **priority**: 1-5 (5 = highest)
- **notes**: Additional notes
- **created_at**: Timestamp

### `extracted_data` table

- **id**: Auto-increment primary key
- **target_id**: Link to targets table
- **data_type**: Type of extracted data
- **content**: JSON or text content
- **metadata**: Additional metadata
- **extracted_at**: Timestamp

### `proxy_sessions` table

- **id**: Auto-increment primary key
- **proxy_ip**: Proxy IP address
- **proxy_port**: Proxy port
- **session_id**: Unique session identifier
- **status**: active/standby/failed
- **last_used**: Last usage timestamp
- **success_count**: Successful operations
- **fail_count**: Failed operations

### `operation_logs` table

- **id**: Auto-increment primary key
- **operation_type**: Type of operation
- **target_username**: Target involved
- **status**: success/failed/pending
- **details**: Additional details
- **timestamp**: Operation timestamp

## 🎯 Current Data

### Targets (5 total)

- `alx.trading` - active (Priority: 5)
- `whatilove1728` - pending (Priority: 3)
- `test_target` - completed (Priority: 1)
- `new_target_test` - pending (Priority: 2)
- `demo_user_123` - pending (Priority: 4)

### Proxies (Available)

- Multiple proxy sessions configured
- Status tracking enabled

## 🔧 Advanced Usage

### Backup Database

```bash
cp quick_realops.db backup_$(date +%Y%m%d_%H%M%S).db
```

### Export Data

```bash
sqlite3 quick_realops.db ".dump" > database_backup.sql
```

### Custom Queries

```sql
-- High priority active targets
SELECT * FROM targets WHERE status='active' AND priority >= 4;

-- Proxy performance
SELECT proxy_ip, success_count, fail_count FROM proxy_sessions;

-- Recent operations
SELECT * FROM operation_logs ORDER BY timestamp DESC LIMIT 10;
```

## 📁 Generated Files

- `operation_dashboard.json` - Current operation status
- `DATABASE_READY.md` - Setup summary
- All integration scripts and helpers

## 🚨 Next Steps

1. **Integrate with existing extractors**: Modify your extraction scripts to log data to the database
2. **Proxy management**: Update proxy rotation to use database tracking
3. **Session persistence**: Save session data to database for recovery
4. **Monitoring**: Use dashboard for operation monitoring

---

**Database Status**: ✅ **READY FOR OPERATIONS**

**Quick Test**: `python3 quick_status.py`
**Last Updated**: May 26, 2025

พร้อมใช้งานเต็มรูปแบบแล้ว! 🎉
