# 📚 Student Attendance System

A desktop-based Student Attendance System developed in Python using Tkinter, OpenCV, and SQLite. This system supports **QR Code-based attendance**, **manual attendance**, and **role-based access** for **students** and **teachers**. It follows a normalized database schema aligning with good design principles.

---

## ✨ Features

### 🔒 User Roles
- **Student**: Register, scan QR to mark attendance, and view their attendance records.
- **Teacher**: View, update, delete, and manually add attendance records.

### 🧠 Functionalities
- QR Code is generated during **student registration**.
- Students use their **webcam (OpenCV)** to scan QR codes.
- Teachers can fully manage attendance records.
- Local **SQLite** database is used to store all information.

---

## 🛠️ Installation

### ✅ Prerequisites
- Python 3.8+
- `pip` package manager

### 📦 Clone the Repository

```bash
git clone git@github.com:mdsajjadhossain25/Sas.git
cd Sas
```

### 📜 Install Dependencies
Install the required Python packages using:
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python -m gui.main
```


## 🗄️ Database Schema Overview

We have used an SQLite database located at `database/sas.db`. The database includes three primary tables: `Users`, `Classes`, and `Attendance`.

---

### 📋 Table: `Users`

Stores user credentials and role details.

| Column      | Type     | Description                         |
|-------------|----------|-------------------------------------|
| user_id     | INTEGER  | Primary Key, auto-incremented       |
| name        | TEXT     | Full name of the user               |
| email       | TEXT     | Unique email identifier             |
| password    | TEXT     | Password (should be hashed in production) |
| user_type   | TEXT     | 'student' or 'teacher'              |
| student_id  | TEXT     | Unique student ID (nullable for teachers) |
| standard    | TEXT     | Class/grade (nullable for teachers) |

---

### 📚 Table: `Classes`

Stores details about class sessions.

| Column   | Type     | Description                         |
|----------|----------|-------------------------------------|
| class_id | INTEGER  | Primary Key, auto-incremented       |
| course   | TEXT     | Name or code of the course          |
| date     | TEXT     | Date of the class (format: YYYY-MM-DD) |
| time     | TEXT     | Time of the class (format: HH:MM)   |

---

### 📆 Table: `Attendance`

Tracks student attendance records.

| Column        | Type     | Description                               |
|---------------|----------|-------------------------------------------|
| attendance_id | INTEGER  | Primary Key, auto-incremented             |
| student_id    | TEXT     | Foreign Key reference to `Users.student_id` |
| class_id      | INTEGER  | Foreign Key reference to `Classes.class_id` |
| status        | TEXT     | 'present', 'absent', or other status      |
| reason        | TEXT     | Reason for absence (optional)             |

---

### 🔗 Relationships

- `Attendance.class_id` → references `Classes.class_id`
- `Attendance.student_id` → references `Users.student_id` 

---

