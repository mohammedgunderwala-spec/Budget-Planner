import sqlite3

def init_db():
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    # 1. Create Users Table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)""")
    
    # 2. Update Transactions Table to include user_id
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
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False # Username already exists
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def fetch_user_transactions(user_id):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    # Logic: Only fetch data where user_id matches the logged-in person
    c.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    data = c.fetchall()
    conn.close()
    return data

def add_transaction(user_id, date, category, amount, t_type):
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    # Logic: Notice we are now including 'user_id' so the entry stays private!
    c.execute("""INSERT INTO transactions (user_id, date, category, amount, type) 
                 VALUES (?, ?, ?, ?, ?)""", (user_id, date, category, amount, t_type))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized and budget.db created!")