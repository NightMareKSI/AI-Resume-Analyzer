"""
AI Resume Analyzer - Production Edition
Advanced AI-powered resume analysis tool with professional UI/UX
"""

import streamlit as st
import pandas as pd
import numpy as np
#import seaborn as sns
import os


def load_css():
    css_path = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "style.css"
    )

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    else:
        st.warning("CSS file not found: assets/style.css")


from datetime import datetime
import io

# Core modules
from parser import extract_text_from_pdf
from skills import extract_skills
from bert_matcher import calculate_semantic_similarity
from matcher import find_missing_skills
from recommendation import get_skill_recommendations
from skills_database import SKILLS_DATABASE, get_all_skills
from utils import get_skill_info

# Enhanced modules
from scoring_advanced import ATSScorer
from visualization import VisualizationEngine, render_score_summary, render_score_breakdown
from section_analyzer import ResumeSectionAnalyzer
from database_enhanced import DatabaseManager
from comparison_engine import ResumeComparisonEngine


# ============================================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "AI-Powered Resume Analyzer built with ❤️"
    }
)
load_css()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "session_token" not in st.session_state:
    st.session_state.session_token = None

# Initialize database
db = DatabaseManager()
scorer = ATSScorer()


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def show_login_page():
    """Display login and registration interface"""
    
    query_params = st.query_params

    if query_params.get("page") == "register":
        st.session_state.page = "register"

    if query_params.get("page") == "login":
        st.session_state.page = "login"


    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("""
        # 📄 AI Resume Analyzer Pro

        ### Professional Resume Analysis Powered by AI
        """)

        st.divider()

        # ---------- LOGIN PAGE ----------

        if st.session_state.page == "login":

            st.subheader("Login to Your Account")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            login_button = st.button(
                "🔐 Login",
                use_container_width=True
            )

            if login_button:

                success, user_data, message = db.login_user(
                    username,
                    password
                )

                if success:

                    st.session_state.logged_in = True
                    st.session_state.username = user_data["username"]
                    st.session_state.user_id = user_data["id"]

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

            st.markdown(
                """
                <span style="color:white;">
                    Don't have an account?
                </span>
                <a href="?page=register" style="
                    color: yellow;
                    font-weight: bold;
                    text-decoration: none;
                    margin-left: 6px;
                    cursor: pointer;
                ">
                    Register here
                </a>
                """,
                unsafe_allow_html=True
            )

        # ---------- REGISTER PAGE ----------

        elif st.session_state.page == "register":

            st.subheader("Create New Account")

            new_username = st.text_input(
                "Username",
                key="register_username"
            )

            email = st.text_input(
                "Email Address",
                key="register_email"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password"
            )

            register_button = st.button(
                "Register",
                use_container_width=True
            )

            if register_button:

                if new_password != confirm_password:

                    st.error("Passwords do not match")

                elif len(new_password) < 6:

                    st.error("Password must be at least 6 characters")

                else:

                    success, message = db.register_user(
                        new_username,
                        email,
                        new_password
                    )

                    if success:

                        st.success(message)

                    else:

                        st.error(message)

            st.markdown(
                """
                <a href="?page=login" style="
                    color: yellow;
                    font-weight: bold;
                    text-decoration: none;
                    cursor: pointer;
                ">
                    Back to Login
                </a>
                """,
                unsafe_allow_html=True
            )

        st.stop()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def show_main_app():
    """Display main application interface"""
    
    # Header with user info
    col_logo, col_title, col_logout = st.columns([1, 6, 1])
    
    with col_logo:
        st.image(
        "assets/logo.png",
        width=60
    )

    with col_title:
        st.markdown(
            """
            <h1 style="
                text-align:left;
                font-size:34px;
                font-weight:700;
                color:white;
                margin-top:10px;
            ">
                AI Resume Analyzer 🚀
            </h1>
            """,
            unsafe_allow_html=True
    )
    
    with col_logout:
        if st.button("🚪 Logout", use_container_width=True):
            db.logout_user(st.session_state.session_token)
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    st.markdown(f"Welcome, **{st.session_state.username}**! 👋")
    st.divider()
    
    dark_mode = st.sidebar.toggle(
        "Dark Mode",
        value=True
    )

    st.markdown(
    """
    <div style="
        background: linear-gradient(
            90deg,
            #6366f1,
            #22c55e
        );
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
    ">
        Upload your resume and get your ATS score instantly ⚡
    </div>
    """,
    unsafe_allow_html=True
)


    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🔍 Resume Analysis",
        "📈 Compare Resumes",
        "📚 History",
        "⚙️ Settings"
    ])
    
    # ========================================================================
    # TAB 1: DASHBOARD
    # ========================================================================
    with tab1:
        show_dashboard()
    
    # ========================================================================
    # TAB 2: RESUME ANALYSIS
    # ========================================================================
    with tab2:
        show_resume_analysis()
    
    # ========================================================================
    # TAB 3: COMPARE RESUMES
    # ========================================================================
    with tab3:
        show_comparison()
    
    # ========================================================================
    # TAB 4: HISTORY
    # ========================================================================
    with tab4:
        show_history()
    
    # ========================================================================
    # TAB 5: SETTINGS
    # ========================================================================
    with tab5:
        show_settings()

    st.markdown(
        "AI Resume Analyzer • Built with Python & Streamlit GitHub Portfolio Project"
    )


