<div align="center">

# mailroom-issues

**The constellation-wide issue hub for LLM-Mailroom-Services.** Every bug, feature
request, task, RFC, and cross-repo workstream that touches more than one
repository — or needs an org-level decision — is filed, labeled, and triaged here.

</div>

This repository holds **no code and no packages**. It is the coordination
surface for the ecosystem: the issue store, the cross-repo epic track, the
design-proposal (RFC) track, and the declarative label taxonomy that routes
work to the right repository. Implementation always lands in a sibling repo.

> **Canonical entry points:** [Agent instructions](AGENTS.md) ·
> [Constellation map](docs/CONSTELLATION.md) · [Issue routing](docs/ROUTING.md) ·
> [Label taxonomy](docs/LABELS.md) · [Issue lifecycle](docs/LIFECYCLE.md)

## What belongs here

File an issue here when the work is **cross-repo**, **org-wide**, or needs a
**shared decision**. Single-repo bugs and package-scoped features belong in the
repository where the code lives.

| Scenario | Example | Where it lands |
|---|---|---|
| Workstream spanning several repos | v9 corpus expansion (architecture, expansion, GT conformance, publish & migration) | this hub, as an epic (#9–#16) |
| Platform / architecture decision | "Add Braintrust as the trace sink", "New specialist agents" | this hub, as an RFC |
| Org-wide agent / governance design | "New Evaluation Tasks → New Specialists + Agents" | this hub (#7) |
| Bug or feature in the monorepo hub | `board_state.py` drift, sync driver failure | [`LLM-Mailroom-Services/Digital-Mailroom`](https://github.com/LLM-Mailroom-Services/Digital-Mailroom) |
| Bug scoped to a single package | sorter hallucinates on `change_of_control` | the package's own repo (`Exios66/*`) |

The full decision tree is [docs/ROUTING.md](docs/ROUTING.md) — read it before
filing so an issue lands in the right store the first time.

## The constellation

`mailroom-issues` is one surface in an ecosystem of ten-plus repositories.
The hub monorepo ([`Digital-Mailroom`](https://github.com/LLM-Mailroom-Services/Digital-Mailroom))
is the central truth and mirrors every package as a git subtree; upstream
`Exios66/*` repositories remain the independent release vehicles. The complete
map (roles, layers, links) is [docs/CONSTELLATION.md](docs/CONSTELLATION.md).

## Filing an issue

Use the issue template that matches the shape of the work:

| Template | For | Labels applied |
|---|---|---|
| [Bug report](.github/ISSUE_TEMPLATE/bug_report.yml) | Something is broken | `bug` + `domain/*` |
| [Feature request](.github/ISSUE_TEMPLATE/feature_request.yml) | New capability or enhancement | `enhancement` + `domain/*` |
| [Task / TODO](.github/ISSUE_TEMPLATE/task_todo.yml) | Small, single-owner work item | `type/task`-style scoping |
| [Epic](.github/ISSUE_TEMPLATE/epic.yml) | Multi-issue, cross-repo workstream | `type/epic` + `status/triage` |
| [RFC](.github/ISSUE_TEMPLATE/rfc.yml) | Design proposal needing org review | `type/rfc` + `status/triage` |

Every issue is then classified by four orthogonal label families — **type**
(what it is), **domain** (which repo/platform it touches), **priority** (how
urgent), and **status** (where it is in the lifecycle). Reference:
[docs/LABELS.md](docs/LABELS.md) and [docs/LIFECYCLE.md](docs/LIFECYCLE.md).

## Repository layout

```
mailroom-issues/
├── AGENTS.md              # rules for agents triaging and coordinating here
├── README.md              # this file — the canonical entry point
├── CHANGELOG.md           # scaffolded release history for this repo's docs/tooling
├── LICENSE                # MIT (matches the org convention)
├── .gitignore
├── .github/
│   ├── ISSUE_TEMPLATE/    # bug / feature / task / epic / RFC forms + config.yml
│   ├── PULL_REQUEST_TEMPLATE/
│   ├── labels.json        # declarative label taxonomy (source of truth)
│   └── workflows/
│       └── issue-governance.yml   # label-manifest drift gate (CI)
├── scripts/
│   └── labels.py          # sync/audit .github/labels.json against the repo
├── data/
│   └── hf_cache/          # colocated HF parquet cache (pin + MANIFEST — see data/hf_cache/README.md)
├── reports/               # generated cross-repo evaluation reports (markdown + SVG; see reports/README.md)
│   ├── MASTER-REPORT.md   # status + research findings: API leg, Modal + vLLM leg, ModernBERT
│   ├── COST-COMPARISON-MODAL-VS-API.md   # cost per doc / per quality, break-even + optimal Modal scenario, sorter routes, spend
│   ├── MODAL-VLLM-GPU-REPORT.md          # Modal + vLLM: cost per token, GPU spend, utilization, second L4
│   └── figures/           # cost/ + gpu/ (drawn for these reports) · sources/<repo>/ (verbatim source charts)
└── docs/
    ├── index.html         # generated Pages site: landing page (static HTML, no JS; see Reports)
    ├── reports/           # generated Pages site: one page per report, figures inlined
    ├── .nojekyll          # serve the generated HTML as is
    ├── CONSTELLATION.md   # the ecosystem map: repos, roles, layers
    ├── ROUTING.md         # which issue belongs in which repository
    ├── LABELS.md          # the four label families and their vocabulary
    └── LIFECYCLE.md       # triage flow: file → triage → schedule → do → close
```

## Reports

[`reports/`](reports/README.md) holds the constellation's cross-repo evaluation
reports. They are generated outputs, not code (law 1): the generator,
`reports/dashboard/export_hub_reports.py`, lives in `Exios66/local-mailroom-sandbox`
next to the reports hub that cross-checks every number against its source file.

- [Master report](reports/MASTER-REPORT.md): where each front stands, and the
  findings from the API leg (eval-environment), the Modal + vLLM leg (sandbox,
  SAND-032) and the ModernBERT intake classifier (mailroom-ml).
- [Cost comparison, Modal L4 vs hosted API](reports/COST-COMPARISON-MODAL-VS-API.md):
  cost per document and per unit of quality for every route and model (Modal
  self-hosts Qwen3-8B-AWQ only; every other model ran via the API), the same
  model on both routes, the warm-fleet and cold-batch break-even volumes, the
  optimal Modal deployment,
  sorter routes and spend.
- [Modal + vLLM GPU economics](reports/MODAL-VLLM-GPU-REPORT.md): the SAND-032
  leg's cost per 1M tokens (warm, cold and at real utilization), warm vs cold
  GPUs, where the GPU spend went, how busy the GPUs were, and what adding the
  second L4 did.

**Reports site:** <https://llm-mailroom-services.github.io/mailroom-issues/>.
The same three reports, rendered as static pages in `docs/index.html` and
`docs/reports/` (inline SVG figures, no JavaScript, no external requests).
GitHub Pages serves them by deploying from a branch, so no workflow is involved.
One-time setup by an org admin: **Settings → Pages → Build and deployment →
Deploy from a branch → `main` / `/docs`**.

Regenerate both from the sandbox with `--out ../mailroom-issues/reports` (the
site goes to `docs/` alongside); `--check` exits 1 when either is stale. Don't
hand-edit the files.

## Governance tooling

The label taxonomy is declarative and machine-checked:

```bash
python scripts/labels.py audit --repo LLM-Mailroom-Services/mailroom-issues
python scripts/labels.py sync --repo LLM-Mailroom-Services/mailroom-issues
```

`audit` reports manifest↔repo drift and exits 1 on missing/drifted labels;
`sync` creates and updates labels from the manifest (extras are reported but
never deleted). The CI gate (`.github/workflows/issue-governance.yml`) audits
on every change to `.github/` and pushes the manifest on merge to `main`.

## Changelog & license

Changes to this repo's own docs, templates, and tooling accumulate under
[CHANGELOG.md](CHANGELOG.md) `[Unreleased]` and are cut per hub release.

Licensed under the [MIT License](LICENSE), matching the org convention.

---

<div align="center">

**[Digital-Mailroom](https://github.com/LLM-Mailroom-Services/Digital-Mailroom)** ·
**[llm-mailroom](https://github.com/Exios66/llm-mailroom)** ·
**[llm-entity-extraction](https://github.com/Exios66/llm-entity-extraction)** ·
**[llm-dojo-scoring](https://github.com/Exios66/llm-dojo-scoring)** ·
**[The-Mailroom](https://github.com/Exios66/The-Mailroom)** ·
**[agent-mailroom](https://github.com/Exios66/agent-mailroom)**

<sub>Built by the governed evaluation family under
[LLM-Mailroom-Services](https://github.com/LLM-Mailroom-Services)
(Exios66 · grantmooslin) · 2026</sub>

</div>