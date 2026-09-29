# INSTRUCTOR ONLY — do not distribute

Complete answer key for every exercise, including the capstone injections.
Verified against the sandbox contract and OpenCode 1.18.33 conventions
(2026-09-28). The known-good importer is
[importer_solution.py](importer_solution.py) — reference it; do not retype it.

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.** Enforced in
`src/panic_pantry/promotions.py` → `PromotionService.create_promotion`
(threshold constant `APPROVAL_THRESHOLD_PCT = 20`, comparison is strictly `>`).

---

## Exercise 0 — The vague ticket

### Part A — expected discoveries from the vague-prompt plan

A typical plan for "Add a CSV importer for promo codes" silently decides most of
these. Learners should list at least three:

| Silent decision | What the repo actually says |
|---|---|
| CSV columns/format guessed | Ticket fixes `code,discount_pct`, header = line 1 |
| No mention of the approval policy | Above 20% → `pending_approval`; exactly 20% → `active` (promotions.py docstring + `create_promotion`) |
| Writes `data/promotions.json` directly or invents its own store | AGENTS.md forbids it; must go through `PromotionService.create_promotion` |
| Duplicates: overwrite, error, or skip? | Contract: `skipped_duplicate`, never overwrite (in-file and pre-existing) |
| Malformed rows: abort vs continue? | Report `(line, reason)` and continue; blank row reason is exactly `"empty row"` |
| Line numbering convention | 1-based, header is line 1, first data row is line 2 |
| Idempotency unaddressed | Second run creates nothing; everything previously created → `skipped_duplicate` |
| Missing header behavior | `(1, reason)`, nothing imported |
| New dependency (pandas etc.) proposed | stdlib only |

The teaching beat survives a "good" plan: use the recorded bad plan in
[fallback-traces.md](fallback-traces.md).

### Part B — expected answer

Policy enforced in `src/panic_pantry/promotions.py`,
`PromotionService.create_promotion` (strictly-greater-than-20 check sets
`pending_approval`); documented in the module docstring and AGENTS.md
"Boundaries." Checkout enforcement: `store.apply_promotion` raises
`PromotionNotActiveError` for non-active codes.

### Part C — sample baseline outcome (typical, not guaranteed)

With the full ticket, a competent model usually produces a near-correct importer
in one to three iterations. Typical scorecard from rehearsal runs:

| Metric | Typical single-agent value |
|---|---|
| Elapsed | 10–15 min (often hits the stop) |
| Contract tests | 6–9 of 9 passing at stop |
| Whole suite | frequently 1–3 failures at stop |
| Policy | usually correct (service enforces it) — but check the *report* classification |
| Interventions | 1–3 |
| Files changed | should be only `src/panic_pantry/importer.py` |

Most common near-misses to look for in learner diffs:
1. **Line numbers off by one** — using `enumerate(reader)` from 0 or 1 instead
   of `csv.reader.line_num` (fails `test_malformed_rows_reported_with_line_numbers`).
2. **Blank-row reason** not the literal `"empty row"` / blank row treated as
   column-count error (line 12 of the messy fixture).
3. **Classifying by threshold instead of status** — deciding
   created vs pending by comparing `discount_pct > 20` locally instead of
   reading `promo.status` returned by the service. Works today, but it
   *reimplements* the policy (contract item 7); the reviewer should flag it.
4. **Missing-header case** imports the row anyway (fails
   `test_missing_header_reported_and_nothing_imported`).

Known-good result: with [importer_solution.py](importer_solution.py) in place,
`python3 -m unittest discover -s tests -v` → **23 tests, OK, 0 skipped**.

---

## Exercise 1 — Task surgery: model artifacts

### Model `workshop/plan.md`

