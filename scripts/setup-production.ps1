# Setup Production Environment Script (PowerShell)
# Usage: .\scripts\setup-production.ps1

$ErrorActionPreference = "Stop"

Write-Host "🔧 Setting up production environment..." -ForegroundColor Cyan

# Create production directories
Write-Host "📁 Creating production directories..." -ForegroundColor Blue
$directories = @("generated_pages", "logs", "output\themes")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    }
}

# Copy and configure environment file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  No .env file found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.production" ".env"
    Write-Host "⚠️  Please edit .env and add your API keys!" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Blue
python -m pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Run database migrations
Write-Host "🗄️  Running database migrations..." -ForegroundColor Blue
alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Database migration failed or no migrations needed" -ForegroundColor Yellow
}

# Test the setup
Write-Host "🧪 Testing configuration..." -ForegroundColor Blue
$testScript = @"
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = ['AI_PROVIDER', 'DATABASE_URL']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f"❌ Missing required environment variables: {', '.join(missing)}")
    exit(1)
else:
    print("✅ All required environment variables are set")
"@

$testScript | python

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Production environment setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Blue
    Write-Host "1. Edit .env and add your API keys"
    Write-Host "2. Run: uvicorn app.main:app --host 0.0.0.0 --port 8000"
    Write-Host "3. Or use Docker: docker-compose up -d"
} else {
    Write-Host "❌ Setup incomplete. Please check the errors above." -ForegroundColor Red
    exit 1
}
