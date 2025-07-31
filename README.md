# AI Fitness Coach 🏃‍♀️🤖

An intelligent coaching system that analyzes Apple Watch fitness data to generate personalized training plans and nutrition recommendations using AI.

## Features

- **Apple Watch Data Analysis**: Process fitness screenshots to extract VO2 max, training volume, and performance metrics
- **Structured Data Models**: Uses Pydantic models for type-safe, validated output generation
- **Personalized Training Plans**: Generate progressive training schedules with specific activities and intensities  
- **Integrated Nutrition Planning**: Create daily meal plans with breakfast, lunch, and dinner suggestions including calorie counts
- **Motivational Coaching**: Provides personalized motivation messages and performance feedback
- **Supplement Recommendations**: Suggests appropriate supplements based on training goals
- **Multiple Output Formats**: Produces HTML, JSON, and database-stored plans
- **Database Integration**: SQLite storage for persistent plan management

## Example Output

The `examples/` directory contains a complete workflow demonstration:

- **`01_apple_watch_input.png`** - Apple Watch fitness data showing VO2 max (52), daily distance (16.4km), and activity metrics
- **`02_console_output_part1.png`** - System processing and initial results generation
- **`03_console_output_part2.png`** - Complete console output with motivation, feedback, and structured plan
- **`04_html_output_part1.png`** - Generated HTML training plan (weeks 1-4) with integrated nutrition
- **`05_html_output_part2.png`** - Complete HTML training plan (weeks 5-8) showing progression
- **`sample_output.json`** - Raw JSON structure of the AI-generated training plan

These examples demonstrate the complete pipeline from Apple Watch data input to professional training plan output.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-fitness-coach.git
   cd ai-fitness-coach
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration (choose one method)**

   **Option A: Using config.py (Recommended)**
   ```bash
   # Copy the example config file
   cp config_example.py config.py
   
   # Edit config.py and add your OpenAI API key
   # OPENAI_API_KEY = "your-actual-api-key-here"
   ```

   **Option B: Using environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your API key
   # OPENAI_API_KEY=your-actual-api-key-here
   ```

4. **Add your Apple Watch screenshot**
   - Take a screenshot of your Apple Watch fitness data
   - Save it as `IMG_4830.png` in the project root
   - Or update the path in `config.py`

5. **Run the application**
   ```bash
   python main.py
   ```

## Project Structure

```
ai-fitness-coach/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example                    # Environment variables template
├── config_example.py               # Configuration template (copy to config.py)
├── main.py                         # Main application entry point
├── models.py                       # Pydantic data models and prompts
├── database.py                     # SQLite database operations
├── utils.py                        # Image processing and utilities
├── output_generators.py            # HTML/JSON output generation
├── examples/
│   ├── 01_apple_watch_input.png    # Example Apple Watch fitness data
│   ├── 02_console_output_part1.png # System processing output (part 1)
│   ├── 03_console_output_part2.png # System processing output (part 2)
│   ├── 04_html_output_part1.png    # Generated HTML training plan (weeks 1-4)
│   ├── 05_html_output_part2.png    # Generated HTML training plan (weeks 5-8)
│   └── sample_output.json          # Example structured JSON output
├── instance/                       # Auto-created directory
│   └── flaskr.sqlite              # SQLite database (auto-created)
└── docs/
    └── blog_post.md               # Detailed explanation blog post
```

## How It Works

### 1. Structured Data Models
```python
from pydantic import BaseModel

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

class RunningPlan(BaseModel):
    motivation: str
    feedback: str
    supplement_suggestion: str
    plan: List[List[DailyPlan]]
```

### 2. AI Analysis with Structured Output
```python
# From main.py
response = client.responses.parse(
    model="gpt-4o",
    input=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": [
            {"type": "input_text", "text": user_query},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}
        ]}
    ],
    text_format=RunningPlan
)
plan = response.output_parsed
```

### 3. Multiple Output Formats
- **Console Display**: Formatted plan summary with emojis and structure
- **HTML Generation**: Professional web page with embedded CSS styling
- **Database Storage**: SQLite database with normalized relational structure
- **JSON Export**: Structured data for API integration and portability

## Key Technologies

- **OpenAI GPT-4o**: Latest model with enhanced multimodal capabilities
- **Pydantic**: Type-safe data validation and structured output parsing
- **Computer Vision**: Apple Watch screenshot processing and data extraction
- **SQLite Database**: Persistent storage with relational data structure
- **Modern OpenAI API**: Using `responses.parse()` method with `text_format` parameter
- **Multi-format Output**: HTML with CSS classes, JSON export, database storage

## Example Use Cases

- **Recreational Runners**: Generate progressive training plans for 5K to marathon goals
- **Fitness Enthusiasts**: Get nutrition plans aligned with training intensity
- **Coaches**: Create personalized programs based on actual performance data
- **Developers**: Integrate AI fitness intelligence into health apps

## Contributing

This project demonstrates practical AI application development for health and fitness. Contributions welcome for:

- Additional fitness metric processing
- Enhanced nutrition databases  
- Integration with other wearable devices
- Performance optimization
- Web interface development
- Mobile app integration

## Development Setup

For contributors:

1. **Fork and clone the repository**
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows
   ```
3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up your config.py file**
5. **Run tests** (when available)
6. **Submit pull requests**

## License

MIT License - see LICENSE file for details.

## Disclaimer

This system is designed as a technology demonstration and educational tool. It is not intended as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers regarding fitness and nutrition decisions.

## Contact

Questions or collaboration opportunities? Feel free to reach out!

---

*Read the full development story and technical insights in our [blog post](docs/blog_post.md).*