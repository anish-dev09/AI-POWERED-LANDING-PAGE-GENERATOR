# 🚀 Quick Start Guide - What's Next?

## ✅ Current Status
- **Server Running**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: Initialized (SQLite)
- **AI Provider**: Google Gemini (gemini-2.5-flash)

---

## 🎯 Step-by-Step Usage Guide

### Step 1: Create a Business Profile

**Using API Docs (Easy Way):**
1. Open http://localhost:8000/docs
2. Click on **POST /api/v1/businesses**
3. Click "Try it out"
4. Use this sample data:
```json
{
  "name": "TechStart Solutions",
  "industry": "Technology",
  "target_audience": "Small to medium businesses",
  "unique_value": "Affordable cloud solutions with 24/7 support",
  "primary_goal": "lead_generation"
}
```
5. Click "Execute"
6. **Copy the `id` from the response** (you'll need it!)

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/businesses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechStart Solutions",
    "industry": "Technology",
    "target_audience": "Small to medium businesses",
    "unique_value": "Affordable cloud solutions with 24/7 support",
    "primary_goal": "lead_generation"
  }'
```

---

### Step 2: Generate a Landing Page

**Using API Docs:**
1. Click on **POST /api/v1/landing-pages/generate**
2. Click "Try it out"
3. Enter your business_id (from Step 1)
4. Use this configuration:
```json
{
  "business_id": 1,
  "theme": "modern",
  "color_scheme": "blue",
  "include_testimonials": true,
  "include_faq": true,
  "include_pricing": false
}
```
5. Click "Execute" and wait (AI generation takes 10-30 seconds)
6. **Copy the `page_id` from response**

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/landing-pages/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": 1,
    "theme": "modern",
    "color_scheme": "blue",
    "include_testimonials": true,
    "include_faq": true
  }'
```

---

### Step 3: Download Your Landing Page

**Method 1: Using API Docs:**
1. Click on **GET /api/v1/landing-pages/{page_id}/download**
2. Enter your page_id
3. Click "Execute" and "Download file"

**Method 2: Direct Browser:**
- Visit: http://localhost:8000/api/v1/landing-pages/1/download

**Method 3: Check Output Folder:**
- Files are saved in: `generated_pages/` directory
- Look for: `page_{id}.html` and `page_{id}.css`

---

### Step 4: Preview the Landing Page

**Option 1: Open HTML File**
1. Navigate to `generated_pages/` folder
2. Double-click `page_1.html` to open in browser

**Option 2: Using API (if live preview endpoint exists)**
- GET http://localhost:8000/api/v1/landing-pages/1/preview

---

## 🧪 Testing Different Scenarios

### Example 1: E-commerce Store
```json
{
  "name": "StyleHub Fashion",
  "industry": "E-commerce",
  "target_audience": "Fashion-conscious millennials",
  "unique_value": "Curated sustainable fashion at affordable prices",
  "primary_goal": "sales"
}
```

### Example 2: SaaS Product
```json
{
  "name": "CloudTask Pro",
  "industry": "SaaS",
  "target_audience": "Remote teams and project managers",
  "unique_value": "AI-powered task management with smart automation",
  "primary_goal": "signup"
}
```

### Example 3: Local Service
```json
{
  "name": "Elite Fitness Studio",
  "industry": "Health & Fitness",
  "target_audience": "Health-conscious professionals",
  "unique_value": "Personal training with certified experts",
  "primary_goal": "booking"
}
```

---

## 🎨 Available Themes & Color Schemes

**Themes:**
- `modern` - Clean, contemporary design
- `creative` - Bold, artistic layout
- `minimal` - Simple, focused design
- `corporate` - Professional business look
- `startup` - Dynamic, tech-focused

**Color Schemes:**
- `blue` - Trust and professionalism
- `green` - Growth and sustainability
- `purple` - Creativity and innovation
- `orange` - Energy and enthusiasm
- `red` - Passion and urgency

---

## 📊 View All Your Data

### List All Businesses:
```bash
GET http://localhost:8000/api/v1/businesses
```

### List All Landing Pages:
```bash
GET http://localhost:8000/api/v1/landing-pages
```

### Get Specific Business:
```bash
GET http://localhost:8000/api/v1/businesses/1
```

### Get Specific Landing Page:
```bash
GET http://localhost:8000/api/v1/landing-pages/1
```

---

## 🔧 Development Tasks

### 1. **Test the Frontend** (if you want to build it)
```bash
cd frontend
npm install
npm run dev
```
Then visit: http://localhost:5173

### 2. **Run Tests**
```bash
pytest tests/ -v
```

### 3. **Check Code Coverage**
```bash
pytest --cov=app tests/
```

### 4. **Run Linting**
```bash
black app/
flake8 app/
```

---

## 🚀 Deployment Options

### Option 1: Deploy to Render
```bash
# Follow guide in DEPLOYMENT.md
./scripts/deploy-render.sh
```

### Option 2: Docker Deployment
```bash
docker-compose up --build
```

### Option 3: Manual Deployment
- See detailed instructions in `DEPLOYMENT.md`

---

## 📝 Key Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/api/v1/health/status` | Health check |
| POST | `/api/v1/businesses` | Create business |
| GET | `/api/v1/businesses` | List businesses |
| GET | `/api/v1/businesses/{id}` | Get business |
| POST | `/api/v1/landing-pages/generate` | Generate page |
| GET | `/api/v1/landing-pages` | List pages |
| GET | `/api/v1/landing-pages/{id}` | Get page details |
| GET | `/api/v1/landing-pages/{id}/download` | Download page |

---

## 🆘 Troubleshooting

### Server won't start:
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F
```

### Gemini API errors:
- Check your API key in `.env`
- Verify at: https://makersuite.google.com/app/apikey
- Check quota limits

### Database errors:
```bash
# Reset database
rm landing_pages.db
python -m app.main
```

---

## 💡 Pro Tips

1. **Use the Interactive Docs** - http://localhost:8000/docs is the easiest way to test
2. **Check Generated Files** - Always review files in `generated_pages/` folder
3. **Experiment with Themes** - Try different themes and colors to see variations
4. **Save Business IDs** - Keep track of business_id for reuse
5. **Enable SQL Logging** - Set `echo=True` in `database.py` for debugging

---

## 🎓 Learn More

- **API Documentation**: [docs/api-documentation.md](docs/api-documentation.md)
- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Report**: [PROJECT_REPORT.md](PROJECT_REPORT.md)

---

## 📞 Need Help?

- Check the logs in terminal for error messages
- Review API responses for detailed error information
- Consult the documentation in `docs/` folder

---

**🎉 Happy Generating! Start creating amazing landing pages with AI!**
