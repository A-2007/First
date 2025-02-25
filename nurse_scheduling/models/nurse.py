# models/nurse.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now you can import from the data_loader module
from data_handling.data_loader import fetch_nurses  # ✅ Use the data loader instead of direct DB access

class Nurse:
    def __init__(self, nurse_id, name, age, availability, preferred_shifts):
        self.nurse_id = nurse_id
        self.name = name
        self.age = age
        self.availability = availability
        self.preferred_shifts = preferred_shifts

    def is_available(self, date, shift_type):
        """
        Check if the nurse is available for the given date and shift type.
        :param date: The date of the shift (format: "YYYY-MM-DD").
        :param shift_type: The type of shift (e.g., "Morning", "Afternoon", "Night").
        :return: True if the nurse is available, False otherwise.
        """
        # Parse the availability string to check if the nurse is available on the given date
        available_days = self.availability.split(", ")
        shift_day = date.strftime("%a")  # Extract day of the week (e.g., "Mon", "Tue")

        # Check if the nurse is available on the given day and prefers the shift type
        if shift_day in available_days and shift_type in self.preferred_shifts:
            return True
        return False

    @staticmethod
    def fetch_all_nurses():
        """Fetch all nurses using the data loader."""
        nurses_data = fetch_nurses()  # ✅ Load from data_loader.py
        return [Nurse(**nurse) for nurse in nurses_data]  # ✅ Convert dicts to Nurse objects

    @staticmethod
    def get_nurse_by_id(nurse_id):
        """Fetch a specific nurse by their ID."""
        nurses = Nurse.fetch_all_nurses()  # Load all nurses
        for nurse in nurses:
            if nurse.nurse_id == nurse_id:
                return nurse
        return None  # Return None if not found

# ✅ Debugging: Test loading nurses
if __name__ == "__main__":
    nurses = Nurse.fetch_all_nurses()
    for nurse in nurses[:5]:  # Print first 5 nurses
        print(vars(nurse))  # This will print the attributes of the nurse objects