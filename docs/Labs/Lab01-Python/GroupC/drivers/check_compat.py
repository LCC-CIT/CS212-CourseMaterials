"""Group C, Part 1 -- PC component compatibility checker. Prints one PASS/FAIL line per case."""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import find_student_file, run_cases, words, report  # noqa: E402

ROLES = {'socket': r'socket|cpu|processor', 'ram': r'ram|memory'}


def judge(ret, out, expected):
    if isinstance(ret, bool) and not (out or '').strip():
        return ret == (expected == 'compatible')
    t = words(ret, out)
    incompatible = bool(re.search(r'incompatible|not compatible|un-?compatible', t))
    compatible = bool(re.search(r'(?<!in)(?<!not )(?<!un)compatible', t))
    return incompatible if expected == 'incompatible' else (compatible and not incompatible)


root = os.getcwd()
path = find_student_file(root, r'socket|ddr')
if not path:
    print('no compatibility checker found')
    sys.exit(2)

TABLE = [
    ('LGA1700', 'DDR5', 'compatible'), ('LGA1700', 'DDR4', 'incompatible'), ('LGA1700', 'DDR3', 'incompatible'),
    ('AM4', 'DDR4', 'compatible'), ('AM4', 'DDR5', 'incompatible'), ('AM4', 'DDR3', 'incompatible'),
    ('AM5', 'DDR5', 'incompatible'), ('AM5', 'DDR4', 'incompatible'), ('Other', 'DDR5', 'incompatible'),
    ('am4', 'ddr4', 'compatible'), ('lga1700', 'ddr5', 'compatible'),
]
cases = [(f'{s} with {r} is {e.capitalize()}', {'socket': s, 'ram': r}, e) for s, r, e in TABLE]
results, note = run_cases(path, ROLES, cases, judge)
for name, _, _ in cases:
    report(name, results[name], note)
