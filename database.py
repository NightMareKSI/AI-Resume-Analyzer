import sqlite3

def create_database():

    conn = sqlite3.connect("resume_analyzer.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            resume_name TEXT,
            semantic_score REAL,
            skill_score REAL,
            overall_score REAL
        )
    """)

    conn.commit()

    conn.close()

def register_user(username, password):

    conn = sqlite3.connect("resume_analyzer.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()

    conn.close()


def login_user(username, password):

    conn = sqlite3.connect("resume_analyzer.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user

def save_history(
    username,
    resume_name,
    semantic_score,
    skill_score,
    overall_score
):

    conn = sqlite3.connect("resume_analyzer.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (
            username,
            resume_name,
            semantic_score,
            skill_score,
            overall_score
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        resume_name,
        semantic_score,
        skill_score,
        overall_score
    ))

    conn.commit()

    conn.close()

def get_history(username):

    conn = sqlite3.connect("resume_analyzer.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history WHERE username=?",
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return data

