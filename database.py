
import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, wallet INTEGER DEFAULT 0, verified INTEGER DEFAULT 0)")
cursor.execute("CREATE TABLE IF NOT EXISTS ip_logs (ip TEXT UNIQUE, user_id INTEGER)")
conn.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def mark_verified(user_id):
    cursor.execute("UPDATE users SET verified=1, wallet=wallet+1 WHERE user_id=?", (user_id,))
    conn.commit()

def is_verified(user_id):
    cursor.execute("SELECT verified FROM users WHERE user_id=?", (user_id,))
    r = cursor.fetchone()
    return r and r[0] == 1

def get_wallet(user_id):
    cursor.execute("SELECT wallet FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0]

def ip_exists(ip):
    cursor.execute("SELECT ip FROM ip_logs WHERE ip=?", (ip,))
    return cursor.fetchone()

def save_ip(ip, user_id):
    cursor.execute("INSERT INTO ip_logs (ip, user_id) VALUES (?, ?)", (ip, user_id))
    conn.commit()
