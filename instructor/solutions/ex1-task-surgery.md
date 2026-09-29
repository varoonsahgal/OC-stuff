# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 1 — Task surgery**: model plan and task cards.
Verified against the sandbox contract and OpenCode 1.18.33 conventions
(2026-09-28).

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

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
