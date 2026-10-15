#!/usr/bin/env python3
"""Generate lecture-00 JSON and build the PDF."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("/Users/bonorinoa/Desktop/Github_Repositories/ecn593-poc-abm/docs/lectures")

P = lambda text: {"type": "paragraph", "text": text}
H = lambda n, text: {"type": "heading", "level": n, "text": text}
B = lambda *items: {"type": "bullet", "items": list(items)}
D = lambda text: {"type": "display", "text": text}
C = lambda title, text: {"type": "callout", "title": title, "text": text}
R = lambda text: {"type": "ref", "text": text}
T = lambda rows, caption, header=True: {
    "type": "table",
    "rows": rows,
    "caption": caption,
    "header": header,
}

spec = {
    "lecture_number": 0,
    "title": "Introduction",
    "subtitle": "Prerequisites, notation, and the shape of the argument",
    "running_header": "Lecture 0 · Introduction",
    "author": "ECN 593 short course notes (study draft, not a frozen specification)",
    "date": "August 2026",
    "abstract": (
        "These six notes are a short course for one applied project: a network agent-based "
        "model is calibrated to World Bank moments by history matching; the image of a named "
        "policy contrast over the surviving calibrations is reported as a set; two one-world "
        "estimators — a SUTVA learner and an exposure-mapped design-based estimator — are "
        "audited against that set. This lecture supplies the prerequisites an economics "
        "master's student needs before Lectures 1–5, states the argument from the top down, "
        "and freezes the language the rest of the course will not be allowed to abuse. "
        "No calibration wave has been run. Nothing here is a result."
    ),
    "elements": [
        H(1, "1. How to use these notes"),
        P(
            "Read this lecture first, then 1 through 5 in order. Each later lecture is written "
            "to be self-contained on its own objects, but the argument is a composition, and "
            "Lecture 5 will not re-teach history matching or Manski. The notes assume first-year "
            "graduate training in econometrics — expectations, OLS, potential outcomes as a "
            "notation, the idea of an estimand — and almost no training in agent-based models, "
            "uncertainty quantification, or partial identification as a research method. Where "
            "a term of art is unavoidable it is defined on first use."
        ),
        P(
            "The notes are a study draft. They are not a freeze of METHODOLOGY.md, not a "
            "proposal to advisors, and not a finding. METHODOLOGY.md remains the specification "
            "of the engine. If a sentence here and a sentence there disagree, the specification "
            "wins and the notes are wrong. AMENDMENT-01, which adds a second diagnostic "
            "estimator, is itself a draft and is labelled as such whenever it appears."
        ),
        P(
            "Each lecture ends with a short reading list. You do not need to read the lists "
            "before the next lecture. You will want them when a definition here feels thinner "
            "than the paper it came from."
        ),
        H(1, "2. The project, from the top"),
        P(
            "The applied project asks a narrow question. A stochastic network model of a "
            "preventive behaviour is written down in closed form. It is calibrated not by "
            "picking a best-fit parameter vector but by discarding those vectors that cannot "
            "reproduce a small set of real cross-country moments, once sampling error, "
            "simulation error, and a stated model-discrepancy budget are allowed for. The "
            "survivors form a not-ruled-out-yet set in parameter space. A named policy "
            "contrast — the change in mean behaviour if one seeds an intervention at network "
            "hubs rather than at nobody — is then evaluated at many survivors. The collection "
            "of those evaluations is the honest answer. It is a set, not a number."
        ),
        P(
            "Separately, one surviving world is treated as if it were the world. A modern "
            "heterogeneous-treatment-effect estimator, built under the stable unit treatment "
            "value assumption, is fitted to a simulated panel from that world and publishes "
            "an interval. A second estimator, built to handle interference and using the "
            "known randomisation of a different assignment rule, publishes another. Each "
            "interval is compared with the image of <i>its own</i> estimand over the surviving "
            "worlds. If a one-world interval sits inside the image and misses part of it, "
            "that is a pre-registered finding about overconfidence. If it covers the image, "
            "that is a pre-registered finding that the interesting story is false here. If "
            "no world survives calibration, that too is a finding, and the protocol forbids "
            "loosening the threshold to rescue the exercise."
        ),
        P(
            "Two advisors sit on opposite sides of this picture. History matching and model "
            "discrepancy are a Durham / computer-experiment tradition. Causal forests and "
            "Bayesian causal forests are a causal-machine-learning tradition. The project is "
            "interesting, if it is, because it forces those two traditions to share an "
            "estimand and then refuses to let either tradition's native interval stand in "
            "for the image. The composition is the claim. Equifinality in simulators is not "
            "a discovery of this course (Lecture 5 names the near-neighbours). Economist-native "
            "policy contrasts under interference, mapped through a history-matched set, with "
            "a paired SUTVA foil and an interference-aware foil, on a simulator where the "
            "planner's number is known, is the remaining wedge."
        ),
        H(1, "3. Potential outcomes, in the form we will use them"),
        P(
            "For a single unit <i>i</i> and a binary treatment <i>D<sub>i</sub></i> ∈ {0, 1}, "
            "the Neyman–Rubin notation writes two potential outcomes, <i>Y<sub>i</sub></i>(1) "
            "and <i>Y<sub>i</sub></i>(0). The observed outcome is "
            "<i>Y<sub>i</sub></i> = <i>Y<sub>i</sub></i>(<i>D<sub>i</sub></i>). The unit-level "
            "effect <i>Y<sub>i</sub></i>(1) − <i>Y<sub>i</sub></i>(0) is not observed. Holland "
            "(1986) called this the fundamental problem of causal inference. Random assignment "
            "of <i>D</i> identifies the average treatment effect "
            "E[<i>Y<sub>i</sub></i>(1) − <i>Y<sub>i</sub></i>(0)] because it makes the two "
            "observed conditional means unbiased for the two average potential outcomes. "
            "That is the whole trick, and it is enough for most of first-year econometrics."
        ),
        P(
            "The trick rests on an assumption that is usually stated once and then ignored. "
            "The stable unit treatment value assumption (SUTVA; Rubin 1980, building on "
            "Cox 1958) has two parts: there is one version of treatment, and unit <i>i</i>'s "
            "outcome does not depend on anyone else's treatment. The second part is the one "
            "this project is about. If it fails, <i>Y<sub>i</sub></i> is a function of the "
            "<i>entire</i> assignment vector <b>D</b>,"
        ),
        D("Y<sub>i</sub> = Y<sub>i</sub>(<b>D</b>), <b>D</b> ∈ {0,1}<super>N</super>."),
        P(
            "There are then 2<sup>N−1</sup> different “effects of treating <i>i</i>,” one for "
            "each configuration of the others, and the scalar <i>Y<sub>i</sub></i>(1) − "
            "<i>Y<sub>i</sub></i>(0) is not an object of the experiment. Well-posed questions "
            "are questions about <i>assignment rules</i>: what is the expected population mean "
            "under rule π compared with rule π′? Those are the objects Halloran and Struchiner, "
            "and later Hudgens and Halloran (2008), organised into direct, indirect, total and "
            "overall effects. Lecture 4 returns to the taxonomy. What you need now is only "
            "this: once interference is admitted, the estimand must be named as a contrast of "
            "policies, not as an average of individual effects."
        ),
        H(2, "The project's three rules, in that language"),
        P(
            "The kernel, written out in METHODOLOGY.md §2, updates each agent's behaviour "
            "by a logistic of own lag, a linear-in-means peer term with coefficient γ, "
            "covariates, and a treatment shifter that turns on at date zero. The peer term "
            "is interference by construction, and γ = 0 is excluded from the parameter box "
            "so that a no-interference world cannot silently survive calibration. Three "
            "assignment rules are frozen, all with the same budget of 80 treated agents "
            "out of N = 800 when anyone is treated:"
        ),
        B(
            "π<sub>0</sub>, control: D = 0 for everyone.",
            "π<sub>1</sub>, random: a simple random sample of 80 agents, without replacement.",
            "π<sub>2</sub>, degree: the 80 highest-degree agents. Deterministic given the graph.",
        ),
        P(
            "The headline estimand is the overall contrast of hub-seeding against control,"
        ),
        D(
            "θ<sub>2</sub>(c) = E<sub>c</sub>[Ȳ<sub>T</sub> | π<sub>2</sub>] − E<sub>c</sub>[Ȳ<sub>T</sub> | π<sub>0</sub>]."
        ),
        P(
            "θ<sub>1</sub>(c) is the same contrast with π<sub>1</sub> in place of π<sub>2</sub>. "
            "The targeting premium τ(c) = θ<sub>2</sub>(c) − θ<sub>1</sub>(c) is zero in any "
            "SUTVA world with a constant individual effect, because any 80 treated agents "
            "then produce the same mean. A nonzero premium is interference made visible as "
            "an estimand. Expectations are over simulation noise only. The rules, given the "
            "graph, are deterministic for π<sub>0</sub> and π<sub>2</sub> and are a known "
            "design for π<sub>1</sub>. That last distinction will matter in Lecture 4: a "
            "design-based estimator needs a design, and π<sub>2</sub> does not have one."
        ),
        H(1, "4. Identification is not estimation"),
        P(
            "A parameter, or a functional of a complete-data law, is <i>point-identified</i> "
            "if the distribution of observables, plus the maintained assumptions, pick out "
            "a single value. It is <i>set-identified</i> (partially identified) if they pick "
            "out a set with more than one point and less than the whole parameter space. "
            "It is unidentified if they pick out the whole space. Identification is a "
            "statement about the population and the assumptions. It does not mention sample "
            "size. Estimation is what one does with a sample once the identified object "
            "has been named. A confidence interval is a statement about sampling uncertainty "
            "around an identified object. It is not itself an identified set."
        ),
        P(
            "Lecture 2 is entirely about that distinction, in Manski's language. What you "
            "need now is only the discipline it imposes on later lectures. The image "
            "Θ<sub>hm</sub> = { θ<sub>2</sub>(c) : c not ruled out } will be reported the "
            "way one reports an identified set: as the values still compatible with the "
            "objects one is willing to maintain. It will not be claimed as a theorem that "
            "Θ<sub>hm</sub> <i>is</i> a Manski identified set. The reasons are in Lectures "
            "2 and 5; the short version is that ruling-out uses a thresholded discrepancy, "
            "folds sampling and Monte Carlo error into the test, and lives in a complete "
            "simulator whose incompleteness is the unknown calibration, not a missing "
            "counterfactual."
        ),
        C(
            "A set is not a distribution",
            "Putting a uniform (or any) probability on the surviving calibrations, and "
            "reporting a mean and standard deviation of θ<sub>2</sub>(c) as if they were "
            "posterior moments, is an extra assumption. History matching refuses that "
            "assumption. So does partial identification. The notes will not smuggle it "
            "back in by calling Θ a “distribution of treatment effects.”",
        ),
        H(1, "5. What the simulator is, and is not"),
        P(
            "An agent-based model, in the sense this project uses the phrase, is a "
            "stochastic recursive map on a finite population. Each of N = 800 agents has "
            "a state Y<sub>i</sub>(t) ∈ (0, 1), a covariate vector X<sub>i</sub>, and a "
            "place in an Erdős–Rényi graph drawn once and then frozen. The next state is "
            "a logistic of own lag, mean neighbour state, covariates, own treatment, and "
            "Gaussian noise. That is the entire “ABM.” There are no emergent institutions, "
            "no integer programming, no GIS layer, no Mesa schedule. The minimality is "
            "intentional. The scientific object is not a realistic society. It is a "
            "complete data-generating process in which interference is explicit, cheap to "
            "simulate, and impossible for a SUTVA estimator to represent unless neighbour "
            "treatment is handed to it as a feature."
        ),
        P(
            "Three consequences follow, and they are why a simulator is the right host "
            "for the question. First, the planner's number θ<sub>true</sub>(c<sub>0</sub>) "
            "exists, because we can run the kernel at c<sub>0</sub> under both rules as "
            "often as we like. In a field study that number is the thing one never sees. "
            "Second, the assignment mechanism is known, including when it is degenerate. "
            "Third, “calibration uncertainty” can be separated from “sampling uncertainty "
            "in a panel,” because we can hold the world fixed and vary the panel, or hold "
            "the panel's design fixed and vary the world. Those two variations are the two "
            "legs of the pipeline."
        ),
        H(1, "6. Two ways the model is not the world"),
        P(
            "History matching (Lecture 1) already admits that the kernel, even at the right "
            "c, will not reproduce the real system. That admission is the discrepancy "
            "budget δ, frozen at two percentage points on each moment. It is an admission "
            "about the <i>simulator</i>."
        ),
        P(
            "A second, logically distinct failure is that the number treated as the outcome "
            "is not the thing the estimand named. That is a question about operationalization, "
            "not about the kernel. Lecture 3 treats it as an admission restriction on "
            "scoring rules: an oracle, a noisy survey, and a bad item that loads on a "
            "treatment-channel covariate, of which only the first two pass a pre-declared "
            "correlation threshold. The image of the estimand over the admissible scores, "
            "at one world, is a second set, Θ<sub>cv</sub>. It is not a second pass over "
            "the not-ruled-out calibrations. Folding the two sets into one “uncertainty "
            "interval” would undo the diagnosis."
        ),
        H(1, "7. The pipeline, named"),
        T(
            [
                ["Stage", "Input", "Output", "Consumes NROY?"],
                ["Anchors", "World Bank API v2", "z (DPT mean 86.2, corr 0.605, internet 68.6)", "No"],
                ["History matching", "z, box C, I(c) ≤ τ", "NROY set C", "Produces it"],
                ["Image maps", "C, θ<sub>2</sub>(·), δ<sub>spill</sub>(·)", "Θ<sub>hm</sub>, Θ<sub>exp</sub>", "Yes"],
                ["Select c<sub>0</sub>", "C", "median-I survivor", "As a selection"],
                ["Simulate panel", "c<sub>0</sub>, π, kernel", "micro-data (Y, D, X)", "No"],
                ["Measurement admission", "scores m<sub>1</sub>, m<sub>2</sub>, m<sub>3</sub>", "M*, Θ<sub>cv</sub>", "No"],
                ["Foil 1 (forest / BCF)", "panel at c<sub>0</sub>", "I<sub>BCF</sub>", "No"],
                ["Foil 2 (exposure map)", "π<sub>1</sub> panel at c<sub>0</sub>", "I<sub>E2</sub>", "No"],
                ["Oracle", "kernel at c<sub>0</sub>", "θ<sub>true</sub>(c<sub>0</sub>)", "No"],
            ],
            "Table 1. Assembled pipeline. Anchor values are from the 2026-08-12 fetch (scripts/data/anchors.json). Θ_exp and I_E2 exist only if draft AMENDMENT-01 is accepted. No stage after “Anchors” has been run.",
        ),
        P(
            "The money plot of the project is an overlay of I<sub>BCF</sub>, I<sub>E2</sub>, "
            "Θ<sub>hm</sub>, Θ<sub>exp</sub>, Θ<sub>cv</sub>, and a tick at "
            "θ<sub>true</sub>(c<sub>0</sub>). Each one-world interval is judged against its "
            "own honest set. Cross-plotting the forest interval against Θ<sub>exp</sub> mixes "
            "estimands. Pre-registered verdicts — F-OVERCONF, F-HONEST, F-EMPTY, "
            "F-SINGLETON — are defined in METHODOLOGY.md §10 and restated in Lecture 5. "
            "All of them are publishable. A paper that can only be written if the forest "
            "looks overconfident is not a pre-registered paper."
        ),
        H(1, "8. Language discipline"),
        P(
            "Several compressions were tried, in conversation and in a set of notes produced "
            "with an external chatbot, and then rejected. They are listed here so they do "
            "not re-enter the later lectures, or the eventual write-up, by habit."
        ),
        T(
            [
                ["Rejected phrase", "Why", "Replacement"],
                [
                    "NROY = observationally valid calibrations",
                    "Low I does not certify truth or observational equivalence",
                    "Not ruled out yet, given V and τ",
                ],
                [
                    "I(c) is a stack of moment inequalities",
                    "I ≤ τ is one joint ellipsoid, not E[g] ≥ 0",
                    "A pedagogical bridge, not a Pakes–Tamer model",
                ],
                [
                    "Distribution of treatment effects over NROY",
                    "Smuggles a measure onto a set",
                    "Image of a named functional; a set",
                ],
                [
                    "HM assumes perfect measurements",
                    "δ exists because they are not",
                    "HM assumes the chosen moments are the right ones",
                ],
                [
                    "Θ_hm is a Manski identified set",
                    "Threshold, sampling-in-V, complete kernel",
                    "Same reporting logic; not-ruled-out image",
                ],
                [
                    "Equifinal c's give wildly different θ",
                    "Width is empirical, not a theorem",
                    "They can differ; if they do not, that is a finding",
                ],
                [
                    "A point estimate is structurally dishonest",
                    "Moral language for an estimator asked a different question",
                    "A selection from the image",
                ],
                [
                    "The field typically reports a single number",
                    "Unscoped universal; not evidenced here",
                    "Name the tradition and what its interval contains",
                ],
                [
                    "Cvprofiles screens out simulations",
                    "The layer screens measures, at one world",
                    "Admission of scoring rules; Θ_cv at c<sub>0</sub>",
                ],
                [
                    "Causal forests are SOTA for interference",
                    "They are SOTA for HTE under SUTVA",
                    "Architecture cannot see a γ edge it is not handed",
                ],
            ],
            "Table 2. Forbidden compressions. Lectures 1–5 are written against this table. If a later sentence violates it, the sentence is wrong.",
        ),
        H(1, "9. What this course is not"),
        B(
            "It is not a course in building agent-based models. The kernel is one equation.",
            "It is not a course in do-calculus. Graphical identification is a parallel language; Lecture 4 mentions it only to put it down.",
            "It is not a proof of a new estimator. Aronow–Samii and Wager–Athey and Hahn–Murray–Carvalho are used off the shelf.",
            "It is not a literature review of equifinality. Lecture 5 names the near-neighbours so the wedge can be stated narrowly.",
            "It is not a forecast of the overlay. Waves have not been run.",
            "It is not, yet, a freeze of the specification. You will read, then ask, then we will decide what to freeze.",
        ),
        H(1, "10. Reading order, and what each lecture is for"),
        T(
            [
                ["Lecture", "Object it defines", "What it refuses"],
                [
                    "1 History matching",
                    "I(c), V, τ, NROY, δ, waves",
                    "A posterior; a policy number; “observationally valid”",
                ],
                [
                    "2 Partial identification",
                    "Identified set as a population object; Law of Decreasing Credibility",
                    "Set = confidence set; set = distribution; Θ_hm is a Manski set",
                ],
                [
                    "3 Measurement admission",
                    "m<sub>1</sub>, m<sub>2</sub>, m<sub>3</sub>, M*, Θ_cv",
                    "Screening NROY; a general proxy-validity test",
                ],
                [
                    "4 Two foils",
                    "I_BCF, I_E2, exposure strata, the π<sub>2</sub> design fact",
                    "Forests as SOTA for interference; E2 on a deterministic rule",
                ],
                [
                    "5 Composition",
                    "The overlay; modern simulation practice; the December deliverable",
                    "A claim of uniqueness about equifinality; promised findings",
                ],
            ],
            "Table 3. The course as five objects and five refusals.",
        ),
        H(1, "11. Notation, collected"),
        T(
            [
                ["Symbol", "Meaning"],
                ["N, A, k<sub>i</sub>", "Population size 800; adjacency; degree (floored at 1)"],
                ["c = (α, β, γ, κ, σ<sub>ε</sub>)", "Free calibration; η fixed"],
                ["C, NROY", "Original box; not-ruled-out-yet subset after wave 3"],
                ["z, M(c), I(c), τ, δ", "Anchors; moment map; implausibility; threshold; discrepancy"],
                ["π<sub>0</sub>, π<sub>1</sub>, π<sub>2</sub>", "Control; SRSWOR of 80; top-80 degree"],
                ["θ<sub>1</sub>, θ<sub>2</sub>, τ", "Random-seed contrast; hub-seed contrast; premium"],
                ["Θ<sub>hm</sub>, Θ<sub>exp</sub>, Θ<sub>cv</sub>", "Images: of θ<sub>2</sub> over NROY; of δ_spill over NROY; of θ<sub>2</sub> over M* at c<sub>0</sub>"],
                ["c<sub>0</sub>", "Pre-declared median-implausibility survivor"],
                ["I<sub>BCF</sub>, I<sub>E2</sub>", "One-world intervals: SUTVA forest / BCF; exposure-mapped Hájek"],
                ["θ<sub>true</sub>(c<sub>0</sub>)", "Planner's number; known only because we simulate"],
            ],
            "Table 4. Notation used from Lecture 1 onward. Subscripts on Θ and I are labels, not indexes over units.",
        ),
        H(1, "12. A last orientation before Lecture 1"),
        P(
            "If you remember four sentences from this lecture, remember these. Interference "
            "makes individual effects ill-defined; name a policy contrast. Calibration by "
            "ruling-out produces a set in parameter space, not a posterior. The honest "
            "policy report is the image of the contrast over that set, plus, separately, "
            "the image over admissible ways of scoring Y. A modern one-world interval, "
            "however honest on its own terms, answers a different question, and the project "
            "is built to say so even if, in the event, that interval covers the image."
        ),
        P(
            "Lecture 1 starts from the simulator's problem, not from ours: why a best-fit "
            "input is the wrong primitive once the model is not the world."
        ),
        H(1, "References"),
        R(
            "Cox, D. R. (1958). <i>Planning of Experiments</i>. New York: Wiley. (No-interference "
            "as a design assumption.)"
        ),
        R(
            "Holland, P. W. (1986). “Statistics and Causal Inference.” <i>Journal of the "
            "American Statistical Association</i> 81(396): 945–960."
        ),
        R(
            "Hudgens, M. G. and M. E. Halloran (2008). “Toward Causal Inference with "
            "Interference.” <i>Journal of the American Statistical Association</i> "
            "103(482): 832–842."
        ),
        R(
            "Manski, C. F. (2003). <i>Partial Identification of Probability Distributions</i>. "
            "New York: Springer."
        ),
        R(
            "Rubin, D. B. (1980). “Randomization Analysis of Experimental Data: The Fisher "
            "Randomization Test. Comment.” <i>Journal of the American Statistical "
            "Association</i> 75(371): 591–593. (SUTVA named.)"
        ),
        R(
            "Vernon, I., M. Goldstein and R. G. Bower (2010). “Galaxy Formation: A Bayesian "
            "Uncertainty Analysis.” <i>Bayesian Analysis</i> 5(4): 619–669."
        ),
    ],
}

json_path = OUT / "lecture-00-introduction.json"
json_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {json_path} ({json_path.stat().st_size} bytes, {len(spec['elements'])} elements)")
