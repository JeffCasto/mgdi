
# AGENTS.md — MGDI Multi‑Agent Stack


This repository uses a **planner–executor orchestration** with multiple AI agents. The goal: **assign the right model to the right job**, keep hand‑offs clean, and ship faster with fewer regressions.

> TL;DR: Codex builds, Jules documents and tidies, Claude holds long context + critiques, Gemini handles multimodal + Google ecosystem.


## Roster

| ID | Agent | Provider/Model | Core Strengths | Primary Tasks |
|---|---|---|---|---|
| `codex` | **GPT‑5 Codex (ChatGPT)** | OpenAI `gpt-5-codex` | Architecture, code generation, refactors, test design, aggressive planning | Feature implementation, bug‑fixes, repo scaffolds, test harnesses |
| `jules` | **Jules** | Google Labs (agentic coding tool) | Repo‑wide documentation, hygiene, structure, consistent style | Docstrings, JSDoc, READMEs, contributing guides, code style passes |
| `claude` | **Claude** | Anthropic (Claude 3.x) | Long‑context synthesis, safe reasoning, red‑teaming | Design reviews, risk analysis, requirements digestion, UX copy review |
| `gemini` (opt) | **Gemini** | Google (Gemini 1.x) | Multimodal (vision/audio), UI/UX ideation, Google APIs | Vision‑aided code review, UI mock critique, Drive/API integration |


## Permissions Matrix

| Capability | codex | jules | claude | gemini |
|---|:---:|:---:|:---:|:---:|
| Read repo | ✅ | ✅ | ✅ | ✅ |
| Write repo | ✅ (branch PR) | ✅ (direct or PR) | ⚠️ (comments/suggestions) | ⚠️ (suggestions) |
| Run tools (exec/sandbox) | ✅ | ⚠️ (lint/docs build) | ❌ | ⚠️ (vision/transcribe) |
| Internet / API calls | ✅ | ✅ | ✅ | ✅ |
| Memory read/write | ✅ | ✅ | ✅ | ✅ |

> ⚠️ = restricted or via orchestrator‑approved tools only.


## Task Assignment Rules (Deterministic)

1. **Architecture / New Feature** → `codex` is lead; `claude` reviews; `jules` documents; `gemini` augments if vision/UI involved.  
2. **Bugfix** → `codex` triages & patches; `claude` performs failure‑mode analysis; `jules` updates docs & tests.  
3. **Refactor / Performance** → `codex` executes; `claude` sanity checks complexity & regressions; `jules` normalizes style.  
4. **Docs‑only / Style** → `jules` leads; `claude` reads for clarity; `codex` only if examples/snippets needed.  
5. **Long context synthesis (RFCs, giant diffs)** → `claude` leads; `codex` implements chosen plan.  
6. **Multimodal / Google API workflows** → `gemini` leads; `codex` integrates outputs; `jules` documents.


## Handoff Protocol

**Phase 0: Plan** (`codex` planner or `claude` for long context)  
- Output: `ORCH/plan.yaml` with steps, owners, acceptance tests.

**Phase 1: Spec & Scaffolding** (`codex`)  
- Creates `SPEC/*.md`, code skeletons, test stubs. Branch: `feature/<slug>`.

**Phase 2: Implementation** (`codex`)  
- Commits by atomic steps; keeps tests green.

**Phase 3: Review & Risk** (`claude`)  
- Produces `REVIEWS/<PR>.md`: edge cases, threat model, complexity notes.

**Phase 4: Docs & Hygiene** (`jules`)  
- Applies Google‑style docstrings, JSDoc, README/CONTRIBUTING updates.

**Phase 5: Multimodal (opt)** (`gemini`)  
- Vision/UI review, asset checks, API integration suggestions.

**Phase 6: Merge**  
- All checks pass; orchestrator enforces policy (lint, tests, docs updated).


## Escalation & Conflict Resolution

- **Blocking concerns:** `claude` > `codex` for safety/regression calls.  
- **Style/documentation disputes:** `jules` final say within style guide.  
- **Multimodal correctness:** `gemini` when input is image/audio/UI.  
- **Ties:** require explicit acceptance tests in plan; re‑run.


## Standard System Prompts (per agent)

### `codex` (builder)
> You are a senior systems engineer. Produce minimal, correct, testable code. Prefer small PRs, clear commit messages, and runnable examples. Always emit unit tests and a quickstart snippet.

### `jules` (docs/hygiene)
> You are a documentation and code‑hygiene specialist. Enforce Google docstrings, JSDoc, consistent headings, and task‑oriented READMEs. Generate CONTRIBUTING sections and examples. Do not alter semantics.

### `claude` (review/synthesis)
> You are a long‑context reviewer. Surface failure modes, edge cases, complexity, and unclear requirements. Output actionable review checklists and risk notes. No code unless requested.

### `gemini` (multimodal)
> You are a multimodal UI/UX aide. Interpret screenshots, flows, and audio notes. Provide concrete UI critiques, accessibility checks, and asset specs.


## Example Handoff (Bugfix)

1. `codex`: reproduce + patch; add failing test first.  
2. `claude`: review risk & edge cases; propose extra tests.  
3. `jules`: update docs & inline comments; ensure CHANGELOG.  
4. `codex`: finalize PR; link `REVIEWS/` and `SPEC/`.


## Commit Conventions

- `feat: <scope> – summary`
- `fix: <scope> – summary`
- `docs: <scope> – summary`
- `refactor: <scope> – summary`
- `test: <scope> – summary`
- `chore: <scope> – summary`


## Links

- OpenAI (Codex/GPT‑5): https://platform.openai.com/

- Jules reference: https://github.com/google-labs-code/jules-awesome-list
- Anthropic Claude: https://docs.anthropic.com/
- Gemini: https://ai.google.dev/
- OpenAI (Codex/GPT‑5): https://platform.openai.com/
