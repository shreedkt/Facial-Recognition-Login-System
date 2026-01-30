# 🪟 Windows Setup Guide - Facial Recognition Login System

This guide provides step-by-step instructions for setting up the facial recognition system on Windows.

## 📋 Prerequisites

### 1. Python Installation
- **Download**: Python 3.7+ from [python.org](https://python.org/downloads/)
- **Important**: ✅ Check "Add Python to PATH" during installation
- **Verify**: Open Command Prompt and run `python --version`

### 2. Visual C++ Build Tools (if needed)
- **Download**: [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- **Note**: Only needed if you get compilation errors during package installation

### 3. Git (optional)
- **Download**: [Git for Windows](https://git-scm.com/download/win)
- **Alternative**: Download project as ZIP file

## 🚀 Quick Setup (Recommended)

### Option 1: PowerShell Script (Recommended)
1. **Open PowerShell as Administrator**
2. **Navigate to project folder**:
   ```powershell
   cd "C:\path\to\opencv"
   ```
3. **Run setup script**:
   ```powershell
   .\setup_windows.ps1
   ```
4. **If execution policy error**:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\setup_windows.ps1
   ```

### Option 2: Batch Script
1. **Open Command Prompt**
2. **Navigate to project folder**:
   ```cmd
   cd "C:\path\to\opencv"
   ```
3. **Run setup script**:
   ```cmd
   setup_windows.bat
   ```

## 🔧 Manual Setup

If you prefer to set up manually or the scripts don't work:

### Step 1: Create Virtual Environment
```cmd
python -m venv venv
```

### Step 2: Activate Virtual Environment
```cmd
venv\Scripts\activate
```

### Step 3: Upgrade pip
```cmd
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies
```cmd
python -m pip install -r requirements.txt
```

### Step 5: Create Directories
```cmd
mkdir static\images
mkdir models
```

### Step 6: Test Installation
```cmd
python -c "import cv2; print('OpenCV', cv2.__version__, 'installed')"
```

## 🎯 Running the Application

### Start the Server
```cmd
python app.py
```

### Access the Application
- **URL**: http://localhost:5001
- **Admin Panel**: http://localhost:5001/admin

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. "Python is not recognized"
- **Solution**: Reinstall Python with "Add to PATH" checked
- **Alternative**: Add Python to PATH manually in System Environment Variables

#### 2. "Microsoft Visual C++ 14.0 is required"
- **Solution**: Install Visual C++ Build Tools
- **Link**: https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### 3. "Execution of scripts is disabled"
- **Solution**: Change PowerShell execution policy
- **Command**: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### 4. OpenCV Installation Fails
- **Solution 1**: Try installing OpenCV separately
  ```cmd
  pip install opencv-python
  pip install opencv-contrib-python
  ```
- **Solution 2**: Use conda instead of pip
  ```cmd
  conda install opencv
  ```

#### 5. Camera Not Working
- **Check**: Camera permissions in Windows Settings
- **Path**: Settings > Privacy > Camera
- **Solution**: Allow apps to access camera

#### 6. Port 5000 Already in Use
- **Note**: The app now runs on port 5001 by default
- **If still issues**: Change port in `app.py` line 238

### Camera Permissions
1. **Windows Settings** > **Privacy & Security** > **Camera**
2. **Allow apps to access your camera**: ON
3. **Allow desktop apps to access your camera**: ON

### Firewall Settings
If you can't access the app:
1. **Windows Security** > **Firewall & network protection**
2. **Allow an app through firewall**
3. **Add Python** if not listed

## 📁 Project Structure After Setup

```
opencv/
├── venv/                     # Virtual environment
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── setup_windows.ps1         # PowerShell setup script
├── setup_windows.bat         # Batch setup script
├── templates/                # HTML templates
├── static/images/            # User face images
├── models/                   # AI models
└── README.md                 # Documentation
```

## 🎮 Using the Application

### 1. Registration
1. Open http://localhost:5001
2. Click "Register Now"
3. Fill name and email
4. Position face in camera
5. Click "Capture Face & Register"

### 2. Login
1. Click "Login with Face"
2. Position face in camera
3. Click "Recognize Me"
4. Wait for recognition

### 3. Testing (Admin Panel)
1. Go to http://localhost:5001/admin
2. Use "Test Recognition" to see confidence scores
3. Debug recognition issues

## 💡 Tips for Better Recognition

### Registration Tips:
- **Good lighting**: Face should be well-lit
- **Face size**: Fill about 1/3 of the camera frame
- **Direct view**: Look straight at camera
- **No glasses**: Remove if possible for better accuracy

### Login Tips:
- **Same conditions**: Use similar lighting as registration
- **Same position**: Try to match registration pose
- **Single face**: Only one person in camera view

## ⚙️ Configuration

### Adjust Recognition Sensitivity
Edit `app.py` line 17:
```python
CONFIDENCE_THRESHOLD = 50  # Lower = stricter (30-70 range)
```

### Change Port
Edit `app.py` line 238:
```python
app.run(host='0.0.0.0', port=5002, debug=True, threaded=True)
```

## 🆘 Getting Help

### Check Logs
- Look at the Command Prompt/PowerShell where you ran `python app.py`
- Confidence scores and errors are displayed there

### Admin Panel
- Use http://localhost:5001/admin for testing
- Shows detailed recognition information

### File Issues
- Check that all files from the project are present
- Ensure `requirements.txt` is in the same folder as setup scripts

## 🎉 Success!

Once setup is complete, you should have:
- ✅ Python virtual environment
- ✅ All dependencies installed  
- ✅ Flask app running on port 5001
- ✅ Camera access working
- ✅ Face recognition system ready

**Happy face recognition!**
