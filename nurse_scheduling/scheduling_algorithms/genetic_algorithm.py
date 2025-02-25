# scheduling_algorithms/genetic_algorithm.py

import random
import sys
import os

# Ensure proper path for importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary modules
from scheduling_algorithms.greedy_initialization import greedy_initialization
from evaluation.fitness_function import evaluate_schedule
from constraints.constraints import validate_schedule
from models.shift import Shift  # Import Shift class

try:
    from data_loader import fetch_nurses, fetch_shifts  # ✅ Check if this exists
except ImportError:
    print("⚠️ WARNING: data_loader module not found. Make sure it exists!")

from models.schedule import Schedule

# Genetic Algorithm Parameters
POPULATION_SIZE = 10
MUTATION_RATE = 0.1
GENERATIONS = 50
FITNESS_THRESHOLD = -10  # Stop early if fitness reaches this level
STAGNANT_LIMIT = 10  # Stop if no improvement for 10 generations

def initialize_population():
    """
    Initializes the population using greedy initialization and adds randomness for diversity.
    """
    nurses = fetch_nurses()
    shifts = fetch_shifts()
    population = []

    # Use greedy initialization for half the population
    for _ in range(POPULATION_SIZE // 2):
        schedule = Schedule()  # Create a new Schedule object
        schedule.assignments = greedy_initialization(nurses, shifts)  # Assign the dictionary to `assignments`
        population.append(schedule)

    # Add random initialization for the other half
    for _ in range(POPULATION_SIZE // 2):
        schedule = Schedule()  # Create a new Schedule object
        random_schedule = {nurse["nurse_id"]: [] for nurse in nurses}  # Initialize as a list of Shift objects
        for shift in shifts:
            available_nurses = [nurse for nurse in nurses if shift["date"] in nurse["availability"]]
            if available_nurses:
                nurse = random.choice(available_nurses)
                # Create a Shift object and assign it to the nurse
                shift_obj = Shift(shift["shift_id"], shift["date"], shift["shift_type"], nurse["nurse_id"])
                random_schedule[nurse["nurse_id"]].append(shift_obj)
        schedule.assignments = random_schedule  # Assign the dictionary to `assignments`
        population.append(schedule)

    # Debugging: Print the first schedule in the population
    print("First schedule in population:")
    for nurse_id, shifts in population[0].assignments.items():
        print(f"Nurse {nurse_id} has {len(shifts)} shifts assigned.")

    return population

def evaluate_population(population):
    """
    Evaluates fitness scores for the entire population.
    """
    evaluated_population = []
    for schedule in population:
        fitness_score = evaluate_schedule(schedule)
        evaluated_population.append((schedule, fitness_score))

    return evaluated_population

def selection(population_scores):
    """
    Selects two parents using tournament selection.
    """
    # Tournament selection: Randomly pick 2 individuals and select the best one
    tournament_size = 2
    parents = []
    for _ in range(2):
        tournament = random.sample(population_scores, tournament_size)
        winner = max(tournament, key=lambda x: x[1])  # Select the one with the highest fitness
        parents.append(winner[0])
    return parents[0], parents[1]

def crossover(parent1, parent2):
    """
    Creates a child schedule by combining shifts from two parent schedules.
    Resolves conflicts by prioritizing shifts from parent1.
    """
    child = Schedule()
    child.assignments = {}

    # Combine shifts from both parents
    for nurse_id in parent1.assignments:
        child.assignments[nurse_id] = parent1.assignments[nurse_id].copy()

    for nurse_id in parent2.assignments:
        for shift in parent2.assignments[nurse_id]:
            if shift not in child.assignments.get(nurse_id, []):
                if nurse_id not in child.assignments:
                    child.assignments[nurse_id] = []
                child.assignments[nurse_id].append(shift)

    return child

def mutate(schedule):
    """
    Randomly mutates a schedule by reassigning shifts.
    Ensures that constraints are still satisfied after mutation.
    """
    for nurse_id in schedule.assignments:
        if random.random() < MUTATION_RATE:
            shifts = schedule.assignments[nurse_id]
            if shifts:
                random_shift = random.choice(shifts)
                available_shifts = ["Morning", "Afternoon", "Night"]
                random_shift.shift_type = random.choice(available_shifts)

    # Validate the mutated schedule
    if not validate_schedule(schedule):
        # If the schedule is invalid, revert the mutation
        for nurse_id in schedule.assignments:
            if random.random() < MUTATION_RATE:
                shifts = schedule.assignments[nurse_id]
                if shifts:
                    random_shift = random.choice(shifts)
                    available_shifts = ["Morning", "Afternoon", "Night"]
                    random_shift.shift_type = random.choice(available_shifts)

    return schedule

def genetic_algorithm():
    """
    Runs the Genetic Algorithm for nurse scheduling.
    """
    print("🚀 Genetic Algorithm Started!")

    # Step 1: Initialize Population
    population = initialize_population()
    population_scores = evaluate_population(population)

    best_schedule = None
    best_fitness = float('-inf')
    stagnant_generations = 0

    for generation in range(GENERATIONS):
        print(f"⚡ Generation {generation + 1}/{GENERATIONS}")

        # Step 2: Evaluate Fitness
        population_scores = evaluate_population(population)

        # Step 3: Selection
        parent1, parent2 = selection(population_scores)

        # Step 4: Crossover
        child = crossover(parent1, parent2)

        # Step 5: Mutation
        child = mutate(child)

        # Replace worst individual with child
        population_scores.sort(key=lambda x: x[1])
        population_scores[0] = (child, evaluate_schedule(child))

        # Update population
        population = [schedule for schedule, _ in population_scores]

        # Step 6: Track Best Fitness
        current_best_fitness = max(population_scores, key=lambda x: x[1])[1]
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_schedule = max(population_scores, key=lambda x: x[1])[0]
            stagnant_generations = 0
        else:
            stagnant_generations += 1

        print(f"✅ Best Fitness So Far: {best_fitness}")

        # Step 7: Stopping Conditions
        if best_fitness >= FITNESS_THRESHOLD:
            print("🚀 Stopping early: Fitness threshold met!")
            break
        if stagnant_generations >= STAGNANT_LIMIT:
            print("🚀 Stopping early: No improvement in 10 generations.")
            break

    return best_schedule

if __name__ == "__main__":
    final_schedule = genetic_algorithm()
    print("✅ Genetic Algorithm Finished!")
    print(final_schedule)  # Print final optimized schedule