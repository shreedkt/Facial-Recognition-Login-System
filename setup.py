#!/usr/bin/env python3
"""
Setup script for Facial Recognition Login System
Checks dependencies and environment setup
"""

import sys
import subprocess
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ pip is not installed")
        return False

def install_requirements():
    """Install required packages"""
    print("📥 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_opencv():
    """Check if OpenCV is properly installed"""
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} is installed")
        return True
    except ImportError:
        print("❌ OpenCV is not installed")
        return False

def check_camera():
    """Check camera access"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera access successful")
            cap.release()
            return True
        else:
            print("⚠️  Camera not accessible")
            return False
    except Exception as e:
        print(f"❌ Camera check failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['static/images', 'models']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")

def main():
    """Main setup function"""
    print("🔒 Facial Recognition Login System Setup")
    print("=" * 45)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check pip
    if not check_pip():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check OpenCV
    if not check_opencv():
        return False
    
    # Create directories
    create_directories()
    
    # Check camera
    check_camera()
    
    print("\n🚀 Setup complete!")
    print("Run 'python app.py' to start the application")
    print("Then open http://localhost:5000 in your browser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
