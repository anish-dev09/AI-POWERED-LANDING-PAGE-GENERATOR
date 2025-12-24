# 🚀 Production Deployment Guide

Complete guide to deploy your AI-Powered Landing Page Generator to production.

## 📋 Pre-Deployment Checklist

- [ ] All tests passing (`pytest`)
- [ ] Environment variables configured
- [ ] API keys obtained (Gemini/OpenAI)
- [ ] Database configured
- [ ] GitHub repository created
- [ ] Domain name ready (optional)

## 🎯 Deployment Options

### Option 1: Render (Recommended for Backend)

**Why Render?**
- Free tier available
- Automatic deployments from GitHub
- Built-in PostgreSQL database
- Easy environment variable management
- HTTPS included

**Steps:**

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create PostgreSQL Database**
   ```
   - Click "New +" → "PostgreSQL"
   - Name: landing-page-db
   - Plan: Free
   - Note the connection string
   ```

3. **Create Web Service**
   ```
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Name: landing-page-api
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   DATABASE_URL=postgres://... (from step 2)
   ENVIRONMENT=production
   DEBUG=False
   CORS_ORIGINS=https://your-frontend-url.netlify.app
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your API URL: `https://your-app.onrender.com`

### Option 2: Netlify (For Frontend)

**Why Netlify?**
- Free tier available
- Global CDN
- Automatic HTTPS
- Easy form handling
- Great for React/Vue apps

**Steps:**

1. **Build Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Create Netlify Account**
   - Go to [netlify.com](https://netlify.com)
   - Sign up with GitHub

3. **Deploy**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Login
   netlify login
   
   # Deploy
   netlify deploy --prod --dir=frontend/dist
   ```

4. **Configure Environment**
   - Go to Site Settings → Environment Variables
   - Add: `VITE_API_URL=https://your-render-api-url.onrender.com`

### Option 3: Docker Deployment

**For VPS/Cloud Server (DigitalOcean, AWS, Azure)**

1. **Prepare Server**
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/landing-page-generator.git
   cd landing-page-generator
   ```

3. **Configure Environment**
   ```bash
   cp .env.production .env
   # Edit .env with your API keys
   nano .env
   ```

4. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Setup Nginx Reverse Proxy** (Optional)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Option 4: Railway

**Quick Deployment**

1. **Install Railway CLI**
   ```bash
   npm install -g railway
   ```

2. **Login and Initialize**
   ```bash
   railway login
   railway init
   ```

3. **Add Environment Variables**
   ```bash
   railway variables set AI_PROVIDER=gemini
   railway variables set GEMINI_API_KEY=your_key_here
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## 🔐 Security Checklist

- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS properly
- [ ] Use strong database passwords
- [ ] Enable rate limiting
- [ ] Set up monitoring/logging
- [ ] Regular backups
- [ ] Update dependencies regularly

## 📊 Post-Deployment

### 1. Test Your Deployment

```bash
# Test health endpoint
curl https://your-api-url.com/health

# Test API
curl -X POST https://your-api-url.com/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Business",
    "industry": "technology",
    "target_audience": "developers"
  }'
```

### 2. Setup Monitoring

**Sentry (Error Tracking)**
```bash
pip install sentry-sdk
```

```python
# In app/main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

**Render Monitoring**
- View logs in Render Dashboard
- Set up health check endpoints
- Configure alerts

### 3. Database Backups

**Render PostgreSQL:**
- Automatic daily backups (paid plans)
- Manual backups: Dashboard → Database → Backups

**Docker:**
```bash
# Backup
docker exec landing-page-db pg_dump -U postgres landing_pages > backup.sql

# Restore
docker exec -i landing-page-db psql -U postgres landing_pages < backup.sql
```

## 🔄 CI/CD Setup

GitHub Actions is already configured! Just add secrets:

1. Go to GitHub repository → Settings → Secrets
2. Add these secrets:
   ```
   RENDER_API_KEY=your_render_api_key
   RENDER_SERVICE_ID=your_service_id
   GEMINI_API_KEY=your_gemini_key
   DOCKER_USERNAME=your_docker_username
   DOCKER_PASSWORD=your_docker_password
   ```

3. Push to main branch → Automatic deployment! 🎉

## 🐛 Troubleshooting

### Build Failures

```bash
# Check logs
render logs --tail

# Local test
docker build -t landing-page-test .
docker run -p 8000:8000 landing-page-test
```

### Database Connection Issues

```bash
# Test connection
python -c "from app.database import engine; engine.connect()"

# Check environment variable
echo $DATABASE_URL
```

### API Errors

```bash
# Check logs
docker-compose logs api

# Test locally with production env
cp .env.production .env
uvicorn app.main:app --reload
```

## 📈 Performance Optimization

1. **Enable Caching**
   - Redis for session storage
   - CDN for static assets

2. **Database Optimization**
   - Add indexes
   - Connection pooling
   - Query optimization

3. **Frontend Optimization**
   - Minify assets
   - Enable compression
   - Lazy loading

## 🎯 Next Steps

- [ ] Custom domain setup
- [ ] SSL certificate configuration
- [ ] Monitoring and analytics
- [ ] Automated backups
- [ ] Load testing
- [ ] Documentation updates
- [ ] User feedback collection

## 📞 Support

If you encounter issues:
1. Check logs first
2. Review environment variables
3. Test locally with production settings
4. Open an issue on GitHub

---

**Deployment Status:** ✅ Ready for Production
**Last Updated:** December 2025
