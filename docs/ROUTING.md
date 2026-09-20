# Issue routing

**Read this before filing or triaging anything.** The routing question is:
*does this concern one repository, or does it span the constellation?* The
answer decides which store the issue lands in.

## Decision tree

```
Does the issue name one package/repo and nothing else?
│
├─ YES — is that repo the hub monorepo?
│   ├─ Yes (Digital-Mailroom scope: board, sync driver, hub tooling,
│   │   root docs, the monorepo itself)
│   │       → file in LLM-Mailroom-Services/Digital-Mailroom
│   └─ No (a single package: Exios66/* or the org-owned ml package —
│       llm-mailroom, llm-entity-extraction, llm-dojo-scoring, The-Mailroom,
│       agent-mailroom, local-mailroom-sandbox, Enron-Evaluation-Environment,
│       claims-data-eda, llm-mailroom-graph, Mailroom-Corpus-EDA,
│       LLM-Mailroom-Services/mailroom-ml)
│           → file in that package's repo
│
└─ NO — does it touch two or more repositories, the org, or a shared decision?
    ├─ Yes
    │   → FILE IT HERE (LLM-Mailroom-Services/mailroom-issues)
    └─ No — it is a question, a design proposal, or org governance
        → ALSO HERE: questions are welcome, design proposals use the RFC
          template, org/agent/governance work uses epic or feature templates
```

## What this hub accepts

File here (with the matching template and labels):

| Concern | Template | Domain label example |
|---|---|---|
| Workstream spanning multiple repos | Epic | multiple `domain/*` |
| Platform / architecture decision | RFC | platform label (`Langfuse`, `Braintrust`, `Modal`, …) |
| Corpus program of work (publish + migration) | Epic | `HuggingFace`, `Datasets` |
| Agent / specialist / governance design | Feature / Epic | `Agents`, `Governance` |
| Cross-cutting bug (several repos affected) | Bug report | multiple `domain/*` |
| Question about the constellation | Question (blank) | the domain it asks about |

## What this hub does NOT accept

- **Single-package bugs/features** → the package's repo. Cite the open issue
  here as a link if a program of work tracks it.
- **Hub-monorepo scope** (board state, sync driver, hub labels, monorepo
  docs) → `Digital-Mailroom`.
- **Code, packages, pipelines** → never implemented here, full stop (Law 1).

## After filing: triage

Every issue filed here enters `status/triage`. The triage pass:

1. **Confirm routing** — is the domain label correct? If it should live in a
   sibling repo, move it (file there, link this issue, close with
   `invalid`/duplicate-style reason).
2. **Scope it** — one concern per issue; split or restructure into child
   issues under an epic if it is really several concerns.
3. **Prioritize** — assign `priority/*` from the backlog.
4. **Release from triage** — set `status/accepted` (scheduled, owner or
   backlog) or close with a reason.

Labels are the routing mechanism; a mislabeled issue is a misrouted issue
([`LABELS.md`](LABELS.md), [`LIFECYCLE.md`](LIFECYCLE.md)).