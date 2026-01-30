# Facial Recognition Login System - Windows Setup Script
# PowerShell script for automated setup on Windows

param(
    [switch]$Force = $false
)

Write-Host "🔒 Facial Recognition Login System - Windows Setup" -ForegroundColor Cyan
Write-Host "=" * 55 -ForegroundColor Cyan

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to write colored output
function Write-Status($Message, $Type = "Info") {
    switch ($Type) {
        "Success" { Write-Host "✅ $Message" -ForegroundColor Green }
        "Error" { Write-Host "❌ $Message" -ForegroundColor Red }
        "Warning" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "Info" { Write-Host "ℹ️  $Message" -ForegroundColor Blue }
        default { Write-Host "$Message" }
    }
}

# Check if Python is installed
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow

if (-not (Test-Command "python")) {
    Write-Status "Python is not installed or not in PATH" "Error"
    Write-Status "Please install Python 3.7+ from https://python.org/downloads/" "Error"
    Write-Status "Make sure to check 'Add Python to PATH' during installation" "Warning"
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Status "Python found: $pythonVersion" "Success"

# Check Python version
$versionString = $pythonVersion -replace "Python ", ""
$version = [Version]$versionString
if ($version -lt [Version]"3.7") {
    Write-Status "Python 3.7 or higher is required. Current version: $versionString" "Error"
    exit 1
}

# Check if we're in the correct directory
if (-not (Test-Path "requirements.txt")) {
    Write-Status "requirements.txt not found in current directory" "Error"
    Write-Status "Please run this script from the project root directory" "Error"
    exit 1
}

Write-Status "Found requirements.txt" "Success"

# Check if virtual environment exists
if (Test-Path "venv") {
    if ($Force) {
        Write-Status "Removing existing virtual environment..." "Warning"
        Remove-Item -Recurse -Force "venv"
    } else {
        Write-Status "Virtual environment already exists" "Info"
        Write-Status "Use -Force parameter to recreate it" "Info"
    }
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    try {
        python -m venv venv
        Write-Status "Virtual environment created successfully" "Success"
    } catch {
        Write-Status "Failed to create virtual environment: $_" "Error"
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow

$activateScript = "venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Status "Virtual environment activation script not found" "Error"
    exit 1
}

# Check execution policy
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Status "PowerShell execution policy is Restricted" "Warning"
    Write-Status "Temporarily allowing script execution..." "Info"
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
}

try {
    & $activateScript
    Write-Status "Virtual environment activated" "Success"
} catch {
    Write-Status "Failed to activate virtual environment: $_" "Error"
    Write-Status "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" "Info"
    exit 1
}

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    Write-Status "pip upgraded successfully" "Success"
} catch {
    Write-Status "Failed to upgrade pip: $_" "Warning"
}

# Install requirements
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
Write-Status "This may take a few minutes, especially for OpenCV..." "Info"

try {
    python -m pip install -r requirements.txt
    Write-Status "Dependencies installed successfully" "Success"
} catch {
    Write-Status "Failed to install some dependencies: $_" "Error"
    Write-Status "You may need to install Visual C++ Build Tools" "Info"
    Write-Status "Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/" "Info"
    exit 1
}

# Verify OpenCV installation
Write-Host "🔍 Verifying OpenCV installation..." -ForegroundColor Yellow
try {
    $opencvVersion = python -c "import cv2; print(cv2.__version__)" 2>&1
    Write-Status "OpenCV $opencvVersion installed successfully" "Success"
} catch {
    Write-Status "OpenCV verification failed: $_" "Error"
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating project directories..." -ForegroundColor Yellow
$directories = @("static\images", "models")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Status "Created directory: $dir" "Success"
    } else {
        Write-Status "Directory already exists: $dir" "Info"
    }
}

# Test camera access (optional)
Write-Host "📹 Testing camera access..." -ForegroundColor Yellow
try {
    $cameraTest = python -c @"
import cv2
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print('Camera accessible')
        cap.release()
        exit(0)
    else:
        print('Camera not accessible')
        exit(1)
except Exception as e:
    print(f'Camera test failed: {e}')
    exit(1)
"@ 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Status "Camera access test passed" "Success"
    } else {
        Write-Status "Camera not accessible: $cameraTest" "Warning"
        Write-Status "This is normal if no camera is connected" "Info"
    }
} catch {
    Write-Status "Camera test failed: $_" "Warning"
}

# Final setup completion
Write-Host ""
Write-Host "🚀 Setup completed successfully!" -ForegroundColor Green
Write-Host "=" * 55 -ForegroundColor Cyan

Write-Host ""
Write-Status "To start the application:" "Info"
Write-Host "1. Make sure you're in the project directory" -ForegroundColor White
Write-Host "2. Run: python app.py" -ForegroundColor White
Write-Host "3. Open your browser to: http://localhost:5001" -ForegroundColor White
Write-Host ""

Write-Status "Virtual environment location: $(Get-Location)\venv" "Info"
Write-Status "To activate manually: venv\Scripts\Activate.ps1" "Info"
Write-Status "To deactivate: deactivate" "Info"

Write-Host ""
Write-Host "📚 Additional Resources:" -ForegroundColor Yellow
Write-Host "- README.md - Complete documentation" -ForegroundColor White
Write-Host "- PROJECT_SUMMARY.md - Quick overview" -ForegroundColor White
Write-Host "- FIXES_APPLIED.md - Recent improvements" -ForegroundColor White

Write-Host ""
Write-Status "Ready to run facial recognition system! 🎉" "Success"

# Ask if user wants to start the app immediately
$response = Read-Host "Would you like to start the application now? (y/N)"
if ($response -match "^[Yy]") {
    Write-Host ""
    Write-Status "Starting the application..." "Info"
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    try {
        python app.py
    } catch {
        Write-Status "Application stopped" "Info"
    }
}
