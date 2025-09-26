#!/bin/bash

# Script to set up the preview container system

echo "Setting up preview container system..."

# Create necessary directories
mkdir -p nginx preview-data

# Build the preview manager image
docker build -t sevdo-preview-manager -f Dockerfile.preview-manager .

# Update docker-compose
echo "Please add the preview services to your docker-compose.yml file"
echo "Refer to the provided docker-compose.yml modifications"

# Test the setup
echo "Testing Docker socket access..."
docker ps > /dev/null && echo "✓ Docker access OK" || echo "✗ Docker access failed"

echo "Setup complete!"
echo "Start with: docker-compose up -d preview-manager preview-proxy"