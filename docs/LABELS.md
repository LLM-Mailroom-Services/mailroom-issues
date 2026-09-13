# Label taxonomy

Labels are the routing mechanism of this hub. The declarative manifest
`.github/labels.json` is the **source of truth** — never hand-edit labels on
GitHub. New or changed labels are a manifest change (same commit updates this
file), applied by `scripts/labels.py sync` and the CI gate.

There are four orthogonal families. Every issue carries at least one label
from **each applicable family** — a bug filed about the visualizer gets
`bug` + `Vercel` + `priority/*` + `status/*`.

## type — what the issue *is*

| Label | Meaning |
|---|---|
| `bug` | Something is broken |
| `enhancement` | New feature or capability |
| `documentation` | Docs-only change (READMEs, guides, wiki) |
| `question` | Information is requested; no work implied |
| `type/epic` | Cross-repo workstream: a program of work with child issues, one per repo/phase |
| `type/rfc` | Design proposal for cross-repo review before implementation |

## domain — which repo/platform it *touches*

| Label | Touches |
|---|---|
| `Digital Mailroom` | The hub monorepo |
| `LLM Mailroom` | The `llm-mailroom` LangGraph pipeline |
| `Mailroom Sandbox` | `local-mailroom-sandbox` |
| `Agents` | Agent infrastructure, specialists, harnesses |
| `HuggingFace` | HF Hub org, datasets, models, Hub APIs |
| `Modal` | Modal compute surfaces |
| `Langfuse` | Langfuse tracing / prompts / datasets |
| `Braintrust` | Braintrust experiment logging |
| `Governance` | Board laws, AGENTS.md, templates, workflow discipline |
| `Database` | SQLite / Postgres / Google Drive storage |
| `Datasets` | Non-HF dataset work |
| `Vercel` | Vercel surfaces (served board, web apps) |

Cross-repo work carries **multiple** `domain/*` labels (one per touched repo).

## priority — how *urgent*

| Label | Meaning |
|---|---|
| `priority/critical` | Blocks other work; must land immediately |
| `priority/high` | Lands before routine work |
| `priority/medium` | Normal priority |
| `priority/low` | When capacity allows |

## status — where it *is* (the lifecycle)

| Label | Meaning |
|---|---|
| `status/triage` | Freshly filed; needs routing, scoping, prioritization, or a decision |
| `status/accepted` | Triaged and scheduled — owned or explicitly backlogged |
| `status/in-progress` | Work is actively underway |
| `status/blocked` | Blocked on a dependency or decision (named in the thread) |

## GitHub lifecycle labels

`duplicate`, `invalid`, `wontfix`, `good first issue`, `help wanted`,
`accessibility` follow their standard GitHub meanings. `duplicate` links the
surviving issue; `wontfix` carries a reason; `invalid` marks a
misrouted/misfiled issue (route it to the right repo first).

## Rules of thumb

- **Labels do the routing** — a wrong `domain/*` label sends work to the
  wrong repo.
- **New labels are manifest changes**, not GitHub edits (Law 4).
- **Triage is explicit** — nothing ships straight to `status/accepted`; it
  passes through `status/triage` first (Law 5).
- **Extras are informational** — labels present on GitHub but absent from the
  manifest are reported by `audit` but never auto-deleted.