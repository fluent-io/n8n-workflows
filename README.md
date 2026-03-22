# n8n-workflows

n8n automation workflows for `fluent-io` — PR review, CI failure handling, merge notifications, and auto-review triggers.

## Workflows

| File | Purpose |
|------|---------|
| `wf-pr-trigger-auto-review-on-push.json` | Fires on PR push/open → dispatches PR Review GitHub Actions workflow |
| `wf-review-pr-review-agent-enhanced.json` | Receives reviewer bot result → retry logic → wakes builder agent or escalates |
| `wf-ci-ci-failure-wake-agent.json` | CI check failure → wakes builder agent |
| `wf-merge-pr-merged-wake-agent.json` | PR merged → notifies agent |

## GitHub Webhooks

| Hook ID | Events | URL |
|---------|--------|-----|
| 602116420 | pull_request | /webhook/github-pr-push |
| 602012518 | pull_request_review | /webhook/github-review |
| 602012520 | check_run | /webhook/github-ci |
| 602012521 | pull_request | /webhook/github-merge |

All routes via Cloudflare tunnel: `flow.getonit.io` → n8n on G10 (port 5678)

## Scripts

```bash
# Export current n8n state to this repo
python3 scripts/export.py

# Import/update workflows from this repo into n8n
python3 scripts/import.py
```

## Setup

- n8n: `http://192.168.68.140:5678`
- API key in `secrets.md`
