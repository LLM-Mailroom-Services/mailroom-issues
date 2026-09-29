# Changelog

All notable changes to this repository's own files (docs, templates, the
label manifest, and governance tooling) are documented here. Issue numbers
refer to this repo's issues.

## [Unreleased]

### Added — frozen v1 prompt reference & lineage docs

- `docs/PROMPTS.md` — constellation prompt lineage: frozen v1 vs GEPA mutation
  heads vs production pins, with links to eval-environment and sandbox.
- `docs/prompts/frozen-v1/` — sha256-locked read-only copies of `sorter_v1` and
  the five specialist `*_v1` stems (sourced from eval-environment manifest and
  sandbox `eval_environment_lineage.json` @ sandbox `52c92392`, eval-environment
  `48aab48c`).
- `docs/prompts/README.md` — layout, integrity check, refresh procedure.
- `README.md`, `docs/CONSTELLATION.md`, `AGENTS.md`, `reports/README.md` —
  cross-links to the prompt reference.

### Added — cross-repo evaluation reports

- `reports/MASTER-REPORT.md` — current status and research findings for the
  API leg (eval-environment), the Modal + vLLM leg (local-mailroom-sandbox,
  SAND-032) and the ModernBERT intake classifier (mailroom-ml), with the
  cross-leg verdict and the report-audit record.
- `reports/COST-COMPARISON-MODAL-VS-API.md` — Modal L4 vs hosted API cost per
  document and per 0.1 quality, batch and warm-fleet break-even, sorter routes,
  spend and caveats.
- `reports/figures/` — five cost figures drawn for these reports, plus verbatim
  copies of the source repos' charts; `reports/README.md` indexes them.
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