# Deployment Guide - AI Resume Analyzer Pro

## 📦 Environment Setup

### Prerequisites
- Python 3.10+
- pip or conda package manager
- Git (for version control)
- 4GB+ RAM (for BERT model)
- 5GB+ disk space (for dependencies)

### Local Development Setup

```bash
# 1. Clone repository
cd "d:\Project Folder\AI_Resume_Analyzer"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
streamlit run app_production.py
```

The app will be available at `http://localhost:8501`

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended for Beginners)

**Easiest deployment - Free tier available**

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and `app_production.py`
   - Click "Deploy"

3. **Configuration** (`~/.streamlit/config.toml`)
   ```toml
   [client]
   showErrorDetails = false
   
   [logger]
   level = "warning"
   
   [theme]
   primaryColor = "#1f77b4"
   backgroundColor = "#FFFFFF"
   ```

**Pros:**
- Zero infrastructure setup
- Automatic HTTPS
- Free tier available
- Auto-deploys on git push

**Cons:**
- Limited to 1GB RAM
- Public repository required
- Limited environment variables

### Option 2: Heroku Deployment

**Simple cloud deployment with better resources**

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create Procfile**
   ```
   web: streamlit run app_production.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Create .gitignore**
   ```
   venv/
   __pycache__/
   *.pyc
   .env
   *.db
   ```

4. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku logs --tail
   ```

### Option 3: Docker Deployment

**Best for production - Consistent across environments**

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       build-essential \
       curl \
       && rm -rf /var/lib/apt/lists/*
   
   # Copy requirements
   COPY requirements.txt .
   
   # Install Python dependencies
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application
   COPY . .
   
   # Create non-root user
   RUN useradd -m -u 1000 streamlit
   USER streamlit
   
   # Expose port
   EXPOSE 8501
   
   # Run application
   CMD ["streamlit", "run", "app_production.py", \
        "--server.port=8501", \
        "--server.address=0.0.0.0", \
        "--logger.level=info"]
   ```

2. **Create .dockerignore**
   ```
   venv
   __pycache__
   *.pyc
   .git
   .gitignore
   .env
   *.db
   ```

3. **Build and Run**
   ```bash
   # Build image
   docker build -t resume-analyzer:latest .
   
   # Run container
   docker run -p 8501:8501 resume-analyzer:latest
   ```

4. **Push to Docker Hub**
   ```bash
   docker tag resume-analyzer:latest yourusername/resume-analyzer:latest
   docker push yourusername/resume-analyzer:latest
   ```

### Option 4: AWS EC2 Deployment

**Production-grade deployment with full control**

1. **Launch EC2 Instance**
   - Instance type: t3.medium (minimum)
   - Storage: 20GB
   - Security group: Allow ports 80, 443, 8501

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt-get update && sudo apt-get upgrade -y
   
   # Install dependencies
   sudo apt-get install -y python3.10 python3.10-venv python3-pip
   
   # Clone repository
   git clone your-repo-url
   cd AI_Resume_Analyzer
   
   # Setup
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Systemd Service**
   Create `/etc/systemd/system/resume-analyzer.service`:
   ```ini
   [Unit]
   Description=Resume Analyzer
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/AI_Resume_Analyzer
   Environment="PATH=/home/ubuntu/AI_Resume_Analyzer/venv/bin"
   ExecStart=/home/ubuntu/AI_Resume_Analyzer/venv/bin/streamlit run app_production.py \
             --server.port=8501 \
             --server.address=0.0.0.0
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service**
   ```bash
   sudo systemctl enable resume-analyzer
   sudo systemctl start resume-analyzer
   sudo systemctl status resume-analyzer
   ```

5. **Setup Nginx Reverse Proxy**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

6. **Setup SSL Certificate**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## 🔒 Security Configuration

### Environment Variables (.env)
```
DATABASE_PATH=/path/to/resume_analyzer.db
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
DEBUG=False
LOG_LEVEL=INFO
```

### Database Hardening
```python
# Enable these in database_enhanced.py
PRAGMA foreign_keys = ON;  # Already enabled
PRAGMA journal_mode = WAL;  # Write-ahead logging
PRAGMA synchronous = NORMAL;  # Balance safety/performance
```

### Application Security Checklist
- [ ] Change all default credentials
- [ ] Enable HTTPS/SSL
- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Validate all user inputs
- [ ] Implement rate limiting
- [ ] Setup error logging
- [ ] Regular security updates
- [ ] Backup database daily
- [ ] Monitor application logs

## 📊 Monitoring & Maintenance

### Log Monitoring
```bash
# View recent logs
tail -f /var/log/resume-analyzer.log

# Search for errors
grep ERROR /var/log/resume-analyzer.log
```

### Database Maintenance
```python
# Backup database
import shutil
shutil.copy2('resume_analyzer.db', 'resume_analyzer.db.backup')

# Or use system backup
sqlite3 resume_analyzer.db ".backup backup.db"
```

### Performance Monitoring
```bash
# Monitor resource usage
htop
# or
ps aux | grep streamlit
```

## 🔧 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'sentence_transformers'"**
```bash
pip install sentence-transformers
pip install torch torchvision torchaudio
```

**Issue: PDF extraction fails**
- Ensure PDF is text-based (not scanned image)
- Try re-saving PDF in standard format
- Check pdfplumber compatibility

**Issue: Application runs slow**
- Allocate more RAM (minimum 4GB recommended)
- Check database size and optimize queries
- Clear old analyses regularly

**Issue: Database locked error**
- Close other connections
- Restart the service
- Check file permissions

### Performance Tuning

```python
# Add caching to scoring_advanced.py
@lru_cache(maxsize=1024)
def calculate_keyword_density_score(resume_text, job_description):
    # Implementation
    pass

# Add connection pooling
from sqlalchemy import create_engine
engine = create_engine('sqlite:///resume_analyzer.db', 
                      connect_args={'timeout': 15})
```

## 📈 Scaling

### Single Server Limit: ~100 concurrent users
- Streamlit server: ~50 users
- Process: ~2GB RAM per 10 users
- Database: SQLite->PostgreSQL for >1000 analyses/day

### Scaling Strategy

**Stage 1: Single Server** (Current)
- Streamlit on EC2 t3.medium
- SQLite database
- Good for 50-100 users

**Stage 2: Separate Database**
- Upgrade to PostgreSQL
- Move database to RDS
- Improves performance

**Stage 3: Multiple Servers**
- Load balancer (ELB/ALB)
- Multiple Streamlit instances
- Shared database (PostgreSQL RDS)
- Session management (Redis)

**Stage 4: Kubernetes**
- Container orchestration
- Auto-scaling
- Better resource management

## 📋 Production Checklist

Before going live, verify:

- [ ] Streamlit configured for production
- [ ] HTTPS/SSL enabled
- [ ] Database backed up
- [ ] Error logging configured
- [ ] User authentication working
- [ ] Rate limiting implemented
- [ ] Performance tested under load
- [ ] Disaster recovery plan ready
- [ ] Monitoring alerts setup
- [ ] Documentation complete
- [ ] All dependencies pinned
- [ ] Security audit passed

## 🆘 Support

For deployment issues:
1. Check Streamlit documentation: https://docs.streamlit.io
2. Review application logs
3. Test locally before deploying
4. Contact cloud provider support for infrastructure issues

---

**Deployment Status:** Ready for production ✅
