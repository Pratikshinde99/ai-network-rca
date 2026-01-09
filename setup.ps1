# AI-Powered Network RCA Platform - Setup Script
# Run this script to set up the project quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI-Powered Network RCA Platform" -ForegroundColor Cyan
Write-Host "Automated Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Check Azure Functions Core Tools
try {
    $funcVersion = func --version 2>&1
    Write-Host "✓ Azure Functions Core Tools found: $funcVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Azure Functions Core Tools not found" -ForegroundColor Red
    Write-Host "  Install from: https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "All prerequisites met!" -ForegroundColor Green
Write-Host ""

# Backend setup
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Set-Location backend

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create local.settings.json if it doesn't exist
if (-Not (Test-Path "local.settings.json")) {
    Write-Host "Creating local.settings.json..." -ForegroundColor Yellow
    Copy-Item "local.settings.json.example" "local.settings.json"
    
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit backend/local.settings.json" -ForegroundColor Yellow
    Write-Host "   Add your Azure OpenAI credentials:" -ForegroundColor Yellow
    Write-Host "   - AZURE_OPENAI_ENDPOINT" -ForegroundColor Yellow
    Write-Host "   - AZURE_OPENAI_API_KEY" -ForegroundColor Yellow
    Write-Host "   - AZURE_OPENAI_DEPLOYMENT" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✓ local.settings.json already exists" -ForegroundColor Green
}

Set-Location ..

# Frontend setup
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Set-Location frontend

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

# Create .env if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env created with default settings" -ForegroundColor Green
} else {
    Write-Host "✓ .env already exists" -ForegroundColor Green
}

Set-Location ..

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Edit backend/local.settings.json with your Azure OpenAI credentials" -ForegroundColor White
Write-Host ""
Write-Host "2. Start the backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Cyan
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "   func start" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. In a new terminal, start the frontend:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Cyan
Write-Host "   npm start" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "5. Run tests:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Cyan
Write-Host "   python test_backend.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Good luck with your demo! 🚀" -ForegroundColor Green
Write-Host ""
