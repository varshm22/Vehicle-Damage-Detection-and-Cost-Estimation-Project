# Car Damage Detection - Setup Instructions

Complete step-by-step guide to set up and run the Car Damage Detection system.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for training)
- **Storage**: 5GB free space (more for datasets)
- **GPU**: Optional but recommended for faster training (NVIDIA with CUDA support)

### Software Dependencies
- Python 3.8+
- pip (Python package manager)
- Git (for version control)
- Web browser (Chrome, Firefox, Safari, Edge)

## Installation Steps

### Step 1: Clone the Repository
```bash
# Clone the project
git clone https://github.com/your-username/car-damage-detection.git
cd car-damage-detection

# Or download and extract ZIP file
# Download from: https://github.com/your-username/car-damage-detection/archive/main.zip
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv car_damage_env

# Activate virtual environment
# On Windows:
car_damage_env\Scripts\activate

# On macOS/Linux:
source car_damage_env/bin/activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import tensorflow; print('TensorFlow version:', tensorflow.__version__)"
python -c "import flask; print('Flask version:', flask.__version__)"
```

### Step 4: Initialize Database
```bash
# Create and initialize SQLite database
python database/init_db.py
```

### Step 5: Create Required Directories
```bash
# Create necessary directories
mkdir -p static/uploads
mkdir -p models/saved_model
mkdir -p datasets/raw
mkdir -p datasets/processed
```

## Configuration

### Step 1: Environment Variables
Create a `.env` file in the project root:
```bash
# .env file
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database/car_damage.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Step 2: Flask Configuration
```bash
# Set Flask app
export FLASK_APP=app.py

# On Windows:
set FLASK_APP=app.py
```

## Dataset Setup

### Option 1: Use Synthetic Data (Quick Start)
```bash
# The system will automatically generate synthetic data for demonstration
# No additional setup required
```

### Option 2: Download Real Datasets (Recommended for Production)
```bash
# Create datasets directory
mkdir -p datasets/raw

# Download CarDD dataset (example - replace with actual URL)
cd datasets/raw
wget https://example-dataset-host.com/cardd_v1.0.zip
unzip cardd_v1.0.zip

# Download additional datasets
# Follow instructions in DATASETS.md
```

### Option 3: Prepare Custom Dataset
```bash
# Organize your images in this structure:
datasets/
├── raw/
│   ├── dent/
│   │   ├── low/
│   │   ├── medium/
│   │   └── high/
│   ├── scratch/
│   │   ├── low/
│   │   ├── medium/
│   │   └── high/
│   └── ... (other damage types)
```

## Model Training

### Step 1: Train the Model
```bash
# Train with synthetic data (quick demo)
python models/train_model.py

# Train with real dataset
python models/train_model.py --dataset datasets/processed --epochs 50
```

### Step 2: Verify Model Training
```bash
# Check if model was created
ls -la models/saved_model/

# Should see:
# - damage_detection_model.h5
# - training_history.json
# - training_history.png
```

## Running the Application

### Step 1: Start the Flask Server
```bash
# Make sure virtual environment is activated
# Activate if not already active:
# source car_damage_env/bin/activate  # macOS/Linux
# car_damage_env\Scripts\activate     # Windows

# Start the application
python app.py
```

### Step 2: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

### Step 3: Test the System
1. **Register**: Create a new user account
2. **Login**: Sign in with your credentials
3. **Select Category**: Choose car category (Economy/Mid-range/Premium)
4. **Upload Image**: Upload a car damage image
5. **View Results**: See damage detection and cost estimation

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'tensorflow'
# Solution: Ensure virtual environment is activated and dependencies installed
source car_damage_env/bin/activate  # Activate environment
pip install -r requirements.txt     # Reinstall dependencies
```

#### Issue 2: Database Errors
```bash
# Error: sqlite3.OperationalError: no such table: users
# Solution: Initialize database
python database/init_db.py
```

#### Issue 3: Model Loading Errors
```bash
# Error: OSError: SavedModel file does not exist
# Solution: Train the model first
python models/train_model.py
```

#### Issue 4: Upload Directory Errors
```bash
# Error: FileNotFoundError: [Errno 2] No such file or directory: 'static/uploads'
# Solution: Create upload directory
mkdir -p static/uploads
```

#### Issue 5: Port Already in Use
```bash
# Error: OSError: [Errno 48] Address already in use
# Solution: Use different port
python app.py --port 5001

# Or kill existing process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :5000   # Windows (find PID and kill)
```

### Performance Issues

#### Slow Model Training
```bash
# Check if GPU is available
python -c "import tensorflow as tf; print('GPU Available:', tf.config.list_physical_devices('GPU'))"

# Install GPU support (if NVIDIA GPU available)
pip install tensorflow-gpu
```

#### Large File Upload Issues
```bash
# Increase max file size in app.py
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

## Development Setup

### Step 1: Install Development Dependencies
```bash
# Install additional development tools
pip install pytest flask-testing black flake8 mypy

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Step 2: Run Tests
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.
```

### Step 3: Code Formatting
```bash
# Format code with Black
black .

# Check code style with flake8
flake8 .

# Type checking with mypy
mypy .
```

## Production Deployment

### Step 1: Production Configuration
```bash
# Update .env for production
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-production-key
```

### Step 2: Use Production WSGI Server
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Step 3: Database Migration (if using PostgreSQL)
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update database URL
DATABASE_URL=postgresql://user:password@localhost/car_damage_db
```

## Docker Setup (Optional)

### Step 1: Build Docker Image
```bash
# Create Dockerfile (provided in project)
docker build -t car-damage-detection .
```

### Step 2: Run Docker Container
```bash
# Run container
docker run -p 5000:5000 car-damage-detection
```

## Monitoring and Logging

### Step 1: Enable Logging
```python
# Add to app.py
import logging
logging.basicConfig(level=logging.INFO)
```

### Step 2: Monitor Performance
```bash
# Install monitoring tools
pip install flask-monitoring-dashboard

# Access dashboard at /dashboard
```

## Security Considerations

### Step 1: Secure File Uploads
- Validate file types and sizes
- Scan uploaded files for malware
- Store uploads outside web root

### Step 2: Database Security
- Use strong passwords
- Enable SSL connections
- Regular backups

### Step 3: Application Security
- Keep dependencies updated
- Use HTTPS in production
- Implement rate limiting

## Support and Resources

### Documentation
- **API Documentation**: `/docs` endpoint
- **Dataset Guide**: `DATASETS.md`
- **Architecture**: `ARCHITECTURE.md`

### Community
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Community support and questions
- **Wiki**: Additional documentation and tutorials

### Contact
- **Email**: support@car-damage-detection.com
- **Discord**: Join our development community
- **Twitter**: @CarDamageAI for updates

## Next Steps

After successful setup:
1. **Explore the Interface**: Familiarize yourself with all features
2. **Test with Real Images**: Upload various damage types
3. **Review Results**: Understand the AI predictions
4. **Customize**: Modify for your specific use case
5. **Contribute**: Help improve the project

## Changelog

### Version 1.0.0
- Initial release
- Basic damage detection
- Cost estimation
- Web interface

### Version 1.1.0 (Planned)
- Multiple damage detection
- Improved accuracy
- Mobile app support
- API endpoints