# AI Fitness Coach 

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

**Input**: Apple Watch screenshot + "run a 10k in 8 weeks"
**Output**: 
- **Motivation**: *"🏃‍♂️ You're embarking on an amazing 8-week journey to crush your 10K goal! Every step you take brings you closer to that finish line..."*
- **Feedback**: *"Based on your Apple Watch data showing excellent cardiovascular fitness and consistent daily activity, your body is well-prepared for this 10K challenge."*
- **Supplement Recommendations**: Multivitamin, electrolytes, omega-3s, and protein supplements
- **8-week structured plan** with daily training activities and complete meal plans
- **Daily nutrition**: "Oatmeal with banana and almonds (420 kcal)", "Grilled chicken salad with quinoa (520 kcal)"

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

3. **Set up your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run the notebook**
   ```bash
   jupyter notebook ai_fitness_coach.ipynb
   ```

## Project Structure

```
ai-fitness-coach/
├── README.md
├── requirements.txt
├── ai_fitness_coach.ipynb          # Main implementation notebook
├── src/
│   ├── image_processing.py         # Apple Watch screenshot processing
│   ├── prompt_templates.py         # AI prompt engineering
│   └── output_generators.py       # HTML/JSON generation
├── examples/
│   ├── sample_apple_watch.png      # Example input image
│   ├── sample_training_plan.html   # Example output
│   └── sample_output.json          # Example structured data
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

### 2. AI Analysis with New API
```python
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
- **Console Display**: Formatted plan summary with emojis
- **HTML Generation**: Professional web page with embedded CSS
- **Database Storage**: SQLite database with relational structure
- **JSON Export**: Structured data for API integration

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
- Expanded nutrition databases  
- Integration with other wearable devices
- Performance optimization

## License

MIT License - see LICENSE file for details.

## Disclaimer

This system is designed as a technology demonstration and educational tool. It is not intended as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers regarding fitness and nutrition decisions.

## Contact

Questions or collaboration opportunities? Feel free to reach out!

---

*Read the full development story and technical insights in our [blog post](docs/blog_post.md).*
