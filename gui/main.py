import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from models.db import create_tables
from services.auth import register_user, login_user
from services.attendance import mark_attendance, get_attendance_report, update_attendance, delete_attendance
from services.qr import generate_qr, scan_qr
import os

create_tables()

root = tk.Tk()
root.title("Student Attendance System")
root.geometry("500x500")

# === QR Attendance ===


def qr_attendance(class_id):
    try:
        sid = scan_qr()  # Always open the webcam
        if sid:
            mark_attendance(sid, class_id, "present")
            messagebox.showinfo(
                "QR Success", f"Attendance marked for student ID {sid}")
        else:
            messagebox.showerror("QR Failed", "No QR code detected.")
    except Exception as e:
        messagebox.showerror("Error", f"QR Scan failed: {str(e)}")

# === Registration Window ===


def show_register_screen():
    def submit():
        user_type = user_type_var.get()
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        student_id = student_id_entry.get()
        standard = standard_entry.get()

        if user_type == "student" and (not student_id or not standard):
            messagebox.showerror(
                "Error", "Student ID and Standard are required for student registration.")
            return

        user_id = register_user(name, email, password,
                                user_type, student_id, standard)
        if user_id:
            if user_type == "student":
                generate_qr(student_id)
                messagebox.showinfo(
                    "Success", f"Student Registered.\nQR Code saved in qr_codes/")
            else:
                messagebox.showinfo("Success", "Teacher Registered.")
            register_win.destroy()
        else:
            messagebox.showerror("Error", "Registration failed")

    register_win = tk.Toplevel(root)
    register_win.title("Register")
    register_win.geometry("400x500")

    user_type_var = tk.StringVar(value="student")
    tk.Label(register_win, text="User Type").pack()
    tk.OptionMenu(register_win, user_type_var, "student", "teacher").pack()

    tk.Label(register_win, text="Name").pack()
    name_entry = tk.Entry(register_win)
    name_entry.pack()

    tk.Label(register_win, text="Email").pack()
    email_entry = tk.Entry(register_win)
    email_entry.pack()

    tk.Label(register_win, text="Password").pack()
    password_entry = tk.Entry(register_win, show="*")
    password_entry.pack()

    tk.Label(register_win, text="Student ID (for students)").pack()
    student_id_entry = tk.Entry(register_win)
    student_id_entry.pack()

    tk.Label(register_win, text="Standard/Class (for students)").pack()
    standard_entry = tk.Entry(register_win)
    standard_entry.pack()

    tk.Button(register_win, text="Register", command=submit).pack(pady=10)

# === Login Window ===


def show_login_screen():
    def submit():
        user = login_user(email_entry.get(), password_entry.get())
        if user:
            messagebox.showinfo("Welcome", f"Logged in as {user['name']}")
            login_win.destroy()
            if user['user_type'] == 'teacher':
                show_teacher_dashboard(user)
            else:
                show_student_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.geometry("400x300")

    tk.Label(login_win, text="Email").pack()
    email_entry = tk.Entry(login_win)
    email_entry.pack()

    tk.Label(login_win, text="Password").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    tk.Button(login_win, text="Login", command=submit).pack(pady=10)

# === Student Dashboard ===


