"""
Interactive profile setup
Collects user information through terminal prompts
"""

from sessions.profile_manager import UserProfile, save_profile
from datetime import datetime


def setup_profile() -> UserProfile:
    """
    Interactively collect user information.
    Returns a completed UserProfile object.
    """
    print("\n" + "="*50)
    print("🏃 MARATHON TRAINING AGENT - PROFILE SETUP")
    print("="*50)
    print("\nLet's set up your training profile.\n")
    
    profile = UserProfile()
    
    # Basic Information
    print("--- Basic Information ---")
    profile.name = input("What's your name? ").strip()
    

    # Email (unique identifier)
    while True:
        email = input("What's your email? ").strip()
        if '@' in email and '.' in email:
            profile.email = email
        break
        print("Please enter a valid email address")
        
    # Age with validation
    while True:
        try:
            age_input = input("What's your age? ").strip()
            profile.age = int(age_input)
            if profile.age < 10 or profile.age > 100:
                print("Please enter a valid age (10-100)")
                continue
            break
        except ValueError:
            print("Please enter a number")
    
    # Weight (optional)
    weight_input = input("What's your current weight in lbs? (press Enter to skip) ").strip()
    if weight_input:
        try:
            profile.weight = float(weight_input)
        except ValueError:
            print("Invalid weight, skipping...")
    
    # Goal Distance
    print("\n--- Training Goal ---")
    print("What's your goal race distance?")
    distances = {
        "1": "5K",
        "2": "10K",
        "3": "10 Mile",
        "4": "Half Marathon",
        "5": "Marathon"
    }
    
    for key, value in distances.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("\nEnter choice (1-5): ").strip()
        if choice in distances:
            profile.goal_distance = distances[choice]
            break
        print("Invalid choice. Please enter 1-5")
    
    # Ability Level
    print("\n--- Running Experience ---")
    print("How would you rate your running ability?")
    abilities = {
        "1": ("beginner", "0-6 months running"),
        "2": ("intermediate", "6-24 months running"),
        "3": ("advanced", "2-5 years running"),
        "4": ("elite", "5+ years, competitive")
    }
    
    for key, (level, desc) in abilities.items():
        print(f"  {key}. {level.title()} - {desc}")
    
    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        if choice in abilities:
            profile.ability_level = abilities[choice][0]
            break
        print("Invalid choice. Please enter 1-4")
    
    # Current Weekly Mileage
    print("\n--- Current Training ---")
    while True:
        try:
            mileage = input("What's your average weekly mileage (miles)? ").strip()
            profile.current_weekly_mileage = float(mileage)
            if profile.current_weekly_mileage < 0:
                print("Mileage cannot be negative")
                continue
            break
        except ValueError:
            print("Please enter a number")
    
    # Goal Race Date
    print("\n--- Race Schedule ---")
    while True:
        date_str = input("When is your goal race? (YYYY-MM-DD, e.g. 2025-08-15) ").strip()
        try:
            profile.goal_race_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Check if date is in the future
            if profile.goal_race_date < datetime.now():
                print("Goal race should be in the future!")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
    
    # Milestone Race (Optional)
    print("\n--- Milestone Race (Optional) ---")
    print("A milestone race helps build fitness for your main goal.")
    has_milestone = input("Do you have a milestone race planned? (yes/no) ").strip().lower()
    
    if has_milestone in ['yes', 'y']:
        profile.has_milestone = True
        
        # Milestone date
        while True:
            date_str = input("When is your milestone race? (YYYY-MM-DD) ").strip()
            try:
                profile.milestone_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                # Validate milestone is before goal race
                if profile.milestone_date >= profile.goal_race_date:
                    print("Milestone race must be before goal race!")
                    continue
                
                # Check if date is in the future
                if profile.milestone_date < datetime.now():
                    print("Milestone race should be in the future!")
                    continue
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        # Milestone distance
        while True:
            try:
                dist = input("What distance is the milestone race (in miles)? ").strip()
                profile.milestone_distance = float(dist)
                
                if profile.milestone_distance <= 0:
                    print("Distance must be positive")
                    continue
                break
            except ValueError:
                print("Please enter a number")
    
    # Summary
    print("\n" + "="*50)
    print("PROFILE SUMMARY")
    print("="*50)
    print(profile)
    
 # Confirm or Edit
    while True:
        confirm = input("\nIs this information correct? (yes/no/edit) ").strip().lower()
        
        if confirm in ['yes', 'y']:
            print("\n✅ Profile setup complete!")
            save_profile(profile)  # ← Add this line
            return profile
        
        elif confirm in ['edit', 'e']:
            # Show edit menu
            print("\n" + "="*50)
            print("EDIT PROFILE")
            print("="*50)
            print("What would you like to edit?")
            print("  1. Name")
            print("  2. Age")
            print("  3. Weight")
            print("  4. Goal distance")
            print("  5. Ability level")
            print("  6. Weekly mileage")
            print("  7. Goal race date")
            print("  8. Milestone race")
            print("  9. Start over completely")
            print("  0. Cancel (back to summary)")
            
            edit_choice = input("\nEnter number (0-9): ").strip()
            
            if edit_choice == "1":
                profile.name = input("New name: ").strip()
            
            elif edit_choice == "2":
                while True:
                    try:
                        profile.age = int(input("New age: ").strip())
                        break
                    except ValueError:
                        print("Please enter a number")
            
            elif edit_choice == "3":
                weight_input = input("New weight (lbs): ").strip()
                try:
                    profile.weight = float(weight_input) if weight_input else None
                except ValueError:
                    print("Invalid weight")
            
            elif edit_choice == "4":
                print("\nGoal distance:")
                distances = {
                    "1": "5K", "2": "10K", "3": "10 Mile",
                    "4": "Half Marathon", "5": "Marathon"
                }
                for key, value in distances.items():
                    print(f"  {key}. {value}")
                choice = input("Enter choice (1-5): ").strip()
                if choice in distances:
                    profile.goal_distance = distances[choice]
            
            elif edit_choice == "5":
                print("\nAbility level:")
                abilities = {
                    "1": "beginner", "2": "intermediate",
                    "3": "advanced", "4": "elite"
                }
                for key, value in abilities.items():
                    print(f"  {key}. {value.title()}")
                choice = input("Enter choice (1-4): ").strip()
                if choice in abilities:
                    profile.ability_level = abilities[choice]
            
            elif edit_choice == "6":
                while True:
                    try:
                        mileage = float(input("New weekly mileage: ").strip())
                        if mileage >= 0:
                            profile.current_weekly_mileage = mileage
                            break
                        print("Mileage cannot be negative")
                    except ValueError:
                        print("Please enter a number")
            
            elif edit_choice == "7":
                while True:
                    date_str = input("New goal race date (YYYY-MM-DD): ").strip()
                    try:
                        profile.goal_race_date = datetime.strptime(date_str, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date format")
            
            elif edit_choice == "8":
                has_milestone = input("Have milestone race? (yes/no): ").strip().lower()
                if has_milestone in ['yes', 'y']:
                    profile.has_milestone = True
                    while True:
                        date_str = input("Milestone date (YYYY-MM-DD): ").strip()
                        try:
                            profile.milestone_date = datetime.strptime(date_str, "%Y-%m-%d")
                            break
                        except ValueError:
                            print("Invalid date format")
                    while True:
                        try:
                            profile.milestone_distance = float(input("Milestone distance (miles): ").strip())
                            break
                        except ValueError:
                            print("Please enter a number")
                else:
                    profile.has_milestone = False
                    profile.milestone_date = None
                    profile.milestone_distance = None
            
            elif edit_choice == "9":
                print("\nStarting over...")
                return setup_profile()
            
            elif edit_choice == "0":
                print("\nReturning to summary...")
            
            else:
                print("Invalid choice")
            
            # Show updated summary after edit
            print("\n" + "="*50)
            print("UPDATED PROFILE SUMMARY")
            print("="*50)
            print(profile)
        
        elif confirm in ['no', 'n']:
            print("\nLet's start over...")
            return setup_profile()
        
        else:
            print("Please enter 'yes', 'no', or 'edit'")
    
    print("\n✅ Profile setup complete!")
    return profile


# Test if running directly
if __name__ == "__main__":
    profile = setup_profile()
    print("\n--- Profile Dictionary ---")
    print(profile.to_dict())