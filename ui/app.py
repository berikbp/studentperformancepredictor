import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Student Score Predictor", layout="centered")

st.title("🎓 Student Performance Predictor")
st.markdown("Predict final Exam Scores based on study habits and environmental factors.")

# API Endpoint (using service name for Docker compatibility later)
API_URL = "http://api:8000/predict" 
# Fallback for local testing outside Docker
LOCAL_API_URL = "http://localhost:8000/predict"

def get_prediction(data):
    try:
        response = requests.post(LOCAL_API_URL, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            # Try the docker URL
            response = requests.post(API_URL, json=data)
            return response.json()
    except Exception as e:
        return {"error": str(e)}

with st.form("student_data_form"):
    st.subheader("Personal & Study Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        hours_studied = st.slider("Hours Studied", 0, 50, 20)
        attendance = st.slider("Attendance %", 0, 100, 80)
        sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
        previous_scores = st.slider("Previous Scores", 0, 100, 70)
        tutoring_sessions = st.number_input("Tutoring Sessions", 0, 10, 0)
        physical_activity = st.slider("Physical Activity (Level)", 0, 6, 3)

    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        parental_involvement = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
        access_to_resources = st.selectbox("Access to Resources", ["Low", "Medium", "High"])
        motivation_level = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
        family_income = st.selectbox("Family Income", ["Low", "Medium", "High"])
        teacher_quality = st.selectbox("Teacher Quality", ["Low", "Medium", "High"])

    st.subheader("Environmental & Lifestyle Factors")
    col3, col4 = st.columns(2)
    with col3:
        extracurricular = st.selectbox("Extracurricular Activities", ["No", "Yes"])
        internet_access = st.selectbox("Internet Access", ["No", "Yes"])
        learning_disabilities = st.selectbox("Learning Disabilities", ["No", "Yes"])
    with col4:
        school_type = st.selectbox("School Type", ["Public", "Private"])
        peer_influence = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
        distance = st.selectbox("Distance from Home", ["Near", "Moderate", "Far"])
        parental_edu = st.selectbox("Parental Education Level", ["High School", "College", "Postgraduate"])

    submit = st.form_submit_button("Predict Exam Score")

if submit:
    payload = {
        "Hours_Studied": hours_studied,
        "Attendance": attendance,
        "Parental_Involvement": parental_involvement,
        "Access_to_Resources": access_to_resources,
        "Extracurricular_Activities": extracurricular,
        "Sleep_Hours": sleep_hours,
        "Previous_Scores": previous_scores,
        "Motivation_Level": motivation_level,
        "Internet_Access": internet_access,
        "Tutoring_Sessions": tutoring_sessions,
        "Family_Income": family_income,
        "Teacher_Quality": teacher_quality,
        "School_Type": school_type,
        "Peer_Influence": peer_influence,
        "Physical_Activity": physical_activity,
        "Learning_Disabilities": learning_disabilities,
        "Parental_Education_Level": parental_edu,
        "Distance_from_Home": distance,
        "Gender": gender
    }
    
    with st.spinner("Calculating prediction..."):
        result = get_prediction(payload)
    
    if "prediction" in result:
        st.success(f"### Predicted Exam Score: {result['prediction']:.2f}")
    else:
        st.error(f"Error: {result.get('detail', 'Could not connect to backend')}")
