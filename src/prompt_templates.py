"""
Pydantic models and prompt templates for AI fitness coach.
Contains structured data models and prompts for generating training plans with nutrition.
"""

from pydantic import BaseModel, Field
from typing import List

# Pydantic models for structured output
class DailyMeal(BaseModel):
    suggestion: str
    calories: str

class DailyPlan(BaseModel):
    day: str
    titles: str
    details: str
    breakfast: DailyMeal
    lunch: DailyMeal
    dinner: DailyMeal

WeeklyPlan = List[DailyPlan]

class RunningPlan(BaseModel):
    motivation: str
    feedback: str
    supplement_suggestion: str
    plan: List[WeeklyPlan]

# System prompt for the AI fitness coach
SYSTEM_PROMPT = """You are an expert running coach. First, determine the total number of training weeks required from the user's query. Then, generate a running plan with a 'motivation' message, 'feedback' message from the stats provided on the uploaded image, 'supplement suggestion' for suggestion the supplements that the person should take for their best performance, and a 'plan' list, where each item in the list represents one week's schedule. Again, make sure to match the number of weeks exactly, no more and no fewer weeks. Also, please include a daily breakfast, lunch, and dinner suggestion that has the name of the meal and the calories"""

def create_structured_request(user_query: str, base64_image: str):
    """
    Create a structured request for the OpenAI API using the new responses.parse method.
    
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

def validate_plan_structure(plan: RunningPlan) -> bool:
    """
    Validate that the generated plan has the expected structure.
    
    Args:
        plan (RunningPlan): The generated running plan
        
    Returns:
        bool: True if structure is valid
    """
    try:
        # Check required fields
        required_fields = ['motivation', 'feedback', 'supplement_suggestion', 'plan']
        for field in required_fields:
            if not hasattr(plan, field):
                return False
        
        # Check that plan is a list and has content
        if not isinstance(plan.plan, list) or len(plan.plan) == 0:
            return False
            
        # Check weekly structure
        for week in plan.plan:
            if not isinstance(week, list) or len(week) == 0:
                return False
                
            # Check daily structure
            for day in week:
                if not isinstance(day, DailyPlan):
                    return False
                    
                # Check meal structure
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    meal = getattr(day, meal_type)
                    if not isinstance(meal, DailyMeal):
                        return False
        
        return True
        
    except Exception:
        return False