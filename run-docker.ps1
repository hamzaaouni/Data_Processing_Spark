# PowerShell script to run Spark Lab in Docker
# This avoids winutils.exe issues on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Spark Streaming Lab - Docker Runner" -ForegroundColor Cyan
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
Write-Host "Building and starting Spark Lab container..." -ForegroundColor Yellow
Write-Host "   (This may take a few minutes on first run)" -ForegroundColor Gray
Write-Host ""

# Stop and remove existing container if it exists
Write-Host "Cleaning up any existing containers..." -ForegroundColor Gray
docker-compose down 2>&1 | Out-Null

# Build and run with docker-compose
Write-Host "Building Docker image and starting container..." -ForegroundColor Yellow
Write-Host ""
docker-compose up --build

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Lab completed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "WARNING: Container exited with errors. Check the output above." -ForegroundColor Yellow
}
