"""
Utility functions for AI fitness coach.
Includes image processing, validation, and helper functions.
"""

import base64
import os
from PIL import Image
from typing import Optional

def encode_image(image_path: str) -> str:
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

def validate_image(image_path: str) -> bool:
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

def get_image_info(image_path: str) -> dict:
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

def prepare_image_for_analysis(image_path: str) -> dict:
    """
    Prepare an Apple Watch screenshot for AI analysis.
    
    Args:
        image_path (str): Path to the Apple Watch screenshot
        
    Returns:
        dict: Prepared data including base64 encoding and metadata
        
    Raises:
        ValueError: If image is invalid or unreadable
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

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_user_input(query: str) -> tuple[bool, str]:
    """
    Validate user input for running goals.
    
    Args:
        query (str): User's running goal input
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not query or not query.strip():
        return False, "Please enter a running goal"
    
    if len(query.strip()) < 5:
        return False, "Please provide a more detailed running goal"
    
    if len(query) > 500:
        return False, "Please keep your goal under 500 characters"
    
    return True, ""

def extract_weeks_from_query(query: str) -> Optional[int]:
    """
    Try to extract number of weeks from user query.
    
    Args:
        query (str): User's running goal
        
    Returns:
        Optional[int]: Number of weeks if found, None otherwise
    """
    import re
    
    # Look for patterns like "8 weeks", "in 12 weeks", etc.
    week_patterns = [
        r'(\d+)\s*weeks?',
        r'in\s*(\d+)\s*weeks?',
        r'(\d+)-week',
    ]
    
    for pattern in week_patterns:
        match = re.search(pattern, query.lower())
        if match:
            try:
                weeks = int(match.group(1))
                if 1 <= weeks <= 52:  # Reasonable range
                    return weeks
            except ValueError:
                continue
    
    return None

def print_system_info():
    """Print system information for debugging."""
    print("🔧 System Information:")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   Python path: {os.sys.executable}")
    
    # Check for required packages
    required_packages = ['openai', 'pydantic', 'pillow']
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: installed")
        except ImportError:
            print(f"   ❌ {package}: not installed")

def create_example_image_path() -> str:
    """
    Create path for example image with helpful error message.
    
    Returns:
        str: Path to example image
    """
    example_path = "IMG_4830.png"
    
    if not os.path.exists(example_path):
        print(f"📸 Image Setup Instructions:")
        print(f"   1. Take a screenshot of your Apple Watch fitness data")
        print(f"   2. Save it as '{example_path}' in the current directory")
        print(f"   3. Or update the image_path variable in main.py")
        print(f"   Current directory: {os.getcwd()}")
    
    return example_path