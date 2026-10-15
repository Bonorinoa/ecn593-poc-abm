# ECN593 PoC — Set-ID Policy ABM

**Policy interventions in agent-based models are set-identified under calibration uncertainty.**

A pre-registered proof-of-concept for an M.S. Economics applied project (ECN 593,
Fall 2026, ASU). Spec freeze: 2026-08-26 (`METHODOLOGY.md`), AMENDMENT-02
2026-08-27 (planted \(z\)). WB country totals archived as F-EMPTY; the overlay
runs on the planted village DGP.

## The claim (one paragraph)

History matching a stochastic ABM produces a *not-ruled-out-yet* set of
calibrations — a set, not a posterior. The image of a named **policy** estimand
θ₂ (hub-seed vs control) over that set is the honest report, Θ_hm. One-world
estimators fitted at two pre-declared survivors (best match and median
implausibility) publish intervals that can be overconfident relative to their
*own* image: a SUTVA interval (gold-standard interval *at a world*; this run is
OLS-HC1, not a forest and not BCF) and an exposure-mapped Hájek estimator
(interference-aware, still silent on calibration). A minimal measurement layer
adds a second image over admissible scorings of Y at those worlds. The
simulator is where this is checkable, because only there does the planner know
the truth. Empty NROY is a finding; τ_I is never loosened.

## Architecture

```
src/poc_abm/            Python engine (the science) — Phase A
  config.py             ALL frozen constants: parameters, thresholds, seeds
  data_worldbank.py     API fetcher for external anchors
  kernel.py             the ABM: graph, covariates, linear-in-means update, 3 arms
  moments.py            moment map M(c), implausibility I(c)
  history_matching.py   LHS waves -> NROY set
  estimand.py           theta_1, theta_2, targeting premium
  measures.py           [A5] measurement layer m1/m2/m3 + admission
  diagnostic.py         [A6] Foil 1 (OLS-HC1 this run) + E2 at c0_min and c0_med
  figures.py            [A7] overlay figure (two rows: min I, median I)
data/anchors.json       frozen 2026-08-12 World Bank summary (committed)
docs/lectures/          study notes (not specification)
tests/                  hand-example tests FIRST (pedagogical contract)
notebooks/              walkthroughs, one per concept
```

`METHODOLOGY.md` is the single source of truth. Code that disagrees is a bug.
NetLogo is deferred past December.

## Decisions locked (see MANIFEST.md for dependency rationale)

| Question | Decision |
|---|---|
| Language | Python engine; NetLogo **out of December scope** |
| Dependencies | Exact pins in `requirements.txt` |
| Pedagogy | Every module ships with a hand-example test |
| Blueprint | `METHODOLOGY.md` frozen 2026-08-26 before any wave |
| External data | World Bank API v2; summary committed at `data/anchors.json` |
| Estimand | θ₂ = hub-seed vs control; ψ = hub − random (targeting premium) |
| Moments | 3 village functionals (historical slot names); τ_I = χ²₃(0.95) |
| Units | planted z already in [0,1]; δ = (0.02, 0.05, 0.02) |
| Diagnostic worlds | **both** min I and median I |
| Foil 1 | Role: SUTVA one-world interval. This run: **OLS-HC1** (CausalForestDML does not import on the numpy pin). BCF only if Hahn asks, extra row. Do not call OLS “BCF.” |
| Foil 2 | AMENDMENT-01 accepted: Hájek on π₁ vs Θ_exp |

## Status

- [x] Project created, scaffold written
- [x] Spec freeze 2026-08-26 (METHODOLOGY.md / config.py / this file)
- [x] A1 kernel.py + hand-example test (`hash()` replaced by length-prefixed crc32)
- [x] A2 moments.py + rescale anchors to [0,1] (fetcher already ran 2026-08-12)
- [x] A3 history matching waves → planted \(z\) (AMENDMENT-02): |NROY|=991; WB pair archived as F-EMPTY
- [x] A4–A7 run on the planted NROY (Θ_hm, Θ_exp, two \(c_0\), overlay)
- [ ] B1–B3 NetLogo twin — **deferred**, not a December deliverable

Planted run: |NROY|=991, \(\Theta_{\mathrm{hm}}=[0.006,0.073]\). Foil 1 estimator
**OLS-HC1** (neither F-OVERCONF nor F-HONEST vs Θ_hm: different functional).
Foil 2: F-OVERCONF-E2 at both \(c_0\); oracle gate passed. WB attempt archived
in `results/poc_results_wb_F-EMPTY.json`. Overlay: `figures/overlay.png`.
Study note with the numbers: `docs/notes/nroy-images.tex`.
Lectures in `docs/lectures/` are **pre-wave study drafts**; they are not the
result write-up.

## Reproduce and verify

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -q                      # hand-example tests must pass first (pedagogical contract)
PYTHONPATH=src python -m poc_abm.pipeline   # re-draws noise; re-runs the waves
```

The committed JSON in `results/` is the run that produced the findings below.
Re-running the pipeline **re-draws simulation noise**, so it will not reproduce
those exact numbers; do not overwrite the committed results just to "refresh" a
number. `METHODOLOGY.md` is the single source of truth — if code and that file
disagree, the file wins and the code is a bug.

## Honesty of the reproducibility record

`MANIFEST.md` pins dependencies exactly and requires that *every result table
records the commit SHA and `pip freeze` digest* that produced it. Honest status of
that contract here: this folder was placed under version control on **2026-10-14**
with a single initial commit, while the results in `results/*.json` were produced
on **2026-08-28** — so the earlier result tables have **no commit SHA** binding
them to the code that generated them. A freeze snapshot exists for the A3 gate
(`locks/freeze-A3.txt`); later gates have no lock file yet. Treat pre-10-14
results as "the code as frozen on the freeze date," not as bit-for-bit
reproducible from a recorded SHA.

## Deeper documentation

- `METHODOLOGY.md` — the frozen blueprint (single source of truth).
- `MANIFEST.md` — pinned dependencies and the audit-trail contract.
- `docs/AMENDMENT-*.md` — the two accepted spec amendments.
- `docs/notes/nroy-images.tex` — the study note with the committed numbers.
