import sqlite3
import os

def connect_db():
    db_path = 'database/sas.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL,
        student_id TEXT,
        standard TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Classes (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        date TEXT,
        time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        class_id INTEGER,
        status TEXT,
        reason TEXT,
        FOREIGN KEY(class_id) REFERENCES Classes(class_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
