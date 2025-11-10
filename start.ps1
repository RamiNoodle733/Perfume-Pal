# Perfume Pal - Quick Start Script
# This script helps you set up and run the project locally

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "    Perfume Pal - Quick Start Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "    Environment Configuration" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
    Write-Host "`nCurrent environment variables:" -ForegroundColor Yellow
    Get-Content .env | ForEach-Object {
        if ($_ -and !$_.StartsWith("#")) {
            $parts = $_ -split "=", 2
            if ($parts[0] -like "*KEY*" -or $parts[0] -like "*SECRET*") {
                Write-Host "  $($parts[0])=****" -ForegroundColor Gray
            } else {
                Write-Host "  $_" -ForegroundColor Gray
            }
        }
    }
} else {
    Write-Host "✗ .env file not found" -ForegroundColor Red
    Write-Host "`nCreating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host "`n⚠️  IMPORTANT: Please edit .env and add your API keys!" -ForegroundColor Yellow
    Write-Host "   Required variables:" -ForegroundColor Yellow
    Write-Host "   - GOOGLE_API_KEY (get from https://aistudio.google.com/app/apikey)" -ForegroundColor Yellow
    Write-Host "   - GOOGLE_CLOUD_PROJECT (your GCP project ID)" -ForegroundColor Yellow
    
    $response = Read-Host "`nWould you like to open .env file now? (y/n)"
    if ($response -eq "y") {
        notepad .env
    }
}

# Check if API key is set
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "    Validation" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$envContent = Get-Content ".env" -Raw
if ($envContent -match "GOOGLE_API_KEY=your-" -or $envContent -notmatch "GOOGLE_API_KEY=\w+") {
    Write-Host "⚠️  WARNING: GOOGLE_API_KEY not configured!" -ForegroundColor Yellow
    Write-Host "   The application will not work without a valid API key." -ForegroundColor Yellow
    Write-Host "   Get your key from: https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
} else {
    Write-Host "✓ GOOGLE_API_KEY appears to be configured" -ForegroundColor Green
}

# Offer to run tests
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "    Testing" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$runTests = Read-Host "Would you like to run tests? (y/n)"
if ($runTests -eq "y") {
    Write-Host "`nRunning tests..." -ForegroundColor Yellow
    pytest tests/ -v
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  Some tests failed" -ForegroundColor Yellow
    }
}

# Final instructions
Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "    Setup Complete!" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Green
Write-Host "  1. Make sure your .env file has valid API keys" -ForegroundColor White
Write-Host "  2. Run: " -NoNewline -ForegroundColor White
Write-Host "uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload" -ForegroundColor Cyan
Write-Host "  3. Open: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick commands:" -ForegroundColor Yellow
Write-Host "  Start server:    uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host "  Run tests:       pytest tests/ -v" -ForegroundColor Gray
Write-Host "  Build Docker:    docker build -t perfume-pal ." -ForegroundColor Gray
Write-Host "  Deploy to Cloud: gcloud run deploy perfume-pal --source ." -ForegroundColor Gray
Write-Host ""

$startNow = Read-Host "Would you like to start the server now? (y/n)"
if ($startNow -eq "y") {
    Write-Host "`nStarting Perfume Pal server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
}
