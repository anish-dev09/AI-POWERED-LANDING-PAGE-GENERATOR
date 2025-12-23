# 🚀 AI-Powered Landing Page Generator

> **Generate professional, SEO-optimized landing pages in minutes using AI**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Project Overview

An AI-powered SaaS application that enables businesses to generate fully functional, responsive, and SEO-optimized landing pages by providing minimal business details. Built as a production-ready web application with Python/FastAPI backend and modern frontend technologies.

### 🎯 Key Features

- **AI Content Generation**: Intelligent copy generation for headlines, features, CTAs, and testimonials
- **Smart Section Ordering**: AI-powered layout optimization based on industry and goals
- **Responsive Design**: Mobile-first, fully responsive HTML/CSS output
- **SEO Optimization**: Auto-generated meta tags, descriptions, and keywords
- **Theme Customization**: Multiple themes with color customization
- **Image Integration**: Automatic relevant image selection via Unsplash API
- **Live Preview**: Real-time preview before export
- **Easy Export**: Downloadable ZIP with deployment-ready files
- **Version Management**: Regenerate and manage multiple versions

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **AI/ML**: OpenAI GPT-4
- **Template Engine**: Jinja2

### Frontend
- **HTML5, CSS3, JavaScript**
- **Tailwind CSS** for styling
- **Responsive Design**

### Deployment
- **Backend**: Render / Railway
- **Frontend**: Netlify / Vercel
- **CI/CD**: GitHub Actions

## 📁 Project Structure

```
landing-page-generator/
├── app/                        # Main application package
│   ├── models/                 # Database models
│   ├── schemas/                # Pydantic schemas
│   ├── routers/                # API route handlers
│   ├── services/               # Business logic services
│   ├── templates/              # Jinja2 HTML templates
│   ├── crud/                   # Database CRUD operations
│   ├── utils/                  # Utility functions
│   ├── middleware/             # Custom middleware
│   └── main.py                 # Application entry point
├── frontend/                   # Frontend static files
│   ├── index.html
│   ├── css/
│   └── js/
├── tests/                      # Test suite
│   ├── test_api/
│   ├── test_services/
│   └── conftest.py
├── docs/                       # Documentation
│   ├── architecture.md
│   ├── api-documentation.md
│   └── deployment-guide.md
├── generated_pages/            # Output directory for generated pages
├── alembic/                    # Database migrations
├── .env.example               # Environment variables template
├── .gitignore
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- OpenAI API key
- Unsplash API key (optional, for images)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/landing-page-generator.git
   cd landing-page-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   copy .env.example .env
   
   # Edit .env and add your API keys
   # OPENAI_API_KEY=your_key_here
   # UNSPLASH_ACCESS_KEY=your_key_here
   ```

5. **Initialize database**
   ```bash
   # Database will be auto-created on first run
   # Or use Alembic for migrations
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend: Open `frontend/index.html` in browser

## 📖 Usage

### Basic Usage

1. **Fill in Business Details**
   - Business name
   - Industry
   - Target audience
   - Tone (professional, friendly, bold, elegant)
   - Primary goal

2. **Customize (Optional)**
   - Select theme
   - Choose primary color
   - Toggle sections

3. **Generate**
   - Click "Generate Landing Page"
   - Preview in real-time
   - Download as ZIP file

### API Usage

```python
import requests

# Generate landing page
response = requests.post("http://localhost:8000/api/v1/generate", json={
    "name": "TechStartup Inc",
    "industry": "technology",
    "target_audience": "Small businesses and startups",
    "tone": "professional",
    "goal": "Generate leads for our SaaS product",
    "unique_value_proposition": "We help businesses automate their workflows"
})

result = response.json()
print(f"Page ID: {result['page_id']}")
print(f"Preview URL: {result['preview_url']}")
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_generate.py -v
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api-documentation.md)
- [Deployment Guide](docs/deployment-guide.md)

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for content generation | Yes |
| `UNSPLASH_ACCESS_KEY` | Unsplash API key for images | No |
| `DATABASE_URL` | Database connection string | Yes |
| `DEBUG` | Debug mode (True/False) | No |
| `PORT` | Server port | No |

## 🛣️ Roadmap

- [x] Phase 1: Project Setup & Architecture
- [ ] Phase 2: Database Design & Models
- [ ] Phase 3: AI Content Generation Engine
- [ ] Phase 4: HTML/CSS Template System
- [ ] Phase 5: FastAPI Backend APIs
- [ ] Phase 6: Image Integration
- [ ] Phase 7: Frontend Development
- [ ] Phase 8: Testing & QA
- [ ] Phase 9: Production Deployment
- [ ] Phase 10: Documentation & Presentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Unsplash for image API
- FastAPI framework
- Tailwind CSS

## 📧 Support

For support, email support@example.com or open an issue in the GitHub repository.

---

**Built with ❤️ for final year engineering project - December 2025**
