from sqlite3 import Row
from datetime import datetime
from src.data.db import get_connection

# Creates a ping
def create_ping(sender_user_id: int, receiver_user_id: int, ping_type: str, message: str | None, cost: int) -> None:
    created_at = datetime.utcnow().isoformat() # Record when the ping was created using the appropriate format
    with get_connection() as conn: # Connect to the database to perform the action
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO pings (sender_user_id, receiver_user_id, ping_type, message, cost, created_at) VALUES (?, ?, ?, ?, ?, ?)", (sender_user_id, receiver_user_id, ping_type, message, cost, created_at))
        conn.commit() # After the SQL is done, commit the changes to the database

# Retrieve ping info for users
def get_pings_for_user(user_id: int, limit: int = 20) -> list[Row]:
    with get_connection() as conn: # Connect to the database
        cur = conn.cursor()
        cur.execute("SELECT * FROM pings WHERE sender_user_id = ? OR receiver_user_id = ? ORDER BY id DESC LIMIT ?", (user_id, user_id, limit))
        rows = cur.fetchall()
        return rows # Return the records of the user's pings