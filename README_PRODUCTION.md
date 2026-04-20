# AI Resume Analyzer - Production Edition

A production-grade AI resume analyzer that provides:
- Professional ATS-style scoring
- Advanced semantic analysis using BERT
- Multi-factor resume evaluation
- Professional visualizations
- Section-by-section feedback
- Resume comparison tools
- Secure user management

## 🚀 Features

### Core Analysis
- ✅ **ATS Score Calculation** - More accurate than basic scoring
  - 30% Semantic Match (job description alignment)
  - 25% Skill Match (required skills)
  - 15% Keyword Optimization (frequency & density)
  - 15% Experience Relevance (achievements & metrics)
  - 10% Education Relevance (degree & field)
  - 5% Formatting & Structure (completeness)

- ✅ **Advanced Visualizations**
  - Gauge charts for overall scores
  - Radar charts for component breakdown
  - Comparison bar charts
  - Professional color-coded feedback
  - Progress indicators

- ✅ **Section Analysis**
  - Contact Information validation
  - Professional Summary evaluation
  - Work Experience depth analysis
  - Education requirements check
  - Skills section optimization
  - Projects portfolio assessment

- ✅ **Multi-Resume Comparison**
  - Side-by-side score comparison
  - Ranking system
  - Improvement gap analysis
  - Job description alignment

### User Management
- ✅ **Secure Authentication**
  - Password hashing (PBKDF2-SHA256)
  - Session management
  - Account registration
  - Login tracking

- ✅ **History & Analytics**  
  - Analysis history tracking
  - Performance metrics
  - Resume comparison storage
  - Progress visualization

## 📋 Technology Stack

- **Frontend:** Streamlit
- **NLP:** Sentence-Transformers (BERT)
- **ML:** Scikit-learn
- **Visualizations:** Plotly
- **Database:** SQLite
- **PDF Processing:** PDFPlumber
- **Reports:** ReportLab

## 🛠️ Installation

### 1. Clone and Set Up

```bash
cd "d:\Project Folder\AI_Resume_Analyzer"
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

#### Option A: Using New Production App
```bash
streamlit run app_production.py
```

This is the recommended version with:
- Professional UI with multiple tabs
- Enhanced security features
- All advanced analysis capabilities
- Multi-resume comparison
- Settings management

#### Option B: Using Legacy App
```bash
streamlit run app.py
```

## 📁 Project Structure

```
AI_Resume_Analyzer/
├── app.py                    # Legacy version (basic features)
├── app_production.py         # NEW: Production-ready app ⭐
│
├── Core Modules
├── parser.py                 # PDF text extraction
├── skills.py                 # Skill detection
├── bert_matcher.py          # Semantic similarity
├── matcher.py               # Basic score matching
├── recommendation.py        # Skill recommendations
├── report_generator.py      # PDF report generation
│
├── Enhanced Modules ⭐ NEW
├── scoring_advanced.py      # Advanced ATS scoring system
├── visualization.py         # Professional visualizations
├── section_analyzer.py      # Resume section analysis
├── database_enhanced.py     # Secure database with sessions
├── comparison_engine.py     # Multi-resume comparison
│
├── Data Files
├── skills_list.txt         # Known skills database
├── resume_analyzer.db      # SQLite database
│
├── Configuration
├── requirements.txt        # Python dependencies
├── .streamlit/config.toml  # Streamlit configuration
├── README.md              # This file
└── DEPLOYMENT.md          # Deployment guide
```

## 🎯 Usage Guide

### Basic Usage

1. **Register/Login**
   - Create an account with secure password
   - Sessions automatically managed

2. **Upload Resume**
   - Upload PDF version of your resume
   - Paste complete job description

3. **Get Analysis**
   - Instant ATS score calculation
   - Section-by-section feedback
   - Skill gap analysis

4. **Receive Recommendations**
   - Specific improvement suggestions
   - Missing skills with descriptions
   - Section enhancements

5. **Compare & Track**
   - Compare multiple resume versions
   - Track progress over time
   - Download detailed PDF reports

### Advanced Features

#### Multi-Resume Comparison
1. Analyze multiple resume versions
2. Go to "Compare Resumes" tab
3. Select 2-3 resumes to compare
4. View ranking and improvement suggestions

#### Section Analysis
- Get individual scores for each section
- View section-specific strengths/weaknesses
- Get targeted improvement suggestions

#### Performance Tracking
- View all analyses in History tab
- Track score improvements
- Export data for personal records

## 🔐 Security Features

- ✅ **Password Security**
  - PBKDF2-SHA256 hashing with salt
  - Minimum 6-character passwords
  - Secure session tokens

- ✅ **User Privacy**
  - User data isolation
  - Secure database access
  - Session-based authentication

- ✅ **Data Protection**
  - SQLite with foreign keys
  - Input validation
  - Error handling

## 📊 Scoring Methodology

### ATS Score Breakdown

```
Overall ATS Score = 
  (0.30 × Semantic Match) +
  (0.25 × Skill Match) +
  (0.15 × Keyword Optimization) +
  (0.15 × Experience Relevance) +
  (0.10 × Education Relevance) +
  (0.05 × Formatting Score)
