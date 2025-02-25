# models/schedule.py

from .shift import Shift
from .nurse import Nurse

class Schedule:
    def __init__(self):
        # Initialize nurses and shifts by fetching them
        self.nurses = Nurse.fetch_all_nurses()
        self.shifts = Shift.fetch_all_shifts()
        self.all_shifts = set(self.shifts)  # Initialize all_shifts as a set of all shifts
        self.assignments = {}  # This will hold shift assignments by nurse_id

    def __repr__(self):
        return f"Schedule with {len(self.nurses)} nurses and {len(self.shifts)} shifts"

    def get_unassigned_shifts(self):
        """Returns a list of unassigned shifts."""
        return [shift for shift in self.shifts if shift.assigned_nurse is None]

    def assign_nurse_to_shift(self, shift, nurse):
        """
        Assigns a nurse to a shift if they are available.
        :param shift: The shift to assign.
        :param nurse: The nurse to assign to the shift.
        :return: True if the assignment was successful, False otherwise.
        """
        if nurse.is_available(shift.date, shift.shift_type):
            shift.assigned_nurse = nurse.nurse_id

            # Ensure assignments is a dictionary that stores shifts by nurse_id
            if nurse.nurse_id not in self.assignments:
                self.assignments[nurse.nurse_id] = []

            # Add the shift (which is a Shift object) to the nurse's assignments
            self.assignments[nurse.nurse_id].append(shift)
            return True
        return False

    def generate_initial_schedule(self):
        """
        Tries to assign nurses to shifts based on availability and preferences.
        Ensures all shifts are covered and constraints are satisfied.
        """
        unassigned_shifts = self.get_unassigned_shifts()

        for shift in unassigned_shifts:
            for nurse in self.nurses:
                if self.assign_nurse_to_shift(shift, nurse):
                    break  # Move to the next shift once a nurse is assigned

        # Check if all shifts are assigned
        if len(self.get_unassigned_shifts()) > 0:
            print("Warning: Not all shifts were assigned.")

    def display_schedule(self):
        """Prints the full schedule in a readable format."""
        for shift in self.shifts:
            nurse_name = "Unassigned"
            if shift.assigned_nurse:
                nurse = next((n for n in self.nurses if n.nurse_id == shift.assigned_nurse), None)
                nurse_name = nurse.name if nurse else "Unassigned"
            print(f"Shift ID: {shift.shift_id}, Date: {shift.date}, Type: {shift.shift_type}, Assigned Nurse: {nurse_name}")

    def add_shift(self, shift):
        """Adds a shift to the schedule and updates all_shifts."""
        self.shifts.append(shift)
        self.all_shifts.add(shift)

    def remove_shift(self, shift):
        """Removes a shift from the schedule and updates all_shifts."""
        self.shifts.remove(shift)
        self.all_shifts.remove(shift)

# Example usage:
if __name__ == "__main__":
    schedule = Schedule()
    schedule.generate_initial_schedule()
    schedule.display_schedule()