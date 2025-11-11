# PowerShell script to run the dashboard (backend + frontend)
# This script starts both the Flask backend and React frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Spark Streaming Lab - Dashboard Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow

# Check Python packages
try {
    python -c "import flask" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
    } else {
        Write-Host "[OK] Python dependencies installed" -ForegroundColor Green
    }
} catch {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check Node.js
try {
    node --version 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Node.js installed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
if (-not (Test-Path "dashboard_frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location dashboard_frontend
    npm install
    Set-Location ..
    Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend API will run on: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend Dashboard will run on: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both services" -ForegroundColor Yellow
Write-Host ""

# Start backend in background
Write-Host "Starting Flask backend..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python dashboard_backend.py
}

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "Starting React frontend..." -ForegroundColor Green
Set-Location dashboard_frontend
npm start

# Cleanup when script exits
Set-Location ..
Stop-Job $backendJob
Remove-Job $backendJob

