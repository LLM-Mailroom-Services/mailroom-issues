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
└── docs/
    ├── CONSTELLATION.md   # the ecosystem map: repos, roles, layers
    ├── ROUTING.md         # which issue belongs in which repository
    ├── LABELS.md          # the four label families and their vocabulary
    └── LIFECYCLE.md       # triage flow: file → triage → schedule → do → close
```

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