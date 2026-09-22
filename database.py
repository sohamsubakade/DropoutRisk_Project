import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dropout_system.db")


def create_database():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ================ STUDENT TABLE ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS student(
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,

        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        date_of_birth TEXT,
        age TEXT,

        email TEXT,
        phone_number TEXT,
        enrollment_date TEXT,

        course_id TEXT,
        academic_year TEXT,
        semester TEXT,

        category TEXT,
        nationality TEXT,

        current_status TEXT
    )
    """)

    # ================ COURSE TABLE ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS course(
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        department TEXT,
        duration TEXT,
        total_credits TEXT,
        course_level TEXT,
        admission_criteria TEXT,
        course_fee TEXT,
        delivery_mode TEXT,
        syllabus_version TEXT,
        start_date TEXT,
        end_date TEXT,
        intake_capacity TEXT,
        accreditation TEXT
    )
    """)

    # ================ ACADEMIC PERFOeRMANCE ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS academic_performance(
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        semester TEXT,
        GPA TEXT,
        CGPA TEXT,
        total_credits_registered TEXT,
        credits_earned TEXT,
        failed_subjects TEXT,
        attendance_percentage TEXT,
        internal_marks TEXT,
        external_marks TEXT,
        class_rank TEXT,
        improvement_status TEXT,
        academic_warning TEXT,
        evaluation_date TEXT
    )
    """)

    # ================ ATTENDANCE ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        course_id TEXT,
        semester TEXT,
        total_classes TEXT,
        classes_attended TEXT,
        attendance_percentage TEXT,
        late_attendance TEXT,
        medical_leave_days TEXT,
        unauthorized_absence TEXT,
        attendance_status TEXT,
        last_updated TEXT,
        attendance_trend TEXT,
        flagged TEXT
    )
    """)

    # ================ BEHAVIORAL RECORD ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS behavioral_record(
        behavior_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        disciplinary_actions TEXT,
        counseling_sessions TEXT,
        classroom_participation TEXT,
        peer_interaction_score TEXT,
        teacher_feedback TEXT,
        motivation_level TEXT,
        stress_level TEXT,
        extracurricular_participation TEXT,
        leadership_roles TEXT,
        punctuality_score TEXT,
        behavior_rating TEXT,
        recorded_date TEXT
    )
    """)

    # ================ FINANCIAL STATUS ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS financial_status(
        financial_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        family_income TEXT,
        fee_paid TEXT,
        fee_due TEXT,
        scholarship TEXT,
        scholarship_type TEXT,
        loan_taken TEXT,
        financial_aid_amount TEXT,
        payment_history TEXT,
        financial_stress_level TEXT,
        late_payments TEXT,
        sponsor_details TEXT,
        last_payment_date TEXT
    )
    """)

    # ================ ENGAGEMENT METRICS ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS engagement_metrics(
        engagement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        LMS_login_frequency TEXT,
        assignments_submitted TEXT,
        assignments_missed TEXT,
        quiz_participation TEXT,
        online_activity_score TEXT,
        discussion_forum_posts TEXT,
        video_lecture_completion TEXT,
        library_usage TEXT,
        project_submissions TEXT,
        engagement_level TEXT,
        trend TEXT,
        last_updated TEXT
    )
    """)

    # ================ RISK ASSESSMENT ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS risk_assessment(
        risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        academic_risk_score TEXT,
        attendance_risk_score TEXT,
        financial_risk_score TEXT,
        behavioral_risk_score TEXT,
        engagement_risk_score TEXT,
        overall_risk_score TEXT,
        risk_level TEXT,
        predicted_dropout TEXT,
        model_used TEXT,
        confidence_score TEXT,
        assessment_date TEXT,
        reviewed_by TEXT
    )
    """)

    # ================ INTERVENTION ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS intervention(
        intervention_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        risk_id TEXT,
        intervention_type TEXT,
        assigned_staff TEXT,
        intervention_start_date TEXT,
        intervention_end_date TEXT,
        follow_up_required TEXT,
        progress_status TEXT,
        outcome TEXT,
        notes TEXT,
        effectiveness_score TEXT,
        communication_mode TEXT,
        last_updated TEXT
    )
    """)

    # ================ SYSTEM ANALYTICS ================
    c.execute("""
    CREATE TABLE IF NOT EXISTS system_analytics(
        analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
        academic_year TEXT,
        total_students TEXT,
        dropout_count TEXT,
        dropout_rate TEXT,
        high_risk_students TEXT,
        medium_risk_students TEXT,
        low_risk_students TEXT,
        model_accuracy TEXT,
        precision TEXT,
        recall TEXT,
        f1_score TEXT,
        most_common_risk_factor TEXT,
        intervention_success_rate TEXT,
        generated_date TEXT
    )
    """)

    conn.commit()
    conn.close()



# Run directly
if __name__ == "__main__":
    create_database()
