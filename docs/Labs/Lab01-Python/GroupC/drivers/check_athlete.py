"""Group C, Part 2 -- athlete performance rating. Prints one PASS/FAIL line per case."""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import find_student_file, run_cases, words, report  # noqa: E402

TIERS = ['elite', 'advanc', 'intermediate', 'beginner']   # 'advanc' accepts "advance" and "advanced"
ROLES = {'speed': r'speed', 'strength': r'strength|strong|power'}
OBJECT_ATTRS = {'speed': ['speed', 'speed_score', 'speedScore'], 'strength': ['strength', 'strength_score', 'strengthScore'], 'name': []}


def judge(ret, out, expected):
    t = words(ret, out)
    found = {x for x in TIERS if re.search(r'\b%s' % x, t)}
    return found == {expected}


root = os.getcwd()
path = find_student_file(root, r'speed')
if not path:
    print('no athlete rating program found')
    sys.exit(2)

TIER_NAMES = {'advanc': 'Advanced'}
TABLE = [
    (95, 85, 'elite'), (90, 80, 'elite'), (100, 100, 'elite'),
    (90, 79, 'advanc'), (89, 80, 'advanc'), (70, 0, 'advanc'), (0, 70, 'advanc'), (49, 100, 'advanc'),
    (69, 69, 'intermediate'), (50, 0, 'intermediate'), (60, 60, 'intermediate'),
    (49, 69, 'beginner'), (0, 0, 'beginner'), (10, 40, 'beginner'),
]
cases = [(f'Speed {s}, strength {g}: {TIER_NAMES.get(e, e.capitalize())}', {'speed': s, 'strength': g}, e) for s, g, e in TABLE]
results, note = run_cases(path, ROLES, cases, judge, object_attrs=OBJECT_ATTRS, strict_name='rate_athlete')
for name, _, _ in cases:
    report(name, results[name], note)
