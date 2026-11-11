"""Run every program in the course and report which ones fail.

    python tests/run_all.py              # run everything
    python tests/run_all.py u06 u07      # only units whose folder starts so
    python tests/run_all.py --save OUT   # also save each program's output

Python programs always run. The Prolog (.pl) and Lisp (.lisp) programs of
Unit 14 run only if SWI-Prolog (swipl) or SBCL (sbcl) is installed.
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"search.py", "resolution.py"}          # imported, not run
args = sys.argv[1:]
save = None
if "--save" in args:
    i = args.index("--save")
    save = Path(args[i + 1]).resolve()
    del args[i:i + 2]


def command(prog):
    if prog.suffix == ".py":
        return [sys.executable, prog.name]
    if prog.suffix == ".pl" and shutil.which("swipl"):
        return ["swipl", "-q", "-g", "main", "-t", "halt", prog.name]
    if prog.suffix == ".lisp" and shutil.which("sbcl"):
        return ["sbcl", "--script", prog.name]
    return None


env = dict(os.environ, MPLBACKEND="Agg", PYTHONHASHSEED="0")
failed, skipped, n = [], [], 0
for unit in sorted(ROOT.glob("u[0-9][0-9]-*")):
    if args and not any(unit.name.startswith(a) for a in args):
        continue
    for prog in sorted(unit.iterdir()):
        if prog.suffix not in (".py", ".pl", ".lisp") or \
                prog.name in MODULES:
            continue
        cmd = command(prog)
        if cmd is None:
            skipped.append(f"{unit.name}/{prog.name}")
            continue
        n += 1
        t0 = time.time()
        try:
            r = subprocess.run(cmd, cwd=unit, env=env, capture_output=True,
                               text=True, timeout=600)
            ok, out = r.returncode == 0, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            ok, out = False, "timed out"
        print(f"{'PASS' if ok else 'FAIL'}  {unit.name}/{prog.name}"
              f"  ({time.time() - t0:.1f} s)", flush=True)
        if not ok:
            failed.append(f"{unit.name}/{prog.name}")
            print(out[-2000:])
        elif save:
            dest = save / unit.name
            dest.mkdir(parents=True, exist_ok=True)
            (dest / (prog.name + ".txt")).write_text(r.stdout)
for s in skipped:
    print(f"SKIP  {s}  (install swipl or sbcl to run it)")
print(f"\n{n - len(failed)} of {n} programs passed")
sys.exit(1 if failed else 0)
