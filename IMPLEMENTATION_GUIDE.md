# Implementation Guide - Integration & Customization

## 🔧 How to Integrate New Modules

### Quick Integration into Your Code

If you want to keep using the original `app.py` but incorporate new features:

#### 1. Add Advanced Scoring

**Before:**
```python
from scoring import calculate_overall_score

overall_score = calculate_overall_score(semantic_score, skill_score)
```

**After:**
```python
from scoring_advanced import ATSScorer

scorer = ATSScorer()

# Calculate individual components
keyword_score = scorer.calculate_keyword_density_score(resume_text, job_description)
experience_score = scorer.calculate_experience_relevance(resume_text)
education_score = scorer.calculate_education_relevance(resume_text, job_description)
formatting_score = scorer.calculate_formatting_score(resume_text)

# Calculate overall with all components
overall_score, components = scorer.calculate_overall_score(
    semantic_score,
    skill_score,
    keyword_score,
    experience_score,
    education_score,
    formatting_score
)

# Get detailed feedback
feedback = scorer.generate_detailed_feedback(components, {})
```

#### 2. Add Professional Visualizations

**Before:**
```python
col1, col2, col3 = st.columns(3)
col1.metric("Semantic Match", f"{score}%")
col2.metric("Skill Match", f"{skill_score}%")
col3.metric("Overall ATS Score", f"{overall_score}%")

st.progress(int(overall_score))
```

**After:**
```python
from visualization import VisualizationEngine, render_score_summary, render_score_breakdown

# Create gauge chart
fig_gauge = VisualizationEngine.create_gauge_chart(overall_score, "ATS Score")
st.plotly_chart(fig_gauge, use_container_width=True)

# Create radar chart for components
fig_radar = VisualizationEngine.create_radar_chart(components)
st.plotly_chart(fig_radar, use_container_width=True)

# Render professional summary
render_score_summary(overall_score, components)
render_score_breakdown(components)
```

#### 3. Add Section Analysis

**Before:**
```python
# No section-by-section feedback
```

**After:**
```python
from section_analyzer import ResumeSectionAnalyzer

# Analyze all sections
sections = ResumeSectionAnalyzer.analyze_all_sections(resume_text, job_description)

# Display feedback
for section_name, section_score in sections.items():
    st.subheader(f"{section_name}: {section_score.score:.0f}%")
    
    for strength in section_score.strengths:
        st.success(f"✓ {strength}")
    
    for weakness in section_score.weaknesses:
        st.error(f"✗ {weakness}")
    
    for suggestion in section_score.suggestions:
        st.info(f"→ {suggestion}")
```

#### 4. Add Secure Database

**Before:**
```python
from database import register_user, login_user, save_history, get_history

# Plain password (INSECURE)
register_user(username, password)
user = login_user(username, password)
```

**After:**
```python
from database_enhanced import DatabaseManager

# Secure password hashing
db = DatabaseManager()

# Register with email validation
success, message = db.register_user(username, email, password)

# Login returns session token
success, user_data, message = db.login_user(username, password)

# Save analysis with full component scores
success, message, analysis_id = db.save_analysis(
    user_id,
    resume_filename,
    resume_text,
    job_description,
    scores,
    matched_skills,
    missing_skills
)

# Logout properly
db.logout_user(session_token)
```

#### 5. Add Resume Comparison

**Before:**
```python
# Compare just overall scores manually
```

**After:**
```python
from comparison_engine import ResumeComparisonEngine

# Compare multiple analyses
analyses = [analysis1, analysis2, analysis3]
comparison = ResumeComparisonEngine.compare_resumes(analyses)

# Rank resumes
ranked = ResumeComparisonEngine.rank_resumes(analyses)

# Get improvement plan
plan = ResumeComparisonEngine.generate_improvement_plan(comparison, target_resume='best_resume')

# Compare against job
job_comparison = ResumeComparisonEngine.compare_against_job_description(
    resumes,
    job_description
)
```

## 📝 Customization Guide

### 1. Adjust Scoring Weights

In `scoring_advanced.py`:
```python
class ATSScorer:
    def __init__(self):
        # Modify these weights for your use case
        self.weights = {
            'semantic_match': 0.30,      # Original: 0.30
            'skill_match': 0.25,          # Original: 0.25
            'keyword_optimization': 0.15, # Original: 0.15
            'experience_relevance': 0.15, # Original: 0.15
            'education_relevance': 0.10,  # Original: 0.10
            'formatting_structure': 0.05  # Original: 0.05
        }

# Example: Emphasize skills more for tech roles
weights = {
    'semantic_match': 0.25,      # Reduced
    'skill_match': 0.35,          # Increased
    'keyword_optimization': 0.15,
    'experience_relevance': 0.15,
    'education_relevance': 0.05,  # Reduced
    'formatting_structure': 0.05
}
```

### 2. Add Custom Skills

In `skills_list.txt`, add your own skills:
```
# Add lines like:
kubernetes
terraform
datadog
jenkins
helm
prometheus
grafana
elasticsearch
```

### 3. Customize Color Scheme

In `visualization.py`:
```python
class VisualizationEngine:
    COLOR_SCHEME = {
        'excellent': '#10B981',  # Change green to your color
        'good': '#3B82F6',       # Change blue
        'average': '#F59E0B',    # Change yellow
        'poor': '#EF4444'        # Change red
    }

# Example for a tech company branding
COLOR_SCHEME = {
    'excellent': '#00D084',  # LinkedIn green
    'good': '#0A66C2',       # LinkedIn blue
    'average': '#FA7921',    # Custom orange
    'poor': '#E74C3C'        # Red
}
```

### 4. Modify Scoring Thresholds

