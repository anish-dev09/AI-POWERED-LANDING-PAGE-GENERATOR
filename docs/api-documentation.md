# API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, the API is open for development. Production will use API keys.

```bash
# Future: Include API key in headers
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check

#### `GET /health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Generate Landing Page

#### `POST /api/v1/generate`

Generate a complete landing page from business input.

**Request Body:**
```json
{
  "name": "TechStartup Inc",
  "industry": "technology",
  "target_audience": "Small businesses and startups",
  "tone": "professional",
  "goal": "Generate leads for our SaaS product",
  "unique_value_proposition": "We help businesses automate their workflows",
  "additional_info": "Focus on enterprise security features"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Business name (2-100 chars) |
| `industry` | string | Yes | Industry/sector |
| `target_audience` | string | Yes | Description of target audience |
| `tone` | string | No | Tone: professional, friendly, bold, elegant |
| `goal` | string | Yes | Primary goal of the landing page |
| `unique_value_proposition` | string | No | What makes the business unique |
| `additional_info` | string | No | Any additional context |

**Response:**
```json
{
  "success": true,
  "page_id": "550e8400-e29b-41d4-a716-446655440000",
  "landing_page_id": 1,
  "preview_url": "/generated/550e8400-e29b-41d4-a716-446655440000/index.html",
  "content": {
    "headline": "Transform Your Business Workflow Today",
    "subheadline": "Automate repetitive tasks and boost productivity by 10x",
    "cta_text": "Start Free Trial",
    "features": [
      {
        "title": "Easy Integration",
        "description": "Connect with your existing tools in minutes",
        "icon": "integration"
      }
    ],
    "testimonials": [
      {
        "name": "John Doe",
        "role": "CEO, Example Corp",
        "content": "This tool changed how we work!",
        "rating": 5
      }
    ],
    "about_section": "We are dedicated to helping businesses succeed..."
  },
  "seo": {
    "meta_title": "TechStartup Inc - Workflow Automation Software",
    "meta_description": "Transform your business with automated workflows...",
    "keywords": ["workflow automation", "productivity", "business software"],
    "og_title": "TechStartup Inc - Workflow Automation",
    "og_description": "Boost productivity by 10x with automation"
  }
}
```

**Status Codes:**
- `200 OK`: Successfully generated
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Generation failed

---

### Generate with Customization

#### `POST /api/v1/generate-custom`

Generate with custom theme and color settings.

**Request Body:**
```json
{
  "business": {
    "name": "TechStartup Inc",
    "industry": "technology",
    "target_audience": "Small businesses",
    "tone": "professional",
    "goal": "Generate leads"
  },
  "customization": {
    "theme": "modern",
    "primary_color": "#3B82F6",
    "include_testimonials": true,
    "include_features": true,
    "cta_text": "Get Started Now"
  }
}
```

**Customization Options:**

| Field | Type | Default | Options |
|-------|------|---------|---------|
| `theme` | string | "modern" | modern, minimal, corporate |
| `primary_color` | string | "#3B82F6" | Any hex color |
| `include_testimonials` | boolean | true | true/false |
| `include_features` | boolean | true | true/false |
| `cta_text` | string | null | Custom CTA text |

---

### List Pages

#### `GET /api/v1/pages`

Get list of all generated landing pages.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Max records to return (default: 10)

**Example:**
```bash
GET /api/v1/pages?skip=0&limit=10
```

**Response:**
```json
{
  "pages": [
    {
      "id": 1,
      "business_id": 1,
      "headline": "Transform Your Business",
      "theme": "modern",
      "created_at": "2025-12-23T10:30:00",
      "is_published": false
    }
  ],
  "total": 1
}
```

---

### Get Page Details

#### `GET /api/v1/pages/{page_id}`

Get detailed information about a specific page.

**Parameters:**
- `page_id` (int): The page ID

**Response:**
```json
{
  "id": 1,
  "business_id": 1,
  "version": 1,
  "headline": "Transform Your Business Workflow Today",
  "subheadline": "Automate and boost productivity",
  "cta_text": "Start Free Trial",
  "features": "[{...}]",
  "testimonials": "[{...}]",
  "meta_title": "TechStartup Inc - Workflow Automation",
  "meta_description": "Transform your business...",
  "keywords": "workflow, automation, productivity",
  "theme": "modern",
  "primary_color": "#3B82F6",
  "html_path": "generated_pages/uuid/index.html",
  "css_path": "generated_pages/uuid/styles.css",
  "is_published": false,
  "created_at": "2025-12-23T10:30:00"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Page doesn't exist

---

### Delete Page

#### `DELETE /api/v1/pages/{page_id}`

Delete a landing page and its files.

**Parameters:**
- `page_id` (int): The page ID

**Response:**
```json
{
  "success": true,
  "message": "Page deleted"
}
```

**Status Codes:**
- `200 OK`: Successfully deleted
- `404 Not Found`: Page doesn't exist

---

### Publish Page

#### `PUT /api/v1/pages/{page_id}/publish`

Mark a page as published.

**Parameters:**
- `page_id` (int): The page ID

**Response:**
```json
{
  "success": true,
  "page": {
    "id": 1,
    "is_published": true,
    "updated_at": "2025-12-23T11:00:00"
  }
}
```

---

### Export Page

#### `GET /api/v1/export/{page_id}`

Download the landing page as a ZIP file.

**Parameters:**
- `page_id` (int): The page ID

**Response:**
- Content-Type: `application/zip`
- File: `landing-page-{page_id}.zip`

**ZIP Contents:**
```
landing-page-1.zip
├── index.html
├── styles.css
├── script.js (if applicable)
└── README.md
```

**Status Codes:**
- `200 OK`: File download
- `404 Not Found`: Page doesn't exist

---

### Regenerate Section

#### `POST /api/v1/regenerate/{page_id}`

Regenerate a specific section of an existing page.

**Parameters:**
- `page_id` (int): The page ID

**Request Body:**
```json
{
  "section": "features"
}
```

**Available Sections:**
- `headline`
- `features`
- `testimonials`
- `cta`
- `about`

**Response:**
```json
{
  "success": true,
  "updated_section": "features",
  "new_content": {
    "features": [...]
  }
}
```

---

## Error Responses

### Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Server Error (500)

```json
{
  "detail": "AI generation failed: API key invalid"
}
```

### Not Found (404)

```json
{
  "detail": "Page not found"
}
```

---

## Rate Limiting

- **Development**: No rate limiting
- **Production**: 10 requests per minute per IP

When rate limited:
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## Examples

### cURL Examples

**Generate Page:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Business",
    "industry": "technology",
    "target_audience": "Developers",
    "tone": "professional",
    "goal": "Get signups for beta"
  }'
