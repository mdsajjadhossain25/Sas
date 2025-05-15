from models.db import connect_db

def mark_attendance(student_id, class_id, status, reason=""):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Attendance (student_id, class_id, status, reason)
    VALUES (?, ?, ?, ?)
    """, (student_id, class_id, status, reason))
    conn.commit()
    conn.close()

def get_attendance_report(student_id=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT a.attendance_id, u.name, c.course, c.date, c.time, a.status, a.reason
    FROM Attendance a
    JOIN Users u ON u.student_id = a.student_id
    LEFT JOIN Classes c ON c.class_id = a.class_id
    """

    if student_id:
        query += " WHERE a.student_id = ?"
        cursor.execute(query, (student_id,))
    else:
        cursor.execute(query)

    records = cursor.fetchall()
    conn.close()
    return records

def update_attendance(attendance_id, status, reason):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE Attendance SET status = ?, reason = ? WHERE attendance_id = ?
    """, (status, reason, attendance_id))
    conn.commit()
    conn.close()

def delete_attendance(attendance_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Attendance WHERE attendance_id = ?", (attendance_id,))
    conn.commit()
    conn.close()
