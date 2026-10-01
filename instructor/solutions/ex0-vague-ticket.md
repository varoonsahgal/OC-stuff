# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 0 — The single-agent baseline**. Verified against the sandbox
contract and OpenCode 1.18.33 conventions (2026-09-28). The known-good importer
is [importer_solution.py](importer_solution.py) — reference it; do not retype it.

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.** Enforced in
`src/panic_pantry/promotions.py` → `PromotionService.create_promotion`
(threshold constant `APPROVAL_THRESHOLD_PCT = 20`, comparison is strictly `>`).

---

## Exercise 0 — The single-agent baseline

### Step 1 (warm-up) — expected discoveries from the vague-prompt plan

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

### Step 1 (warm-up) — expected enforcement answer

Policy enforced in `src/panic_pantry/promotions.py`,
`PromotionService.create_promotion` (strictly-greater-than-20 check sets
`pending_approval`); documented in the module docstring and AGENTS.md
"Boundaries." Checkout enforcement: `store.apply_promotion` raises
`PromotionNotActiveError` for non-active codes.

### Step 2 — sample baseline outcome (typical, not guaranteed)

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
