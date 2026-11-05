"""Group A, Part 1 -- shipping cost calculator. Prints one PASS/FAIL line per case."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe import find_student_file, probe, pick_function, build_args, numbers, report  # noqa: E402

RATES = {'A': (10, 15, 20), 'B': (15, 20, 25), 'C': (20, 25, 30)}
WEIGHTS = [(1, 0), (5, 0), (5.01, 1), (7.5, 1), (10, 1), (10.01, 2), (25, 2)]
ROLES = {'weight': r'weight|kg|^w$', 'zone': r'zone|dest|^z$'}

root = os.getcwd()
path = find_student_file(root, r'zone')
if not path:
    print('no shipping calculator found')
    sys.exit(2)

cases = [(w, z, RATES[z][t]) for z in 'ABC' for w, t in WEIGHTS]
info = probe(path)
choice = pick_function(info['functions'], ROLES, strict_name='shipping_cost')
results = {}
if choice:
    fn, found, pnames = choice
    calls = [build_args(ROLES, found, pnames, {'weight': w, 'zone': z}) for w, z, _ in cases]
    calls += [build_args(ROLES, found, pnames, {'weight': 7, 'zone': 'b'}),     # lowercase zone
              build_args(ROLES, found, pnames, {'weight': 7, 'zone': 'Z'})]     # invalid zone
    out = probe(path, fn, calls)['calls']
    for (w, z, exp), r in zip(cases, out):
        got = r['ret'] if isinstance(r['ret'], (int, float)) and not isinstance(r['ret'], bool) else None
        if got is None and isinstance(r['ret'], str) and numbers(r['ret']):
            got = numbers(r['ret'])[-1]
        if got is None and numbers(r['out']):
            got = numbers(r['out'])[-1]
        results[(w, z)] = (got is not None and abs(got - exp) < 0.005, f'got {got}' if r['err'] is None else r['err'])
    lc, bad = out[len(cases)], out[len(cases) + 1]
    exp_lc = RATES['B'][1]
    txt = ' '.join(str(x) for x in (lc['ret'], lc['out']))
    results['lowercase'] = (any(abs(n - exp_lc) < 0.005 for n in numbers(txt)), 'lowercase zone not accepted')
    txt = ' '.join(str(x) for x in (bad['ret'], bad['out']))
    results['invalid'] = (not any(n in (10, 15, 20, 25, 30) for n in numbers(txt) if n != 7),
                          'invalid zone produced a cost')
else:
    for w, z, exp in cases:
        results[(w, z)] = (False, 'no function taking weight and zone found')
    results['lowercase'] = (False, 'no function')
    results['invalid'] = (False, 'no function')

for w, z, exp in cases:
    ok, why = results[(w, z)]
    report(f'Zone {z} {w} kg costs ${exp}', ok, why)
report('Lowercase zone accepted', *results['lowercase'])
report('Invalid zone does not produce a cost', *results['invalid'])
