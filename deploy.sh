#!/bin/bash
# Deployment script for AfriLens AI

set -e

echo "🚀 AfriLens AI Deployment Script"
echo "=================================="

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✓ Docker found"
    
    echo ""
    echo "Building Docker images..."
    docker-compose build
    
    echo ""
    echo "Starting services..."
    docker-compose up -d
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "Services:"
    echo "  - Frontend: http://localhost"
    echo "  - Backend: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo ""
    echo "View logs: docker-compose logs -f"
    echo "Stop: docker-compose down"
else
    echo "❌ Docker not found. Please install Docker first."
    echo ""
    echo "Alternative: Deploy to cloud platform (see DEPLOY.md)"
    exit 1
fi