In `visualization.py`:
```python
SCORE_LEVELS = {
    (0, 40): ('Poor', '#EF4444'),
    (40, 70): ('Average', '#F59E0B'),
    (70, 100): ('Excellent', '#10B981')
}

# Example: More stringent criteria
SCORE_LEVELS = {
    (0, 50): ('Needs Work', '#EF4444'),
    (50, 75): ('Good', '#F59E0B'),
    (75, 90): ('Excellent', '#10B981'),
    (90, 100): ('Outstanding', '#8B5CF6')
}
```

### 5. Add Custom Section Types

In `section_analyzer.py`:
```python
class ResumeSectionAnalyzer:
    SECTION_PATTERNS = {
        'contact': r'(email|phone|linkedin|github|portfolio)',
        'summary': r'(professional summary|objective|profile)',
        'experience': r'(experience|employment|worked at)',
        
        # Add custom sections:
        'publications': r'(publications|published|paper|conference)',
        'awards': r'(awards|recognition|honors)',
        'languages': r'(languages|fluent|proficiency)',
    }

    @staticmethod
    def analyze_publications(resume_text):
        # Your custom analysis logic
        pass
```

### 6. Customize Recommendation Engine

In `recommendation.py`:
```python
def get_skill_recommendations(missing_skills):
    recommendations = {
        # Existing recommendations...
        
        # Add custom recommendations:
        "aws": "Master AWS services for cloud-native development",
        "kubernetes": "Learn container orchestration at scale",
        "terraform": "Master infrastructure as code",
    }
    
    return recommendations
```

## 🎨 UI Customization

### Change App Logo and Title

In `app_production.py`:
```python
st.set_page_config(
    page_title="Your Company AI Resume Analyzer",  # Change this
    page_icon="🚀",  # Change emoji
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("# 🚀 Your Company Resume Analysis Platform")  # Change this
```

### Add Company Branding

In `app_production.py`, at the start of `show_main_app()`:
```python
# Add company logo
col1, col2 = st.columns([1, 3])
with col1:
    st.image("company_logo.png", width=50)
with col2:
    st.markdown("# Your Company | AI Resume Analyzer")

# Add company info
st.markdown("""
    Powered by Your Company's AI hiring platform
    [Website](https://yourcompany.com) | [Contact Us](mailto:support@yourcompany.com)
""")
```

### Customize Colors

In `app_production.py`:
```python
st.markdown("""
    <style>
    .stButton > button {
        background-color: #Your_Color;
        color: white;
    }
    .stMetric {
        background-color: #Your_Brand_Color_Light;
        border-left: 4px solid #Your_Brand_Color;
    }
    </style>
""", unsafe_allow_html=True)
```

## 🔌 Integration Points

### 1. With ATS Systems

```python
# Export scores in ATS format
def export_to_ats_format(analysis_result):
    return {
        'candidate_id': analysis_result['user_id'],
        'resume_score': analysis_result['overall_score'],
        'skills_matched': len(analysis_result['matched_skills']),
        'skills_missing': len(analysis_result['missing_skills']),
        'timestamp': analysis_result['created_at']
    }

# Import job requirements
def import_from_ats_job(job_data):
    return {
        'title': job_data['position'],
        'description': job_data['description'],
        'required_skills': job_data['required_skills']
    }
```

### 2. With Email Systems

```python
# Send analysis report via email
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def email_report(email, analysis_result, report_file):
    msg = MIMEMultipart()
    msg['To'] = email
    msg['Subject'] = f"Resume Analysis Report - {analysis_result['overall_score']:.0f}%"
    
    with open(report_file, 'rb') as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header('Content-Disposition', 'attachment', filename=report_file)
        msg.attach(part)
    
    # Send via your email provider
    return send_email(msg)
```

### 3. With Analytics

```python
# Track analytics
def log_analytics(user_id, analysis_result, action):
    analytics_event = {
        'user_id': user_id,
        'event': action,
        'score': analysis_result['overall_score'],
        'timestamp': datetime.now().isoformat(),
        'metadata': analysis_result
    }
    
    # Send to your analytics service (Mixpanel, Segment, etc.)
    analytics_client.track(analytics_event)
```

## 🧪 Testing Guide

### Test Individual Modules

```python
# Test scoring
from scoring_advanced import ATSScorer

scorer = ATSScorer()
test_resume = "Python, 5 years experience, led team..."
test_jd = "Looking for Python expert with team lead experience"

score, components = scorer.calculate_overall_score(
    semantic_match=85,
    skill_match=90,
    keyword_score=75,
    experience_relevance=80,
    education_relevance=70,
    formatting_score=80
)

print(f"Overall Score: {score}")
assert score > 70, "Score should be > 70"

# Test with real data
print("\nTesting all components:")
for component, value in components.items():
    print(f"  {component}: {value}%")
```

### Test Section Analysis

```python
from section_analyzer import ResumeSectionAnalyzer

resume_text = open("sample_resume.txt").read()
sections = ResumeSectionAnalyzer.analyze_all_sections(resume_text)

for section_name, section_score in sections.items():
    print(f"{section_name}: {section_score.score}%")
    print(f"  Strengths: {section_score.strengths}")
    print(f"  Weaknesses: {section_score.weaknesses}")
```

## 📊 Monitoring & Logging

### Add Logging

```python
import logging

# In your app
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('resume_analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.info(f"User {username} analyzed resume: {resume_filename}")
logger.warning(f"Slow analysis: {analysis_time}s for {resume_filename}")
logger.error(f"Analysis failed for user {user_id}: {error}")
```

### Performance Monitoring

```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

# Use decorator
@monitor_performance
def analyze_resume(resume_text, job_description):
    # Your analysis code
    pass
```

---

**Ready to customize? Start with the integration examples above! 🚀**
