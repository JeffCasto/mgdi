
# ORCHESTRATION.md — Planner–Executor Spec

This document defines the **deterministic orchestration** for ChatGPT (GPT‑5 Codex), Jules, Claude, and Gemini.

## Overview

- **Planner**: Chooses pipeline, assigns owners, emits acceptance tests.
- **Executors**: Agents carry out steps within guardrails.
- **Observer**: Logs artifacts, enforces policies (tests/docs/lint).

## Routing Rules

| Condition | Route |
|---|---|
| `tokens_in_context > 60k` or `> 20 files` | `claude` (synthesis first) |
| `input_modality in {image,audio}` | `gemini` lead; `codex` integrate |
| `task contains {"perf","refactor","scaffold","api client","sdk"}` | `codex` lead |
| `task contains {"docs","readme","jsdoc","docstring"}` | `jules` lead |
| `risk or compliance` | `claude` review mandatory |

## Pipeline Templates

### A. Feature Implementation
1. **Plan** (`codex`) → `ORCH/plan.yaml`
2. **Spec** (`codex`) → `SPEC/feature_<slug>.md`
3. **Build** (`codex`) → code + tests
4. **Review** (`claude`) → `REVIEWS/<PR>.md`
5. **Docs** (`jules`) → README/CONTRIBUTING updates
6. **Merge** (observer enforces all checks)

### B. Bugfix
1. Repro + failing test (`codex`)
2. Patch + green tests (`codex`)
3. Risk/edge review (`claude`)
4. Docs changelog (`jules`)

### C. Docs‑Only
1. Scope & style map (`jules`)
2. Cross‑file pass (`jules`)
3. Clarity review (`claude`)

### D. Multimodal UI
1. Asset intake (`gemini`)
2. UX critique + a11y (`gemini`)
3. Implementation (`codex`)
4. Docs (`jules`)

## Guardrails

- **No direct force‑push** from agents. PRs only (except `jules` docs micro‑passes if configured).  
- **Tests must pass** (`pytest`/`vitest` etc.).  
- **Linters** gate CI (flake8/ruff, eslint, prettier).  
- **Docs present** (README updated when public API changes).

## Observability

- Store artifacts in: `SPEC/`, `REVIEWS/`, `ORCH/`, `REPORTS/`  
- Log per‑step metadata: `reports/<iso8601>.json` (agent, tokens, status)

## Security

- Tool access is registry‑based; deny by default.  
- Sandboxed exec with time/memory limits.  
- Redaction of secrets; secret scanning in CI.  

## Failure Policy

- Step fails → orchestrator retries once with smaller context + explicit constraints.  
- Repeated failure → escalate to `claude` for reduction/replan.  
- Conflicts → tie‑break per AGENTS.md.

- **Multimodal (gemini):** _“Analyze these screenshots; list UI defects and a11y issues; provide concrete CSS/ARIA fixes.”_
