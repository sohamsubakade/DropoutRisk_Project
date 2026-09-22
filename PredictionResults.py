import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_PATH
from ml_predictor import run_ml_model
from PredictionDashboard import prediction_dashboard   # Dashboard Import


def prediction_screen():

    top = tk.Toplevel()
    top.title("Dropout Prediction Results")
    top.geometry("900x500")

    ttk.Label(
        top,
        text="Predicted Dropout Risk Students",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)

    # ================= TABLE =================
    columns = ("student_id","score","risk","dropout")

    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ================= CHECK IF PREDICTION EXISTS =================
    c.execute("SELECT COUNT(*) FROM risk_assessment")
    count = c.fetchone()[0]

    # If empty → ask to run ML
    if count == 0:

        run = messagebox.askyesno(
            "No Prediction Found",
            "No risk analysis available.\nRun prediction now?"
        )

        if run:
            run_ml_model()

    # ================= LOAD DATA =================
    c.execute("""
    SELECT student_id, overall_risk_score, risk_level, predicted_dropout
    FROM risk_assessment
    ORDER BY overall_risk_score DESC
    """)

    for row in c.fetchall():

        tag = "high" if row[2]=="HIGH" else "medium" if row[2]=="MEDIUM" else "low"

        tree.insert("", "end", values=row, tags=(tag,))

    conn.close()

    # ================= COLOR ROWS =================
    tree.tag_configure("high", background="#ffb3b3")
    tree.tag_configure("medium", background="#fff0b3")
    tree.tag_configure("low", background="#b3ffcc")


    # ================= BUTTON FRAME =================
    btn_frame = ttk.Frame(top)
    btn_frame.pack(pady=10)

    # Run Prediction Button

    # Refresh Button
    ttk.Button(
        btn_frame,
        text="Refresh",
        command=prediction_screen
    ).grid(row=0, column=1, padx=10)

    # Dashboard Button
    ttk.Button(
        btn_frame,
        text="Prediction Dashboard",
        command=prediction_dashboard
    ).grid(row=0, column=2, padx=10)

    # Close Button
    ttk.Button(
        btn_frame,
        text="Close",
        command=top.destroy
    ).grid(row=0, column=3, padx=10)