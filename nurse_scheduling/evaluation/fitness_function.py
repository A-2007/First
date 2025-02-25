# evaluation/fitness_function.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Corrected import statement
from constraints.constraints import SHIFT_HOURS, check_max_hours, check_consecutive_shifts, check_rest_period, check_shift_coverage, check_nurse_preferences
from evaluation.workload_analysis import calculate_nurse_workload
from models.schedule import Schedule
from models.nurse import Nurse

def evaluate_schedule(schedule: Schedule) -> float:
    """
    Calculates the fitness score of a given schedule.
    Higher score means a better schedule based on fairness, efficiency, and constraint compliance.
    """
    total_score = 0

    # Check hard constraints
    for nurse in schedule.nurses:
        if not check_max_hours(nurse, schedule):
            total_score -= 50  # Adjusted penalty for max hours violation
        if not check_consecutive_shifts(nurse, schedule):
            total_score -= 50  # Adjusted penalty for consecutive shifts violation
        if not check_rest_period(nurse, schedule):
            total_score -= 50  # Adjusted penalty for rest period violation

    # Check shift coverage
    if not check_shift_coverage(schedule):
        total_score -= 100  # Adjusted penalty for shift coverage violation

    # Reward for nurse preferences
    for nurse in schedule.nurses:
        for shift in schedule.assignments.get(nurse.nurse_id, []):
            if check_nurse_preferences(nurse, shift):
                total_score += 10  # Reward for matching preferences

    # Reward for fair workload distribution
    workload_score = calculate_nurse_workload(schedule)
    total_score += workload_score

    return total_score