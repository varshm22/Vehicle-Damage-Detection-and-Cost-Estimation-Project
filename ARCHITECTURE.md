# Car Damage Detection - System Architecture

## Overview

The Car Damage Detection system is a full-stack web application that uses computer vision and machine learning to detect car damage and estimate repair costs. The system follows a modular architecture with clear separation of concerns.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  HTML Templates  │  CSS Styles  │  JavaScript  │  Bootstrap UI  │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Web Framework Layer                        │
├─────────────────────────────────────────────────────────────────┤
│                         Flask Application                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   Routes    │ │ Middleware  │ │   Session   │ │    Auth     ││
│  │ Management  │ │   Layer     │ │ Management  │ │ Management  ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   Image     │ │   Damage    │ │    Cost     │ │    User     ││
│  │ Processing  │ │ Detection   │ │ Estimation  │ │ Management  ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ML/AI Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │     CNN     │ │   Model     │ │ Prediction  │ │   Training  ││
│  │   Model     │ │   Loading   │ │   Engine    │ │   Pipeline  ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│  │   SQLite    │ │    File     │ │   Model     │ │   Upload    ││
│  │  Database   │ │   System    │ │   Storage   │ │   Storage   ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Frontend Layer

#### Technologies Used
- **HTML5**: Semantic markup and structure
- **CSS3**: Styling with custom CSS and Bootstrap
- **JavaScript**: Client-side interactivity and validation
- **Bootstrap 5**: Responsive UI framework

#### Key Components
```
templates/
├── base.html           # Base template with navigation
├── index.html          # Landing page
├── login.html          # User authentication
├── register.html       # User registration
├── dashboard.html      # Main dashboard
├── select_category.html # Car category selection
├── upload_image.html   # Image upload interface
├── results.html        # Analysis results display
└── history.html        # Analysis history
```

#### Features
- Responsive design for mobile and desktop
- Progressive image upload with drag-and-drop
- Real-time form validation
- Loading states and progress indicators
- Toast notifications for user feedback

### 2. Web Framework Layer

#### Flask Application Structure
```python
app.py                  # Main Flask application
├── Route Handlers      # URL routing and request handling
├── Session Management  # User session handling
├── Authentication      # Login/logout functionality
├── File Upload         # Image upload processing
├── Error Handling      # Global error management
└── Template Rendering  # Jinja2 template processing
```

#### Key Routes
- `/` - Landing page
- `/login` - User authentication
- `/register` - User registration
- `/dashboard` - Main dashboard
- `/select_category` - Car category selection
- `/upload_image` - Image upload and processing
- `/results/<id>` - Analysis results
- `/history` - Analysis history

### 3. Business Logic Layer

#### Core Modules

##### Authentication Module (`utils/auth.py`)
```python
class AuthManager:
    - login_required()      # Decorator for protected routes
    - init_auth()          # Initialize authentication
    - is_authenticated()   # Check authentication status
    - get_current_user()   # Get current user info
```

##### Image Processing Module (`utils/image_processor.py`)
```python
class ImageProcessor:
    - allowed_file()           # Validate file types
    - preprocess_image()       # Prepare image for ML model
    - validate_image_content() # Verify image integrity
    - create_thumbnail()       # Generate thumbnails
```

##### Cost Estimation Module (`utils/cost_estimator.py`)
```python
class CostEstimator:
    - estimate_repair_cost()   # Calculate repair costs
    - get_base_cost()         # Retrieve base costs from DB
    - get_cost_breakdown()    # Detailed cost analysis
    - get_cost_range()        # Cost range by severity
```

### 4. ML/AI Layer

#### Model Architecture (`models/damage_model.py`)
```python
class DamageDetectionModel:
    - build_model()        # Construct CNN architecture
    - load_model()         # Load pre-trained model
    - save_model()         # Save trained model
    - predict_damage()     # Make damage predictions
    - predict_batch()      # Batch predictions
```

#### CNN Architecture
```
Input Layer (224, 224, 3)
    ↓
Data Augmentation Layer
    ↓
Conv2D (32 filters, 3x3) + ReLU + MaxPool2D
    ↓
Conv2D (64 filters, 3x3) + ReLU + MaxPool2D
    ↓
Conv2D (128 filters, 3x3) + ReLU + MaxPool2D
    ↓
Conv2D (256 filters, 3x3) + ReLU + MaxPool2D
    ↓
GlobalAveragePooling2D
    ↓
Dense (512) + ReLU + Dropout(0.5)
    ↓
Dense (256) + ReLU + Dropout(0.3)
    ↓
┌─────────────────┐    ┌─────────────────┐
│ Damage Type     │    │ Severity Level  │
│ Output (5)      │    │ Output (3)      │
│ Softmax         │    │ Softmax         │
└─────────────────┘    └─────────────────┘
```

#### Training Pipeline (`models/train_model.py`)
```python
class DamageModelTrainer:
    - prepare_synthetic_data() # Generate demo data
    - load_real_dataset()      # Load actual datasets
    - train_model()            # Model training process
    - evaluate_model()         # Performance evaluation
    - plot_training_history()  # Visualization
```

### 5. Data Layer

#### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Damage analyses table
CREATE TABLE damage_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    car_category TEXT NOT NULL,
    damage_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    confidence REAL NOT NULL,
    estimated_cost REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Cost matrix table
