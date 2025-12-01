"""
Marathon Training Agent - Main Application
Entry point for the training assistant
"""

import asyncio
import os
from dotenv import load_dotenv
from sessions.profile_manager import load_profile, list_all_users
from sessions.setup_profile import setup_profile
from agents.orchestrator import create_orchestrator
from agents.planning_agent import create_planning_agent  
from agents.injury_agent import create_injury_agent     
from google.adk.runners import InMemoryRunner

# Load environment variables
load_dotenv()


def display_welcome():
    """Display welcome banner."""
    print("\n" + "="*60)
    print("🏃 MARATHON TRAINING AGENT")
    print("="*60)
    print("Your AI-powered training coach with:")
    print("  • Milestone continuity (training phases build on each other)")
    print("  • Proactive injury prevention (ACWR monitoring)")
    print("  • Personalized training plans")
    print("="*60)


def get_user_profile():
    """
    Get user profile (login or signup).
    Returns UserProfile object.
    """
    # Show existing users
    existing_users = list_all_users()
    
    if existing_users:
        print(f"\n📋 Registered users: {len(existing_users)}")
        for user_info in existing_users:
            print(f"  • {user_info}")
    
    print("\n--- User Login/Signup ---")
    email = input("Enter your email: ").strip().lower()
    
    # Try to load existing profile
    profile = load_profile(email)
    
    if profile:
        print(f"\n✅ Welcome back, {profile.name}!")
        print(f"Goal: {profile.goal_distance} | Level: {profile.ability_level}")
        
        # Option to update profile
        update = input("\nUpdate your profile? (yes/no) ").strip().lower()
        if update in ['yes', 'y']:
            print("\nStarting profile update...")
            profile = setup_profile()
            profile.email = email  # Keep same email
    else:
        print(f"\n🆕 New user! Let's create your profile.")
        profile = setup_profile()
        profile.email = email  # Set the email
    
    return profile


