Write-Host "Starting BFAI Demo Mode..." -ForegroundColor Green
Write-Host "Analyzing sample eCommerce Workflow..." -ForegroundColor Cyan

# Check if python is available
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    python -m bfai analyze data/samples/ecommerce_workflow.csv --demo
} else {
    Write-Host "Error: Python not found. Please install Python 3.11+" -ForegroundColor Red
}

Read-Host -Prompt "Press Enter to exit"