CREATE TABLE cost_matrix (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    damage_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    base_cost REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### File Storage Structure
```
static/
├── uploads/           # User uploaded images
│   ├── uuid1.jpg
│   ├── uuid2.png
│   └── ...
├── css/
│   └── style.css     # Custom styles
└── js/
    └── main.js       # Client-side JavaScript

models/
├── saved_model/      # Trained ML models
│   ├── damage_detection_model.h5
│   ├── training_history.json
│   └── best_model.h5
└── ...
```

## Data Flow

### 1. User Registration/Login Flow
```
User Input → Form Validation → Password Hashing → Database Storage → Session Creation
```

### 2. Damage Analysis Flow
```
Image Upload → File Validation → Image Preprocessing → ML Model Prediction → 
Cost Calculation → Database Storage → Results Display
```

### 3. Detailed Analysis Flow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   Flask     │    │  Database   │
│ Interface   │    │ Application │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        │ 1. Upload Image   │                   │
        ├──────────────────►│                   │
        │                   │ 2. Validate File │
        │                   ├─────────────────► │
        │                   │                   │
        │                   │ 3. Save Image    │
        │                   ├─────────────────► │
        │                   │                   │
        │                   │ 4. Preprocess    │
        │                   │    Image         │
        │                   │                   │
        │                   │ 5. ML Prediction │
        │                   │                   │
        │                   │ 6. Cost Calc     │
        │                   │                   │
        │                   │ 7. Save Results  │
        │                   ├─────────────────► │
        │                   │                   │
        │ 8. Display Results│                   │
        │◄──────────────────┤                   │
```

## Security Architecture

### 1. Authentication & Authorization
- **Password Hashing**: bcrypt with salt
- **Session Management**: Flask-Login with secure cookies
- **CSRF Protection**: Built-in Flask CSRF tokens
- **Input Validation**: Server-side validation for all inputs

### 2. File Upload Security
- **File Type Validation**: Whitelist of allowed extensions
- **File Size Limits**: Maximum 16MB per upload
- **Content Validation**: Image header verification
- **Secure Storage**: Files stored outside web root

### 3. Database Security
- **SQL Injection Prevention**: Parameterized queries
- **Data Encryption**: Sensitive data encryption at rest
- **Access Control**: Role-based access control
- **Audit Logging**: Track all database operations

## Performance Architecture

### 1. Caching Strategy
- **Model Caching**: Load ML model once, reuse for predictions
- **Static File Caching**: Browser caching for CSS/JS
- **Database Query Optimization**: Indexed queries
- **Image Caching**: Thumbnail generation and caching

### 2. Scalability Considerations
- **Horizontal Scaling**: Stateless application design
- **Load Balancing**: Multiple Flask instances
- **Database Scaling**: Read replicas for analytics
- **CDN Integration**: Static file distribution

### 3. Monitoring & Logging
- **Application Logging**: Structured logging with levels
- **Performance Monitoring**: Response time tracking
- **Error Tracking**: Exception monitoring and alerting
- **Usage Analytics**: User behavior tracking

## Deployment Architecture

### 1. Development Environment
```
Local Machine
├── Python Virtual Environment
├── SQLite Database
├── Local File Storage
└── Flask Development Server
```

### 2. Production Environment
```
Production Server
├── Gunicorn WSGI Server
├── Nginx Reverse Proxy
├── PostgreSQL Database
├── Redis Cache
└── File Storage (AWS S3/Local)
```

### 3. Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## API Architecture (Future Enhancement)

### RESTful API Design
```
POST /api/v1/auth/login          # User authentication
POST /api/v1/auth/register       # User registration
POST /api/v1/damage/analyze      # Damage analysis
GET  /api/v1/damage/history      # Analysis history
GET  /api/v1/damage/results/{id} # Specific analysis
POST /api/v1/models/train        # Model training
GET  /api/v1/models/status       # Training status
```

### API Response Format
```json
{
    "status": "success|error",
    "data": {
        "damage_type": "dent",
        "severity": "medium",
        "confidence": 0.87,
        "estimated_cost": 450.00
    },
    "message": "Analysis completed successfully",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## Technology Stack Summary

### Backend
- **Framework**: Flask 2.3.3
- **ML/AI**: TensorFlow 2.13.0, OpenCV 4.8.1
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Authentication**: Flask-Login, bcrypt
- **File Processing**: Pillow, Werkzeug

### Frontend
- **UI Framework**: Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0.0
- **JavaScript**: Vanilla JS with modern ES6+
- **Styling**: Custom CSS with CSS Grid/Flexbox

### DevOps & Deployment
- **WSGI Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Containerization**: Docker
- **Version Control**: Git
- **Testing**: pytest, Flask-Testing

## Future Architecture Enhancements

### 1. Microservices Architecture
- **API Gateway**: Centralized request routing
- **Auth Service**: Dedicated authentication service
- **ML Service**: Separate machine learning service
- **File Service**: Dedicated file storage service

### 2. Cloud-Native Architecture
- **Container Orchestration**: Kubernetes
- **Service Mesh**: Istio for service communication
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

### 3. Advanced ML Pipeline
- **MLOps**: Model versioning and deployment automation
- **A/B Testing**: Model performance comparison
- **Real-time Training**: Continuous model improvement
- **Edge Computing**: Mobile device inference