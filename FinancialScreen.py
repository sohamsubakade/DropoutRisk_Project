import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import DB_PATH
from FinancialDashboard import financial_dashboard   # Dashboard Import


def financial_screen():

    top = tk.Toplevel()
    top.title("Financial Risk Analysis")
    top.geometry("1000x600")

    ttk.Label(top, text="Financial Risk Students",
              font=("Helvetica", 18, "bold")).pack(pady=10)

    # ===================== FORM =====================
    form = ttk.Frame(top)
    form.pack(pady=10)

    ttk.Label(form, text="Student ID").grid(row=0, column=0)
    sid = ttk.Entry(form)
    sid.grid(row=0, column=1)

    ttk.Label(form, text="Family Income").grid(row=1, column=0)
    income = ttk.Entry(form)
    income.grid(row=1, column=1)

    ttk.Label(form, text="Fee Due").grid(row=2, column=0)
    fee = ttk.Entry(form)
    fee.grid(row=2, column=1)

    ttk.Label(form, text="Financial Stress (0-10)").grid(row=3, column=0)
    stress = ttk.Entry(form)
    stress.grid(row=3, column=1)

    # ===================== TABLE =====================
    columns = ("student_id","family_income","fee_due","financial_stress","risk")

    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.replace("_"," ").title())
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    # ===================== FUNCTIONS =====================

    def calculate_risk(stress_val):

        try:
            stress_val = float(stress_val)
        except:
            stress_val = 0

        if stress_val >= 7:
            return "HIGH","high"
        elif stress_val >= 4:
            return "MEDIUM","medium"
        else:
            return "LOW","low"

    def load_data():

        tree.delete(*tree.get_children())

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        SELECT student_id, family_income, fee_due, financial_stress_level
        FROM financial_status
        """)

        for row in c.fetchall():

            risk, tag = calculate_risk(row[3])

            tree.insert(
                "",
                "end",
                values=(row[0],row[1],row[2],row[3],risk),
                tags=(tag,)
            )

        conn.close()

        tree.tag_configure("high", background="#ffb3b3")
        tree.tag_configure("medium", background="#fff0b3")
        tree.tag_configure("low", background="#b3ffcc")

    def clear():

        sid.delete(0, tk.END)
        income.delete(0, tk.END)
        fee.delete(0, tk.END)
        stress.delete(0, tk.END)

    def insert_data():

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        INSERT INTO financial_status(
        student_id,family_income,fee_due,financial_stress_level)
        VALUES(?,?,?,?)
        """,(
            sid.get(),
            income.get(),
            fee.get(),
            stress.get()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Saved","Record Inserted")

        load_data()
        clear()

    def update_data():

        selected = tree.focus()

        if not selected:
            messagebox.showerror("Error","Select record first")
            return

        student = tree.item(selected)["values"][0]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        UPDATE financial_status
        SET family_income=?, fee_due=?, financial_stress_level=?
        WHERE student_id=?
        """,(
            income.get(),
            fee.get(),
            stress.get(),
            student
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Updated","Record Updated")

        load_data()
        clear()

    def select_record(event):

        selected = tree.focus()

        if not selected:
            return

        values = tree.item(selected,"values")

        sid.delete(0,tk.END)
        sid.insert(0,values[0])

        income.delete(0,tk.END)
        income.insert(0,values[1])

        fee.delete(0,tk.END)
        fee.insert(0,values[2])

        stress.delete(0,tk.END)
        stress.insert(0,values[3])

    tree.bind("<ButtonRelease-1>", select_record)

    # ===================== BUTTONS =====================
    btn_frame = ttk.Frame(top)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame,text="Add",command=insert_data)\
        .grid(row=0,column=0,padx=10)

    ttk.Button(btn_frame,text="Update",command=update_data)\
        .grid(row=0,column=1,padx=10)

    ttk.Button(btn_frame,text="Refresh",command=load_data)\
        .grid(row=0,column=2,padx=10)

    ttk.Button(btn_frame,text="Clear",command=clear)\
        .grid(row=0,column=3,padx=10)

    ttk.Button(btn_frame,text="Dashboard",
               command=financial_dashboard)\
        .grid(row=0,column=4,padx=10)

    # Load data initially
    load_data()
