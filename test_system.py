#!/usr/bin/env python3
"""
Test script for Facial Recognition Login System
Verifies all dependencies and basic functionality
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ Pillow (PIL)")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import sqlite3
        print(f"✅ SQLite3 {sqlite3.version}")
    except ImportError as e:
        print(f"❌ SQLite3 import failed: {e}")
        return False
    
    return True

def test_opencv_features():
    """Test OpenCV face detection capabilities"""
    print("\nTesting OpenCV features...")
    
    try:
        import cv2
        
        # Test face cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            print("❌ Face cascade classifier failed to load")
            return False
        else:
            print("✅ Face cascade classifier loaded successfully")
        
        # Test LBPH recognizer
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            print("✅ LBPH Face Recognizer available")
        except AttributeError:
            print("❌ LBPH Face Recognizer not available (opencv-contrib-python needed)")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")
        return False

def test_camera_access():
    """Test camera access"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        
        # Try to open camera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("⚠️  Camera not accessible (this is normal if no camera is connected)")
            return True  # Not a critical error
        
        # Try to read a frame
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            print("✅ Camera access successful")
            return True
        else:
            print("⚠️  Camera accessible but couldn't read frame")
            return True  # Not a critical error
            
    except Exception as e:
        print(f"⚠️  Camera test failed: {e}")
        return True  # Not a critical error

def test_directories():
    """Test required directories"""
    print("\nTesting directories...")
    
    directories = [
        'templates',
        'static',
        'static/images',
        'models'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}/ exists")
        else:
            print(f"❌ {directory}/ missing")
            return False
    
    return True

def test_templates():
    """Test template files"""
    print("\nTesting templates...")
    
    templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/register.html',
        'templates/login.html',
        'templates/dashboard.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} missing")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🔒 Facial Recognition Login System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("OpenCV Features Test", test_opencv_features),
        ("Camera Access Test", test_camera_access),
        ("Directory Structure Test", test_directories),
        ("Template Files Test", test_templates)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready.")
        print("\nTo start the application:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