def show_dashboard():
    """Display user dashboard with recent analysis"""
    
    st.subheader("📊 Your Dashboard")
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #6366f1, #22c55e);
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            color: white;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 25px;
        ">
        🚀 AI Resume Analyzer — Get Your ATS Score in Seconds
        </div>
        """, unsafe_allow_html=True)

    # Get user's recent analyses
    history = db.get_user_history(st.session_state.user_id, limit=1000)
    
    if history:
        col1, col2, col3, col4 = st.columns(4)

        avg_score = sum(h['overall_score'] for h in history) / len(history) if history else 0
        best_score = max((h['overall_score'] for h in history), default=0)

        with col1:
            st.metric(
                "Resumes Analyzed",
                len(history)
            )

        with col2:
            st.metric(
                "Average ATS Score",
                f"{avg_score:.1f}%"
            )

        with col3:
            st.metric(
                "Best Score",
                f"{best_score:.1f}%"
            )

        with col4:
            st.metric(
                "Success Rate",
                "92%"
            )
        
        st.divider()
        
        # Recent analyses table
        st.subheader("📋 Recent Analyses")
        
        recent_df = pd.DataFrame([
            {
                'Resume': h['resume_filename'],
                'Overall Score': f"{h['overall_score']:.1f}%",
                'Skills Match': f"{h['skill_score']:.1f}%",
                'Date': h['created_at'].split()[0]
            }
            for h in history[:5]
        ])
        
        st.dataframe(recent_df, use_container_width=True)
        
        import plotly.express as px
        st.divider()
        st.subheader("📈 ATS Score Trend")
        scores = [h["overall_score"] for h in history]
        fig = px.line(
            y=scores,
            title="ATS Score Progress Over Time",
            markers=True
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()
        st.markdown("""
        ### 🚀 Features

        ✅ AI-Powered Resume Analysis  
        ✅ ATS Score Prediction  
        ✅ Skill Gap Detection  
        ✅ Resume Comparison Engine  
        ✅ PDF Report Generator  
        ✅ User Authentication  
        """)

        st.markdown("""
        ### 🛠 Tech Stack

        Python  
        Streamlit  
        NLP (BERT)  
        Machine Learning  
        SQLite Database  
        Plotly Visualization  
        """)



    else:
        st.info("👋 Welcome! Start by analyzing your first resume in the 'Resume Analysis' tab.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ✨ Key Features
            
            - **ATS Score**: Get instant ATS compatibility score
            - **Section Analysis**: Detailed feedback on each resume section
            - **Keyword Match**: See how well your resume matches the job
            - **Recommendations**: Get specific suggestions to improve
            - **PDF Reports**: Download detailed analysis reports
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 How It Works
            
            1. Upload your resume (PDF)
            2. Paste job description
            3. Get instant AI-powered analysis
            4. Receive personalized recommendations
            5. Download your report
            
            ### 💡 Pro Tips
            
            - Use the comparison feature to optimize multiple resumes
            - Track your progress over time
            - Follow the specific recommendations
            - Keep your history for reference
            """)


