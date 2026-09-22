import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH
from DataCollectionDashboard import data_collection_dashboard


def data_collection_screen():

    top = tk.Toplevel()
    top.title("Data Collection & Integration")
    top.geometry("1100x650")

    ttk.Label(
        top,
        text="Data Collection & Integration",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    tree = ttk.Treeview(top)
    tree.pack(fill="both", expand=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT
        s.student_id,
        s.first_name,
        s.last_name,
        a.attendance_percentage,
        ap.CGPA,
        f.financial_stress_level,
        b.motivation_level,
        b.stress_level
    FROM student s
    LEFT JOIN attendance a ON s.student_id=a.student_id
    LEFT JOIN academic_performance ap ON s.student_id=ap.student_id
    LEFT JOIN financial_status f ON s.student_id=f.student_id
    LEFT JOIN behavioral_record b ON s.student_id=b.student_id
    """)

    columns = [
        "Student ID",
        "First Name",
        "Last Name",
        "Attendance %",
        "CGPA",
        "Financial Stress",
        "Motivation",
        "Behavior Stress"
    ]

    tree["columns"] = columns
    tree["show"] = "headings"

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # -------- TAG COLORS --------
    tree.tag_configure("excellent", background="#b6fcb6")  # green
    tree.tag_configure("good", background="#b6e0fc")       # blue
    tree.tag_configure("average", background="#fff4b6")    # yellow
    tree.tag_configure("poor", background="#fcb6b6")       # red

    for row in c.fetchall():

        try:
            cgpa = float(row[4])
        except:
            cgpa = 0

        # Grade logic
        if cgpa >= 8.5:
            tag = "excellent"
        elif cgpa >= 7:
            tag = "good"
        elif cgpa >= 5:
            tag = "average"
        else:
            tag = "poor"

        tree.insert("", "end", values=row, tags=(tag,))

    conn.close()

    # Buttons
    ttk.Button(top, text="Data Dashboard", command=data_collection_dashboard).pack(pady=5)
    ttk.Button(top, text="Close", command=top.destroy).pack(pady=10)