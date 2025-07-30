"""
Image processing utilities for Apple Watch fitness data extraction.
Handles screenshot processing and data extraction from fitness interfaces.
"""

import base64
import os
from PIL import Image
import io

def encode_image(image_path):
    """
    Encode an image file to base64 string for API transmission.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded string of the image
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        Exception: If image encoding fails
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise Exception(f"Failed to encode image: {str(e)}")

def validate_image(image_path):
    """
    Validate that the image file exists and is readable.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if image is valid, False otherwise
    """
    try:
        if not os.path.exists(image_path):
            return False
            
        # Try to open with PIL to verify it's a valid image
        with Image.open(image_path) as img:
            img.verify()
        return True
        
    except Exception:
        return False

def get_image_info(image_path):
    """
    Get basic information about an image file.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        dict: Image information including size, format, mode
    """
    try:
        with Image.open(image_path) as img:
            return {
                "size": img.size,
                "format": img.format,
                "mode": img.mode,
                "file_size": os.path.getsize(image_path)
            }
    except Exception as e:
        return {"error": str(e)}

def prepare_image_for_analysis(image_path):
    """
    Prepare an Apple Watch screenshot for AI analysis.
    
    Args:
        image_path (str): Path to the Apple Watch screenshot
        
    Returns:
        dict: Prepared data including base64 encoding and metadata
    """
    if not validate_image(image_path):
        raise ValueError(f"Invalid or unreadable image: {image_path}")
    
    # Get image information
    img_info = get_image_info(image_path)
    
    # Encode to base64
    base64_image = encode_image(image_path)
    
    return {
        "base64_image": base64_image,
        "image_info": img_info,
        "data_url": f"data:image/jpeg;base64,{base64_image}"
    }

def create_multimodal_request(text_query, image_path):
    """
    Create a multimodal request combining text and image for OpenAI API.
    
    Args:
        text_query (str): Text prompt for the AI
        image_path (str): Path to the Apple Watch screenshot
        
    Returns:
        list: Formatted message array for OpenAI API
    """
    prepared_image = prepare_image_for_analysis(image_path)
    
    message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": text_query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": prepared_image["data_url"]
                }
            }
        ]
    }
    
    return [message]

# Example usage functions
def analyze_apple_watch_screenshot(image_path, fitness_goal):
    """
    Convenience function to analyze an Apple Watch screenshot with a fitness goal.
    
    Args:
        image_path (str): Path to Apple Watch screenshot
        fitness_goal (str): User's fitness goal description
        
    Returns:
        list: Formatted request ready for OpenAI API
    """
    query = f"""
    Analyze this Apple Watch fitness data and create a personalized training plan for: {fitness_goal}
    
    Please extract relevant metrics from the image (VO2 max, workout history, activity levels) 
    and provide specific, actionable recommendations based on this data.
    """
    
    return create_multimodal_request(query, image_path)