def show_resume_analysis():
    """Display resume analysis interface"""
    
    st.subheader("🔍 Resume Analysis")
    job_role = st.selectbox(
        "Select Target Job Role",
        [
            "Software Developer",
            "Data Scientist",
            "Web Developer",
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Analyst"
        ]
    )


    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            key="resume_upload"
        )
    
    with col2:
        st.markdown("### 📋 Job Description")
        job_description = st.text_area(
            "Paste the job description or requirements",
            height=150,
            placeholder="Paste job requirements and description here..."
        )
    
    if uploaded_file and job_description:
        with st.spinner("🚀 Analyzing your resume... Please wait"):
            try:
                # Extract text from PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                

                resume_skills = [
                    s.strip().lower()
                    for s in extract_skills(resume_text)
                ]

                jd_skills = [
                    s.strip().lower()
                    for s in extract_skills(job_description)
                ]


                matched_skills = list(
                    set(resume_skills).intersection(set(jd_skills))
                )

                role_missing_skills = list(
                    set(jd_skills) - set(resume_skills)
                )

                
                # Calculate scores using advanced scoring
                semantic_match = calculate_semantic_similarity(resume_text, job_description)
                if len(jd_skills) > 0:

                    skill_match = (
                        len(matched_skills) / len(jd_skills)
                    ) * 100

                else:

                    skill_match = 0
                keyword_score = scorer.calculate_keyword_density_score(resume_text, job_description)
                experience_score = scorer.calculate_experience_relevance(resume_text)
                education_score = scorer.calculate_education_relevance(resume_text, job_description)
                formatting_score = scorer.calculate_formatting_score(resume_text)
                
                # Calculate overall ATS score
                overall_score, components = scorer.calculate_overall_score(
                    semantic_match,
                    skill_match,
                    keyword_score,
                    experience_score,
                    education_score,
                    formatting_score
                )
                
                # Get detailed feedback
                feedback = scorer.generate_detailed_feedback(components, {})
                
                # Find missing skills
                jd_missing_skills = list(
                    set(jd_skills) - set(resume_skills)
                )
                


                # Get recommendations
                recommendations = get_skill_recommendations(jd_missing_skills)
                
                # Analyze sections
                section_analyses = ResumeSectionAnalyzer.analyze_all_sections(
                    resume_text,
                    job_description
                )
                
                # Save analysis to database
                db.save_analysis(
                    st.session_state.user_id,
                    uploaded_file.name,
                    resume_text,
                    job_description,
                    components,
                    resume_skills,
                    role_missing_skills
                )
                
                # Display results
                st.divider()
                st.success("✅ Analysis Complete!")
                

                st.subheader("ATS Skill Match Score")
                st.progress(skill_match / 100)
                st.write(f"Score: {int(skill_match)}%")


                # Main score visualization
                st.markdown("## 🎯 Overall ATS Score")
                render_score_summary(overall_score, components)
                
                st.divider()
                
                # Component breakdown
                render_score_breakdown(components)
                
                st.divider()
                
                # Skills analysis
                st.markdown("## 💼 Skills Analysis")

                matched = list(
                    set(resume_skills).intersection(set(jd_skills))
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Matched Skills", len(matched))
                
                with col2:
                    st.metric("Missing Skills", len(role_missing_skills))
                
                with col3:
                    match_percentage = min(
                        (len(matched) / max(len(jd_skills), 1)) * 100,
                        100
                    )
                    st.metric("Requirement Coverage", f"{match_percentage:.0f}%")
                
                # Matched and missing skills
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ✅ Matched Skills")

                    if matched:
                        for skill in matched:
                            st.success(f"✓ {skill}")
                    else:
                        st.info("No directly matched skills found")
                
                with col2:
                    st.markdown("### ⚠️ Missing Skills")
                    if jd_missing_skills:
                        for skill in jd_missing_skills[:10]:
                            info = get_skill_info(skill)

                            st.warning(
                                f"{skill} — {info['description']}"
                            )
                        if len(jd_missing_skills) > 10:
                            st.info(f"... and {len(jd_missing_skills) - 10} more")
                    else:
                        st.success("All required skills covered!")
                
                st.divider()
                
                # Section analysis
                st.markdown("## 📑 Section-by-Section Analysis")
                
                section_tabs = st.tabs(list(section_analyses.keys()))
                
                for tab, (section_name, section_score) in zip(section_tabs, section_analyses.items()):
                    with tab:
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            level, color = VisualizationEngine.get_score_level(section_score.score)
                            st.markdown(f"""
                            <div style="text-align: center; padding: 20px; background-color: {color}20; border-radius: 10px;">
                                <h1 style="color: {color}; margin: 0;">{section_score.score:.0f}</h1>
                                <p style="color: {color}; margin: 0; font-weight: bold;">{level}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if section_score.strengths:
                                st.markdown("#### ✅ Strengths")
                                for strength in section_score.strengths:
                                    st.success(strength)
                            
                            if section_score.weaknesses:
                                st.markdown("#### ⚠️ Weaknesses")
                                for weakness in section_score.weaknesses:
                                    st.error(weakness)
                            
                            if section_score.suggestions:
                                st.markdown("#### 💡 Suggestions")
                                for suggestion in section_score.suggestions:
                                    st.info(suggestion)
                
                st.divider()
                
                # Strengths and weaknesses
                st.markdown("## 🏆 Overall Feedback")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💪 Key Strengths")
                    if feedback['strengths']:
                        for strength in feedback['strengths']:
                            st.success(strength)
                    else:
                        st.info("Keep working on improvements")
                
                with col2:
                    st.markdown("### 🎯 Areas for Improvement")
                    if feedback['weaknesses']:
                        for weakness in feedback['weaknesses']:
                            st.warning(weakness)
                    if feedback['improvements']:
                        st.markdown("**Suggestions:**")
                        for improvement in feedback['improvements']:
                            st.markdown(improvement)
                
                st.divider()
                
                # Recommendations
                st.markdown("## 📚 Skill Recommendations")

                if jd_missing_skills:

                    for skill in jd_missing_skills:

                        info = get_skill_info(skill)

                        st.markdown(f"### {skill}")

                        st.write(f"Category: {info['category']}")

                        st.write(f"Description: {info['description']}")

                        st.write(f"Demand Level: {info['demand_level']}")

                        st.divider()

                else:

                    st.success("No additional skills recommended")
                
                
            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")
    
    else:
        if not uploaded_file:
            st.info("👆 Upload your resume to get started")
        if not job_description:
            st.info("👆 Enter the job description for accurate matching")


def show_comparison():
    """Display resume comparison interface"""

    st.subheader("📈 Compare Resumes")

    st.info("Upload multiple resumes from your computer to compare them")

    st.markdown("### Select Target Job Role")

    job_role = st.selectbox(
        "Choose Engineering Role",
        [
            "Software Developer",
            "Data Scientist",
            "Web Developer",
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Analyst"
        ],
        key="compare_role"
    )

    st.markdown("### Job Description")

    job_description = st.text_area(
        "Paste job description for comparison",
        height=150,
        key="compare_jd"
    )

    # Browse resumes from File Explorer
    uploaded_resumes = st.file_uploader(
        "Browse and select multiple resumes",
        type=["pdf"],
        accept_multiple_files=True,
        key="compare_resumes_uploader"
    )

    if uploaded_resumes:

        st.success(
            f"{len(uploaded_resumes)} resume(s) uploaded successfully"
        )

        resume_names = [
            file.name for file in uploaded_resumes
        ]

        selected_resumes = st.multiselect(
            "Select resumes to compare",
            resume_names,
            max_selections=3,
            key="compare_select_box"
        )

        if len(selected_resumes) >= 2:

            st.markdown("### Selected Resumes")

            selected_files = [
                file for file in uploaded_resumes
                if file.name in selected_resumes
            ]

            comparison_results = []

            for file in selected_files:

                resume_text = extract_text_from_pdf(file)

                resume_skills = [
                    s.strip().lower()
                    for s in extract_skills(resume_text)
                ]

                jd_skills = [
                    s.strip().lower()
                    for s in extract_skills(job_description)
                ]

                semantic_match = calculate_semantic_similarity(
                    resume_text,
                    job_description
                )

                matched_skills = list(
                    set(resume_skills).intersection(set(jd_skills))
                )
                if len(jd_skills) > 0:

                    skill_match = (
                        len(matched_skills) / len(jd_skills)
                    ) * 100

                else:

                    skill_match = 0

                keyword_score = scorer.calculate_keyword_density_score(
                    resume_text,
                    job_description
                )

                experience_score = scorer.calculate_experience_relevance(
                    resume_text
                )

                education_score = scorer.calculate_education_relevance(
                    resume_text,
                    job_description
                )

                formatting_score = scorer.calculate_formatting_score(
                    resume_text
                )

                overall_score, components = scorer.calculate_overall_score(
                    semantic_match,
                    skill_match,
                    keyword_score,
                    experience_score,
                    education_score,
                    formatting_score
                )

                

                comparison_results.append({
                    "Resume": file.name,
                    "Overall ATS Score": round(overall_score, 2),
                    "Skill Match": round(skill_match, 2),
                    "Semantic Match": round(semantic_match, 2),
                    "Keyword Score": round(keyword_score, 2),
                    "Experience Score": round(experience_score, 2),
                    "Education Score": round(education_score, 2),
                    "Formatting Score": round(formatting_score, 2)
                })

            comparison_df = pd.DataFrame(
                comparison_results
            )

            st.markdown("### 📊 Comparison Table")

            st.dataframe(
                comparison_df,
                use_container_width=True
            )
            st.markdown("## Score Component Breakdown Comparison")

            breakdown_df = comparison_df.set_index("Resume")

            st.bar_chart(breakdown_df)

        else:
            st.warning(
            "Please select at least 2 resumes to compare"
            )



def show_history():
    """Display analysis history"""
    
    st.subheader("📚 Analysis History")
    
    # Get user's analysis history
    history = db.get_user_history(st.session_state.user_id, limit=100)
    
    if not history:
        st.info("No analyses yet. Start by analyzing your first resume!")
    else:
        # Display history table
        history_df = pd.DataFrame([
            {
                'Resume': h['resume_filename'],
                'Date': h['created_at'].split()[0],
                'Time': h['created_at'].split()[1],
                'Overall Score': f"{h['overall_score']:.1f}%",
                'Semantic': f"{h['semantic_score']:.1f}%",
                'Skills': f"{h['skill_score']:.1f}%",
                'ID': h['id']
            }
            for h in history
        ])
        
        # Add delete option
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.dataframe(history_df, use_container_width=True)
        
        with col2:
            st.write("**Actions**")
            selected_id = st.selectbox(
                "Select entry to delete",
                [h['id'] for h in history],
                format_func=lambda x: f"ID: {x}"
            )
            
            if st.button("🗑️ Delete", use_container_width=True):
                success, message = db.delete_analysis(selected_id, st.session_state.user_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def show_settings():
    """Display user settings"""
    
    st.subheader("⚙️ Settings")
    
    # Get current settings
    settings = db.get_user_settings(st.session_state.user_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Appearance")
        
        theme = st.radio(
            "Theme",
            ["Light", "Dark"],
            index=0 if (settings and settings.get('theme') == 'light') else 1
        )
    
    with col2:
        st.markdown("### 🔔 Notifications")
        
        notifications = st.toggle(
            "Enable notifications",
            value=True if (settings and settings.get('notifications_enabled')) else False
        )
    
    st.markdown("### 🔐 Privacy")
    
    privacy_level = st.select_slider(
        "Privacy Level",
        options=["Public", "Private", "Friends Only"],
        value="Private"
    )
    
    if st.button("💾 Save Settings", use_container_width=True):
        updates = {
            'theme': theme.lower(),
            'notifications_enabled': 1 if notifications else 0,
            'privacy_level': privacy_level
        }
        
        success, message = db.update_user_settings(st.session_state.user_id, updates)
        
        if success:
            st.success("✅ Settings saved successfully!")
        else:
            st.error(f"❌ Error: {message}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def apply_theme():
    if True:

        st.markdown("""
<style>
body {
    background-color: #020617;
    color: white;
}

.stApp {
    background-color: #020617;
}

section[data-testid="stSidebar"] {
    display: none;
}

.stButton>button {
    background-color: #6366f1;
    color: white;
    border-radius: 8px;
}

/* THIS IS THE NEW RULE — ADD HERE */

button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: none !important;
    color: yellow !important;
    font-weight: bold !important;
    padding: 0 !important;
}

</style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point"""
    
    apply_theme()

    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #1f77b4;
    }
    
    .st-emotion-cache-1q8dd3e {
        padding: 2rem 1rem 10rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_main_app()

def load_js():
    js_path = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "script.js"
    )

    if os.path.exists(js_path):
        with open(js_path) as f:
            st.markdown(
                f"<script>{f.read()}</script>",
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
    load_js()