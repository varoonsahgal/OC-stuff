# INSTRUCTOR ONLY — do not distribute

Deterministic fallback transcripts. All are **RECORDED** — Traces 1–2 captured
during instructor rehearsal (2026-09-26, OpenCode 1.18.33), Trace 3 on a V1
build with an experimental flag (see its header); all lightly trimmed for
class use. Present them as recordings, never as live output. Traces 1–3 predate the
Module 1 rewrite, so they use the old card names (`csv_parser`, `import_tests`,
"test author"); today those are `builder.md`, `breaker.md` and "the Breaker". Use them when a
live model behaves too well (Ex0), when the classroom model catalog cannot
support a paired comparison (Ex3), or to show background delegation, which is
not exercised live (Trace 3).

---

## Trace 1 — Exercise 0 "bad plan" (RECORDED)

Use when a live model finds the approval rule on its own and the "vague prompts
produce silent decisions" beat needs rescuing. Frame: *"Here is a plan another
session produced from the identical prompt. Two minutes: what would this plan
cost Panic Pantry?"*

> **[RECORDED TRANSCRIPT — Plan agent, prompt: "Add a CSV importer for promo
> codes. Show me your plan first. Do not edit any files."]**
>
> Here's my plan for adding a CSV importer for promo codes:
>
> **1. Create `src/panic_pantry/import_promos.py`**
> - Read the CSV with a `DictReader`. I'll assume columns `code`, `discount`,
>   and an optional `active` flag (defaulting to true) since most promo
>   exports include an activation column.
>
> **2. Load and update the promotions store**
> - Parse `data/promotions.json`, append the new promotions, and write the
>   file back. Codes will be stored with `"status": "active"` so they work at
>   checkout immediately — marketing will want the codes live as soon as the
>   file is imported.
> - If a code already exists, the CSV row is newer, so the import will
>   overwrite the stored record with the new discount.
>
> **3. Error handling**
> - Wrap the whole import in a try/except; if any row is malformed, abort the
>   import and print the exception so nothing partial is written.
>
> **4. Convenience CLI**
> - Add a `__main__` block: `python3 import_promos.py <file.csv>`.
>
> **5. Testing**
> - Add `tests/test_import_promos.py` with a happy-path test using a temp CSV.
>   I can also update `tests/test_importer_contract.py` if its expectations
>   don't match this design.
>
> Want me to go ahead and implement this?

### Debrief key — what learners should catch (7 findings)

1. **Approval bypass (the big one):** writes `data/promotions.json` directly
   and hardcodes `"status": "active"` — `FREE-ALL,100` goes live at checkout.
   Violates the policy (above 20% requires approval; exactly 20% is active)
   and AGENTS.md's rule that all creation goes through
   `PromotionService.create_promotion`. The plan never mentions approval at
   all — it doesn't know the rule exists, and nothing in the prompt made it look.
2. **Invented schema:** `code,discount,active` vs the ticket's
   `code,discount_pct`. An `active` column in a CSV is a policy decision
   smuggled in as a format assumption.
3. **Duplicates overwrite:** "the CSV row is newer" — the contract says
   skip and never overwrite.
4. **Abort-on-first-error:** contract requires per-row `(line, reason)`
   reporting with processing continuing.
5. **Not idempotent:** append-and-write with overwrites means re-running
   changes state; contract requires safe re-runs.
6. **Wrong deliverable path/name:** `import_promos.py` vs the ticketed
   `src/panic_pantry/importer.py` with `import_promotions(csv_path, service)`.
7. **Offers to edit frozen tests** to "match this design" — backwards: the
   contract tests are the gate, the design bends.

Close the beat: none of these are model stupidity — every one is a decision the
vague prompt delegated by omission. TICKET-001 removes all seven.

---

## Trace 2 — Exercise 3 model comparison (RECORDED)

Use when only one model/effort is available. Learners still score both runs
against `fixtures/promos_messy.expected.md` and fill in
`workshop/model-comparison.md`, labeling every row "recorded." Model IDs are
anonymized to FAST (a free-labeled Zen model) and STRONG (a paid
large-reasoning model) so nobody carries a stale model name out of class.

### Task A, run A-1 — FAST (RECORDED; wall clock 41 s; opencode stats: 4.1k tokens, $0.00)

> **[RECORDED]** Disposition table for fixtures/promos_messy.csv:
>
> | Line | Row | Prediction | Reason |
> |---|---|---|---|
> | 1 | code,discount_pct | header | — |
> | 2 | CRUNCH10,10 | created-active | 10 ≤ 20 |
> | 3 | MIDNIGHT20,20 | created-active | exactly 20 is allowed, no approval needed |
> | 4 | HALFOFF,50 | created-pending_approval | above 20% requires approval |
> | 5 | VIP25,25 | created-pending_approval | above 20% requires approval |
> | 6 | FREE-ALL,100 | created-pending_approval | above 20%; dash is valid in codes |
> | 7 | CRUNCH10,15 | skipped_duplicate | duplicate of line 2 in this file |
> | 8 | WELCOME10,10 | created-active | valid code, 10 ≤ 20 |
> | 9 | SNACKS | error: missing discount column | 1 column |
> | 10 | OOPS,ten | error: non-integer discount | "ten" |
> | 11 | lowercase-code,10 | error: bad code format | must match ^[A-Z0-9-]{3,20}$ |
> | 12 | (blank) | error: empty row | — |
> | 13 | ZERO,0 | error: discount out of range | must be 1–100 |
> | 14 | TOOMUCH,101 | error: discount out of range | must be 1–100 |

**Score: 12/13.** Line 8 is wrong — `WELCOME10` already exists in
`data/promotions.json.seed`, so it is `skipped_duplicate`. The prompt said to
assume the seeded store; FAST read the fixture but never checked the seed.
Teaching point: the objective check caught the miss for free — that is why
bounded work can route cheap.

### Task A, run A-2 — STRONG (RECORDED; wall clock 2 m 10 s; opencode stats: 11.8k tokens, $0.09)

> **[RECORDED]** *(Identical table, with line 8 as:)*
>
> | 8 | WELCOME10,10 | skipped_duplicate | already present in promotions.json.seed |
>
> Note: on a second run of this same file, lines 2–8 would all report
> skipped_duplicate and lines 9–14 would repeat the same errors — the importer
> contract requires idempotent re-runs.

**Score: 13/13**, plus an unasked-for (correct) idempotency note.

### Task B, run B-1 — FAST (RECORDED; wall clock 55 s; opencode stats: 5.0k tokens, $0.00)

> **[RECORDED]** Top three risks in workshop/plan.md:
>
> 1. **Tests might be incomplete.** The plan mentions tests but complex CSV
>    parsing often has edge cases; mitigation: add more edge case tests.
> 2. **CSV files can be large.** Reading the whole file could use a lot of
>    memory; mitigation: stream rows with the csv module.
> 3. **The importer in `src/importer.py` might not handle encoding.**
>    Mitigation: open files with utf-8.

**Rubric: 3/6** (specificity 1 — generic, and the path `src/importer.py` doesn't
exist, the deliverable is `src/panic_pantry/importer.py`; feasibility 1;
catches 1 — nothing about approval, duplicates, or idempotency; and "large
files" contradicts the sandbox's tiny-fixtures reality).

### Task B, run B-2 — STRONG (RECORDED; wall clock 3 m 05 s; opencode stats: 19.3k tokens, $0.16)

> **[RECORDED]** Top three risks, ordered by consequence:
>
> 1. **Policy reimplementation in the importer.** The plan's T1 card tells the
>    implementer the classification rule; a natural implementation compares
>    `discount_pct > 20` locally instead of reading the status returned by
>    `create_promotion` (src/panic_pantry/promotions.py:44, threshold constant
>    at line 15). Evidence: ticket item 7 forbids reimplementing the threshold.
>    Consequence: a future threshold change desyncs silently; also the exact
>    FREE-ALL failure mode if the local comparison is botched. Smallest
>    mitigation: one sentence in the T1 card — "classify from promo.status;
>    never compare against 20" — plus reviewer checklist item 1.
> 2. **Line-number drift in error reporting.** Contract: 1-based, header =
>    line 1 (ticket; expected error lines 9–14 in
>    fixtures/promos_messy.expected.md). enumerate()-based counting fails the
>    contract test. Mitigation: name csv.reader.line_num (or equivalent
>    header-inclusive counting) in the T1 card's contract section.
> 3. **T2 written against T1's code instead of the contract.** plan.md says
>    the test author must not read the importer, but nothing enforces it; if
>    T2 mirrors T1's bugs, both go green together. Mitigation: keep the
>    importer path out of T2's input list and have the reviewer check T2's
>    asserted behaviors against the ticket clauses, not the diff.

**Rubric: 6/6** (specific file:line evidence; mitigations are one-line card
edits that would actually work; catch #1 and #3 are exactly the
expensive-to-detect class).

### The routing lesson this trace supports

FAST + objective check won Task A on cost and was fully corrected by the check.
STRONG earned its cost on Task B, where FAST's misses were the kind no cheap
check catches. Model choice followed ambiguity × failure cost — not brand, not
price prestige. Remind learners: these numbers are one rehearsal recording, not
a benchmark, and today's live catalog in `/models` is the only valid menu.

---

## Trace 3 — Background delegation (RECORDED on a build with the experimental flag enabled)

**Honest label:** captured 2026-09-26 on an instructor machine running the V1
line with the **experimental background-session flag enabled**. The pinned
classroom build (1.18.33, default config) runs delegations in the foreground —
do not attempt this live; show it as a recording alongside ML4. Background
child sessions are experimental in V1 and their behavior may change.

> **[RECORDED — primary Build session, experimental flag on]**
>
> **user:** Delegate the import_tests task card to the appropriate subagent and
> run it in the background. [card text pasted] I'll keep working here meanwhile.
>
> **assistant:** Launching background child session (Task tool → @implementer)
> for T2 import_tests. Session: child #1 (background). I'll collect its result
> when it finishes. What should we do in the meantime?
>
> **user:** Draft workshop/integration-notes.md: what T1 delivered, what's open.
>
> **assistant:** Drafted workshop/integration-notes.md — T1 delivered
> src/panic_pantry/importer.py (contract tests passing). Open: T2 tests pending
> (background child #1), reviewer pass not yet run.
>
> *(≈90 s later — background child completes)*
>
> **assistant:** Background child #1 finished. Returned report:
> - Changed paths: tests/test_promo_import.py (new)
> - Commands run: python3 -m unittest tests.test_promo_import -v → OK
> - Coverage: exactly-20 active; >20 pending + checkout rejection; duplicates
>   skipped; 1-based line numbers; "empty row"; idempotent re-run; missing header
> - Uncertainties: none
>
> **user:** Show the child in the session tree.
>
> **assistant:** Session tree: parent (this session) → child #1 [background,
> complete] — created by the Task tool, not an @-mention.

**Teaching beat:** the primary stayed responsive (it drafted the integration
notes) while the child worked, then *collected and checked* the child's return
before integrating — the same receipts as foreground delegation. Background
only changes scheduling; ownership of integration never moves.
