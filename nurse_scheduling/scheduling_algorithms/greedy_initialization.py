# scheduling_algorithms/greedy_initialization.py

import random
import sys
import os

# Add the path to the 'data_handling' folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_handling')))

# Now you can import fetch_nurses and fetch_shifts
from data_loader import fetch_nurses, fetch_shifts
from models.shift import Shift  # Import the Shift class

# Fetch the data from the database
nurses = fetch_nurses()  # List of nurses from the database
shifts = fetch_shifts()  # List of shifts from the database

def get_available_shifts_for_day(nurse, day):
    """
    Returns a list of shift types (morning, afternoon, night) available to the nurse for the given day.
    If the nurse is not available on the day, return an empty list.
    """
    available_shifts = []
    availability = nurse['availability']

    # Parse the availability string to extract available days and shifts
    availability_slots = availability.split(", ")
    for slot in availability_slots:
        if day in slot:
            # Extract the shift types that the nurse prefers for that day
            if 'Morning' in nurse['preferred_shifts']:
                available_shifts.append('Morning')
            if 'Afternoon' in nurse['preferred_shifts']:
                available_shifts.append('Afternoon')
            if 'Night' in nurse['preferred_shifts']:
                available_shifts.append('Night')
    return available_shifts

def greedy_initialization(nurses, shifts):
    """
    Performs a greedy initialization of the nurse scheduling by assigning shifts to nurses
    based on their availability and preferences.
    """
    # Initialize the schedule with empty lists for each nurse
    schedule = {nurse["nurse_id"]: [] for nurse in nurses}

    # Sort nurses by the number of preferred shifts (more specific preferences are prioritized)
    nurses_sorted = sorted(nurses, key=lambda nurse: len(nurse['preferred_shifts']), reverse=True)

    # Assign shifts to nurses based on their availability and preferences
    for nurse in nurses_sorted:
        for shift_data in shifts:
            # Get the available shift types for the nurse on this shift date
            available_shifts = get_available_shifts_for_day(nurse, shift_data["date"])

            # Debugging: Print nurse availability and shift data
            print(f"Nurse {nurse['nurse_id']} - Available Shifts on {shift_data['date']}: {available_shifts}")
            print(f"Shift Data: {shift_data}")

            # If the nurse is available and prefers this shift type, assign them the shift
            if shift_data["shift_type"] in available_shifts:
                # Create a Shift object
                shift = Shift(
                    shift_id=shift_data["shift_id"],
                    date=shift_data["date"],
                    shift_type=shift_data["shift_type"],
                    assigned_nurse=nurse["nurse_id"]
                )
                schedule[nurse["nurse_id"]].append(shift)
                print(f"Assigned Shift {shift_data['shift_id']} to Nurse {nurse['nurse_id']}")

    # Fill remaining shifts with any available nurse (if not assigned already)
    for nurse in nurses:
        for shift_data in shifts:
            # Check if the shift is already assigned
            shift_assigned = any(shift_data["shift_id"] == shift.shift_id for shift in schedule[nurse["nurse_id"]])
            if not shift_assigned and shift_data["date"] in nurse["availability"]:
                # Create a Shift object
                shift = Shift(
                    shift_id=shift_data["shift_id"],
                    date=shift_data["date"],
                    shift_type=shift_data["shift_type"],
                    assigned_nurse=nurse["nurse_id"]
                )
                schedule[nurse["nurse_id"]].append(shift)
                print(f"Assigned Shift {shift_data['shift_id']} to Nurse {nurse['nurse_id']} (Fallback)")

    return schedule

# Print the generated schedule for review
def print_schedule(schedule):
    """
    Prints the nurse schedule in a readable format.
    :param schedule: A dictionary containing the nurse schedule (nurse_id -> [Shift objects])
    """
    for nurse_id, shifts in schedule.items():
        nurse_name = next(nurse['name'] for nurse in nurses if nurse['nurse_id'] == nurse_id)
        print(f"{nurse_name} - Assigned Shifts:")
        for shift in shifts:
            print(f"  Shift ID: {shift.shift_id}, Date: {shift.date}, Type: {shift.shift_type}")

if __name__ == "__main__":
    # Generate the schedule using Greedy Initialization
    schedule = greedy_initialization(nurses, shifts)

    # Print the schedule
    print_schedule(schedule)