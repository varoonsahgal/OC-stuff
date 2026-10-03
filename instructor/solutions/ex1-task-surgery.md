# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 1 — Split the job** (Module 1: Micro-lecture 1, 4 min,
plus Exercise 1, 20 min). Checked against the sandbox on 2026-10-03.

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

---

## Micro-lecture 1 — the two Predicts

**Predict 1: four agents start at once. What goes wrong?** A, B and C all
change `importer.py`. Depending on how each agent edits, one overwrites
another's work, edits fail against a file that changed underneath them, or you
get three halves of one loop nobody designed together. Parsing, validating and
skipping duplicates live in the same loop, so they're one job: the **Builder**.
D writes a different file: the **Breaker**.

Accept any answer that names the shared file plus a concrete failure
(overwritten work, failed or conflicting edits, tangled code). Push back on
"they'd conflict" with no mechanism.

**Predict 2: how many of 8 planted bugs do the 9 contract tests catch?** 4.
Reproduce it live in about a second:

```bash
python3 instructor/tools/breaker-mutants/check_tests.py sandbox/panic-pantry tests.test_importer_contract
```

The four misses: a wrong header that still imports every row (criterion 8), a
3-column row (criterion 1), `20.9` accepted as `20` (criterion 4), and a blank
row reported as `"blank line"` (criterion 4). None of them lets `FREE-ALL` go
live: the service still blocks that. Say so if asked. That's why the Breaker
attacks every criterion, not just the 20% rule.

## Step 1 — Keep or delegate? (answers)

| Task | Answer | Why |
|---|---|---|
| Settle an unclear rule in the ticket | Keep | A judgment call; no command can check it |
| Write `importer.py` | Delegate | Short brief; the contract tests and the Breaker's tests check it |
| Rename one variable | Keep | Briefing it takes longer than doing it |
| Write tests that attack the importer | Delegate | Short brief; the tests run against the finished importer |
| Predict all 13 rows of the messy CSV | Delegate | Short brief; `fixtures/promos_messy.expected.md` checks every row (it's Module 3's Task A) |
| GO / NO-GO at midnight | Keep | A judgment call, and the human's |

The rule to repeat aloud: **delegate when the brief is shorter than the job,
the result can be checked, and it's not a judgment call.**

## Step 2 — `workshop/plan.md` (blanks)

- breaker row, Writes: `tests/test_promo_import.py`
- Kept by me: settling unclear rules, the GO/NO-GO call (plus freezing the
  contract and combining the files, already on the line). "Rename one
  variable" is a generic example, not part of this ticket's plan: fine to
  leave out.

## Step 3 — `workshop/cards/builder.md`

Copied as-is from the handout.

## Step 4 — model `workshop/cards/breaker.md`

Show this after learners have written their own and run the Stranger Test.
**Exception:** the 9-minute rescue in [../README.md](../README.md): a stuck
learner gets this card and runs the Stranger Test on it.

```text
DO:     Create tests/test_promo_import.py: tests that attack the importer. First, every way FREE-ALL,100 could go live: the importer sets a status itself, writes data/promotions.json directly, or bypasses the threshold (for example, calls approve()). Then the ticket rules the exam never tests: a wrong header still imports rows, a 3-column row slips through, a 20.9 discount is accepted as 20, a blank row's reason isn't exactly "empty row".
READ:   tickets/TICKET-001.md, fixtures/promos_messy.expected.md, data/promotions.json.seed, src/panic_pantry/promotions.py, src/panic_pantry/store.py, tests/test_importer_contract.py
RULES:  Never open src/panic_pantry/importer.py. Exactly 20% → active. Above 20% → pending_approval, and rejected at checkout. Skip every test, don't fail, while importer.py is missing. Each test uses its own temp copy of the seed store. If a test fails against a real importer, report it; never weaken it.
TOUCH:  tests/test_promo_import.py only.
DONE:   python3 -m unittest tests.test_promo_import -v → OK, every test skipped until importer.py exists.
REPORT: files changed · the exact command you ran + its last line · which ticket criterion each test covers · anything you guessed.
```

