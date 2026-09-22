import tkinter as tk

# --- Dashboard Imports ---
from AnalyticsScreen import analytics_screen
from AcademicDashboard import academic_dashboard
from AttendanceDashboard import attendance_dashboard
from BehaviorDashboard import behavior_dashboard
from FinancialDashboard import financial_dashboard
from PredictionDashboard import prediction_dashboard
from DataCollectionDashboard import data_collection_dashboard

def master_dashboard(main_container, back_func, create_btn_func):
    # 1. Clear main screen
    for widget in main_container.winfo_children():
        widget.destroy()

    # 2. Define grid items
    dash_items = [
        ("👨‍🎓 STUDENT ANALYTICS", analytics_screen),
        ("📚 ACADEMIC PERFORMANCE", academic_dashboard),
        ("📅 ATTENDANCE TRENDS", attendance_dashboard),
        ("🧠 BEHAVIORAL INSIGHTS", behavior_dashboard),
        ("💰 FINANCIAL STATUS", financial_dashboard),
        ("📈 PREDICTION MODELS", prediction_dashboard),
        ("🗂 DATA REPOSITORY", data_collection_dashboard),
    ]

    # 3. Create Grid (2 Columns for Dashboards)
    r, c = 0, 0
    for text, cmd in dash_items:
        create_btn_func(text, cmd, r, c, 1)
        c += 1
        if c > 1: r += 1; c = 0

    # 4. Back Button (Spanning both columns)
    # Using a red-tinted text for the back button
    back_btn = create_btn_func("⬅ BACK TO MAIN MENU", back_func, r + 1, 0, 2, fg_color="#ef4444")