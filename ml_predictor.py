import sqlite3
import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from database import create_database

# Always ensure DB exists before ML runs
create_database()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dropout_system.db")

# =========================================================
# SAFE NUMBER CONVERTER (TEXT → FLOAT)
# =========================================================
def num(x):
    try:
        return float(x)
    except:
        return 0.0


# =========================================================
# LOAD DATA FROM DATABASE
# =========================================================
def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        s.student_id,

        a.attendance_percentage,
        ap.GPA,
        ap.CGPA,
        ap.failed_subjects,

        f.financial_stress_level,
        f.fee_due,

        e.assignments_missed,
        e.online_activity_score,

        b.stress_level,
        b.motivation_level,

        CASE
            WHEN s.current_status='Dropped' THEN 1
            ELSE 0
        END AS dropout

    FROM student s
    LEFT JOIN attendance a ON s.student_id=a.student_id
    LEFT JOIN academic_performance ap ON s.student_id=ap.student_id
    LEFT JOIN financial_status f ON s.student_id=f.student_id
    LEFT JOIN engagement_metrics e ON s.student_id=e.student_id
    LEFT JOIN behavioral_record b ON s.student_id=b.student_id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert TEXT → numeric
    for col in df.columns:
        if col not in ["student_id", "dropout"]:
            df[col] = df[col].apply(num)

    df = df.fillna(0)
    return df


# =========================================================
# RISK CATEGORY
# =========================================================
def risk_level(score):
    if score < 0.40:
        return "LOW"
    elif score < 0.70:
        return "MEDIUM"
    else:
        return "HIGH"


# =========================================================
# TRAIN + PREDICT MODEL
# =========================================================
def predict_dropout():

    df = load_data()

    # Minimum data check
    if len(df) < 3:
        print("Not enough data for ML training")
        return False

    X = df.drop(["student_id", "dropout"], axis=1)
    y = df["dropout"]

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)

    probabilities = model.predict_proba(X)[:, 1]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Clear previous predictions
    c.execute("DELETE FROM risk_assessment")

    for i, sid in enumerate(df["student_id"]):

        score = float(probabilities[i])
        level = risk_level(score)
        pred = "YES" if score > 0.65 else "NO"

        # Individual factor risk scores
        academic = df.iloc[i]["CGPA"] / 10
        attendance = 1 - (df.iloc[i]["attendance_percentage"] / 100)
        financial = df.iloc[i]["financial_stress_level"] / 10
        behavioral = df.iloc[i]["stress_level"] / 10
        engagement = df.iloc[i]["assignments_missed"] / 10

        # Insert into risk_assessment table (ALL 13 columns)
        c.execute("""
        INSERT INTO risk_assessment(
            student_id,
            academic_risk_score,
            attendance_risk_score,
            financial_risk_score,
            behavioral_risk_score,
            engagement_risk_score,
            overall_risk_score,
            risk_level,
            predicted_dropout,
            model_used,
            confidence_score,
            assessment_date,
            reviewed_by
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            int(sid),
            round(academic, 3),
            round(attendance, 3),
            round(financial, 3),
            round(behavioral, 3),
            round(engagement, 3),
            round(score, 3),
            level,
            pred,
            "RandomForest",
            round(score * 100, 2),
            pd.Timestamp.now().strftime("%Y-%m-%d"),
            "AI Model"
        ))

    conn.commit()
    conn.close()

    print("Prediction completed and stored in database")
    return True


# =========================================================
# FUNCTION CALLED BY TKINTER BUTTON
# =========================================================
def run_ml_model():
    try:
        return predict_dropout()
    except Exception as e:
        print("ML Error:", e)
        return False
