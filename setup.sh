#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}AI-Driven Threat Detection System Setup${NC}"
echo "========================================"

# Check system requirements
echo -e "\n${YELLOW}Checking system requirements...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ System requirements met${NC}"

# Create environment files if they don't exist
echo -e "\n${YELLOW}Setting up environment files...${NC}"

if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate random passwords
    POSTGRES_PASSWORD=$(openssl rand -base64 12)
    MONGO_PASSWORD=$(openssl rand -base64 12)
    API_SECRET_KEY=$(openssl rand -base64 32)
    GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 12)
    
    # Update .env file
    sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$POSTGRES_PASSWORD/" .env
    sed -i "s/MONGO_PASSWORD=.*/MONGO_PASSWORD=$MONGO_PASSWORD/" .env
    sed -i "s/API_SECRET_KEY=.*/API_SECRET_KEY=$API_SECRET_KEY/" .env
    sed -i "s/GRAFANA_ADMIN_PASSWORD=.*/GRAFANA_ADMIN_PASSWORD=$GRAFANA_ADMIN_PASSWORD/" .env
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env file..."
    cp frontend/.env.example frontend/.env
fi

echo -e "${GREEN}✓ Environment files created${NC}"

# Create necessary directories
echo -e "\n${YELLOW}Creating required directories...${NC}"
mkdir -p ml_models
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"

# Pull Docker images
echo -e "\n${YELLOW}Pulling Docker images...${NC}"
docker-compose pull

# Build and start services
echo -e "\n${YELLOW}Building and starting services...${NC}"
docker-compose up -d --build

# Wait for services to be ready
echo -e "\n${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Initialize database
echo -e "\n${YELLOW}Initializing database...${NC}"
docker-compose exec backend alembic upgrade head

echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "\nAccess the system at:"
echo -e "Frontend: ${GREEN}http://localhost${NC}"
echo -e "Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "Grafana Dashboard: ${GREEN}http://localhost:3000${NC}"
echo -e "\nDefault credentials can be found in the .env file"
