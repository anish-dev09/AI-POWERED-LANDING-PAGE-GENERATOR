# System Architecture

## Overview

The AI-Powered Landing Page Generator follows a modern three-tier architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Web Browser (Frontend Interface)             │   │
│  │         - HTML/CSS/JavaScript                        │   │
│  │         - Tailwind CSS Styling                       │   │
│  │         - Real-time Preview                          │   │
│  └────────────────────┬─────────────────────────────────┘   │
└────────────────────────┼──────────────────────────────────────┘
                         │ HTTP/HTTPS (REST API)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FastAPI Application                     │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │           API Routes Layer                     │  │   │
│  │  │  - /api/v1/generate                           │  │   │
│  │  │  - /api/v1/pages                              │  │   │
│  │  │  - /api/v1/export                             │  │   │
│  │  └───────────────────┬────────────────────────────┘  │   │
│  │                      ▼                                │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │        Business Logic Layer                    │  │   │
│  │  │                                                │  │   │
│  │  │  ┌──────────────┐  ┌────────────────────┐    │  │   │
│  │  │  │ AI Service   │  │ Page Builder       │    │  │   │
│  │  │  │ - OpenAI GPT │  │ - Jinja2 Templates │    │  │   │
│  │  │  │ - Prompts    │  │ - HTML/CSS Gen     │    │  │   │
│  │  │  └──────────────┘  └────────────────────┘    │  │   │
│  │  │                                                │  │   │
│  │  │  ┌──────────────┐  ┌────────────────────┐    │  │   │
│  │  │  │ Image Svc    │  │ SEO Service        │    │  │   │
│  │  │  │ - Unsplash   │  │ - Meta Tags        │    │  │   │
│  │  │  └──────────────┘  └────────────────────┘    │  │   │
│  │  └───────────────────┬────────────────────────────┘  │   │
│  │                      ▼                                │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         Data Access Layer (CRUD)               │  │   │
│  │  │         - SQLAlchemy ORM                       │  │   │
│  │  │         - Business & Page Models               │  │   │
│  │  └───────────────────┬────────────────────────────┘  │   │
│  └────────────────────────┼─────────────────────────────┘   │
└────────────────────────────┼──────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────────┐        ┌─────────────────────────┐    │
│  │  PostgreSQL/     │        │  File System            │    │
│  │  SQLite DB       │        │  - Generated Pages      │    │
│  │  - businesses    │        │  - Static Assets        │    │
│  │  - landing_pages │        │  - Exports (ZIP)        │    │
│  └──────────────────┘        └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  ┌──────────────┐   ┌────────────┐   ┌─────────────────┐   │
│  │  OpenAI API  │   │ Unsplash   │   │  Deployment     │   │
│  │  - GPT-4     │   │  API       │   │  - Render       │   │
│  │  - Content   │   │  - Images  │   │  - Netlify      │   │
│  └──────────────┘   └────────────┘   └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Description

### 1. Client Layer
- **Frontend Interface**: Single-page application providing user input forms and preview
- **Responsibilities**:
  - Collect business information
  - Display live preview
  - Handle user interactions
  - Download/export functionality

### 2. Application Layer

#### API Routes
- RESTful endpoints for all operations
- Request validation using Pydantic
- Authentication and authorization
- Error handling and logging

#### Services

**AI Service**
- Interfaces with OpenAI GPT-4 API
- Prompt engineering and template management
- Content generation and validation
- SEO metadata generation

**Page Builder Service**
- HTML generation using Jinja2 templates
- CSS customization based on themes
- Responsive design implementation
- Asset management

**Image Service**
- Integration with Unsplash API
- Intelligent image selection
- Image optimization and caching
- Alt text generation

**SEO Service**
- Meta tag generation
- Keyword extraction
- Schema markup
- Open Graph tags

### 3. Data Layer

#### Database (PostgreSQL/SQLite)
- **businesses**: Store business profiles
- **landing_pages**: Store generated page metadata
- **generation_history**: Track versions and changes

#### File System
- **generated_pages/**: HTML/CSS output files
- **static/**: Template assets
- **uploads/**: User-uploaded content

## Data Flow

### Landing Page Generation Flow

```
User Input → API Request → Business Logic → AI Generation
    ↓
Validation → Content Creation → Template Rendering
    ↓
Database Save → File Generation → Preview URL
    ↓
Response to Client
```

### Detailed Generation Process

1. **Input Validation** (0.1s)
   - Validate business data
   - Check required fields
   - Sanitize inputs

2. **AI Content Generation** (3-5s)
   - Generate headline and copy
   - Create feature list
   - Generate testimonials
   - Create CTAs

3. **SEO Optimization** (1-2s)
   - Generate meta tags
   - Extract keywords
   - Create descriptions

4. **Image Selection** (1-2s)
   - Search relevant images
   - AI-powered selection
   - Optimize for web

5. **HTML/CSS Generation** (0.5s)
   - Apply templates
   - Inject content
   - Apply theme/colors
   - Generate responsive CSS

6. **Persistence** (0.2s)
   - Save to database
   - Write files to disk
   - Update metadata

7. **Response** (0.1s)
   - Return preview URL
   - Provide download link
   - Send metadata

**Total Time**: ~5-10 seconds per generation

## Security Architecture

### Authentication & Authorization
- API key authentication
- Rate limiting per user/IP
- CORS configuration
- Input sanitization

### Data Security
- Environment variable protection
- SQL injection prevention (ORM)
- XSS prevention in templates
- HTTPS in production

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Session management
- Load balancing ready

### Caching Strategy
- Template caching
- AI response caching (for similar requests)
- Static asset CDN
- Database query optimization

### Performance Optimization
- Async/await for I/O operations
- Background tasks for heavy operations
- Database indexing
- Connection pooling

## Technology Decisions

### Why FastAPI?
- High performance (async support)
- Automatic API documentation
- Type validation with Pydantic
- Modern Python features
- Easy testing

### Why SQLAlchemy?
- ORM flexibility
- Database agnostic
- Migration support with Alembic
- Type-safe queries

### Why Jinja2?
- Powerful templating
- Template inheritance
- Filters and macros
- Security features (auto-escaping)

### Why OpenAI GPT-4?
- Superior content quality
- Instruction following
- JSON output support
- Wide knowledge base

## Deployment Architecture

### Development
```
Local Machine
├── SQLite Database
├── File System Storage
└── Dev Server (uvicorn --reload)
```

### Production
```
Render/Railway (Backend)
├── PostgreSQL Database
├── Persistent Storage Volume
└── Gunicorn + Uvicorn Workers

Netlify/Vercel (Frontend)
├── Static Files
├── CDN Distribution
└── Automatic SSL
```

## Monitoring & Logging

### Application Logs
- Request/response logging
- Error tracking
- Performance metrics
- AI API usage

### Metrics to Track
- API response times
- Generation success rate
- Database query performance
- AI API costs
- User engagement

## Future Enhancements

1. **Microservices**: Split AI service into separate service
2. **Caching Layer**: Redis for session and response caching
3. **Message Queue**: Celery for background tasks
4. **CDN**: CloudFlare for static assets
5. **Analytics**: User behavior tracking
6. **A/B Testing**: Template performance testing

---

*Last Updated: December 23, 2025*
