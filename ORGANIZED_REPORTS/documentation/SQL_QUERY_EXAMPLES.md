# 📚 SQL Query Examples - ตัวอย่าง SQL ที่มีประโยชน์

## 🎯 1. การจัดการ Targets (เป้าหมาย)

### ค้นหาเป้าหมายตาม Priority และ Status
```sql
-- เป้าหมาย Critical ที่ยังไม่เสร็จ
SELECT target_name, target_value, priority, status, scan_count 
FROM targets 
WHERE priority = 4 AND status != 'completed'
ORDER BY scan_count ASC;

-- เป้าหมายที่สแกนบ่อยที่สุด
SELECT target_name, target_type, scan_count, last_scanned
FROM targets 
ORDER BY scan_count DESC 
LIMIT 5;

-- เป้าหมายที่ไม่ได้สแกนนานแล้ว
SELECT target_name, target_value, last_scanned, 
       datetime('now') - last_scanned as days_since_scan
FROM targets 
WHERE last_scanned IS NOT NULL
ORDER BY last_scanned ASC;
```

---

## 🔍 2. การวิเคราะห์ข้อมูล Extracted Data

### หา Target ที่มี Risk Score สูง
```sql
-- Top 5 targets ที่มี risk สูงสุด
SELECT t.target_name, t.target_value, e.risk_score, e.summary, e.data_type
FROM extracted_data e
JOIN targets t ON e.target_id = t.id
ORDER BY e.risk_score DESC
LIMIT 5;

-- เปรียบเทียบ Risk Score ระหว่าง data types
SELECT data_type, 
       COUNT(*) as total_scans,
       AVG(risk_score) as avg_risk,
       MAX(risk_score) as max_risk,
       MIN(risk_score) as min_risk
FROM extracted_data
GROUP BY data_type
ORDER BY avg_risk DESC;

-- หา targets ที่มี findings มาก
SELECT t.target_name, e.data_type, e.findings_count, e.risk_score
FROM extracted_data e
JOIN targets t ON e.target_id = t.id
WHERE e.findings_count > 0
ORDER BY e.findings_count DESC;
```

---

## 🌐 3. การจัดการ Proxy Sessions

### วิเคราะห์ประสิทธิภาพ Proxy
```sql
-- Proxy ที่มีประสิทธิภาพสูงสุด
SELECT session_id, proxy_type, country, success_rate, requests_made,
       (requests_made * success_rate / 100) as successful_requests
FROM proxy_sessions
WHERE status = 'active'
ORDER BY success_rate DESC;

-- การใช้งาน Proxy ตาม Country
SELECT country, 
       COUNT(*) as proxy_count,
       AVG(success_rate) as avg_success,
       SUM(requests_made) as total_requests,
       AVG(data_transferred) as avg_data_mb
FROM proxy_sessions
GROUP BY country
ORDER BY avg_success DESC;

-- Proxy ที่ใกล้หมดอายุ
SELECT session_id, proxy_type, country, expires_at,
       (julianday(expires_at) - julianday('now')) as days_left
FROM proxy_sessions
WHERE expires_at IS NOT NULL AND days_left < 7
ORDER BY days_left ASC;
```

---

## 📋 4. การวิเคราะห์ Operation Logs

### ติดตาม Operations และ Errors
```sql
-- Log ล่าสุดของแต่ละ operation type
SELECT operation_type, log_level, message, timestamp
FROM operation_logs o1
WHERE timestamp = (
    SELECT MAX(timestamp) 
    FROM operation_logs o2 
    WHERE o2.operation_type = o1.operation_type
)
ORDER BY timestamp DESC;

-- นับ Error/Warning ในแต่ละ operation
SELECT operation_type, log_level, COUNT(*) as count
FROM operation_logs
WHERE log_level IN ('ERROR', 'WARNING', 'CRITICAL')
GROUP BY operation_type, log_level
ORDER BY count DESC;

-- Operations ที่ใช้ Proxy มากที่สุด
SELECT o.session_id, p.proxy_type, p.country, COUNT(*) as operations,
       AVG(CASE WHEN o.log_level = 'ERROR' THEN 1 ELSE 0 END) as error_rate
FROM operation_logs o
JOIN proxy_sessions p ON o.session_id = p.session_id
WHERE o.session_id IS NOT NULL
GROUP BY o.session_id
ORDER BY operations DESC;
```

---

## 🔒 5. การวิเคราะห์ Security & Vulnerabilities

