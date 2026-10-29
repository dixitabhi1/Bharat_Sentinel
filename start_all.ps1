# Bharat Sentinel Launcher Script
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   BHARAT SENTINEL — MULTI-AGENT OSINT COMMAND PLATFORM          " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "[1/2] Starting Python FastAPI Backend on http://localhost:8000..." -ForegroundColor Green

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting Vite Frontend on http://localhost:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot/frontend'; npm run dev"

Write-Host "`nBharat Sentinel is launching! Open http://localhost:5173 in your browser." -ForegroundColor Yellow
