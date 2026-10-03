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


def run_module(checkout, module):
    clear_caches(checkout)
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", module],
        cwd=checkout, capture_output=True, text=True, timeout=120,
    )
    out = proc.stdout + proc.stderr
    status = [l for l in out.splitlines() if l.startswith(("OK", "FAILED"))]
    last = status[-1] if status else ""
    ran = next((l.split()[1] for l in out.splitlines() if l.startswith("Ran ")), "0")
    if last.startswith("FAILED") or (not last and "Error" in out):
        return "CAUGHT"
    if "skipped=" in last and " ok" not in out:
        return f"skipped ({ran})" if ran != "0" else "skipped"
    if last.startswith("OK"):
        return "missed" if ran != "0" else "no tests"
    return "no result"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    checkout = Path(sys.argv[1]).resolve()
    modules = sys.argv[2:]
    target = checkout / "src" / "panic_pantry" / "importer.py"
    if not target.parent.is_dir():
        sys.exit(f"{checkout} doesn't look like a Panic Pantry checkout")

    backup = target.read_bytes() if target.exists() else None
    width = max(len(m) for m in modules) + 2
    print(f"{'variant':<26}" + "".join(f"{m:<{width}}" for m in modules) + "what the bug does")
    totals = {m: 0 for m in modules}
    try:
        with tempfile.TemporaryDirectory() as tmp:
            variants = build_variants(Path(tmp))
            for name, (desc, _code) in variants.items():
                shutil.copy(Path(tmp) / f"{name}.py", target)
                row = []
                for m in modules:
                    verdict = run_module(checkout, m)
                    if name == "correct":
                        verdict = {"CAUGHT": "FAILS on correct code!", "missed": "passes"}.get(verdict, verdict)
                    if name != "correct" and verdict == "CAUGHT":
                        totals[m] += 1
                    row.append(verdict)
                print(f"{name:<26}" + "".join(f"{v:<{width}}" for v in row) + desc)
    finally:
        if backup is None:
            target.unlink(missing_ok=True)
        else:
            target.write_bytes(backup)
        clear_caches(checkout)
    print()
    for m in modules:
        print(f"{m}: catches {totals[m]} of {len(MUTANTS)} planted bugs")


if __name__ == "__main__":
    main()
