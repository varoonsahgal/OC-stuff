# Courseware project instructions

Use these rules whenever you work on this repository's OpenCode orchestration course.

## Source of truth

- Follow `OpenCode_Orchestration_4-Hour_Course_Build_Plan.md` for the instructional design, 240-minute schedule, target of 183 hands-on minutes, recurring Panic Pantry story, exercises, and acceptance gates.
- Follow `COURSE_OUTLINE.md` for the client-provided course scope, audience, prerequisites, and learning objectives. Preserve all objectives; the build plan may add examples and evidence, not silently remove scope.
- The build plan includes a Claude Code agent-definition appendix from an earlier workflow. Do not treat those Claude-specific files as course deliverables; use this pack's GitHub Copilot profiles to create the course.
- Inspect existing repo structure, samples, renderer, conventions, and classroom setup before editing. Preserve established project decisions unless the coordinator records a reasoned change.
- Research version-sensitive OpenCode behavior and current model availability against official sources, then validate commands in the pinned class environment. Date the research and flag facts that need rechecking before delivery.

## Quality bar

- Produce world-class technical teaching: exact, useful, memorable, visually clear, and immediately applicable at work.
- Keep language concise and beginner-friendly. Prefer one memorable point per slide/page, concrete examples, short explanations, and exact steps. Do not make materials long to make them look thorough.
- Teach in short bursts followed by learner action. Preserve at least 75% hands-on time; target the plan's 183 of 240 minutes. Interim, while the rewrite is in progress: 173 hands-on (see `STUDENT_REWRITE_PLAN.md` §10); 183 lands with Phases 3–4.
- Use the Panic Pantry promotion importer throughout. Keep the `>20%` approval rule, code, tests, student prompts, instructor key, and explanations consistent.
- Make learner exercises no-solution-first. Put full answers and recovery keys in clearly instructor-only files.
- Use diagrams and screenshots when they clarify workflow, boundaries, or evidence. Prefer original course-specific diagrams. Include alt text, captions, source links, and attribution.
- Use restrained humor to help ideas stick; never let it obscure the engineering lesson.

## Student materials style guide

Every page under `student/` must pass these rules. The full rationale and word budgets are in `STUDENT_REWRITE_PLAN.md` §2–§5; the rollout is §13 and progress is §16.

**Reader:** an impatient developer who has used an AI coding assistant but has never orchestrated agents. Get to the point in the first line. Every word earns its place.

**Writing**
- The heading is the claim ("Split by file, not by function", not "How the work splits").
- At most 3 sentences per paragraph. Prefer bullets of 15 words or fewer. Use a table for any comparison.
- Explain each concept in at most 4 beats: name → one-line meaning → analogy → why you care.
- Show the whole before the part, and concrete before abstract (the `FREE-ALL,100` row before the word "policy").
- Numbers over adjectives. No hedging in student text: caveats go in one troubleshooting table or the instructor guide.
- Second person, present tense, active verbs.

**Every module, in this order:** 🎯 Goal + "You'll leave with" → the spine table (current row bold) → Why (≤3 bullets) + one 🌍 Real world box → 1–3 ideas, each with its analogy → the exercise, each step written as Do / Why / Done when → optional ⚡ Level up in a collapsed `<details>` block → debrief (collapsed answers) and one 🔑.

**The spine table** opens every module, word for word. Bold the whole current row and add "← you are here" to its module number (see `student/module-1-decomposition.md`):

| Module | You learn to… | Orchestration step | The one rule |
|---|---|---|---|
| 0 | Watch one agent do the whole job alone | The baseline to beat | Measure before you multiply |
| 1 | Split the job and write down each piece | Split | Split by file, not by function |
| 2 | Build agents with hard limits on what they can touch | Staff | A role is a permission, not a name |
| 3 | Pick the right model for each piece | Budget | Cheap model + hard check beats pricey model + blind trust |
| 4 | Hand the cards to agents, run them, compare with Module 0 | Run | Parallel only when tasks share no files |
| 5 | Handle a launch-night failure | Recover | Green tests are evidence, not a verdict |

**Callouts: four kinds only.** 🎯 goal (1 per module) · 🌍 real-world story with a number, a date, a link, and a one-line "so what" (1–2 per module) · ⚡ optional Level up, collapsed (1–3 per module) · 🔑 the bumper sticker (exactly 1 per module, at the end). Don't use 📘 or 💡.

**Vocabulary:** at most 3 new terms per module, each defined where it's first used. The glossary lives in the appendix. Retired words: *packet* (the card is the message), *seeded collision* (say "a code the store already has"), *matched comparison* (say "fair comparison").

**The task card:** one format everywhere, six lines:

```text
DO:     <the one thing to produce, with its exact path>
READ:   <the files to read first>
RULES:  <what must stay true: contract, policy, traps>
TOUCH:  <the only files it may change>
DONE:   <a command you can paste, and the result that means "finished">
REPORT: files changed · exact command + last line of its output · anything you guessed
```

If the agent doesn't need it to do the job, it's not on the card. Ownership rule: one *writer* per file at a time (reading never collides). Checkers report and the owner fixes; a second writer only gets a file through an explicit handoff with its own card and an independent review. A read-only card (a reviewer's) has no command to run, so its DONE line is the bar the report must meet. Dependencies and order belong in `plan.md`; permissions and model belong in the agent file. The two TICKET-001 cards are `workshop/cards/builder.md` (writes `src/panic_pantry/importer.py`) and `workshop/cards/breaker.md` (writes `tests/test_promo_import.py` from the ticket, never from the Builder's code: tests that attack the importer, starting with every way `FREE-ALL` could go live).

**Master analogy:** the restaurant kitchen (the chef at the pass, stations, tickets). Add one vivid second analogy only where the kitchen is weak.

## Build and evidence rules

- Use the repository's existing format and build/test tools. Keep the teaching sandbox small and offline where the plan requires it.
- Every delegated task needs a named deliverable, scope, dependency, acceptance check, and return format.
- Do not let multiple agents edit the same files at once. Review every handoff and integrate results deliberately.
- Run documented commands and tests; record exact commands and outcomes. Never say something passed if it was not run.
- QA the frozen candidate from a clean disposable checkout. Verify schedule arithmetic, exercise steps, test/reset paths, story/contract consistency, links, visuals, and OpenCode version accuracy.
- Do not expose secrets, request credentials, run against production, push, publish, or deploy.
- Report uncertainties plainly. A useful fallback trace is better than depending on a live provider, model, or UI state that may be unavailable.
