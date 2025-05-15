import hashlib
from models.db import connect_db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password, user_type, student_id=None, standard=None):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO Users (name, email, password, user_type, student_id, standard)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, hash_password(password), user_type, student_id, standard))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Registration error:", e)
        return None
    finally:
        conn.close()

def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM Users WHERE email = ? AND password = ?
    """, (email, hash_password(password)))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "user_id": result[0],
            "name": result[1],
            "email": result[2],
            "user_type": result[4],
            "student_id": result[5],
            "standard": result[6]
        }
    return None
