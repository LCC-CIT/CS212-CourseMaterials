"""
Tests for the scheduler (requirement 8). Run them with:  uv run test_scheduler.py
(or with pytest:  uv run pytest)

check_schedule() checks a schedule against the six rules in plain Python,
without Z3, so it doesn't depend on the code it is testing.
"""

import os

from data_loader import load_data
from scheduler import (TIME_SLOTS, solve_schedule, minimize_part_time_with_loop,
                       minimize_part_time_with_optimizer, part_time_lower_bound)

# These paths start at the folder where the tests are run (run them from this folder).
DATA_FOLDER = os.path.join("..", "Data")
UNSOLVABLE_FOLDER = "unsolvable_data"


def check_schedule(schedule, data):
    """Return a list of the rules the schedule breaks. An empty list means it's valid."""
    broken = []

    # Look up mechanics, bays and jobs by ID
    mechanics_by_id = {}
    for mechanic_info in data["mechanics"]:
        mechanics_by_id[mechanic_info["mechanic_id"]] = mechanic_info
    bay_ids = []
    for bay_info in data["bays"]:
        bay_ids.append(bay_info["bay_id"])
    jobs_by_id = {}
    for job in data["jobs"]:
        jobs_by_id[job["job_id"]] = job

    # Rule 1: every job is scheduled once, with a slot, mechanic and bay that exist
    scheduled_ids = []
    for entry in schedule:
        scheduled_ids.append(entry["job_id"])
    if sorted(scheduled_ids) != sorted(jobs_by_id.keys()):
        broken.append("domain")
    for entry in schedule:
        if (entry["slot"] < 0 or entry["slot"] >= len(TIME_SLOTS)
                or entry["mechanic_id"] not in mechanics_by_id
                or entry["bay_id"] not in bay_ids):
            broken.append("domain")

    # Rules 2 and 3: no shared bay or mechanic in the same slot
    for j in range(len(schedule)):
        for k in range(j):
            if schedule[j]["slot"] == schedule[k]["slot"]:
                if schedule[j]["bay_id"] == schedule[k]["bay_id"]:
                    broken.append("bay_conflict")
                if schedule[j]["mechanic_id"] == schedule[k]["mechanic_id"]:
                    broken.append("mechanic_conflict")

    # Rules 4 and 6: qualified mechanic and allowed time window
    for entry in schedule:
        mechanic_info = mechanics_by_id.get(entry["mechanic_id"])
        job = jobs_by_id.get(entry["job_id"])
        if mechanic_info is None or job is None:
            continue    # already reported as a domain problem
        if job["service"] not in mechanic_info["certifications"]:
            broken.append("qualification")
        if entry["slot"] < job["earliest_slot"] or entry["slot"] > job["latest_slot"]:
            broken.append("time_window")

    # Rule 5: no mechanic over their limit
    counts = {}
    for entry in schedule:
        mechanic_id = entry["mechanic_id"]
        counts[mechanic_id] = counts.get(mechanic_id, 0) + 1
    for mechanic_id in counts:
        mechanic_info = mechanics_by_id.get(mechanic_id)
        if mechanic_info is not None and counts[mechanic_id] > mechanic_info["max_jobs"]:
            broken.append("workload")

    # Report each broken rule only once
    unique = []
    for name in broken:
        if name not in unique:
            unique.append(name)
    return unique


def count_part_time(schedule, data):
    """Count the jobs done by part-time mechanics, in plain Python."""
    part_time_ids = []
    for mechanic_info in data["mechanics"]:
        if mechanic_info["max_jobs"] == 2:    # part-time
            part_time_ids.append(mechanic_info["mechanic_id"])
    count = 0
    for entry in schedule:
        if entry["mechanic_id"] in part_time_ids:
            count = count + 1
    return count


# ----- The schedule from the real data -----

def test_real_data_schedule_passes_every_rule():
    data = load_data(DATA_FOLDER)
    answer = solve_schedule(data)
    assert answer["status"] == "sat"
    assert check_schedule(answer["schedule"], data) == []


