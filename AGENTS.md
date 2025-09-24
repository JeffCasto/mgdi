# AGENTS.md

This document defines the roles and responsibilities of the agents involved in this project.

## Agent Roles

| Agent | Role | Responsibilities |
|---|---|---|
| **Codex** | Planner / Builder | - Choose pipeline for feature implementation and bugfixes.<br>- Assign owners for tasks.<br>- Emit acceptance tests.<br>- Write code and tests for new features and bugfixes.<br>- Create initial specs for new features. |
| **Jules** | Docs Lead | - Write and maintain documentation, including READMEs, JSDoc, and docstrings.<br>- Ensure documentation is clear, complete, and up-to-date.<br>- Update changelogs for bugfixes. |
| **Claude** | Reviewer / Synthesizer | - Review code for risks, edge cases, and clarity.<br>- Synthesize information when the context is large.<br>- Handle repeated failures by reducing or replanning the task. |
| **Gemini** | Multimodal Specialist | - Handle tasks involving image and audio modalities.<br>- Perform asset intake and UX/accessibility critiques for multimodal UI.<br>- Provide concrete CSS/ARIA fixes for UI defects. |

## Conflict Resolution

- In case of conflicts, the final decision will be made by the agent with the most relevant expertise for the task at hand, as defined in the `ORCHESTRATION.md` routing rules.
- If the conflict cannot be resolved, it will be escalated to a human for a final decision.

## Addendum for Claude

- **Ambiguous Section:** The `_handle_stream` method in `backend/app/models/base.py` was intended to be a generic stream handler for all model providers. However, the response formats for OpenAI and Anthropic are different, making a single generic handler difficult to implement. The current implementation is specific to OpenAI. This should be refactored to be more generic or each provider should have its own stream handler.
