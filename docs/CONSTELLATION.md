# Constellation map

The ecosystem `mailroom-issues` coordinates. Every repository listed here owns
its own code, its own issues, and (where present) its own `AGENTS.md`. This
file exists so an issue can be routed to the right repo from the first write.

## Architecture

```
                    ┌── corpus feeds (colocated data) ─────────────────────┐
                    │  Enron-Evaluation-Environment   claims-data-eda      │
                    │  mailroom-corpus-eda   (mailroom-corpus, P0–P6 EDA)  │
                    └──────────────────────────┬───────────────────────────┘
                                               ▼
                    ┌── prompt-experiment loop ────────────────────────────┐
                    │  llm-entity-extraction        (GEPA prompt versions) │
                    └──────────────────────────┬───────────────────────────┘
                                               ▼
┌────────────────────────┐        ┌───────────────────────────────────────┐
│  llm-dojo-scoring      │◀───────│           llm-mailroom                │
│  shared scoring engine │ import │  LangGraph multi-agent pipeline       │
└────────────────────────┘        └──────────────────┬────────────────────┘
                                                     ▼
                    ┌── surfaces ──────────────────────────────────────────┐
                    │  The-Mailroom (visualizer)     agent-mailroom        │
                    │  local-mailroom-sandbox        llm-mailroom-graph    │
                    └──────────────────────────┬───────────────────────────┘
                                               ▼
                    ┌──────────────────────────────────────────────────────┐
                    │  Digital-Mailroom — the hub monorepo                  │
                    │  (central truth; every box lives in it)              │
                    └──────────────────────────────────────────────────────┘
```

## Repository map

| Layer | Repository | Pages / surface |
|:---|:---|:---|
| **Issue hub (this repo)** | [`LLM-Mailroom-Services/mailroom-issues`](https://github.com/LLM-Mailroom-Services/mailroom-issues) | cross-repo issues, epics, RFCs, label taxonomy |
| **Hub (central truth)** | [`LLM-Mailroom-Services/Digital-Mailroom`](https://github.com/LLM-Mailroom-Services/Digital-Mailroom) | [Dispatch Board](https://digital-mailroom-theta.vercel.app) |
| **Corpus feed** | [`Exios66/Enron-Evaluation-Environment`](https://github.com/Exios66/Enron-Evaluation-Environment) | [exios66.github.io/Enron-Evaluation-Environment](https://exios66.github.io/Enron-Evaluation-Environment/) |
| **Corpus feed** | [`Exios66/claims-data-eda`](https://github.com/Exios66/claims-data-eda) | [exios66.github.io/claims-data-eda](https://exios66.github.io/claims-data-eda/) |
| **Corpus EDA + HF** | [`Exios66/Mailroom-Corpus-EDA`](https://github.com/Exios66/Mailroom-Corpus-EDA) | [exios66.github.io/Mailroom-Corpus-EDA](https://exios66.github.io/Mailroom-Corpus-EDA/) |
| **Prompt experiments** | [`Exios66/llm-entity-extraction`](https://github.com/Exios66/llm-entity-extraction) | [exios66.github.io/llm-entity-extraction](https://exios66.github.io/llm-entity-extraction/) |
| **Scoring engine** | [`Exios66/llm-dojo-scoring`](https://github.com/Exios66/llm-dojo-scoring) | — |
| **LangGraph pipeline** | [`Exios66/llm-mailroom`](https://github.com/Exios66/llm-mailroom) | — |
| **ML training / intake contract** | [`LLM-Mailroom-Services/mailroom-ml`](https://github.com/LLM-Mailroom-Services/mailroom-ml) | ModernBERT classifier, calibration, eval harness, `intake_handoff` contract |
| **Pixel visualizer** | [`Exios66/The-Mailroom`](https://github.com/Exios66/The-Mailroom) | [exios66.github.io/The-Mailroom](https://exios66.github.io/The-Mailroom/) |
| **Walking floor** | [`Exios66/agent-mailroom`](https://github.com/Exios66/agent-mailroom) | — |
| **Local sandbox** | [`Exios66/local-mailroom-sandbox`](https://github.com/Exios66/local-mailroom-sandbox) | — |
| **Knowledge graph** | [`Exios66/llm-mailroom-graph`](https://github.com/Exios66/llm-mailroom-graph) | [exios66.github.io/llm-mailroom-graph](https://exios66.github.io/llm-mailroom-graph/) |

## Platform / service domains

Issues also touch external platforms, each with its own domain label:

- **HuggingFace** — `Lucius-Morningstar` org datasets (the `mailroom-corpus`
  family), model/eval artifacts, Hub APIs.
- **Modal** — serverless compute, GPU jobs, `modal deploy` surfaces.
- **Langfuse** — tracing, prompts, datasets, scores (observability sink).
- **Braintrust** — experiment logging / evaluation platform.
- **Vercel** — the served board and any web surface.
- **Database / Datasets** — SQLite/Postgres/Google Drive storage, and
  non-HF dataset concerns.

## Where each concern is governed

- **Cross-repo task state** lives on `Digital-Mailroom/governance/TASKS.md`
  and its served board — not here.
- **Prompt versions** live in `llm-entity-extraction` (its own GEPA board and
  `PROMPT_ENGINEER_GEPA_PROVENANCE.md`).
- **The label taxonomy for THIS hub** lives in `.github/labels.json`, mirrored
  by `scripts/labels.py`; the hub's own taxonomy lives in
  `Digital-Mailroom/.github/labels.json`.

See [`ROUTING.md`](ROUTING.md) for the filing decision tree.