def show_student_dashboard(user):
    dashboard = tk.Toplevel(root)
    dashboard.title("Student Dashboard")
    dashboard.geometry("500x500")

    def view_qr():
        qr_path = f"qr_codes/student_{user['student_id']}.png"
        if os.path.exists(qr_path):
            qr_win = tk.Toplevel(dashboard)
            qr_win.title("Your QR Code")
            qr_win.geometry("300x300")
            img = Image.open(qr_path).resize((250, 250))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(qr_win, image=photo)
            label.image = photo
            label.pack()
        else:
            messagebox.showerror("Error", "QR code not found.")

    def view_attendance():
        records = get_attendance_report(student_id=user['student_id'])
        report_win = tk.Toplevel(dashboard)
        report_win.title("Your Attendance Records")
        report_win.geometry("600x300")

        tree = ttk.Treeview(report_win, columns=(
            "Course", "Date", "Time", "Status", "Reason"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        for row in records:
            # skipping attendance_id and name
            tree.insert("", tk.END, values=row[2:])

    def manual_attendance():
        manual_win = tk.Toplevel(dashboard)
        manual_win.title("Manual Attendance")
        manual_win.geometry("300x300")

        tk.Label(manual_win, text="Class ID").pack()
        class_id_entry = tk.Entry(manual_win)
        class_id_entry.pack()

        tk.Label(manual_win, text="Status").pack()
        status_entry = tk.Entry(manual_win)
        status_entry.insert(0, "present")
        status_entry.pack()

        tk.Label(manual_win, text="Reason (optional)").pack()
        reason_entry = tk.Entry(manual_win)
        reason_entry.pack()

        def submit():
            mark_attendance(user['student_id'], class_id_entry.get(
            ), status_entry.get(), reason_entry.get())
            messagebox.showinfo("Success", "Manual attendance marked.")
            manual_win.destroy()

        tk.Button(manual_win, text="Submit", command=submit).pack()

    def scan_attendance():
        # pass class/standard as class_id or actual class ID
        qr_attendance(class_id=user['standard'])

    tk.Button(dashboard, text="View QR Code", command=view_qr).pack(pady=10)
    tk.Button(dashboard, text="Manual Attendance",
              command=manual_attendance).pack(pady=10)
    tk.Button(dashboard, text="QR Code Attendance",
              command=scan_attendance).pack(pady=10)
    tk.Button(dashboard, text="View Attendance Records",
              command=view_attendance).pack(pady=10)

# === Teacher Dashboard ===


def show_teacher_dashboard(user):
    dashboard = tk.Toplevel(root)
    dashboard.title("Teacher Dashboard")
    dashboard.geometry("600x500")

    def view_attendance():
        report_win = tk.Toplevel(dashboard)
        report_win.title("All Attendance Records")
        report_win.geometry("800x400")

        tree = ttk.Treeview(report_win, columns=(
            "ID", "Student", "Course", "Date", "Time", "Status", "Reason"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        records = get_attendance_report()
        for row in records:
            tree.insert("", tk.END, values=row)

        def edit_record():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "No record selected.")
                return

            values = tree.item(selected[0])["values"]
            edit_win = tk.Toplevel(report_win)
            edit_win.title("Edit Record")
            edit_win.geometry("300x200")

            tk.Label(edit_win, text="Status").pack()
            status = tk.Entry(edit_win)
            status.insert(0, values[5])
            status.pack()

            tk.Label(edit_win, text="Reason").pack()
            reason = tk.Entry(edit_win)
            reason.insert(0, values[6])
            reason.pack()

            def save():
                update_attendance(values[0], status.get(), reason.get())
                messagebox.showinfo("Updated", "Record updated")
                edit_win.destroy()
                report_win.destroy()
                view_attendance()

            tk.Button(edit_win, text="Save", command=save).pack()

        def delete_record():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "No record selected.")
                return
            attendance_id = tree.item(selected[0])["values"][0]
            delete_attendance(attendance_id)
            messagebox.showinfo("Deleted", "Record deleted.")
            report_win.destroy()
            view_attendance()

        tk.Button(report_win, text="Edit Selected",
                  command=edit_record).pack(pady=5)
        tk.Button(report_win, text="Delete Selected",
                  command=delete_record).pack(pady=5)

    def add_attendance():
        add_win = tk.Toplevel(dashboard)
        add_win.title("Add Attendance")
        add_win.geometry("300x300")

        tk.Label(add_win, text="Student ID").pack()
        sid = tk.Entry(add_win)
        sid.pack()

        tk.Label(add_win, text="Class ID").pack()
        cid = tk.Entry(add_win)
        cid.pack()

        tk.Label(add_win, text="Status").pack()
        status = tk.Entry(add_win)
        status.pack()

        tk.Label(add_win, text="Reason").pack()
        reason = tk.Entry(add_win)
        reason.pack()

        def submit():
            mark_attendance(sid.get(), cid.get(), status.get(), reason.get())
            messagebox.showinfo("Success", "Attendance added.")
            add_win.destroy()

        tk.Button(add_win, text="Submit", command=submit).pack()

    tk.Button(dashboard, text="View Attendance Records",
              command=view_attendance).pack(pady=10)
    tk.Button(dashboard, text="Add Attendance",
              command=add_attendance).pack(pady=10)


# === Entry Buttons ===
tk.Button(root, text="Register", command=show_register_screen).pack(pady=20)
tk.Button(root, text="Login", command=show_login_screen).pack(pady=10)

root.mainloop()
