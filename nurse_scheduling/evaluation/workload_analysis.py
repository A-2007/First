# evaluation/workload_analysis.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now you can import from the constraints module
from constraints.constraints import SHIFT_HOURS

from collections import defaultdict

def calculate_nurse_workload(schedule):
    """
    Returns the total assigned hours for all nurses in the schedule.
    """
    total_workload = 0

    # Loop through all shifts in the schedule to calculate total workload
    for shift in schedule.shifts:
        if shift.assigned_nurse:  # Ensure the shift is assigned to a nurse
            total_workload += SHIFT_HOURS.get(shift.shift_type, 0)  # Use SHIFT_HOURS to get shift duration

    return total_workload

def check_overtime(schedule, max_hours_per_week=48):
    """
    Checks if any nurse exceeds the allowed working hours.
    Returns a list of nurses who are overworked.
    """
    overworked_nurses = []

    # Loop through all nurses and check their individual workload
    for nurse in schedule.nurses:
        workload = calculate_nurse_workload(nurse, schedule)  # Calculate the nurse's workload
        if workload > max_hours_per_week:
            overworked_nurses.append(nurse)  # Add the nurse to the list if overworked

    return overworked_nurses

def shift_distribution(schedule):
    """
    Checks whether shifts are fairly distributed among nurses.
    Returns a dictionary of shift counts per nurse.
    """
    shift_counts = defaultdict(int)

    # Loop through all shifts in the schedule
    for shift in schedule.shifts:
        if shift.assigned_nurse:  # If the shift has an assigned nurse
            shift_counts[shift.assigned_nurse] += 1  # Increment the shift count for the nurse

    return shift_counts