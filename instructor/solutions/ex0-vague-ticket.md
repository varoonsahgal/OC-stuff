# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 0 — The baseline** (Module 0, 25 min: warm-up 8, run 15, score 2). Verified against the sandbox
contract and OpenCode 1.18.33 conventions (2026-09-28). The known-good importer
is [importer_solution.py](importer_solution.py) — reference it; do not retype it.

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.** Enforced in
`src/panic_pantry/promotions.py` → `PromotionService.create_promotion`
(threshold constant `APPROVAL_THRESHOLD_PCT = 20`, comparison is strictly `>`).

---

## Exercise 0 — The single-agent baseline

### Step 1 (warm-up) — what learners should write down

The handout asks two questions: where the plan's rules came from (prompt,
`AGENTS.md`, or the ticket) and where the 20% rule is enforced (answer below).
At the debrief, push one step further with: "what did it decide that no file
told it?" A typical plan for "Add a CSV importer for promo codes" silently
decides several of these:

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

### Step 3 — reading `bash scripts/score.sh`

Learners copy four rows from `score.sh` into the Module 0 column of
`workshop/scorecard.md` and fill the rest by hand (model + variant,
interventions, elapsed, tokens/cost or "unavailable").

What the rows look like, so you can sanity-check a learner's sheet:

| Situation | Contract tests | Policy source check |
|---|---|---|
| No importer | `0/9 (SKIPPED: …counts as 0)` | `n/a` |
| `import_promotions` misnamed | `0/9 (SKIPPED: …counts as 0)` | still scanned |
| Importer has a syntax error | `0/9 (ERROR: … in src/panic_pantry/importer.py line N)` | still scanned |
| Known-good importer | `9/9 (OK)` | `nothing flagged` |
| Near-miss 3 above (`discount_pct > 20` decides the report) | often 9/9 | `CHECK BY EYE` on that line: a criterion-7 violation even when every test passes |

"Files changed" should list only `src/panic_pantry/importer.py` (Builder's
file). If `tests/test_promo_import.py` shows up, it's labeled "reserved for the
Ex4 Breaker": the agent added scope the ticket didn't ask for.

**Level up L0.1 (agent grades itself):** there's no fixed answer. The point is
the gap between the agent's self-rating and `score.sh`, whichever way it
goes. Use it to open Module 2's "it grades its own homework".
