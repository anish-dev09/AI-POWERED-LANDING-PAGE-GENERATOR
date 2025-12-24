#!/bin/bash

# Setup Production Environment Script

set -e

echo "🔧 Setting up production environment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Create production directories
echo -e "${BLUE}📁 Creating production directories...${NC}"
mkdir -p generated_pages
mkdir -p logs
mkdir -p output/themes

# Copy and configure environment file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.production .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your API keys!${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo -e "${BLUE}🗄️  Running database migrations...${NC}"
alembic upgrade head

# Create initial data (optional)
echo -e "${BLUE}📊 Setting up initial data...${NC}"
python -c "from app.database import init_db; init_db()"

# Test the setup
echo -e "${BLUE}🧪 Testing configuration...${NC}"
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = ['AI_PROVIDER', 'DATABASE_URL']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f'❌ Missing required environment variables: {', '.join(missing)}')
    exit(1)
else:
    print('✅ All required environment variables are set')
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Production environment setup complete!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Edit .env and add your API keys"
    echo "2. Run: uvicorn app.main:app --host 0.0.0.0 --port 8000"
    echo "3. Or use Docker: docker-compose up -d"
else
    echo -e "${RED}❌ Setup incomplete. Please check the errors above.${NC}"
    exit 1
fi
