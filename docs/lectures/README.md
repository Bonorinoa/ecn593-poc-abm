# ECN 593 short course (study draft)

Six standalone lecture-note PDFs. Not a freeze of `METHODOLOGY.md`.
Read **00 → 05** in order. Come back with questions before any specification change.

**Status stamp (read this before the PDFs).** These notes were drafted
*before* the planted waves. They still say, in places, that no NROY and no
overlay exist. That sentence is false as of 2026-08-28. The result write-up
is `docs/notes/nroy-images.tex`. Foil 1 on this pin is **OLS-HC1**, not a
causal forest and not BCF. Finding codes `I_BCF` / F-OVERCONF in
`METHODOLOGY.md` name a *role*; the run file names the estimator. Do not
treat a lecture table as a numerical result. Do not rebuild these PDFs as
if they were the overlay.

| File | Topic | Pages |
|---|---|---|
| [lecture-00-introduction.pdf](lecture-00-introduction.pdf) | Prerequisites, pipeline, language discipline | 7 |
| [lecture-01-history-matching.pdf](lecture-01-history-matching.pdf) | Implausibility, NROY, discrepancy | 7 |
| [lecture-02-partial-identification.pdf](lecture-02-partial-identification.pdf) | Identified sets, Law of Decreasing Credibility | 10 |
| [lecture-03-measurement-admission.pdf](lecture-03-measurement-admission.pdf) | Scoring rules, Θ_cv | 11 |
| [lecture-04-two-foils.pdf](lecture-04-two-foils.pdf) | Forests/BCF and exposure-mapped E2 | 10 |
| [lecture-05-composition.pdf](lecture-05-composition.pdf) | Overlay, literature gap, December deliverable | 12 |

Rebuild a note after editing its JSON:

```bash
.venv/bin/python docs/lectures/_build_lecture.py \
  docs/lectures/lecture-XX-….json \
  -o docs/lectures/lecture-XX-….pdf
```

JSON sources and the two generator scripts (`_write_lecture00.py`, `_write_lecture01.py`) sit beside the PDFs. Lectures 02–05 were drafted by subagents and reviewed in place; 00 and 01 were written after that review.
