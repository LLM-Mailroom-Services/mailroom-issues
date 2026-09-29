# AMFAM biweekly one-pager — LLM Mailroom experiments

**Date:** 2026-09-29  
**Dataset:** Hub tag **`v9.1`** · `Lucius-Morningstar/mailroom-dataset` @ **`ed7576b…`** · **3,302** docs  
**Sources:** [MASTER-REPORT](MASTER-REPORT.md) · [COST-COMPARISON-MODAL-VS-API](COST-COMPARISON-MODAL-VS-API.md) · [MODAL-VLLM-GPU-REPORT](MODAL-VLLM-GPU-REPORT.md)  
**Tips at MASTER export:** sandbox `95d89fa8f401` · eval `86b4e54fc5a2` · mailroom-ml `d3ad22263da0`

---

## 1. GPU scale-out (Modal L4, same docs)

| Fleet (correspondence n=100) | Wall | $/doc | Score |
|---|---:|---:|---:|
| 1×L4 · c8 | 95.0 s | ~$0.00021 | 0.2886 |
| **2×L4 · c16** | **46.1 s (2.06×)** | **~$0.00020 (flat)** | 0.2966 |

- Second L4 is **near-linear on wall time** with **flat $/doc** when routing is balanced.
- Serving ladder **L0→L5** alone cut wall and $/doc **~44%** at equal quality (L5 frozen).
- Mis-set `max_inputs` collapsed scale-out (97/100 on one replica → ~3.2× worse $/token) — ops discipline matters as much as GPU count.
- Slide assets: hub `viz/` for `second-l4` + `sand032-ladder`.

---

## 2. Per-class quality (one slide)

| Class | Best API | Modal Qwen3-8B-AWQ | Takeaway |
|---|---|---|---|
| **Insurance** | DeepSeek **0.797** / Qwen3.7-Flash **0.773** (n=50) | **0.688** | API wins quality · ⚠ Modal **schema validity 22%** (score real; JSON compliance not production-ready) |
| **Contracts** | Qwen3-8B **0.617** / Flash **0.546** (n=50) | **0.596** CUAD F1 | API cheaper; **scoring differs** (suite vs CUAD) — do not bar-chart as one metric |
| **Corporate** | DeepSeek **0.442** / Flash **0.418** (n=50) | **0.458–0.469** | **Modal wins cost + quality** |
| **Correspondence** | Qwen3-8B **0.513** / Flash **0.493** (n=50) | **0.300** (v2 promoted **0.345**) | Modal cheap; quality gap vs ≥0.50 pipeline gate |
| **Merger** | **Qwen3.7-Flash 0.521** (n=50) | MAUD **8.5%** | Best result is **API Flash**; Modal MAUD is a **different metric** and still unsolved — **do not stack on one bar** |

**Intake / sorter**

| Surface | Class | Subclass | Notes |
|---|---:|---:|---|
| ModernBERT **Arm B** | **95.05%** ✓ P0 | **58.3%** ✕ | Cite Arm B — not older run-3 **92.57%** |
| LLM sorter API n=100 | **91–95%** | **49–64%** | Best ECE: Qwen3.7-Flash **0.019** |
| Modal sorter S6 | **89.5%** (n=457) | — | Mergers under-recalled |

**Recommended production routing (MASTER §5)**  
**ModernBERT** (class intake) → **API** for insurance / contracts / merger → **Modal dual-L4** for **corporate only**. Subclass stays off the “ready” list on every route.

---

## 3. Cost per 1M tokens (busy-window Modal vs OpenRouter)

**Modal warm 2×L4 ($/1M tokens, busy-window):** corr **$0.060** · corp **$0.078–0.095** · insurance **$0.117–0.146** · contracts **$0.275** · merger **$0.301** · sorter **$0.052**.

**Cheapest API (Qwen3.7-Flash unless noted):** corr **$0.087** · insurance **$0.089** · corp **$0.053** · contracts **$0.063** · merger **$0.037**.

| Insight | Detail |
|---|---|
| When Modal undercuts API *per token* | Correspondence only, when **warm & busy** |
| When Modal wins *per document* | **Corporate** (and optionally corr if quality OK) |
| Same-model hosted Qwen3-8B | **$0.17–0.31**/1M — self-host AWQ is **~2.6–21×** cheaper per doc than renting that model |
| Cold batches | **~2–22×** warm cost at current n — amortize boots with bigger batches or keep warm (&lt;~5.6 min gaps) |

Campaign spend so far: ~**$14.40** Modal + &lt;**$1** API (SAND-032 alone **$2.80** of $5).

---

## 4. Ask: **$100–$250** research stipend

| Budget | Roughly buys (at measured floors) |
|---|---|
| **$100** | ~35× SAND-032 program, or ~60 h warm 2×L4 (~$1.60/h), or ~20 full-corpus (~3.3k doc) cheap-API passes |
| **$175** | Mid: replicate five-class sweeps at n=500–1k + prompt/scorer iters on merger / subclass |
| **$250** | ~155 h 2×L4 research time, or multi-model API + Modal scale-out on **~10×** current draw sizes |

**Pitch line:** We’ve proven GPU scale-out is flat-cost and mapped where self-host vs API wins by class. **$100–250** funds the next order-of-magnitude on data volume so AMFAM sees production-scale confidence intervals — not another ~$15 pilot.

---

## Caveats (keep on the slide footnotes)

1. API ≠ Modal (different pins / N / prompts / scorers) — compare within a leg.
2. Insurance Modal **schema 22%** footnote.
3. Merger: API Flash **0.521** vs Modal MAUD **8.5%** — different metrics.
4. ModernBERT cite **Arm B 95.05%**, not run-3 92.57%.
5. Corpus pin: Hub tag **`v9.1`** / SHA **`ed7576b…`**.
