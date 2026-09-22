import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_PATH
from BehaviorDashboard import behavior_dashboard


def behavior_screen():

    top = tk.Toplevel()
    top.title("Behavioral & Engagement Analysis")
    top.geometry("1000x600")

    ttk.Label(
        top,
        text="Behavioral & Engagement Analysis",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)

    # ================= FORM =================
    form = ttk.Frame(top)
    form.pack(pady=10)

    ttk.Label(form, text="Student ID").grid(row=0, column=0)
    sid = ttk.Entry(form)
    sid.grid(row=0, column=1)

    ttk.Label(form, text="Motivation Level (0-10)").grid(row=1, column=0)
    motivation = ttk.Entry(form)
    motivation.grid(row=1, column=1)

    ttk.Label(form, text="Stress Level (0-10)").grid(row=2, column=0)
    stress = ttk.Entry(form)
    stress.grid(row=2, column=1)

    ttk.Label(form, text="Class Participation").grid(row=3, column=0)
    participation = ttk.Entry(form)
    participation.grid(row=3, column=1)

    # ================= TABLE =================
    columns = ("student_id", "motivation", "stress", "participation", "risk")

    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    # ================= FUNCTIONS =================

    def calculate_risk(stress_val, motivation_val):

        try:
            stress_val = float(stress_val)
            motivation_val = float(motivation_val)
        except:
            return "LOW", "low"

        score = stress_val - motivation_val

        if score >= 4:
            return "HIGH", "high"
        elif score >= 1:
            return "MEDIUM", "medium"
        else:
            return "LOW", "low"

    def load_data():

        tree.delete(*tree.get_children())

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        SELECT student_id, motivation_level, stress_level, classroom_participation
        FROM behavioral_record
        """)

        for row in c.fetchall():

            risk, tag = calculate_risk(row[2], row[1])

            tree.insert(
                "",
                "end",
                values=(row[0], row[1], row[2], row[3], risk),
                tags=(tag,)
            )

        conn.close()

        tree.tag_configure("high", background="#ffb3b3")
        tree.tag_configure("medium", background="#fff0b3")
        tree.tag_configure("low", background="#b3ffcc")

    def clear():

        sid.delete(0, tk.END)
        motivation.delete(0, tk.END)
        stress.delete(0, tk.END)
        participation.delete(0, tk.END)

    def insert_data():

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        INSERT INTO behavioral_record(student_id,motivation_level,stress_level,classroom_participation)
        VALUES(?,?,?,?)
        """, (
            sid.get(),
            motivation.get(),
            stress.get(),
            participation.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Behavior record inserted")
        load_data()
        clear()

    def update_data():

        selected = tree.focus()

        if not selected:
            messagebox.showerror("Error", "Select record first")
            return

        student = tree.item(selected)["values"][0]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        UPDATE behavioral_record
        SET motivation_level=?, stress_level=?, classroom_participation=?
        WHERE student_id=?
        """, (
            motivation.get(),
            stress.get(),
            participation.get(),
            student
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Behavior record updated")

        load_data()
        clear()

    def select_record(event):

        selected = tree.focus()

        if not selected:
            return

        values = tree.item(selected, "values")

        sid.delete(0, tk.END)
        sid.insert(0, values[0])

        motivation.delete(0, tk.END)
        motivation.insert(0, values[1])

        stress.delete(0, tk.END)
        stress.insert(0, values[2])

        participation.delete(0, tk.END)
        participation.insert(0, values[3])

    tree.bind("<ButtonRelease-1>", select_record)

    # ================= BUTTONS =================
    btn_frame = ttk.Frame(top)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Add", command=insert_data).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Update", command=update_data).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Refresh", command=load_data).grid(row=0, column=2, padx=10)
    ttk.Button(btn_frame, text="Clear", command=clear).grid(row=0, column=3, padx=10)

    # DASHBOARD BUTTON
    ttk.Button(btn_frame, text="Dashboard", command=behavior_dashboard).grid(row=0, column=4, padx=10)

    load_data()