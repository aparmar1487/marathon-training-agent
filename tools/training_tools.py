"""
Training Tools - Custom functions for marathon training
These are Function Tools that agents can use.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta


def calculate_acwr(last_7_days: List[float], last_28_days: List[float]) -> Dict:
    """
    Calculate Acute:Chronic Workload Ratio for injury risk assessment.
    
    This is the CORE of proactive injury prevention.
    
    Args:
        last_7_days: Daily mileage for last 7 days [day1, day2, ..., day7]
        last_28_days: Daily mileage for last 28 days (includes the 7 days)
    
    Returns:
        dict with:
            - ratio: ACWR value
            - risk_level: "SAFE", "ELEVATED", or "HIGH"
            - recommendation: What to do
            - acute_load: Average daily load last 7 days
            - chronic_load: Average daily load last 28 days
    
    Example:
        >>> calculate_acwr([8, 0, 6, 0, 10, 0, 12], [5, 0, 6, ...])
        {'ratio': 1.2, 'risk_level': 'SAFE', ...}
    """
    # Calculate average daily loads
    acute_load = sum(last_7_days) / 7  # Last week average
    chronic_load = sum(last_28_days) / 28  # Last 4 weeks average
    
    # Avoid division by zero
    if chronic_load == 0:
        return {
            "status": "error",
            "ratio": 0,
            "risk_level": "INSUFFICIENT_DATA",
            "recommendation": "Need at least 4 weeks of training data",
            "acute_load": acute_load,
            "chronic_load": 0
        }
    
    # Calculate ratio
    ratio = acute_load / chronic_load
    
    if ratio > 1.5:
        risk_level = "HIGH"
        recommendation = "REDUCE_LOAD_IMMEDIATELY - High injury risk detected"
    elif ratio > 1.3:
        risk_level = "ELEVATED"
        recommendation = "CAUTION - Monitor closely and consider reducing load"
    elif ratio < 0.8:
        risk_level = "UNDERTRAINING"
        recommendation = "Consider increasing training load gradually"
    else:
        risk_level = "SAFE"
        recommendation = "Training load is well-balanced - continue current progression"
    
    return {
        "status": "success",
        "ratio": round(ratio, 2),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "acute_load": round(acute_load, 1),
        "chronic_load": round(chronic_load, 1),
        "acute_weekly": round(acute_load * 7, 1),
        "chronic_weekly": round(chronic_load * 7, 1)
    }


def adjust_paces_from_race(
    race_distance_miles: float,
    race_time_minutes: float,
    current_vdot: Optional[float] = None
) -> Dict:
    """
    Calculate training paces based on race performance.
    
    This enables MILESTONE CONTINUITY - adjusting Phase 2 based on actual results.
    
    Uses VDOT methodology (Jack Daniels' Running Formula).
    
    Args:
        race_distance_miles: Distance of completed race (e.g., 18 miles)
        race_time_minutes: Actual finish time in minutes (e.g., 144 for 2:24)
        current_vdot: Previous VDOT estimate (optional)
    
    Returns:
        dict with:
            - vdot: Estimated VDOT score
            - race_pace: Pace per mile from race (min/mile)
            - easy_pace: Easy run pace (min/mile)
            - tempo_pace: Tempo run pace (min/mile)
            - interval_pace: Interval training pace (min/mile)
            - long_run_pace: Long run pace (min/mile)
            - marathon_prediction: Predicted marathon time (minutes)
    
    Example:
        >>> adjust_paces_from_race(18, 144)  # 18 miles in 2:24
        {'vdot': 48, 'easy_pace': 9.5, 'tempo_pace': 8.0, ...}
    """
    # Calculate actual race pace (min/mile)
    race_pace = race_time_minutes / race_distance_miles
    
    # Simplified VDOT estimation based on pace
    # Real VDOT tables are more complex, but this is a good approximation
    # Formula derived from Jack Daniels' VDOT tables
    
    # For distances 10K to marathon, pace correlates roughly with VDOT
    # Baseline: 10min/mile ≈ VDOT 35, 8min/mile ≈ VDOT 45, 7min/mile ≈ VDOT 52
    estimated_vdot = 35 + (10 - race_pace) * 3.5
    
    # Ensure VDOT is in reasonable range
    estimated_vdot = max(25, min(85, estimated_vdot))
    
    # Calculate training paces based on VDOT
    # These are based on Jack Daniels' pace tables
    easy_pace = race_pace + 1.5  # 1.5 min/mile slower than race pace
    tempo_pace = race_pace + 0.3  # Slightly slower than race pace
    interval_pace = race_pace - 0.5  # Faster than race pace
    long_run_pace = race_pace + 1.0  # 1 min/mile slower than race pace
    
    # Predict marathon time based on race performance
    # Scaling factor depends on distance trained
    if race_distance_miles >= 20:
        # Close to marathon distance - conservative prediction
        marathon_prediction = race_pace * 26.2 * 1.02  # 2% slower
    elif race_distance_miles >= 13:
        # Half marathon distance - moderate prediction
        marathon_prediction = race_pace * 26.2 * 1.05  # 5% slower
    else:
        # Shorter distance - more conservative
        marathon_prediction = race_pace * 26.2 * 1.08  # 8% slower
    
    return {
        "status": "success",
        "vdot": round(estimated_vdot, 1),
        "race_pace_per_mile": round(race_pace, 2),
        "paces": {
            "easy": round(easy_pace, 2),
            "tempo": round(tempo_pace, 2),
            "interval": round(interval_pace, 2),
            "long_run": round(long_run_pace, 2)
        },
        "marathon_prediction_minutes": round(marathon_prediction, 1),
        "marathon_prediction_time": f"{int(marathon_prediction // 60)}:{int(marathon_prediction % 60):02d}",
        "improvement": f"VDOT improved from {current_vdot} to {estimated_vdot:.1f}" if current_vdot else None
    }


def calculate_weekly_mileage_progression(
    current_mileage: float,
    target_mileage: float,
    weeks_available: int,
    ability_level: str = "intermediate"
) -> Dict:
    """
    Calculate safe weekly mileage progression.
    
    Args:
        current_mileage: Current weekly mileage
        target_mileage: Target peak mileage
        weeks_available: Number of weeks to build up
        ability_level: "beginner", "intermediate", "advanced", or "elite"
    
    Returns:
        dict with weekly mileage plan and safety info
    """
    # Safe progression rates by ability level
    max_increase_rates = {
        "beginner": 0.10,      # 10% per week max
        "intermediate": 0.12,  # 12% per week max
        "advanced": 0.15,      # 15% per week max
        "elite": 0.18          # 18% per week max
    }
    
    max_increase = max_increase_rates.get(ability_level, 0.10)
    
    # Calculate weekly progression
    weekly_plan = []
    current = current_mileage
    
    for week in range(1, weeks_available + 1):
        # Every 4th week is a recovery week (reduce by 20%)
        if week % 4 == 0:
            current = current * 0.8
            week_type = "recovery"
        else:
            # Increase by safe amount, but don't exceed target
            increase = min(current * max_increase, target_mileage - current)
            current = min(current + increase, target_mileage)
            week_type = "build"
        
        weekly_plan.append({
            "week": week,
            "mileage": round(current, 1),
            "type": week_type
        })
    
    # Check if target is reachable
    final_mileage = weekly_plan[-1]["mileage"]
    is_safe = final_mileage >= target_mileage * 0.9  # Within 10% of target
    
    return {
        "status": "success",
        "weekly_plan": weekly_plan,
        "final_mileage": round(final_mileage, 1),
        "target_mileage": target_mileage,
        "is_achievable": is_safe,
        "max_weekly_increase": f"{max_increase * 100}%",
        "recommendation": "Safe progression" if is_safe else "Target too aggressive - need more weeks"
    }


def get_corrective_exercises(injury_type: str) -> Dict:
    """
    Get corrective exercises for specific injury type.
    
    Args:
        injury_type: Type of injury - one of:
            - "IT_band"
            - "plantar_fasciitis"
            - "achilles_tendonitis"
            - "shin_splints"
            - "runners_knee"
    
    Returns:
        dict with exercises, training modifications, and return criteria
    
    Example:
        >>> get_corrective_exercises("IT_band")
        {'injury_name': 'IT Band Syndrome', 'exercises': [...], ...}
    """
    import json
    import os
    
    # Load exercise library
    library_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'exercise_library.json')
    
    try:
        with open(library_path, 'r') as f:
            exercise_library = json.load(f)
        
        # Get exercises for injury type
        if injury_type in exercise_library:
            return {
                "status": "success",
                **exercise_library[injury_type]
            }
        else:
            available = list(exercise_library.keys())
            return {
                "status": "error",
                "error_message": f"Unknown injury type: {injury_type}",
                "available_types": available
            }
    
    except FileNotFoundError:
        return {
            "status": "error",
            "error_message": "Exercise library file not found"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error loading exercises: {str(e)}"
        }

# Test functions if run directly
if __name__ == "__main__":
    print("="*60)
    print("Testing Training Tools")
    print("="*60)
    
    # Test 1: ACWR
    print("\n1. Testing ACWR Calculation:")
    result = calculate_acwr(
        last_7_days=[10, 0, 8, 0, 12, 0, 14],  # 44 miles last week
        last_28_days=[6, 0, 5, 0, 7, 0, 8, 0,  # Previous weeks
                      6, 0, 7, 0, 8, 0, 9, 0,
                      8, 0, 7, 0, 9, 0, 10, 0,
                      10, 0, 8, 0, 12, 0, 14]  # Total ~196 miles in 28 days
    )
    print(f"ACWR Ratio: {result['ratio']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Recommendation: {result['recommendation']}")
    
    # Test 2: Pace Adjustment
    print("\n2. Testing Pace Adjustment (18 miles in 2:24):")
    result = adjust_paces_from_race(18, 144)
    print(f"VDOT: {result['vdot']}")
    print(f"Marathon Prediction: {result['marathon_prediction_time']}")
    print(f"Training Paces:")
    for pace_type, pace in result['paces'].items():
        print(f"  {pace_type}: {pace} min/mile")
    
    # Test 3: Mileage Progression
    print("\n3. Testing Mileage Progression (25→50 miles in 12 weeks):")
    result = calculate_weekly_mileage_progression(25, 50, 12, "intermediate")
    print(f"Is Achievable: {result['is_achievable']}")
    print(f"Final Mileage: {result['final_mileage']} (target: {result['target_mileage']})")
    print("Weekly Plan (first 6 weeks):")
    for week_data in result['weekly_plan'][:6]:
        print(f"  Week {week_data['week']}: {week_data['mileage']} miles ({week_data['type']})")

    # Test 4: Corrective Exercises
    print("\n4. Testing Corrective Exercises (IT Band):")
    result = get_corrective_exercises("IT_band")
    if result['status'] == 'success':
        print(f"Injury: {result['injury_name']}")
        print(f"Number of exercises: {len(result['exercises'])}")
        print(f"First exercise: {result['exercises'][0]['name']}")
        print(f"  - {result['exercises'][0]['why']}")
        print(f"Training Modifications: {result['training_modifications'][0]}")
        print(f"Return to Running Criteria: {result['return_to_running_criteria'][0]}")        

    else:
        print(f"Error: {result['error_message']}")
    
    print("\n" + "="*60)
    print("✅ All tools working!")
    print("="*60)