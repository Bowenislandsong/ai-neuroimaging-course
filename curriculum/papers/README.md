# Papers first: the research problem before the machinery

Start here, then open [R00: how to read](../../notebooks/00_paper_orientation/00_how_to_read.ipynb). The first two weeks introduce **three essential papers paired with three recent frontier papers**. She does not need to understand their equations yet. She should see why processing, research design, statistics and modeling matter, and collect questions she wants the later classes to answer.

This library contains **18 papers** with targeted reading paths, evidence questions, original assignments and instructor checks. Six are opening readings; the others introduce their relevant technical blocks. PP05 is a specialist fetal-imaging extension. Follow the [26-week sequence](../STUDY_PLAN.md), rather than trying to master all 18 before beginning. The 79 computational notebooks each contain a paper question and a return-to-paper task; four additional notebooks conduct the opening reading seminars.

## The six opening readings

| Seminar | Essential reading | Recent frontier reading | Question to carry into the fundamentals |
|---|---|---|---|
| [R01: processing](../../notebooks/00_paper_orientation/01_why_processing.ipynb) | [PP01 · fMRIPrep (2019)](processing.md#pp01) | [PP04 · BrainMorph (2025)](processing.md#pp04) | What transformations stand between a scan and an interpretable result? A registration component and a complete preprocessing workflow have different scopes. |
| [R02: generalization](../../notebooks/00_paper_orientation/02_why_generalization.ipynb) | [PD02 · Marek: reproducible BWAS (2022)](design.md#pd02) | [PM03 · BrainIAC (2026)](modeling.md#pm03) | When can evidence from these people support a claim about new people? Association estimation and predictive transfer ask different questions. |
| [R03: evidence and choices](../../notebooks/00_paper_orientation/03_why_evidence_audits.ipynb) | [PD01 · NARPS (2020)](design.md#pd01) | [PM05 · Omni-fMRI (2026)](modeling.md#pm05) | Which analysis choices and benchmark comparisons support a claim, and which narrow it? |

These are conceptual pairings, not head-to-head benchmarks. Do not compare the papers' headline numbers as if their tasks, data and metrics were interchangeable.

For each paper: read its abstract and introduction, inspect the assigned figure/table and caption, then read the relevant result and limitations. Write the scientific question in your own words before asking AI for help. The guides specify what to postpone. Use the [three-pass reading method](READING_METHOD.md): **motivation now → mechanism during the notebooks → judgment after the experiment**.

## All readings and the coursework they motivate

The title links lead to a primary publication record; each guide links the assigned full text and exact sections. Publication year and the version of the assigned reading copy can differ.

| ID | Paper | Role and first encounter | Original coursework |
|---|---|---|---|
| [PP01 guide](processing.md#pp01) | [fMRIPrep: a robust preprocessing pipeline for functional MRI (2019)](https://doi.org/10.1038/s41592-018-0235-4) | Essential · opening | Draw and audit a preprocessing decision graph |
| [PP02 guide](processing.md#pp02) | [Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion (2012)](https://doi.org/10.1016/j.neuroimage.2011.10.018) | Essential · before motion/QC | Explain a motion counterexample and compare censoring choices |
| [PP03 guide](processing.md#pp03) | [SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining (2023)](https://doi.org/10.1016/j.media.2023.102789) | Essential modern method · before structural processing | Trace simulated-image variation to segmentation assumptions |
| [PP04 guide](processing.md#pp04) | [BrainMorph: A Foundational Keypoint Model for Robust and Flexible Brain MRI Registration (2025)](https://doi.org/10.59275/j.melba.2025-59g7) | Frontier · opening | Trace keypoints, transform estimation and resampling separately |
| [PP05 guide](processing.md#pp05) | [Towards contrast- and pathology-agnostic clinical fetal brain MRI segmentation using SynthSeg (2026)](https://doi.org/10.1016/j.neuroimage.2026.121729) | 2026 specialist extension · fetal imaging | Audit transfer into a different developmental population |
| [PP06 guide](processing.md#pp06) | [The challenge of mapping the human connectome based on diffusion tractography (2017)](https://doi.org/10.1038/s41467-017-01285-x) | Essential · before diffusion | Explain ambiguous pathways with an original endpoint/graph exercise |
| [PD01 guide](design.md#pd01) | [Variability in the analysis of a single neuroimaging dataset by many teams (2020)](https://www.nature.com/articles/s41586-020-2314-9) | Essential · opening | Hold an analysis-decision hearing and expose alternatives |
| [PD02 guide](design.md#pd02) | [Reproducible brain-wide association studies require thousands of individuals (2022)](https://www.nature.com/articles/s41586-022-04492-9) | Essential · opening | Separate task effects, between-person associations and prediction |
| [PD03 guide](design.md#pd03) | [What Is the Test-Retest Reliability of Common Task-Functional MRI Measures? New Empirical Evidence and a Meta-Analysis (2020)](https://doi.org/10.1177/0956797620916786) | Essential · before reliability | Distinguish average activation from stable individual differences |
| [PD04 guide](design.md#pd04) | [Circular analysis in systems neuroscience: the dangers of double dipping (2009)](https://doi.org/10.1038/nn.2303) | Essential · before feature selection | Expose double dipping with independent evaluation |
| [PD05 guide](design.md#pd05) | [Cluster failure: Why fMRI inferences for spatial extent have inflated false-positive rates (2016)](https://www.pnas.org/doi/10.1073/pnas.1602413113) | Essential · before temporal noise/inference | Name the inferential family and inspect null assumptions; read correction |
| [PD06 guide](design.md#pd06) | [Study design features increase replicability in brain-wide association studies (2024)](https://www.nature.com/articles/s41586-024-08260-9) | 2024 methodological follow-up · before sampling | Compare designs under a fixed scan budget and target population |
| [PM01 guide](modeling.md#pm01) | [Encoding and decoding in fMRI (2011)](https://doi.org/10.1016/j.neuroimage.2010.07.073) | Essential review · before modeling | Draw encoding/decoding diagrams and change a toy prediction target |
| [PM02 guide](modeling.md#pm02) | [Representational similarity analysis – connecting the branches of systems neuroscience (2008)](https://doi.org/10.3389/neuro.06.004.2008) | Essential · preview before PCA; return before RSA | Build qualitative representational dissimilarity matrices |
| [PM03 guide](modeling.md#pm03) | [A generalizable foundation model for analysis of human brain MRI (2026)](https://doi.org/10.1038/s41593-026-02202-6) | Frontier · opening | Write a transfer contract and inspect a task-specific result panel |
| [PM04 guide](modeling.md#pm04) | [An OpenMind for 3D Medical Vision Self-supervised Learning (2025)](https://openaccess.thecvf.com/content/ICCV2025/html/Wald_An_OpenMind_for_3D_Medical_Vision_Self-supervised_Learning_ICCV_2025_paper.html) | Frontier benchmark · before model comparison | Plan a fair comparison with matched adaptation conditions |
| [PM05 guide](modeling.md#pm05) | [Omni-fMRI: A Universal Atlas-Free fMRI Foundation Model (2026)](https://arxiv.org/abs/2601.23090v1) | Frontier · opening | Audit tokenization and find a within-paper performance exception |
| [PB01 guide](measurement.md#pb01) | [Neurophysiological investigation of the basis of the fMRI signal (2001)](https://www.nature.com/articles/35084005) | Essential measurement bridge · before F02 | Separate neural activity, physiological coupling and measured BOLD |

## Actual submissions

Use these reusable templates inside the notebooks or in your own study folder. Reuse a paper-card artifact in the portfolio; do not write the same assignment twice.

1. **[A1: figure brief](../coursework/PAPER_TO_EXPERIMENT.md#a1--first-pass-figure-brief).** Six opening evidence ledgers, three pair comparisons and a first frontier-paper audit. Explain what is being counted, what the comparison is, and what the figure cannot establish. Unknown methods are questions to investigate.
2. **[A2: mechanism experiment](../coursework/PAPER_TO_EXPERIMENT.md#a2--mechanism-experiment).** Predict one transformation, ask AI for a short implementation, deliberately change one assumption, inspect the result and revise a paper interpretation.
3. **[A3: reconstruction proposal](../coursework/PAPER_TO_EXPERIMENT.md#a3--figure-or-table-reconstruction-proposal).** Choose an exact paper panel or table, define data/code/compute requirements and specify whether the work is an explanatory reconstruction, reanalysis or computational reproduction. Complete a feasible agreed scope and record what remains untested.
4. **[A4: research review and defense](../coursework/PAPER_TO_EXPERIMENT.md#a4--reviewer-response-and-research-proposal).** Explain how the literature changes the learner's own research question, choices, validation and claim boundaries; defend an unexpected change without relying on AI's answer.

Each uses an [evidence ledger](../coursework/EVIDENCE_LEDGER.md). The [SOTA audit](../coursework/SOTA_AUDIT.md) is completed once at the opening level, then revised after the modeling block. Read the instructor checks only after attempting the work. Rubrics reward evidence and explanation, not vocabulary or flawless prose.

## How “SOTA” is used here

BrainMorph, BrainIAC, OpenMind and Omni-fMRI are representative 2025–2026 frontier readings. The fetal-imaging extension adds a 2026 application. This is a dated editorial selection, **not a verified ranking of every model available**. A performance claim must name the task, data, split, baseline, adaptation protocol, metric and uncertainty. The Omni-fMRI coursework deliberately examines a comparison where its model is not the best on the reported metrics.

BrainMorph's assigned manuscript is arXiv v3, associated with its 2025 MELBA publication. OpenMind's publication record is ICCV 2025; its assigned reading copy is arXiv v2. Omni-fMRI is listed in the official ICML 2026 program; the worksheet assigns arXiv v1 and does not assume every conference-version detail is identical. BrainIAC is a 2026 Nature Neuroscience article. PD06 is a 2024 methodological follow-up, not a latest-model claim. The individual guides and registry retain dates, versions and verification links.

## Source access and reuse

The [machine-readable registry](paper_registry.json) records all 18 citations, publication status, assigned sections, primary links, notebook connections and available code links. Its component source records preserve access limitations and the passages inspected. Verification was performed on **25 September 2026 UTC**. Some sources were accessible through author manuscripts or indexed full-text passages when a publisher page blocked access; figure-caption review does not imply that every figure image or supplement was inspected. No complete literature search or empirical leaderboard replication is claimed.

The papers are linked, and the coursework is original. PDFs, publisher figures, participant data and model weights are not copied into this repository. Open reading access does not by itself grant redistribution rights. Code and weights have separate terms: for example, BrainIAC's official repository uses a research-only license. Follow each source's terms before any optional model work. Source reuse notices for the separately preserved teaching notebooks remain in [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

To maintain this course, edit the strand source JSON files and [lesson_readings.json](lesson_readings.json), then run `python scripts/build_reading_indexes.py` from the repository root. Recheck primary publication/version records when replacing a frontier paper; do not silently substitute an evolving manuscript while retaining old figure questions.
