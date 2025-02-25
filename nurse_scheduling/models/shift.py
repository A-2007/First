# models/shift.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now you can import from the data_loader module
from data_handling.data_loader import fetch_shifts  # ✅ Use data_loader instead of direct DB access

class Shift:
    def __init__(self, shift_id, date, shift_type, assigned_nurse=None):
        """
        Initialize a Shift object.
        :param shift_id: The unique ID of the shift.
        :param date: The date of the shift (format: "YYYY-MM-DD").
        :param shift_type: The type of shift (e.g., "Morning", "Afternoon", "Night").
        :param assigned_nurse: The ID of the nurse assigned to the shift (default: None).
        """
        self.shift_id = shift_id
        self.date = date
        self.shift_type = shift_type
        self.assigned_nurse = assigned_nurse  # Can be None if not assigned

    @staticmethod
    def fetch_all_shifts():
        """
        Fetch all shifts using the data loader.
        :return: A list of Shift objects.
        """
        shifts_data = fetch_shifts()  # ✅ Load from data_loader.py
        return [Shift(**shift) for shift in shifts_data]  # ✅ Convert dicts to Shift objects

    def __repr__(self):
        """
        Return a string representation of the Shift object.
        """
        return f"Shift(shift_id={self.shift_id}, date={self.date}, shift_type={self.shift_type}, assigned_nurse={self.assigned_nurse})"

# ✅ Debugging: Test loading shifts
if __name__ == "__main__":
    shifts = Shift.fetch_all_shifts()
    for shift in shifts[:5]:  # Print first 5 shifts
        print(vars(shift))  # This will print the attributes of the shift objects