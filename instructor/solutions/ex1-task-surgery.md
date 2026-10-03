# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 1 — Split the job** (Module 1, 15 min). Checked against
the sandbox on 2026-10-03.

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

---

## Step 1 — Spot the bad split (answer)

Agents A, B and C all write `src/panic_pantry/importer.py`. Run them at once and
the last save wins, so two jobs vanish. A + B + C are one job: the **Builder**.
D writes a different file and needs nothing from the others: the **Breaker**.

Accept any sentence that names "same file" and "overwrite / last save wins".
Push back on "they'd conflict" with no mechanism: *why* would they conflict?

## Step 2 — Keep or delegate? (answers)

| Task | Answer | Why |
|---|---|---|
| Settle an unclear rule in the ticket | Keep | A judgment call; no command can check it |
| Write `importer.py` | Delegate | Short brief; the contract tests check it |
| Rename one variable | Keep | Briefing it takes longer than doing it |
| Write attack tests from the ticket | Delegate | Short brief; the tests run |
| Find every file that calls `create_promotion` | Delegate | Short brief; a search checks the answer (built-in `explore` is a good fit) |
| Make the GO / NO-GO call at midnight | Keep | The final call is the human's |

The rule to repeat aloud: **delegate when the brief is shorter than the job and
the result can be checked.**

## Step 3 — `workshop/plan.md`

Learners copy it from the handout as-is. Check it exists and that the Order
line says the contract is frozen *before* either card runs.

## Step 4 — `workshop/cards/builder.md`

Copied as-is from the handout. It's the worked example the Breaker card
imitates.

## Step 5 — model `workshop/cards/breaker.md`

Show this only after learners have written their own and run the Stranger
Test. It has been tested: an agent given only this card wrote tests that
catch planted bugs the official exam misses (see "Evidence" below).

```text
DO:     Create tests/test_promo_import.py: unittest tests that try to break the TICKET-001 importer. Attack every way FREE-ALL,100 (or any code above 20%) could go live, then each edge case in criteria 1–9.
READ:   tickets/TICKET-001.md, fixtures/promos_messy.expected.md, fixtures/promos_clean.csv, fixtures/promos_messy.csv, data/promotions.json.seed, src/panic_pantry/promotions.py, src/panic_pantry/models.py, src/panic_pantry/store.py, tests/test_importer_contract.py (to see what's already covered and to copy its skip-if-missing setup)
RULES:  Never open src/panic_pantry/importer.py: test the ticket, not the code. Exactly 20 → active. 21 and above → pending_approval, absent from list_active(), and rejected by store.apply_promotion, including after a second import. A duplicate (twice in one file, or already in the store like WELCOME10 or BIGSPENDER) is skipped and never overwritten. Bad rows report a 1-based line number (header = line 1); a blank row's reason is exactly "empty row". Non-integers (like 20.9) and rows without exactly 2 columns are errors. A wrong or missing header → (1, reason) and nothing imported. Skip the whole class if panic_pantry.importer can't be imported. Each test builds its own PromotionService on a temp copy of data/promotions.json.seed; no clock, network, or randomness.
TOUCH:  tests/test_promo_import.py only.
DONE:   python3 -m unittest tests.test_promo_import -v → no errors; every test skips while importer.py is missing.
REPORT: files changed · the exact command you ran + its last line · which criterion each test covers · anything you guessed.
```

**Three ways a bad importer lets `FREE-ALL,100` go live** (the RULES prompt in
Step 5). Accept any three:

1. It sets `status` itself, or builds a `Promotion` directly, instead of calling
   `PromotionService.create_promotion`.
2. It calls `service.approve()` on pending codes.
3. It writes `data/promotions.json` directly.
4. It compares the discount to 20 itself, with the wrong operator (`>= 20`), so
   the report lies about what's pending.

Tests that catch them: after importing, `FREE-ALL` is `pending_approval`, not in
`list_active()`, and `store.apply_promotion` raises `PromotionNotActiveError`,
including after a second import.

## Grading (pass/fail per line)

- [ ] The two TOUCH lines name different files (`importer.py` vs. `tests/test_promo_import.py`).
- [ ] The Breaker card forbids opening `importer.py`.
- [ ] Exactly 20 → active and 21+ → pending *and* rejected at checkout are both on the card.
- [ ] DONE is a pasteable command and says tests skip until the importer exists.
- [ ] The learner changed their card after the Stranger Test.

## Level up — critical path (answer)

Chain: **you freeze the contract → Builder → you merge and run every test →
Reviewer → you make the GO/NO-GO call.** The Breaker is off the critical path:
it's shorter than the Builder and runs alongside it. Three of the steps on the
critical path are the human's (freeze, merge, GO/NO-GO), which is why adding
agents can't shrink them.
