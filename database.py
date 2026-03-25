import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()  

def add_transaction(date, category, amount, trans_type):
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    
    query = "INSERT INTO transactions (date, category, amount, type) VALUES (?, ?, ?, ?)"
    
    cursor.execute(query, (date, category, amount, trans_type))
    
    # 4. Commit (Save) and close
    conn.commit()
    conn.close()

def fetch_all_transactions():
    conn = sqlite3.connect('budget.db')
    # Using Pandas makes it easy to create charts in Streamlit
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

# 4. Trigger Execution (The part that actually creates the file)
if __name__ == "__main__":
    init_db()
    print("Database and Table initialized successfully!")          