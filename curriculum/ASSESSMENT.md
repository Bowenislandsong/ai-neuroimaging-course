# Assessment: can she supervise the AI?

Passing code is a necessary computational check, not the learning outcome. Assess independent explanation and transfer. The learner may use AI and references while preparing, but must answer the final questions in her own words.

## Every class

Submit an input → operation → output card with shapes, units, space/time axis, parameters, fitting population, invariant, lost information, diagnostic and failure condition. Include a prediction made before execution, one intentionally wrong run, a repair with a reason, a source assignment note, and a short research-transfer explanation.

The instructor changes one meaningful setting and asks for a prediction before running it. Examples: nearest-neighbor to linear interpolation on a label image; TR without changing event units; high-pass relative to task frequency; participant split to row split; independent ROI to selected ROI; mean baseline to z normalization. Do not reward merely repeating the AI's explanation.

## Strand checkpoints

| Strand | Independent demonstration | Passing evidence |
|---|---|---|
| Processing | Trace a raw scan to a derivative, including geometry, interpolation, nuisance choices and QC | Correct transformation manifest, overlays/diagnostics, rejected failure and reason |
| Design | Defend question, estimand, timing, contrast, hierarchy, correction and validation | Frozen plan and a numerical counterexample to a misleading analysis |
| Data science | Turn scan/participant metadata into an auditable analysis table | Correct keys/units/missingness, train-only fitting, uncertainty at the right unit |
| Modeling | Compare a baseline with a more complex model under a defensible split | Untouched evaluation, leakage audit, metric/uncertainty interpretation and failure report |

Score each checkpoint 0–4 for (a) input/measurement, (b) transformation, (c) assumptions/QC, (d) validation, and (e) explanation. **0:** absent/wrong; **1:** repeats words without tracing effects; **2:** partly correct with prompts; **3:** correct independent explanation and repair; **4:** correct transfer to unfamiliar data and nuanced limits. Passing requires at least 3 in each category, with no unresolved major inference or data-integrity error.

## Final project

P04 requires the question and primary outcome, source/data permissions, metadata and acquisition, preprocessing provenance, QC/exclusions, primary analysis, validation/multiplicity, sensitivity plan, environment, rerun record and limits. The oral defense is 15 minutes, followed by an unexpected perturbation. See [P04](../notebooks/05_projects/04_research_defense.ipynb).

Do not call a linked practical completed unless its environment and data were used, exercises solved, and outputs inspected. Do not call an entire syllabus covered because one notebook mentions its topics. The [coverage audit](COVERAGE_AUDIT.md) gives the explicit remaining work.
