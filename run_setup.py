#!/usr/bin/env python3
"""
Car Damage Detection - Complete Setup Script
Automates the entire setup process for the car damage detection system
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_step(step_num, description):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*60}")

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error {description}: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/uploads',
        'models/saved_model',
        'datasets/raw',
        'datasets/processed',
        'database'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "installing dependencies"):
        return False
    
    print("✅ Dependencies installed successfully")
    return True

def initialize_database():
    """Initialize the SQLite database"""
    print("Initializing database...")
    
    try:
        # Run the database initialization script
        if not run_command(f"{sys.executable} database/init_db.py", "initializing database"):
            return False
        
        # Verify database was created
        if os.path.exists('database/car_damage.db'):
            print("✅ Database initialized successfully")
            return True
        else:
            print("❌ Database file not found after initialization")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def train_model():
    """Train the machine learning model"""
    print("Training machine learning model...")
    print("⚠️  This may take several minutes...")
    
    if not run_command(f"{sys.executable} models/train_model.py", "training model"):
        print("❌ Model training failed")
        return False
    
    # Check if model file was created
    if os.path.exists('models/saved_model/damage_detection_model.h5'):
        print("✅ Model trained and saved successfully")
        return True
    else:
        print("❌ Model file not found after training")
        return False

def verify_installation():
    """Verify that all components are properly installed"""
    print("Verifying installation...")
    
    # Check critical files
    critical_files = [
        'database/car_damage.db',
        'models/saved_model/damage_detection_model.h5',
        'static/uploads',
        'app.py'
    ]
    
    all_good = True
    for file_path in critical_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    # Test imports
    try:
        import flask
        import tensorflow
        import cv2
        import PIL
        print("✅ All required packages can be imported")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        all_good = False
    
    return all_good

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# Car Damage Detection - Environment Configuration
SECRET_KEY=your-secret-key-change-in-production-please
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database/car_damage.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚗 Car Damage Detection System - Automated Setup")
    print("This script will set up the complete system for you.")
    print("Please ensure you have Python 3.8+ installed.")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create directories
    print_step(2, "Creating Required Directories")
    create_directories()
    
    # Step 3: Create environment file
    print_step(3, "Creating Environment Configuration")
    create_env_file()
    
    # Step 4: Install dependencies
    print_step(4, "Installing Dependencies")
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Step 5: Initialize database
    print_step(5, "Initializing Database")
    if not initialize_database():
        print("❌ Setup failed at database initialization")
        sys.exit(1)
    
    # Step 6: Train model
    print_step(6, "Training Machine Learning Model")
    if not train_model():
        print("❌ Setup failed at model training")
        sys.exit(1)
    
    # Step 7: Verify installation
    print_step(7, "Verifying Installation")
    if not verify_installation():
        print("❌ Setup verification failed")
        sys.exit(1)
    
    # Success message
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run the application:")
    print(f"   {sys.executable} app.py")
    print("\n2. Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n3. Register a new account and start analyzing car damage!")
    print("\nFor more information, see:")
    print("- README.md - Project overview")
    print("- SETUP.md - Detailed setup instructions")
    print("- DATASETS.md - Dataset information")
    print("- ARCHITECTURE.md - System architecture")
    print("\n🚗 Happy damage detecting! 🔍")

if __name__ == "__main__":
    main()