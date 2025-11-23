# Check if Python 3.11 is available
$py311 = Get-Command py -ErrorAction SilentlyContinue
if ($py311) {
    $version = py -3.11 --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Python 3.11 not found via 'py' launcher. Please install it first." -ForegroundColor Red
        exit 1
    }
    Write-Host "Found $version" -ForegroundColor Green
} else {
    Write-Host "Python launcher 'py' not found." -ForegroundColor Red
    exit 1
}

# Remove old venv
if (Test-Path ".venv") {
    Write-Host "Removing old .venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

# Create new venv
Write-Host "Creating new virtual environment with Python 3.11..." -ForegroundColor Cyan
py -3.11 -m venv .venv

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Done! Environment setup complete." -ForegroundColor Green