```

**List Pages:**
```bash
curl -X GET "http://localhost:8000/api/v1/pages?limit=5"
```

**Export Page:**
```bash
curl -X GET "http://localhost:8000/api/v1/export/1" \
  -o landing-page.zip
```

### Python Example

```python
import requests

# Generate landing page
response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "name": "TechCorp",
        "industry": "technology",
        "target_audience": "Small businesses",
        "tone": "professional",
        "goal": "Generate leads"
    }
)

data = response.json()
print(f"Page ID: {data['page_id']}")
print(f"Preview: {data['preview_url']}")

# Download the page
page_id = data['landing_page_id']
zip_response = requests.get(f"http://localhost:8000/api/v1/export/{page_id}")
with open("landing-page.zip", "wb") as f:
    f.write(zip_response.content)
```

### JavaScript Example

```javascript
// Generate landing page
async function generatePage() {
  const response = await fetch('http://localhost:8000/api/v1/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'My Business',
      industry: 'technology',
      target_audience: 'Developers',
      tone: 'professional',
      goal: 'Get beta signups'
    })
  });
  
  const data = await response.json();
  console.log('Generated:', data.page_id);
  return data;
}
```

---

## WebSocket Support (Future)

Real-time generation progress updates (planned for v2.0):

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generate');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Progress: ${data.progress}%`);
};
```

---

*API Version: 1.0.0*  
*Last Updated: December 23, 2025*
