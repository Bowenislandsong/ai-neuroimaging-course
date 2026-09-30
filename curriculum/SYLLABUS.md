# Course syllabus

## Neuroimaging Research Methods with AI

A 26-week, paper-led course in structural, functional and diffusion MRI, experimental design, data science, and computational modeling. Students learn to connect a research question to a measurement, trace each analysis transformation, and defend a claim with inspected evidence.

This is an independent open course. It is not an official USC course and does not confer university credit. The public materials support self-paced study or a supervised seminar. A local instructor sets meeting times, submission dates and any institutional grading policies.

## Course format and workload

The course combines 83 notebook lessons, research-paper discussions, longer software practicals, and a supervised research project. Plan for 8–12 hours most weeks. Weeks 5–6 and the processing practicals in weeks 8–13 can require 10–15 hours. Insert consolidation weeks as needed. The [weekly schedule](STUDY_PLAN.md) specifies the full sequence and the evidence required before progressing.

Each class has lecture slides, full lesson notes, and a downloadable Jupyter notebook. Slides introduce the mechanism and discussion questions. The notebook contains the complete experiment, code and diagnostic outputs.

## Preparation

Begin with the reading seminars before programming. Students should be willing to interpret figures, reason about measurements, and work through introductory Python and quantitative concepts. Foundations and data-science lessons supply the computational bridge. Specialist practicals may require additional software, data access and supervision.

Follow the [environment setup](SETUP.md) and complete R00 before F01. The core environment uses Python and Jupyter. [AI-assisted study](AI_WORKFLOW.md) explains how to use Ollama with Goose or ChatGPT while preserving independent understanding.

## Learning outcomes

By the end of the course, students should be able to:

- Distinguish MRI and BOLD measurements from the biological processes they inform.
- Trace image geometry, registration, segmentation, preprocessing and quality-control decisions.
- Define an estimand, explain experimental timing, and justify a statistical contrast and inferential family.
- Build auditable participant tables and fit transformations inside the training boundary.
- Compare models with appropriate participant or site splits, baselines and uncertainty.
- Interpret a published figure in relation to its actual methods, data and evaluation conditions.
- Document a reproducible analysis and defend its limitations independently.

## Coursework

| Assignment | Submission | Suggested checkpoint |
|---|---|---|
| A1 · Figure brief | Six opening evidence ledgers, three paper comparisons and a first model audit | After week 2 |
| A2 · Mechanism experiment | Prediction, controlled transformation, deliberate failure, repair and revised paper interpretation | Week 13 |
| A3 · Figure or table reconstruction | An agreed scope, exact target, completed artifact and run evidence | Scope by week 22; completion in week 24 |
| A4 · Research review and defense | Research question, literature synthesis, analysis plan, validation boundaries and independent defense | Weeks 25–26 |

The [assignment specifications](coursework/PAPER_TO_EXPERIMENT.md) contain the full rubrics. Every computational class also requires a transformation card, prediction before execution, an intentionally wrong run with a justified repair, and a research-transfer explanation.

## Assessment

Assessment rewards traceable evidence and independent explanation. Strand checkpoints score measurement, transformation, assumptions and QC, validation, and explanation on a 0–4 scale. Passing requires at least 3 in each category with no unresolved major inference or data-integrity error. A1 uses its own opening-reading rubric. This open course specifies mastery criteria rather than percentage weights or a letter-grade formula. See [assessment and learning outcomes](ASSESSMENT.md).

## AI use and research integrity

AI may help explain a source or write a short operation. Students must predict what will happen, inspect the actual output, and explain decisions in their own words. Record consequential AI assistance and verify citations against the assigned source. An AI response is not evidence that a method works. The final defense requires independent explanation and adaptation to an unexpected change.

Synthetic demonstrations illustrate mechanisms. They do not reproduce the original experiments, datasets or large foundation models. A3 distinguishes explanatory reconstruction, reanalysis and computational reproduction and records unavailable data or compute.

## Readings and practicals

The [paper library](papers/README.md) contains 24 core papers and guides with assigned figures and questions. The [bibliography](papers/REFERENCES.md) supplies technique references. Required longer practicals come from established teaching sources and research-software workshops, listed in the [study plan](STUDY_PLAN.md#required-longer-practicals). Preserve their attribution and source environments.

## Access and support

Lecture slides support keyboard navigation and a printable handout view. Full text notes and downloadable notebooks provide alternative ways to study the material. For a supervised offering, arrange additional formats or workload adjustments with the instructor. Use the [repository issue tracker](https://github.com/Bowenislandsong/ai-neuroimaging-course/issues) to report broken materials or technical problems.

## Reuse

Original course materials use CC BY-SA 4.0; standalone original scripts use MIT. External papers, diagrams, datasets and software retain their own terms. See the [third-party notices](../THIRD_PARTY_NOTICES.md).
