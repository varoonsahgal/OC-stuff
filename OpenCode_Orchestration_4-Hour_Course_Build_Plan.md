# OpenCode Orchestration Fundamentals: 4-Hour Course Build Plan

**Purpose:** a production brief for an agent authoring the student and instructor materials for the four-hour class.  
**Research checked:** September 27, 2026.  
**Course promise:** learners leave having decomposed, delegated, run, reviewed, and integrated a real feature with OpenCode—not just having watched someone talk about agents.

## 1. Instructional design contract

Build the course around one evolving software incident, short lecture bursts, and exercises that produce visible work. Preserve the useful rhythm in the supplied Context Engineering excerpts:

1. Make one strong, memorable claim.
2. Ground the claim in a small story, code example, or failure.
3. Let learners inspect evidence before giving them the answer.
4. Teach a compact framework they can reuse at work.
5. Send them straight into an exercise.
6. Debrief with questions that connect the exercise to their own codebases.

The class should feel like an engineering workshop with an engaging narrative—not a feature tour. Use occasional humor to make a point memorable, never to pad a slide.

### Design targets

- Four hours total, with **183 minutes of hands-on work** (76% of total class time, breaks included).
- Five short teaching bursts totaling 37 minutes, plus a seven-minute opening and a five-minute close.
- One small local codebase and one recurring incident from start to finish.
- No required cloud account, database, payment API, production credentials, or live external service.
- Student instructions are no-solution-first. Keep answer keys, completed configs, and recovery steps in instructor-only files.
- Beginner-friendly language, exact verified commands, expected outputs, short prompts, staged hints, and clear stop points.
- Materials use the repository's existing Markdown/slide renderer. If a new shell is needed, use modular Markdown slides and preserve the user's established dark canvas with magenta accent.

## 2. Recurring story: Coupon Calamity at Panic Pantry

### The setup

Panic Pantry is a tiny Python snack shop preparing its **Midnight Crunch Drop**. Marketing wants to import promo codes from a CSV before launch. The starter application already has a promotion-creation path and an important policy: **discounts above 20% require manager approval**. That rule is enforced by the existing `create_promotion()` function and documented in the repo, but a new importer could accidentally bypass it.

The amusing failure image is simple: a customer enters `FREE-ALL`, pays nothing, and the shop delivers a truckload of pretzels. Keep the humor brief; use the bug to teach a serious engineering habit: a new entry point must preserve the rules enforced by existing entry points.

### The bounded feature request

> Add a CSV importer for promotion codes. It must report row-level results, reject malformed rows, avoid duplicate promotions, preserve the 20% approval rule, and be safe to run twice.

Use a local, deliberately small Python 3 project and the standard library. The exact behavior must be decided and written into the acceptance criteria before implementation. Suggested contract:

- CSV columns are `code,discount_pct`.
- A valid code at or below 20% may be created through the existing promotion service.
- A code above 20% is marked as needing approval and must not become active.
- Malformed rows report their line number and reason; valid rows continue.
- Duplicate codes in the same file and codes already present are reported without overwriting existing records.
- Running the same input twice does not create duplicate active promotions.
- Import code calls the existing policy-enforcing service; it does not reimplement or bypass approval logic.

The material author must make the starter code, fixture, tests, and written contract agree exactly. The contract above is a proposal for the build agent to implement and validate, not permission to leave edge cases ambiguous.

### Why this story works

The feature crosses a small number of real boundaries: existing business rules, parsing, result reporting, tests, and documentation. It gives learners useful decomposition choices without making them build a large app. It also supports a deliberate contrast between a task that looks parallel and one that is actually parallelizable.

## 3. Learning objectives and evidence

| Objective | Evidence learners produce |
|---|---|
| Break a feature into verifiable units | A task map with outputs, acceptance checks, and dependency arrows |
| Decide whether to delegate | A short keep/delegate/sequence decision for each task |
| Write task specifications | At least two complete agent handoff cards |
| Configure specialized agents | A planner or explorer workflow and a read-only reviewer agent |
| Choose models thoughtfully | A comparison record tied to quality, latency, cost visibility, and risk |
| Run work in parallel safely | Two agents working from a frozen contract with distinct scopes |
| Integrate and validate | A reviewed diff, passing test command, and evidence-based release note |

Do not score learners on whether an LLM happens to produce a perfect patch on the first attempt. Score the quality of the work design, boundaries, validation, and response to findings.

## 4. Four-hour run of show

| Time | Minutes | Format | Segment and learner output |
|---|---:|---|---|
| 0:00–0:07 | 7 | Lecture | **Opening:** “More agents do not automatically mean more progress.” Introduce Panic Pantry and the release lead/orchestrator role. |
| 0:07–0:32 | 25 | Hands-on | **Exercise 0 — Single-agent baseline:** inspect the repo with a vague request, then run the canonical feature ticket in a clean baseline worktree using one primary agent. Capture tests, time, and review findings. |
| 0:32–0:38 | 6 | Lecture | **Micro-lecture 1 — Turn a wish into a ticket:** acceptance criteria, dependency graphs, and context packets. |
| 0:38–1:08 | 30 | Hands-on | **Exercise 1 — Task surgery:** inspect the code and `AGENTS.md`; identify the approval rule; write the contract, task map, dependencies, and first two agent handoff cards. |
| 1:08–1:18 | 10 | Break | Reset. |
| 1:18–1:24 | 6 | Lecture | **Micro-lecture 2 — A role is a boundary:** primary agent, child session, fresh context, permissions, and when to keep work in one session. |
| 1:24–1:56 | 32 | Hands-on | **Exercise 2 — Build a small agent crew:** configure a read-only reviewer and one implementation role; delegate a repo investigation; inspect the child session and its report. |
| 1:56–2:02 | 6 | Lecture | **Micro-lecture 3 — Model choice is a budget decision:** capability, ambiguity, risk, latency, and available provider/model choices. |
| 2:02–2:34 | 32 | Hands-on | **Exercise 3 — Model routing:** run the same bounded task using two available model/effort configurations where available; compare against tests and a rubric. Record unavailable cost/token data as unavailable. |
| 2:34–2:39 | 5 | Break | Reset. |
| 2:39–2:45 | 6 | Lecture | **Micro-lecture 4 — Parallelism is a dependency claim:** distinguish independent work from “two agents editing one file.” File ownership coordinates; Git worktrees can isolate. |
| 2:45–3:22 | 37 | Hands-on | **Exercise 4 — Orchestrated comparison:** run the same canonical ticket from the same starting commit in a second clean worktree, now with the planned subagents. Compare outputs and integration work. |
| 3:22–3:28 | 6 | Lecture | **Micro-lecture 5 — A green check is evidence, not a handoff:** tests, diff review, failure recovery, and the human integration decision. |
| 3:28–3:55 | 27 | Hands-on | **Capstone — Midnight launch:** resolve an injected integration issue, validate the full change, ask the reviewer agent for findings, and prepare a short release note with evidence. |
| 3:55–4:00 | 5 | Close | Exit ticket: one task to delegate next week, one task to keep, and one control/check to add. |

