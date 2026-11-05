"""
probe.py -- shared helpers for the Lab 01 Group A checks (check_shipping.py, check_recommend.py).

The students were not told how their programs take input or print results, so these checks
are deliberately tolerant. A student's file is run in a child process (a crash or a
call to input() can't take the checker down) and is exercised either way it might be built:
  * function mode  -- the file defines a function with the right parameters; call it directly
  * script mode    -- the file reads input() / prints; feed it stdin in several plausible styles
A case passes when ANY of those attempts produces the right answer.
"""
import glob
import inspect
import json
import os
import re
import subprocess
import sys

CHILD = r'''
import sys, os, io, json, inspect, contextlib, importlib.util
path, payload = sys.argv[1], json.loads(sys.argv[2])
real_out = sys.stdout
sys.path.insert(0, os.path.dirname(path))
os.chdir(os.path.dirname(path))
def conv(a):
    if isinstance(a, dict) and "__enum__" in a:   # the module's enum member with this value, if it has one
        import enum
        for v in list(vars(sys.modules["student_mod"]).values()):
            if isinstance(v, type) and issubclass(v, enum.Enum):
                for m in v:
                    if m.value == a["__enum__"]:
                        return m
        return a["__enum__"]
    if isinstance(a, dict) and "__obj__" in a:
        import types
        return types.SimpleNamespace(**a["__obj__"])
    return a
def run(fn):
    buf = io.StringIO()
    err = None
    ret = None
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        try:
            ret = fn()
        except SystemExit:
            pass
        except BaseException as e:
            err = type(e).__name__
    return ret, buf.getvalue(), err
spec = importlib.util.spec_from_file_location("student_mod", path)
mod = importlib.util.module_from_spec(spec)
_, _, load_err = run(lambda: (sys.modules.__setitem__("student_mod", mod), spec.loader.exec_module(mod)))
funcs = []
for name, f in vars(mod).items():
    if inspect.isfunction(f) and f.__module__ == "student_mod":
        try:
            ps = [(p.name, p.default is not inspect.Parameter.empty, p.kind.name) for p in inspect.signature(f).parameters.values()]
        except Exception:
            continue
        funcs.append((name, ps))
result = {"load_error": load_err, "functions": funcs, "calls": []}
if payload.get("calls"):
    f = getattr(mod, payload["function"], None)
    for args in payload["calls"]:
        if isinstance(args, dict):
            kw = {k: conv(v) for k, v in args.items()}
            ret, out, err = run(lambda: f(**kw))
        else:
            pos = [conv(v) for v in args]
            ret, out, err = run(lambda: f(*pos))
        try:
            json.dumps(ret)
        except Exception:
            ret = repr(ret)
        result["calls"].append({"ret": ret, "out": out, "err": err})
real_out.write("\n@@RESULT@@" + json.dumps(result))
'''


def find_student_file(root, kind_regex, skip_regex=r'(^|[\\/_.-])(test|tests|check|grader_checks)([\\/_.-]|$)'):
    """Return the student's .py (or .ipynb) file whose text matches kind_regex; the biggest match wins."""
    best, best_size = None, -1
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ('.venv', '__pycache__', '__MACOSX', '.git', 'node_modules', 'grader_checks')]
        for f in files:
            if not f.endswith('.py'):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root)
            if re.search(skip_regex, rel, re.I):
                continue
            try:
                text = open(full, errors='replace').read()
            except OSError:
                continue
            if re.search(kind_regex, text, re.I) and len(text) > best_size:
                best, best_size = full, len(text)
    return best


def probe(path, function=None, calls=None, timeout=20):
    payload = {"function": function, "calls": calls or []}
    try:
        p = subprocess.run([sys.executable, '-c', CHILD, path, json.dumps(payload)], stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"load_error": "Timeout", "functions": [], "calls": []}
    m = p.stdout.rsplit('@@RESULT@@', 1)
    if len(m) != 2:
        return {"load_error": "NoResult", "functions": [], "calls": []}
    return json.loads(m[1])


def run_script(path, stdin_text, timeout=6):
    try:
        p = subprocess.run([sys.executable, path], input=stdin_text, capture_output=True, text=True,
                           timeout=timeout, cwd=os.path.dirname(path))
        return p.stdout
    except subprocess.TimeoutExpired as e:
        return (e.stdout or b'').decode('utf-8', 'replace') if isinstance(e.stdout, bytes) else (e.stdout or '')


def strict_only(functions, strict_name):
    """Strict mode (environment variable LAB_STRICT=1): only the function named in the lab instructions counts."""
    if strict_name and os.environ.get('LAB_STRICT'):
        return [f for f in functions if f[0] == strict_name]
    return functions


