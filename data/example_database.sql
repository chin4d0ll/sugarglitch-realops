
-- ตัวอย่าง SQLite Database
-- สามารถใช้กับ SQLite extension

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ข้อมูลตัวอย่าง
INSERT OR REPLACE INTO users (id, name, email) VALUES 
(1, 'สมชาย ใจดี', 'somchai@example.com'),
(2, 'สมหญิง รักดี', 'somying@example.com'),
(3, 'ประยุทธ์ ทำงาน', 'prayuth@example.com');

INSERT OR REPLACE INTO products (id, name, price, category) VALUES
(1, 'โน๊ตบุ๊ค', 25000.00, 'Electronics'),
(2, 'เมาส์', 500.00, 'Computer'),
(3, 'คีย์บอร์ด', 1500.00, 'Computer');
