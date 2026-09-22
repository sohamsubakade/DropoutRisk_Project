import tkinter as tk
from tkinter import messagebox
import time

# --- Your Original Imports ---
import FinancialScreen
from PredictionResults import prediction_screen
from ml_predictor import run_ml_model
from BehaviorScreen import behavior_screen
from DataCollectionScreen import data_collection_screen
from InterventionScreen import intervention_screen
from MainDashboard import master_dashboard  # We will update this call
from AttendanceScreen import attendance_screen

def open_main():
    top = tk.Tk()
    top.title("Dropout Risk Prediction System")

    # ================= COLORS =================
    BG_COLOR = "#f1f5f9"  # Soft Slate Gray
    HEADER_COLOR = "#ffffff"  # Pure White Header
    ACCENT_COLOR = "#000000"  # Bold Black

    # ================= SETTINGS =================
    top.attributes('-fullscreen', True)
    top.configure(bg=BG_COLOR)

    # ================= HEADER =================
    header = tk.Frame(top, bg=HEADER_COLOR, pady=40, highlightbackground="#e2e8f0", highlightthickness=1)
    header.pack(fill="x")

    tk.Label(
        header,
        text="DROPOUT RISK MANAGEMENT SYSTEM",
        bg=HEADER_COLOR,
        fg=ACCENT_COLOR,
        font=("Helvetica", 36, "bold")
    ).pack()

    tk.Frame(header, bg=ACCENT_COLOR, height=4, width=800).pack(pady=10)

    # ================= CLOCK =================
    clock_label = tk.Label(top, font=("Segoe UI", 11, "bold"), bg=HEADER_COLOR, fg=ACCENT_COLOR)
    clock_label.place(relx=0.02, rely=0.03)

    def update_clock():
        current_time = time.strftime('%H:%M:%S\n%A, %b %d')
        clock_label.config(text=current_time)
        top.after(1000, update_clock)

    update_clock()

    # ================= MAIN CONTAINER =================
    # This is the "Stage" where we swap menus
    main_container = tk.Frame(top, bg=BG_COLOR)
    main_container.place(relx=0.5, rely=0.55, anchor="center")

    # ================= NAVIGATION FUNCTIONS =================
    def student_profile():
        from StudentProfileScreen import student_profile_screen
        student_profile_screen()

    def open_academic():
        from AcademicPerformanceScreen import academic_performance_screen
        academic_performance_screen()

    def risk_scoring():
        confirm = messagebox.askyesno("Run Analysis", "Initialize ML Prediction Model?")
        if confirm and run_ml_model():
            messagebox.showinfo("Success", "Risk Analysis Complete.")

    # ================= SHARED STYLING =================
    def on_enter(e):
        e.widget.config(bg=ACCENT_COLOR, fg="#ffffff")

    def on_leave(e):
        # We handle special coloring for the "Back" button text here
        original_fg = e.widget.original_fg if hasattr(e.widget, 'original_fg') else ACCENT_COLOR
        e.widget.config(bg="#ffffff", fg=original_fg)

    def create_btn(text, cmd, row, col, span=1, fg_color="#000000"):
        btn = tk.Button(
            main_container, text=text, command=cmd,
            width=26 if span == 1 else 0, pady=22,
            font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=fg_color,
            border=0, highlightthickness=1, highlightbackground="#cbd5e1",
            cursor="hand2", activebackground="#333333", activeforeground="#ffffff"
        )
        btn.original_fg = fg_color
        btn.grid(row=row, column=col, columnspan=span, padx=12, pady=12, sticky="nsew" if span > 1 else "")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # ================= MENU LOADING LOGIC =================
    def load_main_menu():
        for widget in main_container.winfo_children():
            widget.destroy()

        buttons = [
            ("STUDENT PROFILE", student_profile),
            ("ACADEMIC PERFORMANCE", open_academic),
            ("ATTENDANCE MONITORING", attendance_screen),  # Replace with actual attendance import
            ("DATA COLLECTION", data_collection_screen),
            ("BEHAVIORAL ANALYSIS", behavior_screen),
            ("FINANCIAL ANALYSIS", FinancialScreen.financial_screen),
            ("PREDICTION RESULTS", prediction_screen),
            ("RUN RISK SCORING", risk_scoring),
            ("INTERVENTION STRATEGY", intervention_screen),
        ]

        r, c = 0, 0
        for text, cmd in buttons:
            create_btn(text, cmd, r, c)
            c += 1
            if c > 2: r += 1; c = 0

        # Large Dashboard Button
        dash_btn = create_btn("📊 SYSTEM ANALYTICS DASHBOARD", None, r + 1, 0, 3)
        dash_btn.config(command=lambda: master_dashboard(main_container, load_main_menu, create_btn))

    # Initial Load
    load_main_menu()

    # ================= EXIT =================
    exit_btn = tk.Button(top, text="[ ESC ] CLOSE SYSTEM", command=top.destroy,
                         bg=BG_COLOR, fg="#64748b", font=("Segoe UI", 10, "bold"), relief="flat")
    exit_btn.place(relx=0.98, rely=0.02, anchor="ne")
    top.bind("<Escape>", lambda e: top.attributes("-fullscreen", False))

    top.mainloop()


if __name__ == "__main__":
    open_main()