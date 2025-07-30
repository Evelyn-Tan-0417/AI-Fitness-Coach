"""
Main execution script for AI fitness coach.
Handles user input, image processing, API calls, and output generation.
"""

import os
import sys
from models import RunningPlan, SYSTEM_PROMPT
from database import save_plan_to_db, create_database_schema
from output_generators import generate_html_training_plan, print_plan_summary, create_css_file
from utils import encode_image, validate_image, validate_user_input, create_example_image_path

# Try to import config, fall back to basic setup if not available
try:
    from config import setup_openai_client, get_image_path
    client = setup_openai_client()
    IMAGE_PATH = get_image_path()
except ImportError:
    print("⚠️  config.py not found. Using basic configuration.")
    print("   For better setup, copy config_example.py to config.py")
    
    # Basic fallback configuration
    from openai import OpenAI
    
    # Check for API key in environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("   Please set OPENAI_API_KEY environment variable or create config.py")
        sys.exit(1)
    
    client = OpenAI()
    IMAGE_PATH = "IMG_4830.png"

def create_structured_request(user_query: str, base64_image: str) -> dict:
    """
    Create a structured request for the OpenAI API.
    
    Args:
        user_query (str): User's running goal
        base64_image (str): Base64 encoded image data
        
    Returns:
        dict: Formatted request parameters
    """
    return {
        "model": "gpt-4o",
        "input": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_query},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
        "text_format": RunningPlan
    }

def main():
    """Main execution function."""
    print("🏃‍♂️ AI Fitness Coach - Personalized Training Plans")
    print("=" * 50)
    
    # Get user input with validation
    while True:
        query = input("\\nWhat is your running goal? (e.g., 'run a 10k in 8 weeks'): ").strip()
        is_valid, error_message = validate_user_input(query)
        if is_valid:
            break
        print(f"❌ {error_message}")
    
    # Image processing
    image_path = create_example_image_path()
    base64_image = ""
    
    try:
        if validate_image(image_path):
            base64_image = encode_image(image_path)
            print(f"✅ Image loaded successfully: {image_path}")
        else:
            print(f"⚠️  Image file not found at {image_path}.")
            print("   Proceeding without image (results may be less personalized)")
    except Exception as e:
        print(f"⚠️  Error loading image: {str(e)}")
        print("   Proceeding without image (results may be less personalized)")
    
    # Generate training plan
    print("\\n🤖 Generating your personalized running plan...")
    print("   This may take 10-30 seconds...")
    
    try:
        # Create API request
        request_params = create_structured_request(query, base64_image)
        
        # Make API call using new responses.parse method
        response = client.responses.parse(**request_params)
        
        # Extract parsed plan
        plan = response.output_parsed
        
        # Display results
        print_plan_summary(plan)
        
        # Generate outputs
        print("\\n📄 Generating output files...")
        
        # Create CSS file
        create_css_file()
        
        # Generate HTML output
        html_content = generate_html_training_plan(plan)
        with open("training_plan.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ HTML file generated: training_plan.html")
        
        # Save to database
        try:
            create_database_schema()  # Ensure database schema exists
            plan_id = save_plan_to_db(plan)
            if plan_id:
                print(f"✅ Plan saved to database with ID: {plan_id}")
            else:
                print("⚠️  Database save failed")
        except Exception as db_error:
            print(f"⚠️  Database save failed: {str(db_error)}")
        
        print("\\n🎉 Training plan generation complete!")
        print("\\nFiles created:")
        print("  📄 training_plan.html - Open in browser to view your plan")
        print("  🎨 style.css - Styling for the HTML file")
        print("  🗄️  Database record - Plan saved for future reference")
        print("\\n💡 Next steps:")
        print("  • Open training_plan.html in your web browser")
        print("  • Save your Apple Watch image for future use")
        print("  • Run the program again to create new plans")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("\\nTroubleshooting:")
        print("• Check your internet connection")
        print("• Verify your OpenAI API key is correct")
        print("• Ensure you have sufficient API credits")
        print("• Try running again in a few minutes")

def print_help():
    """Print help information."""
    print("🆘 AI Fitness Coach Help")
    print("=" * 30)
    print("Usage: python main.py")
    print()
    print("Setup Requirements:")
    print("1. OpenAI API key (set in environment or config.py)")
    print("2. Apple Watch screenshot (optional but recommended)")
    print("3. Internet connection")
    print()
    print("Example goals:")
    print("• 'run a 5K in 6 weeks'")
    print("• 'train for a half marathon in 12 weeks'") 
    print("• 'improve my 10K time in 8 weeks'")
    print("• 'prepare for my first marathon in 16 weeks'")

if __name__ == "__main__":
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
    else:
        main()