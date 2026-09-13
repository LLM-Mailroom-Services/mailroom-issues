# Changelog

All notable changes to this repository's own files (docs, templates, the
label manifest, and governance tooling) are documented here. Issue numbers
refer to this repo's issues.

## [Unreleased]

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