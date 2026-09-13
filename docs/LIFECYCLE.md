# Issue lifecycle

The path every issue takes through this hub, from filing to close. The
`status/*` labels mark where an issue is; the lifecycle rules below decide
which label is true.

## The flow

```
filed ──▶ status/triage ──▶ (route + scope + prioritize) ──▶ status/accepted
                                                               │
                               ┌───────────────────────────────┴───────────────┐
                               ▼                                               ▼
                    status/in-progress                             closed (reason)
                               │                                     ▲
                               ▼                                     │
                    status/blocked ──▶ unblocked ────────────────────┘
```

## Stage 1 — Filed

An issue arrives via a template. It is immediately `status/triage`: routing
has not been confirmed, scope has not been checked, priority has not been
set.

## Stage 2 — Triage (a first-class act, Law 5)

A triage pass does four things, in order:

1. **Confirm routing** (`docs/ROUTING.md`). If the issue names a single
   package or hub scope, it moves to that repo: file it there, link this
   issue, close here with a reason. Otherwise it stays.
2. **Scope it** (Law 3). One issue = one concern. Several concerns → split
   into child issues under a `type/epic` parent.
3. **Label it** (Law 4). Correct `domain/*` (or `invalid`/`wontfix`), a
   `priority/*`, and the target `status/*`.
4. **Release or close.** Release = `status/accepted` with an owner or an
   explicit backlog decision. Close = `invalid` (wrong store — routed away),
   `wontfix` (decision: not doing this), or `duplicate` (linked to the
   surviving issue).

Nothing leaves `status/triage` until it is routed, scoped, and prioritized.

## Stage 3 — Accepted

Scheduled work: owned, or explicitly in the backlog with a priority.
Implementation happens in the sibling repo; this issue tracks it. Link the
implementing repo's issue/PRs in this thread as they appear.

## Stage 4 — In progress / blocked

`status/in-progress` means work is underway (in the implementing repo).
`status/blocked` means a dependency or decision is pending — the blocker is
**named in the thread**, never left implicit.

## Stage 5 — Closed (with a reason, Law 7)

| Close reason | Evidence required |
|---|---|
| `fixed` | Link the commit/PR in the implementing repo |
| `duplicate` | Link the surviving issue |
| `invalid` | Misrouted / misfiled — where it actually went |
| `wontfix` | The decision and why |

Closing never happens silently. Leave evidence in the thread.

## Epic lifecycle

An epic (`type/epic`) is a cross-repo program of work. It opens with a
statement of scope, then enumerates child issues — one per repository or
phase — as links in the epic body. Children carry their own `status/*` and
`priority/*`; the epic thread tracks overall progress. The epic closes only
when every child is closed (or explicitly descoped).

## Backlog hygiene

- **Search before filing** (Law 2): update the existing issue instead of
  duplicating it.
- **Stale triage**: an issue parked in `status/triage` too long is a signal —
  re-run the triage pass and either release it or close it with a reason.
- **Audits**: `scripts/labels.py audit` keeps the taxonomy honest;
  `gh issue list` reviews surface stale `status/*` labels for the monthly
  governance pass.