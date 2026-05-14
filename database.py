import sqlite3

def create_database():
    conn = sqlite3.connect("fitness_chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        goal TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_user(name, age, weight, height, goal):
    conn = sqlite3.connect("fitness_chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (name, age, weight, height, goal)
    VALUES (?, ?, ?, ?, ?)
    """, (name, age, weight, height, goal))

    conn.commit()
    conn.close()