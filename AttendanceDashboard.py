import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def attendance_dashboard(parent=None):

    # ===== WINDOW SETUP =====
    top = tk.Toplevel(parent) if parent else tk.Tk()
    top.title("Attendance Analytics Dashboard")
    top.geometry("1100x700")

    # ===== TITLE =====
    ttk.Label(
        top,
        text="Attendance Analytics Dashboard",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    # ===== DATABASE =====
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Attendance %
    c.execute("SELECT attendance_percentage FROM attendance")
    attendance = [float(row[0]) for row in c.fetchall() if row[0]]

    # Semester trend
    c.execute("""
        SELECT semester, AVG(attendance_percentage)
        FROM attendance
        GROUP BY semester
        ORDER BY semester
    """)
    sem_data = c.fetchall()

    semesters = [row[0] for row in sem_data]
    avg_attendance = [float(row[1]) for row in sem_data]

    # Defaulters
    c.execute("SELECT COUNT(*) FROM attendance WHERE attendance_percentage < 75")
    defaulters = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM attendance WHERE attendance_percentage >= 75")
    regular = c.fetchone()[0]

    conn.close()

    # ===== HANDLE EMPTY DATA =====
    if not attendance:
        ttk.Label(top, text="No Attendance Data Available", font=("Arial", 14)).pack()
        return

    # ===== FIGURE =====
    fig = plt.Figure(figsize=(11, 6))

    # ===== PIE =====
    ax1 = fig.add_subplot(221)
    ax1.pie(
        [regular, defaulters],
        labels=["Regular (>=75%)", "Defaulters (<75%)"],
        autopct="%1.0f%%",
        startangle=90
    )
    ax1.set_title("Attendance Status Distribution")

    # ===== DISTRIBUTION =====
    low = mid1 = mid2 = good = excellent = 0

    for att in attendance:
        if att < 50:
            low += 1
        elif att < 65:
            mid1 += 1
        elif att < 75:
            mid2 += 1
        elif att < 85:
            good += 1
        else:
            excellent += 1

    ax2 = fig.add_subplot(222)
    ax2.bar(
        ["0-50%", "50-65%", "65-75%", "75-85%", "85-100%"],
        [low, mid1, mid2, good, excellent]
    )
    ax2.set_title("Attendance Distribution")
    ax2.set_xlabel("Range")
    ax2.set_ylabel("Students")
    ax2.grid(axis="y")

    # ===== TREND =====
    ax3 = fig.add_subplot(223)
    ax3.plot(semesters, avg_attendance, marker="o")
    ax3.set_title("Semester Trend")
    ax3.set_xlabel("Semester")
    ax3.set_ylabel("Attendance %")
    ax3.grid(True)

    # ===== BAR =====
    ax4 = fig.add_subplot(224)
    ax4.bar(["Regular", "Defaulters"], [regular, defaulters])
    ax4.set_title("Regular vs Defaulters")

    fig.tight_layout()

    # ===== CANVAS =====
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # ===== BACK BUTTON =====
    ttk.Button(
        top,
        text="Back",
        command=top.destroy
    ).pack(pady=10)