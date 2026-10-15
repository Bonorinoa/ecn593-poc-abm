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
numpy==2.4.6        # kernel / moments / LHS stream through A2
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
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
pytest tests/          # hand examples must pass BEFORE any wave runs
```

Python 3.11 pinned (matches the verified-working numpy wheel on this machine;
3.9 system python is broken for numpy>=2).

## Locking procedure at each phase gate

When a phase completes: `pip freeze > locks/freeze-A<n>.txt`, commit alongside
results. Results tables cite their lock file. No results without a lock.
