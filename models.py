"""
Pydantic models for AI fitness coach structured output.
Defines data structures for training plans, meals, and daily activities.
"""

from pydantic import BaseModel, Field
from typing import List

class DailyMeal(BaseModel):
    """Model for individual meal recommendations."""
    suggestion: str
    calories: str

class DailyPlan(BaseModel):
    """Model for a single day's training and nutrition plan."""
    day: str
    titles: str
    details: str
    breakfast: DailyMeal
    lunch: DailyMeal
    dinner: DailyMeal

# Type alias for a week's worth of daily plans
WeeklyPlan = List[DailyPlan]

class RunningPlan(BaseModel):
    """Complete running plan with motivation, feedback, and weekly schedules."""
    motivation: str
    feedback: str
    supplement_suggestion: str
    plan: List[WeeklyPlan]

# System prompt for the AI fitness coach
SYSTEM_PROMPT = """You are an expert running coach. First, determine the total number of training weeks required from the user's query. Then, generate a running plan with a 'motivation' message, 'feedback' message from the stats provided on the uploaded image, 'supplement suggestion' for suggestion the supplements that the person should take for their best performance, and a 'plan' list, where each item in the list represents one week's schedule. Again, make sure to match the number of weeks exactly, no more and no fewer weeks. Also, please include a daily breakfast, lunch, and dinner suggestion that has the name of the meal and the calories"""