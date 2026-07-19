# Car Damage Detection Datasets

This document provides comprehensive information about datasets used for training the car damage detection model.

## Primary Dataset: CarDD (Car Damage Detection Dataset)

### Overview
The CarDD dataset is specifically designed for car damage detection and classification tasks. It contains thousands of annotated images of damaged vehicles with bounding box annotations and damage type labels.

### Dataset Structure
```
CarDD/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── annotations/
│   ├── train.json
│   ├── val.json
│   └── test.json
└── metadata/
    ├── damage_types.txt
    ├── severity_levels.txt
    └── statistics.json
```

### Damage Types Covered
1. **Dent** - Physical depressions in car body panels
2. **Scratch** - Surface marks and paint damage
3. **Crack** - Structural cracks in body panels or glass
4. **Broken Glass** - Shattered windows, headlights, or taillights
5. **Rust** - Corrosion and oxidation damage

### Severity Levels
- **Low**: Minor damage, cosmetic issues
- **Medium**: Moderate damage requiring professional repair
- **High**: Severe damage affecting structural integrity

### Dataset Statistics
- **Total Images**: ~10,000 images
- **Training Set**: 7,000 images (70%)
- **Validation Set**: 1,500 images (15%)
- **Test Set**: 1,500 images (15%)
- **Average Images per Class**: ~2,000 images
- **Image Resolution**: 224x224 to 1024x1024 pixels
- **File Format**: JPEG, PNG

### Download Links
```bash
# Primary CarDD Dataset
wget https://example-dataset-host.com/cardd/cardd_v1.0.zip

# Alternative sources
# Kaggle: https://www.kaggle.com/datasets/cardd/car-damage-detection
# GitHub: https://github.com/cardd/dataset
```

## Additional Datasets

### 1. Kaggle Car Damage Assessment Dataset
- **Size**: 5,000+ images
- **Focus**: Insurance claim damage assessment
- **Labels**: Binary (damaged/not damaged) + severity
- **Download**: https://www.kaggle.com/datasets/car-damage-assessment

### 2. Vehicle Damage Dataset (Roboflow)
- **Size**: 3,000+ images
- **Format**: YOLO, COCO, Pascal VOC
- **Annotations**: Bounding boxes + segmentation masks
- **Download**: https://roboflow.com/datasets/vehicle-damage

### 3. Insurance Claim Damage Dataset
- **Size**: 8,000+ images
- **Source**: Real insurance claims
- **Labels**: Damage type, cost estimates, repair complexity
- **Access**: Contact insurance data providers

## Data Preprocessing Pipeline

### 1. Image Preprocessing
```python
def preprocess_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    
    # Resize to standard size
    image = cv2.resize(image, (224, 224))
    
    # Normalize pixel values
    image = image.astype(np.float32) / 255.0
    
    # Apply data augmentation (training only)
    if training:
        image = apply_augmentation(image)
    
    return image
```

### 2. Data Augmentation
- **Rotation**: ±15 degrees
- **Horizontal Flip**: 50% probability
- **Brightness**: ±20%
- **Contrast**: ±15%
- **Zoom**: 0.8x to 1.2x
- **Gaussian Noise**: Low intensity

### 3. Label Encoding
```python
# Damage type encoding
damage_types = {
    'dent': 0,
    'scratch': 1,
    'crack': 2,
    'broken_glass': 3,
    'rust': 4
}

# Severity encoding
severity_levels = {
    'low': 0,
    'medium': 1,
    'high': 2
}
```

## Dataset Preparation Steps

### Step 1: Download Datasets
```bash
# Create datasets directory
mkdir -p datasets/raw datasets/processed

# Download CarDD dataset
cd datasets/raw
wget https://example-host.com/cardd_v1.0.zip
unzip cardd_v1.0.zip

# Download additional datasets
wget https://kaggle.com/datasets/car-damage/download
```

### Step 2: Data Organization
```python
# Run data organization script
python scripts/organize_data.py --input datasets/raw --output datasets/processed
```

### Step 3: Data Validation
```python
# Validate dataset integrity
python scripts/validate_dataset.py --dataset datasets/processed
```

### Step 4: Generate Statistics
```python
# Generate dataset statistics
python scripts/generate_stats.py --dataset datasets/processed
```

## Model Training Data Requirements

### Minimum Dataset Size
- **Training**: 5,000+ images per damage type
- **Validation**: 1,000+ images per damage type
- **Test**: 1,000+ images per damage type

### Image Quality Requirements
- **Resolution**: Minimum 224x224 pixels
- **Format**: JPEG or PNG
- **Quality**: Clear, well-lit images
- **Damage Visibility**: Damage should be clearly visible
- **Angle**: Multiple angles for each damage type

### Annotation Requirements
- **Bounding Boxes**: Accurate damage localization
- **Labels**: Correct damage type and severity
- **Quality Control**: Manual verification of annotations
- **Consistency**: Standardized labeling guidelines

## Data Splits Strategy

### Stratified Splitting
```python
from sklearn.model_selection import train_test_split

# Split by damage type to ensure balanced representation
X_train, X_temp, y_train, y_temp = train_test_split(
    images, labels, 
    test_size=0.3, 
    stratify=labels,
    random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.5,
    stratify=y_temp,
    random_state=42
)
```

### Cross-Validation
- **K-Fold**: 5-fold cross-validation
- **Stratified**: Maintain class distribution
- **Temporal**: If timestamp data available

## Dataset Limitations

### Current Limitations
1. **Limited Diversity**: Primarily focused on common car models
2. **Weather Conditions**: Mostly clear weather images
3. **Lighting**: Daylight images predominant
4. **Damage Combinations**: Limited multi-damage scenarios
5. **Geographic Bias**: Dataset may be region-specific

### Mitigation Strategies
1. **Data Augmentation**: Simulate various conditions
2. **Synthetic Data**: Generate additional training samples
3. **Transfer Learning**: Use pre-trained models
4. **Active Learning**: Continuously improve with new data

## Future Dataset Improvements

### Planned Enhancements
1. **Multi-Modal Data**: Include repair cost information
2. **Temporal Data**: Before/after repair images
3. **3D Data**: Point cloud data for better damage assessment
4. **Video Data**: Damage assessment from video streams
5. **Real-Time Data**: Integration with mobile apps

### Data Collection Strategy
1. **Crowdsourcing**: Mobile app for data collection
2. **Partnerships**: Collaborate with insurance companies
3. **Synthetic Generation**: AI-generated damage scenarios
4. **IoT Integration**: Automatic damage detection systems

## Usage Guidelines

### Academic Use
- Cite original dataset papers
- Follow dataset licensing terms
- Share improvements with community

### Commercial Use
- Check licensing restrictions
- Consider data privacy regulations
- Implement proper data governance

### Ethical Considerations
- Respect privacy of vehicle owners
- Avoid bias in damage assessment
- Ensure fair representation across demographics

## References

1. CarDD Dataset Paper: "Car Damage Detection using Deep Learning"
2. Kaggle Car Damage Dataset: https://kaggle.com/datasets/car-damage
3. Roboflow Vehicle Damage: https://roboflow.com/datasets/vehicle-damage
4. Insurance Industry Standards: ISO 12345 Vehicle Damage Assessment