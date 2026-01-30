@echo off
REM Facial Recognition Login System - Windows Batch Setup Script
REM Simple batch file for Command Prompt users

echo.
echo ============================================================
echo 🔒 Facial Recognition Login System - Windows Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org/downloads/
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found in current directory
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo ✅ Found requirements.txt

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ℹ️  Virtual environment already exists
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Upgrade pip
echo.
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo 📥 Installing dependencies...
echo This may take a few minutes, especially for OpenCV...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo You may need to install Visual C++ Build Tools
    echo Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Verify OpenCV
echo.
echo 🔍 Verifying OpenCV installation...
python -c "import cv2; print('✅ OpenCV', cv2.__version__, 'installed successfully')"
if errorlevel 1 (
    echo ❌ OpenCV verification failed
    pause
    exit /b 1
)

REM Create directories
echo.
echo 📁 Creating project directories...
if not exist "static\images" mkdir "static\images"
if not exist "models" mkdir "models"
echo ✅ Directories created

REM Test camera (optional)
echo.
echo 📹 Testing camera access...
python -c "import cv2; cap = cv2.VideoCapture(0); print('✅ Camera accessible' if cap.isOpened() else '⚠️  Camera not accessible'); cap.release()" 2>nul
if errorlevel 1 (
    echo ⚠️  Camera test failed - this is normal if no camera is connected
)

REM Setup complete
echo.
echo ============================================================
echo 🚀 Setup completed successfully!
echo ============================================================
echo.
echo To start the application:
echo 1. Make sure you're in the project directory
echo 2. Run: python app.py
echo 3. Open your browser to: http://localhost:5001
echo.
echo Virtual environment location: %CD%\venv
echo To activate manually: venv\Scripts\activate.bat
echo To deactivate: deactivate
echo.
echo 📚 Additional Resources:
echo - README.md - Complete documentation
echo - PROJECT_SUMMARY.md - Quick overview
echo - FIXES_APPLIED.md - Recent improvements
echo.

set /p "start=Would you like to start the application now? (y/N): "
if /i "%start%"=="y" (
    echo.
    echo Starting the application...
    echo Press Ctrl+C to stop the server
    echo.
    python app.py
)

echo.
echo ✅ Ready to run facial recognition system! 🎉
pause
