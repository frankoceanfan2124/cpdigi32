"""
database.py
------------
Handles all SQLite database logic for the Contact Us feature.

Kept separate from app.py so the routing code (app.py) stays clean and
the database logic is easy to document/explain on its own for the
assessment (e.g. in your Buildstage doc).
"""

import sqlite3

DATABASE_NAME = "contacts.db"


def get_db_connection():
    """
    Opens a new connection to the SQLite database file.
    row_factory lets me access columns by name (e.g. row['email'])
    instead of only by index (e.g. row[0]), which makes the code
    in app.py much easier to read.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Creates the 'messages' table if it doesn't already exist.
    Safe to call every time the app starts up.
    """
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
 