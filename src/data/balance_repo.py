from sqlite3 import Row
from src.data.db import get_connection

# Setting the initial balance if missing
def init_balance_if_missing(user_id: int, daily_tokens: int, today: str) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO token_balances (user_id, balance, last_refresh) VALUES (?, ?, ?)", (user_id, daily_tokens, today))
        conn.commit()

# Retrieving the token balance
def get_balance(user_id: int) -> Row | None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM token_balances WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row

# Updates balance    
def upsert_balance(user_id: int, balance: int, last_refresh: str) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO token_balances (user_id, balance, last_refresh) VALUES (?, ?, ?)",
            (user_id, balance, last_refresh),
        )
        conn.commit()
