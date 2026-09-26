# Research papers and reading guides

Begin with [R00: Reading a research paper](../../notebooks/00_paper_orientation/00_how_to_read.ipynb). The first two weeks pair three established studies with three recent methods. Students identify the questions that motivate processing, research design, statistics, and modeling before working through the technical lessons.

The library contains **24 papers**, each with assigned sections, evidence questions, coursework, and instructor notes. Six appear in the opening seminars. The remaining readings introduce their corresponding technical blocks in the [study plan](../STUDY_PLAN.md). PP05 supports the optional fetal-imaging extension.

## The six opening readings

| Seminar | Essential reading | Recent frontier reading | Question to carry into the fundamentals |
|---|---|---|---|
| [R01: processing](../../notebooks/00_paper_orientation/01_why_processing.ipynb) | [PP01 · fMRIPrep (2019)](processing.md#pp01) | [PP04 · BrainMorph (2025)](processing.md#pp04) | What transformations stand between a scan and an interpretable result? A registration component and a complete preprocessing workflow have different scopes. |
| [R02: generalization](../../notebooks/00_paper_orientation/02_why_generalization.ipynb) | [PD02 · Marek: reproducible BWAS (2022)](design.md#pd02) | [PM03 · BrainIAC (2026)](modeling.md#pm03) | When can evidence from these people support a claim about new people? Association estimation and predictive transfer ask different questions. |
| [R03: evidence and choices](../../notebooks/00_paper_orientation/03_why_evidence_audits.ipynb) | [PD01 · NARPS (2020)](design.md#pd01) | [PM05 · Omni-fMRI (2026)](modeling.md#pm05) | Which analysis choices and benchmark comparisons support a claim, and which narrow it? |

Each pair approaches a shared research problem from a different angle. Compare the questions and evidence while keeping the papers' distinct tasks, datasets, and metrics in view.

For each paper, read the abstract and introduction, inspect the assigned figure or table, and study the relevant result and discussion. Write the scientific question in your own words before consulting AI. The [reading method](READING_METHOD.md) has three passes: **motivation → mechanism → evaluation**.

## Reading list and coursework

Paper titles link to publication records. Each guide identifies the reading copy, relevant sections, and its place in the course.

| ID | Paper | Role and first encounter | Original coursework |
|---|---|---|---|
| [PP01 guide](processing.md#pp01) | [fMRIPrep: a robust preprocessing pipeline for functional MRI (2019)](https://doi.org/10.1038/s41592-018-0235-4) | Essential · opening | Draw and audit a preprocessing decision graph |
| [PP02 guide](processing.md#pp02) | [Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion (2012)](https://doi.org/10.1016/j.neuroimage.2011.10.018) | Essential · before motion/QC | Explain a motion counterexample and compare censoring choices |
| [PP03 guide](processing.md#pp03) | [SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining (2023)](https://doi.org/10.1016/j.media.2023.102789) | Essential modern method · before structural processing | Trace simulated-image variation to segmentation assumptions |
| [PP04 guide](processing.md#pp04) | [BrainMorph: A Foundational Keypoint Model for Robust and Flexible Brain MRI Registration (2025)](https://doi.org/10.59275/j.melba.2025-59g7) | Frontier · opening | Trace keypoints, transform estimation and resampling separately |
| [PP05 guide](processing.md#pp05) | [Towards contrast- and pathology-agnostic clinical fetal brain MRI segmentation using SynthSeg (2026)](https://doi.org/10.1016/j.neuroimage.2026.121729) | 2026 specialist extension · fetal imaging | Audit transfer into a different developmental population |
| [PP06 guide](processing.md#pp06) | [The challenge of mapping the human connectome based on diffusion tractography (2017)](https://doi.org/10.1038/s41467-017-01285-x) | Essential · before diffusion | Explain ambiguous pathways with an original endpoint/graph exercise |
| [PP07 guide](processing.md#pp07) | [FastSurfer - A fast and accurate deep learning based neuroimaging pipeline (2020)](https://doi.org/10.1016/j.neuroimage.2020.117012) | Essential · cortical surfaces and morphometry | Contrast volumetric Dice with mesh Euler topology and cortical thickness |
| [PP08 guide](processing.md#pp08) | [QSIPrep: an integrative platform for preprocessing and reconstructing diffusion MRI data (2021)](https://doi.org/10.1038/s41592-021-01185-5) | Essential · diffusion workflows and q-space | Audit B-table rotation, single-interpolation resampling, and ODF reconstruction |
| [PD01 guide](design.md#pd01) | [Variability in the analysis of a single neuroimaging dataset by many teams (2020)](https://www.nature.com/articles/s41586-020-2314-9) | Essential · opening | Hold an analysis-decision hearing and expose alternatives |
| [PD02 guide](design.md#pd02) | [Reproducible brain-wide association studies require thousands of individuals (2022)](https://www.nature.com/articles/s41586-022-04492-9) | Essential · opening | Separate task effects, between-person associations and prediction |
| [PD03 guide](design.md#pd03) | [What Is the Test-Retest Reliability of Common Task-Functional MRI Measures? New Empirical Evidence and a Meta-Analysis (2020)](https://doi.org/10.1177/0956797620916786) | Essential · before reliability | Distinguish average activation from stable individual differences |
| [PD04 guide](design.md#pd04) | [Circular analysis in systems neuroscience: the dangers of double dipping (2009)](https://doi.org/10.1038/nn.2303) | Essential · before feature selection | Expose double dipping with independent evaluation |
| [PD05 guide](design.md#pd05) | [Cluster failure: Why fMRI inferences for spatial extent have inflated false-positive rates (2016)](https://www.pnas.org/doi/10.1073/pnas.1602413113) | Essential · before temporal noise/inference | Name the inferential family and inspect null assumptions; read correction |
| [PD06 guide](design.md#pd06) | [Study design features increase replicability in brain-wide association studies (2024)](https://www.nature.com/articles/s41586-024-08260-9) | 2024 methodological follow-up · before sampling | Compare designs under a fixed scan budget and target population |
| [PD07 guide](design.md#pd07) | [Harmonization of cortical thickness measurements across scanners and sites (2018)](https://doi.org/10.1016/j.neuroimage.2017.11.024) | Essential · multi-site ComBat harmonization | Separate additive/multiplicative site batch effects from biological covariates |
| [PM01 guide](modeling.md#pm01) | [Encoding and decoding in fMRI (2011)](https://doi.org/10.1016/j.neuroimage.2010.07.073) | Essential review · before modeling | Draw encoding/decoding diagrams and change a sample prediction target |
| [PM02 guide](modeling.md#pm02) | [Representational similarity analysis – connecting the branches of systems neuroscience (2008)](https://doi.org/10.3389/neuro.06.004.2008) | Essential · preview before PCA; return before RSA | Build qualitative representational dissimilarity matrices |
| [PM03 guide](modeling.md#pm03) | [A generalizable foundation model for analysis of human brain MRI (2026)](https://doi.org/10.1038/s41593-026-02202-6) | Frontier · opening | Write a transfer contract and inspect a task-specific result panel |
| [PM04 guide](modeling.md#pm04) | [An OpenMind for 3D Medical Vision Self-supervised Learning (2025)](https://openaccess.thecvf.com/content/ICCV2025/html/Wald_An_OpenMind_for_3D_Medical_Vision_Self-supervised_Learning_ICCV_2025_paper.html) | Frontier benchmark · before model comparison | Plan a fair comparison with matched adaptation conditions |
| [PM05 guide](modeling.md#pm05) | [Omni-fMRI: A Universal Atlas-Free fMRI Foundation Model (2026)](https://arxiv.org/abs/2601.23090v1) | Frontier · opening | Audit tokenization and find a within-paper performance exception |
| [PM06 guide](modeling.md#pm06) | [MindEye2: Shared-Subject Models Enable fMRI-To-Image With 1 Hour of Data (2024)](https://arxiv.org/abs/2403.11207) | Frontier · shared-subject decoding and reconstruction | Audit linear subject-specific ridge alignment vs generative diffusion priors |
| [PM07 guide](modeling.md#pm07) | [Using connectome-based predictive modeling to predict individual behavior from brain connectivity (2017)](https://doi.org/10.1038/nprot.2016.178) | Essential · connectome predictive modeling | Screen graph edges strictly inside cross-validation folds |
| [PM08 guide](modeling.md#pm08) | [Brain network dynamics are hierarchically organized in time (2017)](https://doi.org/10.1073/pnas.1705120114) | Essential · latent dynamical brain states | Compare static connectivity with Hidden Markov Model state transitions |
| [PB01 guide](measurement.md#pb01) | [Neurophysiological investigation of the basis of the fMRI signal (2001)](https://www.nature.com/articles/35084005) | Essential measurement bridge · before F02 | Separate neural activity, physiological coupling and measured BOLD |

## Key references for each lesson

The 24 papers above set the research questions. Each computational lesson also opens with **Why this technique matters** and two to four **key references** for the technique it teaches: at least one foundational method or standard-tool paper and at least one published in 2019 or later (a current method, benchmark, or critical evaluation). The [course bibliography](REFERENCES.md) collects them by lesson, with verification status and OpenAlex citation counts. Citation counts indicate how widely a work is used, not whether it is correct; older papers accumulate more citations.

## Assignments

Use these assignments throughout the course. Evidence sheets and diagrams prepared for a paper guide can be included in the final portfolio.

1. **[A1: figure brief](../coursework/PAPER_TO_EXPERIMENT.md#a1--first-pass-figure-brief).** Six opening evidence ledgers, three pair comparisons and a first frontier-paper audit. Explain what is being counted, what the comparison is, and what the figure cannot establish. Unknown methods are questions to investigate.
2. **[A2: mechanism experiment](../coursework/PAPER_TO_EXPERIMENT.md#a2--mechanism-experiment).** Predict one transformation, ask AI for a short implementation, deliberately change one assumption, inspect the result and revise a paper interpretation.
3. **[A3: reconstruction proposal](../coursework/PAPER_TO_EXPERIMENT.md#a3--figure-or-table-reconstruction-proposal).** Choose an exact paper panel or table, define data/code/compute requirements and specify whether the work is an explanatory reconstruction, reanalysis or computational reproduction. Complete a feasible agreed scope and record what remains untested.
4. **[A4: research review and defense](../coursework/PAPER_TO_EXPERIMENT.md#a4--reviewer-response-and-research-proposal).** Explain how the literature changes the learner's own research question, choices, validation and claim boundaries; defend an unexpected change without relying on AI's answer.

Each uses an [evidence ledger](../coursework/EVIDENCE_LEDGER.md). The [SOTA audit](../coursework/SOTA_AUDIT.md) is completed once at the opening level, then revised after the modeling block. Read the instructor checks only after attempting the work. Rubrics reward evidence and explanation, not vocabulary or flawless prose.

## Evaluating recent methods

BrainMorph, BrainIAC, OpenMind, and Omni-fMRI provide 2025–2026 examples of active research; the fetal-imaging paper adds a clinical application. Students evaluate each reported result against its task, data, split, baseline, adaptation protocol, metric, and uncertainty. The Omni-fMRI assignment includes a comparison where another method performs better on the reported metrics.

The guides identify the version used for each assignment. BrainMorph uses arXiv v3 alongside its 2025 MELBA publication; OpenMind uses arXiv v2 alongside ICCV 2025. Omni-fMRI uses arXiv v1 and is listed in the ICML 2026 program. BrainIAC appeared in *Nature Neuroscience* in 2026. PD06 is a 2024 study-design follow-up.

## Source records and reuse

The [source registry](paper_registry.json) records citations, publication status, assigned versions and sections, notebook connections, and code links. Two notebook lists serve different purposes: `motivation_notebook_ids` is generated from [lesson_readings.json](lesson_readings.json) and names the lessons whose opening research question assigns the paper; `notebook_ids` is curated in the strand source files and lists later lessons suited to follow-up work on the paper; most guides name them as forward links. The records also identify author manuscripts and access limitations where relevant. Source information was checked on **25 September 2026 UTC**; the key references and all 24 library records were re-checked against Crossref, OpenAlex and arXiv on **26 September 2026 UTC** ([reference_verification.json](reference_verification.json)).

The coursework is original and links to papers at their publisher or author sites. Consult the source terms before using paper figures, code, data, or model weights in a project; BrainIAC's official repository, for example, uses a research-only license. Attribution for preserved teaching materials appears in the [third-party notices](../../THIRD_PARTY_NOTICES.md).

Course maintainers edit the strand source files, [lesson_readings.json](lesson_readings.json) and [key_references.json](key_references.json). After changing a key reference, run `uv run --frozen python scripts/verify_references.py` (network required; every entry must report `MATCH`). Then run `uv run --frozen python scripts/build_reading_indexes.py` from the repository root to regenerate the notebook question blocks, key-reference blocks, indexes and bibliography. `scripts/check_repository.py` fails if a block is stale or a reference is unverified. Update figure questions whenever the assigned manuscript version changes.
