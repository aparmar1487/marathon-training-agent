import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

# Load environment variables
load_dotenv()

# Get API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found!")
    exit()

print(f"✅ API Key loaded: {api_key[:10]}...")

# Create a simple training agent
agent = LlmAgent(
    name="training_helper",
    model=Gemini(model_name="gemini-1.5-flash"),
    instruction="""
    You are a helpful marathon training assistant.
    
    When users ask about training, provide encouraging and practical advice.
    Keep responses concise and actionable.
    """
)

print(f"✅ Agent created: {agent.name}")

# Create runner
runner = InMemoryRunner(agent=agent)

# Test the agent
print("\n🤖 Testing agent...\n")

# Use asyncio to run the async function
async def test_agent():
    response = await runner.run_debug(
        "I want to start training for a marathon. Where should I begin?"
    )
    return response

# Run the async function
response = asyncio.run(test_agent())

print("\n✅ Test complete!")