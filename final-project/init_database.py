import sqlite3

conn = sqlite3.connect("door_log.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS door_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    event TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized with session support")