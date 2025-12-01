"""
Planning Agent
Creates personalized training plans and handles milestone continuity.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from tools.training_tools import (
    adjust_paces_from_race,
    calculate_weekly_mileage_progression
)


def create_planning_agent() -> LlmAgent:
    """
    Create the Planning Agent with milestone continuity logic.
    
    This agent is responsible for:
    - Creating training plans based on user profile
    - Handling milestone race results
    - Adjusting Phase 2 based on actual performance
    - Providing daily/weekly workouts
    """
    
    agent = LlmAgent(
        name="planning_agent",
        model=Gemini(model_name="gemini-1.5-pro"),
        instruction="""
        You are an expert marathon training coach specializing in PROGRESSIVE PERIODIZATION.
        
        Your superpower: MILESTONE CONTINUITY - training phases build on actual results.
        
        # CORE RESPONSIBILITIES
        
        ## 1. CREATE TRAINING PLANS
        When user sets a goal with milestone race:
        - Design Phase 1: Build to milestone race (e.g., 12 weeks)
        - Design Phase 2: Build to goal race FROM milestone fitness (e.g., 12 weeks)
        - Phase 2 is ADAPTIVE - adjusts based on milestone results
        
        ## 2. MILESTONE CONTINUITY (YOUR KEY INNOVATION)
        When user completes milestone race:
        - Use adjust_paces_from_race() tool with race distance and time
        - Update ALL training paces for Phase 2 based on new VDOT
        - CRITICAL: Phase 2 starts from CURRENT fitness level, NOT from scratch
        - If they ran faster than predicted: upgrade goal, increase Phase 2 mileage
        - If they ran slower: adjust goal conservatively, modify Phase 2
        
        Example:
        User completes 18-mile race in 2:24 (8:00/mile), faster than predicted 8:30/mile
        → Use adjust_paces_from_race(18, 144)
        → New tempo pace: 7:45/mile (was 8:00/mile)
        → New marathon goal: 3:28 (was 3:40)
        → Phase 2 starts at 40 miles/week (current fitness), NOT 25 miles
        
        ## 3. SAFE MILEAGE PROGRESSION
        Use calculate_weekly_mileage_progression() to ensure safe buildup:
        - Beginner: max 10% increase per week
        - Intermediate: max 12% per week
        - Advanced: max 15% per week
        - Every 4th week is recovery week (reduce 20%)
        
        ## 4. PROVIDE SPECIFIC WORKOUTS
        When user asks for workouts, give SPECIFIC details:
        - Day of week
        - Workout type (easy, tempo, intervals, long run)
        - Distance in miles
        - Pace ranges (use adjusted paces if post-milestone)
        - Purpose/why this workout matters
        
        # USER PROFILE CONTEXT
        Always consider from profile:
        - Current weekly mileage (starting point)
        - Ability level (affects progression rate)
        - Goal race date (timeline for plan)
        - Milestone race date and distance (if applicable)
        
        # TONE & STYLE
        - Encouraging but realistic
        - Explain WHY behind workouts
        - Celebrate milestone achievements
        - Clear about adjustments made
        
        # CRITICAL RULES
        - NEVER restart training from scratch after milestone
        - ALWAYS use tools for calculations (don't guess paces)
        - Phase 2 builds FROM Phase 1, not independently
        - Safety first - use proper progression rates
        """,
        tools=[
            adjust_paces_from_race,
            calculate_weekly_mileage_progression
        ]
    )
    
    return agent


# Test the agent if run directly
if __name__ == "__main__":
    import asyncio
    from google.adk.runners import InMemoryRunner
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Verify API key is loaded
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not found in environment!")
        print("Make sure .env file exists with your API key")
        exit(1)
    async def test_planning_agent():
        print("="*60)
        print("Testing Planning Agent")
        print("="*60)
        
        # Create agent
        agent = create_planning_agent()
        print(f"\n✅ Agent created: {agent.name}")
        print(f"Model: gemini-1.5-pro")
        print(f"Tools: {len(agent.tools)}")
        
        # Create runner
        runner = InMemoryRunner(agent=agent)
        
        # Test 1: Ask for training plan
        print("\n--- Test 1: Request Training Plan ---")
        response = await runner.run_debug(
            """I'm an intermediate runner currently at 25 miles per week.
            I want to run a marathon in 24 weeks with an 18-mile race at week 12.
            Can you create my training plan?"""
        )
        
        # Test 2: Report milestone result
        print("\n--- Test 2: Report Milestone Race ---")
        response = await runner.run_debug(
            """I just completed my 18-mile milestone race in 2 hours and 24 minutes.
            How should my training adjust for the remaining weeks to marathon?"""
        )
        
        print("\n" + "="*60)
        print("✅ Planning Agent test complete!")
        print("="*60)
    
    asyncio.run(test_planning_agent())