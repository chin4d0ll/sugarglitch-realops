import sqlite3


def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        asset TEXT NOT NULL,
        amount REAL NOT NULL,
        trade_type TEXT NOT NULL CHECK(trade_type IN ('buy', 'sell')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS session_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_id TEXT NOT NULL UNIQUE,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logout_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()


def insert_user(username, email):
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, email) VALUES (?, ?)',
            (username, email)
        )
        conn.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")
    finally:
        conn.close()


def insert_trade(user_id, asset, amount, trade_type):
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute(
            (
                'INSERT INTO trades (user_id, asset, amount, trade_type) '
                'VALUES (?, ?, ?, ?)'
            ),
            (user_id, asset, amount, trade_type)
        )
        conn.commit()
        print(f"Trade for user_id {user_id} added successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting trade: {e}")
    finally:
        conn.close()


def insert_session_log(user_id, session_id, login_time=None, logout_time=None):
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()
    try:
        cursor.execute(
            (
                'INSERT INTO session_logs (user_id, session_id, '
                'login_time, logout_time) VALUES (?, ?, ?, ?)'
            ),
            (user_id, session_id, login_time, logout_time)
        )
        conn.commit()
        print(f"Session log for user_id {user_id} added successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting session log: {e}")
    finally:
        conn.close()


def get_all_users():
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


def get_user_by_username(username):
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


if __name__ == '__main__':
    create_database()
    print("Database and tables created successfully.")
    print("All users in the database:")
    users = get_all_users()
    for user in users:
        print(user)
    # ตัวอย่างการเพิ่มผู้ใช้จริง
    insert_user('alx.trading', 'alx.trading@example.com')
    insert_user('whatilove1728', 'whatilove1728@example.com')
    print("All users in the database after insert:")
    users = get_all_users()
    for user in users:
        print(user)

    print("\n--- USERS ---")
    users = get_all_users()
    for user in users:
        print(user)

    print("\n--- TRADES ---")
    conn = sqlite3.connect('alx_trading_database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trades')
    trades = cursor.fetchall()
    for trade in trades:
        print(trade)

    print("\n--- SESSION LOGS ---")
    cursor.execute('SELECT * FROM session_logs')
    session_logs = cursor.fetchall()
    for log in session_logs:
        print(log)
    conn.close()
