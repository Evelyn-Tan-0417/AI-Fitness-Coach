"""
Configuration example for AI fitness coach.
Copy this file to config.py and add your actual API key.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Model Configuration
DEFAULT_MODEL = "gpt-4o"

# Database Configuration
DATABASE_PATH = "instance/flaskr.sqlite"

# Image Configuration
DEFAULT_IMAGE_PATH = "IMG_4830.png"

# Output Configuration
HTML_OUTPUT_FILE = "training_plan.html"
JSON_OUTPUT_FILE = "training_plan.json"
CSS_OUTPUT_FILE = "style.css"

# Validation Settings
MAX_QUERY_LENGTH = 500
MIN_QUERY_LENGTH = 5
MAX_WEEKS = 52
MIN_WEEKS = 1

def setup_openai_client():
    """
    Set up OpenAI client with API key.
    
    Returns:
        OpenAI: Configured OpenAI client
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
        raise ValueError(
            "OpenAI API key not found. Please:\n"
            "1. Copy config_example.py to config.py\n"
            "2. Add your OpenAI API key to config.py\n"
            "3. Or set OPENAI_API_KEY environment variable"
        )
    
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    from openai import OpenAI
    return OpenAI()

def get_image_path():
    """
    Get the path to the Apple Watch image file.
    
    Returns:
        str: Path to image file
    """
    return DEFAULT_IMAGE_PATH

def print_setup_instructions():
    """Print setup instructions for new users."""
    print("🚀 AI Fitness Coach Setup")
    print("=" * 40)
    print("1. Copy config_example.py to config.py")
    print("2. Add your OpenAI API key to config.py")
    print("3. Add your Apple Watch screenshot as IMG_4830.png")
    print("4. Run: python main.py")
    print()
    print("Need help? Check the README.md file!")

if __name__ == "__main__":
    print_setup_instructions()