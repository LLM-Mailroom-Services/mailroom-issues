# Changelog

All notable changes to this repository's own files (docs, templates, the
label manifest, and governance tooling) are documented here. Issue numbers
refer to this repo's issues.

## [Unreleased]

### Added — cross-repo evaluation reports

- `reports/MASTER-REPORT.md` — current status and research findings for the
  API leg (eval-environment), the Modal + vLLM leg (local-mailroom-sandbox,
  SAND-032) and the ModernBERT intake classifier (mailroom-ml), with the
  cross-leg verdict and the report-audit record.
- `reports/COST-COMPARISON-MODAL-VS-API.md` — Modal L4 vs hosted API cost per
  document and per 0.1 quality, batch and warm-fleet break-even, sorter routes,
  spend and caveats.
- `reports/MODAL-VLLM-GPU-REPORT.md` — the Modal + vLLM leg's GPU economics
  (SAND-032): cost per token for all 24 runs and against the hosted API, the
  spend ledger broken into busy, idle, boot and out-of-run time, client-slot
  occupancy and per-replica vLLM metrics, and the effect of the second L4
  (scale-out, routing, admission, load balance).
- `reports/figures/` — cost and GPU figures drawn for these reports
  (`cost/`, `gpu/`), plus verbatim copies of the source repos' charts;
  `reports/README.md` indexes them.
- `README.md` — new Reports section and `reports/` in the repository layout.

### Added — repository scaffold (initial)

- `README.md` — canonical entry point: what this hub is, what belongs here,
  the constellation, templates, and governance tooling. Rewritten from the
  one-line placeholder.
- `AGENTS.md` — agent navigation rules: the ten laws, triage duties,
  specialist roster, commands, and label-taxonomy summary.
- `docs/CONSTELLATION.md`, `docs/ROUTING.md`, `docs/LABELS.md`,
  `docs/LIFECYCLE.md` — ecosystem map, filing decision tree, label reference,
  and the triage flow.
- `.github/labels.json` — declarative label taxonomy (source of truth),
  codifying the existing repo labels and adding the `type/epic`, `type/rfc`,
  `priority/*`, and `status/*` routing families.
- `.github/ISSUE_TEMPLATE/` — `config.yml`, `bug_report.yml`,
  `feature_request.yml`, `task_todo.yml`, `epic.yml`, `rfc.yml`.
- `.github/PULL_REQUEST_TEMPLATE/pull_request.yml` — hub governance PR form.
- `.github/workflows/issue-governance.yml` — label-manifest audit (PR) and
  sync (merge to main) gate.
- `scripts/labels.py` — `audit`/`sync` driver for the label manifest.
- `CHANGELOG.md`, `LICENSE` (MIT), `.gitignore`.