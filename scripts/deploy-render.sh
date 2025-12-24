#!/bin/bash

# Deploy to Render Script
# Make this executable with: chmod +x scripts/deploy-render.sh

set -e

echo "🚀 Deploying Landing Page Generator to Render..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if required environment variables are set
if [ -z "$RENDER_API_KEY" ]; then
    echo -e "${RED}❌ Error: RENDER_API_KEY is not set${NC}"
    echo "Please set it with: export RENDER_API_KEY=your_api_key"
    exit 1
fi

if [ -z "$RENDER_SERVICE_ID" ]; then
    echo -e "${RED}❌ Error: RENDER_SERVICE_ID is not set${NC}"
    echo "Please set it with: export RENDER_SERVICE_ID=your_service_id"
    exit 1
fi

echo -e "${BLUE}📦 Checking application...${NC}"

# Run tests
echo -e "${BLUE}🧪 Running tests...${NC}"
pytest tests/ -v --tb=short

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Tests failed! Aborting deployment.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Tests passed!${NC}"

# Trigger deployment on Render
echo -e "${BLUE}🔄 Triggering deployment on Render...${NC}"

RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $RENDER_API_KEY" \
    -H "Accept: application/json" \
    "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys")

DEPLOY_ID=$(echo $RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)

if [ -z "$DEPLOY_ID" ]; then
    echo -e "${RED}❌ Failed to trigger deployment${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi

echo -e "${GREEN}✅ Deployment triggered successfully!${NC}"
echo -e "${BLUE}Deploy ID: $DEPLOY_ID${NC}"
echo -e "${BLUE}Check status at: https://dashboard.render.com/${NC}"

echo ""
echo -e "${GREEN}🎉 Deployment initiated! Your application will be live in a few minutes.${NC}"
