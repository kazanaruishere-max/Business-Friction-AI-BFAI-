$VenvPython = "c:\PROJECT\BFAI\.venv\Scripts\python.exe"

Write-Host "BFAI Setup & Demo Runner" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

if (Test-Path $VenvPython) {
    Write-Host "Found local virtual environment Python at: $VenvPython" -ForegroundColor Green
    
    Write-Host "Step 1: Installing Dependencies..." -ForegroundColor Yellow
    # Installing without 'python -m pip' redundancy, just calling pip module directly via executable if possible, 
    # or using -m pip correctly.
    & $VenvPython -m pip install typer rich pandas pydantic google-generativeai
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Dependencies installed successfully!" -ForegroundColor Green
        
        Write-Host "Step 2: Running Demo..." -ForegroundColor Yellow
        & $VenvPython -m bfai analyze data/samples/ecommerce_workflow.csv --demo
    }
    else {
        Write-Host "Failed to install dependencies." -ForegroundColor Red
    }
}
else {
    Write-Host "Error: Could not find Python at $VenvPython" -ForegroundColor Red
    Write-Host "Please ensure you have a standard Python installation or a valid .venv folder." -ForegroundColor Gray
}

Read-Host -Prompt "Press Enter to exit"