def pick_function(functions, roles, name_hint=r'ship|cost|calc|rate|recommend|product|invest|advice|suggest|get_', strict_name=None):
    """roles: {role: regex}. Return (function name, {role: param name}) for the best candidate."""
    best = None
    for name, params in strict_only(functions, strict_name):
        pnames = [p[0] for p in params]
        found = {}
        for role, rx in roles.items():
            for pn in pnames:
                if re.search(rx, pn, re.I) and pn not in found.values():
                    found[role] = pn
                    break
        if len(found) < len(roles) and len(pnames) < len(roles):
            continue
        score = len(found) * 10 + (3 if re.search(name_hint, name, re.I) else 0)
        if best is None or score > best[0]:
            best = (score, name, found, pnames)
    if not best:
        return None
    return best[1], best[2], best[3]


def build_args(roles, found, pnames, values):
    """values: {role: value}. Bind by parameter name when possible, else by position in role order."""
    if len(found) == len(roles):
        args = {found[r]: values[r] for r in roles}
        for pn in pnames:                       # extra parameters (e.g. an is_valid flag)
            args.setdefault(pn, True)
        return args
    return [values[r] for r in roles]


def numbers(text):
    return [float(x.replace(',', '')) for x in re.findall(r'-?\d[\d,]*\.?\d*', text or '')]


def report(name, ok, why=''):
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" ({why})" if why and not ok else ''))


def candidate_functions(functions, roles):
    """Every function whose parameters fit all roles (bound by name, else by count), best name first."""
    out = []
    for name, params in functions:
        pnames = [p[0] for p in params]
        found = {}
        for role, rx in roles.items():
            for pn in pnames:
                if re.search(rx, pn, re.I) and pn not in found.values():
                    found[role] = pn
                    break
        if len(found) == len(roles) or len(pnames) == len(roles):
            hint = 1 if re.search(r'recommend|rating|rate|status|alert|priority|check|compat|room|get_', name, re.I) else 0
            out.append((-hint, name, found, pnames))
    return [(n, f, p) for _, n, f, p in sorted(out, key=lambda t: t[0])]


def run_cases(path, roles, cases, judge, variants=None, object_attrs=None, strict_name=None):
    """
    Try the student's code on each case; a case passes when ANY attempt is judged right.
      roles    {role: param-name regex}, e.g. {'speed': r'speed', 'strength': r'strength'}
      cases    [(name, {role: value}, expected)]
      judge    judge(ret, out, expected) -> bool, where ret is the return value and out what was printed
      variants variants(role, value) -> alternative spellings of an input (default: just the value)
      object_attrs  {role: [attribute names]}: also try a one-parameter function given an object with those attributes
      strict_name   the function name the lab instructions require; with LAB_STRICT=1 only that function is
                    called, with the inputs exactly as given (no alternative spellings, no objects)
    Returns ({case name: bool}, note) -- note explains a total failure to find anything callable.
    """
    import itertools
    info = probe(path)
    results = {name: False for name, _, _ in cases}
    if strict_name and os.environ.get('LAB_STRICT'):
        info['functions'] = strict_only(info['functions'], strict_name)
        variants, object_attrs = None, None
    cands = candidate_functions(info['functions'], roles)
    one_param = [(n, p) for n, params in info['functions'] for p in [[x[0] for x in params]] if len(p) == 1] if object_attrs else []
    if not cands and not one_param:
        return results, ('program did not load (%s)' % info['load_error']) if info['load_error'] else 'no function taking these inputs was found'
    attempts = []   # (function name, args, case name, expected)
    for name, values, expected in cases:
        alts = [list((variants(r, values[r]) if variants else [values[r]])) for r in roles]
        for combo in itertools.product(*alts):
            vals = dict(zip(roles, combo))
            for fn, found, pnames in cands:
                if len(found) == len(roles):
                    args = {found[r]: vals[r] for r in roles}
                    for pn in pnames:
                        args.setdefault(pn, True)
                else:
                    args = [vals[r] for r in roles]
                attempts.append((fn, args, name, expected))
            if object_attrs:
                attrs = {a: vals[r] for r, names in object_attrs.items() for a in names}
                for fn, _ in one_param:
                    attempts.append((fn, [{'__obj__': attrs}], name, expected))
    by_fn = {}
    for a in attempts:
        by_fn.setdefault(a[0], []).append(a)
    for fn, group in by_fn.items():
        outs = probe(path, fn, [g[1] for g in group])['calls']
        for (_, _, name, expected), r in zip(group, outs):
            if not results[name] and r['err'] is None and judge(r['ret'], r['out'], expected):
                results[name] = True
    return results, ''


def words(ret, out):
    return ('%s %s' % (ret if ret is not None else '', out or '')).lower()
