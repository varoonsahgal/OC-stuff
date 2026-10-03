# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 2 — Build the crew** (Module 2, 36 min: setup 3, Step 1 2,
Step 2 10, Step 3 5, Step 4 8, Step 5 3, Step 6 5). Every config behavior below
was checked on the OpenCode **1.18.33** binary with `opencode debug agent` in a
git checkout of the sandbox (2026-10-03).

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

---

## What 1.18.33 actually does (read before class)

| Config | Behavior | Consequence for the handout |
|---|---|---|
| `edit: deny` (shorthand) | Removes the `edit`, `write` and `apply_patch` tools from the agent entirely | A live edit request shows **no red denial**: the reviewer has nothing to call. Step 3's pass bar is the `debug agent` output, not the chat |
| `edit: {"*": deny, "<path>": allow}` | Allows create/edit/patch on that one path, refuses the rest with an error | The implementer's lock. Paths are matched relative to the **git worktree root**; `*` crosses `/`; the last matching rule wins |
| Same map, allow first and `"*": deny` last | `"*": deny` wins for everything, and the edit tools disappear | The learner sees "I have no edit tool" from the implementer |
| Non-git directory | Path patterns never match, so `"*": deny` refuses everything | Not reachable in class (the sandbox is a git repo), but it explains odd reports from people who copied the sandbox elsewhere |
| `task: {"*": deny, implementer: allow, reviewer: allow}` | The task tool's description lists only the allowed agents; any other `subagent_type` errors | Step 6 |
| Subagent sessions | Get `task: deny` (and `todowrite: deny`) by default | "Helpers can't hire anyone" |
| A key with an unquoted `*` (e.g. `*: deny`) | The YAML fails to parse, and the file **still loads**: mode `all`, the whole file as its prompt, default permissions (**everything allowed**) | The most dangerous learner bug. The model even reads "edit: deny" in its prompt, so it may *act* locked. Step 3's `debug agent` write succeeds and `store.py` becomes `# hi` |
| A tab in the indentation, or a key with no value | `Error: Configuration is invalid at …/agents/<file>.md`; OpenCode won't start at all | Loud; the message names the file |
| No `description` | Loads anyway (the docs call it required) | The main agent has nothing to route by; the handout says "always write one" |
| "Always" on any edit prompt | Approves edit `"*"` for the whole running instance (every agent), evaluated after each agent's own rules, until restart | It overrides the implementer's path lock. If anyone clicked it, have them restart OpenCode |
| `explore` built-in | Docs say read-only; config allows `bash` (and `read` of `.env` without asking) | "Read-only" is its prompt only |
| A user `@mention` | Bypasses the parent's `permission.task` check for that turn | Step 6 asks the lead in words rather than @-mentioning, and the proof is `debug agent` |

`opencode debug agent <name>` prints the resolved agent (JSON). With
`--tool <id> --params '<json>'` it runs that one tool for real, with that agent's
permissions and no model. It works with no provider configured, so Step 3 and
Step 6's checks are offline-safe. It can't run `task` past the permission check,
which is all Step 6 needs.

---

## Step 1 — implementer (copied verbatim)

```markdown
---
description: Writes src/panic_pantry/importer.py from a task card. Builds code only; never writes tests or reviews.
mode: subagent
temperature: 0.1
permission:
  edit:
    "*": deny
    "src/panic_pantry/importer.py": allow
  bash:
    "*": deny
    "python3 -m unittest*": allow
---
You carry out exactly one task card. It arrives in your first message.

- Change only the files on the card's TOUCH line.
- Follow the card's RULES exactly. If something is unclear, stop and say so.
- Run the card's DONE command before you finish.

Report back exactly what the card's REPORT line asks for.
```

Verified: `debug agent implementer --tool write` on `src/panic_pantry/importer.py`
creates the file; on `src/panic_pantry/store.py` it is refused (output below).
Don't demo the positive write in the main checkout: an `importer.py` there
un-skips the contract tests for everyone who copies your screen.

## Step 2 — reviewer

The known-good file is [reviewer-agent.md](reviewer-agent.md). Pass bar:
`description` present; `mode: subagent`; `permission` (not the deprecated
`tools:`) with `edit: deny`; bash `"*": deny` first, then only the review
commands; every `*` key quoted; checklist covers approval bypass, duplicates,
row reporting, missing tests; a fixed report format with `file:line`.

## Step 3 — expected outputs

