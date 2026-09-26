# Neuroimaging Research Methods with AI

A 26-week course in neuroimaging analysis, experimental design, data science, and computational modeling. Students read research papers to understand the scientific questions, investigate the underlying methods in Jupyter notebooks, and use AI as a tutor and coding assistant. Each lesson asks them to explain what an analysis changes, inspect its output, and defend the resulting claim.

**Begin with [R00: Reading a research paper](notebooks/00_paper_orientation/00_how_to_read.ipynb).** The [study plan](curriculum/STUDY_PLAN.md) then guides students through the full course. [Setup](curriculum/SETUP.md) covers Jupyter, Ollama with Goose, and ChatGPT.

[![Notebook checks](https://github.com/Bowenislandsong/ai-neuroimaging-course/actions/workflows/notebooks.yml/badge.svg)](https://github.com/Bowenislandsong/ai-neuroimaging-course/actions/workflows/notebooks.yml)

## Get started

On macOS, Linux, or Windows Subsystem for Linux, run:

```sh
git clone https://github.com/Bowenislandsong/ai-neuroimaging-course.git
cd ai-neuroimaging-course
./setup.sh
uv run --locked jupyter lab notebooks
```

The setup script installs [uv](https://docs.astral.sh/uv/) if needed, installs the pinned Python version and course libraries, and prepares Jupyter. Run `./setup.sh --check` for the offline lessons or `./setup.sh --check-all` to include the public-data project. Both checks cover the four notebooks in the introductory supplement. The reading seminars open directly on GitHub.

## Course sequence

The opening two weeks use six papers in three seminars. Students first identify the question, interpret a figure, and record what they need to learn. They revisit those papers after studying the relevant methods.

| Seminar | Foundational study | Recent method | Guiding question |
|---|---|---|---|
| [Processing](notebooks/00_paper_orientation/01_why_processing.ipynb) | [fMRIPrep](curriculum/papers/processing.md#pp01) | [BrainMorph](curriculum/papers/processing.md#pp04) | Which transformations connect a scan to an analysis? |
| [Generalization](notebooks/00_paper_orientation/02_why_generalization.ipynb) | [Marek et al.](curriculum/papers/design.md#pd02) | [BrainIAC](curriculum/papers/modeling.md#pm03) | When will a result extend to new participants? |
| [Evidence](notebooks/00_paper_orientation/03_why_evidence_audits.ipynb) | [NARPS](curriculum/papers/design.md#pd01) | [Omni-fMRI](curriculum/papers/modeling.md#pm05) | How do analysis choices and evaluation conditions shape a conclusion? |

The complete [paper library](curriculum/papers/README.md) contains **24 foundational and SOTA readings** with assigned sections, figure questions, coursework, and instructor notes. Each computational lesson opens with a paper question, grounds its mathematical formulation in both landmark studies and 2023–2026 frontier models, and closes with a return to the research claim.

## Curriculum

| Component | Classes | Topics |
|---|---:|---|
| Reading seminars | 4 | Research questions, Three-Pass figure forensics, Foundational vs. SOTA comparisons, and evidence evaluation |
| Foundations | 4 | Transformation contracts, MR physics ($T_1/T_2/T_2^*$) & neurovascular BOLD coupling, snippet auditing, and deterministic computational state |
| [Image processing](curriculum/processing_coverage.md) | 21 | Coordinate frames, affine & diffeomorphic registration, N4 bias, tissue/surface morphometry, fMRI motion/susceptibility/CompCor/ICA denoising, diffusion MRI (DTI/CSD/tractography), connectomes, and DAG provenance |
| [Research design](curriculum/design_coverage.md) | 16 | Potential-outcomes estimands, sampling & missingness, ICC reliability, power & Type M/S errors, HRF/FIR design efficiency, factorial confounding, GLS prewhitening, mixed effects, permutation/TFCE, circularity, Bayesian/TOST intervals, and multiverse analysis |
| [Data science](curriculum/data_science_coverage.md) | 16 | 4D tensor strides & broadcasting, relational BIDS joins, NIfTI binary precision, robust statistics, fold-isolated imputation, Bayes PPV, cluster bootstrap, SVD/PCA, feature-screening leakage, and SHA-256 reproducibility |
| [Modeling](curriculum/modeling_coverage.md) | 18 | Encoding/decoding & Haufe transforms, Ridge/Lasso/ElasticNet, kernels & ensembles, nested CV & ComBat harmonization, PCA/ICA, clustering stability, graph theory & CPM, Crossnobis RSA, searchlight MVPA, ISC/SRM alignment, HMM/Kalman/DCM dynamics, CNN backprop, Dice/Focal segmentation, 3D SSL transfer, Transformer attention, and calibration |
| Projects | 4 | MNI152 anatomical transformations, single-run task fMRI GLM, multi-site clinical cohort prediction & harmonization, and a preregistered multiverse research defense |

The [class index](curriculum/NOTEBOOK_INDEX.md) links all **83 original notebooks**: four reading seminars and 79 computational lessons and projects. Every computational notebook features **1,800–2,600+ words of graduate-level theory and mathematical derivations**, **4–5 executable code cells** (synthetic phantom implementation, deliberate failure mode & forensic repair, parameter sensitivity / SOTA ablation sweep, and hands-on verification), and a **publication-grade multi-panel `matplotlib` visualization dashboard**. The course also assigns longer practicals from established university courses and research software workshops. Selected source notebooks are preserved with [attribution and license records](THIRD_PARTY_NOTICES.md).

## Coursework and assessment

Students keep an [evidence ledger](curriculum/coursework/EVIDENCE_LEDGER.md) for each paper and complete four integrated assignments:

1. **[Figure brief](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a1--first-pass-figure-brief):** explain the motivating question and evidence in the six opening papers.
2. **[Mechanism experiment](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a2--mechanism-experiment):** predict, run, inspect, and explain a transformation relevant to a paper.
3. **[Figure or table reconstruction](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a3--figure-or-table-reconstruction-proposal):** plan and complete an agreed analysis with documented inputs and methods.
4. **[Research review and defense](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a4--reviewer-response-and-research-proposal):** connect the literature to a research question, analysis plan, and independent evaluation.

A separate [model evaluation worksheet](curriculum/coursework/SOTA_AUDIT.md) examines a method's inputs, training target, comparison, metrics, and generalization. Students can work with **Ollama and Goose** using Qwen or Gemma, or use **ChatGPT** beside Jupyter. The [AI workflow](curriculum/AI_WORKFLOW.md) keeps each interaction focused on a source, a prediction, a short operation, and an explanation.

## Teaching sources and university curriculum alignment

The pedagogical depth, mathematical rigor, and laboratory sequence synthesize best practices from leading graduate neuroimaging and computational neuroscience curricula:

| Teaching sequence | Source examples |
|---|---|
| University and open courses | USC NIIN (520/540/550/580), Stanford Psych 204A/B & CS231n, [DartBrains](https://github.com/ljchang/dartbrains), [Berkeley PSYCH214](https://bic-berkeley.github.io/psych-214-fall-2016/), [Data 8](https://inferentialthinking.com/) / Data 100, [MIT OpenCourseWare (9.07/9.63)](https://ocw.mit.edu/), [Neuromatch](https://compneuro.neuromatch.io/), [BrainIAK](https://github.com/brainiak/brainiak-tutorials) |
| Specialist practicals | [FSL](https://fsl.fmrib.ox.ac.uk/fslcourse/), [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial), [DIPY](https://docs.dipy.org/stable/examples_built/index.html), [Nipype](https://github.com/nipy/nipype_tutorial) |

The [source registry](curriculum/SOURCES.md) records selected materials and versions; the [coverage map](curriculum/COVERAGE_AUDIT.md) shows how each topic is taught.

## Verification

`./setup.sh --check` validates repository links and runs **82 offline notebooks** in fresh kernels: 78 current lessons and four from the introductory supplement. `./setup.sh --check-all` also runs the public-data fMRI project, for **83 computational notebooks** in total. The four reading seminars use instructor assessment. Preserved third-party notebooks are separate source assignments with their original tool and data requirements. See the [verification record](curriculum/VERIFICATION.md) for results.

## Reuse

Original lessons and notebooks are licensed [CC BY-SA 4.0](LICENSE); original standalone scripts use [MIT](LICENSES/MIT.txt). External publications, datasets, notebooks, and software retain their own terms, documented in [third-party notices](THIRD_PARTY_NOTICES.md).
