import tkinter as tk
from tkinter import ttk
import sqlite3

from database import DB_PATH
from AttendanceDashboard import attendance_dashboard


# ===== LOAD DATA =====
def load_data():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM attendance")
    rows = c.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    conn.close()


# ===== ANALYZE ATTENDANCE =====
def analyze():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT AVG(attendance_percentage) FROM attendance")
    avg = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM attendance WHERE attendance_percentage < 75")
    defaulters = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM attendance")
    total = c.fetchone()[0]

    conn.close()

    lbl_avg.config(text=f"Average Attendance : {round(avg,2) if avg else 0}%")
    lbl_def.config(text=f"Defaulters (<75%) : {defaulters}")
    lbl_total.config(text=f"Total Records : {total}")


# ===== MAIN SCREEN =====
def attendance_screen():

    global tree, lbl_avg, lbl_def, lbl_total

    top = tk.Tk()
    top.title("Attendance Monitoring")

    # Fullscreen
    top.attributes('-fullscreen', True)
    top.bind("<Escape>", lambda e: top.attributes('-fullscreen', False))

    # ===== TITLE =====
    ttk.Label(
        top,
        text="Attendance Monitoring & Analysis",
        font=("Helvetica", 22, "bold")
    ).pack(pady=10)

    # ===== SUMMARY =====
    summary_frame = ttk.Frame(top, padding=10)
    summary_frame.pack()

    lbl_avg = ttk.Label(summary_frame, text="Average Attendance : 0%", font=("Arial", 14))
    lbl_avg.grid(row=0, column=0, padx=20)

    lbl_def = ttk.Label(summary_frame, text="Defaulters (<75%) : 0", font=("Arial", 14))
    lbl_def.grid(row=0, column=1, padx=20)

    lbl_total = ttk.Label(summary_frame, text="Total Records : 0", font=("Arial", 14))
    lbl_total.grid(row=0, column=2, padx=20)

    # ===== BUTTONS =====
    btn_frame = ttk.Frame(top)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Analyze", command=analyze).grid(row=0, column=0, padx=10)

    ttk.Button(
        btn_frame,
        text="Attendance Dashboard",
        command=lambda: attendance_dashboard(top)
    ).grid(row=0, column=1, padx=10)

    ttk.Button(btn_frame, text="Refresh", command=load_data).grid(row=0, column=2, padx=10)

    ttk.Button(btn_frame, text="Back", command=top.destroy).grid(row=0, column=3, padx=10)

    # ===== TABLE =====
    tree = ttk.Treeview(
        top,
        columns=(
            "id", "student_id", "course_id", "semester",
            "total_classes", "attended", "percentage",
            "late", "medical", "unauthorized",
            "status", "updated", "trend", "flag"
        ),
        show="headings"
    )

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True)

    load_data()
    top.mainloop()