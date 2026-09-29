# Module 1 — Micro-lecture 1 + Exercise 1: task surgery

**Where you are:** you have a baseline scorecard and a saved diff from a single agent given the full ticket. You also have a list of assumptions a vague prompt invited. This module turns that experience into a repeatable decomposition method — the plan and task cards you write here drive everything in Exercises 2 and 4.

---

## Micro-lecture 1 — Turn a wish into a ticket

**Claim: a delegated task needs a deliverable and a way to tell whether it is done.** Everything else — model choice, parallelism, agent roles — multiplies on top of that.

"Add a CSV importer" is a wish. `tickets/TICKET-001.md` is a ticket: exact function signature, exact report fields, exact edge cases (blank rows are errors; a missing header reports `(1, reason)` and imports nothing; re-runs are idempotent), and an executable acceptance gate. The difference is who does the deciding — you, or an agent guessing at midnight.

See the difference side by side. The bad task is the one you already watched in Exercise 0 Part A:

> **Bad:** "Build the importer."
> The agent now decides the columns, the duplicate policy, the error behavior, the file it writes, and whether the approval rule even exists. Every one of those is a silent decision you'll discover at midnight.

> **Good (task card excerpt):**
> `Outcome: src/panic_pantry/importer.py satisfying every acceptance criterion in tickets/TICKET-001.md.`
> `In scope: src/panic_pantry/importer.py only.`
> `Acceptance checks: python3 -m unittest tests.test_importer_contract -v`
> Three lines in, the agent already knows what "done" produces, what it may touch, and how it will be judged.

The compact framework, for every task: **keep / delegate / sequence / defer.**

| Verdict | When | Importer example |
|---|---|---|
| **Keep** | tiny edits, coupled decisions, high ambiguity — coordination cost exceeds benefit | freezing the contract; owning the final integration |
| **Delegate** | distinct output, standalone context, checkable result | the importer implementation; the contract tests |
| **Sequence** | the task reads an output that doesn't exist yet | nothing implementation-shaped starts until the interface is frozen |
| **Defer** | value unclear, or blocked on information you don't have | a CLI wrapper nobody asked for — after midnight, if ever |

The phrase to carry home: **delegate by output and boundary, not by job title.** "You are a senior test engineer" produces a costume. "Deliver `tests/test_promo_import.py` asserting these six behaviors; touch nothing else; run this command" produces work.

> 🔑 **Key takeaway:** A delegated task needs a deliverable and a way to tell whether it is done — everything else multiplies on top of that.

Dependencies matter as much as outputs: the parser and the tests only become parallel *after* the interface between them is frozen. Before that, they are one conversation.

```mermaid
flowchart TD
    T[TICKET-001] --> C{{"Contract FROZEN:<br/>import_promotions(csv_path, service) -> ImportReport"}}
    C --> P["Implement importer<br/>(src/panic_pantry/importer.py)"]
    C --> Q["Write contract tests<br/>(tests/test_promo_import.py)"]
    C --> R["Integration notes / docs<br/>(workshop/integration-notes.md)"]
    P --> I[Integrate & review diff]
    Q --> I
    R --> I
    I --> V["python3 -m unittest discover -s tests -v"]
```

*Figure 2 — The importer feature as a dependency graph. Nothing below the gate starts until the contract freezes.*
Text alternative: TICKET-001 flows into a frozen-contract gate; only after the gate do three parallel tracks begin — importer implementation, contract tests, and integration notes — and all three merge into integration, diff review, and the full test command.

Every card you write in this exercise answers five questions. If a part is missing, a specific failure gets in:

```mermaid
flowchart TB
    O["Outcome:<br/>one observable deliverable"] --> S["Scope:<br/>in-scope files it may change /<br/>out-of-scope files it must not touch"]
    S --> C["Contract:<br/>the frozen interface, policy,<br/>and stated assumptions"]
    C --> A["Acceptance checks:<br/>exact commands —<br/>'looks good' doesn't count"]
    A --> R["Return format:<br/>summary, changed paths,<br/>checks run, uncertainties"]
    O -.answers.-> QO(["What does 'done' produce?"])
    S -.answers.-> QS(["What could it collide with?"])
    C -.answers.-> QC(["What must it not decide alone?"])
    A -.answers.-> QA(["How do we verify without trust?"])
    R -.answers.-> QR(["What does the parent need to integrate?"])
```

*Figure 3 — Anatomy of a task card: the five core parts; the full template adds inputs, dependencies, why-separate, and permissions/model.*
Text alternative: a vertical chain of the five task-card parts — outcome, scope, contract, acceptance checks, return format — each linked to the question it answers: what "done" produces, what it could collide with, what it must not decide alone, how to verify without trust, and what the parent needs to integrate.

