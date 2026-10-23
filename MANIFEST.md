# Dependency manifest — rationale and pins

## Decision: pin exactly, justify every entry

Yes, we fix dependencies. Reasons specific to this project:

1. **Reproducibility is part of the claim.** The paper says "public implementation
   small enough that a colleague can rerun it." An unpinned environment breaks
   that sentence in six months (we just watched numpy 2.4.3 fail to import under
   the system python 3.9 — version drift is not hypothetical here).
2. **The audit trail needs it.** Every result table records the commit SHA and the
   `pip freeze` digest. Reviewers and the advisors can reproduce bit-for-bit.

## The pinned set (deliberately tiny)

```
numpy==2.5.4        # kernel / moments / LHS stream through A2 (was 2.4.6 until 2026-10-22)
```

Added later, each with its own rationale line when the time comes:

| When | Package | Why | Why not the alternative |
|---|---|---|---|
| A3 | scipy | `chi2.ppf` for τ (df=3); `scipy.stats.qmc.LatinHypercube` | numpy has no χ² quantile |
| A6 | econml | CausalForestDML with honest CIs (Wager–Athey GRF lineage) | `causalml` is uplift/MSE, weak CI story; `bcf` is R-only — rpy2 ONLY if Hahn asks |
| A7 | matplotlib | overlay figure | — |
| dev | pytest | hand-example tests | — |

Deliberately excluded:

- **Mesa** — agent-loop framework; our kernel is vectorized algebra, Mesa adds
  overhead and abstraction without adding science.
- **pandas** — nothing here is tabular until figures; plain dicts and arrays.
- **torch / anything GPU** — no gradient flows anywhere in Phase A.

## Environment contract

```bash
uv venv .venv --python 3.14
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
pytest tests/          # hand examples must pass BEFORE any wave runs
```

Python 3.14 pinned since 2026-10-22. Earlier pins (Python 3.11, numpy 2.4.6, scipy 1.15.3,
matplotlib 3.10.3, pytest 8.4.2) stopped working after macOS 27.0.1: its loader rejects the
compiled scipy 1.15.3 extension (`__thread_bss … offset field is not zero`). The pins moved to
Python 3.14, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, pytest 9.1.1. Results produced before
that date used the earlier pins; `locks/freeze-A3.txt` still records them.

## Locking procedure at each phase gate

When a phase completes: `pip freeze > locks/freeze-A<n>.txt`, commit alongside
results. Results tables cite their lock file. No results without a lock.
