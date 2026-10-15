#!/usr/bin/env python3
"""Generate lecture-01 JSON and build the PDF."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("/Users/bonorinoa/Desktop/Github_Repositories/ecn593-poc-abm/docs/lectures")

P = lambda text: {"type": "paragraph", "text": text}
H = lambda n, text: {"type": "heading", "level": n, "text": text}
B = lambda *items: {"type": "bullet", "items": list(items)}
E = lambda *items: {"type": "enum", "items": list(items)}
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
    "lecture_number": 1,
    "title": "History Matching",
    "subtitle": "Ruling out worlds rather than fitting them",
    "running_header": "Lecture 1 · History Matching",
    "author": "ECN 593 short course notes (study draft, not a frozen specification)",
    "date": "August 2026",
    "abstract": (
        "History matching is a method for discarding regions of a simulator's input space "
        "that cannot, given stated uncertainties, reproduce a vector of observed moments. "
        "Its native deliverable is a not-ruled-out-yet (NROY) set in parameter space, not a "
        "posterior and not a policy number. This lecture traces the method from reservoir "
        "engineering through Bayes-linear uncertainty quantification to the Galform galaxy-formation "
        "studies, defines implausibility, waves, and model discrepancy, and works a one-dimensional "
        "numerical example in full. The project's own design — direct evaluation, a χ² threshold "
        "on four moments, a frozen discrepancy budget — is located at the end. No calibration "
        "wave has been run; nothing here is a result."
    ),
    "elements": [
        H(1, "1. The problem a simulator creates"),
        P(
            "A computer model takes a vector of inputs <i>c</i> — physical constants, "
            "tuning parameters, initial conditions — and returns a vector of outputs. "
            "When the model is cheap and the input dimension is small, one can search for a "
            "best fit. When the model is expensive, the input box is high-dimensional, and "
            "the model is known to be a simplification of the system it represents, "
            "best-fit search is the wrong primitive. A point that matches the data slightly "
            "better than its neighbours may do so for the wrong physical reason, and a point "
            "that matches slightly worse may be equally acceptable once one admits that the "
            "model is not the world."
        ),
        P(
            "The scientific question then changes. It is no longer “what is the maximum-likelihood "
            "input?” It is “which inputs have not yet been shown to be incompatible with the "
            "observations, once we have budgeted for observation error, for the fact that we "
            "evaluate the model only a finite number of times, and for the fact that even the "
            "right input would not reproduce the system exactly?” That is the question history "
            "matching was built to answer."
        ),
        P(
            "An economist already knows a cousin of this question. Identification asks which "
            "parameter values are compatible with the distribution of observables under a "
            "stated assumption menu (Lecture 2). History matching asks which <i>simulator "
            "inputs</i> are compatible with a finite vector of moments, under a stated "
            "discrepancy budget. The objects live in different spaces and the tests have "
            "different formal status. The reporting instinct is the same: do not collapse a "
            "set of still-possible values to a convenience point."
        ),
        H(1, "2. A short history of the method"),
        H(2, "Reservoirs, and the word “history”"),
        P(
            "In petroleum engineering, “history matching” originally meant something more "
            "literal: adjust the geological description of a reservoir until a fluid-flow "
            "simulator reproduces the observed pressure and production <i>history</i> at the "
            "wells. The input space is large (porosities, permeabilities, fault multipliers); "
            "each run of the reservoir simulator is expensive; and no geologist believes the "
            "simulator is the reservoir. Craig, Goldstein, Seheult and Smith recast that craft "
            "as a Bayes-linear computer experiment. A preliminary account appears as Craig, "
            "Goldstein, Seheult and Smith (1996); the case study that became the canonical "
            "reference is Craig, Goldstein, Seheult and Smith (1997), in <i>Case Studies in "
            "Bayesian Statistics</i> III, pages 37–93."
        ),
        P(
            "Two design choices in that work still organise the literature. First, beliefs "
            "are specified only through means, variances and covariances, and are updated by "
            "linear fitting — the Bayes-linear programme later treated at book length by "
            "Goldstein and Wooff (2007). Full posterior distributions over high-dimensional "
            "input spaces are not required and, the authors argue, not honest: the expert "
            "cannot specify them. Second, the aim is not to produce a single matched geology. "
            "It is to discard geologies that cannot match, and to keep those that still might."
        ),
        H(2, "From oil to galaxies"),
        P(
            "The same apparatus was applied, at much larger scientific scale, to Galform, "
            "a semi-analytic model of galaxy formation. Vernon, Goldstein and Bower (2010), "
            "<i>Bayesian Analysis</i> 5(4): 619–669, is the technical uncertainty analysis: "
            "iterative emulation, implausibility cut-offs, and an explicit structural-uncertainty "
            "(model-discrepancy) term, used to cut the input space down to the region that "
            "could still match luminosity-function data. A shorter account, written for a "
            "statistical audience as a case study in history matching itself, is Vernon, "
            "Goldstein and Bower (2014), <i>Statistical Science</i> 29(1): 81–90. A companion "
            "astronomy paper, Bower, Vernon, Goldstein and co-authors (2010), "
            "<i>Monthly Notices of the Royal Astronomical Society</i> 407: 2017–2045, reports "
            "that successive waves of emulation left about 0.26 percent of the original volume "
            "of interest — and that, inside that volume, the previously published “best” Galform "
            "calibration is only one of many acceptable points."
        ),
        P(
            "That last sentence is the one an economist should not skim. History matching, "
            "done honestly, routinely produces a large set of inputs that fit the calibration "
            "targets. The scientific product of the Galform analysis is that set, and the "
            "physical degeneracies it reveals, not a preferred point."
        ),
        H(2, "A parallel, and different, Bayesian tradition"),
        P(
            "Kennedy and O'Hagan (2001), <i>Journal of the Royal Statistical Society</i> Series B "
            "63(3): 425–464, is the other canonical paper on calibrating computer models. It is "
            "not history matching. Kennedy and O'Hagan place a Gaussian-process emulator on the "
            "simulator, a second Gaussian process on the discrepancy between the best-fitting "
            "run and the real system, and then compute a posterior over inputs and discrepancy "
            "given the field data. The deliverable is probabilistic: a posterior-predictive "
            "distribution for future system behaviour. History matching's deliverable is "
            "set-valued: a region of input space that has not been ruled out. Both traditions "
            "treat model discrepancy as first-class. They disagree about whether the analyst "
            "should put a probability measure on the remaining inputs."
        ),
        P(
            "Applied work often mixes the two. Many “history matching” papers now use Gaussian-process "
            "emulators as cheap surrogates and then apply implausibility cut-offs to the "
            "emulator rather than to the simulator (Andrianakis, Vernon, McCreesh and "
            "co-authors, 2015, <i>PLOS Computational Biology</i> 11(1): e1003968, is a clear "
            "epidemiological example). The project's own specification does <i>not</i> do this. "
            "METHODOLOGY.md §6 freezes direct evaluation of the kernel: no emulator. That is a "
            "deliberate small-model choice. At N = 800 and half a millisecond per run, the "
            "simulator is cheap enough that the surrogate is an unnecessary source of "
            "approximation. The lecture will treat emulation as part of the literature, not "
            "as part of the project."
        ),
        H(1, "3. Formal objects"),
        H(2, "The input box and the moment map"),
        P(
            "Write <i>C</i> for a closed box in input space — the set of calibrations the "
            "analyst is willing to entertain before seeing the data. Write <i>f</i>(<i>c</i>, ω) "
            "for one run of the simulator at input <i>c</i> with internal noise ω. A "
            "<i>moment map</i> <i>M</i> sends <i>c</i> to a low-dimensional vector of "
            "functionals of the simulated output that have empirical counterparts. The "
            "empirical counterparts are the <i>anchors</i> <i>z</i>. In this project the "
            "anchors are three World Bank statistics (a mean immunization rate, an "
            "education–behaviour correlation, a mean internet-use rate), assembled into a "
            "four-dimensional <i>z</i> once sampling variances are counted; they are moments "
            "of a cross-country distribution, not “empirical parameters” of the kernel."
        ),
        P(
            "Because each run is noisy, one does not observe <i>M</i>(<i>c</i>). One observes "
            "a Monte Carlo estimate <i>M̂</i>(<i>c</i>), whose variance σ²<sub>MC</sub> can be "
            "driven down by replication. The anchors <i>z</i> themselves are sample moments, "
            "with sampling variances σ²<sub>sampling</sub>. A third variance, δ², is not "
            "estimated from either sample. It is a <i>model-discrepancy budget</i>: the "
            "analyst's statement of how close the simulator, even at the right <i>c</i>, is "
            "required to come to the real system on these moments."
        ),
        H(2, "Implausibility"),
        P(
            "The implausibility of a point <i>c</i> is a standardised, squared distance "
            "between anchors and simulated moments. In the form this project freezes "
            "(METHODOLOGY.md §6),"
        ),
        D(
            "I(c) = (z − M̂(c))′ V<sup>−1</sup> (z − M̂(c)), "
            "V = diag(σ²<sub>sampling</sub>(z) + σ²<sub>MC</sub>(M̂) + δ²)."
        ),
        P(
            "A point is <i>ruled out</i> if I(<i>c</i>) exceeds a threshold τ, and "
            "<i>not ruled out yet</i> otherwise. The acronym NROY is the claim: a low score "
            "does not certify that <i>c</i> is true, or even that it is observationally "
            "equivalent to the data-generating process in Manski's sense. It certifies only "
            "that, given V and τ, we are not yet entitled to discard it. Vernon, Goldstein "
            "and Bower (2010, §3) are explicit on this reading: large implausibility is "
            "evidence against an input; small implausibility is not evidence for it."
        ),
        P(
            "Two common choices of τ should not be confused. The folklore cut-off I = 3, "
            "applied to a <i>standardised</i> (not squared) implausibility, comes from "
            "Pukelsheim's three-sigma rule (Pukelsheim 1994, <i>The American Statistician</i> "
            "48(2): 88–91). For a unimodal distribution, P(|X − μ| ≥ 3σ) ≤ 4/81 &lt; 0.05. "
            "If one is willing to treat the standardised moment error as unimodal, a "
            "standardised implausibility above 3 is grounds to discard at a 95 percent "
            "standard. The project's specification does something different and more "
            "transparent for a four-dimensional moment vector: it treats I(<i>c</i>) as a "
            "χ²-type quadratic form and sets"
        ),
        D("τ = χ²<sub>4; 0.95</sub> ≈ 9.488."),
        P(
            "That is a joint ellipsoid in moment space, not four separate three-sigma tests "
            "and not Pukelsheim's bound applied coordinate-wise. Section 5 computes both "
            "objects on a toy example so the difference is visible."
        ),
        H(2, "Waves"),
        P(
            "A single pass over C is usually wasteful. Most of the box is implausible, and "
            "the interesting region, if it exists, occupies a small subset. History matching "
            "therefore proceeds in <i>waves</i>. Wave 1 draws a space-filling design over "
            "the original box (in this project, a Latin hypercube of 1,000 points), evaluates "
            "I, and discards. Wave 2 redraws inside a modest inflation of the surviving "
            "bounding box. Wave 3 repeats. NROY is defined as the union of points that "
            "survive the final wave (METHODOLOGY.md §6: three waves, next-wave box inflated "
            "by 20 percent). If the union is empty, the pair (kernel, anchors) is rejected "
            "at the stated δ and τ. That outcome has a name in the specification, F-EMPTY, "
            "and a forbidden response: do not loosen τ to rescue the exercise."
        ),
        P(
            "In the Galform analyses the waves are built around emulators, because a single "
            "Galform evaluation is expensive. In this project the waves are built around "
            "the kernel itself. The logic of ruling-out is the same; the approximation "
            "stack is thinner."
        ),
        H(1, "4. Model discrepancy is not an afterthought"),
        P(
            "If δ = 0 and the Monte Carlo and sampling variances are small, I(<i>c</i>) "
            "becomes a test of whether the simulator can hit the anchors exactly. No "
            "interesting simulator can. Craig, Goldstein, Seheult and Smith already treated "
            "the gap between simulator and system as an object of belief, not as a residual "
            "to be ignored. Kennedy and O'Hagan (2001) gave the same gap a Gaussian-process "
            "name, “model inadequacy,” and insisted that calibration without it produces "
            "overconfident posteriors. Vernon, Goldstein and Bower (2010) carry an explicit "
            "structural-uncertainty term and note that, with a realistic such term, Galform "
            "can match data sets previously declared incompatible."
        ),
        P(
            "This project's δ is cruder than any of those: a frozen, diagonal, "
            "two-percentage-point budget on each moment. Crude is not the same as absent. "
            "The specification refuses to pretend that M(c) would equal z at the true c. "
            "What it does <i>not</i> do — and this is Lecture 3, not this one — is ask "
            "whether the simulated outcome, scored as we score it, is a valid "
            "operationalization of the construct the estimand named. Discrepancy is about "
            "the kernel as a model of the world. Construct failure is about the number we "
            "treat as Y. They are not substitutes."
        ),
        C(
            "This is not a claim that measurements are perfect",
            "A common misreading, including in notes produced while preparing this course, "
            "is that history matching “implicitly assumes measurements perfectly represent "
            "the underlying system.” That is the opposite of the method's point. The term δ "
            "exists because they do not. What history matching does assume is that the "
            "<i>chosen moments</i> are the right functionals to match, and that the budget δ "
            "is adequate for everything the kernel cannot do. Those are substantial "
            "assumptions. They are not the assumption that z is the truth of the system.",
        ),
        H(1, "5. Worked example: one moment, then two"),
        P(
            "The numbers in this section are invented for arithmetic. They are not World Bank "
            "estimates and they are not project results."
        ),
        H(2, "One moment"),
        P(
            "Suppose a single anchor is z = 86, a simulated moment at a candidate c is "
            "M̂(c) = 81, the sampling standard deviation of the anchor is 2, the Monte Carlo "
            "standard deviation of M̂ is 1, and the discrepancy budget is δ = 2, all in the "
            "same units. Then"
        ),
        D(
            "V = 2<sup>2</sup> + 1<sup>2</sup> + 2<sup>2</sup> = 4 + 1 + 4 = 9, "
            "z − M̂ = 5, I(c) = 25/9 ≈ 2.778."
        ),
        P(
            "The standardised implausibility is √I = 5/3 ≈ 1.667. Against Pukelsheim's "
            "cut-off of 3, the point is retained. Against a one-degree-of-freedom χ² test "
            "at 95 percent, τ = χ²<sub>1; 0.95</sub> ≈ 3.841, and 2.778 &lt; 3.841, so the "
            "point is retained on that rule too. If instead M̂(c) = 80, then I = 36/9 = 4, "
            "which exceeds the χ² cut-off 3.841, while √I = 2 still sits below Pukelsheim's 3. "
            "The two rules disagree on that row. Careful with the scale:"
        ),
        T(
            [
                ["M̂(c)", "z − M̂", "I = (z−M̂)² / 9", "√I", "vs χ²<sub>1;0.95</sub> ≈ 3.84", "vs Pukelsheim √I ≥ 3"],
                ["81", "5", "2.778", "1.667", "retain", "retain"],
                ["80", "6", "4.000", "2.000", "reject (I>3.84)", "retain (√I&lt;3)"],
                ["77", "9", "9.000", "3.000", "reject", "borderline"],
                ["76", "10", "11.111", "3.333", "reject", "reject"],
            ],
            "Table 1. Invented one-moment arithmetic. V = 9 throughout. The χ² rule, applied to squared I, is more aggressive here than Pukelsheim's rule applied to √I. The two cut-offs are not interchangeable, and this project uses the χ² form in four dimensions.",
        ),
        P(
            "Two observations. First, “I = 3” in the folklore is a statement about the "
            "<i>standardised</i> implausibility, i.e. about √I in our notation, not about "
            "the quadratic form. Mixing the two is a common source of off-by-a-square "
            "errors. Second, even in one dimension the retain/reject decision is sensitive "
            "to δ. Set δ = 0 in the first row and V drops to 5, I becomes 5, and a point "
            "that looked comfortable is now rejected at 95 percent. The discrepancy budget "
            "is not a technicality. It is often the term that decides membership in NROY."
        ),
        H(2, "Two moments, and why the restriction is an ellipsoid"),
        P(
            "Now suppose a second moment has the same V<sub>22</sub> = 9, residual "
            "z<sub>2</sub> − M̂<sub>2</sub> = 9, and the off-diagonal of V is zero. The "
            "joint implausibility is the sum of the coordinate-wise terms,"
        ),
        D("I(c) = 25/9 + 81/9 = 106/9 ≈ 11.778."),
        P(
            "The 95 percent χ² threshold with two degrees of freedom is "
            "χ²<sub>2; 0.95</sub> ≈ 5.991. The point is ruled out jointly even though the "
            "first coordinate, on its own, was not. A rectangle of separate 95 percent "
            "tests would reject a coordinate if |e<sub>k</sub>| / √V<sub>kk</sub> exceeded "
            "1.96. That rectangle, mapped back into the I-scale, is not the χ² ellipse. "
            "The corner of the 95 percent box has squared radius 2 × 1.96² ≈ 7.68, which "
            "is larger than 5.991: the ellipse is inside the box. Joint implausibility is "
            "stricter than a pair of marginal tests at the same nominal level, and it is "
            "a single inequality I ≤ τ, not a stack of linear moment inequalities "
            "E[g] ≥ 0."
        ),
        C(
            "A pedagogical bridge, not a theorem",
            "It is useful, when talking to an econometrician, to say that I(c) ≤ τ is a "
            "restriction on moments, hence in the same broad family as moment inequalities. "
            "It is not useful to say that history matching <i>is</i> a Pakes–Tamer or "
            "Ciliberto–Tamer model. Those models generate sets because a solution concept "
            "or an optimizing inequality fails to select a unique outcome. Here the kernel "
            "is a complete map. The set lives in input space because the anchors, plus a "
            "tolerance, fail to select a unique input. Lecture 2 returns to this distinction.",
        ),
        H(1, "6. What history matching does not give you"),
        C(
            "This is not",
            "A posterior over c. A probability that c is true. A policy number. A validated "
            "construct for Y. A statement that the surviving inputs are observationally "
            "equivalent to one another, or to the real system, in Manski's sense. A licence "
            "to average θ(c) over NROY as if the average were a posterior mean. All of "
            "those objects require extra assumptions that history matching, as defined here, "
            "refuses to make.",
        ),
        P(
            "What it does give you is a set C<sub>NROY</sub> ⊆ C and a transparent account "
            "of why each discarded point was discarded. That set is the right input to a "
            "<i>later</i> calculation, if the scientific question lives in a different space. "
            "The Galform papers stop at the set, because the scientific question was which "
            "galaxy-formation inputs remain viable. A policy question — what is the effect "
            "of a named intervention — lives in estimand space. Mapping the set through a "
            "named functional is a further step. It is the step this project is built to "
            "take, and it is the subject of Lecture 5, not of this one."
        ),
        P(
            "Two failure modes of the set itself are pre-registered in METHODOLOGY.md §7. "
            "If C<sub>NROY</sub> is empty, the pair (kernel, anchors) is rejected "
            "(F-EMPTY). If the surviving box collapses to a sliver of the original volume, "
            "the design is too tight to be informative about a set (F-SINGLETON), and the "
            "protocol says to widen one declared coordinate rather than to celebrate "
            "point identification. Neither failure is to be repaired by moving τ."
        ),
        H(1, "7. A cousin the economist already knows"),
        P(
            "The method of simulated moments (McFadden 1989; Pakes and Pollard 1989) uses "
            "the same ingredients: a simulator, a vector of moments, a weight matrix, a "
            "search over a parameter box. The deliverable is a point, ĉ, that minimises a "
            "quadratic form in z − M̂(c), together with a standard-error matrix that treats "
            "sampling variation in z (and, if one is careful, simulation noise in M̂) as the "
            "uncertainty. If the model is correctly specified and the moments identify c, "
            "the point is consistent and the standard errors are a licence to draw a "
            "confidence ellipse around it."
        ),
        P(
            "History matching uses the same quadratic form as a <i>test</i>, not as an "
            "objective to be minimised. Every c that fails to reject is kept. There is no "
            "preferred point, and there is no sampling distribution over the survivors. "
            "The weight matrix V includes a discrepancy term that simulated-moment "
            "standard errors do not. And the scientific claim, if the set is large, is not "
            "that estimation was imprecise. It is that the moments do not pin the input "
            "down — a statement about identification, not about sample size."
        ),
        P(
            "This project's moment count makes the contrast concrete. The free coordinates "
            "of c are five (α, β, γ, κ, σ<sub>ε</sub>); η is held fixed. The anchor vector "
            "is four-dimensional. A simulated-moment estimator would be underidentified on "
            "that count alone, before any of the kernel's nonlinearities or the discrepancy "
            "budget are considered. History matching does not need the count to go the "
            "other way. A set-valued answer is the intended object, not a failure of the "
            "estimator to find a unique minimum."
        ),
        P(
            "Generalised likelihood uncertainty estimation (GLUE; Beven and Binley 1992) "
            "is a closer cousin still: keep the “behavioural” parameter vectors, discard "
            "the rest, propagate the ensemble through a prediction. Lecture 5 returns to "
            "GLUE and to later equifinality papers when the question is what to do with "
            "the set. This lecture only needs the distinction of deliverables: MSM wants "
            "a point; HM and GLUE want a set in input space; this project wants the "
            "<i>image</i> of a named causal estimand over that set."
        ),
        H(1, "8. Where this sits in the applied project"),
        P(
            "METHODOLOGY.md §6 freezes the following design. The kernel is cheap, so there "
            "is no emulator. Each wave is a 1,000-point Latin hypercube. Moments are "
            "evaluated with R<sub>m</sub> = 30 Monte Carlo replications per arm. The "
            "implausibility uses the quadratic form above, with δ = (2, 2, 2, 2) percentage "
            "points and τ = χ²<sub>4; 0.95</sub>. Three waves; next-wave box inflated 20 "
            "percent; NROY is the union of survivors. The policy estimand θ<sub>2</sub> "
            "(hub-seeding versus control) is then evaluated on a sample of 400 survivors, "
            "and the empirical range of those evaluations is the reported image Θ<sub>hm</sub>."
        ),
        P(
            "Two comments, both about what this lecture has earned and what it has not. "
            "First, sampling 400 survivors to trace an image is a computational device. It "
            "is not a claim that every survivor is equally likely, and it is not a posterior "
            "mean of θ<sub>2</sub>. Lecture 2 will refuse to put a uniform measure on an "
            "identified set for the same reason. Second, no wave has been run. There is no "
            "NROY yet. There is no Θ<sub>hm</sub> yet. Empty NROY is an admissible finding. "
            "The lecture has defined the objects; it has not filled them."
        ),
        H(1, "9. What to read first"),
        P(
            "If you read only two papers before Lecture 2, read Vernon, Goldstein and Bower "
            "(2010) for the formal apparatus (implausibility, waves, discrepancy) and "
            "Kennedy and O'Hagan (2001, §§1–2 and 6) for the contrasting Bayesian-calibration "
            "deliverable. Craig, Goldstein, Seheult and Smith (1997) is the historical "
            "source but is longer than it is conceptually denser. Pukelsheim (1994) is four "
            "pages and will stop you from misquoting the three-sigma rule."
        ),
        H(1, "References"),
        R(
            "Beven, K. and A. Binley (1992). “The Future of Distributed Models: Model "
            "Calibration and Uncertainty Prediction.” <i>Hydrological Processes</i> 6(3): 279–298."
        ),
        R(
            "McFadden, D. (1989). “A Method of Simulated Moments for Estimation of Discrete "
            "Response Models without Numerical Integration.” <i>Econometrica</i> 57(5): 995–1026."
        ),
        R(
            "Pakes, A. and D. Pollard (1989). “Simulation and the Asymptotics of Optimization "
            "Estimators.” <i>Econometrica</i> 57(5): 1027–1057."
        ),
        R(
            "Andrianakis, I., I. Vernon, N. McCreesh, T. J. McKinley, J. E. Oakley, "
            "R. N. Nsubuga, M. Goldstein and R. G. White (2015). “Bayesian History Matching "
            "of Complex Infectious Disease Models Using Emulation: A Tutorial and a Case "
            "Study on HIV in Uganda.” <i>PLOS Computational Biology</i> 11(1): e1003968."
        ),
        R(
            "Bower, R. G., I. Vernon, M. Goldstein, A. J. Benson, C. G. Lacey, C. M. Baugh, "
            "S. Cole and C. S. Frenk (2010). “The Parameter Space of Galaxy Formation.” "
            "<i>Monthly Notices of the Royal Astronomical Society</i> 407(4): 2017–2045."
        ),
        R(
            "Craig, P. S., M. Goldstein, A. H. Seheult and J. A. Smith (1996). “Bayes Linear "
            "Strategies for Matching Hydrocarbon Reservoir History.” In J. M. Bernardo, "
            "J. O. Berger, A. P. Dawid and A. F. M. Smith (eds.), <i>Bayesian Statistics 5</i>, "
            "69–95. Oxford: Clarendon Press."
        ),
        R(
            "Craig, P. S., M. Goldstein, A. H. Seheult and J. A. Smith (1997). “Pressure "
            "Matching for Hydrocarbon Reservoirs: A Case Study in the Use of Bayes Linear "
            "Strategies for Large Computer Experiments.” In C. Gatsonis, J. S. Hodges, "
            "R. E. Kass, R. McCulloch, P. Rossi and N. D. Singpurwalla (eds.), "
            "<i>Case Studies in Bayesian Statistics</i>, vol. III, 37–93. New York: Springer."
        ),
        R(
            "Goldstein, M. and D. Wooff (2007). <i>Bayes Linear Statistics: Theory and "
            "Methods</i>. Chichester: Wiley."
        ),
        R(
            "Kennedy, M. C. and A. O'Hagan (2001). “Bayesian Calibration of Computer "
            "Models” (with discussion). <i>Journal of the Royal Statistical Society</i>, "
            "Series B, 63(3): 425–464."
        ),
        R(
            "Pukelsheim, F. (1994). “The Three Sigma Rule.” <i>The American Statistician</i> "
            "48(2): 88–91."
        ),
        R(
            "Vernon, I., M. Goldstein and R. G. Bower (2010). “Galaxy Formation: A Bayesian "
            "Uncertainty Analysis” (with discussion). <i>Bayesian Analysis</i> 5(4): 619–669."
        ),
        R(
            "Vernon, I., M. Goldstein and R. G. Bower (2014). “Galaxy Formation: Bayesian "
            "History Matching for the Observable Universe.” <i>Statistical Science</i> "
            "29(1): 81–90."
        ),
    ],
}

json_path = OUT / "lecture-01-history-matching.json"
json_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"wrote {json_path} ({json_path.stat().st_size} bytes, {len(spec['elements'])} elements)")
