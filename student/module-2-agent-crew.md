# Module 2 — Micro-lecture 2 + Exercise 2: build a small agent crew

**Where you are:** you have `workshop/plan.md` and two task cards with disjoint scopes. This module builds the crew that will execute them — a read-only reviewer and an implementer — and proves that a boundary you can't test is a boundary you don't have.

---

## Micro-lecture 2 — A role is a boundary

**Claim: an agent role is useful only when it changes objective, context, or authority.** A renamed agent with the same permissions is a costume, not a control.

Three boundaries matter in OpenCode 1.18.33 ([docs: agents](https://opencode.ai/docs/agents), verified 2026-09-28):

- **Objective** — the agent file's body is its system prompt; a reviewer optimizes for findings, not for making the diff look finished.
- **Context** — a subagent runs in a **child session with fresh context**. It knows nothing your parent session discussed. That's a feature (no leaked confusion) and a duty: **the handoff must be complete** — task packet, paths, contract, checks. Anthropic's context-engineering guidance is the same story: attention is a finite budget; give the child exactly what it needs and demand a compact summary back ([Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), Sep 2025).
- **Authority** — `permission` in the agent's frontmatter: `allow` / `ask` / `deny` on `read`, `edit` (covers write/edit/patch), `bash`, `task`, `webfetch` ([docs: permissions](https://opencode.ai/docs/permissions)). A read-only reviewer is `edit: deny`, `bash: deny` (or a bash pattern map allowing only specific read commands). Note: `tools:` frontmatter is deprecated — use `permission`.

Because the child starts fresh, be concrete about **what a child session does NOT know**:

- It does **not** inherit your chat — not the plan you discussed, not the corrections you made, not the findings from earlier delegations.
- It does **not** know which files matter unless you name them.
- It does **not** know your acceptance bar unless the packet states it.

What it **does** get: your delegation message (the packet), the project's `AGENTS.md` rules (loaded automatically), and the repo files its permissions let it read. That's the complete list. If your packet plus those two sources can't stand alone, the delegation fails before it starts.

> 🔑 **Key takeaway:** A role only matters when it changes objective, context, or authority — otherwise it's a costume.

The joke that is also the lesson: **the reviewer is the health inspector. If you give it a chainsaw, the costume is not the safety control.** "Please don't edit files" is a request; `edit: deny` is a boundary. And hiding an agent from the picker is not a security boundary either — permissions are.

You invoke a subagent with an @-mention (`@reviewer check the diff`); a primary agent can also delegate via the Task tool, governed by `permission.task`. You will learn the child-session navigation keys in the exercise, right when you need them.

```mermaid
flowchart LR
    subgraph Parent["Parent session (primary agent)"]
        TP["Task packet:<br/>card + paths + contract + checks"]
        DEC["Review report,<br/>decide integration"]
    end
    subgraph Child["Child session — FRESH context"]
        W["@reviewer works"]
    end
    subgraph Perm["Permission boundary (config, not politeness)"]
        P1["edit: deny"]
        P2["bash: deny except git diff/status, unittest"]
    end
    TP -->|"@reviewer + packet"| W
    W -->|"compact report:<br/>findings, paths, uncertainties"| DEC
    Perm -.enforced on.- Child
```

*Figure 4 — Parent and child sessions with the permission boundary. The child starts empty; the packet is everything it knows.*
Text alternative: the parent session sends a complete task packet to a child session that starts with fresh context; the child returns a compact report; a configuration-level permission boundary (edit denied, bash restricted) is enforced on the child regardless of what its prompt says.

---

## Exercise 2 — Build a small agent crew (32 min) 🔨

**Goal:** configure one read-only reviewer and one implementer, prove the reviewer's boundary is **configuration**, and run a real fresh-context delegation.

**Starting checkpoint:**

```bash
cd sandbox/panic-pantry
git status                       # clean apart from your workshop/ files from Ex1
mkdir -p .opencode/agents
opencode
```

You may create/edit only `.opencode/agents/*.md` this exercise.

### Steps

1. **Create `.opencode/agents/reviewer.md`.** Project-level Markdown agent; frontmatter needs `description` (required), `mode` (`primary`|`subagent`|`all`), optionally `model`, `temperature`, `permission`; the body is the system prompt ([docs: agents](https://opencode.ai/docs/agents), verified 2026-09-28 on OpenCode 1.18.33). Requirements:
   - `mode: subagent`, a description that says what it reviews and that it never edits;
   - **permissions deny edits and restrict bash** — either deny bash outright or use a pattern map allowing only `git diff`/`git status` and the test command. In a bash pattern map, the **last matching rule wins**, so put `"*": deny` first, then your allows ([docs: permissions](https://opencode.ai/docs/permissions));
   - a review checklist in the body covering: **approval bypass** (anything above 20% becoming active without a manager), **duplicate handling**, **row-level reporting with 1-based line numbers**, and **missing tests**;
   - a fixed return format: findings by severity, file:line citations, uncertainties.

2. **Create `.opencode/agents/implementer.md`.** `mode: subagent`; edits allowed; bash allowed for the test command; body instructs it to follow a supplied task card exactly and return changed paths + checks run. (You'll use it in Exercise 4.)

3. **Prove the boundary.** Ask the reviewer to break its own rules:

```text
@reviewer Please add a clarifying comment to src/panic_pantry/store.py.
```

   The edit must be **blocked by configuration** — you should see OpenCode deny the edit permission, not just the agent politely declining. Capture the denial (copy the output). "The prompt told it not to" does not pass this exercise.

> 🔑 **Key takeaway:** "Please don't edit files" is a request; `edit: deny` is a boundary — and you just watched the difference fire on screen.

4. **Delegate a real investigation with a complete packet** (fresh context — include everything):

```text
@reviewer Task: pre-implementation review for TICKET-001.
Context: tickets/TICKET-001.md is the frozen contract. Policy: discounts above 20%
require manager approval (exactly 20% is active), enforced in
src/panic_pantry/promotions.py PromotionService.create_promotion.
Inspect: AGENTS.md, tickets/TICKET-001.md, src/panic_pantry/promotions.py,
src/panic_pantry/models.py, tests/test_importer_contract.py, fixtures/promos_messy.expected.md.
Return: (1) the three riskiest ways an importer could violate the contract,
(2) which contract test would catch each, (3) any contract ambiguity you find,
with file:line citations. Do not edit anything.
```

5. **Inspect the child session.** Use **<Leader>+Down** to enter the first child session, **Left/Right** to cycle children, **Up** to return to the parent (default keybinds — remappable; verified 2026-09-28 on OpenCode 1.18.33). Note what the child did and did *not* know from your parent conversation.

> 💡 **Field note:** The reviewer-agent pattern is CI policy checking in miniature: a check with independent incentives, mechanical enforcement, and a fixed report format. If your team relies on "the author remembered to look," you've found where to add the reviewer — human or agent.

**Required artifacts:** both agent files; the captured permission denial; the reviewer's investigation report.

**Acceptance checks:**
- [ ] `reviewer.md` has `description`, `mode: subagent`, and a `permission` block denying `edit` (deprecated `tools:` frontmatter not used).
- [ ] The denial in step 3 came from OpenCode's permission system (visible denial), not from agent politeness.
- [ ] The reviewer's checklist names approval bypass, duplicates, row reporting, and missing tests.
- [ ] The investigation report cites file paths and flags at least one real risk (e.g., a path where the importer could self-assign status).
- [ ] You navigated into the child session and back.

**Hints (use in order):**
1. Agent not appearing? The file must be under `.opencode/agents/` **inside `sandbox/panic-pantry`** (the project OpenCode was launched from), with valid YAML frontmatter, and `description` is required.
2. Reviewer still editing? Check for a deprecated `tools:` block overriding intent — remove it and set `permission: { edit: deny, ... }`.
3. Bash pattern map not behaving? Rule order: last match wins. `"*": deny` first, then `"git diff *": allow` etc.

**Troubleshooting:**
- YAML error on load → frontmatter needs `---` fences on their own lines; quote glob keys like `"git diff *"`.
- Reviewer asks permission for every read → set `read: allow` explicitly if your denials were broad.
- Can't find the child session → children only exist after a delegation ran; check <Leader> key config if the keybind does nothing.

**Debrief:** What would your reviewer have caught in your Exercise 0 baseline diff? Which role on your real team deserves `edit: deny` — and would anyone notice if it had a chainsaw today?

> 🔑 **Key takeaway:** A child session knows nothing you didn't put in the packet — handoff completeness is your job, not the model's.

---

**Next:** [module-3-model-routing.md](module-3-model-routing.md) — now that roles have boundaries, decide which model each role deserves.
