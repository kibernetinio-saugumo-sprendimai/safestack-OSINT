# SafeStack OSINT Environment Setup Script
# Run this in PowerShell. Administrator privileges are not normally required.

Write-Host "--- SafeStack OSINT Setup ---" -ForegroundColor Cyan

# 1. Python Dependencies
Write-Host "`n[1/2] Installing pinned Python dependencies..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install Python dependencies via pip." -ForegroundColor Red
} else {
    Write-Host "Python dependencies installed successfully." -ForegroundColor Green
}

# 2. Create Audit Log Directory
Write-Host "`n[2/2] Preparing audit directories..." -ForegroundColor Yellow
$logDir = Join-Path (Get-Location) "logs\audit"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
    Write-Host "Created $logDir" -ForegroundColor Green
} else {
    Write-Host "Audit directory already exists." -ForegroundColor Green
}

Write-Host "`nSetup process complete." -ForegroundColor Cyan