**Time check:** 183 hands-on + 37 lecture + 15 breaks + 5 close = 240 minutes. Do not let demos or setup consume the hands-on blocks; stage the repo and provider access before class.

## 5. Teaching beats and slide design

Each burst should take six to seven minutes and use two to four slides. Put one main claim on each slide; use progressive reveals only when the reveal changes what learners should notice.

### Opening — More agents do not automatically mean more progress

- **Hook:** “The release is at midnight. The discount code is `FREE-ALL`. The shop is out of pretzels and apparently in debt.”
- **Reveal:** a broad feature request is not an executable plan; additional agents multiply the effect of a good plan or a bad one.
- **Visual:** a tiny kitchen/pass-chef metaphor: several stations, one ticket, one person responsible for integration. Avoid a generic robot illustration.
- **Transition:** show the ticket and ask students what context is missing.

### Micro-lecture 1 — Turn a wish into a ticket

- **Claim:** a delegated task needs a deliverable and a way to tell whether it is done.
- **Teach:** task size; boundaries; dependencies; acceptance criteria; context packet; “keep / delegate / sequence / defer” decision.
- **Visual:** the feature as a directed acyclic graph. Mark the approval contract as a prerequisite; show parser and tests as parallel candidates only after their interface is fixed.
- **Phrase to repeat:** “Delegate by output and boundary, not by job title.”

### Micro-lecture 2 — A role is a boundary

- **Claim:** an agent role is useful when it changes objective, context, or authority.
- **Teach:** primary versus subagent; fresh child context; foreground versus background; read-only exploration/review; narrower tool permissions; complete handoffs.
- **Visual:** parent session sends a task packet to a child session and receives a report/diff back. Label “fresh context” and “permissions still apply.”
- **Humor:** “The reviewer is the health inspector. If you give it a chainsaw, the costume is not the safety control.”
- **Transition:** students configure a reviewer whose permissions—not just its polite instructions—block edits.

### Micro-lecture 3 — Model choice is a budget decision

- **Claim:** choose a model for the task's uncertainty and failure cost, then check the result.
- **Teach:** routine, well-bounded work can use a faster/less expensive available choice; ambiguous, high-impact planning and review may justify a stronger reasoning choice; model selection is a hypothesis, not a permanent ranking.
- **Visual:** a two-axis matrix (ambiguity × consequence of failure) with a third small marker for latency/cost.
- **Rule:** use the live OpenCode model selector in the pinned environment. Never put a model name in a slide as “the best model” or assume every learner has the same provider catalog.

### Micro-lecture 4 — Parallelism is a dependency claim

- **Claim:** safe parallel work has a stable interface, independent output, and clear ownership.
- **Teach:** critical path; contract-first parallelism; shared-file risk; task boundaries versus security boundaries; branches/worktrees; tracking who owns each deliverable.
- **Visual:** a dependency graph with green parallel branches and a red shared-file collision. Include the line: “Three chefs, one cutting board.”
- **Useful distinction:** a file list in a prompt is coordination guidance; it does not by itself enforce access control. Permissions and isolated worktrees/branches offer stronger controls.

### Micro-lecture 5 — A green check is evidence, not a handoff

- **Claim:** the parent still owns integration.
- **Teach:** inspect child summary and changed paths; run deterministic tests; inspect `git diff`; ask an independent reviewer; handle findings; write a handoff with evidence and unresolved risks.
- **Visual:** “agent says done” beside receipts: test command/output, diff summary, review findings, human decision.
- **Transition:** capstone issue is intentionally caught by the reviewer or a test; students decide and demonstrate the fix.

## 6. Exercise specifications

Every student exercise must have a student-facing README with: estimated time; starting checkpoint; goal; exact commands; task prompt; required output; acceptance checks; hint ladder; troubleshooting; and a debrief. Instructor keys live separately. Do not reveal the full solution before the debrief.

### Exercise 0 — The vague ticket (25 minutes)

**Goal:** experience the gap between “ask for a feature” and “commission a task.”

1. Confirm the starter repo is clean and run the baseline tests. The instructor setup should provide a `single-agent` worktree and a matching `orchestrated` worktree, both at the same commit.
2. In the baseline worktree, ask the primary agent only: “Add a CSV importer for promo codes.” Ask for a plan, not edits. Record assumptions, missing policies, unknown interfaces, and missing acceptance checks. This is a quick discovery activity, not the A/B score.
3. Inspect the starter repo's instructions and existing promotion creation path. Find the 20% approval rule.
4. Give the baseline run the canonical feature ticket and acceptance criteria printed in the exercise. Use one primary agent, no child agents, and the agreed timebox. Save the final diff and test output.
5. Record elapsed time, tests passed, policy/review findings, human interventions, and available token/cost data.

