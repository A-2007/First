import sqlite3

DB_PATH = "C:\\Users\\elmaw\\OneDrive\\Documents\\nurse_scheduling\\nurse_schedule.db"


def fetch_nurses():
    """Loads nurse data from the database and returns a list of dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT nurse_id, name, age, availability, preferred_shifts FROM nurses;")
    nurses = cursor.fetchall()
    
    conn.close()

    return [
        {
            "nurse_id": row[0],
            "name": row[1],
            "age": row[2],
            "availability": row[3],
            "preferred_shifts": row[4],
        }
        for row in nurses
    ]

def fetch_shifts():
    """Loads shift data from the database and returns a list of dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT shift_id, date, shift_type, assigned_nurse FROM shifts;")
    shifts = cursor.fetchall()
    
    conn.close()

    return [
        {
            "shift_id": row[0],
            "date": row[1],
            "shift_type": row[2],
            "assigned_nurse": row[3]  # Will be None if not assigned
        }
        for row in shifts
    ]

if __name__ == "__main__":
    # Test loading data
    nurses = fetch_nurses()
    shifts = fetch_shifts()

    print("Sample Nurse Data:")
    for nurse in nurses[:5]:  # Print first 5 nurses
        print(nurse)

    print("\nSample Shift Data:")
    for shift in shifts[:5]:  # Print first 5 shifts
        print(shift)

