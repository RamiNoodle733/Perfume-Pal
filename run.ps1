# Perfume Pal - Quick Start Script
# This script starts the server and opens your browser

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  🌸 Starting Perfume Pal..." -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Load environment variables
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#].+?)=(.+)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "env:$key" -Value $value
    }
}

Write-Host "✓ Environment variables loaded" -ForegroundColor Green
Write-Host ""
Write-Host "Server starting at: http://localhost:8080" -ForegroundColor Yellow
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Wait a moment then open browser
Start-Sleep -Seconds 5
Start-Process "http://localhost:8080"

# Start the server
& .\venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

