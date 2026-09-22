import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database import DB_PATH
from AcademicDashboard import academic_dashboard   # <-- Added


# ===== LOAD PERFORMANCE DATA =====
def load_data():

    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM academic_performance")

    for row in c.fetchall():
        tree.insert("", "end", values=row)

    conn.close()


# ===== SUMMARY ANALYSIS =====
def analyze():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Average CGPA
    c.execute("SELECT AVG(CGPA) FROM academic_performance")
    avg = c.fetchone()[0]

    # Failed count
    c.execute("SELECT COUNT(*) FROM academic_performance WHERE failed_subjects > 0")
    failed = c.fetchone()[0]

    # Warnings
    c.execute("SELECT COUNT(*) FROM academic_performance WHERE academic_warning='Yes'")
    warn = c.fetchone()[0]

    conn.close()

    lbl_avg.config(text=f"Average CGPA : {round(avg,2) if avg else 0}")
    lbl_fail.config(text=f"Students with Backlogs : {failed}")
    lbl_warn.config(text=f"Academic Warnings : {warn}")


# ===== MAIN SCREEN =====
def academic_performance_screen():

    global tree, lbl_avg, lbl_fail, lbl_warn

    top = tk.Tk()
    top.title("Academic Performance Analysis")

    # FULL SCREEN
    top.attributes('-fullscreen', True)
    top.bind("<Escape>", lambda e: top.attributes('-fullscreen', False))

    ttk.Label(top,
        text="Academic Performance Analysis",
        font=("Helvetica", 22, "bold")
    ).pack(pady=10)

    # ===== SUMMARY FRAME =====
    s = ttk.Frame(top, padding=10)
    s.pack()

    lbl_avg = ttk.Label(s, text="Average CGPA : 0", font=("Arial", 14))
    lbl_avg.grid(row=0, column=0, padx=20)

    lbl_fail = ttk.Label(s, text="Students with Backlogs : 0", font=("Arial", 14))
    lbl_fail.grid(row=0, column=1, padx=20)

    lbl_warn = ttk.Label(s, text="Academic Warnings : 0", font=("Arial", 14))
    lbl_warn.grid(row=0, column=2, padx=20)

    ttk.Button(top, text="Analyze", command=analyze).pack(pady=5)

    # ===== DASHBOARD BUTTON (Added) =====
    ttk.Button(top, text="Academic Dashboard", command=academic_dashboard).pack(pady=5)

    # ===== TABLE =====
    tree = ttk.Treeview(top,
        columns=(
        "id","student_id","semester","GPA","CGPA",
        "credits_reg","credits_earned","failed",
        "attendance","internal","external",
        "rank","improve","warning","date"),
        show="headings"
    )

    for col in tree["columns"]:
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True)

    ttk.Button(top, text="Refresh", command=load_data).pack(pady=5)
    ttk.Button(top, text="Back", command=top.destroy).pack(pady=5)

    load_data()
    top.mainloop()