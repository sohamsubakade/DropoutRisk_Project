import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database import DB_PATH, create_database
from AnalyticsScreen import analytics_screen   # ← Added import


# ===== SAVE STUDENT =====
def save_student():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT INTO student(
    first_name,last_name,gender,date_of_birth,age,
    email,phone_number,enrollment_date,course_id,
    academic_year,semester,category,nationality,current_status)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        txt_fn.get(),
        txt_ln.get(),
        cmb_gender.get(),
        txt_dob.get(),
        txt_age.get(),
        txt_email.get(),
        txt_phone.get(),
        txt_enroll.get(),
        cmb_course.get(),
        txt_year.get(),
        txt_sem.get(),
        cmb_category.get(),
        txt_nationality.get(),
        cmb_status.get()
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student Added Successfully")
    load_data()
    clear()


# ===== LOAD DATA =====
def load_data():

    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM student")

    for row in c.fetchall():
        tree.insert("", "end", values=row)

    conn.close()


# ===== WHEN ROW SELECTED =====
def select_record(event):

    selected = tree.item(tree.focus())['values']
    if not selected:
        return

    txt_fn.delete(0, tk.END); txt_fn.insert(0, selected[1])
    txt_ln.delete(0, tk.END); txt_ln.insert(0, selected[2])
    cmb_gender.set(selected[3])
    txt_dob.delete(0, tk.END); txt_dob.insert(0, selected[4])
    txt_age.delete(0, tk.END); txt_age.insert(0, selected[5])
    txt_email.delete(0, tk.END); txt_email.insert(0, selected[6])
    txt_phone.delete(0, tk.END); txt_phone.insert(0, selected[7])
    txt_enroll.delete(0, tk.END); txt_enroll.insert(0, selected[8])
    cmb_course.set(selected[9])
    txt_year.delete(0, tk.END); txt_year.insert(0, selected[10])
    txt_sem.delete(0, tk.END); txt_sem.insert(0, selected[11])
    cmb_category.set(selected[12])
    txt_nationality.delete(0, tk.END); txt_nationality.insert(0, selected[13])
    cmb_status.set(selected[14])


# ===== UPDATE =====
def update_student():

    selected = tree.item(tree.focus())['values']

    if not selected:
        messagebox.showerror("Error", "Select Record First")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    UPDATE student SET
    first_name=?, last_name=?, gender=?, date_of_birth=?, age=?,
    email=?, phone_number=?, enrollment_date=?, course_id=?,
    academic_year=?, semester=?, category=?, nationality=?, current_status=?
    WHERE student_id=?
    """,
    (
        txt_fn.get(), txt_ln.get(), cmb_gender.get(), txt_dob.get(),
        txt_age.get(), txt_email.get(), txt_phone.get(),
        txt_enroll.get(), cmb_course.get(), txt_year.get(),
        txt_sem.get(), cmb_category.get(), txt_nationality.get(),
        cmb_status.get(), selected[0]
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Updated", "Record Updated Successfully")
    load_data()
    clear()


# ===== CLEAR =====
def clear():
    for e in [txt_fn, txt_ln, txt_dob, txt_age, txt_email,
              txt_phone, txt_enroll, txt_year, txt_sem,
              txt_nationality]:
        e.delete(0, tk.END)


# ===== MAIN UI =====
def student_profile_screen():

    global txt_fn, txt_ln, cmb_gender, txt_dob, txt_age
    global txt_email, txt_phone, txt_enroll, cmb_course
    global txt_year, txt_sem, cmb_category, txt_nationality
    global cmb_status, tree

    create_database()

    top = tk.Tk()
    top.title("Student Profile Management")

    # FULL SCREEN
    top.attributes('-fullscreen', True)
    top.bind("<Escape>", lambda e: top.attributes('-fullscreen', False))

    ttk.Label(top, text="Student Profile Management",
              font=("Helvetica", 22, "bold")).pack(pady=10)

    f = ttk.Frame(top, padding=10)
    f.pack()

    # ===== FORM =====
    ttk.Label(f,text="First Name").grid(row=0,column=0)
    txt_fn = ttk.Entry(f); txt_fn.grid(row=0,column=1)

    ttk.Label(f,text="Last Name").grid(row=1,column=0)
    txt_ln = ttk.Entry(f); txt_ln.grid(row=1,column=1)

    ttk.Label(f,text="Gender").grid(row=2,column=0)
    cmb_gender = ttk.Combobox(f, values=["Male","Female","Other"])
    cmb_gender.grid(row=2,column=1)

    ttk.Label(f,text="Date of Birth").grid(row=3,column=0)
    txt_dob = ttk.Entry(f); txt_dob.grid(row=3,column=1)

    ttk.Label(f,text="Age").grid(row=4,column=0)
    txt_age = ttk.Entry(f); txt_age.grid(row=4,column=1)

    ttk.Label(f,text="Email").grid(row=5,column=0)
    txt_email = ttk.Entry(f); txt_email.grid(row=5,column=1)

    ttk.Label(f,text="Phone").grid(row=6,column=0)
    txt_phone = ttk.Entry(f); txt_phone.grid(row=6,column=1)

    ttk.Label(f,text="Enrollment Date").grid(row=7,column=0)
    txt_enroll = ttk.Entry(f); txt_enroll.grid(row=7,column=1)

    ttk.Label(f,text="Course").grid(row=8,column=0)
    cmb_course = ttk.Combobox(f, values=["MCA","MBA","BBA"])
    cmb_course.grid(row=8,column=1)

    ttk.Label(f,text="Academic Year").grid(row=9,column=0)
    txt_year = ttk.Entry(f); txt_year.grid(row=9,column=1)

    ttk.Label(f,text="Semester").grid(row=10,column=0)
    txt_sem = ttk.Entry(f); txt_sem.grid(row=10,column=1)

    ttk.Label(f,text="Category").grid(row=11,column=0)
    cmb_category = ttk.Combobox(f, values=["General","OBC","SC","ST"])
    cmb_category.grid(row=11,column=1)

    ttk.Label(f,text="Nationality").grid(row=12,column=0)
    txt_nationality = ttk.Entry(f); txt_nationality.grid(row=12,column=1)

    ttk.Label(f,text="Status").grid(row=13,column=0)
    cmb_status = ttk.Combobox(f, values=["Active","Dropped","Completed"])
    cmb_status.grid(row=13,column=1)

    ttk.Button(f,text="Save",command=save_student).grid(row=14,column=0,pady=10)
    ttk.Button(f,text="Update",command=update_student).grid(row=14,column=1)

    # ===== TABLE =====
    tree = ttk.Treeview(top,
        columns=("id","fn","ln","gender","dob","age","email",
                 "phone","enroll","course","year","sem",
                 "category","nationality","status"),
        show="headings")

    for col in tree["columns"]:
        tree.heading(col,text=col)

    tree.pack(fill="both",expand=True)

    tree.bind("<ButtonRelease-1>", select_record)

    # ===== BUTTONS =====
    ttk.Button(top,text="Refresh",command=load_data).pack(pady=5)

    # Dashboard button added
    ttk.Button(top,text="Analytics Dashboard",command=analytics_screen).pack(pady=5)

    ttk.Button(top,text="Back",command=top.destroy).pack(pady=5)

    load_data()
    top.mainloop()