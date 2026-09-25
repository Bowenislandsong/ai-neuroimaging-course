# Assignment sequence: from motivating paper to an analysis you can defend

Paper cards may have a short 10-point local checkpoint; the 20-point rubrics below assess the complete course submission.

The paper leads the lesson. A notebook is then the smallest useful experiment for understanding a part of that paper. It is not automatically a reproduction of the paper's result.

Reuse the evidence sheets, diagrams and experiments produced in the paper cards and seminars; these integrated assessments do not require a second copy of the same work. One experiment may support several paper returns if each connection is explained. Multiple notebook links on a card are a learning path, not a demand for a new report after every linked notebook.

**Common 0–4 scale:** 0 = absent; 1 = major unresolved misconception; 2 = partly correct but missing evidence or explanation; 3 = correct, traceable and independently explained for the assigned stage; 4 = meets 3 and adds a well-justified check, alternative or limitation. For A1, a precisely located unknown with a sensible next question can meet 3; prior command of technical methods is not required. For A2 and A3, passing requires at least 3 in each area. A4 uses the existing P04 passing rule.

<a id="a1--first-pass-figure-brief"></a>
## A1 · First-pass figure brief

**Due:** opening R01–R03 seminars. **Work:** six short evidence ledgers, one per opening paper, plus three paired comparisons. For each paper give a 150-word motivation, a figure/section location, what is plotted or counted, three questions, and one limited result claim. Distinguish the plotted unit from the sampling unit when the source makes this clear; otherwise record the uncertainty. For each pair give a one-page data → operation → evidence diagram and explain what fundamentals you want to learn next. Do not solve equations yet. The same brief format can be used when later papers enter the study plan.

**Marking:** question/motivation 4; figure reading 4; source evidence 4; claim boundary 4; independent explanation 4. Passing is at least 3 in each area. Technical vocabulary and complete methods understanding are not required on this first pass.

<a id="a2--mechanism-experiment"></a>
## A2 · Mechanism experiment

**Due:** at the relevant strand checkpoint, after the notebook needed for the chosen operation. Select one operation the paper depends on. Predict a consequence, run the named local exercise, change one meaningful parameter, inspect a failure, and explain the result. Submit the exact notebook/cell, original and changed parameter, labeled output, invariant, lost information and revised paper interpretation. State whether the failure was deliberately introduced or observed in the baseline; do not describe an invented failure as a real run.

Choose an appropriate scope:

| Paper-led question | Local experiment | Honest deliverable label |
|---|---|---|
| How can alignment change what a scan means? | PR02/PR03 and P01 geometry/resampling | Synthetic registration mechanism plus real-template transformation; not BrainMorph reproduction |
| Why can reasonable analyses reach different decisions? | D13/D16 multiplicity/multiverse and PR14 nuisance choices | Controlled sensitivity demonstration; not rerunning NARPS teams |
| Why does a result fail on new people or sites? | DS07/DS08, M04 and P03 | Sampling/validation mechanism; not a new BWAS or BrainIAC benchmark |
| What do pretraining and adaptation actually change? | M14/M16/M17 | Small CNN/autoencoder/attention calculation; not training a full MRI foundation model |
| Why is a brain signal not a direct readout of firing? | F02, D05/D06 and PR13 | Measurement/convolution/filter mechanism; not an electrophysiology experiment |

**Marking:** valid mapping 4; prediction 4; controlled change and diagnostic 4; correct interpretation 4; honest provenance/scope 4. The numerical output need not match a paper figure because the data and method scope may differ. Claiming a reproduction when only a toy calculation ran is an error to fix.

<a id="a3--figure-or-table-reconstruction-proposal"></a>
## A3 · Figure or table reconstruction proposal

**Due:** draft after the relevant strand checkpoint and settle the scope by the end of week 22; complete the agreed work in the specialist/project period. Choose one exact published panel/table row. Before running anything, state which of the following you will do:

1. **Explanatory reconstruction:** a newly drawn schematic or synthetic example illustrating the mechanism, clearly labeled as such.
2. **Reanalysis:** a new analysis of lawfully accessible public data, possibly using a different implementation.
3. **Computational reproduction:** original released data/code/configuration, with deviations and unavailable components recorded.

Submit a one-page plan: target/version; permitted inputs; repository/commit and dependencies when code is used; transformation chain; expected metric and a justified tolerance when numerical comparison is appropriate; failure/QC criteria; compute estimate; provenance; missing access; and a fallback that preserves the learning goal. For an explanatory schematic, replace numerical agreement with explicit conceptual properties it must show. Do not promise exact numerical agreement without knowing the original randomness and environment. Do not upload publisher figures or restricted inputs into the public repository merely to complete the assignment.

The supervisor chooses a feasible plan with the learner. Complete it in the specialist/project period, preserve the run, compare with the target and explain discrepancies. If the required data are unavailable, complete the explanatory reconstruction and access audit, explicitly labeling the reproduction uncompleted. Do not silently substitute one for the other.

**Marking, 20 points:** precise target and honest scope (4); input/source access and provenance (4); feasible transformation plan (4); appropriate comparison and failure criteria (4); completed evidence and interpretation for the agreed scope (4). Give formative feedback on the first four areas before execution; award the final score after the artifact is delivered. An explicitly agreed explanatory fallback can pass, while the record must still say that a full reproduction was not completed. A proposal alone is not evidence of execution.

<a id="a4--reviewer-response-and-research-proposal"></a>
## A4 · Reviewer response and research proposal

**Due:** final P04 defense. Write a 600–900 word note with the question, strongest source evidence, important uncertainty, the operation you now understand, a proposed new experiment, a simple baseline and independent validation. Attach first-pass and revised claims side by side. Explain how the papers changed the study design rather than merely listing them in a bibliography.

The instructor selects one figure from the submitted paper set and one pipeline choice without advance notice. The learner explains each without the AI, then uses the AI to propose a check and critiques that proposal. Retain the existing P04 technical rubric; add paper evidence and uncertainty to the same five scoring areas, rather than awarding an additional score for identical work:

| P04 area, 0–4 each | Paper-based evidence to include |
|---|---|
| Measurement/metadata | How the paper's measurements and population compare with the proposed data |
| Transformations/QC | Why an operation is needed, what it changes, and how failure will be detected |
| Design/inference | Which claim the design can test and which plausible alternative remains |
| Validation/reproducibility | Source/version, development boundary, independent evaluation and actual run record |
| Independent explanation | A defensible interpretation of the selected figure and a checked AI suggestion |

Passing requires at least 3 in every area and no unresolved data or inference error in the submitted analysis. An explicitly stated limit or a future research question is not itself an error. All source facts must be locatable in the cited version.
