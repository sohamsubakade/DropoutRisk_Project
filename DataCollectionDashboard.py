import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def data_collection_dashboard():

    top = tk.Toplevel()
    top.title("Integrated Data Dashboard")
    top.geometry("1000x650")

    ttk.Label(
        top,
        text="Integrated Data Analytics Dashboard",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT
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

    attendance = []
    cgpa = []
    financial = []
    motivation = []
    stress = []

    for row in c.fetchall():
        try:
            attendance.append(float(row[0]))
            cgpa.append(float(row[1]))
            financial.append(float(row[2]))
            motivation.append(float(row[3]))
            stress.append(float(row[4]))
        except:
            pass

    conn.close()

    fig = plt.Figure(figsize=(10,5))

    # =====================================================
    # 1️⃣ Attendance Category Distribution (Bar Graph)
    # =====================================================
    ax1 = fig.add_subplot(131)

    excellent = len([x for x in attendance if x >= 90])
    good = len([x for x in attendance if 75 <= x < 90])
    low = len([x for x in attendance if 50 <= x < 75])
    critical = len([x for x in attendance if x < 50])

    labels = ["Excellent", "Good", "Low", "Critical"]
    values = [excellent, good, low, critical]

    ax1.bar(labels, values)

    ax1.set_title("Attendance Category Distribution")
    ax1.set_ylabel("Number of Students")
    ax1.set_xlabel("Attendance Level")

    # =====================================================
    # 2️⃣ Financial Stress Distribution (Pie Chart)
    # =====================================================
    ax2 = fig.add_subplot(132)

    low = len([x for x in financial if x < 4])
    medium = len([x for x in financial if 4 <= x < 7])
    high = len([x for x in financial if x >= 7])

    labels = ["Low", "Medium", "High"]
    values = [low, medium, high]

    ax2.pie(values, labels=labels, autopct="%1.0f%%", startangle=90)

    ax2.set_title("Financial Stress Distribution")

    # =====================================================
    # 3️⃣ Motivation vs Stress (Stacked Line)
    # =====================================================
    ax3 = fig.add_subplot(133)

    x = list(range(len(motivation)))

    ax3.stackplot(
        x,
        motivation,
        stress,
        labels=["Motivation", "Stress"]
    )

    ax3.set_title("Motivation vs Stress Trend")
    ax3.set_xlabel("Students")
    ax3.set_ylabel("Score")
    ax3.legend(loc="upper right")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)