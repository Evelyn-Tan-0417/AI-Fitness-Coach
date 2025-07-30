"""
Database operations for AI fitness coach.
Handles SQLite storage and retrieval of training plans.
"""

import sqlite3
import os
from typing import Optional
from models import RunningPlan, DailyPlan, DailyMeal

def create_database_schema(db_path: str = "instance/flaskr.sqlite") -> bool:
    """
    Create the database schema for storing training plans.
    
    Args:
        db_path (str): Path to SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Create running_plan table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS running_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                motivation TEXT NOT NULL,
                feedback TEXT NOT NULL,
                supplement_suggestion TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create daily_plan table
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
        
        # Create daily_meal table
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
        return True
        
    except Exception as e:
        print(f"❌ Error creating database schema: {str(e)}")
        return False

def save_plan_to_db(plan: RunningPlan, db_path: str = "instance/flaskr.sqlite") -> Optional[int]:
    """
    Save training plan to SQLite database.
    
    Args:
        plan (RunningPlan): Structured training plan
        db_path (str): Path to SQLite database file
        
    Returns:
        Optional[int]: Running plan ID if successful, None otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Insert into running_plan table
        cur.execute(
            "INSERT INTO running_plan (motivation, feedback, supplement_suggestion) VALUES (?, ?, ?)",
            (plan.motivation, plan.feedback, plan.supplement_suggestion),
        )
        running_plan_id = cur.lastrowid

        # Insert weekly schedules and daily plans
        for week_num, weekly_schedule in enumerate(plan.plan, start=1):
            for daily in weekly_schedule:
                # Insert daily plan
                cur.execute(
                    "INSERT INTO daily_plan (running_plan_id, day, titles, details, week_number) VALUES (?, ?, ?, ?, ?)",
                    (running_plan_id, daily.day, daily.titles, daily.details, week_num),
                )
                daily_plan_id = cur.lastrowid

                # Insert meals for this day
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    meal = getattr(daily, meal_type)
                    cur.execute(
                        "INSERT INTO daily_meal (daily_plan_id, meal_type, suggestion, calories) VALUES (?, ?, ?, ?)",
                        (daily_plan_id, meal_type, meal.suggestion, meal.calories),
                    )

        conn.commit()
        conn.close()
        return running_plan_id
        
    except Exception as e:
        print(f"❌ Error saving to database: {str(e)}")
        return None

def load_plan_from_db(plan_id: int, db_path: str = "instance/flaskr.sqlite") -> Optional[RunningPlan]:
    """
    Load a training plan from the database by ID.
    
    Args:
        plan_id (int): ID of the plan to load
        db_path (str): Path to SQLite database file
        
    Returns:
        Optional[RunningPlan]: Reconstructed training plan object or None
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Get plan details
        cur.execute("SELECT motivation, feedback, supplement_suggestion FROM running_plan WHERE id = ?", (plan_id,))
        plan_data = cur.fetchone()
        
        if not plan_data:
            print(f"❌ Plan with ID {plan_id} not found")
            return None
        
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
                breakfast=DailyMeal(suggestion=breakfast_suggestion, calories=breakfast_calories),
                lunch=DailyMeal(suggestion=lunch_suggestion, calories=lunch_calories),
                dinner=DailyMeal(suggestion=dinner_suggestion, calories=dinner_calories)
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
        return None

def list_all_plans(db_path: str = "instance/flaskr.sqlite") -> list:
    """
    List all training plans in the database.
    
    Args:
        db_path (str): Path to SQLite database file
        
    Returns:
        list: List of plan summaries
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        cur.execute('''
            SELECT id, motivation, created_at 
            FROM running_plan 
            ORDER BY created_at DESC
        ''')
        
        plans = cur.fetchall()
        conn.close()
        
        return [
            {
                "id": plan[0],
                "motivation": plan[1][:50] + "..." if len(plan[1]) > 50 else plan[1],
                "created_at": plan[2]
            }
            for plan in plans
        ]
        
    except Exception as e:
        print(f"❌ Error listing plans: {str(e)}")
        return []

def delete_plan(plan_id: int, db_path: str = "instance/flaskr.sqlite") -> bool:
    """
    Delete a training plan and all associated data.
    
    Args:
        plan_id (int): ID of the plan to delete
        db_path (str): Path to SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Delete in reverse order of foreign key dependencies
        cur.execute('''
            DELETE FROM daily_meal 
            WHERE daily_plan_id IN (
                SELECT id FROM daily_plan WHERE running_plan_id = ?
            )
        ''', (plan_id,))
        
        cur.execute('DELETE FROM daily_plan WHERE running_plan_id = ?', (plan_id,))
        cur.execute('DELETE FROM running_plan WHERE id = ?', (plan_id,))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error deleting plan: {str(e)}")
        return False