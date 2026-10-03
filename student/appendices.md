# Appendices

## Appendix A — Objective coverage map

Every objective and topic from [COURSE_OUTLINE.md](../COURSE_OUTLINE.md):

| Outline objective / topic area | Where covered |
|---|---|
| Break complex features into agent-ready units; boundaries; task size | ML1 (bad-split Predict: split by file) ([module 1](module-1-decomposition.md)) |
| Write task specifications and acceptance criteria | ML1 (the 6-line card), Ex1 Steps 3–5, including the Stranger Test in Step 5 ([module 1](module-1-decomposition.md)) |
| Identify dependencies, sequencing, safe parallel work, needed context | ML1 (Fig. 2), Ex1 (plan's Order line; critical-path Level up), ML4, Ex4 ([module 1](module-1-decomposition.md), [module 4](module-4-parallel-run.md)) |
| Prompting → orchestrating; too-large/ambiguous/coupled tasks | Opening, Ex0 ([module 0](module-0-baseline.md)) |
| Primary agent vs subagents; child sessions; fresh context | ML2, Ex2 ([module 2](module-2-agent-crew.md)) |
| Delegating (Task tool) vs invoking directly (@-mention); letting primary pick subagents | ML2, Ex2, Ex4 ([module 2](module-2-agent-crew.md), [module 4](module-4-parallel-run.md)) |
| Foreground vs background delegated work | ML4 — explained + recorded instructor demo (experimental in pinned V1; not exercised live) ([module 4](module-4-parallel-run.md)) |
| Navigating parent/child sessions | ML2, Ex2 step 5 ([module 2](module-2-agent-crew.md)) |
| When delegation adds value vs keeping work local | Ex1 Step 1 (keep or delegate), capstone step 2 ([module 1](module-1-decomposition.md), [module 5](module-5-capstone.md)) |
| Creating custom agents; instructions; roles; reusable designs | Ex2 (reviewer + implementer) ([module 2](module-2-agent-crew.md)) |
| Tool/permission control; read-only reviewer; controlled write access; preventing dangerous actions; controlling delegation targets | ML2, Ex2 (`permission`: `edit`, `bash`); `permission.task` governs the Task tool in Ex4 ([module 2](module-2-agent-crew.md), [module 4](module-4-parallel-run.md)) |
| Model capability vs complexity/risk; reasoning-quality/latency/cost; variants and effort levels; escalation; avoiding expensive-model waste | ML3, Ex3 ([module 3](module-3-model-routing.md)) |
| Selecting models in OpenCode; per-agent models | ML3 (`/models`, per-agent `model`), Ex3 ([module 3](module-3-model-routing.md)) |
| Parallel orchestration; shared context; file ownership; conflict prevention; branches/worktrees; deliverable tracking | ML4, Ex4 ([module 4](module-4-parallel-run.md)) |
| Review, validate, integrate multi-agent results | ML5, Ex4 integration, capstone ([module 4](module-4-parallel-run.md), [module 5](module-5-capstone.md)) |

## Appendix B — Command crib sheet

```bash
python3 -m unittest discover -s tests -v          # canonical test gate (repo root)
python3 -m unittest tests.test_importer_contract -v
bash scripts/reset.sh                             # restore seed data, remove importer
bash scripts/check_env.sh                         # environment + suite check
bash sandbox/setup.sh                             # (pack root) rebuild worktrees — DISCARDS worktree work
opencode models                                   # list model IDs (CLI)
opencode stats                                    # token/cost data
# TUI: /models picker · Tab = Build/Plan · @agent = invoke subagent
# <Leader>+Down = first child session · Left/Right = cycle children · Up = parent (default keybinds — remappable)
# <Leader> = ctrl+x by default (press, release, then the next key)
# /new or <Leader>+n = fresh session · /models or <Leader>+m = model picker · /sessions or <Leader>+l = session list
# ctrl+t = cycle model variants (effort) · ctrl+p = command palette · esc = interrupt · /connect = add a provider
git switch -c scratch/ex3                         # throwaway branch; delete later with git branch -D
```

**Agent file skeleton** (`.opencode/agents/<name>.md`; the file name is the agent name):

```markdown
---
description: <what it does and what it never does — primaries route on this>
mode: subagent                 # omit and it defaults to "all"
permission:
  edit: deny                   # allow | ask | deny
  bash:
    "*": deny                  # catch-all FIRST — last matching rule wins
    "git diff*": allow
---
<system prompt: objective, checklist, return format>
```

## Appendix C — Sources

- OpenCode agents: https://opencode.ai/docs/agents · permissions: https://opencode.ai/docs/permissions · models: https://opencode.ai/docs/models · Zen: https://opencode.ai/docs/zen · CLI: https://opencode.ai/docs/cli · rules: https://opencode.ai/docs/rules (all verified 2026-09-28 against OpenCode 1.18.33)
- Anthropic, *How We Built Our Multi-Agent Research System* (Jun 2025): https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, *Effective Context Engineering for AI Agents* (Sep 2025): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- OpenAI, *Harness Engineering* (Feb 2026): https://openai.com/index/harness-engineering/

Model catalogs and free-model availability change; anything dated above should be rechecked before you rely on it after class.

## Appendix D — Image credits

| Image | Source | License |
|---|---|---|
| [images/kitchen-pass.jpg](images/kitchen-pass.jpg) | MarkBuckawicki, "Restaurant Kitchen expo station," [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Restaurant_Kitchen_expo_station.jpg) (resized) | CC0 1.0 |
| [images/opencode-tui.png](images/opencode-tui.png) | [OpenCode project](https://github.com/sst/opencode) README screenshot (resized) | MIT License, © 2025 opencode |
| [images/critical-path.png](images/critical-path.png) | Illes, "5n PERT graph with critical path," [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:5n_PERT_graph_with_critical_path.svg) (rasterized, cropped) | Public domain |
| [images/swiss-cheese-model.png](images/swiss-cheese-model.png) | Davidmack, "Swiss cheese model of accident causation," [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Swiss_cheese_model_of_accident_causation.png) (resized) | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) |

Images are stored locally so the handout works offline, like the rest of the course.

---

Back to the [course index](README.md).
