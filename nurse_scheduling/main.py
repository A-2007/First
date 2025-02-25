# main.py

import sys
import os

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary modules
from data_handling.database_setup import setup_database
from scheduling_algorithms.genetic_algorithm import genetic_algorithm
from models.schedule import Schedule

def main():
    # Step 1: Initialize the database (if not already done)
    print("🚀 Setting up the database...")
    setup_database()

    # Step 2: Run the genetic algorithm
    print("🚀 Running the genetic algorithm...")
    final_schedule = genetic_algorithm()

    # Step 3: Display the final optimized schedule
    print("✅ Genetic Algorithm Finished!")
    print("📅 Final Optimized Schedule:")
    final_schedule.display_schedule()

if __name__ == "__main__":
    main()
