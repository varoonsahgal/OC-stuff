# INSTRUCTOR ONLY — do not distribute

Do not commit, print, screen-share, or copy any file under `instructor/` into a
student-visible location. Students get the `student/` folder and the sandbox only.

---

# Instructor Guide — Orchestration Fundamentals for Agentic Development (OpenCode)

Pinned environment: **OpenCode 1.18.33** (V1 syntax). All commands, keybinds, and
config examples were verified 2026-09-28 on that binary. If the classroom image
changes version, re-verify before teaching — permission vocabulary and agent
config differ across major versions.

## Files in this pack

| File | Purpose |
|---|---|
| [solutions/ex0-vague-ticket.md](solutions/ex0-vague-ticket.md) | Answer key: Ex0 expected discoveries, baseline scorecard, common near-misses |
| [solutions/ex1-task-surgery.md](solutions/ex1-task-surgery.md) | Answer key: model plan.md and both task cards, grading criteria |
| [solutions/ex2-agent-crew.md](solutions/ex2-agent-crew.md) | Answer key: implementer agent, expected denial behavior, model reviewer report |
| [solutions/ex3-model-routing.md](solutions/ex3-model-routing.md) | Answer key: recorded comparison example, Task A scoring keys |
| [solutions/ex4-orchestrated-run.md](solutions/ex4-orchestrated-run.md) | Answer key: integration checklist, expected worktree states, honest comparison |
| [solutions/capstone-injections.md](solutions/capstone-injections.md) | The four capstone injection steps, diagnoses, and model release note |
| [solutions/reviewer-agent.md](solutions/reviewer-agent.md) | Known-good `.opencode/agents/reviewer.md` learners build in Ex2 |
| [solutions/importer_solution.py](solutions/importer_solution.py) | Known-good importer; drop into `src/panic_pantry/importer.py` to make the full suite pass |
| [solutions/fallback-traces.md](solutions/fallback-traces.md) | Recorded transcripts: Ex0 "bad plan," Ex3 model comparison, background-delegation demo |

## Pre-class setup (day before + morning of)

1. From the pack root: `bash sandbox/setup.sh`. Confirm output shows tag
   `starter` and both worktrees (`sandbox/worktrees/single-agent`,
   `sandbox/worktrees/orchestrated`) at the same commit.
2. In `sandbox/panic-pantry`: `bash scripts/check_env.sh`. Expected:
   `opencode --version` → 1.18.33; suite ends `OK (skipped=9)` (23 tests, 9 skipped).
3. Verify the known-good path end to end:
   `cp instructor/solutions/importer_solution.py sandbox/panic-pantry/src/panic_pantry/importer.py`
   then `python3 -m unittest discover -s tests -v` → **23 tests, OK, 0 skipped**.
   Then `bash scripts/reset.sh` to remove it. Never leave the solution in place.
4. Model access: launch OpenCode in the sandbox, run `/models`, and record
   today's catalog. Choose and note (a) the model/effort every learner will use
   for the Ex0 and Ex4 matched runs (must be identical in both), and (b) two
   configurations for Ex3. If a free-labeled Zen model is planned, confirm the
   account/billing gate is already satisfied on every seat and note the
   train-on-data caveat aloud. If the catalog is thin, plan to teach Ex3 from
   [solutions/fallback-traces.md](solutions/fallback-traces.md).
5. Verify keybinds on the classroom image: Tab toggles Build/Plan;
   `<Leader>+Down` enters the first child session, Left/Right cycle, Up returns.
6. Do one full timed dry run of Ex4 in a scratch worktree, then re-run
   `bash sandbox/setup.sh` to restore. **Warn learners (and yourself): re-running
   setup.sh discards all worktree changes.**

## Room-running rules

- You call the 15-minute implementation timeboxes in Ex0 Step 2 and Ex4 —
  a visible countdown, hard stop, "unfinished" is valid data.
- The matched comparison is only fair if model/effort is identical across Ex0
  and Ex4. Announce the pinned model before Ex0 Step 2 and again before Ex4.
- Never let learners put credentials in the repo. Provider auth was done at
  seat setup, not during class.
- Keep interpretation modest at debriefs: one classroom run is a demonstration,
  not a benchmark.

## Per-exercise timing cues and recovery

### Exercise 0 — single-agent baseline (25 min: Step 1 warm-up ≈8, Step 2 =15 hard timebox; scorecard fill-in happens during the transition into ML1)
- **Cue @ 6 min:** anyone still chatting with the Plan agent should stop and
  write down source / decisions / one claim; the plan doesn't need to be bad,
  the *notes* need to exist.
- **Cue @ 8 min:** everyone should have found `PromotionService.create_promotion`
  and can state ">20% pending, exactly 20 active." If not, point at the
  `promotions.py` docstring directly — don't burn baseline time.
- **Recovery:** model finds the rule on its own and proposes a *correct* plan?
  Great — pivot the debrief using the recorded "bad plan" transcript in
  [solutions/fallback-traces.md](solutions/fallback-traces.md): "here is what a
  plausible plan looked like in another session; what would it have cost?"
- **Recovery:** baseline run rabbit-holes (rewriting the service, editing frozen
  tests) — let it, within the timebox; it's comparison gold. Stop at 15:00 sharp.
