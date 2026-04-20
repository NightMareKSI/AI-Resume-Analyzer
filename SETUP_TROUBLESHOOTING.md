# 🛠️ Setup & Troubleshooting Guide

## 📦 Installation Guide

### Step 1: Verify Python Installation
```bash
# Check Python version (must be 3.8+, ideally 3.10+)
python --version

# If Python not found, install Python 3.10+ from python.org
```

### Step 2: Install Dependencies

#### Method A: Traditional pip (Recommended)
```bash
# Navigate to project directory
cd "d:\Project Folder\AI_Resume_Analyzer"

# Create virtual environment
python -m venv venv

# Activate virtual environment

## Windows:
.\venv\Scripts\activate

## macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

#### Method B: Using Conda
```bash
# Create conda environment
conda create -n resume-analyzer python=3.10

# Activate environment
conda activate resume-analyzer

# Install dependencies
pip install -r requirements.txt
```

#### Method C: Using Poetry
```bash
# Install Poetry first (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Create environment and install dependencies
poetry install
```

### Step 3: Download BERT Model (First Time Only)
```bash
# The first run will download the BERT model (~400MB)
# This happens automatically when you run the app
# Make sure you have good internet connection

# Optional: Pre-download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Step 4: Verify Installation
```bash
# Activate your environment (if not already activated)
.\venv\Scripts\activate

# Test Python imports
python -c "
import streamlit
import pandas
import torch
import sentence_transformers
print('✅ All imports successful!')
"
```

## 🚀 Running the Application

### First Time Run
```bash
# Activate environment
.\venv\Scripts\activate

# Run the production app
streamlit run app_production.py

# (Optional) Run legacy app
streamlit run app.py
```

The app will open at: **http://localhost:8501**

### Troubleshooting First Run

**Issue: Different ports (not 8501)**
```bash
# Specify port explicitly
streamlit run app_production.py --server.port 8501
```

**Issue: Server not found on localhost:8501**
```bash
# The app might be running on a different port
# Check terminal output for correct URL
# Usually: http://your-machine-name:port
```

**Issue: Browser doesn't open automatically**
```bash
# Manually open the URL shown in terminal
# Usually http://localhost:8501
```

---

## 🐛 Troubleshooting

### 1. DEPENDENCY ISSUES

#### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# If still failing, clean install:
pip uninstall -y streamlit pandas plotly sentence-transformers torch
pip install -r requirements.txt
```

#### Error: "No module named 'sentence_transformers'"

**Solution:**
```bash
# Install torch first (required dependency)
pip install torch torchvision torchaudio

# Then install transformers
pip install sentence-transformers

# Or reinstall everything
pip install --no-cache-dir -r requirements.txt
```

#### Error: "Failed to import pdfplumber"

**Solution:**
```bash
pip install --upgrade pdfplumber

# If still failing, try complete reinstall:
pip uninstall pdfplumber
pip install pdfplumber==0.10.3
```

### 2. RUNTIME ERRORS

#### Error: "CUDA not available" or GPU warnings

**Solution (this is usually not a problem):**
```bash
# CPU mode is fine for this app
# To suppress warnings, add to app start:
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

#### Error: "Out of memory" or "RAM exceeded"

**Solution:**
```bash
# This app needs ~2GB RAM
# Check available RAM
# Windows: Task Manager → Performance
# Mac: Activity Monitor
# Linux: free -h

# If low on RAM:
# Close other applications
# Try smaller BERT model:
# In bert_matcher.py, change:
# model = SentenceTransformer("all-MiniLM-L6-v2")  # Good
# to:
# model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightest
```

### 3. PDF ISSUES

#### Error: "Could not extract text from PDF"

**Causes and Solutions:**

```bash
# Issue 1: Scanned PDF (image-based)
# Solution: Use OCR tool to convert or copy-paste text instead

# Issue 2: Password-protected PDF
# Solution: Remove password in PDF editor

# Issue 3: Corrupted PDF
# Solution: Try re-saving the PDF in another format
# Adobe Reader → Save As → PDF format

# Issue 4: Non-standard encoding
# Solution: Convert PDF using an online tool first
```

**Test PDF extraction:**
```python
import pdfplumber

try:
    with pdfplumber.open("your_resume.pdf") as pdf:
        text = pdf.pages[0].extract_text()
        print(f"Extracted {len(text)} characters")
except Exception as e:
    print(f"Error: {e}")
```

### 4. DATABASE ISSUES

#### Error: "Database is locked"

**Solution:**
```bash
# Close all connections to the database
# Restart the application

# If persists, check file permissions:
# Windows: Right click → Properties → Security → Full Control
# macOS/Linux: chmod 644 resume_analyzer.db
```

#### Error: "No such table: users"

**Solution:**
```bash
# Database not initialized properly
# Delete the old database to reset:
# Windows: del resume_analyzer.db
# Mac/Linux: rm resume_analyzer.db

# Restart app to create new database
```

#### Error: "Foreign key constraint failed"

**Solution:**
```bash
# Restart the application
# If continues, reset database:
import os
if os.path.exists('resume_analyzer.db'):
    os.remove('resume_analyzer.db')
# Restart app
```

### 5. STREAMLIT ISSUES

#### Error: "Unable to bind to port 8501"

**Solution:**
```bash
# Port is already in use
# Option 1: Kill process using the port
# Windows: netstat -ano | findstr :8501
# macOS/Linux: lsof -i :8501

# Option 2: Use different port
streamlit run app_production.py --server.port 8502
```

#### Error: "Chrome/Browser not found"

**Solution:**
```bash
# Streamlit can't open browser automatically
# Just open the URL manually in your browser:
# http://localhost:8501

# Or specify browser:
streamlit run app_production.py --logger.level=error
```

#### Error: "Theme not found"