async def chat_with_agent(orchestrator, runner, profile):
    """
    Interactive chat loop with the orchestrator agent.
    
    Args:
        orchestrator: The orchestrator agent
        runner: InMemoryRunner for the agent
        profile: User profile with training info
    """
    # Create profile context string
    profile_context = f"""
    User Profile:
    - Name: {profile.name}
    - Age: {profile.age}
    - Goal: {profile.goal_distance}
    - Ability Level: {profile.ability_level}
    - Current Weekly Mileage: {profile.current_weekly_mileage} miles
    - Goal Race Date: {profile.goal_race_date.strftime('%Y-%m-%d')}
    """
    
    if profile.has_milestone:
        profile_context += f"""
    - Milestone Race: {profile.milestone_distance} miles on {profile.milestone_date.strftime('%Y-%m-%d')}
        """
    
    print("\n" + "="*60)
    print(f"CHAT WITH YOUR TRAINING COACH")
    print("="*60)
    print("\nI can help you with:")
    print("  • Training plans and workouts")
    print("  • Milestone race adjustments")
    print("  • Injury prevention and ACWR monitoring")
    print("  • Recovery protocols and exercises")
    print("\nType 'menu' to return to main menu, 'exit' to quit")
    print("="*60)
    
    while True:
        user_input = input(f"\n{profile.name}> ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['exit', 'quit']:
            print(f"\n👋 Goodbye, {profile.name}! Keep training!")
            break
        
        if user_input.lower() == 'menu':
            return  # Return to main menu
        
        # Add profile context to user message
        full_message = f"{profile_context}\n\nUser question: {user_input}"
        
        try:
            print(f"\n🤖 Coach: ")
            
            # Get response from agent
            response = await runner.run_debug(full_message)
            
            # Extract text from response
            if hasattr(response, 'text'):
                print(response.text)
            elif isinstance(response, list) and len(response) > 0:
                for event in response:
                    if hasattr(event, 'text') and event.text:
                        print(event.text)
            else:
                print("No response received")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'menu' to return to main menu.")


async def main():
    """Main application loop."""
    
    # Verify API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not found!")
        print("Please create a .env file with your API key")
        return
    
    # Display welcome
    display_welcome()
    
    # Get user profile
    profile = get_user_profile()
    
    if not profile:
        print("\n❌ No profile created. Exiting.")
        return
    
    # Create orchestrator agent
    print("\n⚙️  Initializing AI training coach...")
    orchestrator = create_orchestrator()
    planning_agent = create_planning_agent()
    injury_agent = create_injury_agent()
    
    orchestrator_runner = InMemoryRunner(agent=orchestrator)
    planning_runner = InMemoryRunner(agent=planning_agent)
    injury_runner = InMemoryRunner(agent=injury_agent)
    print("✅ Training coach ready!\n")
    
    # Main menu
    while True:
        print("\n" + "="*60)
        print(f"MAIN MENU - {profile.name.upper()}")
        print("="*60)
        print("1. Chat with training coach (ask anything!)")
        print("2. Quick: Get training plan")
        print("3. Quick: Get today's workout")
        print("4. Quick: Check training load (ACWR)")
        print("5. Quick: Report injury")
        print("6. Update profile")
        print("7. Exit")
        print("="*60)
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            # Free-form chat
            await chat_with_agent(orchestrator, orchestrator_runner, profile)
        
        elif choice == "2":
            # Quick: Get training plan
            print("\n🤖 Coach: ")
            message = f"""
            User Profile:
            - Name: {profile.name}
            - Goal: {profile.goal_distance}
            - Ability Level: {profile.ability_level}
            - Current Weekly Mileage: {profile.current_weekly_mileage} miles
            - Goal Race Date: {profile.goal_race_date.strftime('%Y-%m-%d')}
            {"- Milestone: " + str(profile.milestone_distance) + " miles on " + profile.milestone_date.strftime('%Y-%m-%d') if profile.has_milestone else ""}
            
            User question: Can you create my complete training plan?
            """
            
            response = await planning_runner.run_debug(message)
            
            # Extract text from response
            if hasattr(response, 'text'):
                print(response.text)
            elif isinstance(response, list) and len(response) > 0:
                for event in response:
                    if hasattr(event, 'text') and event.text:
                        print(event.text)
            else:
                print("No response received")
        
        elif choice == "3":
            # Quick: Today's workout
            print("\n🤖 Coach: ")
            message = f"""
            User Profile:
            - Name: {profile.name}
            - Age: {profile.age}
            - Goal: {profile.goal_distance}
            - Ability Level: {profile.ability_level}
            - Current Weekly Mileage: {profile.current_weekly_mileage} miles
            - Goal Race Date: {profile.goal_race_date.strftime('%Y-%m-%d')}
            {"- Milestone: " + str(profile.milestone_distance) + " miles on " + profile.milestone_date.strftime('%Y-%m-%d') if profile.has_milestone else ""}
            
            User question: What's my workout for today?
            """
            
            response = await planning_runner.run_debug(message)
            
            # Extract text from response
            if hasattr(response, 'text'):
                print(response.text)
            elif isinstance(response, list) and len(response) > 0:
                for event in response:
                    if hasattr(event, 'text') and event.text:
                        print(event.text)
            else:
                print("No response received")
        
        elif choice == "4":
            # Quick: ACWR check
            print("\n📊 Training Load Check")
            print("Enter your daily mileage for the last 28 days (comma-separated):")
            print("Example: 5,0,6,0,7,0,8,0,6,0,7,0,8,0,9,0,7,0,8,0,9,0,10,0,8,0,9,0,10,0")
            mileage_input = input("> ").strip()
            
            print("\n🤖 Coach: ")
            message = f"""
            User has logged these daily miles over the last 28 days:
            {mileage_input}
            
            User question: Is my training load safe? What's my ACWR?
            """
            
            response = await injury_runner.run_debug(message)
            
            # Extract text from response
            if hasattr(response, 'text'):
                print(response.text)
            elif isinstance(response, list) and len(response) > 0:
                for event in response:
                    if hasattr(event, 'text') and event.text:
                        print(event.text)
            else:
                print("No response received")
        
        elif choice == "5":
            # Quick: Report injury
            print("\n🩹 Injury Report")
            injury_description = input("Describe your pain/injury: ").strip()
            
            print("\n🤖 Coach: ")
            message = f"User reports: {injury_description}"
            
            response = await injury_runner.run_debug(message)
            
            # Extract text from response
            if hasattr(response, 'text'):
                print(response.text)
            elif isinstance(response, list) and len(response) > 0:
                for event in response:
                    if hasattr(event, 'text') and event.text:
                        print(event.text)
            else:
                print("No response received")
        
        elif choice == "6":
            # Update profile
            print("\n⚙️ Updating profile...")
            profile = setup_profile()
            profile.email = profile.email  # Keep same email
            print("\n✅ Profile updated!")
        
        elif choice == "7":
            # Exit
            print(f"\n👋 Goodbye, {profile.name}! Keep training!")
            print("\n" + "="*60)
            print("Thanks for using Marathon Training Agent!")
            print("="*60 + "\n")
            break
        
        else:
            print("Invalid choice. Please enter 1-7")


if __name__ == "__main__":
    asyncio.run(main())