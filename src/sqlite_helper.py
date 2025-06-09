# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import sqlite3
from typing import Any, List, Tuple

DB_PATH = 'data/project_operations.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        # Table for targets
        c.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                full_name TEXT,
                profile_pic_url TEXT,
                bio TEXT,
                is_private INTEGER,
                is_verified INTEGER
            )
        ''')
        # Table for DMs
        c.execute('''
            CREATE TABLE IF NOT EXISTS dms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                sender TEXT,
                message TEXT,
                timestamp TEXT,
                FOREIGN KEY(target_id) REFERENCES targets(id)
            )
        ''')
        # Table for personal data
        c.execute('''
            CREATE TABLE IF NOT EXISTS personal_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER,
                key TEXT,
                value TEXT,
                FOREIGN KEY(target_id) REFERENCES targets(id)
            )
        ''')
        conn.commit()

def add_target(username: str, full_name: str, profile_pic_url: str, bio: str, is_private: bool, is_verified: bool):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT OR IGNORE INTO targets (username, full_name, profile_pic_url, bio, is_private, is_verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, full_name, profile_pic_url, bio, int(is_private), int(is_verified)))
        conn.commit()
        return c.lastrowid

def add_dm(target_id: int, sender: str, message: str, timestamp: str):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO dms (target_id, sender, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (target_id, sender, message, timestamp))
        conn.commit()
        return c.lastrowid

def add_personal_data(target_id: int, key: str, value: str):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO personal_data (target_id, key, value)
            VALUES (?, ?, ?)
        ''', (target_id, key, value))
        conn.commit()
        return c.lastrowid

def get_target_by_username(username: str) -> Any:
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM targets WHERE username = ?', (username,))
        return c.fetchone()

def get_dms_for_target(target_id: int) -> List[Tuple]:
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM dms WHERE target_id = ?', (target_id,))
        return c.fetchall()

def get_personal_data_for_target(target_id: int) -> List[Tuple]:
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT key, value FROM personal_data WHERE target_id = ?', (target_id,))
        return c.fetchall()

if __name__ == '__main__':
    init_db()
    print('Database initialized.')