```markdown
# Plan — TICKET-001 CSV promo importer (Midnight Crunch Drop)

## Frozen contract
As written in tickets/TICKET-001.md (copied, not paraphrased):
`import_promotions(csv_path, service) -> ImportReport` with fields
created / pending_approval / skipped_duplicate / errors[(line, reason)];
1-based lines, header = line 1; blank row → error "empty row"; missing/wrong
header → (1, reason) and nothing imported; duplicates skipped, never
overwritten; idempotent re-runs; all creation via
PromotionService.create_promotion (policy: above 20% requires approval,
exactly 20% is active); stdlib only.

## Tasks
| ID | Owner | Deliverable | Acceptance check |
|---|---|---|---|
| T0 contract-freeze | me (primary) | contract confirmed + pasted here | this file reviewed before launch |
| T1 csv_parser | @implementer | src/panic_pantry/importer.py | python3 -m unittest tests.test_importer_contract -v |
| T2 import_tests | @implementer (2nd delegation) | tests/test_promo_import.py | tests collect and express the contract's edge cases |
| T3 integration | me (primary) | workshop/integration-notes.md + merged, reviewed diff | python3 -m unittest discover -s tests -v; @reviewer findings dispositioned |

## Dependencies / critical path
T0 → (T1 ∥ T2) → T3. Critical path: T0 → T1 → T3 (T1 is the largest task and
T3 cannot finish without it). T1 and T2 are parallel ONLY after T0: both read
the contract; neither reads the other's file.

## Keep vs delegate
T0 and T3 stay with the primary: freezing the contract and owning integration
are judgment calls with the whole-repo context; delegation cost exceeds benefit.
T1/T2 are delegated: distinct outputs, standalone context, checkable results.

## Context each child needs
- T1: task card, tickets/TICKET-001.md, promotions.py + models.py signatures,
  fixture paths, test command. NOT: store.py internals, workshop files.
- T2: task card, ticket contract, fixtures/promos_messy.expected.md, test
  command. NOT: the importer's implementation (tests target the contract).
```

### Model card — `workshop/cards/csv_parser.md`

```markdown
## T1 — csv_parser: implement the TICKET-001 importer
Outcome: src/panic_pantry/importer.py defining ImportReport and
import_promotions(csv_path, service) -> ImportReport, satisfying every
acceptance criterion in tickets/TICKET-001.md.
Why this task is separate: bounded, contract-checked implementation with a
distinct output file; frees the primary for integration.
Inputs and source paths: tickets/TICKET-001.md; src/panic_pantry/promotions.py
(create_promotion, DuplicatePromotionError, InvalidPromotionError);
src/panic_pantry/models.py (code format, discount range);
fixtures/promos_clean.csv; fixtures/promos_messy.csv.
Contract: report fields created/pending_approval/skipped_duplicate/errors in
file order; 1-based line numbers with header = line 1; blank row → error
"empty row"; missing/wrong header → (1, reason) and nothing imported; classify
created vs pending from the status the service returns — never compare against
20 locally; policy is service-owned: above 20% requires approval, exactly 20%
is active.
In scope: src/panic_pantry/importer.py (new file) only.
Out of scope: tests/, fixtures/, data/, scripts/, all other src files,
AGENTS.md; never write data/promotions.json directly; no new dependencies.
Dependencies: T0 contract-freeze.
Acceptance checks: python3 -m unittest tests.test_importer_contract -v (all 9
pass, none skipped); python3 -m unittest discover -s tests -v (whole suite OK).
Permissions/model: edit allowed for the in-scope file; bash for the test
command; classroom-pinned model, default effort.
Return format: summary; changed paths; exact commands run + pass/fail;
assumptions made; open questions.
```

### Model card — `workshop/cards/import_tests.md`

```markdown
## T2 — import_tests: contract tests in the team's own words
Outcome: tests/test_promo_import.py — unittest cases expressing TICKET-001's
edge cases against the frozen interface (importable whether or not the importer
exists yet: skip cleanly on ImportError like tests/test_importer_contract.py does).
Why this task is separate: independent deliverable written from the contract,
deliberately NOT from the implementation; parallel to T1 after the freeze.
Inputs and source paths: tickets/TICKET-001.md;
fixtures/promos_messy.expected.md; fixtures/promos_clean.csv;
tests/test_importer_contract.py (READ ONLY, as a style/skip-pattern reference);
data/promotions.json.seed.
Contract: same as T1; must cover at minimum — exactly 20% → active; 21+ →
pending_approval and rejected at checkout; in-file and pre-existing duplicates
skipped without overwrite; error line numbers 1-based; blank row reason
"empty row"; idempotent second run; missing header → (1, reason), nothing
imported.
In scope: tests/test_promo_import.py (new file) only.
Out of scope: tests/test_importer_contract.py (frozen), tests/test_promotions.py,
src/, fixtures/, data/, scripts/. Tests must be deterministic and offline.
Dependencies: T0 contract-freeze. NOT T1 — do not read the importer's code.
Acceptance checks: python3 -m unittest tests.test_promo_import -v collects and
runs (skips cleanly if importer absent; passes against the known-good importer).
Permissions/model: edit allowed for the in-scope file; bash for the test
command; a faster/cheaper model is appropriate — the contract is written down.
Return format: summary; changed paths; commands run + result; which contract
clauses are covered by which test; uncertainties.
```

