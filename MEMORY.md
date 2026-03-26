# QA Multi-Agent System — Long-Term Memory

## Repo
https://github.com/jolinliwip101-png/qa-multi-agent

## System
- **Stack:** Python 3.12+ · Playwright · pytest · REST APIs · CI/CD · OpenClaw + OpenViking
- **Target:** automationexercise.com (API + UI smoke)
- **Agents:** orchestrator, test-gen, self-healer, fail-analyst, api-tester, reporter, ci-manager
- **Memory:** OpenViking (auto-capture on, recall manual, no direct store)

## Architecture
- Shared `~/qa-multi-agent/` for all QA code
- Isolated agent state: `~/.openclaw/agents/{agent}/workspace/`
- orchestrator = memory gatekeeper
- Raw logs → `memory/YYYY-MM-DD.md`; long-term knowledge → this file

## Coverage Map
| Area | Status | Notes |
|------|--------|-------|
| API smoke | ✅ | pytest + requests |
| UI smoke | ✅ | Playwright |
| CI pipeline | 🔧 | scripts + workflow |
| Reporting | ✅ | generate-report.sh |

## Flakiness Scores
| Test | Score | Pattern |
|------|-------|---------|
| (none recorded) | — | — |

## Agent Performance
| Agent | Role | Notes |
|-------|------|-------|
| orchestrator | Coordination + memory gatekeeping | New role added 2026-03-25 |
| test-gen | Test creation | Lean, deterministic output |
| self-healer | Minimal fixes | Scope-bounded, no symptom-patching |
| fail-analyst | RCA + classification | 5-type taxonomy |
| api-tester | Contract validation | 14 endpoints |
| reporter | Status + memory candidates | Structured output format |
| ci-manager | Pipeline reliability | Retry + signal quality |

## Validated Patterns

### Failure Taxonomy
- **app_bug** — product/endpoint defect → escalate
- **test_issue** — incorrect test logic → self-healer
- **env_issue** — infra/setup problem → reporter flag
- **timing_issue** — flaky by design → test-gen harden
- **data_issue** — test data problem → test-gen fix

### Orchestration Workflow
```
orchestrator → test-gen → api-tester → fail-analyst
                                       ↓
                    app_bug    → reporter (escalate)
                    test_issue → self-healer (fix + re-run)
                    env_issue  → reporter (flag)
                    timing/data → test-gen (harden)
                                       ↓
                               reporter → PASS / PARTIAL / FAIL
```

### Self-Healer Rules
- Smallest safe fix only
- Never weaken tests to pass
- Scope-bounded: defect boundary only

### Reporter Memory Candidate Format
```
Memory candidate:
- type: <pattern|convention|fix|architecture>
- title: <short descriptor>
- value: <what makes it reusable>
- confidence: <high|medium>
- rationale: <why this belongs in long-term memory>
```

## Project Conventions
- Smoke tests: fast (< 30s total), deterministic, isolated
- No secrets in test code
- Scripts use `set -e` for safety
- Report output: `reports/` directory
- Daily logs: `memory/YYYY-MM-DD.md`
- Long-term: this file (MEMORY.md)

## Framework Decisions
| Decision | Date | Rationale |
|----------|------|-----------|
| Isolated agent workspaces | 2026-03-25 | Auth/state isolation per OpenClaw docs |
| Auto-capture on, recall manual | 2026-03-25 | Reduces token burn; recall only when needed |
| bubblewrap 0.11.1 symlink | 2026-03-25 | Codex sandbox requires `--argv0` support |
| text-embedding-3-small | 2026-03-25 | WolfAI key access confirmed |

---

## Stack Decision (2026-03-27)

### Canonical UI Test Stack
- **Python + Playwright + pytest + Allure**
- Page Object Model (POM) in `pages/`
- Centralised selectors in `locators/registry.py`
- Fixtures in `conftest.py`
- Tests in `tests/ui/test_ui_smoke.py`

### Canonical API Test Stack
- **Python + httpx + pytest + Allure**
- Tests in `tests/api/test_api_smoke.py`

### Archived (do not regenerate)
- `tests/ui/_archive/smoke.spec.ts` — TypeScript Playwright test (retired)
- `_archive/playwright.config.ts.legacy` — orphaned TS config (retired)
- TS Playwright / Node.js test runner is NO LONGER ACTIVE
- Do not generate TypeScript test files for this repo

### Entry Points
- `scripts/run-smoke.sh` — full smoke suite (UI + API)
- `scripts/run-ui-smoke.sh` — UI only
- `scripts/run-api-smoke.sh` — API only
