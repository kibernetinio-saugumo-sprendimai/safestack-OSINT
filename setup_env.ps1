# SafeStack OSINT Environment Setup Script
# Run this in PowerShell with Administrator privileges if installing minisign

Write-Host "--- SafeStack OSINT Setup ---" -ForegroundColor Cyan

# 1. Python Dependencies
Write-Host "`n[1/3] Installing Python dependencies (dnspython, requests, cryptography)..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Python dependencies via pip." -ForegroundColor Red
} else {
    Write-Host "Python dependencies installed successfully." -ForegroundColor Green
}

# 2. Check for minisign
Write-Host "`n[2/3] Checking for minisign..." -ForegroundColor Yellow
if (Get-Command "minisign" -ErrorAction SilentlyContinue) {
    Write-Host "minisign is already installed." -ForegroundColor Green
} else {
    Write-Host "minisign is NOT found." -ForegroundColor Yellow
    Write-Host "To install minisign on Windows:"
    Write-Host "1. Download it from: https://jedisct1.github.io/minisign/"
    Write-Host "2. Extract and add the directory to your PATH."
    Write-Host "Alternatively, if you have 'scoop' installed: scoop install minisign"
}

# 3. Create Audit Log Directory
Write-Host "`n[3/3] Preparing audit directories..." -ForegroundColor Yellow
$logDir = Join-Path (Get-Location) "logs\audit"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
    Write-Host "Created $logDir" -ForegroundColor Green
} else {
    Write-Host "Audit directory already exists." -ForegroundColor Green
}

Write-Host "`nSetup process complete." -ForegroundColor Cyan
