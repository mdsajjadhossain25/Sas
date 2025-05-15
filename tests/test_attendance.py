import unittest
from services.auth import register_user, login_user
from services.attendance import mark_attendance, get_attendance_report

class TestAttendanceSystem(unittest.TestCase):
    def test_register_and_login(self):
        user_id = register_user("Demo Student", "demo@student.com", "pass123", "student", "STU123", "10")
        self.assertIsNotNone(user_id)
        user = login_user("demo@student.com", "pass123")
        self.assertIsNotNone(user)
        self.assertEqual(user['user_type'], "student")

    def test_mark_attendance(self):
        user = login_user("demo@student.com", "pass123")
        self.assertIsNotNone(user)
        mark_attendance(user['student_id'], 1, "present", "On time")
        report = get_attendance_report(user['student_id'])
        self.assertTrue(len(report) > 0)

if __name__ == "__main__":
    unittest.main()
