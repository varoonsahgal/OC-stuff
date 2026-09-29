# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 2 — Agent crew**. Verified against the sandbox
contract and OpenCode 1.18.33 conventions (2026-09-28).

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

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