Grading Ex1: pass if (a) policy stated as above-20%-requires-approval /
exactly-20-active, (b) every task has owner+deliverable+executable check,
(c) card scopes are disjoint, (d) out-of-scope lists the frozen files,
(e) critical path named with a reason.

---

## Exercise 2 — Agent crew

### Reviewer agent file

The exact known-good file is [reviewer-agent.md](reviewer-agent.md); learners
should produce something equivalent at `.opencode/agents/reviewer.md`.
Pass bar: `description` present; `mode: subagent`; `permission` (not deprecated
`tools:`) with `edit: deny` and bash denied or pattern-restricted (map order:
`"*": deny` first — last matching rule wins); checklist covers approval bypass,
duplicates, row reporting, missing tests; fixed return format.

### Implementer agent file (model answer)

```markdown
---
description: Implements exactly one supplied task card in the Panic Pantry sandbox, then reports changed paths and checks run
mode: subagent
temperature: 0.2
permission:
  read: allow
  edit: allow
  webfetch: deny
  bash:
    "*": deny
    "python3 -m unittest*": allow
    "git status": allow
    "git diff*": allow
---
You implement exactly one task card supplied in the delegation message.

Rules:
- Change only the files the card lists as in scope. If the card and reality
  conflict, stop and report; do not improvise.
- All promotion creation goes through PromotionService.create_promotion.
  Policy: discounts above 20% require approval; exactly 20% is active. Never
  reimplement or bypass this.
- Standard library only. Run the card's acceptance command before returning.

Return format: summary (≤5 lines); changed paths; exact commands run with
pass/fail; assumptions; open questions.
```

### Expected denial behavior (step 3)

