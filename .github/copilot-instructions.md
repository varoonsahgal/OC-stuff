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
- Teach in short bursts followed by learner action. Preserve at least 75% hands-on time; target the plan's 183 of 240 minutes.
- Use the Panic Pantry promotion importer throughout. Keep the `>20%` approval rule, code, tests, student prompts, instructor key, and explanations consistent.
- Make learner exercises no-solution-first. Put full answers and recovery keys in clearly instructor-only files.
- Use diagrams and screenshots when they clarify workflow, boundaries, or evidence. Prefer original course-specific diagrams. Include alt text, captions, source links, and attribution.
- Use restrained humor to help ideas stick; never let it obscure the engineering lesson.

## Build and evidence rules

- Use the repository's existing format and build/test tools. Keep the teaching sandbox small and offline where the plan requires it.
- Every delegated task needs a named deliverable, scope, dependency, acceptance check, and return format.
- Do not let multiple agents edit the same files at once. Review every handoff and integrate results deliberately.
- Run documented commands and tests; record exact commands and outcomes. Never say something passed if it was not run.
- QA the frozen candidate from a clean disposable checkout. Verify schedule arithmetic, exercise steps, test/reset paths, story/contract consistency, links, visuals, and OpenCode version accuracy.
- Do not expose secrets, request credentials, run against production, push, publish, or deploy.
- Report uncertainties plainly. A useful fallback trace is better than depending on a live provider, model, or UI state that may be unavailable.