**The three ways `FREE-ALL` could go live** (the DO blank; criterion 7, as
the handout's hint names them):

1. The importer sets `status` itself, or builds a `Promotion` directly,
   instead of calling `PromotionService.create_promotion`.
2. It writes `data/promotions.json` directly.
3. It bypasses the threshold, for example by calling `service.approve()` on
   pending codes.

**If a learner writes "reimplements the threshold":** accept it as a
criterion-7 rule worth testing, but say what it does. Comparing to 20 locally
(for example `>= 20`) only makes the *report* lie: MIDNIGHT20 is listed as
pending. The service still stores FREE-ALL as pending and checkout still
rejects it. The contract test `test_boundary_exactly_20_is_created_active`
catches the `>= 20` version. A copy that uses the right operator is only caught
by the test-technique answer in Step 5 below.

## Step 5 — what the Stranger Test usually finds

Expect many HIGH guesses (our one simulated run marked all five HIGH); don't
let learners chase a count. What matters is where each answer goes:

| Typical guess | Kind | Where the answer goes |
|---|---|---|
| How to catch an importer that copies the 20% check (it behaves the same as the real rule) | How to test | Breaker RULES (e.g. "patch `panic_pantry.promotions.APPROVAL_THRESHOLD_PCT` to 50 and check the report follows the service: VIP25 must land in `created`") |
| How to detect a direct write to `data/promotions.json` or a status set by hand | How to test | Breaker RULES (e.g. "wrap `create_promotion` with `unittest.mock` and check it's called once for every created or pending code; reload the store through a fresh `PromotionService` and compare") |
| What counts as a wrong header (reordered? extra column? different case? spaces?) | **About the rules** | **Both cards' RULES + `plan.md`** |
| What counts as a blank row (empty line? spaces only? a bare comma?) | **About the rules** | **Both cards' RULES + `plan.md`** |
| Whether the 20 / 21 boundaries need their own tests | Scope | Breaker DO |

Suggested rule answers, which match the reference solution:

- **Header:** wrong unless it is exactly `code,discount_pct` after trimming
  spaces around each name. Reordered, extra columns and other letter cases
  are wrong.
- **Blank row:** a line with no characters, or only spaces and commas, is an
  `"empty row"`.

A recorded example is Trace 4 in [fallback-traces.md](fallback-traces.md).

## Grading (pass/fail per line)

- [ ] The two TOUCH lines name different files.
- [ ] The Breaker card forbids opening `importer.py`.
- [ ] RULES keeps "Skip every test, don't fail" and the temp-store line.
- [ ] DO names at least two of the four rules the exam misses.
- [ ] The learner changed a card after the Stranger Test, and rule-level answers
      went on both cards.

## Level up — critical path (answer)

Chain: **you freeze the contract → Builder → Breaker → you combine and run
every test → Reviewer → your GO/NO-GO.** In this classroom delegations run one
after another, so the Builder and the Breaker are both on the critical path.
If they truly ran in parallel (Level up L4.1, planned), only the longer of the
two would be. Three steps on the path are the human's: freeze, combine,
GO/NO-GO. No number of extra agents shortens those.

---

## Evidence: the cards were tested on real agents (2026-10-03)

Each role was played by a fresh Claude subagent that received only the card
text and an isolated copy of the sandbox (with its `AGENTS.md`). These are
simulations of the OpenCode roles, not OpenCode runs. The Breaker's tests were
then graded with `instructor/tools/breaker-mutants/check_tests.py`.

| Card | What the agent produced | Planted bugs caught (of 8) |
|---|---|---|
| Builder card (earlier wording: "codes already in the store"; the handout now says "codes the shop already has (WELCOME10 is one)") | An 83-line importer; contract tests 9/9 OK, full suite green | — |
| Vague first draft (below) | Tests that **failed** while `importer.py` was missing, instead of skipping. It never read the contract tests. | 6 (missed: 3 columns, `20.9`) |
| A simulated learner's filled skeleton (below) | 9 tests, all skipped cleanly before the merge | 7: all four the exam misses. Missed only duplicates-as-errors, which the exam catches, so exam + Breaker = 8 of 8 |
| Model card (above) | 8 tests, all skipped cleanly before the merge | 8 |
| *Frozen contract tests, for comparison* | — | 4 |

**Integration:** each Breaker's tests, combined with the Builder agent's
importer (written independently, from its own card), pass the whole suite: 32
tests OK (learner card) and 31 OK (model card). Two agents that never saw each
other's work fit together. That's the Module 4 promise, rehearsed.

**The vague first draft** (what a rushed learner writes without the skeleton):

```text
DO:     Write tests for the importer in tests/test_promo_import.py.
READ:   tickets/TICKET-001.md, fixtures/
RULES:  Test the 20% rule. Don't read importer.py.
TOUCH:  tests/test_promo_import.py
DONE:   python3 -m unittest tests.test_promo_import -v
REPORT: what you changed and anything you guessed.
```

A Stranger Test on this draft ranked "should the tests skip or fail while
`importer.py` is missing?" as its #1 guess. The Breaker that ran it guessed
"fail", which was the exact mistake the stranger predicted. Use that story when
learners ask whether the Stranger Test is worth four minutes.

**The simulated learner's filled skeleton** (7.5 minutes for Step 4, within
the 8 now planned):

```text
DO:     Create tests/test_promo_import.py: tests that attack the importer. First, every way FREE-ALL,100 could go live: the importer writes data/promotions.json directly, sets the status to active itself, or reimplements/bypasses the 20% threshold (any of these would put FREE-ALL in created/active instead of pending_approval). Then the ticket rules the exam never tests: a wrong header imports nothing at all, a row with 3 columns is an error, a 20.9 discount is rejected (not accepted as 20), a blank row's reason is exactly "empty row".
READ:   tickets/TICKET-001.md, fixtures/promos_messy.expected.md, data/promotions.json.seed, src/panic_pantry/promotions.py, src/panic_pantry/store.py, tests/test_importer_contract.py
RULES:  Never open src/panic_pantry/importer.py. Exactly 20% → active. Above 20% → pending_approval, and rejected at checkout. Skip every test, don't fail, while importer.py is missing. Each test uses its own temp copy of the seed store. If a test fails against a real importer, report it; never weaken it.
TOUCH:  tests/test_promo_import.py only.
DONE:   python3 -m unittest tests.test_promo_import -v → OK, every test skipped until importer.py exists.
REPORT: files changed · the exact command you ran + its last line · which ticket criterion each test covers · anything you guessed.
```
