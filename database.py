import sqlite3
import hashlib

# Helper function to scramble passwords (Hashing)
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def init_db():
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    type TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id))""")
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    hashed_pw = hash_password(password) # Security step
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except:
        return False 
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    hashed_pw = hash_password(password) # Check against scrambled version
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def add_transaction(user_id, date, category, amount, t_type):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("""INSERT INTO transactions (user_id, date, category, amount, type) 
                 VALUES (?, ?, ?, ?, ?)""", (user_id, date, category, amount, t_type))
    conn.commit()
    conn.close()

def fetch_user_transactions(user_id):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    data = c.fetchall()
    conn.close()
    return data

if __name__ == "__main__":
    init_db()