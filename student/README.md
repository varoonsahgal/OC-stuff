# Orchestration Fundamentals for Agentic Development — Student Guide

**Tool:** OpenCode **1.18.33** (your instructor pinned this version; every command and config example in these materials was verified 2026-09-28 on OpenCode 1.18.33).
**Sandbox:** the Panic Pantry snack shop in [../sandbox/panic-pantry](../sandbox/panic-pantry/README.md). Pure Python 3 standard library. Everything runs offline.
**Promise:** you leave having decomposed, delegated, run, reviewed, and integrated a real feature with OpenCode — not having watched someone talk about agents.

---

## The story you are walking into

Panic Pantry is a tiny late-night snack shop preparing the **Midnight Crunch Drop**. Marketing will hand over a CSV of promo codes minutes before launch. The shop already has one hard rule, enforced in code and written on the wall:

> **Discounts above 20% require manager approval.** A promo of exactly 20% is fine and becomes active. A promo of 21% or more is stored as `pending_approval` and cannot be applied at checkout until a human manager approves it.

The nightmare scenario: someone imports `FREE-ALL,100`, the importer skips the approval rule, a customer pays nothing, and the shop ships a truckload of pretzels into bankruptcy. Your job all afternoon is to build the importer *without* letting any agent — fast, clever, or free — bypass that rule.

One incident, four hours, every orchestration skill you need at work.

---

## Schedule (240 minutes total, 183 hands-on)

| Time | Min | Type | Segment |
|---|---:|---|---|
| 0:00–0:07 | 7 | Lecture | Opening — more agents ≠ more progress |
| 0:07–0:32 | 25 | **Hands-on** | Exercise 0 — the vague ticket + single-agent baseline |
| 0:32–0:38 | 6 | Lecture | Micro-lecture 1 — turn a wish into a ticket |
| 0:38–1:08 | 30 | **Hands-on** | Exercise 1 — task surgery |
| 1:08–1:18 | 10 | Break | |
| 1:18–1:24 | 6 | Lecture | Micro-lecture 2 — a role is a boundary |
| 1:24–1:56 | 32 | **Hands-on** | Exercise 2 — build a small agent crew |
| 1:56–2:02 | 6 | Lecture | Micro-lecture 3 — model choice is a budget decision |
| 2:02–2:34 | 32 | **Hands-on** | Exercise 3 — model routing |
| 2:34–2:39 | 5 | Break | |
| 2:39–2:45 | 6 | Lecture | Micro-lecture 4 — parallelism is a dependency claim |
| 2:45–3:22 | 37 | **Hands-on** | Exercise 4 — orchestrated run + matched comparison |
| 3:22–3:28 | 6 | Lecture | Micro-lecture 5 — a green check is evidence, not a handoff |
| 3:28–3:55 | 27 | **Hands-on** | Capstone — midnight launch |
| 3:55–4:00 | 5 | Close | Exit ticket |

**Arithmetic check:** hands-on = 25 + 30 + 32 + 32 + 37 + 27 = **183 min**. Lecture = 7 + 6 + 6 + 6 + 6 + 6 = 37. Breaks = 10 + 5 = 15. Close = 5. Total = 183 + 37 + 15 + 5 = **240 min**. ✔

---

## One-time setup (instructor runs this before class; you verify)

From the pack root:

```bash
bash sandbox/setup.sh
```

This makes `sandbox/panic-pantry` a git repo, tags the starter commit `starter`, and creates two matched worktrees at the **same commit**:

- `sandbox/worktrees/single-agent` — Exercise 0 baseline
- `sandbox/worktrees/orchestrated` — Exercise 4 orchestrated run

> ⚠️ **Re-running `bash sandbox/setup.sh` DISCARDS all changes inside both worktrees.** Only re-run it when you deliberately want a fresh comparison.

Verify your environment (from `sandbox/panic-pantry`):

```bash
bash scripts/check_env.sh
```

Expected: python3 and git versions print, `opencode --version` prints `1.18.33`, and the test suite ends with `OK (skipped=9)` — 23 tests, 9 skipped. The 9 skips are the importer acceptance tests waiting for a file you have not written yet. They are the finish line, not a problem.

Reset the sandbox anytime with:

```bash
bash scripts/reset.sh
```

**File ownership manifest:** [workshop/WRITABLE_FILES.md](../sandbox/panic-pantry/workshop/WRITABLE_FILES.md) lists exactly what you (and your agents) may edit per exercise. Treat it as law.

**Project rules for agents:** [AGENTS.md](../sandbox/panic-pantry/AGENTS.md) at the repo root is read automatically by OpenCode as project rules — no prompt needed ([docs: rules](https://opencode.ai/docs/rules), verified 2026-09-28 on OpenCode 1.18.33). `/init` can generate one; ours already exists. OpenAI's harness-engineering write-up recommends keeping this file a ~100-line table of contents and enforcing the real rules mechanically with tests — which is exactly how this sandbox is built ([OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/), Feb 2026).

---

## How to use these files

Work through the modules in order. Each module is a short lecture summary followed by the hands-on exercise it sets up — the course rhythm is always **claim → story/evidence → framework → exercise → debrief**.

| Module | File | Segments covered |
|---|---|---|
| 0 | [module-0-baseline.md](module-0-baseline.md) | Opening lecture + Exercise 0 — the vague ticket + single-agent baseline |
| 1 | [module-1-decomposition.md](module-1-decomposition.md) | Micro-lecture 1 + Exercise 1 — task surgery + the task-card template |
| 2 | [module-2-agent-crew.md](module-2-agent-crew.md) | Micro-lecture 2 + Exercise 2 — build a small agent crew |
| 3 | [module-3-model-routing.md](module-3-model-routing.md) | Micro-lecture 3 + Exercise 3 — model routing |
| 4 | [module-4-parallel-run.md](module-4-parallel-run.md) | Micro-lecture 4 + Exercise 4 — orchestrated run + matched comparison |
| 5 | [module-5-capstone.md](module-5-capstone.md) | Micro-lecture 5 + Capstone — midnight launch + the 5-minute close |
| — | [appendices.md](appendices.md) | Objective coverage map, command crib sheet, sources |

Watch for two recurring callouts:

- 🔑 **Key takeaway** — the one sentence to remember from that point in the module.
- 💡 **Field note** — how the exercise maps to your daily engineering work.

---

## Classroom version note

> **One-time version note:** OpenCode V2 exists and renames some vocabulary (`permissions`, `shell`, `subagent`). This class uses **V1 syntax only**, matching the pinned 1.18.33 binary. If a doc page or blog snippet looks different from these materials, check which major version it targets before trusting it.

Start here: [module-0-baseline.md](module-0-baseline.md)