### หา Vulnerabilities ที่ Critical
```sql
-- Vulnerabilities ตาม Severity
SELECT t.target_name, s.vulnerability, s.severity, s.cve_id, s.exploit_available
FROM scan_results s
JOIN targets t ON s.target_id = t.id
WHERE s.vulnerability IS NOT NULL
ORDER BY 
    CASE s.severity 
        WHEN 'critical' THEN 1 
        WHEN 'high' THEN 2 
        WHEN 'medium' THEN 3 
        WHEN 'low' THEN 4 
    END;

-- Ports ที่เปิดบ่อยที่สุด
SELECT port, service, COUNT(*) as found_count,
       GROUP_CONCAT(DISTINCT t.target_name) as found_on_targets
FROM scan_results s
JOIN targets t ON s.target_id = t.id
WHERE port IS NOT NULL
GROUP BY port, service
ORDER BY found_count DESC;

-- CVE ที่มี Exploit Available
SELECT t.target_name, s.port, s.service, s.vulnerability, s.cve_id
FROM scan_results s
JOIN targets t ON s.target_id = t.id
WHERE s.exploit_available = 1
ORDER BY t.target_name;
```

---

## 📊 6. รายงานแบบรวม (Dashboard Queries)

### สร้าง Security Dashboard
```sql
-- Security Overview
SELECT 
    'Total Targets' as metric, COUNT(*) as value FROM targets
UNION ALL
SELECT 
    'High Risk Targets', COUNT(*) FROM extracted_data WHERE risk_score >= 60
UNION ALL
SELECT 
    'Active Proxies', COUNT(*) FROM proxy_sessions WHERE status = 'active'
UNION ALL
SELECT 
    'Critical Vulnerabilities', COUNT(*) FROM scan_results WHERE severity = 'critical'
UNION ALL
SELECT 
    'Recent Errors', COUNT(*) FROM operation_logs 
    WHERE log_level IN ('ERROR', 'CRITICAL') AND date(timestamp) = date('now');

-- Target Status Summary
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM targets), 2) as percentage
FROM targets
GROUP BY status
ORDER BY count DESC;

-- Risk Assessment Summary
SELECT 
    CASE 
        WHEN risk_score >= 80 THEN 'Critical Risk'
        WHEN risk_score >= 60 THEN 'High Risk'
        WHEN risk_score >= 40 THEN 'Medium Risk'
        WHEN risk_score >= 20 THEN 'Low Risk'
        ELSE 'Minimal Risk'
    END as risk_category,
    COUNT(*) as count,
    AVG(risk_score) as avg_score
FROM extracted_data
GROUP BY risk_category
ORDER BY avg_score DESC;
```

---

## 🔧 7. การ Update และ Maintenance

### Update Status และ Priority
```sql
-- อัพเดท Priority ของ targets ที่มี risk สูง
UPDATE targets 
SET priority = 4, notes = 'High risk detected'
WHERE id IN (
    SELECT DISTINCT t.id 
    FROM targets t 
    JOIN extracted_data e ON t.id = e.target_id 
    WHERE e.risk_score >= 70
);

-- Mark targets as completed หลังจากสแกนแล้ว
UPDATE targets 
SET status = 'completed', last_scanned = datetime('now')
WHERE id IN (SELECT DISTINCT target_id FROM extracted_data);

-- เคลียร์ proxy sessions ที่หมดอายุ
UPDATE proxy_sessions 
SET status = 'expired' 
WHERE expires_at < datetime('now') AND status != 'expired';
```

---

## 🎯 8. Advanced Analytics Queries

### Performance Analysis
```sql
-- Proxy Performance vs Target Success
SELECT 
    p.proxy_type,
    p.country,
    AVG(p.success_rate) as avg_proxy_success,
    COUNT(DISTINCT o.target_id) as targets_scanned,
    AVG(e.risk_score) as avg_risk_found
FROM proxy_sessions p
LEFT JOIN operation_logs o ON p.session_id = o.session_id
LEFT JOIN extracted_data e ON o.target_id = e.target_id
WHERE p.status = 'active'
GROUP BY p.proxy_type, p.country
ORDER BY avg_proxy_success DESC;

-- Time-based Analysis
SELECT 
    date(timestamp) as scan_date,
    COUNT(DISTINCT target_id) as targets_scanned,
    COUNT(*) as total_operations,
    SUM(CASE WHEN log_level = 'ERROR' THEN 1 ELSE 0 END) as errors
FROM operation_logs
GROUP BY date(timestamp)
ORDER BY scan_date DESC;
```

---

## 💡 การใช้งานจริง

1. **Copy query ที่ต้องการ**
2. **รันผ่าน SQL interface**: `python3 sql_query_interface.py`
3. **เลือก "c" สำหรับ Custom Query**
4. **Paste และรัน**

**ตัวอย่างการใช้**:
```bash
python3 sql_query_interface.py
# เลือก 'c' แล้ว paste query ข้างบน
```