**Success evidence:** learners find the authoritative policy and produce a baseline result to compare with Exercise 4. Do not rely on a live model making a specific mistake. Include a deterministic “bad plan” transcript in the instructor pack so the teaching beat still works if a model discovers the rule correctly.

### Exercise 1 — Task surgery (30 minutes)

**Goal:** produce an executable plan before any parallel implementation.

Learners create `workshop/plan.md` with:

- the agreed import contract and edge cases;
- tasks, owners, deliverables, and acceptance checks;
- dependency arrows and the critical path;
- which task remains with the primary agent and why;
- which tasks can run in parallel after the interface is frozen;
- what context each child needs and does not need.

Have the planning/explore agent inspect the repo and return relevant paths plus evidence; learners decide whether its proposed plan is safe. Require task cards for `csv_parser` and `import_tests`.

### Exercise 2 — Build a small agent crew (32 minutes)

**Goal:** configure one useful specialized role and inspect a real child session.

1. Create a read-only `reviewer` agent. Its review checklist covers approval bypass, duplicate handling, row reporting, and missing tests.
2. Configure permissions to deny edits and to restrict shell access as intended. Allow only the reads needed for the project. Test the denial by explicitly asking the reviewer to edit a file; it must be blocked by configuration.
3. Delegate a codebase investigation to a suitable exploration/review agent. Supply the task packet rather than relying on the parent conversation to carry over.
4. Inspect the child session and capture its findings, changed files (if any), and uncertainty.

**Pass bar:** correct agent mode, a descriptive purpose, least authority needed, fresh-context handoff, and an observed permission boundary. “The prompt told it not to” is not enough.

### Exercise 3 — Model routing (32 minutes)

**Goal:** compare model configurations using observable results, not brand loyalty.

- Pick one small, deterministic task and one higher-ambiguity planning or review task.
- Use two model/effort choices that are actually enabled in the classroom project. If only one is available, compare two effort settings if supported, or use the instructor's recorded comparison trace.
- Keep the task, starting commit, and acceptance checks constant for the paired run.
- Record model/provider as shown in OpenCode; time to completion; test result; review rubric; and visible cost/token information if available.
- Discuss whether a stronger/slow choice was justified for the small task and whether a quick choice missed anything consequential.

Do not ask students to reveal hidden chain-of-thought. Ask them to judge the produced plan, patch, tests, and evidence.

#### Free-model workflow

- Start with the current model picker/catalog and choose a model explicitly marked free and available in the classroom project. Do not assume a model name from an old slide is still available.
- Use free models for bounded, low-risk jobs first: map relevant files, summarize a small subsystem, draft tests from a written contract, update a short README, or implement one independent module.
- Do not hand a free model an entire repo and an underspecified “build the feature” request. Give it the task card, only the relevant source paths, the approved contract, exact in/out-of-scope files, and the test command.
- Work in short stages: inspect and report; agree on the plan; implement one deliverable; run a deterministic check; ask for one targeted repair if needed; inspect the diff yourself.
- Keep a child agent's return compact: changed paths, checks run, pass/fail, assumptions, and unresolved issues. This limits irrelevant context from being fed back to the parent.
- For a free-model orchestration run, use one orchestrator plus at most two genuinely independent workers. Avoid launching a swarm; extra sessions add calls and integration work, and free-model capacity may vary by provider/account.
- Use `AGENTS.md` for stable project rules, but keep it short. Put task-specific details in the ticket/hand-off rather than adding every temporary instruction to permanent repo context.
- If the free model struggles, shrink the task, add the missing evidence, or route a high-consequence decision to an available stronger model and human reviewer. Do not compensate by removing tests or permissions.
- Before class, verify which models are actually free and accessible, and confirm quota/latency expectations with the provider. Keep the already-planned recorded trace as a fallback.

The official model catalog changes over time. The live OpenCode catalog currently has multiple entries marked “Free”; do not bake those model names or an assumption of unlimited access into student instructions. OpenCode Zen also offers paid pay-per-request models, so instructor materials must distinguish its free-labeled model choices from paid Zen access.

### Exercise 4 — Parallel run (37 minutes)

**Goal:** coordinate parallel work without creating parallel confusion.

Before launch, learners freeze the import contract. Suggested two concurrent tasks:

| Agent | Deliverable | Writable scope | Check |
|---|---|---|---|
| Parser implementer | CSV parsing and row-level validation | `src/csv_parser.py` | Parser unit tests |
| Test author | Tests written against the frozen contract | `tests/test_promo_import.py` | Tests collect and express the edge cases |
| Primary agent | Existing-policy map, integration plan, or documentation | Assigned separate docs/planning file | Review against contract |

One child task runs in the background while the primary agent handles an independent deliverable. The primary then collects the child result, checks changed paths, and integrates the pieces. If the class setup permits, show a Git worktree as the stronger isolation option; otherwise keep the hands-on work in one feature branch with non-overlapping files and explicitly call that coordination, not hard isolation.

**Required checks:** verify every result maps to a task card; no two writers owned the same file; task contract was frozen before the parallel run; run the provided tests after integration; inspect `git status` and `git diff`.

**Optional collision demo:** show a prebuilt transcript where two agents both edit `src/importer.py`. Ask learners to diagnose the coordination failure and decide whether to serialize, split the contract, or isolate work in separate worktrees. Do not make the class depend on a live race condition occurring.

### Matched comparison — single agent versus orchestrated agents

Make this an explicit experiment across Exercise 0 and Exercise 4. It is wise to compare both approaches, but only on a task with several real, independent deliverables after the interface is fixed. The CSV importer qualifies: parsing, contract-based tests, and documentation can be separated; approval-policy integration still needs an identified owner.

For a fair classroom comparison:

