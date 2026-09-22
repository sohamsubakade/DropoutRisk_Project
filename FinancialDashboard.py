import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def financial_dashboard():

    top = tk.Toplevel()
    top.title("Financial Analytics Dashboard")
    top.geometry("900x600")

    ttk.Label(
        top,
        text="Financial Risk Dashboard",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT family_income, fee_due, financial_stress_level
    FROM financial_status
    """)

    income = []
    fee_due = []
    stress = []

    for row in c.fetchall():
        try:
            income.append(float(row[0]))
            fee_due.append(float(row[1]))
            stress.append(float(row[2]))
        except:
            pass

    conn.close()

    fig = plt.Figure(figsize=(9,4))

    # =====================================================
    # 1️⃣ Financial Stress Distribution
    # =====================================================
    ax1 = fig.add_subplot(121)

    low = 0
    medium = 0
    high = 0

    for s in stress:
        if s >= 7:
            high += 1
        elif s >= 4:
            medium += 1
        else:
            low += 1

    labels = ["Low Stress", "Medium Stress", "High Stress"]
    values = [low, medium, high]

    ax1.pie(values, labels=labels, autopct="%1.0f%%", startangle=90)

    ax1.set_title("Financial Stress Distribution")


    # =====================================================
    # 2️⃣ Average Income vs Fee Due
    # =====================================================
    ax2 = fig.add_subplot(122)

    avg_income = sum(income)/len(income) if income else 0
    avg_fee = sum(fee_due)/len(fee_due) if fee_due else 0

    labels = ["Family Income", "Fee Due"]
    values = [avg_income, avg_fee]

    ax2.bar(labels, values)

    ax2.set_title("Average Income vs Fee Due")
    ax2.set_ylabel("Amount")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)