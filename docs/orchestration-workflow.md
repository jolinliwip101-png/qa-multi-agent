# QA Orchestration Workflow

## Scope
End-to-end smoke test workflow across 6 agents targeting **automationexercise.com**.

---

## Agent Responsibilities

| Agent | Role |
|-------|------|
| **orchestrator** | Decompose, coordinate, validate final output |
| **test-gen** | Generate deterministic smoke tests (Playwright + pytest) |
| **api-tester** | Execute API smoke suite, report contract violations |
| **fail-analyst** | Diagnose failures, classify root cause |
| **self-healer** | Apply minimal fixes for test/script failures |
| **reporter** | Consolidate and publish final status report |

---

## Workflow

```
[1] orchestrator  → decompose goal into tasks
[2] test-gen      → generate smoke tests
[3] api-tester   → run API smoke suite
[4] fail-analyst  → classify each failure
            │
            ├── app_bug     → reporter: log & escalate
            ├── test_issue   → self-healer: fix test
            ├── env_issue    → reporter: flag infra
            ├── timing_issue → test-gen: retry/harden
            └── data_issue   → test-gen: fix test data
            │
[5] self-healer  → apply fix, re-run affected tests
[6] reporter     → publish final status + evidence
```

---

## Step Details

### Step 1 — Orchestrator
- Break down request into discrete tasks by severity
- Assign task ownership per agent
- Define acceptance criteria per task
- Track pass/fail state

### Step 2 — Test-Gen
- Create/update Playwright (`tests/ui/`) and pytest (`tests/api/`) smoke tests
- Tests must be: deterministic, isolated, fast (< 30s total)
- Each test includes: description, assertions, failure output path

### Step 3 — API Tester
- Run `./scripts/run-api-smoke.sh`
- Validate: HTTP 200, correct schema, no contract drift
- Collect: pass/fail counts, error messages, response times

### Step 4 — Fail Analyst
- For each failure, classify:
  - **app_bug** — product/endpoint defect (escalate)
  - **test_issue** — incorrect test logic (hand to self-healer)
  - **env_issue** — setup/infra problem (flag)
  - **timing_issue** — flaky by design (retry or harden)
  - **data_issue** — test data problem (fix test data)
- Output: ranked RCA per failure with evidence

### Step 5 — Self-Healer
- Applies minimal fix only to confirmed **test_issue** failures
- Fix must not change product behavior
- Re-run affected tests to confirm
- Document: what changed, why

### Step 6 — Reporter
- Consolidate: pass/fail summary, RCA list, healed items
- Publish to `reports/smoke-report.md`
- Output decision-ready verdict: **PASS / PARTIAL / FAIL**

---

## Exit Criteria

| Outcome | Condition | Action |
|---------|-----------|--------|
| **PASS** | All smoke tests green | Report → done |
| **PARTIAL** | Some failures healed | Report + open app_bug issues |
| **FAIL** | Unhealable failures | Report → escalate |

---

## Assumptions

- All agents share `~/qa-multi-agent/` as the working directory
- Each agent has its own isolated OpenClaw workspace (agent state per `~/.openclaw/agents/{agent}/workspace/`)
- Smoke tests target **automationexercise.com** — network access required
- Python 3.12+ with `venv/` and `node_modules/` pre-installed
- Playwright browsers installed (`npx playwright install`)
- Secrets/tokens are NOT stored in test code
