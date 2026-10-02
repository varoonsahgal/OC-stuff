# Module 1 — From ticket to task cards

> 🎯 **Goal:** Turn one feature request into clear, bounded work.
>
> **You'll leave with:** `workshop/plan.md` and two task cards. In Module 4, an implementer builds the importer, a helper writes tests, and your reviewer checks the result.

## Why plan before you delegate?

In Exercise 0, the ticket made most of the decisions for the agent. Real tickets often leave gaps. If you don't define what "done" means, the agent has to guess.

Before handing off work, decide:

1. What should be produced?
2. Which files may the helper change?
3. What check will show the work is done?

## One ticket, two deliverables

The ticket asks for an importer. **This course adds a separate test-writing task** so you can practice assigning independent work and checking requirements from a fresh perspective.

| Task | Deliverable | File |
|---|---|---|
| Implement the importer | CSV import code | `src/panic_pantry/importer.py` |
| Add independent tests | New tests based on the ticket | `tests/test_promo_import.py` |

The existing `tests/test_importer_contract.py` suite is the fixed acceptance check. Leave it unchanged. The new test file adds another set of checks; it does not replace the existing suite.

The importer stays with one owner because two agents editing the same file can collide. The test writer can work from the ticket and fixtures without reading the importer, so its tests check the requirements rather than copying the code's behavior.

Both tasks use the same agreed requirements. **Independent means they can be assigned in either order; it doesn't promise that OpenCode will run them simultaneously.** Run the tests once both files are ready.

> **One feature, two deliverables: one helper builds it; another checks it.**

In Module 2, you'll create an implementer and a read-only reviewer. In Module 4, the primary agent will route the test card to a suitable helper; you do not need to create a third custom agent.

## Agree on the rules first

The **contract** is the ticket's acceptance criteria: what the importer must do. **Freeze the contract** means agree on those criteria before delegating. If a requirement is unclear, settle it first. If it changes later, update both cards before work continues.

## What goes on a task card?

A card gives one helper the information it needs to work on its own:

| Card detail | Question it answers |
|---|---|
| **Outcome** | What should I produce? |
| **Inputs and contract** | What should I read, and what rules must I follow? |
| **File scope** | What may I change? What must I leave alone? |
| **Acceptance check** | What command or review proves the task is done? |

The plan is for you: it shows the full job and what you keep or delegate. Each card goes to one helper and covers just that helper's task.

## Exercise 1 — Make the split and write the cards (10 min) 🔨

From the pack root, open the main checkout:

```bash
cd sandbox/panic-pantry
mkdir -p workshop/cards
```

Create files only in `workshop/`.

### Step 1 — Choose the split (1 min)

Before reading the table below, think: **Would you give two agents the same file to edit? What separate work could one of them do?**

Use this split for the exercise:

| Task | Owner | File | Check |
|---|---|---|---|
| T1 — implement importer | Implementer | `src/panic_pantry/importer.py` | `python3 -m unittest tests.test_importer_contract -v` |
| T2 — add tests | Test helper | `tests/test_promo_import.py` | `python3 -m unittest tests.test_promo_import -v` |

Copy this short template into `workshop/plan.md`. Fill in the split reason.

```markdown
# Plan — TICKET-001 importer

Contract: tickets/TICKET-001.md, criteria 1–9. Freeze before delegation.
My work: freeze the contract; integrate both files and run the full suite.
Split reason: <Why can these tasks be assigned separately?>

| Card | Owner | Output | Check |
|---|---|---|---|
| T1 csv_parser | Implementer | src/panic_pantry/importer.py | python3 -m unittest tests.test_importer_contract -v |
| T2 import_tests | Test helper | tests/test_promo_import.py | python3 -m unittest tests.test_promo_import -v |
```

### Step 2 — Save the importer card (1 min)

Copy this card into `workshop/cards/csv_parser.md`:

```markdown
## T1 — csv_parser: write the importer
Outcome: Create src/panic_pantry/importer.py with import_promotions(csv_path, service) -> ImportReport, following all criteria in tickets/TICKET-001.md.
Inputs: tickets/TICKET-001.md; src/panic_pantry/promotions.py; src/panic_pantry/models.py; fixtures/promos_clean.csv; fixtures/promos_messy.csv.
Contract: Follow criteria 1–9. Duplicates include codes already in the store (WELCOME10, STAFF-PICK, MIDNIGHT-VIP, BIGSPENDER). Let the service decide approval; do not compare against 20 yourself.
In scope: src/panic_pantry/importer.py only.
Out of scope: all files except src/panic_pantry/importer.py; do not edit tests/, fixtures/, data/promotions.json.seed, or scripts.
Dependencies: Contract frozen.
Acceptance check: python3 -m unittest tests.test_importer_contract -v
Permissions/model: TBD
Return: summary, changed paths, checks run, findings, uncertainties
```

### Step 3 — Create the test card (8 min)

Copy T1 into `workshop/cards/import_tests.md`. Change these task-specific lines for T2:

| Card detail | T2 value |
|---|---|
| **Title** | `T2 — import_tests: write independent tests` |
| **Outcome** | Create `tests/test_promo_import.py` with tests for the ticket's acceptance criteria |
| **Inputs** | The ticket and fixtures, including `fixtures/promos_messy.expected.md`; do not read `importer.py` |
| **Contract** | Test the frozen ticket criteria, including the 20% approval boundary, duplicates, and row outcomes. Base expectations on the ticket and fixtures, not the importer. |
| **In scope** | `tests/test_promo_import.py` only |
| **Out of scope** | All files except `tests/test_promo_import.py`; do not edit the fixed contract tests, importer, fixtures, seed data, or scripts. |
| **Acceptance check** | `python3 -m unittest tests.test_promo_import -v` |

Leave the other safety and return-format lines in place. The test command is run after the importer is ready.

### Done when

- [ ] `plan.md` names both tasks and explains why they can be assigned separately.
- [ ] Each card has a different **In scope** file.
- [ ] Neither card allows changes to the fixed contract tests, fixtures, seed data, or scripts.
- [ ] Each card names a command that can check its work.

## Quick check

- **Why only one importer card?** Two writers on one file can collide.
- **Why write tests without seeing the importer?** So the tests reflect the ticket's requirements, not the implementation's choices.
- **What if the ticket is unclear?** Clarify the contract before handing out the cards.

> 🔑 **Key takeaway:** Decide what done means before you hand off the work.

**Next:** [Module 2 — Build the implementer and reviewer](module-2-agent-crew.md).
