$VenvPython = "c:\Users\Lenovo\PROJECT\BFAI\.venv\Scripts\python.exe"

Write-Host "BFAI: Full Feature Demo" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $VenvPython) {
    # 1. Standard Analysis
    Write-Host "[1/3] Running General Workflow Analysis..." -ForegroundColor Yellow
    & $VenvPython -m bfai analyze data/samples/ecommerce_workflow.csv --demo
    Write-Host ""

    # 2. Case Deep Dive
    Write-Host "[2/3] Deep Diving into Case 'ord-102' (Payment Retry Loop)..." -ForegroundColor Yellow
    & $VenvPython -m bfai explain data/samples/ecommerce_workflow.csv ord-102
    Write-Host ""

    # 3. Report Generation
    Write-Host "[3/3] Generating PDF/Markdown Report..." -ForegroundColor Yellow
    & $VenvPython -m bfai report data/samples/ecommerce_workflow.csv --output demo_report.md
    
    if (Test-Path "demo_report.md") {
        $ReportPath = (Get-Item "demo_report.md").FullName
        Write-Host "[OK] Report generated at $ReportPath" -ForegroundColor Green
        Get-Content "demo_report.md" | Select-Object -First 10
    }
}
else {
    Write-Host "Error: Virtual environment not found." -ForegroundColor Red
}

Write-Host ""
Read-Host -Prompt "Demo Complete. Press Enter to exit"
