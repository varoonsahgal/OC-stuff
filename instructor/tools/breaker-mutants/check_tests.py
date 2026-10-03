"""INSTRUCTOR ONLY — do not distribute.

Plant 8 realistic bugs in the known-good importer, one at a time, and show which
test modules catch each one. It backs Module 1's claim that the frozen contract
tests catch only 4 of 8, and it grades a Breaker's tests (Ex4, capstone).

Usage, from the pack root:
    python3 instructor/tools/breaker-mutants/check_tests.py <checkout> <test_module> [<test_module> ...]

Examples:
    python3 instructor/tools/breaker-mutants/check_tests.py sandbox/panic-pantry tests.test_importer_contract
    python3 instructor/tools/breaker-mutants/check_tests.py sandbox/worktrees/orchestrated \
        tests.test_importer_contract tests.test_promo_import

Each bug is generated from instructor/solutions/importer_solution.py, so the
mutants always match the reference solution. The checkout's own importer.py, if
any, is restored afterwards. Standard library only.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOLUTION = HERE.parent.parent / "solutions" / "importer_solution.py"

# name -> (what the bug does, text to find, replacement)
MUTANTS = {
    "local_threshold": (
        "classifies by discount_pct >= 20 itself (exactly-20 codes reported as pending)",
        '                if promo.status == "active":\n'
        "                    report.created.append(code)\n"
        "                else:\n"
        "                    report.pending_approval.append(code)",
        "                if discount_pct >= 20:\n"
        "                    report.pending_approval.append(code)\n"
        "                else:\n"
        "                    report.created.append(code)",
    ),
    "dup_as_error": (
        "reports duplicates as errors instead of skipped_duplicate",
        "            except DuplicatePromotionError:\n"
        "                report.skipped_duplicate.append(code)",
        "            except DuplicatePromotionError:\n"
        '                report.errors.append((line, f"duplicate code: {code}"))',
    ),
    "auto_approve": (
        "approves every pending code: FREE-ALL goes live",
        "                else:\n"
        "                    report.pending_approval.append(code)",
        "                else:\n"
        "                    service.approve(code)\n"
        "                    report.created.append(code)",
    ),
    "line_off_by_one": (
        "numbers the first data row 1 instead of 2",
        "            line = reader.line_num\n",
        "            line = reader.line_num - 1\n",
    ),
    "blank_reason": (
        'reports a blank row as "blank line" instead of "empty row"',
        'report.errors.append((line, "empty row"))',
        'report.errors.append((line, "blank line"))',
    ),
    "bad_header_still_imports": (
        "reports a wrong header but imports every row anyway",
        "            report.errors.append((1, \"missing or invalid header; expected 'code,discount_pct'\"))\n"
        "            return report",
        "            report.errors.append((1, \"missing or invalid header; expected 'code,discount_pct'\"))",
    ),
    "extra_columns_ok": (
        "accepts rows with 3+ columns",
        "            if len(row) != 2:\n",
        "            if len(row) < 2:\n",
    ),
    "fraction_rounds_down": (
        "accepts 20.9 as 20 instead of rejecting a non-integer",
        "                discount_pct = int(pct_raw)\n",
        "                discount_pct = int(float(pct_raw))\n",
    ),
}


def build_variants(dest):
    source = SOLUTION.read_text(encoding="utf-8")
    variants = {"correct": ("the reference solution: every module must pass", source)}
    for name, (desc, old, new) in MUTANTS.items():
        if source.count(old) != 1:
            sys.exit(f"mutant {name!r} no longer matches importer_solution.py; update MUTANTS")
        variants[name] = (desc, source.replace(old, new))
    for name, (_desc, code) in variants.items():
        (dest / f"{name}.py").write_text(code, encoding="utf-8")
    return variants


def clear_caches(checkout):
    for cache in checkout.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)


def summary(out):
    """(ran, skipped, last line) from unittest's own summary, or None if the module didn't load."""
    ran = re.findall(r"^Ran (\d+) tests? in", out, re.M)
    status = re.findall(r"^(OK|FAILED)\b(.*)$", out, re.M)
    if not ran or not status or "_FailedTest" in out:
        return None
    skipped = re.search(r"skipped=(\d+)", status[-1][1])
    return int(ran[-1]), int(skipped.group(1)) if skipped else 0, "".join(status[-1]).strip()


def run_module(checkout, module, seed, store):
    """Run one test module hermetically: fresh store from the seed, no stale caches, output buffered."""
    clear_caches(checkout)
    if seed.exists():
        shutil.copyfile(seed, store)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "-b", module],
            cwd=checkout, capture_output=True, text=True, timeout=120,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    s = summary(proc.stdout + proc.stderr)
    if s is None:
        return "LOAD ERROR"
    ran, skipped, last = s
    if last.startswith("FAILED"):
        return "CAUGHT"
    if ran == 0:
        return "no tests"
    if skipped == ran:
        return f"all skipped ({ran})"
    return "missed"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    checkout = Path(sys.argv[1]).resolve()
    modules = sys.argv[2:]
    target = checkout / "src" / "panic_pantry" / "importer.py"
    seed = checkout / "data" / "promotions.json.seed"
    store = checkout / "data" / "promotions.json"
    if not target.parent.is_dir():
        sys.exit(f"{checkout} doesn't look like a Panic Pantry checkout")

    saved_importer = target.read_bytes() if target.exists() else None
    saved_mode = target.stat().st_mode if target.exists() else None
    saved_store = store.read_bytes() if store.exists() else None
    width = max(max(len(m) for m in modules), len("FAILS on correct code!")) + 2
    print(f"{'variant':<26}" + "".join(f"{m:<{width}}" for m in modules) + "what the bug does")
    totals = {m: 0 for m in modules}
    gradable = {m: True for m in modules}
    try:
        with tempfile.TemporaryDirectory() as tmp:
            variants = build_variants(Path(tmp))
            for name, (desc, code) in variants.items():
                target.write_text(code, encoding="utf-8")
                row = []
                for m in modules:
                    verdict = run_module(checkout, m, seed, store)
                    if name == "correct":
                        if verdict != "missed":
                            gradable[m] = False
                        verdict = {"missed": "passes", "CAUGHT": "FAILS on correct code!"}.get(verdict, verdict)
                    elif verdict == "CAUGHT":
                        totals[m] += 1
                    row.append(verdict)
                print(f"{name:<26}" + "".join(f"{v:<{width}}" for v in row) + desc)
    finally:
        if saved_importer is None:
            target.unlink(missing_ok=True)
        else:
            target.write_bytes(saved_importer)
            os.chmod(target, saved_mode)
        if saved_store is None:
            store.unlink(missing_ok=True)
        else:
            store.write_bytes(saved_store)
        clear_caches(checkout)
    print()
    for m in modules:
        if gradable[m]:
            print(f"{m}: catches {totals[m]} of {len(MUTANTS)} planted bugs")
        else:
            print(f"{m}: can't grade. It doesn't pass on the correct importer, so its catches mean nothing. Fix the tests first.")


if __name__ == "__main__":
    main()
