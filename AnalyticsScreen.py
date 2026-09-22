import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def analytics_screen():

    top = tk.Toplevel()
    top.title("Student Analytics Dashboard")
    top.geometry("1100x700")

    ttk.Label(
        top,
        text="Student Analytics Dashboard",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ================= COURSE DISTRIBUTION =================
    c.execute("""
        SELECT course_id, COUNT(*)
        FROM student
        GROUP BY course_id
    """)
    course_data = c.fetchall()

    courses = [row[0] for row in course_data]
    course_counts = [row[1] for row in course_data]

    # ================= STUDENT STATUS =================
    c.execute("""
        SELECT current_status, COUNT(*)
        FROM student
        GROUP BY current_status
    """)
    status_data = c.fetchall()

    status_labels = [row[0] for row in status_data]
    status_counts = [row[1] for row in status_data]

    # ================= CATEGORY DISTRIBUTION =================
    c.execute("""
        SELECT category, COUNT(*)
        FROM student
        GROUP BY category
    """)
    cat_data = c.fetchall()

    cat_labels = [row[0] for row in cat_data]
    cat_counts = [row[1] for row in cat_data]

    # ================= AGE DISTRIBUTION =================
    c.execute("""
        SELECT age, COUNT(*)
        FROM student
        GROUP BY age
        ORDER BY age
    """)
    age_data = c.fetchall()

    ages = [int(row[0]) for row in age_data if row[0]]
    age_counts = [row[1] for row in age_data if row[0]]

    conn.close()

    # ================= CREATE MATPLOTLIB FIGURE =================
    fig = plt.Figure(figsize=(11,6))

    # -------- COURSE BAR CHART --------
    ax1 = fig.add_subplot(221)
    ax1.bar(courses, course_counts)
    ax1.set_title("Students by Course")
    ax1.set_xlabel("Course")
    ax1.set_ylabel("Number of Students")
    ax1.grid(axis="y")

    # -------- STATUS PIE CHART --------
    ax2 = fig.add_subplot(222)
    ax2.pie(status_counts, labels=status_labels, autopct="%1.0f%%", startangle=90)
    ax2.set_title("Student Status Distribution")

    # -------- CATEGORY PIE CHART --------
    ax3 = fig.add_subplot(223)
    ax3.pie(cat_counts, labels=cat_labels, autopct="%1.0f%%", startangle=90)
    ax3.set_title("Category Distribution")

    # -------- AGE TREND --------
    ax4 = fig.add_subplot(224)
    ax4.plot(ages, age_counts, marker="o")
    ax4.set_title("Student Age Distribution")
    ax4.set_xlabel("Age")
    ax4.set_ylabel("Number of Students")
    ax4.grid(True)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)