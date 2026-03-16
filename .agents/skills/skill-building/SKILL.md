---
name: skill-building
description: Manages the creation, optimization, and auditing of Antigravity skills. Follows official best practices for folder structure, YAML frontmatter, and progressive disclosure.
---

# Skill Building

## When to use this skill

- Generating a new skill from scratch using the **Discovery Interview**.
- Optimizing or auditing an existing skill for quality and predictable behavior.
- Troubleshooting skills that fail to trigger or produce inconsistent results.
- Implementing advanced patterns such as subagent execution or dynamic context.

For technical deep dives into YAML fields, permissions, and internal mechanics, see [reference.md](reference.md).

## Workflow: Build a New Skill

### 1. Discovery Interview
Before writing any files, the agent MUST conduct a structured interview to define the skill's scope. Ask questions one round at a time using `notify_user`.

- **Round 1: Goal & Name**
  - What specific workflow is being automated?
  - Recommended Name: Gerund form (e.g., `managing-logs`). Max 64 chars, lowercase, numbers, hyphens only.
- **Round 2: Triggers & Invocation**
  - What natural language phrases should trigger this?
  - Should it be manual (`/slash-command`), auto-invocable, or both?
- **Round 3: The "Degrees of Freedom" Process**
  - Walk through the step-by-step logic.
  - Identify where to use:
    - **Bullet Points**: For heuristics and high-freedom tasks.
    - **Code Blocks**: For static templates and medium-freedom tasks.
    - **Specific Bash Commands**: For fragile, low-freedom operations.
- **Round 4: Inputs & Outputs**
  - What files or APIs are required?
  - Where should the output be stored (e.g., `.agents/outputs/`)?
- **Round 5: Guardrails**
  - What are the failure modes?
  - Include "Plan-Validate-Execute" loops for complex state changes.

### 2. Implementation Checklist
Copy this checklist into your `task.md` when building:
- [ ] Create folder structure: `.agents/skills/<skill-name>/`
- [ ] Initialize `SKILL.md` with YAML frontmatter.
- [ ] Implement core logic using progressive disclosure (keep under 500 lines).
- [ ] Add supporting files in `scripts/`, `examples/`, or `resources/`.
- [ ] Test via natural language and direct `/` invocation.

## Workflow: Audit an Existing Skill

Audit any skill by checking these requirements:

- **Structure**:
  - [ ] Path is `.agents/skills/<name>/` or `~/.gemini/antigravity/skills/<name>/`.
  - [ ] `SKILL.md` is the entry point.
- **Frontmatter**:
  - [ ] `name` is a gerund (no "claude" or "anthropic").
  - [ ] `description` is in third person and under 1024 chars.
- **Degrees of Freedom**:
  - [ ] Fragile operations use specific shell commands.
  - [ ] Templates are in code blocks.
  - [ ] Heuristics use bullet points.
- **Complexity**:
  - [ ] File is under 500 lines.
  - [ ] Advanced logic is split into secondary files.

## Instructions for Antigravity

- **Forward Slashes**: Always use `/` in paths.
- **Black Boxes**: Treat helper scripts as black boxes; run `--help` if unsure of parameters.
- **Validation**: Always validate preconditions before writing files (e.g., check `list_dir` before `write_to_file`).

## Resources

- [Reference Documentation](reference.md)
- [Official Antigravity Docs](https://antigravity.google/docs/skills)
