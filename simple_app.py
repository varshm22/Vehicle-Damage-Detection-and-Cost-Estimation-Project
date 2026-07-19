"""
Simplified Car Damage Detection App
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from datetime import datetime
import uuid

from models.saved_model.damage_model import DamageDetectionModel

model = DamageDetectionModel()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('database/car_damage.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.context_processor
def inject_user():
    return dict(
        current_user_id=session.get('user_id'),
        current_user_email=session.get('user_email')
    )

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            flash('Email already registered!', 'error')
            conn.close()
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)',
            (email, hashed_password, datetime.now())
        )
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form['category']
        session['car_category'] = category
        return redirect(url_for('upload_image'))
    
    return render_template('select_category.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'car_category' not in session:
        flash('Please select a car category first.', 'warning')
        return redirect(url_for('select_category'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Full image path for YOLO
                image_full_path = filepath

                # Get multiple detections
                detections = model.predict_damage(image_full_path)

                # Calculate total cost
                car_category = session['car_category']
                estimated_cost = model.calculate_total_cost(detections, car_category)

                # For database, store first detection (if exists)
                if detections:
                    damage_type = detections[0]["damage_type"]
                    severity = detections[0]["severity"]
                    confidence = detections[0]["confidence"]
                else:
                    damage_type = "no damage"
                    severity = "none"
                    confidence = 0.0
                
                conn = get_db_connection()
                analysis_id = conn.execute(
                    '''INSERT INTO damage_analyses 
                       (user_id, image_path, car_category, damage_type, severity, 
                        confidence, estimated_cost, created_at) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (session['user_id'], filename, car_category, damage_type, 
                     severity, confidence, estimated_cost, datetime.now())
                ).lastrowid
                conn.commit()
                conn.close()
                
                return redirect(url_for('results', analysis_id=analysis_id))
                
            except Exception as e:
                flash(f'Error processing image: {str(e)}', 'error')
                if os.path.exists(filepath):
                    os.remove(filepath)
                return redirect(request.url)
        else:
            flash('Invalid file type! Please upload JPG, JPEG, or PNG files.', 'error')
    
    return render_template('upload_image.html', category=session.get('car_category'))

@app.route('/results/<int:analysis_id>')
def results(analysis_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    analysis = conn.execute(
        'SELECT * FROM damage_analyses WHERE id = ? AND user_id = ?',
        (analysis_id, session['user_id'])
    ).fetchone()
    conn.close()
    
    if not analysis:
        flash('Analysis not found!', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('results.html', analysis=analysis)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    analyses = conn.execute(
        'SELECT * FROM damage_analyses WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    return render_template('history.html', analyses=analyses)

if __name__ == '__main__':
    print("🚗 Starting Car Damage Detection System...")
    print("📍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)