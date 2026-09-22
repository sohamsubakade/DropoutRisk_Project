import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def prediction_dashboard():

    top = tk.Toplevel()
    top.title("Dropout Prediction Dashboard")
    top.geometry("700x500")

    ttk.Label(
        top,
        text="Dropout Risk Distribution",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ================= RISK DISTRIBUTION =================
    c.execute("""
    SELECT risk_level, COUNT(*)
    FROM risk_assessment
    GROUP BY risk_level
    """)

    risk_data = c.fetchall()

    labels = [row[0] for row in risk_data]
    counts = [row[1] for row in risk_data]

    conn.close()

    # ================= PIE CHART =================
    fig = plt.Figure(figsize=(6,5))

    ax = fig.add_subplot(111)

    ax.pie(
        counts,
        labels=labels,
        autopct="%1.0f%%",
        startangle=90
    )

    ax.set_title("Dropout Risk Level Distribution")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)