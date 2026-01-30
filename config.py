# Configuration for the Facial Recognition Login System

# Flask Configuration
DEBUG = True
SECRET_KEY = 'your-secret-key-change-this-in-production'
HOST = '0.0.0.0'
PORT = 5000

# Database Configuration
DATABASE_PATH = 'users.db'

# File Storage Configuration
UPLOAD_FOLDER = 'static/images'
MODEL_FOLDER = 'models'

# Face Recognition Configuration
CONFIDENCE_THRESHOLD = 100  # Lower means stricter matching
CASCADE_FILE = 'haarcascade_frontalface_default.xml'

# Camera Configuration
CAMERA_INDEX = 0  # 0 for default camera, 1 for external camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Security Configuration
MAX_LOGIN_ATTEMPTS = 5
SESSION_TIMEOUT = 3600  # 1 hour in seconds
