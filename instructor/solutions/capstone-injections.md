# INSTRUCTOR ONLY — do not distribute

Answer key for the **Capstone — the four injectable issues**. Verified against
the sandbox contract and OpenCode 1.18.33 conventions (2026-09-28). The
known-good importer is [importer_solution.py](importer_solution.py) — reference
it; do not retype it.

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

---

## Capstone — the four injectable issues

Inject exactly one per pair into `sandbox/worktrees/orchestrated`, after Ex4,
ideally while learners are away from keyboards. All commands below run from
inside that worktree. If a pair has no working importer, first install the
known-good one:
`cp ../../../instructor/solutions/importer_solution.py src/panic_pantry/importer.py`
and confirm the suite is green before injecting.

> All four injections assume an importer equivalent to
> [importer_solution.py](importer_solution.py). If a learner's structure
> differs wildly, pick Injection C or D (they don't touch the importer).

### Injection A — approval status mishandled (implementation defect)

Make the importer classify by a local threshold — wrongly using `>= 20`, so
exactly-20% codes are misfiled as pending in the report:

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("src/panic_pantry/importer.py")
s = p.read_text()
old = """            else:
                if promo.status == "active":
                    report.created.append(code)
                else:
                    report.pending_approval.append(code)"""
new = """            else:
                if discount_pct >= 20:
                    report.pending_approval.append(code)
                else:
                    report.created.append(code)"""
assert old in s, "importer shape differs — choose injection C or D"
p.write_text(s.replace(old, new))
print("injected A")
EOF
```

- **Symptom:** four contract tests fail — `test_boundary_exactly_20_is_created_active`,
  `test_created_rows_in_file_order`, `test_above_20_is_pending_and_unusable_at_checkout`
  (pending list now wrongly includes MIDNIGHT20), and
  `test_clean_file_creates_active_promotions` (MIDNIGHT-SAVER at exactly 20%
  misfiled). Store status is still correct — only the report lies.
- **Expected diagnosis:** implementation defect — and specifically the
  reimplemented-policy smell: the importer compares against 20 itself instead
  of reading `promo.status`. (Sharp pairs also note the operator is wrong,
  `>= 20` vs the policy's strictly-above-20.)
- **Expected fix:** classify from `promo.status` returned by
  `create_promotion`; delete the local threshold entirely. Suite green after.
- **Reviewer should flag:** policy logic duplicated outside
  `PromotionService` (checklist item: approval bypass).

### Injection B — duplicate handling differs from contract (implementation defect)

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("src/panic_pantry/importer.py")
s = p.read_text()
old = """            except DuplicatePromotionError:
                report.skipped_duplicate.append(code)"""
new = """            except DuplicatePromotionError:
                report.errors.append((line, f"duplicate code: {code}"))"""
assert old in s, "importer shape differs — choose injection C or D"
p.write_text(s.replace(old, new))
print("injected B")
EOF
```

- **Symptom:** `test_in_file_duplicate_skipped_not_overwritten`,
  `test_pre_existing_duplicate_skipped_not_overwritten`,
  `test_second_run_is_idempotent`, and
  `test_malformed_rows_reported_with_line_numbers` (error-line list gains 7, 8)
  fail.
- **Expected diagnosis:** implementation defect vs the frozen contract —
  duplicates belong in `skipped_duplicate`, not `errors`; data was never at
  risk (the service refused the overwrite).
- **Expected fix:** restore the `skipped_duplicate.append(code)` handling.

### Injection C — out-of-scope file changed (boundary conflict)

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("src/panic_pantry/store.py")
s = p.read_text()
s = s.replace('"""', '"""\n# TODO(import-agent): tidy pricing helpers while here\n', 1)
p.write_text(s)
print("injected C")
EOF
```

- **Symptom:** full suite stays **green**. The tell is `git status` /
  `git diff`: `src/panic_pantry/store.py` modified, and no task card owns it.
- **Expected diagnosis:** boundary conflict — a writer left its scope. Green
  tests prove nothing here; the ownership map and diff are the evidence
  (the ML5 point: a green check is evidence, not a handoff — and only of what
  it covers).
- **Expected fix:** `git checkout -- src/panic_pantry/store.py`; note in
  integration-notes which control would have prevented it (permission scope or
  tighter card).

### Injection D — test asserts a stale signature (task/context gap)

Append a bad test to the learner's `tests/test_promo_import.py` (create the
file with the header block below if the pair never produced one):

```bash
cat >> tests/test_promo_import.py <<'EOF'


class StaleContractTests(unittest.TestCase):
    def test_import_uses_default_service(self):
        # stale assumption from an early draft: single-argument signature
        report = import_promotions(CLEAN_CSV)
        self.assertEqual(len(report.created), 6)
EOF
```

(If creating the file from scratch, first copy the import/skip scaffold from the
top of `tests/test_importer_contract.py`, keeping `CLEAN_CSV` defined, then
append the class above.)

- **Symptom:** `TypeError: import_promotions() missing 1 required positional
  argument: 'service'` — one failing test; everything else green.
- **Expected diagnosis:** task/context gap in the test deliverable — the test
  asserts a signature that predates the frozen contract
  (`import_promotions(csv_path, service)` per TICKET-001). The *test* is the
  defect; the importer must not be changed to appease it.
- **Expected fix:** correct or delete the stale test; re-run. Bonus points for
  pairs who check whether other tests share the stale assumption.

### Model five-line release note (for Injection A, shown at debrief)

```markdown
1. Changed behavior: promo CSV import now reports exactly-20% codes as active,
   matching the shop policy (above 20% requires approval; exactly 20% is active).
2. Tests run: python3 -m unittest discover -s tests -v — 33 tests, OK
   (23 starter suite + 10 added by this example pair's Ex4 test author; your
   pairs' totals will vary).
3. Review status: @reviewer flagged duplicated policy logic in the importer;
   fixed by classifying from the service-returned status; re-review clean.
4. Unresolved concern: reason strings for malformed rows are unstandardized
   (contract leaves them free); deferred with a ticket note.
5. Decision: GO for midnight — policy enforcement verified at service, report,
   and checkout layers; I own this call.
```

Score notes: full credit requires the classification step written *before* the
fix, evidence for lines 2–3 (real command output, real findings), and a line 4
that isn't "none" without justification.
