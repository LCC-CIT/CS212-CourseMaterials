"""
Loads the scheduling data from CSV files (requirement 2).
"""

import csv
import os


def load_csv(filename):
    """Load a CSV file into a list of dictionaries, one per row."""
    rows = []
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows


def load_data(folder):
    """Load mechanics.csv, bays.csv and jobs.csv from a folder.

    Returns a dictionary with the keys "mechanics", "bays" and "jobs".
    Numbers are converted to int and semicolon lists are split into Python lists.
    """
    mechanics = load_csv(os.path.join(folder, "mechanics.csv"))
    bays = load_csv(os.path.join(folder, "bays.csv"))
    jobs = load_csv(os.path.join(folder, "jobs.csv"))

    for mechanic_info in mechanics:
        mechanic_info["max_jobs"] = int(mechanic_info["max_jobs"])
        mechanic_info["certifications"] = mechanic_info["certifications"].split(";")
    for job in jobs:
        job["earliest_slot"] = int(job["earliest_slot"])
        job["latest_slot"] = int(job["latest_slot"])

    data = {}
    data["mechanics"] = mechanics
    data["bays"] = bays
    data["jobs"] = jobs
    return data