```

### Score Interpretation

- **80-100%**: Excellent fit - Apply immediately
- **70-79%**: Strong candidate - Highly recommended
- **60-69%**: Good match - Moderately competitive
- **50-59%**: Moderate match - Consider customizing
- **0-49%**: Poor fit - Major customization needed

## 🎨 UI/UX Features

- Modern SaaS-style interface
- Responsive layout
- Color-coded scoring system
  - 🟢 Green: Excellent (70-100)
  - 🟡 Yellow: Average (40-70)
  - 🔴 Red: Poor (0-40)
- Professional data visualizations
- Intuitive navigation with tabs
- Success/error indicators
- Loading spinners
- Tooltips and help text

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app_production.py --logger.level=info
```

### Cloud Deployment (Streamlit Cloud)

1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Create new app pointing to `app_production.py`
4. Deploy

### Docker Deployment

See `DEPLOYMENT.md` for Docker setup instructions.

## 📈 Performance Optimization

- Caching of BERT embeddings
- Efficient PDF parsing
- Optimized database queries
- Streamlit session state management
- Lazy loading of visualizations

## 🐛 Known Limitations

1. PDF parsing works best with text-based PDFs (not scanned images)
2. Skills must be in `skills_list.txt` for detection
3. Skill recommendations limited to known skills
4. Session expires after 30 days

## 🔄 Future Enhancements

- [ ] Support for image-based PDF (OCR)
- [ ] Resume templates
- [ ] Cover letter analyzer
- [ ] Interview prep module
- [ ] Real-time collaboration
- [ ] Mobile app
- [ ] API endpoints
- [ ] Admin dashboard

## 📞 Support & Contributing

For issues and feature requests, please visit the GitHub repository.

## 📄 License

This project is provided as-is for educational and professional use.

## 📈 Using as Production Ready

This version is optimized for:
- **Recruiters**: Evaluate resume quality
- **Candidates**: Optimize before applying
- **HR Teams**: Bulk resume analysis
- **Educational Institutions**: Resume coaching

### Before Deployment

- [ ] Update `skills_list.txt` with industry-specific skills
- [ ] Configure `.streamlit/config.toml` for your environment
- [ ] Set up HTTPS for production
- [ ] Configure SMTP for email notifications
- [ ] Set up monitoring and logging
- [ ] Run security audit
- [ ] Test with sample resumes

## 🎓 What Makes This Production-Ready

1. ✅ **Professional UI** - Multi-tab interface like real SaaS
2. ✅ **Security** - Password hashing, session management
3. ✅ **Scalability** - Database design supports growth
4. ✅ **Performance** - Optimized queries and caching
5. ✅ **Reliability** - Error handling and validation
6. ✅ **Usability** - Intuitive interface with help
7. ✅ **Data Integrity** - Foreign keys, transactions
8. ✅ **Monitoring** - History and analytics
9. ✅ **Documentation** - Clear structure and comments
10. ✅ **Extensibility** - Modular design for additions

---

**Built with ❤️ for resume analysis and career growth**
