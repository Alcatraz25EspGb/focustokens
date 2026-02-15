from datetime import date
from src.data.db import get_connection

# Inserts a user tuple into the database users table
def create_user(username: str) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
        conn.commit()

# Returns user id if such exists
def get_user_id(username: str) -> int | None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row == None:
            return None
        else:
            print(row["id"]) # Debugging statement
            return row["id"]