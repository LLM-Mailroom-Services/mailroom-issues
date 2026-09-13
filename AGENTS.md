# AGENTS.md

Cross-repo issue hub for the LLM-Mailroom constellation. This repository holds
**no code and no packages** — it is the coordination surface. Work done here is
**triage, routing, and governance**: filing and classifying issues, opening
epics and RFCs, keeping the label taxonomy honest, and updating this repo's
docs and templates. Implementation never happens in this repository; it lands
in a sibling repo and is tracked back here by issue link.

## Read first, every session

- `README.md` — what this repo is and the canonical pointers.
- `docs/ROUTING.md` — where an issue belongs. **Read it before filing
  anything.**
- `docs/LABELS.md` — the four label families and their vocabulary. Labels are
  the routing mechanism; a mislabeled issue is a misrouted issue.
- `docs/LIFECYCLE.md` — the triage flow an issue moves through.
- `docs/CONSTELLATION.md` — the ecosystem map (which repo owns which concern).

## Laws

1. **No code.** No packages, no pipelines, no implementation. If a task
   requires writing application code, it belongs in the sibling repo where the
   code lives — open (or move) the issue there and link it.
2. **Search before filing.** Never duplicate an open issue, epic, or RFC.
   Update the existing one instead (update, don't duplicate). If a closed issue
   already settled the question, reference it and reopen only if the decision
   is actually being revisited.
3. **One issue = one concern.** A cross-repo workstream is an **epic** with
   child issues (one per repo/phase), never a giant unstructured issue. Link
   children to the epic; the epic carries `type/epic`.
4. **Labels do the routing.** Every issue carries at least one label from each
   applicable family: `type/*`, `domain/*`, `priority/*`, `status/*`. Never
   hand-edit labels on GitHub outside the manifest workflow — the manifest
   (`.github/labels.json`) is the source of truth. New labels require a
   manifest change, not a GitHub edit.
5. **Triage is a first-class act.** A newly filed issue gets `status/triage`
   until it is routed, scoped, and prioritized. Moving an issue out of triage
   requires: a correct `domain/*` label (or a clear `invalid`/`wontfix`), a
   `priority/*` label, and an owner or an explicit backlog decision.
6. **Cross-repo issues are filed here; package issues live in package repos.**
   If an issue names a single package (`Exios66/*`), it belongs in that
   package's repo. File it here only when it spans repositories, touches the
   org, or needs a shared decision.
7. **Close with a reason.** Closing an issue says why: `fixed` (link the
   commit/PR in the implementing repo), `duplicate` (link the surviving issue),
   `invalid`, or `wontfix` (say why). Leave evidence in the thread.
8. **Commit discipline (for this repo's own files).** Every commit carries a
   fully detailed message: subject line plus a body naming each file changed
   and why (reference issue numbers, e.g. `#12`). Stage targeted paths only —
   never `git add .` or `-A`. Rewrites of pushed history are reserved for
   human-directed corrections.
9. **Docs currency.** When a change alters behavior described by `README.md`,
   `AGENTS.md`, `docs/*`, or the templates, update those files in the same
   commit. Label taxonomy changes update `docs/LABELS.md` in the same commit as
   `.github/labels.json`.
10. **The board lives next door.** Cross-agent task state is tracked on
    `Digital-Mailroom`'s `governance/TASKS.md` and served board — not here.
    This hub tracks *issues*, not agent task cards.

## What agents do here

Typical agent work in this repository:

- **Triage:** classify newly filed issues (`status/triage` → route → priority
  → `status/accepted` or a clear close).
- **Epic management:** open a `type/epic` issue for a cross-repo program of
  work, enumerate child issues per repository/phase, track progress in the
  epic thread.
- **RFC review:** shepherd `type/rfc` proposals — check feasibility against the
  constellation, collect comments, and record the decision (accepted /
  rejected / amended).
- **Governance maintenance:** update templates, the label manifest,
  `docs/*`, and the CI gate.
- **Audit:** run `scripts/labels.py audit` and reconcile drift; review open
  issues for stale `status/*` labels and outdated routing.

## Specialist subagents — call them, don't impersonate them

Every specialty has a dedicated subagent. Invoke it through the **Task tool**
(`subagent_type: <name>`) instead of improvising outside your expertise; the
subagent's report is the evidence for the issue's scope and routing. A vague
brief returns a vague report — name the issue number, the exact scope, and the
repositories/templates involved.

| # | Specialty | `subagent_type` | Call it for |
|---|---|---|---|
| 1 | Data, databases, datasets | `athena-database-agent` | Schema/DB issues, data QA, dataset selection & integration, ingestion pipelines |
| 2 | HuggingFace & data science | `lucius` | HF dataset publish/calibration (e.g. the v9 corpus family), EDA, model eval |
| 3 | Prompt engineering | `prompt-engineer` | Run-failure diagnosis, GEPA prompt versions, sorter/specialist prompt issues in llm-entity-extraction + llm-mailroom |
| 4 | Docs & board | `atom` | README/wiki/changelog drift, template updates, cross-repo doc coordination |
| 5 | Software & UI | `hazel-ui-software-master` | Board-site/visualizer UI issues, Vercel surfaces, HTML/JS/CSS |
| 6 | Systems & repo hygiene | `jarvis-systems-maximizer` | Performance triage, repo bloat, infra hygiene issues |
| 7 | Codebase exploration | `explore` | Fast read-only "where is X / how does Y work" before you file or route |
| 8 | General multi-step | `general` | Cross-specialty research when no single owner fits |

Rules that make the roster work:

- **One specialist per concern** — chain them (`explore` → `lucius` →
  `prompt-engineer`), don't ask one to do another's job.
- **The caller owns the work.** Subagent output is a report, not a merged
  change: the calling agent writes the issue, labels, and commit — the
  specialist is evidence, not an author of record.
- **Specialists verify current upstream docs** (HF Hub APIs, Langfuse,
  Modal, vLLM, Braintrust) before asserting a version or an API in an RFC or
  triage note.

Skills are the second layer — load the `huggingface`, `langfuse`, or
`customize-opencode` skill when a task matches its description.

## Commands

```bash
python scripts/labels.py audit --repo LLM-Mailroom-Services/mailroom-issues   # drift report; exit 1 on missing/drifted
python scripts/labels.py sync  --repo LLM-Mailroom-Services/mailroom-issues   # create/update labels from manifest (--dry-run first)
```

The CI gate (`.github/workflows/issue-governance.yml`) audits the manifest on
changes to `.github/` and syncs it on merge to `main`.

## Label taxonomy (summary)

Four orthogonal families — full reference in `docs/LABELS.md`:

- **`type/*`** — what the issue *is*: `bug`, `enhancement`, `documentation`,
  `question`, `type/epic` (multi-issue workstream), `type/rfc` (design
  proposal).
- **`domain/*`** — which repo/platform it *touches*: `Digital Mailroom`,
  `LLM Mailroom`, `Mailroom Sandbox`, `Agents`, `HuggingFace`, `Modal`,
  `Langfuse`, `Braintrust`, `Governance`, `Database`, `Datasets`, `Vercel`.
- **`priority/*`** — how *urgent*: `priority/critical`, `priority/high`,
  `priority/medium`, `priority/low`.
- **`status/*`** — where it *is*: `status/triage`, `status/accepted`,
  `status/in-progress`, `status/blocked`.

Plus the GitHub lifecycle labels (`duplicate`, `invalid`, `wontfix`, `good
first issue`, `help wanted`, `accessibility`).