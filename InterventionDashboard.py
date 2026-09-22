import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def intervention_dashboard():

    top = tk.Toplevel()
    top.title("Intervention Dashboard")
    top.geometry("900x600")

    ttk.Label(
        top,
        text="Intervention Dashboard (Analytics)",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)

    # ================= FETCH DATA =================
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM intervention")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM intervention WHERE progress_status='Completed'")
    completed = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM intervention WHERE progress_status='Ongoing'")
    ongoing = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM intervention WHERE progress_status='Pending'")
    pending = c.fetchone()[0]

    conn.close()

    # ================= MATPLOTLIB FIGURE =================
    fig = Figure(figsize=(8, 4), dpi=100)

    # -------- PIE CHART --------
    ax1 = fig.add_subplot(121)

    labels = ["Completed", "Ongoing", "Pending"]
    values = [completed, ongoing, pending]

    ax1.pie(values, labels=labels, autopct="%1.1f%%")
    ax1.set_title("Intervention Status Distribution")

    # -------- BAR GRAPH --------
    # -------- SCORE BASED BAR GRAPH --------
    ax2 = fig.add_subplot(122)

    # Fetch scores
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT effectiveness_score FROM intervention")
    scores = c.fetchall()
    conn.close()

    # Count categories
    high = 0
    medium = 0
    low = 0

    for s in scores:
        try:
            val = float(s[0])
            if val >= 8:
                high += 1
            elif val >= 6:
                medium += 1
            else:
                low += 1
        except:
            pass

    categories = ["High", "Medium", "Low"]
    values = [high, medium, low]

    ax2.bar(categories, values)

    ax2.set_title("Effectiveness Score Distribution")
    ax2.set_xlabel("Score Level")
    ax2.set_ylabel("Number of Students")
    # ================= DISPLAY IN TKINTER =================
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)