When the learner sends `@reviewer Please add a clarifying comment to
src/panic_pantry/store.py`, OpenCode blocks the edit tool at the permission
layer — the UI shows the edit attempt being **denied by permission
configuration** (not a polite refusal in prose). Acceptable evidence: the
denied tool call visible in the session. If the agent merely *says* it won't
edit without attempting, have the learner insist ("attempt the edit using your
edit tool") so the configured denial actually fires once.

### Expected investigation packet (step 4) — model reviewer report

```text
Findings — pre-implementation review for TICKET-001

Riskiest contract violations for an importer:
1. HIGH — Policy bypass via direct store writes. Writing data/promotions.json
   or setting status locally would let >20% codes activate. Forbidden by
   AGENTS.md ("Boundaries") and ticket item 7. Caught by:
   test_above_20_is_pending_and_unusable_at_checkout
   (tests/test_importer_contract.py:62).
2. HIGH — Local threshold reimplementation. Classifying created vs pending by
   comparing discount_pct > 20 in the importer duplicates the policy owned by
   promotions.py:APPROVAL_THRESHOLD_PCT; a future threshold change would
   silently desync. Partially caught by the same test; primarily a review catch.
3. MEDIUM — Line-number drift. Contract says 1-based with header = line 1;
   naive enumerate() gives 0- or data-row-based numbers. Caught by:
   test_malformed_rows_reported_with_line_numbers (expects [9,10,11,12,13,14]).

Ambiguity found: the ticket fixes the blank-row reason ("empty row") but not
other reason strings — tests assert non-empty strings only (contract test
lines 80–83), so exact wording is implementer's choice.
Uncertainties: none blocking. No files edited (edit permission is denied).
```

---

## Exercise 3 — Model routing

Filled comparison record — **RECORDED EXAMPLE, NOT LIVE**: from an instructor
rehearsal on 2026-09-26; model IDs anonymized because the live classroom
catalog must come from `/models` on the day. Use it to show the *shape* of a
good record and as the scoring fallback with
[fallback-traces.md](fallback-traces.md).

```markdown
# workshop/model-comparison.md — RECORDED EXAMPLE (not live)

Configurations (as displayed in /models on rehearsal day):
- FAST  = opencode/<free-labeled-small-model-id>  (free tier; may train on data — varies per model)
- STRONG = <provider>/<large-reasoning-model>  (paid)

## Task A — messy-fixture disposition (score vs fixtures/promos_messy.expected.md, /13)
| Run | Model | Time | Score | Notes |
|---|---|---|---|---|
| A-1 | FAST | 41 s | 12/13 | missed line 8: called WELCOME10 "created" — didn't check the seed |
| A-2 | STRONG | 2 m 10 s | 13/13 | also volunteered the idempotency note (unasked) |

## Task B — plan risk review (rubric /6)
| Run | Model | Time | Score | Notes |
|---|---|---|---|---|
| B-1 | FAST | 55 s | 3/6 | generic risks ("tests might be incomplete"), one wrong path cited |
| B-2 | STRONG | 3 m 05 s | 6/6 | caught local-threshold-reimplementation risk with file:line evidence |

## Cost/tokens (opencode stats)
A-1: 4.1k tok / $0.00 · A-2: 11.8k tok / $0.09 · B-1: 5.0k tok / $0.00 ·
B-2: 19.3k tok / $0.16. (Rehearsal values; record "unavailable" if not shown.)

## Routing decision
Bounded, contract-backed work (Task A shape) → FAST with the objective check;
the 1/13 miss was caught by the check, cost of failure ≈ zero. Ambiguous review
(Task B shape) → STRONG; FAST's misses were exactly the expensive-to-detect
kind. Revisit if FAST's Task-B rubric ever reaches 5/6 on two consecutive runs.
```

Scoring keys for Task A disputes: line 3 `MIDNIGHT20,20` → created-active
(exactly 20% needs no approval); line 8 `WELCOME10,10` → skipped_duplicate
(seeded); lines 9–14 errors (missing column; non-integer; lowercase code;
empty row; 0 out of range; 101 out of range). Full table:
`sandbox/panic-pantry/fixtures/promos_messy.expected.md`.

---

## Exercise 4 — Orchestrated run

### Integration checklist (what a passing learner did)

- [ ] Contract confirmed frozen (plan.md/ticket re-read) before first delegation.
- [ ] Same model/effort as Ex0 set via `/models` before the window.
- [ ] Delegations carried the full card text (fresh child context).
- [ ] The tests-card child session was created by the **primary via the Task
      tool** (governed by `permission.task`) — the learner instructed
      "Delegate the import_tests task card to the appropriate subagent"
      rather than @-mentioning; verify in the session tree.
- [ ] `.opencode/agents/implementer.md` carries an explicit `model:` line with
      a `/models` catalog ID (the learner's Ex3 routing choice — equal to the
      Ex0 pinned model/effort for the matched run), and that ID appears in the
      run record.
- [ ] `git status` shows exactly: `src/panic_pantry/importer.py` (new),
      `tests/test_promo_import.py` (new), `workshop/integration-notes.md` (new),
      plus copied `.opencode/agents/*` — nothing else. Any other change =
      boundary violation to disposition.
- [ ] No two writers on one file (compare status output to the ownership map).
- [ ] `python3 -m unittest discover -s tests -v` run by the learner post-merge;
      with a correct importer and valid new tests: **23+ tests** (23 from the
      starter suite + however many your test author added), OK.
- [ ] `@reviewer` findings collected; each fixed / accepted / deferred in
      `workshop/integration-notes.md`.
- [ ] Scorecard includes integration/rework minutes and a modest interpretation.

### Expected worktree states at end of Ex4

| Worktree | Branch | State |
|---|---|---|
| `sandbox/worktrees/single-agent` | `single-agent` | Ex0 baseline: importer (possibly incomplete) + captured diff; untouched since Ex0 |
| `sandbox/worktrees/orchestrated` | `orchestrated` | importer + `tests/test_promo_import.py` + `workshop/integration-notes.md` + copied agents/cards |
| `sandbox/panic-pantry` (main) | `main` | Ex1–Ex3 artifacts only: `workshop/plan.md`, `workshop/cards/*`, `workshop/model-comparison.md`, `.opencode/agents/*`; **no importer** |

Both worktrees still at tag `starter` ancestry — verify with
`git log --oneline -1` matching in both before crediting the comparison.

### Typical honest comparison result

Orchestrated runs usually show: equal-or-better contract-test coverage, an
extra test file the baseline never wrote, more total tokens (two child sessions
+ reviewer), and nonzero integration minutes the baseline didn't have. Neither
condition "wins" universally — say so. The decomposable importer flatters
orchestration; a one-file bug fix would not.

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
