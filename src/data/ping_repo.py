from sqlite3 import Row
from datetime import datetime
from src.data.db import get_connection

# Create a ping
def create_ping(sender_user_id: int, receiver_user_id: int, ping_type: str, message: str | None, cost: int) -> None:
    """
    Docstring for create_ping
    
    :param sender_user_id: Description
    :type sender_user_id: int
    :param receiver_user_id: Description
    :type receiver_user_id: int
    :param ping_type: Description
    :type ping_type: str
    :param message: Description
    :type message: str | None
    :param cost: Description
    :type cost: int
    """
    created_at = datetime.utcnow().isoformat() # Record when the ping was created using the appropriate format
    with get_connection() as conn: # Connect to the database to perform the action
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO pings (sender_user_id, receiver_user_id, ping_type, message, cost, created_at) VALUES (?, ?, ?, ?, ?, ?)", (sender_user_id, receiver_user_id, ping_type, message, cost, created_at))
        conn.commit() # After the SQL is done, commit the changes to the database

# Retrieve ping info for users
def get_pings_for_user(user_id: int, limit: int = 20) -> list[Row]:
    """
    Docstring for get_pings_for_user
    
    :param user_id: Description
    :type user_id: int
    :param limit: Description
    :type limit: int
    :return: Description
    :rtype: list[Row]
    """
    with get_connection() as conn: # Connect to the database
        cur = conn.cursor()
        cur.execute("SELECT * FROM pings WHERE sender_user_id = ? OR receiver_user_id = ? ORDER BY id DESC LIMIT ?", (user_id, user_id, limit))
        rows = cur.fetchall()
        return rows # Return the records of the user's pings

# Delete a ping
def delete_ping(user_id: int, ping_id: int) -> bool:
    """
    Docstring for delete_ping
    
    :param user_id: Description
    :type user_id: int
    :param ping_id: Description
    :type ping_id: int
    :return: Description
    :rtype: bool
    """

    with get_connection() as conn: # CONNECT to database
        cur = conn.cursor() 
        cur.execute("DELETE FROM pings WHERE id = ? AND sender_user_id = ?", (ping_id, user_id)) # Delete the ping from the database
        conn.commit()
        if cur.rowcount == 1:
            return True # If one ping was deleted, return true
        else:
            return False # Otherwise return false or failure     
