# Architecture - AI Resume Analyzer Pro

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  (Streamlit Web Interface - app_production.py)          │
├─────────────────────────────────────────────────────────┤
│                 Authentication Layer                     │
│            (database_enhanced.py - Sessions)            │
├─────────────────────────────────────────────────────────┤
│           Business Logic / Analysis Layer                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Core Components:                                 │  │
│  │ • parser.py - PDF extraction                    │  │
│  │ • skills.py - Skill detection                   │  │
│  │ • bert_matcher.py - Semantic analysis           │  │
│  │ • scoring_advanced.py - ATS scoring             │  │
│  │ • section_analyzer.py - Section feedback        │  │
│  │ • comparison_engine.py - Resume comparison      │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│         Visualization & Presentation Layer              │
│         (visualization.py - Plotly charts)              │
├─────────────────────────────────────────────────────────┤
│                Data Access Layer                        │
│      (database_enhanced.py - SQLite persistence)       │
├─────────────────────────────────────────────────────────┤
│           External Libraries & Models                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │ • Sentence-Transformers (BERT-mini-LM-L6-v2)    │  │
│  │ • Scikit-learn (vectorization, similarity)       │  │
│  │ • PDFPlumber (PDF processing)                    │  │
│  │ • ReportLab (PDF generation)                     │  │
│  │ • Plotly (visualizations)                        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Module Interaction Flow

### Resume Analysis Flow

```
1. User Login (database_enhanced.py)
   ↓
2. Upload PDF (app_production.py)
   ↓
3. Extract Text (parser.py)
   ↓
4. Skill Extraction (skills.py)
   ↓
5. Semantic Analysis (bert_matcher.py)
   ↓
6. Advanced Scoring (scoring_advanced.py)
   ├─ Keyword density
   ├─ Experience relevance
   ├─ Education relevance
   └─ Formatting score
   ↓
7. Section Analysis (section_analyzer.py)
   ├─ Contact section
   ├─ Summary section
   ├─ Experience section
   ├─ Education section
   ├─ Skills section
   └─ Projects section
   ↓
8. Visualization (visualization.py)
   ├─ Gauge charts
   ├─ Radar charts
   ├─ Progress bars
   └─ Cards
   ↓
9. Report Generation (report_generator.py)
   ↓
10. Save to Database (database_enhanced.py)
   ↓
11. Display Results (app_production.py)
```

### Multi-Resume Comparison Flow

```
1. Select Multiple Resumes
2. comparison_engine.py processes each
   ├─ Extract component scores
   ├─ Calculate gaps
   └─ Generate rankings
3. visualization.py creates comparison charts
4. Display rankings and recommendations
5. Save comparison to database
```

## Data Model

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN,
    profile_picture TEXT,
    bio TEXT
)
```

### Analysis History Table
```sql
CREATE TABLE analysis_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    resume_filename TEXT NOT NULL,
    resume_text TEXT,
    job_description TEXT,
    semantic_score REAL,
    skill_score REAL,
    keyword_score REAL,
    experience_score REAL,
    education_score REAL,
    formatting_score REAL,
    overall_score REAL,
    matched_skills TEXT,
    missing_skills TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

## Scoring Algorithm

### Overall Score Calculation

```
Weighted Score Formula:

ATS_Score = (0.30 × Semantic_Match) +
            (0.25 × Skill_Match) +
            (0.15 × Keyword_Score) +
            (0.15 × Experience_Score) +
            (0.10 × Education_Score) +
            (0.05 × Formatting_Score)

Where each component is calculated as:

Semantic_Match = cosine_similarity(BERT_embedding(resume), 
                                   BERT_embedding(job_description)) × 100

Skill_Match = (matched_skills / required_skills) × 100

Keyword_Score = (keyword_frequency_ratio × coverage_ratio) × 100

Experience_Score = (action_verbs + achievements + metrics) / 100 × 100

Education_Score = (degree_score + field_score) / 100 × 100

Formatting_Score = (sections_found + length_check) / 100 × 100
```

## API Endpoints (Future)

While currently Streamlit-based, the architecture supports future API development:

```
/api/v1/analyze         - POST resume and job description
/api/v1/compare         - POST multiple resumes
/api/v1/history         - GET user analysis history
/api/v1/auth/register   - POST new user registration
/api/v1/auth/login      - POST user login
/api/v1/scores          - GET historical scores
/api/v1/recommendations - GET skill recommendations
```

## Performance Characteristics

### Processing Times (Typical)
- PDF extraction: 1-3 seconds
- Skill extraction: 0.5 seconds
- BERT embedding: 2-5 seconds (first run, cached after)
- Scoring calculation: 0.2 seconds
- Report generation: 2-3 seconds

**Total Average Analysis Time: 6-15 seconds**

### Memory Usage
- Application: ~500MB
- BERT model: ~400MB
- Per user session: ~100MB
- Total minimum: ~1GB RAM

### Database Size
- Per analysis record: ~50-100KB
- 1000 analyses: ~100MB
- Indexes: ~10% of data size

## Scalability Considerations

### Current Bottlenecks
1. BERT model loading (mitigated by caching)
2. Single SQLite database (upgrade to PostgreSQL for scale)
3. Single Streamlit server (use Docker + load balancer)

### Optimization Strategies

**Short-term (current users < 100)**
- Redis caching for BERT embeddings
- Connection pooling
- Query optimization
- Database indexing on user_id, created_at

**Medium-term (users 100-1000)**
- PostgreSQL migration
- Session store in Redis
- Background job queue (Celery)
- CDN for static assets

**Long-term (users > 1000)**
- Kubernetes orchestration
- Microservices architecture
- Separate analysis workers
- GraphQL API layer

## Security Architecture

### Authentication Flow
```
1. User registers: Password → Hash (PBKDF2) + Salt → Store
2. User logs in: Password + Salt → Hash → Compare stored
3. Session created: Token → Stash in database
4. Requests validated: Against session token
5. User logout: Invalidate session token
```

### Data Protection
- All passwords hashed with salt
- Sessions expire automatically
- HTTPS for data in transit
- Parameterized queries prevent SQL injection
- Input validation on all fields
- CSRF protection enabled

## Error Handling

### Graceful Degradation Strategy

```python
try:
    resume_text = extract_text_from_pdf(file)
except Exception:
    # Fallback: Ask user to copy-paste text
    resume_text = st.text_area("Copy-paste resume text")

try:
    embedding = bert_model.encode(text)
except Exception:
    # Fallback: Use basic keyword matching
    score = calculate_keyword_match(text, jd)
```

### Logging Strategy
- INFO: User actions (login, analysis, download)
- WARNING: Slow operations, missing data
- ERROR: Failed operations, exceptions
- DEBUG: Detailed operation traces

## Deployment Topology

### Single Server (Current)
```
Domain
  ↓
Streamlit App (Port 8501)
  ↓
SQLite Database
```

### Production Multi-Server (Recommended)
```
Domain → Load Balancer → Streamlit 1
                      ↓ Streamlit 2
                      ↓ Streamlit 3
                      ↓
              PostgreSQL Database
              (Managed RDS)
```

## Technology Choices Rationale

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | Streamlit | Rapid development, no frontend knowledge needed |
| NLP | Sentence-Transformers | Fast BERT embeddings, pre-trained models |
| ML | Scikit-learn | Lightweight, efficient similarity calculations |
| Visualization | Plotly | Interactive charts, professional appearance |
| Database | SQLite (Production: PostgreSQL) | Simple for MVP, scalable when needed |
| PDF Processing | PDFPlumber | Accurate text extraction, well-maintained |

---

**Architecture designed for scalability and production readiness**
