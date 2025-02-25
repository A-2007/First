# data_handling/database_setup.py

import sqlite3
from datetime import datetime, timedelta
import random

def setup_database():
    """
    Sets up the database by creating tables and inserting sample data.
    """
    # Create the database and connect
    conn = sqlite3.connect("nurse_schedule.db")
    cursor = conn.cursor()

    # Drop existing tables if they exist (for testing purposes)
    cursor.execute("DROP TABLE IF EXISTS nurses;")
    cursor.execute("DROP TABLE IF EXISTS shifts;")

    # Create Nurses table
    cursor.execute("""
    CREATE TABLE nurses (
        nurse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        availability TEXT NOT NULL,
        preferred_shifts TEXT NOT NULL
    );
    """)

    # Create Shifts table
    cursor.execute("""
    CREATE TABLE shifts (
        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        shift_type TEXT NOT NULL CHECK(shift_type IN ('Morning', 'Afternoon', 'Night')),
        assigned_nurse INTEGER,
        FOREIGN KEY (assigned_nurse) REFERENCES nurses(nurse_id)
    );
    """)

    # Sample nurse data (adjusted for schema)
    nurse_data = [
        ("Alice Johnson", 34, "Mon-Fri (Morning), Sat (Evening)", "Morning"),
        ("Bob Smith", 45, "Mon-Sun (Flexible)", "Night"),
        ("Claire Williams", 29, "Mon, Wed, Fri (Morning), Sun (Night)", "Morning"),
        ("David Brown", 52, "Tue, Thu, Sat (Evening), Sun (Morning)", "Evening"),
        ("Emily Davis", 27, "Mon-Wed (Afternoon), Fri (Morning)", "Afternoon"),
        ("Frank Miller", 38, "Mon, Tue, Thu (Night), Sat (Morning)", "Night"),
        ("Grace Taylor", 31, "Mon-Fri (Morning), Sat-Sun (Flexible)", "Morning"),
        ("Henry Wilson", 43, "Mon-Fri (Night), Sat (Afternoon)", "Night"),
        ("Isabella Moore", 26, "Mon-Wed (Morning), Thu-Sun (Flexible)", "Morning"),
        ("Jack Thompson", 49, "Mon-Fri (Evening), Sat (Morning)", "Evening"),
        ("Kelly Anderson", 35, "Tue, Thu, Sat (Afternoon), Sun (Morning)", "Afternoon"),
        ("Luke Harris", 41, "Mon-Fri (Morning), Sat-Sun (Flexible)", "Morning"),
        ("Maria Clark", 33, "Mon-Wed (Afternoon), Fri-Sun (Morning)", "Morning"),
        ("Nathan Lewis", 30, "Mon, Wed, Fri (Morning), Sun (Night)", "Morning"),
        ("Olivia Scott", 28, "Mon-Fri (Evening), Sat (Afternoon)", "Evening"),
        ("Peter Young", 54, "Mon-Wed (Night), Thu-Sun (Morning)", "Night"),
        ("Rachel King", 39, "Mon-Fri (Morning), Sat-Sun (Flexible)", "Morning"),
        ("Simon Wright", 42, "Mon-Wed (Afternoon), Thu-Sun (Morning)", "Afternoon"),
        ("Theresa Walker", 37, "Mon-Fri (Morning), Sat-Sun (Night)", "Night"),
        ("Victor Hall", 36, "Mon-Wed (Night), Thu-Sun (Afternoon)", "Night"),
        ("Wendy Allen", 32, "Mon-Fri (Evening), Sat (Morning)", "Evening"),
        ("Xavier Wright", 40, "Mon-Fri (Morning), Sat (Afternoon)", "Morning"),
        ("Yvonne Evans", 29, "Mon-Wed (Afternoon), Fri-Sun (Morning)", "Afternoon"),
        ("Zachary Adams", 44, "Mon-Fri (Night), Sat (Morning)", "Night"),
        ("Abigail Phillips", 25, "Mon-Wed (Morning), Thu-Sun (Flexible)", "Morning")
    ]

    # Insert nurse data into database
    cursor.executemany("INSERT INTO nurses (name, age, availability, preferred_shifts) VALUES (?, ?, ?, ?)", nurse_data)

    # Function to generate two weeks of unassigned shifts
    def insert_shift_data():
        shift_types = ["Morning", "Afternoon", "Night"]
        start_date = datetime(2025, 2, 19)
        shifts = []

        for day in range(14):  # Two weeks
            date = start_date + timedelta(days=day)
            formatted_date = date.strftime("%Y-%m-%d")
            for shift in shift_types:
                shifts.append((formatted_date, shift, None))  # Assigned_nurse is NULL

        cursor.executemany("INSERT INTO shifts (date, shift_type, assigned_nurse) VALUES (?, ?, ?)", shifts)

    # Insert unassigned shifts into database
    insert_shift_data()

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Database setup complete: Nurses and unassigned shifts added!")

# Allow the script to be run directly
if __name__ == "__main__":
    setup_database()