# GitHub Copilot courseware agent pack

This pack is for **GitHub Copilot Chat in VS Code**. It uses project-level custom agents in `.github/agents/*.agent.md` and direct delegation through Copilot's agent tool. It is tailored to create the four-hour *Orchestration Fundamentals for Agentic Development* course for OpenCode.

## Files

- `.github/copilot-instructions.md` — persistent course-wide standards.
- `.github/agents/course-coordinator.agent.md` — lead producer; directly invokes specialists, no handoffs.
- `.github/agents/researcher.agent.md` — current, source-backed research.
- `.github/agents/courseware-author.agent.md` — lectures, exercises, and instructor materials.
- `.github/agents/lab-engineer.agent.md` — runnable Panic Pantry sandbox and tests.
- `.github/agents/pedagogy-reviewer.agent.md` — independent teaching and sample-alignment review.
- `.github/agents/opencode-verifier.agent.md` — version-sensitive OpenCode fact checking.
- `.github/agents/course-qa-tester.agent.md` — independent end-to-end material testing.
- `COURSE_OUTLINE.md` — the supplied audience, prerequisites, objectives, and outline.
- `OpenCode_Orchestration_4-Hour_Course_Build_Plan.md` — the full detailed course build plan.
- `GHCP_Course_Build_Kickoff_Prompt.md` — the prompt to start the build.

## Install

1. Open the course repository in VS Code with GitHub Copilot Chat enabled.
2. Copy the `.github` directory from this pack into the repository root. Merge files if `.github` already exists; preserve existing repo instructions.
3. Copy the included plan, outline, and kickoff prompt into the repository root. Keep their filenames unchanged.
4. In VS Code Chat, choose the **GitHub Copilot** harness and confirm Course Coordinator and the specialists appear in the agent picker. The profiles use VS Code's `agents` allowlist for direct delegation.
5. Select **Course Coordinator**, use Agent mode, and paste the kickoff prompt. You do not need to click handoff buttons. Ensure your chosen model and tools support web research if you expect Researcher to verify current external sources. Tool availability depends on your Copilot/VS Code setup.

The specialist handoffs are suggested workflow buttons. The coordinator can also delegate to custom agents where your current VS Code/Copilot version exposes agent delegation. Run research and drafting in the course repository, then launch QA only against a clean copy/worktree of the frozen candidate.

## Important compatibility note

These are **VS Code Copilot custom agents**, not Claude Code subagents and not OpenCode agent definitions. The `agents` allowlist and direct delegation are configured for VS Code. GitHub.com cloud agent has a different feature set; adapt the profiles and recheck delegation and research behavior before using them there.

Tool lists are workflow controls, not a complete security boundary. In particular, the QA profile has shell access to run tests; follow its disposable-checkout rule and review commands before approval.

