"""
Output generation utilities for AI fitness coach.
Converts structured RunningPlan objects into various output formats and database storage.
"""

import sqlite3
from typing import Dict, Any
from prompt_templates import RunningPlan, DailyPlan

def generate_html_training_plan(plan: RunningPlan) -> str:
    """
    Convert RunningPlan object to formatted HTML with embedded CSS classes.
    
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
        print(f"✅ HTML file generated: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving HTML: {str(e)}")
        return False

def save_plan_to_db(plan: RunningPlan, db_path: str = "instance/flaskr.sqlite") -> bool:
    """
    Save training plan to SQLite database.
    
    Args:
        plan (RunningPlan): Structured training plan
        db_path (str): Path to SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Insert into running_plan
        cur.execute(
            "INSERT INTO running_plan (motivation, feedback, supplement_suggestion) VALUES (?, ?, ?)",
            (plan.motivation, plan.feedback, plan.supplement_suggestion),
        )
        running_plan_id = cur.lastrowid

        for week_num, weekly_schedule in enumerate(plan.plan, start=1):
            for daily in weekly_schedule:
                cur.execute(
                    "INSERT INTO daily_plan (running_plan_id, day, titles, details, week_number) VALUES (?, ?, ?, ?, ?)",
                    (running_plan_id, daily.day, daily.titles, daily.details, week_num),
                )
                daily_plan_id = cur.lastrowid

                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    meal = getattr(daily, meal_type)
                    cur.execute(
                        "INSERT INTO daily_meal (daily_plan_id, meal_type, suggestion, calories) VALUES (?, ?, ?, ?)",
                        (daily_plan_id, meal_type, meal.suggestion, meal.calories),
                    )

        conn.commit()
        conn.close()
        print(f"✅ Plan saved to database: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving to database: {str(e)}")
        return False

def create_database_schema(db_path: str = "instance/flaskr.sqlite") -> bool:
    """
    Create the database schema for storing training plans.
    
    Args:
        db_path (str): Path to SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Create tables
        cur.execute('''
            CREATE TABLE IF NOT EXISTS running_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                motivation TEXT NOT NULL,
                feedback TEXT NOT NULL,
                supplement_suggestion TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS daily_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                running_plan_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                titles TEXT NOT NULL,
                details TEXT NOT NULL,
                week_number INTEGER NOT NULL,
                FOREIGN KEY (running_plan_id) REFERENCES running_plan (id)
            )
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS daily_meal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                daily_plan_id INTEGER NOT NULL,
                meal_type TEXT NOT NULL,
                suggestion TEXT NOT NULL,
                calories TEXT NOT NULL,
                FOREIGN KEY (daily_plan_id) REFERENCES daily_plan (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database schema created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database schema: {str(e)}")
        return False

def print_plan_summary(plan: RunningPlan) -> None:
    """
    Print a formatted summary of the training plan to console.
    
    Args:
        plan (RunningPlan): Structured training plan
    """
    try:
        print("\\n✅ Plan Generated Successfully!\\n")
        print(f"Motivation: {plan.motivation}\\n")
        print(f"Feedback: {plan.feedback}\\n")
        print(f"Supplements: {plan.supplement_suggestion}\\n")

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
        import json
        
        # Convert Pydantic model to dict
        plan_dict = plan.model_dump()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(plan_dict, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON file exported: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error exporting JSON: {str(e)}")
        return False

def load_plan_from_db(plan_id: int, db_path: str = "instance/flaskr.sqlite") -> RunningPlan:
    """
    Load a training plan from the database by ID.
    
    Args:
        plan_id (int): ID of the plan to load
        db_path (str): Path to SQLite database file
        
    Returns:
        RunningPlan: Reconstructed training plan object
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Get plan details
        cur.execute("SELECT motivation, feedback, supplement_suggestion FROM running_plan WHERE id = ?", (plan_id,))
        plan_data = cur.fetchone()
        
        if not plan_data:
            raise ValueError(f"Plan with ID {plan_id} not found")
        
        motivation, feedback, supplement_suggestion = plan_data
        
        # Get daily plans grouped by week
        cur.execute('''
            SELECT dp.day, dp.titles, dp.details, dp.week_number,
                   dm1.suggestion as breakfast_suggestion, dm1.calories as breakfast_calories,
                   dm2.suggestion as lunch_suggestion, dm2.calories as lunch_calories,
                   dm3.suggestion as dinner_suggestion, dm3.calories as dinner_calories
            FROM daily_plan dp
            LEFT JOIN daily_meal dm1 ON dp.id = dm1.daily_plan_id AND dm1.meal_type = 'breakfast'
            LEFT JOIN daily_meal dm2 ON dp.id = dm2.daily_plan_id AND dm2.meal_type = 'lunch'
            LEFT JOIN daily_meal dm3 ON dp.id = dm3.daily_plan_id AND dm3.meal_type = 'dinner'
            WHERE dp.running_plan_id = ?
            ORDER BY dp.week_number, dp.day
        ''', (plan_id,))
        
        daily_data = cur.fetchall()
        conn.close()
        
        # Reconstruct the plan structure
        weeks = {}
        for row in daily_data:
            day, titles, details, week_num = row[:4]
            breakfast_suggestion, breakfast_calories = row[4:6]
            lunch_suggestion, lunch_calories = row[6:8]
            dinner_suggestion, dinner_calories = row[8:10]
            
            if week_num not in weeks:
                weeks[week_num] = []
            
            daily_plan = DailyPlan(
                day=day,
                titles=titles,
                details=details,
                breakfast={"suggestion": breakfast_suggestion, "calories": breakfast_calories},
                lunch={"suggestion": lunch_suggestion, "calories": lunch_calories},
                dinner={"suggestion": dinner_suggestion, "calories": dinner_calories}
            )
            weeks[week_num].append(daily_plan)
        
        # Convert to list of weeks
        plan_weeks = [weeks[week_num] for week_num in sorted(weeks.keys())]
        
        return RunningPlan(
            motivation=motivation,
            feedback=feedback,
            supplement_suggestion=supplement_suggestion,
            plan=plan_weeks
        )
        
    except Exception as e:
        print(f"❌ Error loading plan from database: {str(e)}")
        raise