# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 4 — Orchestrated run**. Verified against the sandbox
contract and OpenCode 1.18.33 conventions (2026-09-28).

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

---

## Exercise 4 — Orchestrated run

### Integration checklist (what a passing learner did)

- [ ] Contract confirmed frozen (plan.md/ticket re-read) before first delegation.
- [ ] Same model/effort as Ex0 set via `/models` before the window.
- [ ] Delegations carried the full card text (fresh child context).
- [ ] The Breaker's child session was created by the **primary via the Task
      tool** (governed by `permission.task`) — the learner instructed
      "Delegate this task card to the appropriate subagent" + the breaker card
      rather than @-mentioning; verify in the session tree.
- [ ] `.opencode/agents/implementer.md` carries an explicit `model:` line with
      a `/models` catalog ID (the learner's Ex3 routing choice — equal to the
      Ex0 pinned model/effort for the matched run), and that ID appears in the
      run record.
- [ ] `git status` shows exactly: `src/panic_pantry/importer.py` (new),
      `tests/test_promo_import.py` (new), `workshop/integration-notes.md` (new),
      plus copied `.opencode/agents/*` and `workshop/cards/*` — nothing else. Any other change =
      boundary violation to disposition.
- [ ] No two writers on one file (compare status output to the ownership map).
- [ ] `python3 -m unittest discover -s tests -v` run by the learner post-merge;
      with a correct importer and valid new tests: **23+ tests** (23 from the
      starter suite + however many your Breaker added), OK.
- [ ] `@reviewer` findings collected; each fixed / accepted / deferred in
      `workshop/integration-notes.md`.
- [ ] Scorecard includes integration/rework minutes and a modest interpretation.

### Expected worktree states at end of Ex4

| Worktree | Branch | State |
|---|---|---|
| `sandbox/worktrees/single-agent` | `single-agent` | Ex0 baseline: importer (possibly incomplete) + captured diff; untouched since Ex0 |
| `sandbox/worktrees/orchestrated` | `orchestrated` | importer + `tests/test_promo_import.py` + `workshop/integration-notes.md` + copied agents/cards |
| `sandbox/panic-pantry` (main) | `main` | Ex1–Ex3 artifacts only: `workshop/plan.md`, `workshop/cards/*`, `workshop/model-comparison.md`, `.opencode/agents/*`; **no importer** |

Both worktrees still at tag `starter` ancestry — verify with
`git log --oneline -1` matching in both before crediting the comparison.

### Typical honest comparison result

Orchestrated runs usually show: equal-or-better contract-test coverage, an
extra test file the baseline never wrote, more total tokens (two child sessions
+ reviewer), and nonzero integration minutes the baseline didn't have. Neither
condition "wins" universally — say so. The decomposable importer flatters
orchestration; a one-file bug fix would not.
