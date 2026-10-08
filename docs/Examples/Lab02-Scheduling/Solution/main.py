"""
Lab 2 class example: schedule auto repair jobs with the Z3 constraint solver.

This module handles the output. Run it with:  uv run main.py
"""

import os

from data_loader import load_data
from scheduler import (solve_schedule, minimize_part_time_with_loop,
                       minimize_part_time_with_optimizer)

# The data files are in the same folder as this program
PROGRAM_FOLDER = os.path.dirname(os.path.abspath(__file__))
UNSOLVABLE_FOLDER = os.path.join(PROGRAM_FOLDER, "unsolvable_data")


def by_slot(entry):
    """Sort key: time slot first, then job ID."""
    return (entry["slot"], entry["job_id"])


def print_schedule(schedule):
    print(f"{'Time':<10}{'Job':<6}{'Service':<18}{'Mechanic':<16}{'Bay'}")
    print("-" * 54)
    for entry in sorted(schedule, key=by_slot):
        print(f"{entry['time']:<10}{entry['job_id']:<6}{entry['service']:<18}"
              f"{entry['mechanic_name']:<16}{entry['bay_id']}")


def print_answer(answer):
    """Print a schedule, or the reason there isn't one."""
    if answer["status"] == "sat":
        print_schedule(answer["schedule"])
    elif answer["status"] == "unsat":
        print("No schedule is possible. Conflicting rules:", ", ".join(answer["conflicts"]))
    else:
        print("The solver timed out before it found an answer.")


def main():
    print("=== Schedule ===")
    data = load_data(PROGRAM_FOLDER)
    print_answer(solve_schedule(data))

    print()
    print("=== Unsolvable data sets ===")
    for name in sorted(os.listdir(UNSOLVABLE_FOLDER)):
        print(name + ": ", end="")
        print_answer(solve_schedule(load_data(os.path.join(UNSOLVABLE_FOLDER, name))))

    print()
    print("=== Challenge 2, Option A: push() and pop() loop ===")
    answer = minimize_part_time_with_loop(data)
    if answer["status"] == "sat":
        print("Jobs done by part-time mechanics:", answer["count"])
    print_answer(answer)

    print()
    print("=== Challenge 2, Option B: Optimize ===")
    answer = minimize_part_time_with_optimizer(data)
    if answer["status"] == "sat":
        print("Jobs done by part-time mechanics:", answer["count"])
    print_answer(answer)


if __name__ == "__main__":
    main()
