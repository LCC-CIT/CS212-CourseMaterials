"""Group A, Part 2 -- investment recommender. Tolerant of how the student takes input. One PASS/FAIL per combination."""
import itertools
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import find_student_file, probe, run_script, pick_function, build_args, report  # noqa: E402

PRODUCTS = {  # (horizon, risk) -> (needs one of, must not contain any of)
    # Keywords are partial on purpose ("corp" accepts a misspelled "Coporate"): spelling is a style matter.
    ('short', 'low'):  (['saving'], ['corp', 'coporate', 'bond', 'government', 'index', 'stock', 'diversified']),
    ('short', 'high'): (['corp', 'coporate', 'bond'], ['saving', 'government', 'index', 'stock', 'diversified']),
    ('long', 'low'):   (['government', 'index'], ['saving', 'corp', 'stock', 'diversified']),
    ('long', 'high'):  (['diversified', 'stock'], ['saving', 'corp', 'government', 'index']),
}
HORIZONS = {'short': [2, 'short', 'Short-Term', 'short term', 's', '1', 'Short'],
            'long':  [10, 'long', 'Long-Term', 'long term', 'l', '2', 'Long']}
RISKS = {'low': ['low', 'Low', 'LOW', 'l', '1'], 'high': ['high', 'High', 'HIGH', 'h', '2']}
ROLES = {'horizon': r'horizon|year|term|time|duration', 'risk': r'risk|toler'}


def right(text, combo):
    t = (text or '').lower()
    need, forbid = PRODUCTS[combo]
    return any(n in t for n in need) and not any(f in t for f in forbid)


root = os.getcwd()
path = find_student_file(root, r'horizon|invest|risk')
if not path:
    print('no recommender found')
    sys.exit(2)

info = probe(path)
choice = pick_function(info['functions'], ROLES)
mode = 'function' if choice else 'script'
combos = list(PRODUCTS)
results = {c: False for c in combos}
if choice:
    fn, found, pnames = choice
    for combo in combos:
        variants = list(itertools.product(HORIZONS[combo[0]], RISKS[combo[1]]))
        calls = [build_args(ROLES, found, pnames, {'horizon': h, 'risk': r}) for h, r in variants]
        for r in probe(path, fn, calls)['calls']:
            if right(f"{r['ret']} {r['out']}", combo):
                results[combo] = True
                break
if mode == 'script' or not any(results.values()):
    for combo in combos:
        if results[combo]:
            continue
        for h, r in itertools.product(HORIZONS[combo[0]], RISKS[combo[1]]):
            if any(right(run_script(path, f"{a}\n{b}\n{a}\n{b}\n"), combo) for a, b in ((h, r), (r, h))):
                results[combo] = True
                break

for (h, r), ok in results.items():
    report(f"{'Short-Term' if h == 'short' else 'Long-Term'} + {r.capitalize()} risk gives the right product", ok,
           f'tried {mode} mode' + (f'; load error {info["load_error"]}' if info['load_error'] else ''))