---

## Exercise 1 — Task surgery (30 min) 🔨

**Goal:** produce an executable plan and two complete handoff cards **before** any parallel implementation.

**Starting checkpoint:**

```bash
cd sandbox/panic-pantry            # the main checkout, at tag starter — NOT a worktree
git status                         # clean
mkdir -p workshop/cards
opencode
```

You may create/edit only `workshop/plan.md` and `workshop/cards/*.md` this exercise (per [WRITABLE_FILES.md](../sandbox/panic-pantry/workshop/WRITABLE_FILES.md)).

### Steps

1. **Delegate the investigation, keep the judgment.** Ask the built-in read-only **Explore** subagent to map the ground truth. @-mention it ([docs: agents](https://opencode.ai/docs/agents), verified 2026-09-28 on OpenCode 1.18.33):

```text
@explore Investigate this repo for TICKET-001 (tickets/TICKET-001.md). Return:
(1) the file and function that enforce the promotion approval policy, with the
exact threshold behavior; (2) the promotion code format and discount range rules;
(3) which files the ticket allows us to create or change; (4) the exact test
command; (5) anything in AGENTS.md that constrains an importer. Cite file paths
for every claim. Do not propose an implementation.
```

2. **Verify before you trust.** Spot-check at least two of its citations against the actual files. An investigation you didn't verify is a rumor with a table of contents.

3. **Write `workshop/plan.md`** containing:
   - the agreed import contract and edge cases (source: TICKET-001 — copy the frozen contract, don't paraphrase it);
   - tasks with owner, deliverable, and acceptance check for each;
   - dependency arrows and the critical path (which single task, if late, delays launch?);
   - which task stays with the primary agent, and **why**;
   - which tasks can run in parallel **after** the interface is frozen;
   - what context each child needs — and what it does *not* need.

4. **Fill the task card template twice**: `workshop/cards/csv_parser.md` (the parsing/validation logic inside `src/panic_pantry/importer.py`) and `workshop/cards/import_tests.md` (`tests/test_promo_import.py` written against the frozen contract). Use this template **verbatim**:

```markdown
## Task ID and title
Outcome: one observable deliverable
Why this task is separate: value of delegation / reason to keep it local
Inputs and source paths: facts the agent should inspect
Contract: agreed interfaces, rules, and assumptions
In scope: files or behavior it may change
Out of scope: files, behavior, and actions it must leave alone
Dependencies: task IDs that must finish first
Acceptance checks: exact tests, commands, or review questions
Permissions/model: authority required and selected model/effort
Return format: summary, changed paths, checks run, findings, uncertainties
```

> 💡 **Field note:** A good task card is a good PR description written *before* the work: outcome, scope, checks, and what reviewers should look at. Teams that adopt the card format usually discover their human tickets improve too.

**Required artifact:** `workshop/plan.md` + two completed cards.

**Acceptance checks:**
- [ ] Plan states the policy as: discounts **above 20%** require approval; exactly 20% is active.
- [ ] Every task has an owner, a deliverable, and an *executable* acceptance check (a command or concrete review question — "looks good" doesn't count).
- [ ] The two cards' "In scope" file lists do not overlap.
- [ ] Each card's "Out of scope" names at least the frozen files: `tests/test_importer_contract.py`, `fixtures/`, `data/promotions.json.seed`, `scripts/`.
- [ ] The plan names the critical path and explains why one task stays with the primary agent.

**Hints (use in order):**
1. Stuck on decomposition? List the *deliverable files* first (the ticket and WRITABLE_FILES name them), then work backward to tasks.
2. Critical path: which artifact do both other tasks read but never write? That freeze is your gate.
3. For "context each child needs": the test author needs the contract and fixture expectations — does it need to read the importer's implementation at all?

**Troubleshooting:**
- Explore tries to edit or wanders → it is read-only by design; restate the task packet with the numbered return format.
- Explore's answer is vague → your prompt probably was too. Ask for file-path citations per claim.
- Not sure what's writable → [WRITABLE_FILES.md](../sandbox/panic-pantry/workshop/WRITABLE_FILES.md), row "1 — Task surgery."

**Debrief:** Which decisions did writing the card force you to make that the vague prompt in Exercise 0 let you skip? On your team's codebase, who freezes an interface — and where would you write it down?

> 🔑 **Key takeaway:** The card forces the decisions the vague prompt let you skip — better to make them at 2 PM than discover them at midnight.

---

**Next:** [module-2-agent-crew.md](module-2-agent-crew.md) — give your cards to agents whose boundaries are configuration, not politeness.