- **Reset if needed:** worktree contaminated before Step 2 → `bash sandbox/setup.sh`
  rebuilds both worktrees (announce that it wipes them).

### Exercise 1 — task surgery (10 min: plan ≈2, first card ≈1, second card ≈7)
- **Cue @ 3 min:** `plan.md` and `cards/csv_parser.md` saved from the handout.
  The critical-path blank should read T0 (the freeze): both build tasks wait on it.
- **Cue @ 8 min:** `cards/import_tests.md` drafted. Check that Dependencies says
  T0 only and that the test author is told not to read the importer.
- **Watch for:** "In scope" lists that overlap between the two cards — flag
  immediately; this is the Ex4 collision seed. Also "check: looks good" —
  demand a command.
- **Recovery:** anyone stuck past 8 min → hand them the model
  `import_tests.md` from the answer key and move on; the learning is in the
  debrief question (why the test author must not read the importer).

### Exercise 2 — agent crew (32 min)
- **Cue @ 12 min:** reviewer.md exists and loads (no YAML errors).
- **Cue @ 18 min:** everyone has run the denial test. The pass bar is a
  **configuration** denial, visible in the UI — walk the room and eyeball it.
- **Common failures:** file in the wrong directory (must be
  `sandbox/panic-pantry/.opencode/agents/`, i.e., the project OpenCode was
  launched from); missing required `description`; unquoted glob keys in the
  bash map; deprecated `tools:` block fighting `permission`.
- **Recovery:** learner hopelessly stuck at 20 min → give them
  [solutions/reviewer-agent.md](solutions/reviewer-agent.md) to transcribe, and
  have them do the denial test + delegation anyway; the observable boundary is
  the point.

### Exercise 3 — model routing (32 min: A ≈14, B ≈12, record ≈6)
- **Cue @ 5 min:** everyone has picked two configurations and written down the
  exact IDs. Nobody proceeds on "the good one."
- **Cue @ 16 min:** Task A scored /13 against `fixtures/promos_messy.expected.md`.
  Common scoring disputes: line 3 (`MIDNIGHT20,20` → active, exactly 20% needs no
  approval) and line 8 (`WELCOME10` seeded → skipped_duplicate).
- **Recovery:** single-model classroom or throttled free tier → run the recorded
  comparison from [solutions/fallback-traces.md](solutions/fallback-traces.md);
  learners still score and record it, clearly labeled "recorded."
- **Recovery:** `opencode stats` blank for a provider → "unavailable" is the
  correct entry; forbid estimating.

### Exercise 4 — orchestrated run (37 min: pre-launch ≈8, window =15, integrate ≈10, record ≈4)
- **Before start:** confirm every learner copied `.opencode/agents/` and cards
  into the orchestrated worktree and set the **same model as Ex0**.
- **Cue @ launch:** contract confirmed frozen; ownership map read aloud once:
  importer → `src/panic_pantry/importer.py`; tests → `tests/test_promo_import.py`;
  primary → `workshop/integration-notes.md`.
- **Hard stop @ 15:00** of the window. Then integration checks even if unfinished.
- **Watch for:** agents editing `tests/test_importer_contract.py` (frozen — this
  becomes a free capstone-style teachable moment); silent parent-side patching of
  a child's bad result (ask for the targeted repair delegation instead).
- **Recovery:** total delegation meltdown → learner implements from their own
  cards manually within the timebox; the comparison stays valid (record
  "interventions: many").
- **Pacing:** the reviewer delegation in the integration segment may take
  2–3 min with strong models and can spill into the record segment; that's
  acceptable.
- **Reset:** only via `bash sandbox/setup.sh`, only before the window starts.

### Capstone (27 min: inject ≈3, work ≈20, notes ≈4)
- Inject **one** issue per pair from the four in
  [solutions/capstone-injections.md](solutions/capstone-injections.md)
  — vary them across the room. Inject while learners are at the ML5 debrief or
  stretching; do not narrate which issue they got.
- If a pair finished Ex4 with no working importer: first drop in the known-good
  importer (`cp ../../../instructor/solutions/importer_solution.py src/panic_pantry/importer.py`
  from inside their worktree), run the suite green, *then* inject. They still
  get the full capstone loop.
- **Cue @ 10 min into work:** classification written before any fix. If someone
  is already patching, stop them and ask for the classification sentence.
- **Scoring:** 0–2 each on task clarity; dependency/boundary quality;
  agent/model choice; permissions; tests + diff review; honest release note.
  Announce up front: a correct fix without evidence does not get full credit.
- **Recovery:** pair out of time → an evidence-backed NO-GO note scores well;
  say so at minute 15 to lower the panic.

### Close (5 min)
Exit ticket on paper or chat: one task to delegate next week, one to keep, one
control/check to add. Collect them — they are your course feedback too.

## If the whole provider is down

The orchestration labs need a working OpenCode + one model. If provider access
dies mid-class: Ex1 proceeds fully offline (planning artifacts); Ex2 agent files
can be written and syntax-checked offline (denial test deferred); Ex3 runs from
recorded traces; Ex0/Ex4 comparison collapses to a walkthrough of the answer-key
artifacts. Say plainly what is live and what is recorded — modeling honest
evidence handling is itself course content.