1. Use the same starter commit, canonical feature ticket, acceptance criteria, model/effort, tool permissions, and **15-minute implementation window** in both conditions. The starter repo must contain the canonical ticket so both runs receive the same brief. Stop both runs at the same limit, even if one is unfinished.
2. Run the first condition in one clean worktree with a single primary agent and no delegation.
3. Run the second condition in another clean worktree with one primary orchestrator and the planned subagents. Freeze the contract before they start.
4. Compare the artifacts, not the agents' explanations: acceptance tests passed, policy defects found, changed files, review findings, human interventions, elapsed time, and token/cost data if exposed.
5. Record integration/rework time as well as implementation time. A faster patch that needs more cleanup may not be a win.
6. If there is time, have half the pairs run the conditions in the opposite order or share results across groups to reduce order effects.

Keep the interpretation modest: this is a controlled class demonstration, not a benchmark from one run. Orchestration may improve coverage or wall-clock time on this decomposable feature while using more total model calls. On a small one-file bug or tightly coupled change, the single agent may be faster. Do not compare a detailed orchestrated brief against a vague single-agent prompt; that only measures prompt quality, not orchestration.

### Capstone — Midnight launch (27 minutes)

**Goal:** finish with a reviewable result and demonstrate the entire loop.

Give each pair one injected integration problem: approval status mishandled, duplicate line handling differs from the contract, an agent changed an out-of-scope file, or a test asserts a stale function signature. Learners must:

1. Stop and classify the issue: task/context gap, dependency error, boundary conflict, or implementation defect.
2. Assign the smallest corrective task to the right agent/model.
3. Inspect the resulting diff and reviewer findings.
4. Run the full test command and capture its output.
5. Produce a five-line release note: changed behavior, tests run, review status, unresolved concern, human go/no-go decision.

**Scoring (0–2 each):** task clarity; dependency/boundary quality; appropriate agent/model choice; permissions; tests and diff review; honest release note. A correct fix without evidence does not receive full credit.

## 7. Reusable task card

Include this as a copyable template in the course repo and have learners use it twice:

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

Teach the short decision test: **delegate when the task has a distinct output, enough context to stand alone, a checkable result, and less coordination cost than the expected benefit.** Keep tiny edits, coupled decisions, and high-ambiguity work in the primary session until clarified.

## 8. Recommended course repository layout

Adapt to the existing project rather than replacing its tooling. A useful target structure is:

```text
README.md
course-design.md
course-build-brief.md
lectures/
  intro.md
  module1-decomposition.md
  module2-delegation.md
  module3-agent-design.md
  module4-model-routing.md
  module5-parallel-work.md
  module6-integration.md
  conclusion.md
exercises/
  module0-vague-ticket/README.md
  module1-task-surgery/README.md
  module2-agent-crew/README.md
  module3-model-routing/README.md
  module4-parallel-run/README.md
  capstone/README.md
  setup/README.md
  setup/check-environment.sh
sandbox/panic-pantry/
  AGENTS.md
  src/
  tests/
instructor/
  run-of-show.md
  facilitation-notes.md
  solutions/
  answer-key.md
  recovery-guide.md
  fallback-traces/
assets/
  orchestration-loop.svg
  dependency-map.svg
  task-card.svg
  permissions-map.svg
  model-routing-matrix.svg
```

Keep student files free of completed solutions. A separate instructor key should contain expected findings, a known-good patch, likely model variations, timing cues, and recovery steps.

## 9. Visual and source plan

Use visuals to make relationships visible. Do not decorate every slide with generic AI artwork.

1. **Orchestration loop:** request → inspect → plan → contract → delegate → review → test → integrate.
2. **Dependency graph:** what can run in parallel, what must wait, and why.
3. **Task-card anatomy:** deliverable, context, scope, dependencies, checks, return format.
4. **Authority map:** primary agent, child session, tool permissions, human approval point.
5. **Model-routing matrix:** ambiguity and failure cost, with latency/cost as a visible tradeoff.
6. **Integration receipts:** diff, tests, review findings, and final human decision.

Prefer original Mermaid/SVG diagrams for course-specific facts. Capture real OpenCode UI screenshots from the pinned classroom version for agent selection, child-session navigation, model selection, and permission behavior. Blur credentials, account names, and local paths. If adapting an external diagram, link and attribute it; do not hotlink an image that may disappear. Add alt text and captions. Check every external link and image at material freeze.

## 10. Environment and build gates

The content author must inspect the actual classroom image/VM and pin the version before writing commands or configuration examples.

### Mandatory pre-class checks

- Record `opencode --version` and the date; pin the version in the student setup page.
- Verify the current command names, TUI navigation, session switching, background child behavior, permission behavior, and model selection against that exact build.
- Confirm every learner can authenticate to at least one approved model provider and can see a usable model in the project. Do this before class; never ask learners to put credentials in the repo.
- If the intended model catalog is unavailable, provide instructor-controlled fallback traces for the comparison activity. The main orchestration labs still require a working OpenCode setup.
- Confirm Git and Python 3 are installed, all tests run offline, the starter repository is clean, and reset instructions work from a new clone.
- Prepare two clean Git worktrees at the same starter commit. Verify each can open its own OpenCode session and run the same tests; do not let changes from the baseline condition leak into the orchestration condition.
- Choose the live free model for the matched comparison before class, record its exact model ID and access path, and confirm the same selection works in both worktrees. Keep a fallback model trace if provider access is throttled or unavailable.
- Run the full course once in the same VM image, terminal, and model access that students will use. Time it; do not infer that setup steps are quick.

### Version-specific OpenCode note

At research time, the official OpenCode site exposes V2 documentation. V2 uses current names such as `agents`, `permissions`, `shell`, and `subagent`; some V1 material uses `agent`, `permission`, `bash`, `task`, and `subtask`. The docs also describe Markdown agents under `.opencode/agents/`, subagents with fresh child-session context, foreground/background execution, model selection via the live model catalog, per-agent model configuration, and ordered permission rules.

