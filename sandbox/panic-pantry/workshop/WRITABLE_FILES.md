# Writable learner files by exercise

Learner planning artifacts live in this `workshop/` directory. This manifest
lists what learners (and their agents) may create or edit per exercise.

| Exercise | Checkpoint | May create/edit | Must not touch |
|---|---|---|---|
| 0 — Vague ticket / baseline | tag `starter`, worktree `single-agent` | `src/panic_pantry/importer.py`, new tests under `tests/` | everything else |
| 1 — Task surgery | tag `starter` | `workshop/plan.md`, `workshop/cards/*.md` | all of `src/`, `tests/` |
| 2 — Agent crew | tag `starter` | `.opencode/agents/*.md` (agent configs) | all of `src/`, `tests/` |
| 3 — Model routing | tag `starter` | `workshop/model-comparison.md`, scratch branch files | shared fixtures and tests |
| 4 — Orchestrated run | tag `starter`, worktree `orchestrated` | `src/panic_pantry/importer.py` (implementer), `tests/test_promo_import.py` (Breaker), `workshop/integration-notes.md` (primary) | each other's files above |
| Capstone | end of Ex. 4 | files from Ex. 4 plus `workshop/release-note.md` | fixtures, scripts |

Always read-only for every exercise: `tests/test_importer_contract.py`,
`fixtures/`, `data/promotions.json.seed`, `tickets/`, `scripts/`, `AGENTS.md`.
Reset between attempts with `bash scripts/reset.sh`.
