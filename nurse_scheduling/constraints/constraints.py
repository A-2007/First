# constraints/constraints.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now you can import from the models and data_handling modules
from models.nurse import Nurse
from models.shift import Shift
from models.schedule import Schedule
from datetime import datetime, timedelta

# NHS Policies (These can be adjusted based on real-world rules)
MAX_HOURS_PER_WEEK = 48  # NHS Working Time Directive
MAX_CONSECUTIVE_SHIFTS = 6  # Prevent burnout
MIN_HOURS_BETWEEN_SHIFTS = 11  # Minimum rest period between shifts
SHIFT_HOURS = {"Morning": 8, "Afternoon": 8, "Night": 10}  # Typical shift durations

def is_nurse_available(nurse: Nurse, shift: Shift) -> bool:
    """Check if a nurse is available for the given shift."""
    available_days = nurse.availability.split(", ")
    shift_day = datetime.strptime(shift.date, "%Y-%m-%d").strftime("%a")  # Extract day of the week
    return any(shift_day in slot for slot in available_days)

def check_max_hours(nurse: Nurse, schedule: Schedule) -> bool:
    """
    Ensure the nurse does not exceed the maximum working hours per week.
    """
    weekly_hours = {}

    # Sort shifts by date before calculating hours
    assigned_shifts = sorted(schedule.assignments.get(nurse.nurse_id, []), key=lambda s: s.date)

    for shift in assigned_shifts:
        shift_week = datetime.strptime(shift.date, "%Y-%m-%d").isocalendar()[1]  # Get ISO week number
        weekly_hours.setdefault(shift_week, 0)
        weekly_hours[shift_week] += SHIFT_HOURS.get(shift.shift_type, 0)  # Default to 0 if shift type is invalid

    return all(hours <= MAX_HOURS_PER_WEEK for hours in weekly_hours.values())

def check_consecutive_shifts(nurse: Nurse, schedule: Schedule) -> bool:
    """
    Ensure nurses do not work more than MAX_CONSECUTIVE_SHIFTS days in a row.
    """
    assigned_dates = sorted([datetime.strptime(shift.date, "%Y-%m-%d") for shift in schedule.assignments.get(nurse.nurse_id, [])])
    consecutive_count = 1

    for i in range(1, len(assigned_dates)):
        if (assigned_dates[i] - assigned_dates[i - 1]).days == 1:
            consecutive_count += 1
            if consecutive_count > MAX_CONSECUTIVE_SHIFTS:
                return False
        else:
            consecutive_count = 1  # Reset counter if a day is skipped

    return True

def check_rest_period(nurse: Nurse, schedule: Schedule) -> bool:
    """
    Ensure nurses have at least MIN_HOURS_BETWEEN_SHIFTS rest.
    """
    assigned_shifts = sorted(schedule.assignments.get(nurse.nurse_id, []), key=lambda s: s.date)

    for i in range(1, len(assigned_shifts)):
        prev_shift = assigned_shifts[i - 1]
        curr_shift = assigned_shifts[i]

        prev_end_time = datetime.strptime(prev_shift.date, "%Y-%m-%d") + timedelta(hours=SHIFT_HOURS.get(prev_shift.shift_type, 0))
        curr_start_time = datetime.strptime(curr_shift.date, "%Y-%m-%d")

        if (curr_start_time - prev_end_time).total_seconds() / 3600 < MIN_HOURS_BETWEEN_SHIFTS:
            return False  # Rest period violation

    return True

def check_shift_coverage(schedule: Schedule) -> bool:
    """
    Ensure all shifts have at least one assigned nurse.
    """
    assigned_shifts = {shift for shifts in schedule.assignments.values() for shift in shifts}
    return schedule.all_shifts.issubset(assigned_shifts)

def check_nurse_preferences(nurse, shift):
    """
    Check if a nurse's preferences match the shift type.
    """
    # Ensure shift is a Shift object
    if isinstance(shift, Shift):
        return shift.shift_type in nurse.preferred_shifts
    else:
        print(f"Expected Shift object, but got {type(shift)}")
        return False

def validate_schedule(schedule: Schedule) -> bool:
    """
    Run all hard constraint checks on the schedule.
    """
    for nurse in schedule.nurses:
        if (not check_max_hours(nurse, schedule) or
            not check_consecutive_shifts(nurse, schedule) or
            not check_rest_period(nurse, schedule) or
            not check_shift_coverage(schedule)):
            return False
    return True