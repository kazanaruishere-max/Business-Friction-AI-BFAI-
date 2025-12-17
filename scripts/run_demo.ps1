$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   BFAI - BUSINESS FRICTION AI - DEMO" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Install/Update Environment
Write-Host "[1/4] Checking Environment..." -ForegroundColor Yellow
$PythonPath = ".venv/Scripts/python.exe"

if (-not (Test-Path $PythonPath)) {
    Write-Host "Virtual environment not found. Please run 'poetry install' first." -ForegroundColor Red
    exit 1
}
Write-Host "Environment OK." -ForegroundColor Green
Write-Host ""

# 2. Analyze
Write-Host "[2/4] Running Analysis Pipeline..." -ForegroundColor Yellow
$SampleLog = "bfai/examples/sample_logs.csv"
$JsonOutput = "analysis_output.json"

& $PythonPath -m bfai analyze $SampleLog --output $JsonOutput --verbose
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "Analysis complete. Output saved to $JsonOutput" -ForegroundColor Green
Write-Host ""

# 3. Explain
Write-Host "[3/4] Explaining Case 'ord-002'..." -ForegroundColor Yellow
& $PythonPath -m bfai explain $SampleLog --case-id "ord-002"
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "Explanation complete." -ForegroundColor Green
Write-Host ""

# 4. Report
Write-Host "[4/4] Generating Report..." -ForegroundColor Yellow
$ReportOutput = "final_report.md"
& $PythonPath -m bfai report $SampleLog --output $ReportOutput
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   DEMO COMPLETED SUCCESSFULLY" -ForegroundColor Cyan
Write-Host "   Report available at: $ReportOutput" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
