import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def academic_dashboard():

    top = tk.Toplevel()
    top.title("Academic Performance Dashboard")
    top.geometry("1100x700")

    ttk.Label(
        top,
        text="Academic Performance Dashboard",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ================= CGPA DATA =================
    c.execute("SELECT CGPA FROM academic_performance")
    cgpa_data = [float(row[0]) for row in c.fetchall() if row[0]]

    # ================= FAILED SUBJECTS =================
    c.execute("""
        SELECT failed_subjects, COUNT(*)
        FROM academic_performance
        GROUP BY failed_subjects
        ORDER BY failed_subjects
    """)
    fail_data = c.fetchall()

    fail_labels = [str(row[0]) for row in fail_data]
    fail_counts = [row[1] for row in fail_data]

    # ================= GPA BY SEMESTER =================
    c.execute("""
        SELECT semester, AVG(GPA)
        FROM academic_performance
        GROUP BY semester
        ORDER BY semester
    """)
    sem_data = c.fetchall()

    semesters = [row[0] for row in sem_data]
    avg_gpa = [float(row[1]) for row in sem_data]

    # ================= CORRELATION DATA =================
    c.execute("SELECT CGPA, failed_subjects FROM academic_performance")

    cgpa_corr = []
    fail_corr = []

    for row in c.fetchall():
        try:
            cgpa_corr.append(float(row[0]))
            fail_corr.append(int(row[1]))
        except:
            pass

    conn.close()

    # ================= CREATE FIGURE =================
    fig = plt.Figure(figsize=(11,6))

    # -------- CGPA PIE CHART --------
    low = 0
    avg = 0
    good = 0
    excellent = 0

    for cg in cgpa_data:
        if cg < 5:
            low += 1
        elif cg < 7:
            avg += 1
        elif cg < 8.5:
            good += 1
        else:
            excellent += 1

    labels = ["0-5 (Low)", "5-7 (Average)", "7-8.5 (Good)", "8.5-10 (Excellent)"]
    values = [low, avg, good, excellent]

    ax1 = fig.add_subplot(221)
    ax1.pie(values, labels=labels, autopct="%1.0f%%", startangle=90)
    ax1.set_title("CGPA Distribution")

    # -------- FAILED SUBJECTS BAR --------
    ax2 = fig.add_subplot(222)
    ax2.bar(fail_labels, fail_counts)
    ax2.set_title("Backlog Distribution")
    ax2.set_xlabel("Failed Subjects")
    ax2.set_ylabel("Number of Students")

    # -------- GPA TREND --------
    ax3 = fig.add_subplot(223)
    ax3.plot(semesters, avg_gpa, marker="o")
    ax3.set_title("Average GPA by Semester")
    ax3.set_xlabel("Semester")
    ax3.set_ylabel("Average GPA")
    ax3.grid(True)

    # -------- CORRELATION GRAPH --------


    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)