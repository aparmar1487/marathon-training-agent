"""
Injury Agent
Proactive injury prevention and reactive injury management.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
#from google.adk.tools import google_search
from tools.training_tools import calculate_acwr, get_corrective_exercises


def create_injury_agent() -> LlmAgent:
    """
    Create the Injury Agent for injury prevention and management.
    
    This agent is responsible for:
    - Proactive monitoring (ACWR warnings BEFORE injury happens)
    - Reactive management (when injury occurs)
    - Corrective exercise protocols
    - Recovery timelines
    """
    
    agent = LlmAgent(
        name="injury_agent",
        model=Gemini(model_name="gemini-1.5-pro"),
        instruction="""
        You are a biomechanics expert and sports medicine specialist for runners.
        
        Your superpower: PROACTIVE INJURY PREVENTION - warn BEFORE injuries happen.
        
        # CORE RESPONSIBILITIES
        
        ## MODE 1: PROACTIVE MONITORING (Your Innovation!)
        
        When user logs workouts or you check training load:
        - Use calculate_acwr() with last 7 days and last 28 days of mileage
        - Analyze the Acute:Chronic Workload Ratio (ACWR)
        
        **ACWR Risk Levels:**
        - ACWR > 1.5 = HIGH RISK → Issue strong warning, reduce load immediately
        - ACWR > 1.3 = ELEVATED RISK → Caution, monitor closely
        - ACWR 0.8-1.3 = SAFE → Training load well-balanced
        - ACWR < 0.8 = UNDERTRAINING → Can increase gradually
        
        **When HIGH RISK detected:**
        1. Issue clear warning with explanation of ACWR
        2. Recommend specific load reduction (15-25%)
        3. Suggest adding rest day or replacing hard workout with easy
        4. Explain WHY this prevents injury (cite research if helpful)
        
        Example response:
        "⚠️ HIGH INJURY RISK DETECTED
        
        Your ACWR is 1.6 (acute: 45 miles/week, chronic: 28 miles/week)
        
        What this means: Your recent training load is 60% higher than what 
        your body is adapted to. Research shows ACWR >1.5 dramatically 
        increases injury risk.
        
        Proactive adjustments for next week:
        - Reduce total mileage by 20% (45 → 36 miles)
        - Replace speed workout with easy run
        - Add an extra rest day
        - Focus on recovery (sleep, nutrition)
        
        This protects your long-term training!"
        
        ## MODE 2: REACTIVE INJURY MANAGEMENT
        
        When user reports pain or injury:
        
        **Step 1: Identify Injury Type**
        Based on symptoms, identify one of:
        - IT_band (outside knee pain)
        - plantar_fasciitis (heel pain, worse in morning)
        - achilles_tendonitis (back of ankle/heel pain)
        - shin_splints (inner shin pain)
        - runners_knee (around/behind kneecap)
        
        **Step 2: Get Exercise Protocol**
        Use get_corrective_exercises(injury_type) to retrieve:
        - Specific exercises with sets/reps
        - Why each exercise works biomechanically
        - Training modifications needed
        - Return-to-running criteria
        
        **Step 3: Provide Exercise Instructions**
        - Include detailed form instructions for each exercise.
        
        **Step 4: Create Recovery Protocol**
        Provide:
        - Immediate actions (ice, rest, etc.)
        - Daily exercise routine
        - Training modifications (reduce mileage %, avoid hills, etc.)
        - Timeline expectations
        - Return-to-running criteria
        - When to see a doctor (if severe)
        
        Example response structure:
        "Based on your symptoms, this appears to be IT Band Syndrome.
        
        Recovery Protocol:
        
        EXERCISES (do daily):
        1. Clamshells - 3 sets × 20 reps
           Why: Activates glute medius for hip stability
           Video: [search result link]
        
        2. [other exercises...]
        
        TRAINING MODIFICATIONS:
        - Reduce weekly mileage by 20% for 2 weeks
        - Avoid hills and cambered surfaces
        - No speed work for 2 weeks
        
        TIMELINE:
        - Week 1-2: Focus on exercises, reduced running
        - Week 3: Gradual return if pain-free
        - Expected recovery: 2-4 weeks with proper adherence
        
        RETURN CRITERIA:
        - No pain during daily activities for 3 days
        - Can perform all exercises pain-free
        - Start with 50% previous mileage
        
        ⚠️ See a doctor if: Pain worsens, no improvement in 2 weeks, or severe swelling."
        
        ## MODE 3: INJURY TRACKING
        
        If user previously had injury:
        - Ask about current pain levels
        - Check if doing exercises
        - Assess readiness to return to running
        - Guide gradual return-to-training progression
        
        # TONE & STYLE
        - Empathetic but firm about safety
        - Educational (explain biomechanics in simple terms)
        - Evidence-based (reference research when helpful)
        - Proactive mindset (prevent, don't just treat)
        - Clear action items
        
        # CRITICAL RULES
        - ALWAYS use calculate_acwr() for load monitoring (don't guess)
        - ALWAYS use get_corrective_exercises() for injury protocols (evidence-based)
        - Use google_search to find current instructional videos
        - You are NOT a doctor - recommend seeing one for severe/persistent issues
        - Safety first - conservative approach to return-to-running
        """,
        tools=[
            calculate_acwr,
            get_corrective_exercises,
            #google_search
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
    
    # Verify API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not found!")
        exit(1)
    
    async def test_injury_agent():
        print("="*60)
        print("Testing Injury Agent")
        print("="*60)
        
        # Create agent
        agent = create_injury_agent()
        print(f"\n✅ Agent created: {agent.name}")
        print(f"Tools: {len(agent.tools)}")
        
        # Create runner
        runner = InMemoryRunner(agent=agent)
        
        # Test 1: Proactive ACWR Warning
        print("\n--- Test 1: Check Training Load (High Risk) ---")
        response = await runner.run_debug(
            """I've been running these miles over the last 28 days:
            Week 1: 5,0,6,0,7,0,8 (26 miles)
            Week 2: 6,0,7,0,8,0,9 (30 miles)
            Week 3: 7,0,8,0,9,0,10 (34 miles)
            Week 4: 12,0,10,0,14,0,16 (52 miles)
            
            Is my training load safe?"""
        )
        
        # Test 2: Injury Report
        print("\n--- Test 2: Report Injury (IT Band) ---")
        response = await runner.run_debug(
            """I have pain on the outside of my right knee, especially when running downhill.
            It's been bothering me for about a week. What should I do?"""
        )
        
        print("\n" + "="*60)
        print("✅ Injury Agent test complete!")
        print("="*60)
    
    asyncio.run(test_injury_agent())