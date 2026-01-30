from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import cv2
import sqlite3
import os
import numpy as np
import base64
from datetime import datetime
import pickle

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
UPLOAD_FOLDER = 'static/images'
DATABASE = 'users.db'
CONFIDENCE_THRESHOLD = 50  # Lower is stricter (0-150 range)

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models', exist_ok=True)

# Initialize face recognizer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Global variables for camera
camera = None

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  image_path TEXT,
                  face_encoding BLOB,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_camera():
    """Get camera instance"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def detect_faces(image):
    """Detect faces in an image"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces, gray

def save_user_face(name, email, face_image):
    """Save user face data to database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Save image
    image_filename = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
    cv2.imwrite(image_path, face_image)
    
    # Extract face features for recognition
    faces, gray = detect_faces(face_image)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        
        # Ensure face is large enough for good recognition
        if w < 100 or h < 100:
            conn.close()
            return False, "Face too small. Please move closer to the camera."
        
        # Extract face region with some padding
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(gray.shape[1] - x, w + 2 * padding)
        h = min(gray.shape[0] - y, h + 2 * padding)
        
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize face to standard size for better recognition
        face_roi = cv2.resize(face_roi, (200, 200))
        
        face_encoding = pickle.dumps(face_roi)
        
        try:
            c.execute("INSERT INTO users (name, email, image_path, face_encoding) VALUES (?, ?, ?, ?)",
                     (name, email, image_path, face_encoding))
            conn.commit()
            user_id = c.lastrowid
            
            # Update face recognizer
            update_face_recognizer()
            
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Email already exists"
    
    conn.close()
    return False, "No face detected"

def update_face_recognizer():
    """Update the face recognizer with all users"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, face_encoding FROM users")
    users = c.fetchall()
    conn.close()
    
    if users:
        faces = []
        labels = []
        
        for user_id, face_encoding_blob in users:
            face_encoding = pickle.loads(face_encoding_blob)
            faces.append(face_encoding)
            labels.append(user_id)
        
        recognizer.train(faces, np.array(labels))
        recognizer.save('models/face_recognizer.yml')

def recognize_face(image):
    """Recognize face in image"""
    faces, gray = detect_faces(image)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        
        # Ensure face region is large enough for recognition
        if w < 100 or h < 100:
            return False, None, None, None
        
        # Extract face region with padding (same as registration)
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(gray.shape[1] - x, w + 2 * padding)
        h = min(gray.shape[0] - y, h + 2 * padding)
        
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize to standard size (same as registration)
        face_roi = cv2.resize(face_roi, (200, 200))
        
        # Load the trained model if it exists
        if os.path.exists('models/face_recognizer.yml'):
            recognizer.read('models/face_recognizer.yml')
            label, confidence = recognizer.predict(face_roi)
            
            # Much stricter confidence threshold (lower is better)
            # Values typically range from 0-150, we want very low confidence for good match
            print(f"Recognition confidence: {confidence}")  # Debug info
            
            if confidence < CONFIDENCE_THRESHOLD:  # Use configurable threshold
                # Get user details
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                c.execute("SELECT name, email FROM users WHERE id = ?", (label,))
                user = c.fetchone()
                conn.close()
                
                if user:
                    return True, user[0], user[1], confidence
    
    return False, None, None, None

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register')
def register():
    """Registration page"""
    return render_template('register.html')

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_name' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session['user_name'])

@app.route('/admin')
def admin():
    """Admin page for testing"""
    return render_template('admin.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    def generate_frames():
        camera = get_camera()
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # Detect faces and draw rectangles
                faces, _ = detect_faces(frame)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_face', methods=['POST'])
def capture_face():
    """Capture face from webcam for registration"""
    name = request.form['name']
    email = request.form['email']
    
    if not name or not email:
        return jsonify({'success': False, 'message': 'Name and email are required'})
    
    camera = get_camera()
    ret, frame = camera.read()
    
    if ret:
        success, result = save_user_face(name, email, frame)
        if success:
            return jsonify({'success': True, 'message': 'Registration successful!'})
        else:
            return jsonify({'success': False, 'message': result})
    
    return jsonify({'success': False, 'message': 'Failed to capture image'})

@app.route('/recognize_face', methods=['POST'])
def recognize_face_route():
    """Recognize face for login"""
    camera = get_camera()
    ret, frame = camera.read()
    
    if ret:
        success, name, email, confidence = recognize_face(frame)
        if success:
            session['user_name'] = name
            session['user_email'] = email
            return jsonify({
                'success': True, 
                'name': name, 
                'message': f'{name} detected (confidence: {confidence:.1f}), logging in...',
                'redirect': url_for('dashboard')
            })
        else:
            return jsonify({'success': False, 'message': 'Face not recognized or confidence too low'})
    
    return jsonify({'success': False, 'message': 'Failed to capture image'})

@app.route('/test_recognition', methods=['POST'])
def test_recognition():
    """Test recognition with confidence info (for debugging)"""
    camera = get_camera()
    ret, frame = camera.read()
    
    if ret:
        faces, gray = detect_faces(frame)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            
            if w >= 100 and h >= 100:
                # Same preprocessing as recognition
                padding = 20
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(gray.shape[1] - x, w + 2 * padding)
                h = min(gray.shape[0] - y, h + 2 * padding)
                
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (200, 200))
                
                if os.path.exists('models/face_recognizer.yml'):
                    recognizer.read('models/face_recognizer.yml')
                    label, confidence = recognizer.predict(face_roi)
                    
                    # Get user details
                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    c.execute("SELECT name, email FROM users WHERE id = ?", (label,))
                    user = c.fetchone()
                    conn.close()
                    
                    if user:
                        return jsonify({
                            'success': True,
                            'name': user[0],
                            'confidence': confidence,
                            'threshold': CONFIDENCE_THRESHOLD,
                            'would_login': confidence < CONFIDENCE_THRESHOLD,
                            'message': f'Detected: {user[0]} (confidence: {confidence:.1f}, threshold: {CONFIDENCE_THRESHOLD})'
                        })
        
        return jsonify({'success': False, 'message': 'No face detected or face too small'})
    
    return jsonify({'success': False, 'message': 'Failed to capture image'})

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
