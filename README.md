# Marathon Training Agent

AI-powered marathon training coach with milestone continuity and proactive injury prevention.

## Key Features

✅ **Milestone Continuity** - Training phases adapt based on actual race results  
✅ **Proactive Injury Prevention** - ACWR monitoring warns BEFORE injuries happen  
✅ **Multi-Agent System** - Specialized agents for training and injury management  
✅ **Personalized Plans** - Based on ability level, goals, and current fitness  

## Architecture

- **Orchestrator Agent** - Routes user requests to specialists
- **Planning Agent** - Creates training plans, handles milestone continuity
- **Injury Agent** - Monitors training load (ACWR), manages injuries
- **Custom Tools** - ACWR calculator, pace adjuster, exercise library

## Setup

### Prerequisites
- Python 3.9+
- Google AI Studio API key ([Get one here](https://aistudio.google.com/apikey))

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/marathon-training-agent
cd marathon-training-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GOOGLE_API_KEY=your-key-here" > .env
```

### Run
```bash
python main.py
```

## Usage

1. **Create Profile** - Enter email, name, goal, ability level
2. **Chat with Coach** - Ask anything about training or injuries
3. **Quick Actions** - Get training plan, check ACWR, report injuries

### Example Interactions

**Training Plan:**
```
User: "I want to train for a marathon in 6 months with an 18-mile race at month 3"
Agent: Creates 2-phase progressive plan
```

**Milestone Continuity:**
```
User: "I finished 18 miles in 2:24"
Agent: Adjusts Phase 2 paces and marathon prediction based on actual performance
```

**Proactive Injury Prevention:**
```
User: Logs rapid mileage increase
Agent: "⚠️ HIGH RISK - Your ACWR is 1.6. Reduce load by 20% this week."
```

## Innovation

### What Makes This Different

**Existing Apps (Runna, etc.):**
- Static plans that don't adapt
- Milestone races treated as separate training blocks
- Reactive injury management (after pain starts)

**This System:**
- ✅ Dynamic: Phase 2 adjusts from actual milestone results
- ✅ Continuous: Training builds progressively across phases
- ✅ Proactive: Warns about injury risk BEFORE pain starts

## Technical Details

**Framework:** Google ADK (Agent Development Kit)  
**Model:** Gemini 1.5 Pro/Flash  
**Language:** Python 3.11  
**Tools:** Custom Function Tools + Built-in Google Tools  

## Project Structure
```
marathon-training-agent/
├── agents/              # Multi-agent system
│   ├── orchestrator.py
│   ├── planning_agent.py
│   └── injury_agent.py
├── tools/               # Custom function tools
│   └── training_tools.py
├── data/                # Exercise library
│   └── exercise_library.json
├── sessions/            # User profile management
│   ├── profile_manager.py
│   └── setup_profile.py
└── main.py             # Entry point
```

## Known Limitations

- Training plans are session-based (not persisted across restarts)
- Single-user sessions (multi-user requires separate logins)

## Future Enhancements

- Persistent plan storage in user profiles
- Google Maps integration for location-aware workouts
- Strava API integration for automatic workout logging
- Video search for exercise demonstrations

## Author

Abhishek  
Google Agentic AI Capstone Project  
December 2025