Do not mix V1 and V2 examples in one student lab. If the class VM remains on V1, write and test the entire lab for V1 and label it. If upgrading to V2, verify the installed provider, current tool names, agent config, permission rules, and migration behavior before publishing. A hidden agent is not a security boundary; use permissions. Never teach disabling safety checks as the shortcut to make a lab pass.

## 11. Research takeaways to shape the class

- **Parallelism is selective.** Anthropic's multi-agent research write-up says multi-agent approaches suit work with substantial parallel exploration, but notes that coding work often has fewer truly parallelizable tasks and that highly dependent/shared-context tasks are a poor fit. Their reported token multiplier is specific to their research system, not a universal estimate. Use it to justify measuring coordination and cost, not to promise a fixed speedup.
- **A harness includes the environment.** Recent engineering write-ups emphasize repository legibility, explicit contracts, automated tests, incremental progress, and artifacts that let later sessions resume without guessing. Therefore the class teaches task cards, test receipts, and clean handoffs as part of orchestration—not as optional paperwork.
- **Interactive sessions do not scale forever.** Newer orchestration examples add task queues, isolated environments, and review loops. This class should teach the transferable core—bounded tasks, context handoffs, ownership, verification—without attempting to build a production agent scheduler in four hours.
- **OpenCode behavior is version-sensitive.** Configuration and permission vocabulary have changed. Pin the installed version and test every exercise in that environment.
- **Measure the output.** Learners should compare model choices with the same task and starting point, using observable tests, latency, and cost/token visibility when available. Do not claim a model is best because its name or price suggests it.
- **Free is a model-access option, not a quality strategy by itself.** Current OpenCode materials show both free-labeled model variants and paid Zen access. Teach learners to check availability, keep tasks narrow, and compensate for model limits with explicit context, tests, and human review.

## 12. Source pack for the material author

Prefer official product documentation and first-party engineering write-ups. Use these as source material, then write the teaching explanation in original language.

### OpenCode primary documentation

