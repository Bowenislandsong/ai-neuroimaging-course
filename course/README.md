> **Introductory supplement.** The expanded 79-notebook course is now in the [repository start page](../README.md) and [complete class index](../curriculum/NOTEBOOK_INDEX.md). This earlier pack is retained for reference.

# AI-assisted neuroimaging: understand every transformation

A beginner course for a learner who uses AI to write short analysis snippets and wants to understand, inspect, and defend what those snippets do.

**Start here:** [Setup and the AI teaching contract](SETUP.md), then [two foundation classes](lessons/00_bridge.md). The [complete reading edition](COURSEBOOK.md) collects the teaching text in one file. The four notebooks contain the executable demonstrations; their HTML companions show the verified outputs without installing Python.

## What this course is

24 core classes, two foundation classes, and two capstone sessions. Allow **14 weeks at two 60–75 minute classes per week**, plus 30–60 minutes of practice weekly. Slow down when the explain-back questions are difficult. The target is informed use of small snippets, not independent software engineering or the full training of a master's degree.

USC's [NIIN curriculum](https://niin.usc.edu/about#curriculum) supplies four broad subject areas. Detailed public syllabi were not located during this research session. The sequence, lessons, prompts, notebooks, assessments, and capstone here are original; **this is not USC course material or an official NIIN syllabus**. [Research and materials record](SOURCES.md).

## What she should be able to do

For a transformation, explain the input, output, parameter units, what changes, what information is lost, one likely failure, and the evidence needed to accept the result. Ask an AI to implement that step, inspect it, and explain its scientific limits. She need not memorize syntax; she must be able to reject plausible-looking code and conclusions.

| Block | Six actual classes | Lesson text | Runnable lab |
| --- | --- | --- | --- |
| Processing • 540-inspired | Coordinates/QC; registration and resampling; smoothing; temporal filtering; nuisance regression; pipeline audit | [540](lessons/540.md) | [Notebook](labs/540_processing.ipynb) · [Outputs](labs/540_processing.html) |
| Research design • 520-inspired | Question and unit; confounding/design; timing and HRF; GLM/contrasts; uncertainty and multiplicity; preregistration/power | [520](lessons/520.md) | [Notebook](labs/520_design.ipynb) · [Outputs](labs/520_design.html) |
| Data science • 580-inspired | Arrays/axes; participant joins; z standardization; regression/residuals; QC/uncertainty; provenance/leakage | [580](lessons/580.md) | [Notebook](labs/580_data_science.ipynb) · [Outputs](labs/580_data_science.html) |
| Modeling • 550-inspired | Representations; baselines; honest splits; metrics; CNNs/segmentation; foundation-model audit | [550](lessons/550.md) | [Notebook](labs/550_modeling.ipynb) · [Outputs](labs/550_modeling.html) |

## Suggested order: interleave understanding with practice

The numbers label subject areas, not a requirement to finish one block before touching another. Introduce a research question early, before choosing processing settings.

| Week | First class | Second class | Evidence she saves |
| --- | --- | --- | --- |
| 1 | Bridge A: MRI and measurement | Bridge B: AI tutor and first plot | A prediction and a checked output |
| 2 | 580.1: shapes/axes | 540.1: images/coordinates/QC | Image identity card |
| 3 | 520.1: question and unit | 580.2: participant tables | Research question and data dictionary |
| 4 | 540.2: registration/resampling | 540.3: smoothing | Before/after transformation cards |
| 5 | 580.3: standardization | 540.4: temporal filtering | Correct axis, reference, and frequency units |
| 6 | 580.4: regression mechanics | 540.5: nuisance regression | Residual explanation |
| 7 | 520.2: confounding/design | 520.3: timing and HRF | Design diagram and matrix |
| 8 | 520.4: GLM and contrasts | 580.5: QC/uncertainty | Contrast definition and sample-flow record |
| 9 | 520.5: multiple comparisons | 520.6: analysis plan/power | Locked analysis plan |
| 10 | 580.6: provenance/leakage | 540.6: pipeline audit | Rerunnable notebook and QC decision |
| 11 | 550.1: representations | 550.2: baseline models | Feature dictionary and baseline score |
| 12 | 550.3: validation splits | 550.4: metrics | Group-disjoint split and error analysis |
| 13 | 550.5: CNN/segmentation | 550.6: foundation models | Model/data card and applicability decision |
| 14 | Capstone A: plan and inspect | Capstone B: run and defend | [Capstone portfolio](lessons/90_capstone.md) |

## The rule for every class

**Predict → ask AI for one small operation → inspect code → run → compare → explain.** No points for the number of lines she writes. Keep the answer key closed until she explains the result. Use short prompts from the lesson, and paste the [tutor contract](SETUP.md#the-tutor-contract) into each fresh AI conversation.

Every class has an explanation, a concrete experiment, an intentional mistake, expected checks, and exit questions. Code cells are short; some experiments need several cells. A successful run is one piece of evidence, not automatic validation.

## Materials included

- [Setup](SETUP.md), [transformation reference](TRANSFORMATIONS.md), and [glossary](GLOSSARY.md).
- Original lesson text and four offline synthetic notebooks; all needed toy data are generated in the cells.
- [Transformation card](templates/transformation_card.md), [analysis record](templates/analysis_record.md), [project plan](templates/project_plan.md), and [assessment rubric](ASSESSMENT.md).
- Primary-source reading links and an optional [real-data bridge](REAL_DATA.md). External books, slides, scans, and model weights are linked rather than bundled.
- [Verification report](verification/REPORT.md) documents what was executed. Local AI setup is documented, not installed or benchmarked on her hardware.

The runnable core uses small synthetic arrays so she can see the correct answer. It does not perform research-grade MRI preprocessing. The real-data stage uses an existing documented teaching pipeline; an instructor reviews the acquisition, processing, and inference decisions.
