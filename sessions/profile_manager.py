"""
User Profile Manager
Handles collecting and storing user information for personalized training plans.
"""

from datetime import datetime
from typing import Optional
import json
import os


class UserProfile:
    """Stores user information for training plan personalization."""
    
    def __init__(self):
        # Basic info
        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.age: Optional[int] = None
        self.weight: Optional[float] = None
        
        # Training info
        self.goal_distance: Optional[str] = None  # "5K", "10K", "Half Marathon", "Marathon"
        self.ability_level: Optional[str] = None  # "beginner", "intermediate", "advanced", "elite"
        self.current_weekly_mileage: Optional[float] = None
        self.goal_race_date: Optional[datetime] = None
        
        # Milestone race (optional)
        self.has_milestone: bool = False
        self.milestone_date: Optional[datetime] = None
        self.milestone_distance: Optional[float] = None
    
    def is_complete(self) -> bool:
        """Check if all required fields are filled."""
        required_fields = [
            self.name,
            self.email,
            self.age,
            self.goal_distance,
            self.ability_level,
            self.current_weekly_mileage,
            self.goal_race_date
        ]
        return all(field is not None for field in required_fields)
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary for saving/agent use."""
        return {
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "weight": self.weight,
            "goal_distance": self.goal_distance,
            "ability_level": self.ability_level,
            "current_weekly_mileage": self.current_weekly_mileage,
            "goal_race_date": self.goal_race_date.isoformat() if self.goal_race_date else None,
            "has_milestone": self.has_milestone,
            "milestone_date": self.milestone_date.isoformat() if self.milestone_date else None,
            "milestone_distance": self.milestone_distance
        }
    
    def __str__(self) -> str:
        """String representation for display."""
        summary = f"Profile for {self.name}:\n"
        summary += f"  Email: {self.email}\n"
        summary += f"  Age: {self.age}\n"
        summary += f"  Goal: {self.goal_distance}\n"
        summary += f"  Level: {self.ability_level}\n"
        summary += f"  Current mileage: {self.current_weekly_mileage} mpw\n"
        if self.has_milestone:
            summary += f"  Milestone: {self.milestone_distance} miles\n"
        return summary

def save_profile(profile: UserProfile, filename: str = "users.json") -> None:
    """Save profile to users file (adds or updates)."""
    
    # Load existing users
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            users = data.get('users', [])
    else:
        users = []
    
    # Convert profile to dict
    profile_dict = profile.to_dict()
    
    # Check if user exists (by email)
    user_exists = False
    for i, user in enumerate(users):
        if user.get('email') == profile.email:
            # Update existing user
            users[i] = profile_dict
            user_exists = True
            print(f"✅ Updated profile for {profile.email}")
            break
    
    # Add new user if doesn't exist
    if not user_exists:
        users.append(profile_dict)
        print(f"✅ Created new profile for {profile.email}")
    
    # Save back to file
    with open(filename, 'w') as f:
        json.dump({'users': users}, f, indent=2)


def load_profile(email: str, filename: str = "users.json") -> Optional[UserProfile]:
    """Load profile for specific email."""
    
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
        users = data.get('users', [])
    
    # Find user by email
    for user_data in users:
        if user_data.get('email') == email:
            profile = UserProfile()
            profile.name = user_data.get('name')
            profile.email = user_data.get('email')
            profile.age = user_data.get('age')
            profile.weight = user_data.get('weight')
            profile.goal_distance = user_data.get('goal_distance')
            profile.ability_level = user_data.get('ability_level')
            profile.current_weekly_mileage = user_data.get('current_weekly_mileage')
            profile.goal_race_date = datetime.fromisoformat(user_data.get('goal_race_date'))
            profile.has_milestone = user_data.get('has_milestone', False)
            milestone_date_str = user_data.get('milestone_date')
            if milestone_date_str:
                profile.milestone_date = datetime.fromisoformat(milestone_date_str)
            profile.milestone_distance = user_data.get('milestone_distance')
            print(f"✅ Profile loaded for {email}")
            return profile
    else:   
        print(f"❌ No profile found for {email}")
        return None


def list_all_users(filename: str = "users.json") -> list:
    """
    Get list of all registered users.
    
    Returns:
        List of strings with format "Name (email)"
    """
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            users = data.get('users', [])
        
        return [f"{user.get('name')} ({user.get('email')})" for user in users]
    except Exception as e:
        print(f"❌ Error reading users: {e}")
        return []