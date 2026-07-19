"""
Image Processing Utilities
Handles image upload, validation, and preprocessing for ML model
"""

import os
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Check if uploaded file has allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image_for_model(image_path, target_size=(224, 224)):
    """
    Preprocess uploaded image for ML model prediction
    
    Args:
        image_path (str): Path to the uploaded image
        target_size (tuple): Target size for model input (width, height)
    
    Returns:
        numpy.ndarray: Preprocessed image array ready for model
    """
    try:
        # Load image using PIL
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to target size
        image = image.resize(target_size)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values to [0, 1]
        image_array = image_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
        
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def process_uploaded_image(image_path):
    """
    Process uploaded image and prepare for damage detection
    
    Args:
        image_path (str): Path to uploaded image
    
    Returns:
        dict: Processing results including image info and preprocessed data
    """
    try:
        # Get image information
        image = Image.open(image_path)
        image_info = {
            'width': image.width,
            'height': image.height,
            'format': image.format,
            'mode': image.mode,
            'size_bytes': os.path.getsize(image_path)
        }
        
        # Preprocess for model
        preprocessed_image = preprocess_image_for_model(image_path)
        
        return {
            'success': True,
            'image_info': image_info,
            'preprocessed_image': preprocessed_image,
            'message': 'Image processed successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to process image'
        }

def validate_image_content(image_path):
    """
    Validate that uploaded file is actually a valid image
    
    Args:
        image_path (str): Path to uploaded file
    
    Returns:
        bool: True if valid image, False otherwise
    """
    try:
        # Try to open and verify image
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def get_image_dimensions(image_path):
    """
    Get image dimensions without loading full image into memory
    
    Args:
        image_path (str): Path to image file
    
    Returns:
        tuple: (width, height) or None if error
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return None

def create_thumbnail(image_path, output_path, size=(300, 300)):
    """
    Create thumbnail version of uploaded image for display
    
    Args:
        image_path (str): Path to original image
        output_path (str): Path to save thumbnail
        size (tuple): Thumbnail size (width, height)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(output_path, optimize=True, quality=85)
        return True
    except Exception:
        return False