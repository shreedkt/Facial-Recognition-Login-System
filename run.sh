#!/bin/bash

# Facial Recognition Login System - Setup and Run Script

echo "🔒 Facial Recognition Login System Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check OpenCV installation
echo "🔍 Verifying OpenCV installation..."
python3 -c "import cv2; print(f'✅ OpenCV {cv2.__version__} installed successfully')" || {
    echo "❌ OpenCV installation failed. Please check the error above."
    exit 1
}

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/images
mkdir -p models
echo "✅ Directories created"

# Check camera access
echo "📹 Checking camera access..."
python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('✅ Camera access successful')
    cap.release()
else:
    print('⚠️  Camera not accessible. Please check camera permissions.')
"

echo ""
echo "🚀 Setup complete! Starting the application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python3 app.py