**Solution:**
```bash
# Delete Streamlit cache:
# Windows: rmdir %USERPROFILE%\.streamlit
# Mac: rm -rf ~/.streamlit
# Linux: rm -rf ~/.streamlit

# Restart app
```

### 6. PERFORMANCE ISSUES

#### Problem: App runs very slowly

**Diagnosis & Solutions:**

```bash
# 1. Check CPU/Memory usage (first run loads model)
# First run: 20-30 seconds (normal - model loading)
# Subsequent: 10-15 seconds (normal - using cache)

# If consistently slow:

# 2. Check internet (needed to download model)
# First time: needs 400MB model download
# Ensure stable internet connection

# 3. Check disk space
# Windows: C: → Right click → Properties
# Mac: Apple → System Settings → Storage
# Linux: df -h

# 4. Use lighter model:
# In bert_matcher.py
# Change: model = SentenceTransformer("all-MiniLM-L6-v2")
#         model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# More options: https://www.sbert.net/docs/pretrained_models.html
```

#### Problem: Analysis takes too long

```bash
# Normal times:
# PDF extraction: 1-3 seconds
# Analysis: 5-15 seconds
# Total: 6-20 seconds

# If taking longer:
# 1. Check system resources
# 2. Reduce model complexity (see above)
# 3. Check PDF size (very large PDFs take longer)
# 4. Clear cache: rm .streamlit/cache
```

### 7. AUTHENTICATION ISSUES

#### Error: "Login failed" but use correct credentials

**Solution:**
```bash
# 1. Check database is working
# Go to SQL explorer to verify user exists

# 2. Verify password was saved correctly
# Reinstall fresh:
import os
os.remove('resume_analyzer.db')
# Restart app and create new account

# 3. Check case sensitivity
# Username might be case-sensitive
```

#### Error: "Session expired"

**Solution:**
```bash
# Session expires after 30 days
# Just login again
# This is a security feature
```

### 8. FUNCTIONALITY ISSUES

#### Skills not being detected

**Solution:**
```bash
# 1. Check skills_list.txt exists
# Verify file is in project root

# 2. Check skill spelling
# Skills are case-sensitive
# "python" ≠ "Python"

# 3. Add missing skills:
# Edit skills_list.txt and add new lines:
kubernetes
terraform
jenkins

# Save and restart app
```

#### PDF report not downloading

**Solution:**
```bash
# 1. Browser download settings
# Check if downloads are blocked
# Allow downloads from localhost

# 2. Check browser storage
# Clear browser cache: Ctrl+Shift+Delete

# 3. Try different browser
# If Chrome fails, try Firefox/Safari

# 4. Check if file was generated
# Look for resume_analysis_report.pdf in project folder
```

#### Comparison feature showing no data

**Solution:**
```bash
# Need at least 2 analyzed resumes
# 1. Analyze first resume
# 2. Analyze another resume
# 3. Then use comparison feature

# If still not working:
# Check database has records:
import sqlite3
conn = sqlite3.connect('resume_analyzer.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM analysis_history")
print(cursor.fetchone())  # Should show > 0
```

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Virtual environment created: `venv` folder exists
- [ ] Dependencies installed: `pip list` shows all packages
- [ ] BERT model available: `sentence-transformers` in pip list
- [ ] App starts: `streamlit run app_production.py`
- [ ] Browser opens: localhost:8501
- [ ] Can register account: Create test user
- [ ] Can login: Use test credentials
- [ ] Can upload PDF: Sample resume uploads
- [ ] Can paste job description: Text area works
- [ ] Analysis works: Runs to completion
- [ ] Scores display: Shows numeric scores
- [ ] Charts render: Visualizations appear
- [ ] Can download report: PDF file generated

---

## 🆘 Advanced Troubleshooting

### Completely Reset Installation

```bash
# 1. Deactivate environment
deactivate

# 2. Remove virtual environment
# Windows: rmdir /s venv
# Mac/Linux: rm -rf venv

# 3. Remove cache files
# Windows: rmdir %USERPROFILE%\.streamlit
# Mac/Linux: rm -rf ~/.streamlit

# 4. Remove database
# Windows: del resume_analyzer.db
# Mac/Linux: rm resume_analyzer.db

# 5. Reinstall from scratch
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# 6. Start app
streamlit run app_production.py
```

### Debug Mode

```bash
# Run with verbose logging
streamlit run app_production.py --logger.level=debug

# Check output for detailed error messages
```

### Check Environment Variables

```python
# Add this to app.py temporarily to debug
import os
import sys

print("Python version:", sys.version)
print("Python path:", sys.executable)
print("Current directory:", os.getcwd())
print("Virtual env active:", os.environ.get('VIRTUAL_ENV'))

# Check if all modules can import
try:
    import streamlit
    print("✓ streamlit")
except: print("✗ streamlit")

try:
    import pdfplumber
    print("✓ pdfplumber")
except: print("✗ pdfplumber")

try:
    from sentence_transformers import SentenceTransformer
    print("✓ sentence_transformers")
except: print("✗ sentence_transformers")

try:
    import plotly
    print("✓ plotly")
except: print("✗ plotly")
```

---

## 📞 Getting Help

If issues persist:

1. **Check Documentation**
   - README_PRODUCTION.md
   - QUICKSTART.md
   - IMPLEMENTATION_GUIDE.md

2. **Check Other Resources**
   - Streamlit docs: https://docs.streamlit.io
   - Sentence-Transformers docs: https://www.sbert.net
   - PDFPlumber docs: https://github.com/jsvine/pdfplumber

3. **Common Solution Pattern**
   - Reset everything (see above)
   - Clean install
   - Test with fresh account
   - Check system resources

---

**Most issues can be fixed with a fresh reinstall! 🔧**
