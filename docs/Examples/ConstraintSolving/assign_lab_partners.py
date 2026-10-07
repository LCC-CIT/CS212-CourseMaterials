#!/usr/bin/env python3
"""
Lab Partner and Version Assignment Solver using Z3 SMT Solver.
Reads student names from a CSV file and assigns lab partner groups (sizes 2 or 3)
and assignment versions (A, B, C) such that no two students in the same group
receive the same version.
"""

import argparse
import csv
import math
import sys
from pathlib import Path
from z3 import Solver, Int, If, Implies, sat


def load_students_from_csv(csv_path: Path) -> list[str]:
    """Load student names from a CSV file.
    
    Supports CSVs with a 'Name'/'Student' column header, or single-column files.
    """
    students = []
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            first_val = row[0].strip()
            # Skip obvious header rows
            if first_val.lower() in {"name", "student", "students", "student name", "student_name"}:
                continue
            if first_val:
                students.append(first_val)

    if not students:
        raise ValueError(f"No student names found in {csv_path}")

    return students


def solve_group_assignments(students: list[str], max_group_size: int = 3):
    """Assign students to groups and versions using Z3."""
    num_students = len(students)
    if num_students < 2:
        raise ValueError(f"At least 2 students are required for groups (found {num_students})")

    # 1. Calculate group parameters
    num_groups = math.ceil(num_students / max_group_size)
    remainder = num_students % max_group_size

    if remainder == 0:
        num_groups_of_2 = 0
    elif remainder == 2:
        num_groups_of_2 = 1
    else:  # remainder == 1 (e.g., 4 students remaining: split into two groups of 2)
        num_groups_of_2 = 2

    num_groups_of_3 = num_groups - num_groups_of_2

    # 2. Decision variables
    group = []
    version = []
    for i in range(num_students):
        group.append(Int(f"group_{i}"))
        version.append(Int(f"version_{i}"))

    s = Solver()

    # 3. Domain / Range constraints
    for i in range(num_students):
        s.add(group[i] >= 0, group[i] < num_groups)
        s.add(version[i] >= 0, version[i] < 3)  # 0=A, 1=B, 2=C

    # 4. Group size constraints using an accumulator loop
    for g in range(num_groups):
        group_size = 0
        for i in range(num_students):
            group_size += If(group[i] == g, 1, 0)

        if g < num_groups_of_3:
            s.add(group_size == 3)
        else:
            s.add(group_size == 2)

    # 5. Version diversity constraints (within each group, distinct versions)
    for i in range(num_students):
        for j in range(i + 1, num_students):
            s.add(Implies(group[i] == group[j], version[i] != version[j]))

    # 6. Solve
    if s.check() != sat:
        return None, num_groups, num_groups_of_3, num_groups_of_2

    m = s.model()
    versions_map = {0: "A", 1: "B", 2: "C"}

    # Organize results by group
    groups_dict = {}
    for g in range(num_groups):
        groups_dict[g] = []

    for i in range(num_students):
        name = students[i]
        g_val = m[group[i]].as_long()
        v_val = m[version[i]].as_long()
        groups_dict[g_val].append((name, versions_map[v_val]))

    return groups_dict, num_groups, num_groups_of_3, num_groups_of_2


def save_results_to_csv(groups_dict: dict, output_path: Path):
    """Save the final group assignments to a CSV file."""
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Group", "Student", "Lab Version"])
        for g in range(len(groups_dict)):
            for name, ver in groups_dict[g]:
                writer.writerow([g + 1, name, ver])


def main():
    parser = argparse.ArgumentParser(
        description="Assign lab partner groups and versions using the Z3 SMT Solver."
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=Path("students.csv"),
        help="Path to input CSV file containing student names (default: students.csv)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Optional path to output CSV file for assignments"
    )
    args = parser.parse_args()

    input_path = args.input
    # If a relative path is passed and doesn't exist in CWD, check relative to the script
    if not input_path.exists():
        script_relative = Path(__file__).parent / input_path
        if script_relative.exists():
            input_path = script_relative

    try:
        students = load_students_from_csv(input_path)
    except Exception as e:
        print(f"Error loading students: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(students)} students from: {input_path}")
    groups_dict, num_groups, g3, g2 = solve_group_assignments(students)

    if groups_dict is None:
        print("No valid grouping or version assignment found.", file=sys.stderr)
        sys.exit(2)

    print(f"Total groups: {num_groups} ({g3} groups of 3, {g2} groups of 2)\n")
    print("=== Lab Partner Groups and Assignments ===\n")
    for g in range(num_groups):
        print(f"Group {g + 1} (Size {len(groups_dict[g])}):")
        for name, ver in groups_dict[g]:
            print(f"  - {name}: Version {ver}")
        print()

    if args.output:
        save_results_to_csv(groups_dict, args.output)
        print(f"Assignments saved to: {args.output}")


if __name__ == "__main__":
    main()
