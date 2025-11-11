# Simple script to start the dashboard
# Run this in two separate terminals:
# Terminal 1: python dashboard_backend.py
# Terminal 2: cd dashboard_frontend && npm start

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Spark Streaming Lab Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the dashboard, run these commands in TWO separate terminals:" -ForegroundColor Yellow
Write-Host ""
Write-Host "TERMINAL 1 (Backend):" -ForegroundColor Green
Write-Host "  python dashboard_backend.py" -ForegroundColor White
Write-Host ""
Write-Host "TERMINAL 2 (Frontend):" -ForegroundColor Green
Write-Host "  cd dashboard_frontend" -ForegroundColor White
Write-Host "  npm start" -ForegroundColor White
Write-Host ""
Write-Host "First time setup:" -ForegroundColor Yellow
Write-Host "  1. pip install -r requirements.txt" -ForegroundColor White
Write-Host "  2. cd dashboard_frontend" -ForegroundColor White
Write-Host "  3. npm install" -ForegroundColor White
Write-Host "  4. cd .." -ForegroundColor White
Write-Host ""
Write-Host "Then start both services as shown above." -ForegroundColor Yellow
Write-Host ""