Live request (`@reviewer Please add a clarifying comment to src/panic_pantry/store.py.`):
the reviewer says it has no edit tool or can't edit, or tries a shell
redirection that bash `"*": deny` refuses. **There is no red permission
denial** for the edit, because the tool doesn't exist for this agent. If a
learner's reviewer *does* edit, check for an unquoted `*` key first.

```text
$ opencode debug agent reviewer --tool write --params '{"filePath":"src/panic_pantry/store.py","content":"# hi"}'
Tool write is disabled for agent reviewer

$ opencode debug agent implementer --tool write --params '{"filePath":"src/panic_pantry/store.py","content":"# hi"}'
Error: Unexpected error

The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"}, … {"permission":"edit","pattern":"*","action":"deny"},{"permission":"edit","pattern":"src/panic_pantry/importer.py","action":"allow"}, …]
```

`git status --short` afterwards shows only `?? .opencode/` (plus the learner's
untracked `workshop/` files). If `store.py` reads `# hi`, the lock failed:
`git checkout -- src/panic_pantry/store.py`, fix the file, re-run.

## Step 4 — model reviewer report (from the 6-line reviewer card)

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
Guessed: nothing. No files edited (no edit tool).
```

## Step 6 — lead

```markdown
---
description: Coordinates TICKET-001. Delegates each card to the right helper and checks the results; never writes code.
mode: primary
temperature: 0.1
permission:
  edit: deny
  bash:
    "*": deny
    "git status*": allow
    "git diff*": allow
    "python3 -m unittest*": allow
  task:
    "*": deny
    "implementer": allow
    "reviewer": allow
---
You coordinate. You never write code yourself: you send each card to the right helper and check what comes back.
```

```text
$ opencode debug agent lead --tool task --params '{"subagent_type":"general","description":"write tests","prompt":"x"}'
Error: Unexpected error

The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [… {"permission":"task","pattern":"*","action":"deny"},{"permission":"task","pattern":"implementer","action":"allow"},{"permission":"task","pattern":"reviewer","action":"allow"} …]
```

(`explore` gives the same refusal; `debug agent lead --tool write …` prints
`Tool write is disabled for agent lead`.)

Asked "Which helpers can you delegate to?", the lead lists implementer and
reviewer only, because the task tool's description is built from the allowed
list. A model may still *mention* `general` from general knowledge; the
`debug agent` refusal is the pass bar.

**Why the lead needs the list:** agent restrictions are not inherited. Without
`task`, a lead with `edit: deny` could delegate "write the importer" to
`general`, which edits anything. That's the whole point of Step 6.

**Module 4 note:** Module 4 runs from **Build**, not the lead, and lets Build
pick a helper for the Breaker card (usually `general`). The lead has no agent
allowed to write `tests/test_promo_import.py`. That's intentional here; it
returns as a question if Module 4 adds a Breaker agent.

## Level up solutions

- **Cap the effort:** `steps: 12` in the reviewer frontmatter. In 1.18.33 the
  limit only injects a "stop and summarize" message; a model can keep calling
  tools. `maxSteps` is deprecated. `doom_loop` defaults to `ask` and fires on
  three identical tool calls (same tool, same input) within one response.
- **One-word review:** the handout's `.opencode/commands/review-ticket.md`.
  `.opencode/command/` works too. A command whose `agent` is a subagent runs
  as a subtask (child session) automatically. The `` !`…` `` lines run in the
  directory OpenCode was started in, **without** a bash permission check,
  after argument substitution: never put `$ARGUMENTS` inside one (it's a shell
  injection). Naming the file `review.md` silently replaces the built-in
  `/review`. In Module 2 the diff is empty; the correct reviewer answer is
  "nothing to review".
- **Lethal trifecta:** as written, all three agents have private data (`read`
  allows everything except `.env`, which only asks), untrusted content (the
  CSV), and a way out (`webfetch` is allowed by default). The reviewer key
  already has `webfetch: deny`. `bash` is the other exit: every crew agent's
  bash map starts with `"*": deny`, which is why `curl` isn't on any list.

## Debrief answers

- **Could the implementer still change `store.py`?** Yes. It may run
  `python3 -m unittest`, the tests import `importer.py`, and `importer.py` is
  code it wrote. Permissions gate tools, not the code those tools execute. In
  1.18.33 `apply_patch` also doesn't check a move destination against `edit`
  rules (a niche escape; don't teach it, but know it if asked).
- **Who should have `edit: deny`?** Reviewers, auditors, anything reading
  untrusted input. Push for one concrete team example.