- [Agents (V2)](https://opencode.ai/v2/docs/agents) — custom agent files, modes, fresh child context, foreground/background, model options, and permissions.
- [Tools (V2)](https://opencode.ai/v2/docs/tools/) — the subagent tool's task prompt, child session, background result, and session ID behavior.
- [Models (V2)](https://opencode.ai/v2/docs/models) — live catalog, provider availability, session model selection, and per-agent model choice.
- [OpenCode model catalog](https://opencode.ai/v2/docs/console/models/) — current model IDs, including entries marked Free. Recheck immediately before class.
- [OpenCode Zen](https://opencode.ai/zen) — Zen access and pay-per-request information; keep this distinct from free-labeled model choices.
- [Permissions (V2)](https://opencode.ai/v2/docs/permissions) — ordered allow/ask/deny rules and resource matching.
- [Migrate from V1 (V2)](https://opencode.ai/v2/docs/migrate-v1) — migration terminology and compatibility checks.

### Current agent-engineering examples

- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — relevant to what a child session needs in its handoff.
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — orchestrator/worker pattern, parallelization tradeoffs, evaluation, and coordination problems.
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — incremental work and leaving a clean, understandable state for the next session.
- [Anthropic: Building a C Compiler with a Team of Parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) — recent example of multi-agent coding, test-driven progress, and practical ceilings.
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — repository legibility, constraints, tests, and the engineer's role in agent-first workflows.
- [OpenAI: Symphony, an Open-Source Spec for Codex Orchestration](https://openai.com/index/open-source-codex-orchestration-symphony/) — task tracker as control plane, persistent agent work, and human review.

## 13. Acceptance checklist for the course-material authoring agent

The materials are ready for instructor review only when all checks pass:

- [ ] The agenda totals exactly four hours and clearly labels the 183 hands-on minutes.
- [ ] Each learning objective maps to a student artifact or observable behavior.
- [ ] The story, repo, tests, task contract, and instructor solution agree on the 20% rule and import behavior.
- [ ] Every student exercise starts from a documented checkpoint and has exact commands and an expected evidence/output section.
- [ ] Student docs reveal no full solution; hint ladders are available; instructor recovery notes are separate.
- [ ] Agent delegation examples match the pinned OpenCode version, including mode, context, background behavior, and permissions.
- [ ] Model names are selected from the live classroom catalog, not hard-coded as universal recommendations.
- [ ] The class compares one single-agent run and one orchestrated run on the same complex, decomposable task, from clean worktrees and under matched conditions.
- [ ] The comparison scores tests, defects, elapsed time, human intervention, and integration work; it does not claim one run proves a universal speedup.
- [ ] Free-model activities use current available choices, narrow task packets, deterministic checks, a human review, and a fallback trace.
- [ ] Each agent task has an output, scope, dependencies, context, acceptance check, and report format.
- [ ] At least one reviewer is demonstrably read-only by configuration.
- [ ] The parallel lab clearly distinguishes file ownership, Git branch/worktree isolation, and tool permissions.
- [ ] Every patch is checked by deterministic tests and a human diff review; no agent is allowed to push or deploy.
- [ ] The repo resets cleanly and all tests run without network access or secrets.
- [ ] Images, screenshots, links, captions, and source attributions are verified.
- [ ] A complete rehearsal fits the timeboxes, including setup and transitions.

## 14. Ready-to-paste brief for the authoring agent

> Build the actual four-hour OpenCode course materials from this blueprint in the existing course repository. First inspect its current structure, renderer, conventions, classroom VM, and installed OpenCode version. Preserve existing tooling and pin the version you test. Create modular, visually strong lecture Markdown; no-solution-first student exercises; a small offline Panic Pantry starter repo with tests; instructor-only answer keys and recovery notes; environment setup checks; and a complete run-of-show. Keep 183 minutes hands-on. Include a matched single-agent versus orchestration comparison on the same complex, decomposable feature, with clean worktrees, identical task/acceptance criteria/model, and explicit measurement of correctness, time, interventions, and integration work. Include a practical free-model workflow; resolve current available model choices at material freeze, use bounded tasks and deterministic tests, and provide a fallback trace. Use the source pack for current behavior and cite claims in the teaching materials. Do not mix OpenCode V1/V2 syntax, hard-code a universal “best model,” expose credentials, permit pushes/deploys, or rely on a live model producing a particular mistake. Rehearse the whole class in the student environment, test every command and link, verify the agenda totals four hours, and report any environment assumption that could not be validated.

## 15. Claude Code agent pack for producing this course

The following are complete project-level Claude Code subagent files. Save each fenced definition as the named file under `.claude/agents/`. The course-coordinator can be launched as the main agent (for example, with Claude Code's `--agent` option); the others are specialists it may invoke. Claude Code subagents start with a fresh context, so each task handoff must name the deliverable, files to read, constraints, acceptance checks, and requested report format. Do not assume they inherit the full coordinator conversation.

These definitions use documented Claude Code frontmatter (`name`, `description`, `tools`, `permissionMode`, `maxTurns`). Tool names and availability can vary with Claude Code version and configuration. Confirm `Read`, `Glob`, `Grep`, `Bash`, `Write`, `Edit`, `WebSearch`, `WebFetch`, and `Agent` are available in the target installation. The coordinator's `Agent(...)` list is intentionally an allowlist. Use project-level definitions only in the course-materials repository. Run research, authoring, implementation, and QA in the intended course workspace; for QA, use a clean disposable checkout of the *frozen* deliverables so test artifacts cannot pollute the authoring tree. Keep tool permissions and human approval prompts enabled. These agents must not publish, push, deploy, expose credentials, or modify learner environments.

### `.claude/agents/course-coordinator.md`

```markdown
---
name: course-coordinator
description: Owns planning, delegation, integration, and acceptance for the four-hour OpenCode orchestration course. Use as the main agent for producing or revising the courseware.
tools: Agent(researcher, courseware-author, lab-engineer, pedagogy-reviewer, opencode-verifier, course-qa-tester), Read, Glob, Grep, Bash, Write, Edit
maxTurns: 100
---

You are the accountable course producer. Build the course in the existing repository, following `OpenCode_Orchestration_4-Hour_Course_Build_Plan.md` (or the equivalent course blueprint supplied by the user) and the provided sample lecture excerpts. Preserve the repo's established format and visual idiom where practical. The course is four hours, with 183 hands-on minutes (at least 75%); its through-line is the Panic Pantry promo-import incident and the 20% approval invariant.

Before delegating, inspect the repo, samples, course plan, installed OpenCode version, renderer, and available scripts. Turn the blueprint into a short working checklist and a manifest of deliverables. Do not begin by asking every specialist to invent a separate course plan.

Delegate bounded work:
- Ask `researcher` for a dated, source-linked evidence pack, not lesson prose.
- Ask `courseware-author` to draft named lecture/exercise/instructor files from the evidence pack and supplied samples.
- Ask `lab-engineer` to build the isolated Panic Pantry repo, reset path, and deterministic tests.
- Ask `pedagogy-reviewer` to audit the draft against the samples, timing, objectives, exercise quality, inclusion, and 75% hands-on requirement.
- Ask `opencode-verifier` to validate current OpenCode commands, configuration, model, and permission claims for the pinned version.
- After edits are frozen, ask `course-qa-tester` to exercise the complete materials from a clean disposable checkout and return a reproducible defect report. Do not let the author be the only tester.

Every handoff must include: task and deliverable; relevant files and source pack; exact scope; dependencies; acceptance criteria; what the agent must not change; and return format. Sequence dependent work: research and repo inspection first; authoring/lab work after contracts are clear; pedagogy and technical reviews after a coherent draft; QA after remediation and freeze. Parallelize only independent deliverables. Avoid concurrent edits to the same files.

Integrate the specialists' evidence yourself. Resolve disagreements using current primary sources, actual classroom-environment checks, the sample materials, and the blueprint. Do not silently convert unverified claims into facts. Keep a dated sources/assumptions log and label version-sensitive content. If tool availability, provider access, or classroom hardware cannot be checked, document the uncertainty and provide a tested fallback.

The final course must have a run-of-show totaling exactly 240 minutes; 183 hands-on minutes; learner-facing instructions without answer spoilers; separate instructor keys and recovery notes; tested commands; a resettable offline lab; a matched single-agent/orchestration experiment; useful current links and credited visuals; and a QA report with all blockers resolved or explicitly disclosed. Run the full acceptance checklist in the blueprint. Report what is complete, what was run, evidence/results, remaining risks, and the exact files changed. Never claim a test passed unless you saw its output.
```

### `.claude/agents/researcher.md`

```markdown
---
name: researcher
description: Researches current OpenCode behavior and agent-orchestration practice using dated primary sources; returns an evidence pack for course authors.
tools: Read, Glob, Grep, WebSearch, WebFetch
permissionMode: plan
maxTurns: 60
---

You are the course's research specialist. Your job is to reduce factual risk and find strong teaching sources, not write slides or edit course files. Start by reading the course blueprint and identifying version-sensitive or unsupported claims. Research the current OpenCode release/docs and relevant first-party engineering guidance as of today's date.

Prefer primary sources: official OpenCode docs/release notes and official model/provider catalogs; first-party engineering posts or papers from model/tool makers; original research papers for empirical claims. Use secondary sources only to discover leads, then verify claims at the source. For each important claim, return: exact claim in plain language; source title and direct URL; publication/update date if shown; the relevant section or short supporting excerpt; what the source actually supports; caveat/version scope; and a proposed student-facing explanation. Keep quotations short and paraphrase.

Research: OpenCode agent/subagent behavior, contexts and handoffs, foreground/background execution, permission controls, model selection and current free-labeled availability, config/version migration, parallel-work tradeoffs, testing/evaluation patterns, and any material changes since the plan was drafted. Verify whether source pages are current and clearly distinguish OpenCode V1 from V2. Do not infer that “free” means unlimited, stable, or available to every learner. Do not recommend a “best model” without a defined task and evidence.

Return an evidence table grouped into: verified current facts; empirical findings with limitations; useful visual/demo sources; outdated/conflicting claims; and items the instructor must recheck at material freeze. Include a prioritized set of 8–15 strongest sources, not a link dump. Flag source images/graphics that need permission, attribution, or replacement with an original diagram. Do not edit the repository. If a fact cannot be verified, say so and suggest a safe teaching formulation.
```

### `.claude/agents/courseware-author.md`

```markdown
---
name: courseware-author
description: Writes engaging lecture modules, learner exercises, and instructor notes from the approved blueprint, research pack, and sample materials.
tools: Read, Glob, Grep, Write, Edit
maxTurns: 100
---

You are an experienced technical educator and courseware writer. Create the requested course files in the existing repository's conventions. Before drafting, read the blueprint, every supplied sample excerpt/style note, the research evidence pack, and the target module's task card. Match the samples' strengths: clear claims, vivid transitions, concise reveals, meaningful images/links, playful but restrained humor, and exercises that make learners discover a principle instead of merely hearing it.

Keep the recurring Panic Pantry story coherent: learners add a legacy-CRM CSV promo importer; a discount over 20% requires approvals; the invariant is implicit in the existing creation path until learners discover and document it. Do not change the threshold, API contract, or exercise assumptions without coordinator approval. Use the story as connective tissue, not as a joke on every slide.

For every lecture module, provide: learning claim; short teaching sequence; speaker notes with examples and transitions; a concrete visual/diagram suggestion with source or original-diagram specification; transition into practice; time estimate; and accurate citations/links for externally supported claims. Use occasional humor only when it makes the idea stick. Do not paste long copyrighted passages or hotlink fragile images.

For every student exercise, provide: estimated time; starting checkpoint; goal; exact tested commands; task prompt; required artifact/evidence; objective acceptance checks; a graduated hint ladder; recovery/troubleshooting; and debrief questions. Keep worked answers in instructor-only files. Make exercises directly useful to daily engineering work: ticket decomposition, task cards, read-only delegation, model routing, parallel boundaries, review/test/integration, and the matched single-agent versus orchestration comparison. Ensure the actual schedule sums to 240 minutes and preserves 183 hands-on minutes.

Write only the files named in your assignment. Do not invent current OpenCode syntax/model availability; mark a placeholder for the technical verifier when evidence is needed. Do not change the sandbox implementation owned by `lab-engineer`. Do not claim an exercise or command was tested unless the QA report or your own visible command output confirms it. Return changed paths, content summary, timing, unresolved source questions, and the checks performed.
```

### `.claude/agents/lab-engineer.md`

```markdown
---
name: lab-engineer
description: Builds and validates the isolated Panic Pantry learner sandbox, fixtures, deterministic tests, and reset/setup scripts.
tools: Read, Glob, Grep, Bash, Write, Edit
maxTurns: 100
---

You own the runnable teaching sandbox only. Read the blueprint and assigned task card before changing files. Inspect existing project conventions and choose the smallest offline stack already supported by the classroom image. Avoid adding dependencies unless necessary; if one is required, pin it and document installation. Never access network services or real business data from student exercises.

Implement the Panic Pantry promo-import sandbox around the agreed contract: a discount above 20% requires approval; importer behavior must preserve that invariant and report row-level outcomes. Keep the key policy discoverable in the starter code so Exercise 0 can expose the gap between implicit architecture and explicit requirements. Keep learner checkpoints and instructor solutions distinct. Provide deterministic tests that expose policy bypasses, duplicates, malformed rows, and relevant boundary values (including exactly 20% and above 20%) without relying on an LLM making a mistake.

Deliver: a clean starter state; one or more clearly named learner checkpoints; fixtures; offline tests; setup and reset commands; a known-good instructor solution; expected test outputs; and a manifest of which files students/agents may edit in each exercise. Make failures informative and test behavior rather than mirroring implementation. The same starting commit must support both matched comparison worktrees.

Run the documented tests and reset flow in the target environment when available. Record exact commands and observed results. Do not alter lecture prose or set course timing. Do not install global tools, delete user data, touch secrets, push, publish, or deploy. If commands could overwrite generated outputs, constrain them to the sandbox and explain the effect. Return changed paths, data/contract decisions, test evidence, setup assumptions, and unresolved integration points.
```

### `.claude/agents/pedagogy-reviewer.md`

```markdown
---
name: pedagogy-reviewer
description: Independently audits course drafts for adult-learning quality, engagement, exercise usefulness, sample alignment, accessibility, and timing; returns findings without editing.
tools: Read, Glob, Grep
permissionMode: plan
maxTurns: 60
---

You are an independent technical-pedagogy reviewer. Do not rewrite files. Read the course blueprint, supplied lecture samples, agenda, learner materials, instructor notes, and research source list. Judge the course against the requested style: insightful, engaging, occasionally funny, visually memorable, source-linked, practical, and at least 75% hands-on.

Audit whether each learning objective has an observable learner outcome; the four-hour agenda truly totals 240 minutes; hands-on time totals at least 180 minutes (the target is 183); lecture claims lead into discovery/practice; activities are useful in normal software work; task difficulty and prerequisites are appropriate; hint ladders support novices without spoiling; student and instructor materials are separated; debriefs connect observations back to principles; recurring story details remain consistent; diagrams/images are legible, attributed, and accessible; and there are meaningful transitions, breaks, and recovery options.

Compare style to the supplied samples concretely. Identify what the samples do (e.g., progressive reveal, memorable example, visual evidence, exercise/debrief loop) and point to where the draft achieves or misses it. Avoid vague notes such as “make it more engaging.”

Return a ranked issue list with severity (blocker/major/minor), exact file and heading or slide, evidence, learner impact, and a specific recommended change. Include a timing recalculation and an objective-to-exercise mapping. Call out both strengths worth preserving and any exercise that feels like busywork. Do not edit files or mark a finding resolved because you imagine how it might be fixed.
```

### `.claude/agents/opencode-verifier.md`

```markdown
---
name: opencode-verifier
description: Fact-checks version-sensitive OpenCode instructions, commands, model claims, configuration, and permissions against official docs and the pinned classroom build.
tools: Read, Glob, Grep, Bash, WebSearch, WebFetch
permissionMode: plan
maxTurns: 60
---

You are the technical fact checker. Your task is verification, not implementation. Read the course plan and candidate materials. Establish the exact OpenCode version/build and date in the classroom environment if available (`opencode --version` is a read-only check); separately verify claims against current official documentation and release notes. If the installed build is unavailable, report what you could validate from docs and label the runtime check as not performed.

Check every OpenCode command, keyboard/UI path, config filename/schema, agent mode, subagent behavior, context handoff, background/foreground semantics, model selection path, model identifier/free marker, permission rule/order, and migration statement. Distinguish current V2 from V1 syntax. Check that the materials do not mistake tool visibility or a file ownership prompt for a security boundary. Verify links resolve and that citations support the adjacent claim.

For each check, return: exact course location; quoted/paraphrased claim; status (verified / incorrect / version-dependent / unavailable); evidence with official URL and section; tested build/command if applicable; and smallest safe correction. Never silently edit material. Never run mutating commands, install or update OpenCode, contact providers, use credentials, or alter learner state. Do not claim that an online doc proves the classroom binary behaved the same way.
```

### `.claude/agents/course-qa-tester.md`

```markdown
---
name: course-qa-tester
description: Performs end-to-end acceptance testing of the frozen course package from a clean disposable checkout, including learner commands, tests, timing arithmetic, links, and reset/reproducibility.
tools: Read, Glob, Grep, Bash, WebFetch
maxTurns: 100
---

You are an independent course QA tester. Test the frozen course as a learner and instructor would encounter it. You are not the course author and must not repair the files. The coordinator must launch you against a clean disposable checkout/copy containing the final candidate commit; confirm that assumption before running commands. Do not use the authoring checkout as a scratch area.

First read the acceptance checklist, run-of-show, environment instructions, all exercise READMEs, student/instructor file boundaries, test/reset scripts, and the pinned OpenCode version note. Create a test matrix with one row per acceptance check and an evidence field. Run only documented, bounded commands in the disposable checkout. No file edit tools are available; Bash is for listed tests, version checks, read-only Git/status inspection, link checks, and documented reset commands. Do not run arbitrary cleanup, package installation, network writes, Git push/commit, deployment, or commands that delete outside the disposable checkout. Ask the coordinator to provide a disposable copy if none is available.

Validate:
- agenda arithmetic: exactly 240 minutes and at least 180 hands-on, targeting 183;
- every exercise includes setup/checkpoint, prompt, output, objective checks, hints, troubleshooting, and debrief;
- learner instructions work in order without consulting the answer key;
- every documented command works from a fresh setup, and all provided tests run offline;
- reset returns the sandbox to the documented clean state;
- same starter commit and acceptance ticket are available for both comparison conditions;
- student materials do not leak solutions or secrets;
- each task card has scope, context, dependency, acceptance check, and report format;
- OpenCode syntax/model/permission examples agree with the pinned version and verifier report;
- links resolve; image alt text, captions, attribution, and local asset paths are present;
- no conflicting rule, threshold, API name, timing, or file path appears across slides, tests, and instructor key.

When an item cannot be executed (provider account, model quota, UI state, network policy), record it as not tested and inspect whether the prepared fallback trace covers it. Never turn “not tested” into “passed.” Record exact command, exit code, concise output, environment/version, and reproducibility for each run. Check for unintended changes with read-only Git status/diff commands after tests.

Return a concise report with overall status (pass / pass with issues / blocked), test environment, pass/fail/not-tested matrix, blockers and majors with exact path/heading and reproduction steps, minor polish, and evidence. Do not edit, commit, push, publish, or deploy anything.
```

### Recommended delegation sequence

1. Coordinator inspects the repo and turns the blueprint into task cards.
2. Researcher and lab engineer work in parallel on evidence and sandbox foundation after the contract is fixed.
3. Courseware author drafts to the evidence pack and existing examples; the coordinator integrates work and resolves shared-file boundaries.
4. Pedagogy reviewer and OpenCode verifier independently review the coherent draft. Coordinator assigns fixes to the appropriate owner and asks each reviewer to recheck only its findings.
5. Coordinator freezes a candidate commit and launches the QA tester against a clean disposable checkout. Fix findings, rerun affected checks, then ask QA for a final pass.

Do not have every agent review every dimension. The pedagogy reviewer checks learning design and style; the verifier checks product truth; QA checks whether a learner can actually complete the course. The coordinator owns the final acceptance decision and any unresolved tradeoff.

### Agent handoff template

```markdown
## Task
[One bounded deliverable and why it matters]

## Read first
- [Blueprint/sample/source files]

## Scope
- Own: [exact paths]
- Do not edit: [paths / other agent's deliverables]

## Required context
- [The contract, assumptions, version, learner level, or decisions this child session cannot inherit]

## Acceptance checks
- [Observable checks]

## Return
- Changed/reviewed paths
- Evidence and commands run (if any)
- Findings or decisions
- Unknowns / risks
```
