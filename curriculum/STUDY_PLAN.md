# Study plan

The course begins with six research papers and four reading seminars. Students identify the scientific problems, interpret selected figures, and record questions that will guide their study of the methods. Programming and mathematics enter in week 3.

Plan for **26 weeks**, with most weeks requiring **8–12 hours**. The schedule includes paper discussions, Jupyter lessons, source practicals, and a supervised project. Specialist installations and real-data work may extend the calendar.

Allow **12–16 hours across the opening two weeks** for the first readings and discussion. Later papers generally take 45–75 minutes on first reading. A technical class generally takes 75–100 minutes, followed by a focused return to the paper. Reuse the original evidence record when a paper appears in several classes.

Weeks 5–6 contain six technical lessons each, about 7.5–10 hours before reading and practicals. The processing practicals add roughly 3–5 hours per week in weeks 8–13. Plan for **10–15 hours** in these periods or insert consolidation weeks. Evidence sheets and paper cards feed directly into A1–A4.

## The learning cycle

**Paper problem and figure → research question → fundamental concept → AI-assisted experiment → return to the paper → revised claim.** The [reading method](papers/READING_METHOD.md) and [coursework sequence](coursework/PAPER_TO_EXPERIMENT.md) specify the work submitted at each stage.

Notebook IDs: **R** reading seminar, **F** foundations, **PR** processing, **D** design, **DS** data science, **M** modeling, **P** projects. Paper IDs point to the [complete reading list](papers/README.md). The [class index](NOTEBOOK_INDEX.md) links all 83 notebooks: 79 computational lessons/projects and four human-assessed reading seminars.

| Week | Classes | Paper before or alongside the block | Evidence before progressing |
|---:|---|---|---|
| 1 | R00, R01 | PP01 fMRIPrep + PP04 BrainMorph | Two diagrams, evidence rows, questions about transforms |
| 2 | R02, R03 | PD02 Marek + PM03 BrainIAC; PD01 NARPS + PM05 Omni-fMRI | Six paper ledgers, three comparisons, first model evaluation audit |
| 3 | F01–F04 | PB01 measurement bridge; revisit the opening questions | Explain why a transformation contract and measurement model matter |
| 4 | DS01–DS04 | Revisit PP01/PD02 inputs and counting units | Correct axes, joins, geometry and EDA; paper-to-data diagram |
| 5 | DS05–DS08; D01–D02 | First pass PD06 design follow-up; revisit PD02 | Missingness/sampling questions and participant bootstrap |
| 6 | DS09–DS12; D03–D04 | First pass PD03 reliability; revisit PB01/PD06 | Distinguish scale, fitting, reliability, power and precision |
| 7 | DS13–DS16 | First pass PD04 circularity; preview PM02 representation comparison | Diagnose selection, train-only fitting and provenance |
| 8 | PR01–PR04 | First pass PP03 SynthSeg before PR04; return to PP04 with coordinate/warp questions | Geometry, resampling, warps and bias audit |
| 9 | PR05–PR08 | Return to PP03; PP05 fetal MRI as selected extension | Explain segmentation, boundaries, morphology and target population |
| 10 | PR09–PR12; D05 | First pass PP02 motion; revisit PP01/PB01 | Link timing, motion/distortion and HRF assumptions to the papers |
| 11 | PR13–PR15; D06 | Return to PP02 and PB01 | Filtering, nuisance/censoring and response-shape failure |
| 12 | PR16–PR19 | First pass PP06 tractography challenge | Trace diffusion measurements to pathways and false positives |
| 13 | PR20–PR21; P01 | Revisit PP01/PP04/PP06 | Transformation manifest and reproducible graph; A2 mechanism experiment |
| 14 | D07–D10 | First pass PD05 cluster failure **and correction** before D10; revisit PD04/PD06 and NARPS questions | Explain contrast, design rank, efficiency and temporal noise |
| 15 | D11–D14 | Return to PD05 and its correction; revisit PD02/PD04 | Hierarchy, exchangeability, multiplicity and independent selection |
| 16 | D15–D16; P02 | Return to PD01/PP01 with full workflow vocabulary | Single-run GLM audit and preprocessing scope |
| 17 | M01–M03 | First pass PM01 encoding/decoding and PM04 OpenMind benchmark before M03; revisit PM03 | Separate targets, representations and generalization questions |
| 18 | M04–M06 | Return to PM04; revisit PD02/PM03 | Nested/group/site split and fair-comparison audit |
| 19 | M07–M09 | Full first pass/return to PM02; revisit PP06 | Labeled RDMs, connectomes, overlapping searchlights and claim boundaries |
| 20 | M10–M12 | Return to PM01/PD03 | Timing, latent variables, state uncertainty and measurement reliability |
| 21 | M13–M15 | Revisit PM03/PP03 | Dynamics, CNN optimization, segmentation, and validation checks |
| 22 | M16–M18 | Return to PM03/PM04/PM05 Methods, ablations and limitations | Revised SOTA card, pretraining/attention/calibration explanation; settle A3 scope and access |
| 23 | P03 | Revisit PD02/PD06/PM03 | Unseen-site failure, baseline and participant-level uncertainty |
| 24 | Specialist track and A3 | Execute the agreed plan for an exact paper panel/table or source practical | Completed artifact, run evidence, and documented method scope |
| 25 | P04 and A4 | Relevant paper pair for the proposed research question | Frozen question, metadata, QC, analysis and validation boundaries |
| 26 | Rerun, defend, revise | First-pass claims versus final interpretations | Independent paper/figure defense and reproducible project evidence |

