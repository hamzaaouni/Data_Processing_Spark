#!/bin/bash
# Bash script to run Spark Lab in Docker

echo "========================================"
echo "Spark Streaming Lab - Docker Runner"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker."
    exit 1
fi

echo "✓ Docker is running"
echo ""
echo "Building and starting Spark Lab container..."
echo ""

# Build and run with docker-compose
docker-compose up --build

echo ""
echo "Lab completed!"

