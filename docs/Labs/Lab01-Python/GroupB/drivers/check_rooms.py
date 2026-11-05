"""Group B, Part 1 -- meeting room reservation. Prints one PASS/FAIL line per case."""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import find_student_file, run_cases, words, report  # noqa: E402

ROOMS = ['alpha', 'beta', 'gamma', 'den']   # 'den' accepts a misspelled "Denied"
ROLES = {'attendees': r'attendee|people|count|size|num|guest', 'projector': r'project|av|equip'}


def judge(ret, out, expected):
    t = words(ret, out)
    if expected == 'none':      # invalid headcount: must not recommend a room
        return not any(r in t for r in ROOMS)
    return expected in t and not any(r in t for r in ROOMS if r != expected)


def variants(role, value):
    if role == 'projector':
        return [value, 'yes' if value else 'no', 'true' if value else 'false']
    return [value]


root = os.getcwd()
path = find_student_file(root, r'room|attendee')
if not path:
    print('no room reservation program found')
    sys.exit(2)

cases = []
for n in (1, 3, 5):
    for p in (False, True):
        cases.append((f'{n} attendees, projector {p}: Room Alpha', {'attendees': n, 'projector': p}, 'alpha'))
for n in (6, 10, 15):
    cases.append((f'{n} attendees, projector needed: Room Beta', {'attendees': n, 'projector': True}, 'beta'))
    cases.append((f'{n} attendees, no projector: Room Gamma', {'attendees': n, 'projector': False}, 'gamma'))
for n in (16, 40):
    for p in (False, True):
        cases.append((f'{n} attendees, projector {p}: Reservation Denied', {'attendees': n, 'projector': p}, 'den'))
cases.append(('0 attendees: no room recommended', {'attendees': 0, 'projector': False}, 'none'))
cases.append(('-3 attendees: no room recommended', {'attendees': -3, 'projector': False}, 'none'))

results, note = run_cases(path, ROLES, cases, judge, variants)
for name, _, _ in cases:
    report(name, results[name], note)
