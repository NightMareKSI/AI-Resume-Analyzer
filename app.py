import streamlit as st
import pandas as pd

from parser import extract_text_from_pdf
from skills import extract_skills
from bert_matcher import calculate_semantic_similarity
from matcher import find_missing_skills
from recommendation import get_skill_recommendations
from scoring import calculate_skill_match_score, calculate_overall_score
from report_generator import generate_report
from database import (create_database, register_user, login_user, save_history, get_history)

create_database()

# ---------------- LOGIN PAGE UI ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"    

if not st.session_state.logged_in:

    # Page config
    st.set_page_config(
        page_title="AI Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )

    # CSS styling
    st.markdown("""
        <style>

        body {
            background-color: #020617;
        }

        .title {
            text-align: center;
            font-size: 34px;
            font-weight: bold;
            color: white;
        }

        .subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 30px;
        }

        div.stButton > button {
            background: linear-gradient(
                to right,
                #6366f1,
                #22c55e
            );
            color: white;
            border-radius: 10px;
            font-weight: bold;
            width: 100%;
            height: 50px;
            border: none;
        }

        a {
            color: #22c55e;
            font-weight: bold;
        }

        hr {
            border-color: #1e293b;
        }

        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        "<h1 class='title'>Professional Resume Analysis Powered by AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>Get instant feedback on your resume's ATS compatibility and receive personalized recommendations.</p>",
        unsafe_allow_html=True
    )

    st.divider()

    # ---------- LOGIN TAB ----------

    if st.session_state.page == "login":

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.subheader("Login to Your Account")

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.button("🔐 Login")

            if login_button:

                user = login_user(username, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success("Login successful")

                    st.rerun()

                else:

                    st.error("Invalid credentials")

            st.markdown("Don't have an account?")

            if st.button("Register here"):

                st.session_state.page = "register"

                st.rerun()


    # ---------- REGISTER PAGE ----------

    elif st.session_state.page == "register":

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.subheader("Create New Account")

            new_username = st.text_input("Username")

            email = st.text_input("Email Address")

            new_password = st.text_input(
                "Password (min 6 chars)",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            register_button = st.button("Register")

            if register_button:

                if new_password != confirm_password:

                    st.error("Passwords do not match")

                elif len(new_password) < 6:

                    st.error("Password must be at least 6 characters")

                else:

                    register_user(
                        new_username,
                        new_password
                    )

                    st.success("User registered successfully")

            if st.button("Back to Login"):

                st.session_state.page = "login"

                st.rerun()


    # STOP APP BEFORE MAIN CONTENT
    st.stop()


if "logged_in" not in st.session_state:

    st.warning("Please login to continue")

    st.stop()


st.title("📄 AI Resume Analyzer")
st.markdown(
    "Upload your resume and compare it against a job description to get an **ATS-style analysis**."
)

st.divider()


st.sidebar.header("How it works")

st.sidebar.markdown("""
1. Upload your resume  
2. Paste job description  
3. View ATS scores  
4. Download report  
""")

st.sidebar.success("Powered by BERT NLP")


col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

with col2:
    job_description = st.text_area(
        "Paste Job Description"
    )



if uploaded_file and job_description:

    with st.spinner("Analyzing resume..."):

        resume_text = extract_text_from_pdf(uploaded_file)

        resume_skills = extract_skills(resume_text)

        jd_skills = extract_skills(job_description)

        score = calculate_semantic_similarity(
            resume_text,
            job_description
        )

        skill_score = calculate_skill_match_score(
            resume_skills,
            jd_skills
        )

        overall_score = calculate_overall_score(
            score,
            skill_score
        )

        save_history(
    st.session_state.username,
    uploaded_file.name,
    score,
    skill_score,
    overall_score
)

        missing_skills = find_missing_skills(
            resume_skills,
            jd_skills
        )

        recommendations = get_skill_recommendations(
            missing_skills
        )

        report_file = generate_report(
            score,
            skill_score,
            overall_score,
            resume_skills,
            missing_skills,
            recommendations
        )

    st.divider()

    
    st.subheader("📊 ATS Score Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Semantic Match",
        f"{score}%"
    )

    col2.metric(
        "Skill Match",
        f"{skill_score}%"
    )

    col3.metric(
        "Overall ATS Score",
        f"{overall_score}%"
    )

    
    st.markdown("### Score Progress")

    st.progress(int(score))

    st.progress(int(skill_score))

    st.progress(int(overall_score))

    st.divider()

    
    st.subheader("📈 Score Visualization")

    score_data = {
        "Metric": [
            "Semantic Match",
            "Skill Match",
            "Overall ATS"
        ],
        "Score": [
            score,
            skill_score,
            overall_score
        ]
    }

    df = pd.DataFrame(score_data)

    st.bar_chart(
        df.set_index("Metric")
    )

    st.divider()

    
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Your Skills")

        for skill in resume_skills:

            st.success(skill)

    with col2:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:

                st.error(skill)

        else:

            st.success("No missing skills")

    st.divider()

    
    st.subheader("💡 Recommended Skills to Learn")

    if recommendations:

        for skill, description in recommendations.items():

            st.info(
                f"{skill} — {description}"
            )

    else:

        st.success("You already meet the requirements!")

    
    st.success("✨ Analysis complete!")





# We are looking for a Software Engineer with experience in Python, SQL, Docker, AWS, Machine Learning, and Git.
