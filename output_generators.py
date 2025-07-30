"""
Output generation utilities for AI fitness coach.
Converts structured RunningPlan objects into various output formats.
"""

import json
from typing import Dict, Any
from models import RunningPlan, DailyPlan

def generate_html_training_plan(plan: RunningPlan) -> str:
    """
    Convert RunningPlan object to formatted HTML with CSS classes.
    Based on the actual implementation with embedded styling.
    
    Args:
        plan (RunningPlan): Structured training plan from AI response
        
    Returns:
        str: Formatted HTML string with CSS classes
    """
    try:
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Your Running Plan</title>
<link rel="stylesheet" href="style.css">
</head>
"""

        html += f"""
<body>
<header class="plan-header">
    <h1>{plan.motivation}</h1>
    <p class="plan-feedback">{plan.feedback}</p>
    <p class="plan-supplements">{plan.supplement_suggestion}</p>
</header>
"""
        
        html += f"""<div class="week-grid">"""
        
        for week_idx, weekly in enumerate(plan.plan, start=1):
            html += f'    <div class="week">\\n'
            html += f'      <h2>Week {week_idx}</h2>\\n'
            
            # Loop through each day in the week
            for day in weekly:
                html += f"""      <div class="day">
            <div class="day-title">{day.day} - {day.titles}</div>
            <div class="details">{day.details}</div>
            <div class="meal_plan">
            <h4>Nutrition Plan</h4>
            <ul>
                <li><strong>Breakfast:</strong> {day.breakfast.suggestion} - ({day.breakfast.calories} kcal)</li>
                <li><strong>Lunch:</strong> {day.lunch.suggestion} - ({day.lunch.calories} kcal)</li>
                <li><strong>Dinner:</strong> {day.dinner.suggestion} - ({day.dinner.calories} kcal)</li>
            </ul>
            </div>
        </div>
    """
            html += '    </div>\\n'
        
        # Close tags
        html += """  </div>
</body>
</html>
"""
        return html
        
    except Exception as e:
        return f"<html><body><h1>Error generating HTML</h1><p>{str(e)}</p></body></html>"

def save_training_plan_html(plan: RunningPlan, filename: str = "training_plan.html") -> bool:
    """
    Save training plan as HTML file.
    
    Args:
        plan (RunningPlan): Structured training plan
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        html = generate_html_training_plan(plan)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html)
        return True
    except Exception as e:
        print(f"❌ Error saving HTML: {str(e)}")
        return False

def print_plan_summary(plan: RunningPlan) -> None:
    """
    Print a formatted summary of the training plan to console.
    Matches the original implementation format.
    
    Args:
        plan (RunningPlan): Structured training plan
    """
    try:
        print("\\n✅ Plan Generated Successfully!\\n")
        print(f"💪 Motivation: {plan.motivation}\\n")
        print(f"📊 Feedback: {plan.feedback}\\n")
        print(f"💊 Supplements: {plan.supplement_suggestion}\\n")

        for i, weekly_schedule in enumerate(plan.plan, 1):
            print(f"--- Week {i} ---")
            for daily_activity in weekly_schedule:
                print(f"- {daily_activity.day}: {daily_activity.titles} - {daily_activity.details}")
                print(f"  🥣 Breakfast: {daily_activity.breakfast.suggestion} ({daily_activity.breakfast.calories})")
                print(f"  🥗 Lunch: {daily_activity.lunch.suggestion} ({daily_activity.lunch.calories})")
                print(f"  🍽️ Dinner: {daily_activity.dinner.suggestion} ({daily_activity.dinner.calories})")
                print()
            
    except Exception as e:
        print(f"❌ Error printing plan summary: {str(e)}")

def export_plan_to_json(plan: RunningPlan, filename: str = "training_plan.json") -> bool:
    """
    Export training plan to JSON file.
    
    Args:
        plan (RunningPlan): Structured training plan
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert Pydantic model to dict
        plan_dict = plan.model_dump()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(plan_dict, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON file exported: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error exporting JSON: {str(e)}")
        return False

def create_css_file() -> bool:
    """
    Create a CSS file for styling the HTML training plans.
    
    Returns:
        bool: True if successful, False otherwise
    """
    css_content = """
/* AI Fitness Coach - Training Plan Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.plan-header {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 30px;
    text-align: center;
}

.plan-header h1 {
    color: #2c3e50;
    margin: 0 0 20px 0;
    font-size: 2.5em;
    font-weight: 700;
}

.plan-feedback {
    background: #e8f5e8;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
    font-style: italic;
    border-left: 4px solid #27ae60;
}

.plan-supplements {
    background: #fff3cd;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
    border-left: 4px solid #ffc107;
}

.week-grid {
    display: grid;
    gap: 25px;
}

.week {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.week:hover {
    transform: translateY(-5px);
}

.week h2 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
    font-size: 1.8em;
}

.day {
    margin: 20px 0;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    border-left: 5px solid #3498db;
}

.day-title {
    font-weight: bold;
    font-size: 1.2em;
    color: #2c3e50;
    margin-bottom: 10px;
}

.details {
    margin: 10px 0;
    line-height: 1.6;
    color: #555;
}

.meal_plan {
    background: #f0f8ff;
    padding: 15px;
    border-radius: 8px;
    margin-top: 15px;
    border: 1px solid #ddd;
}

.meal_plan h4 {
    color: #2c3e50;
    margin: 0 0 10px 0;
    font-size: 1.1em;
}

.meal_plan ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.meal_plan li {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
}

.meal_plan li:last-child {
    border-bottom: none;
}

.meal_plan strong {
    color: #27ae60;
}

/* Responsive design */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .plan-header h1 {
        font-size: 2em;
    }
    
    .week {
        padding: 15px;
    }
    
    .day {
        padding: 15px;
    }
}
"""
    
    try:
        with open("style.css", "w", encoding='utf-8') as f:
            f.write(css_content)
        print("✅ CSS file created: style.css")
        return True
    except Exception as e:
        print(f"❌ Error creating CSS file: {str(e)}")
        return False

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
                print(f"❌ Missing required field: {field}")
                return False
        
        # Check that plan is a list and has content
        if not isinstance(plan.plan, list) or len(plan.plan) == 0:
            print("❌ Plan must contain at least one week")
            return False
            
        # Check weekly structure
        for week_idx, week in enumerate(plan.plan, 1):
            if not isinstance(week, list) or len(week) == 0:
                print(f"❌ Week {week_idx} must contain at least one day")
                return False
                
            # Check daily structure
            for day_idx, day in enumerate(week):
                if not isinstance(day, DailyPlan):
                    print(f"❌ Day {day_idx + 1} in week {week_idx} has invalid structure")
                    return False
                    
                # Check meal structure
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    meal = getattr(day, meal_type, None)
                    if not meal or not hasattr(meal, 'suggestion') or not hasattr(meal, 'calories'):
                        print(f"❌ Invalid {meal_type} structure in week {week_idx}, day {day_idx + 1}")
                        return False
        
        print("✅ Training plan structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error validating structure: {str(e)}")
        return False