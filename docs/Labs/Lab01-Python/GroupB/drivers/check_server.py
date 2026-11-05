"""Group B, Part 2 -- server status and priority alert. Prints one PASS/FAIL line per case."""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import find_student_file, run_cases, words, report  # noqa: E402

LEVELS = ['high', 'medium', 'low', 'clear']
ROLES = {'health': r'health|code|status|state', 'hours': r'hour|time|since|check|last'}


def judge(ret, out, expected):
    t = words(ret, out)
    found = {lv for lv in LEVELS if re.search(r'\b%s\b' % lv, t)}
    return found == {expected}


root = os.getcwd()
path = find_student_file(root, r'health|server')
if not path:
    print('no server status program found')
    sys.exit(2)

TABLE = [  # (health code, hours, priority)
    (1, 0, 'high'), (1, 3, 'high'), (1, 100, 'high'),
    (2, 5, 'high'), (2, 4.5, 'high'), (2, 12, 'high'),
    (2, 4, 'medium'), (2, 1, 'medium'), (2, 0, 'medium'),
    (3, 11, 'low'), (3, 10.5, 'low'), (3, 50, 'low'),
    (3, 10, 'clear'), (3, 5, 'clear'), (3, 0, 'clear'),
]


def variants(role, value):
    # a few programs take the health code as an enum member of their own
    return [value, {'__enum__': value}] if role == 'health' else [value]


cases = [(f'Health {h}, {t} hours: {p.upper()}', {'health': h, 'hours': t}, p) for h, t, p in TABLE]
results, note = run_cases(path, ROLES, cases, judge, variants)
for name, _, _ in cases:
    report(name, results[name], note)