# ----- The unsolvable data sets -----

def check_unsolvable(folder_name, expected_group):
    data = load_data(os.path.join(UNSOLVABLE_FOLDER, folder_name))
    answer = solve_schedule(data)
    assert answer["status"] == "unsat"
    assert expected_group in answer["conflicts"]


def test_uncertified_service_is_unsolvable():
    check_unsolvable("uncertified_service", "qualification")


def test_reversed_time_window_is_unsolvable():
    check_unsolvable("reversed_time_window", "time_window")


def test_too_many_jobs_is_unsolvable():
    check_unsolvable("too_many_jobs", "workload")


# ----- The checker catches schedules broken on purpose -----

def broken_copy(schedule):
    """Copy a schedule so the original isn't changed."""
    copy = []
    for entry in schedule:
        copy.append(dict(entry))
    return copy


def test_checker_catches_bay_conflict():
    data = load_data(DATA_FOLDER)
    schedule = broken_copy(solve_schedule(data)["schedule"])
    # The schedule is in the same order as data["jobs"]. Find a job that can
    # move into job 0's slot, and put it in job 0's bay.
    for j in range(1, len(schedule)):
        job = data["jobs"][j]
        if job["earliest_slot"] <= schedule[0]["slot"] <= job["latest_slot"]:
            schedule[j]["slot"] = schedule[0]["slot"]
            schedule[j]["bay_id"] = schedule[0]["bay_id"]
            break
    assert "bay_conflict" in check_schedule(schedule, data)


def test_checker_catches_unqualified_mechanic():
    data = load_data(DATA_FOLDER)
    schedule = broken_copy(solve_schedule(data)["schedule"])
    # M02 isn't certified for brakes, which job J101 needs
    schedule[0]["mechanic_id"] = "M02"
    assert "qualification" in check_schedule(schedule, data)


def test_checker_catches_time_window():
    data = load_data(DATA_FOLDER)
    schedule = broken_copy(solve_schedule(data)["schedule"])
    # J104 is an afternoon job (slots 6 to 7)
    for entry in schedule:
        if entry["job_id"] == "J104":
            entry["slot"] = 0
    assert "time_window" in check_schedule(schedule, data)


# ----- Challenge 2 -----

def test_loop_finds_fewest_part_time_jobs():
    data = load_data(DATA_FOLDER)
    answer = minimize_part_time_with_loop(data)
    assert answer["status"] == "sat"
    assert check_schedule(answer["schedule"], data) == []
    assert answer["count"] == part_time_lower_bound(data)
    assert count_part_time(answer["schedule"], data) == answer["count"]


def test_optimizer_finds_fewest_part_time_jobs():
    data = load_data(DATA_FOLDER)
    answer = minimize_part_time_with_optimizer(data)
    assert answer["status"] == "sat"
    assert check_schedule(answer["schedule"], data) == []
    assert answer["count"] == part_time_lower_bound(data)
    assert count_part_time(answer["schedule"], data) == answer["count"]


# ----- Test driver, so the tests also run without pytest: uv run test_scheduler.py -----

if __name__ == "__main__":
    tests = [
        test_real_data_schedule_passes_every_rule,
        test_uncertified_service_is_unsolvable,
        test_reversed_time_window_is_unsolvable,
        test_too_many_jobs_is_unsolvable,
        test_checker_catches_bay_conflict,
        test_checker_catches_unqualified_mechanic,
        test_checker_catches_time_window,
        test_loop_finds_fewest_part_time_jobs,
        test_optimizer_finds_fewest_part_time_jobs,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print("PASS:", test.__name__)
            passed = passed + 1
        except AssertionError:
            print("FAIL:", test.__name__)
        except Exception as error:    # a crash in the test is a failure too
            print("ERROR:", test.__name__, "-", error)
    print(passed, "of", len(tests), "tests passed")
