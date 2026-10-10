"""
The Z3 model for scheduling auto repair jobs, and the code that solves it.

This module doesn't read files or print anything (requirement 7). It takes the
data loaded by data_loader.py and returns results as Python dictionaries and lists.
"""

from z3 import Solver, Optimize, Int, Bool, BoolVal, And, Or, Implies, Sum, If, sat, unsat

TIME_SLOTS = ["7:00 am", "8:00 am", "9:00 am", "10:00 am",
              "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm"]

GROUP_NAMES = ["domain", "bay_conflict", "mechanic_conflict", "qualification",
               "workload", "time_window"]


def create_variables(jobs):
    """Make one slot, mechanic and bay variable for each job (requirement 3)."""
    slot = []
    mechanic = []
    bay = []
    for job in jobs:
        job_id = job["job_id"]
        slot.append(Int("slot_" + job_id))
        mechanic.append(Int("mechanic_" + job_id))
        bay.append(Int("bay_" + job_id))
    return slot, mechanic, bay


def create_flags():
    """Make one Boolean tracking flag per constraint group (requirement 6)."""
    flags = {}
    flag_list = []
    for name in GROUP_NAMES:
        flags[name] = Bool(name)
        flag_list.append(flags[name])
    return flags, flag_list


def add_constraints(solver, data, slot, mechanic, bay, flags):
    """Add the constraints for all six scheduling rules (requirement 4).

    solver can be a Solver or an Optimize object, since both have an add() method.
    """
    mechanics = data["mechanics"]
    bays = data["bays"]
    jobs = data["jobs"]

    # Every constraint is added through this function so it belongs to a group.
    # Implies(flag, constraint) means "if the flag is on, the constraint applies".
    # When there's no solution, Z3 reports which flags it had to turn on to find
    # the conflict. That tells us which rules can't all be met at the same time.
    def add(group, constraint):
        solver.add(Implies(flags[group], constraint))

    # j is the job number and w is the mechanic ("worker") number.
    # They are positions in the jobs and mechanics lists.
    for j in range(len(jobs)):
        job = jobs[j]

        # Rule 1: the slot, mechanic and bay all exist
        add("domain", And(slot[j] >= 0, slot[j] < len(TIME_SLOTS),
                          mechanic[j] >= 0, mechanic[j] < len(mechanics),
                          bay[j] >= 0, bay[j] < len(bays)))

        # Rule 4: the mechanic is certified for this service
        qualified = []
        for w in range(len(mechanics)):
            if job["service"] in mechanics[w]["certifications"]:
                qualified.append(mechanic[j] == w)
        if len(qualified) > 0:
            add("qualification", Or(qualified))
        else:
            # No mechanic is certified for this service, so the rule can't be met
            add("qualification", BoolVal(False))

        # Rule 6: the job is done within its time window
        add("time_window", And(slot[j] >= job["earliest_slot"],
                               slot[j] <= job["latest_slot"]))

        # Rules 2 and 3: compare this job with every earlier job
        for k in range(j):
            add("bay_conflict", Implies(slot[j] == slot[k], bay[j] != bay[k]))
            add("mechanic_conflict", Implies(slot[j] == slot[k], mechanic[j] != mechanic[k]))

    # Rule 5: count the jobs each mechanic does
    for w in range(len(mechanics)):
        terms = []
        for j in range(len(jobs)):
            terms.append(If(mechanic[j] == w, 1, 0))
        add("workload", Sum(terms) <= mechanics[w]["max_jobs"])


def read_schedule(model, data, slot, mechanic, bay):
    """Read the solution out of a Z3 model as a list of dictionaries (requirement 5)."""
    schedule = []
    for j in range(len(data["jobs"])):
        job = data["jobs"][j]

        # model_completion=True makes Z3 fill in a value if no rule mentions
        # the variable, so we always get a number back.
        # as_long() converts the Z3 number to a regular Python int.
        slot_number = model.eval(slot[j], model_completion=True).as_long()
        mechanic_number = model.eval(mechanic[j], model_completion=True).as_long()
        bay_number = model.eval(bay[j], model_completion=True).as_long()

        # The numbers are positions in the mechanics and bays lists
        mechanic_info = data["mechanics"][mechanic_number]
        bay_info = data["bays"][bay_number]

        schedule.append({
            "job_id": job["job_id"],
            "service": job["service"],
            "slot": slot_number,
            "time": TIME_SLOTS[slot_number],
            "mechanic_id": mechanic_info["mechanic_id"],
            "mechanic_name": mechanic_info["name"],
            "bay_id": bay_info["bay_id"],
        })
    return schedule


def core_group_names(core):
    """Turn the flags in an unsat core into a sorted list of group names."""
    names = []
    for flag in core:
        names.append(str(flag))
    names.sort()
    return names


