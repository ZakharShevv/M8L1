import sqlite3

DB_NAME = "eco_challenges.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS completed_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            points INTEGER
        )
    """)

    conn.commit()
    conn.close()

def mark_completed(challenge_name, points=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO completed_challenges (name, points) VALUES (?, ?)", (challenge_name, points))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def get_completed():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name FROM completed_challenges")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_total_points():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SUM(points) FROM completed_challenges")
    result = c.fetchone()[0]
    conn.close()
    return result if result else 0
