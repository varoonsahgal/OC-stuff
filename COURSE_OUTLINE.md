# Orchestration Fundamentals for Agentic Development

This course introduces the core skills for planning, delegating, and coordinating agentic development work with **OpenCode**. Participants learn how to break complex features into agent-ready units of work, select appropriate models and reasoning levels for different tasks, and coordinate multiple agents working on related development activities.

The course focuses on practical orchestration patterns, including defining specialized agents, delegating work to subagents, managing parallel work, establishing appropriate file and Git boundaries, and integrating results into a coherent solution.

## Audience

- Developers moving from single-prompt AI assistance to orchestrating agents across larger development tasks
- Technical leads and engineers responsible for planning and delegating agentic development work
- Developers interested in using specialized AI agents for planning, implementation, research, testing, and review

## Prerequisites

- Experience using OpenCode or a similar AI coding assistant for development tasks
- Working knowledge of Git, including creating branches and merging changes
- Comfort navigating and running commands from a terminal
- Basic familiarity with software development workflows

## Learning objectives

After this course, participants will be able to:

- Break complex features into units of work suited for agent execution
- Write clear task specifications and acceptance criteria for agents
- Distinguish between work that should remain in the primary agent and work that should be delegated to specialized subagents
- Select an appropriate model or reasoning level based on task complexity, risk, speed, and cost
- Configure specialized OpenCode agents for different development responsibilities
- Delegate work to OpenCode subagents and coordinate parallel agent execution
- Manage context, file boundaries, and Git workflows across related agent tasks
- Review, validate, and integrate results produced by multiple agents

## Duration

4 hours

## Course outline

### 1. Decomposing Complex Features for Agent Execution

- Moving from prompting an assistant to orchestrating development work
- What makes a task a good candidate for autonomous agent execution
- Identifying tasks that are too large, ambiguous, or tightly coupled
- Breaking a feature into smaller, verifiable units of work
- Defining clear task boundaries
- Writing effective task specifications
- Defining acceptance criteria an agent can verify
- Identifying dependencies between subtasks
- Sequencing work that depends on other agent outputs
- Identifying work that can safely happen in parallel
- Determining what context each agent actually needs

**Hands-on:** Given a larger software feature, decompose it into a set of agent-ready tasks with clear boundaries, dependencies, and acceptance criteria.

### 2. Understanding Agents and Delegation in OpenCode

- Understanding the role of the primary agent
- Understanding OpenCode subagents
- Primary agents versus specialized subagents
- How subagents operate in separate child sessions
- Delegating work from a primary agent to a subagent
- Invoking specialized agents directly
- Allowing the primary agent to select appropriate subagents
- Foreground versus background delegated work
- Navigating between parent and child agent sessions
- Deciding when delegation adds value versus keeping work in the current session

Common agent responsibilities may include planning, codebase exploration, implementation, research, testing, code review, and security review.

**Hands-on:** Delegate separate analysis, implementation, and review tasks to specialized OpenCode agents and inspect the resulting child sessions.

### 3. Designing Specialized OpenCode Agents

- Why different tasks benefit from different agent roles
- Defining an agent's responsibility and scope
- Creating custom OpenCode agents
- Writing effective agent instructions
- Defining which tools an agent can use
- Using read-only agents for exploration and review
- Giving implementation agents controlled write access
- Preventing unnecessary or dangerous agent actions
- Controlling which subagents another agent may delegate to
- Designing reusable agent roles for common development workflows

**Hands-on:** Configure specialized agents for roles such as implementation and code review, with different instructions and permissions.

### 4. Model Selection Strategy for Agentic Development

- Why every development task does not require the same model
- Matching model capability to task complexity and risk
- Balancing reasoning quality, latency, and cost
- Using faster or lower-cost models for well-defined tasks
- Using stronger reasoning models for architecture, debugging, and ambiguous problems
- Understanding model variants and reasoning levels
- Selecting models within OpenCode
- Assigning different models to different agents
- Knowing when to escalate a task to a stronger model
- Avoiding unnecessary use of expensive models for routine work

**Hands-on:** Assign different models or model configurations to specialized agents and compare their suitability for several development tasks.

### 5. Orchestrating Parallel Agent Work

- Identifying work that can safely execute concurrently
- Using OpenCode subagents for parallel units of work
- Running delegated work in background child sessions
- Keeping the primary agent available while delegated work executes
- Managing shared context between agents
- Avoiding unnecessary context sharing
- Establishing file ownership and modification boundaries
- Preventing multiple agents from conflicting over the same code
- Using Git branches or worktrees to isolate independent development work when appropriate
- Coordinating tasks that share dependencies
- Tracking which agent is responsible for which deliverable

**Hands-on:** Orchestrate multiple agents working on independent parts of the same feature while maintaining clear task and file boundaries.
