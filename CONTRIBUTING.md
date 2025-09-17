# Contributing Guide — MGDI Multi-Agent Stack

This repo is maintained by **humans + AI agents** (Codex, Jules, Claude, Gemini).  
All contributions (human or agent) must follow the same pipeline rules.

---

## Branching & PR Flow

- **Never commit directly to `main`.**  
- Use feature branches: `feature/<slug>` or `fix/<slug>`.  
- PR titles must follow Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, etc.).

---

## Agent PR Labels

Apply these labels to PRs (agents will auto-apply where possible):

- `agent:codex` → Implementation or refactor
- `agent:jules` → Docs or hygiene update
- `agent:claude` → Review or risk notes
- `agent:gemini` → UI/UX multimodal feedback

---

## Human + Agent Workflow

1. **Humans create issues** describing work in plain language.  
   Example: _“Add OAuth2 client with tests + README example.”_

2. **Planner (Codex/Claude)** emits `ORCH/plan.yaml` with steps + acceptance tests.

3. **Agents execute tasks**:
   - Codex implements
   - Claude reviews & risk-checks
   - Jules documents
   - Gemini critiques UI/UX (optional)

4. **Humans review final PR** before merge.  
   Agents cannot self-merge.

---

## Checklists

**Every PR must include:**
- ✅ Passing CI (lint + tests)
- ✅ Docs updated (`README.md`, `CHANGELOG.md`)
- ✅ Risk review present (if non-trivial)
- ✅ Acceptance tests satisfied (`ORCH/plan.yaml`)

---

## CI Enforcement

Pull Requests without:
- Failing tests  
- Missing docs updates  
- Missing risk review (for features)  
will be **blocked** by GitHub Actions.

---

## Agent Invocation Notes

- Codex → test-driven, small commits
- Jules → docstrings, JSDoc, style only
- Claude → reviews, edge cases, risks
- Gemini → multimodal UX checks

---

⚡ *This repo is an orchestration playground. Treat AI agents like teammates, but keep humans in the loop.*
