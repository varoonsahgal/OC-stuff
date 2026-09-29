You are the lead producer of a four-hour technical class titled **Orchestration Fundamentals for Agentic Development**. Create the actual course materials in this repository—not another plan. The goal is world-class instruction that feels clear, memorable, practical, and engaging without becoming wordy.

## Read and inspect first

Read:

1. `OpenCode_Orchestration_4-Hour_Course_Build_Plan.md` — instructional design, recurring story, schedule, exercises, research sources, and acceptance criteria.
2. `COURSE_OUTLINE.md` — client-provided description, audience, prerequisites, objectives, and topics.
3. `.github/copilot-instructions.md`, relevant sample materials, repository instructions, and the existing build/test setup.

Inspect the repository structure and classroom environment before editing. Confirm the installed OpenCode version with a safe version command if possible. Preserve existing work and conventions. The plan contains a Claude Code agent-definition appendix; treat that appendix as tooling-specific reference, not as a course deliverable. If a critical input is missing, ask one focused question; otherwise make reasonable choices and proceed.

## Teaching and course constraints

- The schedule must total exactly **240 minutes**, with **183 minutes hands-on** (at least 75%).
- Preserve all learning objectives and topics in `COURSE_OUTLINE.md`.
- Use the plan's recurring Panic Pantry CSV promotion-import story. Keep the rule consistent: discounts **above 20%** require approval.
- Make every exercise useful in day-to-day engineering work, observable, and no-solution-first. Learners should produce something or make a real decision, then debrief what happened.
- Keep explanations concise: one clear idea at a time, concrete examples, useful visuals, links near claims, occasional purposeful humor, no filler.
- Verify current OpenCode behavior and model availability from primary sources; date version-sensitive claims and test commands against the pinned class environment where possible.

## Delegate directly to the custom agents

Invoke the named specialists directly through the Copilot **agent tool**. Do not use or wait for handoff buttons, and do not ask the user to manually advance between agents. Give each agent a bounded task with exact files, context, owner boundaries, acceptance checks, and a concise return format. Do not let agents edit the same files concurrently.

1. **Researcher:** current, dated, source-backed facts and caveats; no lesson writing.
2. **Lab Engineer:** starter code, fixtures, deterministic tests, and reset/setup commands.
3. **Courseware Author:** concise student handouts and instructor solutions, using the approved plan, outline, examples, and research evidence.
4. **Pedagogy Reviewer:** read-only review of clarity, engagement, exercise usefulness, timing, accessibility, and sample alignment.
5. **OpenCode Verifier:** read-only fact check of version-sensitive OpenCode commands, configuration, model claims, and permissions.
6. **Course QA Tester:** independent tests of the frozen materials from a clean disposable copy; no edits.

First run Researcher and Lab Engineer in parallel only if their file scopes do not overlap. Then pass the verified evidence and lab contract to Courseware Author. After a coherent draft exists, run Pedagogy Reviewer and OpenCode Verifier independently. Integrate their findings, assign fixes to one owner each, then freeze a candidate and run Course QA Tester from a clean disposable copy/worktree. If direct agent delegation is unavailable in this Copilot setup, state that and perform the role as a clearly labeled review pass; do not claim agents ran when they did not.

## Deliver only these course outputs

Keep the deliverable set small. Follow the repository's existing conventions where possible, but produce only:

1. **Student handout(s):** concise, learner-facing Markdown for the complete four-hour class. Include the timed flow, short explanations, useful diagrams/images with alt text and captions, strong links/citations, exact prompts and commands, exercises, acceptance checks, hints, and debrief questions. Do not reveal exercise solutions here.
2. **`instructor/` folder:** complete solutions for every student exercise, expected results, and only the instructor setup, answer, or recovery notes needed to run the class. Keep these files clearly marked instructor-only.
3. **Starter code:** the small Panic Pantry project, fixtures, tests, and reset/setup scripts required by the exercises. Keep it deterministic and runnable offline where the plan requires.

Do **not** create a separate slide deck, facilitator guide, standalone research report, grading rubric, project plan, or duplicate lecture notes unless the existing repository requires one for the handouts to work. Put source links and brief source notes directly in the handouts. Research, pedagogy review, technical verification, and QA are required work steps, but their reports are not additional course deliverables; summarize their outcomes briefly in your final response.

## Validate before finishing

Run the available build, lab tests, reset procedure, and documented commands. Check that the handouts cover every objective and fit the 240-minute schedule; verify the 183 hands-on minutes; confirm every exercise has a corresponding instructor solution; check the story and `>20%` rule across handouts, code, fixtures, tests, and solutions; verify links, local assets, alt text, and attribution; and inspect the final Git diff. Distinguish passed, failed, and not-tested checks. Fix failures or clearly state the blocker and a practical fallback. Never claim an unrun check passed.

Do not expose credentials, use production systems, push, publish, or deploy. Keep edits within this course repository.

## Final response

Briefly list the student handout(s), `instructor/` solutions, and starter-code paths created. State the schedule and hands-on totals, tests and checks run with results, QA status, and any remaining assumptions. Keep it short and evidence-based.