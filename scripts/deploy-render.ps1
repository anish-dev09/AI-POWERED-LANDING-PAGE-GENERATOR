# Deploy to Render Script (PowerShell)
# Usage: .\scripts\deploy-render.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying Landing Page Generator to Render..." -ForegroundColor Cyan

# Check if required environment variables are set
if (-not $env:RENDER_API_KEY) {
    Write-Host "❌ Error: RENDER_API_KEY is not set" -ForegroundColor Red
    Write-Host "Please set it with: `$env:RENDER_API_KEY='your_api_key'" -ForegroundColor Yellow
    exit 1
}

if (-not $env:RENDER_SERVICE_ID) {
    Write-Host "❌ Error: RENDER_SERVICE_ID is not set" -ForegroundColor Red
    Write-Host "Please set it with: `$env:RENDER_SERVICE_ID='your_service_id'" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Checking application..." -ForegroundColor Blue

# Run tests
Write-Host "🧪 Running tests..." -ForegroundColor Blue
try {
    pytest tests/ -v --tb=short
    if ($LASTEXITCODE -ne 0) {
        throw "Tests failed"
    }
} catch {
    Write-Host "❌ Tests failed! Aborting deployment." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Tests passed!" -ForegroundColor Green

# Trigger deployment on Render
Write-Host "🔄 Triggering deployment on Render..." -ForegroundColor Blue

$headers = @{
    "Authorization" = "Bearer $env:RENDER_API_KEY"
    "Accept" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "https://api.render.com/v1/services/$env:RENDER_SERVICE_ID/deploys" `
        -Method Post `
        -Headers $headers
    
    Write-Host "✅ Deployment triggered successfully!" -ForegroundColor Green
    Write-Host "Deploy ID: $($response.id)" -ForegroundColor Blue
    Write-Host "Check status at: https://dashboard.render.com/" -ForegroundColor Blue
} catch {
    Write-Host "❌ Failed to trigger deployment" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Deployment initiated! Your application will be live in a few minutes." -ForegroundColor Green
