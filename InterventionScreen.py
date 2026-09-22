import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_PATH
from InterventionDashboard import intervention_dashboard


def intervention_screen():

    top = tk.Toplevel()
    top.title("Intervention & Counseling")
    top.geometry("1200x650")

    ttk.Label(
        top,
        text="Intervention & Counseling Management",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)

    # ================= FORM =================
    form = ttk.Frame(top)
    form.pack(pady=10)

    # Row 1
    ttk.Label(form, text="Student ID").grid(row=0, column=0)
    sid = ttk.Entry(form)
    sid.grid(row=0, column=1)

    ttk.Label(form, text="Risk ID").grid(row=0, column=2)
    risk_id = ttk.Entry(form)
    risk_id.grid(row=0, column=3)

    # Row 2
    ttk.Label(form, text="Intervention Type").grid(row=1, column=0)
    intervention_type = ttk.Combobox(form, values=[
        "Counseling",
        "Academic Mentoring",
        "Financial Aid Support",
        "Psychological Counseling",
        "Peer Support Program"
    ])
    intervention_type.grid(row=1, column=1)

    ttk.Label(form, text="Assigned Staff").grid(row=1, column=2)
    staff = ttk.Entry(form)
    staff.grid(row=1, column=3)

    # Row 3
    ttk.Label(form, text="Start Date").grid(row=2, column=0)
    start_date = ttk.Entry(form)
    start_date.grid(row=2, column=1)

    ttk.Label(form, text="End Date").grid(row=2, column=2)
    end_date = ttk.Entry(form)
    end_date.grid(row=2, column=3)

    # Row 4
    ttk.Label(form, text="Follow-up Required").grid(row=3, column=0)
    followup = ttk.Combobox(form, values=["Yes", "No"])
    followup.grid(row=3, column=1)

    ttk.Label(form, text="Progress Status").grid(row=3, column=2)
    progress = ttk.Combobox(form, values=[
        "Ongoing",
        "Completed",
        "Pending"
    ])
    progress.grid(row=3, column=3)

    # Row 5
    ttk.Label(form, text="Outcome").grid(row=4, column=0)
    outcome = ttk.Combobox(form, values=[
        "Improving",
        "Stable",
        "Successful",
        "Needs Attention"
    ])
    outcome.grid(row=4, column=1)

    ttk.Label(form, text="Effectiveness Score").grid(row=4, column=2)
    effectiveness = ttk.Entry(form)
    effectiveness.grid(row=4, column=3)

    # Row 6
    ttk.Label(form, text="Communication Mode").grid(row=5, column=0)
    communication = ttk.Combobox(form, values=[
        "Online",
        "Offline",
        "Hybrid"
    ])
    communication.grid(row=5, column=1)

    ttk.Label(form, text="Notes").grid(row=5, column=2)
    notes = ttk.Entry(form, width=30)
    notes.grid(row=5, column=3)

    # Default values
    intervention_type.current(0)
    followup.current(0)
    progress.current(0)
    outcome.current(0)
    communication.current(0)

    # ================= TABLE =================
    columns = (
        "id", "student", "risk", "type",
        "staff", "progress", "outcome", "effectiveness"
    )

    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=140)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    # ================= FUNCTIONS =================

    def load_data():
        tree.delete(*tree.get_children())

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        SELECT intervention_id, student_id, risk_id,
               intervention_type, assigned_staff,
               progress_status, outcome, effectiveness_score
        FROM intervention
        """)

        for row in c.fetchall():

            status = row[5]

            # Color tagging
            if status == "Completed":
                tag = "completed"
            elif status == "Ongoing":
                tag = "ongoing"
            else:
                tag = "pending"

            tree.insert("", "end", values=row, tags=(tag,))

        conn.close()

        # Colors
        tree.tag_configure("completed", background="#b3ffcc")  # Green
        tree.tag_configure("ongoing", background="#fff0b3")    # Yellow
        tree.tag_configure("pending", background="#ffb3b3")    # Red

    def clear():
        for field in [sid, risk_id, staff, start_date, end_date,
                      effectiveness, notes]:
            field.delete(0, tk.END)

        intervention_type.current(0)
        followup.current(0)
        progress.current(0)
        outcome.current(0)
        communication.current(0)

    def insert_data():

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        INSERT INTO intervention(
            student_id,
            risk_id,
            intervention_type,
            assigned_staff,
            intervention_start_date,
            intervention_end_date,
            follow_up_required,
            progress_status,
            outcome,
            notes,
            effectiveness_score,
            communication_mode,
            last_updated
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
        """, (
            sid.get(),
            risk_id.get(),
            intervention_type.get(),
            staff.get(),
            start_date.get(),
            end_date.get(),
            followup.get(),
            progress.get(),
            outcome.get(),
            notes.get(),
            effectiveness.get(),
            communication.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Record added")

        load_data()
        clear()

    def update_data():

        selected = tree.focus()

        if not selected:
            messagebox.showerror("Error", "Select record first")
            return

        values = tree.item(selected, "values")
        intervention_id = values[0]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        UPDATE intervention
        SET intervention_type=?,
            assigned_staff=?,
            intervention_start_date=?,
            intervention_end_date=?,
            follow_up_required=?,
            progress_status=?,
            outcome=?,
            notes=?,
            effectiveness_score=?,
            communication_mode=?,
            last_updated=datetime('now')
        WHERE intervention_id=?
        """, (
            intervention_type.get(),
            staff.get(),
            start_date.get(),
            end_date.get(),
            followup.get(),
            progress.get(),
            outcome.get(),
            notes.get(),
            effectiveness.get(),
            communication.get(),
            intervention_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Record updated")

        load_data()
        clear()

    def select_record(event):

        selected = tree.focus()
        if not selected:
            return

        values = tree.item(selected, "values")

        sid.delete(0, tk.END)
        sid.insert(0, values[1])

        risk_id.delete(0, tk.END)
        risk_id.insert(0, values[2])

        intervention_type.set(values[3])

        staff.delete(0, tk.END)
        staff.insert(0, values[4])

        progress.set(values[5])
        outcome.set(values[6])

        effectiveness.delete(0, tk.END)
        effectiveness.insert(0, values[7])

    tree.bind("<ButtonRelease-1>", select_record)

    # ================= BUTTONS =================
    btn_frame = ttk.Frame(top)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Add", command=insert_data).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Update", command=update_data).grid(row=0, column=1, padx=10)
    ttk.Button(btn_frame, text="Refresh", command=load_data).grid(row=0, column=2, padx=10)
    ttk.Button(btn_frame, text="Clear", command=clear).grid(row=0, column=3, padx=10)
    ttk.Button(btn_frame, text="Dashboard", command=intervention_dashboard).grid(row=0, column=4, padx=10)

    load_data()