Paper cards sometimes include a short local rubric; the [A1–A4 rubrics](coursework/PAPER_TO_EXPERIMENT.md) assess the integrated submissions. First-pass grading rewards a traceable question and honest uncertainty, not prior mastery of methods. Paper IDs recur intentionally: the second reading should change the interpretation.

## Required longer practicals

The [source practicals](../third_party/README.md) provide longer technical assignments. Work on copies, preserve source versions, and connect each practical to its assigned paper. Submit the completed exercise and inspected outputs.

- **Processing:** complete all five guided blocks in the [processing coverage map](processing_coverage.md): geometry/fMRI alignment, structural morphometry, cortical surfaces, diffusion, and reproducible workflow/QC. These use Nipype/FSL/FreeSurfer/DIPY and add roughly 19–29 hours plus compute. Spread them across weeks 8–13 and extend the schedule when needed. One specialist track does not replace the five blocks.
- **Design:** complete the Poldrack efficiency and DartBrains resampling assignments. Explain which uncertainty or design question from the papers each calculation addresses. Historical source environments may differ from this core environment.
- **Data science:** complete the assigned Data 8 chapters and Neuromatch MSE/MLE/geometric-basis notebooks. Return to the paper's observations and fitting boundaries when interpreting the numbers.
- **Modeling:** complete BrainIAK RSA/ISC and Neuromatch HMM/CNN; choose the real-data continuation relevant to the project. Separate our small mechanism experiments from reproductions of the modern models.

## Specialist work in week 24

| Track | Required artifact | Paper connection |
|---|---|---|
| Structural MRI | Actual segmentation/surface/registration practical with overlays and QC | PP03/PP04, or PP05 if fetal imaging is relevant |
| Task fMRI | Documented preprocessing/model practical with events, confounds, alignment, residual and inference audit | PP01/PP02, PD01/PD05, PB01 |
| Diffusion | Gradient consistency, reconstruction/tractography and sensitivity to choices | PP06 and its false-positive/false-negative questions |
| Naturalistic/connectivity | Real timing/alignment, ISC/connectivity or representation analysis with independent evaluation | PM01/PM02 and PD03 |
| Imaging machine learning | Real input/label contract, participant/site split, baseline, fit boundaries and model card | PM03/PM04/PM05 |

Use [A3](coursework/PAPER_TO_EXPERIMENT.md#a3--figure-or-table-reconstruction-proposal) to select an honest scope: explanatory reconstruction, reanalysis, or computational reproduction. The paper guides do not claim that large models or original experiments have already been reproduced. Additional data access, supervision and compute may be necessary. P04's final defense connects the paper evidence to the specific analysis she can now justify.
