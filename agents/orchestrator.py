"""
Orchestrator Agent
Routes user requests to Planning Agent or Injury Agent.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from agents.planning_agent import create_planning_agent
from agents.injury_agent import create_injury_agent


def create_orchestrator() -> LlmAgent:
    """
    Create the Orchestrator Agent that coordinates specialist agents.
    
    This agent is responsible for:
    - Understanding user intent
    - Routing to Planning Agent or Injury Agent
    - Returning the specialist's response
    """
    
    # Create specialist agents
    planning_agent = create_planning_agent()
    injury_agent = create_injury_agent()
    
    # Create orchestrator that uses them as tools
    orchestrator = LlmAgent(
        name="orchestrator",
        model=Gemini(model_name="gemini-1.5-flash"),  # Fast for routing
        instruction="""
        You are an intelligent routing agent for a marathon training system.
        
        CRITICAL: You are a ROUTER, not a coach. Your ONLY job is to delegate to specialists.
        
        # YOUR ONLY TASK
        
        Read the user's question and IMMEDIATELY call the appropriate specialist agent.
        DO NOT answer questions yourself.
        DO NOT ask for more information - the user profile contains everything needed.
        DO NOT add commentary - just route and return the specialist's response.
        
        # AVAILABLE SPECIALISTS
        
        ## planning_agent
        Use for:
        - Creating training plans
        - Requesting workout schedules
        - Getting today's/this week's workouts
        - Training phases, paces, mileage
        - Milestone races and adjustments
        - ANY question about training, workouts, or race preparation
        
        ## injury_agent  
        Use for:
        - Reporting pain or injuries
        - Checking if training load is safe (ACWR)
        - Getting corrective exercises
        - Recovery questions
        - ANY question about pain, injury, or safety
        
        # ROUTING RULES
        
        1. If user asks about training/workouts/plans → Call planning_agent IMMEDIATELY
        2. If user asks about injury/pain/ACWR → Call injury_agent IMMEDIATELY
        3. If unclear → Default to planning_agent
        4. NEVER respond yourself - ALWAYS call a specialist
        
        # EXAMPLES
        
        User: "What's my workout today?"
        → IMMEDIATELY call planning_agent (don't ask questions)
        
        User: "Create my training plan"
        → IMMEDIATELY call planning_agent (don't ask for more info)
        
        User: "My knee hurts"  
        → IMMEDIATELY call injury_agent (don't ask questions)
        
        User: "I ran 50 miles this week, is that safe?"
        → IMMEDIATELY call injury_agent (don't ask questions)
        
        The user profile contains all necessary information. Trust it and route immediately.
        """,
        tools=[
            AgentTool(agent=planning_agent),
            AgentTool(agent=injury_agent)
        ]
    )
    
    return orchestrator


# Test the orchestrator if run directly
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
    
    async def test_orchestrator():
        print("="*60)
        print("Testing Orchestrator Agent")
        print("="*60)
        
        # Create orchestrator
        orchestrator = create_orchestrator()
        print(f"\n✅ Orchestrator created: {orchestrator.name}")
        print(f"Specialist agents available: {len(orchestrator.tools)}")
        
        # Create runner
        runner = InMemoryRunner(agent=orchestrator)
        
        # Test 1: Training question (should route to Planning Agent)
        print("\n--- Test 1: Training Question (→ Planning Agent) ---")
        response = await runner.run_debug(
            "I want to train for a marathon in 6 months. Can you create my plan?"
        )
        
        # Test 2: Injury question (should route to Injury Agent)
        print("\n--- Test 2: Injury Question (→ Injury Agent) ---")
        response = await runner.run_debug(
            "My IT band hurts on the outside of my knee. What should I do?"
        )
        
        # Test 3: ACWR check (should route to Injury Agent)
        print("\n--- Test 3: Load Check (→ Injury Agent) ---")
        response = await runner.run_debug(
            "I jumped from 30 to 50 miles this week. Is that safe?"
        )
        
        print("\n" + "="*60)
        print("✅ Orchestrator test complete!")
        print("="*60)
    
    asyncio.run(test_orchestrator())