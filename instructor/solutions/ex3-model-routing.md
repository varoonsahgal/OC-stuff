# INSTRUCTOR ONLY — do not distribute

Answer key for **Exercise 3 — Model routing**. Verified against the sandbox
contract and OpenCode 1.18.33 conventions (2026-09-28).

Policy statement to keep consistent everywhere: **discounts above 20% require
manager approval (stored `pending_approval`, unusable at checkout); exactly 20%
is allowed and becomes `active`.**

---

## Exercise 3 — Model routing

Filled comparison record — **RECORDED EXAMPLE, NOT LIVE**: from an instructor
rehearsal on 2026-09-26; model IDs anonymized because the live classroom
catalog must come from `/models` on the day. Use it to show the *shape* of a
good record and as the scoring fallback with
[fallback-traces.md](fallback-traces.md).

```markdown
# workshop/model-comparison.md — RECORDED EXAMPLE (not live)

Configurations (as displayed in /models on rehearsal day):
- FAST  = opencode/<free-labeled-small-model-id>  (free tier; may train on data — varies per model)
- STRONG = <provider>/<large-reasoning-model>  (paid)

## Task A — messy-fixture disposition (score vs fixtures/promos_messy.expected.md, /13)
| Run | Model | Time | Score | Notes |
|---|---|---|---|---|
| A-1 | FAST | 41 s | 12/13 | missed line 8: called WELCOME10 "created" — didn't check the seed |
| A-2 | STRONG | 2 m 10 s | 13/13 | also volunteered the idempotency note (unasked) |

## Task B — plan risk review (rubric /6)
| Run | Model | Time | Score | Notes |
|---|---|---|---|---|
| B-1 | FAST | 55 s | 3/6 | generic risks ("tests might be incomplete"), one wrong path cited |
| B-2 | STRONG | 3 m 05 s | 6/6 | caught local-threshold-reimplementation risk with file:line evidence |

## Cost/tokens (opencode stats)
A-1: 4.1k tok / $0.00 · A-2: 11.8k tok / $0.09 · B-1: 5.0k tok / $0.00 ·
B-2: 19.3k tok / $0.16. (Rehearsal values; record "unavailable" if not shown.)

## Routing decision
Bounded, contract-backed work (Task A shape) → FAST with the objective check;
the 1/13 miss was caught by the check, cost of failure ≈ zero. Ambiguous review
(Task B shape) → STRONG; FAST's misses were exactly the expensive-to-detect
kind. Revisit if FAST's Task-B rubric ever reaches 5/6 on two consecutive runs.
```

Scoring keys for Task A disputes: line 3 `MIDNIGHT20,20` → created-active
(exactly 20% needs no approval); line 8 `WELCOME10,10` → skipped_duplicate
(seeded); lines 9–14 errors (missing column; non-integer; lowercase code;
empty row; 0 out of range; 101 out of range). Full table:
`sandbox/panic-pantry/fixtures/promos_messy.expected.md`.
