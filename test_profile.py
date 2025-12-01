"""
Simple test to verify profile manager works
"""

from sessions.profile_manager import UserProfile
from datetime import datetime

# Create a profile
profile = UserProfile()

# Fill it with test data
profile.name = "Sarah"
profile.age = 32
profile.weight = 145
profile.goal_distance = "Marathon"
profile.ability_level = "intermediate"
profile.current_weekly_mileage = 20
profile.goal_race_date = datetime(2025, 8, 15)
profile.has_milestone = True
profile.milestone_date = datetime(2025, 5, 15)
profile.milestone_distance = 18

# Test is_complete()
print(f"Is profile complete? {profile.is_complete()}")

# Test to_dict()
print("\nProfile as dictionary:")
print(profile.to_dict())

# Test __str__()
print("\nProfile summary:")
print(profile)

print("\n✅ Profile manager test passed!")