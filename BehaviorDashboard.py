import tkinter as tk
from tkinter import ttk
import sqlite3
from database import DB_PATH

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def behavior_dashboard():

    top = tk.Toplevel()
    top.title("Behavior Analytics Dashboard")
    top.geometry("900x600")

    ttk.Label(
        top,
        text="Behavioral & Engagement Dashboard",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    SELECT motivation_level, stress_level, classroom_participation
    FROM behavioral_record
    """)

    motivation = []
    stress = []
    participation = []

    for row in c.fetchall():
        try:
            motivation.append(float(row[0]))
            stress.append(float(row[1]))
            participation.append(float(row[2]))
        except:
            pass

    conn.close()

    fig = plt.Figure(figsize=(9,4))

    # =====================================================
    # 1️⃣ Average Behavioral Scores
    # =====================================================
    ax1 = fig.add_subplot(121)

    avg_mot = sum(motivation)/len(motivation) if motivation else 0
    avg_stress = sum(stress)/len(stress) if stress else 0
    avg_part = sum(participation)/len(participation) if participation else 0

    labels = ["Motivation", "Stress", "Participation"]
    values = [avg_mot, avg_stress, avg_part]

    ax1.bar(labels, values)

    ax1.set_title("Average Behavioral Scores")
    ax1.set_ylabel("Score")
    ax1.set_ylim(0,10)
    ax1.grid(axis="y")

    # =====================================================
    # 2️⃣ Behavior Risk Distribution
    # =====================================================
    ax2 = fig.add_subplot(122)

    low = 0
    medium = 0
    high = 0

    for m, s in zip(motivation, stress):

        score = s - m

        if score >= 4:
            high += 1
        elif score >= 1:
            medium += 1
        else:
            low += 1

    labels = ["Low Risk", "Medium Risk", "High Risk"]
    values = [low, medium, high]

    ax2.pie(values, labels=labels, autopct="%1.0f%%", startangle=90)

    ax2.set_title("Behavior Risk Distribution")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)