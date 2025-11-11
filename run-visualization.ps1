# PowerShell script to run visualization in Docker
# This creates visualizations from the Spark streaming lab data

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Spark Streaming Lab - Visualization" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
docker info 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker is running" -ForegroundColor Green
} else {
    Write-Host "ERROR: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    Write-Host "   Then run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Running visualization script in Docker..." -ForegroundColor Yellow
Write-Host ""

# Create visualizations directory if it doesn't exist
if (-not (Test-Path "visualizations")) {
    New-Item -ItemType Directory -Path "visualizations" | Out-Null
}

# Run visualization in Docker container
docker-compose run --rm spark-lab python visualize_results.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Visualization completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Visualizations saved to: .\visualizations\" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "WARNING: Visualization script exited with errors." -ForegroundColor Yellow
}