def solve_schedule(data, timeout_ms=10000):
    """Find a schedule (requirement 5) or explain why there isn't one (requirement 6).

    Returns a dictionary with these keys:
      "status":    "sat", "unsat" or "unknown"
      "schedule":  the schedule when status is "sat", otherwise None
      "conflicts": the conflicting group names when status is "unsat", otherwise []
    """
    solver = Solver()
    solver.set("timeout", timeout_ms)
    slot, mechanic, bay = create_variables(data["jobs"])
    flags, flag_list = create_flags()    # the function returns two values
    add_constraints(solver, data, slot, mechanic, bay, flags)

    result = solver.check(flag_list)    # the flags are passed in as assumptions

    answer = {"status": str(result), "schedule": None, "conflicts": []}
    if result == sat:
        answer["schedule"] = read_schedule(solver.model(), data, slot, mechanic, bay)
    elif result == unsat:
        answer["conflicts"] = core_group_names(solver.unsat_core())
    return answer


# ----- Challenge 2: minimizing the jobs done by part-time mechanics -----

def is_part_time(mechanic_info):
    """Part-time mechanics are the ones who can do at most 2 jobs."""
    return mechanic_info["max_jobs"] == 2


def count_part_time_jobs(data, mechanic):
    """A Z3 expression for the number of jobs done by part-time mechanics."""
    part_time_terms = []
    for j in range(len(data["jobs"])):
        done_by_part_time = []
        for w in range(len(data["mechanics"])):
            if is_part_time(data["mechanics"][w]):
                done_by_part_time.append(mechanic[j] == w)
        part_time_terms.append(If(Or(done_by_part_time), 1, 0))
    return Sum(part_time_terms)


def part_time_lower_bound(data):
    """The fewest part-time jobs possible: the jobs full-time mechanics can't cover."""
    full_time_capacity = 0
    for mechanic_info in data["mechanics"]:
        if not is_part_time(mechanic_info):
            full_time_capacity = full_time_capacity + mechanic_info["max_jobs"]
    lower_bound = len(data["jobs"]) - full_time_capacity
    if lower_bound < 0:
        lower_bound = 0
    return lower_bound


def minimize_part_time_with_loop(data, timeout_ms=10000):
    """Option A: lower the limit on part-time jobs with push() and pop().

    Returns a dictionary with these keys:
      "status":    "sat" if at least one schedule was found, otherwise the last check result
      "count":     the fewest part-time jobs found, or None
      "schedule":  the schedule that goes with it, or None
    """
    solver = Solver()
    solver.set("timeout", timeout_ms)
    slot, mechanic, bay = create_variables(data["jobs"])
    flags, flag_list = create_flags()
    add_constraints(solver, data, slot, mechanic, bay, flags)
    part_time_jobs = count_part_time_jobs(data, mechanic)
    lower_bound = part_time_lower_bound(data)

    answer = {"status": "unknown", "count": None, "schedule": None}

    limit = len(data["jobs"])
    while limit >= lower_bound:
        solver.push()                               # save a checkpoint
        solver.add(part_time_jobs <= limit)         # try a tighter limit
        result = solver.check(flag_list)
        if result == sat:
            # Read the model before pop(), because it belongs to this check
            model = solver.model()
            answer["status"] = "sat"
            answer["count"] = model.eval(part_time_jobs, model_completion=True).as_long()
            answer["schedule"] = read_schedule(model, data, slot, mechanic, bay)
        solver.pop()                                # remove the limit
        if result != sat:
            # Keep the last good schedule. Only report the failure
            # if we never found one.
            if answer["count"] is None:
                answer["status"] = str(result)
            break
        limit = limit - 1                           # try one fewer part-time job
    return answer


def minimize_part_time_with_optimizer(data, timeout_ms=30000):
    """Option B: let Z3's Optimize class find the minimum.

    Returns a dictionary with the same keys as minimize_part_time_with_loop().
    """
    optimizer = Optimize()
    optimizer.set("timeout", timeout_ms)
    slot, mechanic, bay = create_variables(data["jobs"])
    flags, flag_list = create_flags()
    add_constraints(optimizer, data, slot, mechanic, bay, flags)
    # Turn every constraint group on. Passing the flags to check() as assumptions
    # made the optimizer time out in testing.
    for flag in flag_list:
        optimizer.add(flag)
    part_time_jobs = count_part_time_jobs(data, mechanic)
    # The lower bound tells the optimizer it can stop at that number. Without it,
    # Z3 spends a long time trying to prove that a smaller number is impossible.
    optimizer.add(part_time_jobs >= part_time_lower_bound(data))
    optimizer.minimize(part_time_jobs)

    result = optimizer.check()

    answer = {"status": str(result), "count": None, "schedule": None}
    if result == sat:
        model = optimizer.model()
        answer["count"] = model.eval(part_time_jobs, model_completion=True).as_long()
        answer["schedule"] = read_schedule(model, data, slot, mechanic, bay)
    return answer
