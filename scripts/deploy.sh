#!/bin/bash

# Deploy script for Telegram Content Parser & Analyzer

set -e

echo "🚀 Starting deployment..."

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "❌ Error: .env.prod file not found!"
    echo "Please create .env.prod file with production environment variables"
    exit 1
fi

# Load production environment variables
export $(cat .env.prod | grep -v '^#' | xargs)

# Build and start services
echo "📦 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🔄 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Service status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "🌐 Services are available at:"
echo "   - Frontend: http://${DOMAIN:-localhost}"
echo "   - API: http://${DOMAIN:-localhost}/api"
echo "   - API Docs: http://${DOMAIN:-localhost}/docs"

