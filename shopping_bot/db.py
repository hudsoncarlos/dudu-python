import sqlite3

DB_NAME = "shopping.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_item(item):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO shopping_list (item) VALUES (?)", (item,))
        conn.commit()

def get_items():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT id, item, done FROM shopping_list").fetchall()

def mark_done(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE shopping_list SET done = 1 WHERE id = ?", (item_id,))
        conn.commit()

def delete_item(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM shopping_list WHERE id = ?", (item_id,))
        conn.commit()
