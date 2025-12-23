# Deployment Guide

## Overview

This guide covers deploying the AI Landing Page Generator to production environments.

## Deployment Options

### Option 1: Render (Recommended)
- Free tier available
- PostgreSQL database included
- Automatic SSL
- Easy environment management

### Option 2: Railway
- Simple deployment
- GitHub integration
- Database provisioning
- Good free tier

### Option 3: Docker + VPS
- Full control
- Custom configuration
- Requires server management

---

## Pre-Deployment Checklist

- [ ] All tests passing (`pytest`)
- [ ] Environment variables documented
- [ ] Database migrations ready
- [ ] API keys obtained (OpenAI, Unsplash)
- [ ] GitHub repository created
- [ ] `.env` file configured locally
- [ ] Production database ready

---

## 1. Deploying Backend to Render

### Step 1: Prepare the Project

1. **Create `render.yaml`** in project root:

```yaml
services:
  - type: web
    name: landing-page-generator-api
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: OPENAI_API_KEY
        sync: false
      - key: UNSPLASH_ACCESS_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: landing-pages-db
          property: connectionString
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: CORS_ORIGINS
        value: '["https://your-frontend-domain.netlify.app"]'

databases:
  - name: landing-pages-db
    databaseName: landing_pages
    user: landing_pages_user
    plan: free
```

2. **Update requirements.txt** for production:

Add these if not already present:
```txt
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

3. **Create Procfile** (optional):

```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### Step 2: Deploy to Render

1. **Sign up** at [render.com](https://render.com)

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Select the repository
   - Render will detect Python

3. **Configure Service**:
   - **Name**: landing-page-generator-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**:
   - Go to "Environment" tab
   - Add all variables from `.env.example`
   - Paste your OpenAI API key
   - Paste your Unsplash API key

5. **Create PostgreSQL Database**:
   - Click "New +" → "PostgreSQL"
   - Name: `landing-pages-db`
   - Copy the internal database URL

6. **Connect Database**:
   - In web service environment variables
   - Add `DATABASE_URL` = (paste internal database URL)

7. **Deploy**:
   - Click "Create Web Service"
   - Wait for build (~5-10 minutes)
   - Check logs for any errors

### Step 3: Run Database Migrations

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Run migrations
render run --service landing-page-generator-api \
  "alembic upgrade head"
```

Or manually via Render Shell:
- Go to your service
- Click "Shell"
- Run: `alembic upgrade head`

---

## 2. Deploying Frontend to Netlify

### Step 1: Prepare Frontend

1. **Update API URLs** in `frontend/js/api.js`:

```javascript
// Change from localhost to your Render URL
const API_BASE_URL = 'https://landing-page-generator-api.onrender.com';
```

2. **Create `netlify.toml`**:

```toml
[build]
  publish = "frontend"
  command = "echo 'No build required'"

[[redirects]]
  from = "/api/*"
  to = "https://landing-page-generator-api.onrender.com/api/:splat"
  status = 200
  force = true

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
```

### Step 2: Deploy to Netlify

1. **Sign up** at [netlify.com](https://netlify.com)

2. **Deploy via GitHub**:
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select your repository
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: (leave empty)
     - **Publish directory**: `.`

3. **Deploy**:
   - Click "Deploy"
   - Wait for deployment
   - Get your URL: `https://your-app-name.netlify.app`

4. **Update CORS in Backend**:
   - Go back to Render dashboard
   - Add environment variable:
     - `CORS_ORIGINS` = `["https://your-app-name.netlify.app"]`

---

## 3. Docker Deployment (Alternative)

### Dockerfile

Already created in Phase 1, but here's an optimized version:

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories
RUN mkdir -p generated_pages

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/landing_pages
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - UNSPLASH_ACCESS_KEY=${UNSPLASH_ACCESS_KEY}
    depends_on:
      - db
    volumes:
      - ./generated_pages:/app/generated_pages

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=landing_pages
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Run migrations
docker-compose exec web alembic upgrade head

# Stop
docker-compose down
```

---

## 4. Environment Configuration

### Production Environment Variables

Create these in your deployment platform:

```bash
# Required
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...

# Optional but Recommended
UNSPLASH_ACCESS_KEY=...
SECRET_KEY=generate-strong-key-here
ENVIRONMENT=production
DEBUG=false

# CORS
CORS_ORIGINS=["https://your-frontend.netlify.app"]

# Performance
MAX_WORKERS=4
WORKER_TIMEOUT=120

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 5. Database Setup

### PostgreSQL Production Setup

1. **Create Database** (if not using Render's):

```sql
CREATE DATABASE landing_pages;
CREATE USER landing_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE landing_pages TO landing_user;
```

2. **Run Migrations**:

```bash
# Set DATABASE_URL
export DATABASE_URL="postgresql://user:pass@host:5432/landing_pages"

# Run migrations
alembic upgrade head
```

3. **Verify Tables**:

```sql
\c landing_pages
\dt
```

---

## 6. CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to Render
      run: |
        curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

### Add Secrets to GitHub

1. Go to repository Settings → Secrets
2. Add:
   - `OPENAI_API_KEY`
   - `RENDER_DEPLOY_HOOK` (from Render dashboard)

---

## 7. Monitoring & Logging

### Application Logging

Update `app/main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### Monitoring Tools

- **Render**: Built-in logs and metrics
- **Sentry**: Error tracking
- **LogTail**: Log management
- **UptimeRobot**: Uptime monitoring

---

## 8. Performance Optimization

### Enable Caching

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="landing-gen:")
```

### CDN for Static Files

Use Cloudflare or similar CDN for:
- Generated landing pages
- Static assets
- Images

---

## 9. Backup Strategy

### Database Backups

**Automated (Render)**:
- Enabled by default on paid plans

**Manual Backup**:
```bash
pg_dump -h hostname -U username landing_pages > backup.sql
```

**Restore**:
```bash
psql -h hostname -U username landing_pages < backup.sql
```

### File Backups

Store generated pages in:
- AWS S3
- Cloudflare R2
- Render Persistent Disk (paid)

---

## 10. Post-Deployment

### Verification Checklist

- [ ] API health check: `https://your-api.onrender.com/health`
- [ ] API docs: `https://your-api.onrender.com/docs`
- [ ] Frontend loads correctly
- [ ] Can generate a test page
- [ ] Can download ZIP file
- [ ] Database is connected
- [ ] Environment variables are set
- [ ] CORS is configured correctly
- [ ] SSL certificate is active
- [ ] Monitoring is set up

### Test Production API

```bash
curl https://your-api.onrender.com/health
```

```bash
curl -X POST https://your-api.onrender.com/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","industry":"tech","target_audience":"devs","tone":"professional","goal":"test"}'
```

---

## Troubleshooting

### Common Issues

**1. Port Binding Error**
```python
# Use environment PORT
port = int(os.getenv("PORT", 8000))
```

**2. Database Connection Error**
- Check DATABASE_URL format
- Ensure database is created
- Run migrations

**3. CORS Errors**
- Update CORS_ORIGINS
- Check frontend URL

**4. AI API Timeouts**
- Increase worker timeout
- Implement retry logic

---

## Costs Estimate (Monthly)

### Free Tier
- **Render**: Free (with limitations)
- **Netlify**: Free (100GB bandwidth)
- **PostgreSQL**: Free (limited)
- **Total**: $0/month

### Production Tier
- **Render**: $7/month
- **Database**: $7/month
- **OpenAI API**: ~$10-50/month (usage-based)
- **Unsplash**: Free
- **Total**: ~$24-64/month

---

*Last Updated: December 23, 2025*
