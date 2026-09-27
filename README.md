# Neuroimaging Research Methods with AI

A 26-week graduate-level course in neuroimaging analysis, experimental design, data science, and computational modeling designed for **macOS on a standard Apple Silicon MacBook Pro**. Students read foundational and state-of-the-art (SOTA) research papers to understand the scientific questions, investigate the underlying mathematical transformations in Jupyter notebooks, and use an **agentic local AI setup (Goose + Ollama running the latest Qwen and Gemma models)** to accelerate class deliverables while maintaining rigorous scientific supervision.

**Start with [Step 0: Set Up Goose + Ollama (Qwen & Gemma) on Your MacBook Pro](curriculum/SETUP.md), then open [R00: Reading a research paper](notebooks/00_paper_orientation/00_how_to_read.ipynb).** The [26-week study plan](curriculum/STUDY_PLAN.md) and [agentic AI workflow](curriculum/AI_WORKFLOW.md) guide you through every deliverable.

[![Notebook checks](https://github.com/Bowenislandsong/ai-neuroimaging-course/actions/workflows/notebooks.yml/badge.svg)](https://github.com/Bowenislandsong/ai-neuroimaging-course/actions/workflows/notebooks.yml)

## Step 0 · Set up your MacBook Pro agentic environment (macOS + Ollama + Goose)

This course targets **macOS on a standard Apple Silicon MacBook Pro (`M1` / `M2` / `M3` / `M4`)**. Before starting the lessons, set up your local agentic pair-programming stack (**Ollama** serving the latest **Qwen** and **Gemma 4** models connected to **Goose**) alongside the locked Python environment.

Open **Terminal.app** on your MacBook Pro and run:

```zsh
# 1. Clone the course repository and install the locked Python 3.12 + Jupyter environment
git clone https://github.com/Bowenislandsong/ai-neuroimaging-course.git
cd ai-neuroimaging-course
./setup.sh

# 2. Install Ollama for macOS and pull BOTH Qwen and Gemma's latest models for a standard MacBook Pro
brew install --cask ollama
open -a Ollama

# Standard 16 GB – 24 GB MacBook Pro (runs smoothly alongside JupyterLab):
ollama pull qwen3.5:9b      # Latest compact Qwen (~6.6 GB, 256K context, agentic tool use & coding)
ollama pull gemma4:e4b      # Latest Gemma 4 (~9.6 GB, 128K context, multimodal reasoning & scientific audit)

# (Optional) If your MacBook Pro has 32 GB+ unified memory, pull the larger flagship pair:
# ollama pull qwen3.6:27b   # Latest Qwen 3.6 agentic coding flagship (~18 GB, 256K context)
# ollama pull gemma4:26b    # Latest Gemma 4 MoE reasoning model (~19 GB, 256K context)

# 3. Install Goose for macOS and connect it to your local Ollama server
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
goose configure             # Select: Ollama -> http://localhost:11434 -> qwen3.5:9b (or qwen3.6:27b)

# 4. Launch JupyterLab in one Terminal tab and Goose in a second tab
uv run --frozen jupyter lab notebooks
```

*(You can also run `./setup.sh --setup-ai` on macOS to automatically detect your MacBook Pro's unified memory via `sysctl -n hw.memsize` and pull the matching Qwen + Gemma model pair.)* See [curriculum/SETUP.md](curriculum/SETUP.md) for the complete macOS Step 0 guide and verification smoke test.

## How we use AI for class deliverables: delegate the grunt work, supervise the science

In modern neuroimaging research, an AI coding agent (**Goose** driven by **Qwen** for code/tool execution and cross-checked with **Gemma 4** for scientific reasoning) can draft data loaders, matrix operations, and multi-panel plots in seconds. **Your job as the researcher is not to type boilerplate syntax from scratch—it is to direct the agent efficiently, spot silent methodological errors immediately, trace bugs back to their mathematical or physical root cause, and verify that the outcome makes scientific sense.**

To build that skill, every lesson and deliverable in this repository provides three structured supervision tools (detailed in [curriculum/AI_WORKFLOW.md](curriculum/AI_WORKFLOW.md)):

1. **Suggestive Prompts (*"in the spirit of what to ask," not a rigid script*):** Goal-oriented prompt patterns that tell Goose/Ollama *what transformation contract to implement* (input/output shapes, physical units, fitting boundaries, and required diagnostics) while letting the agent handle the coding grunt work.
2. **What to Look For & How to Trace Errors Back Down:** AI-generated neuroimaging code rarely crashes with a syntax error; instead, it fails *silently* (e.g., resetting a NIfTI affine to `np.eye(4)`, reshaping `(T, V)` instead of transposing, linearly interpolating integer parcellation labels, filtering before frame scrubbing, or leaking feature screening across cross-validation folds). Each lesson highlights the exact visual and numerical red flags to spot immediately, how to trace the discrepancy back to the exact line/axis/unit/split where the bug entered, and how to fix it.
3. **Expected Outcome Ranges & Why It Must Look That Way:** Instead of asking you to match a single brittle magic number, every lesson specifies the **expected numerical and visual range** for a valid implementation versus a broken baseline—and explains from first principles (MR physics, linear algebra, or statistical theory) **why** the outcome must fall inside that range.

## Course sequence

The opening two weeks use six papers in three seminars (`R00`–`R03`). Students first identify the question, interpret a figure, and record what they need to learn. They revisit those papers after studying the relevant methods.

| Seminar | Foundational study | Recent method | Guiding question |
|---|---|---|---|
| [Processing](notebooks/00_paper_orientation/01_why_processing.ipynb) | [fMRIPrep](curriculum/papers/processing.md#pp01) | [BrainMorph](curriculum/papers/processing.md#pp04) | Which transformations connect a scan to an analysis? |
| [Generalization](notebooks/00_paper_orientation/02_why_generalization.ipynb) | [Marek et al.](curriculum/papers/design.md#pd02) | [BrainIAC](curriculum/papers/modeling.md#pm03) | When will a result extend to new participants? |
| [Evidence](notebooks/00_paper_orientation/03_why_evidence_audits.ipynb) | [NARPS](curriculum/papers/design.md#pd01) | [Omni-fMRI](curriculum/papers/modeling.md#pm05) | How do analysis choices and evaluation conditions shape a conclusion? |

The complete [paper library](curriculum/papers/README.md) contains **24 foundational and SOTA readings** with assigned sections, figure questions, coursework, and instructor notes, complemented by the [complete lesson reference index](curriculum/papers/REFERENCES.md) (**310 verified citations across 263 distinct foundational and 2019–2026 works**, with OpenAlex citation counts and per-lesson *"Why this technique matters"* rationales). Each computational lesson opens with a paper question, grounds its mathematical formulation in both landmark studies and frontier models, and closes with an **Agentic Supervision & Deliverable Guide** and a return to the research claim.

## Curriculum

| Component | Classes | Topics |
|---|---:|---|
| Reading seminars | 4 | Research questions, Three-Pass figure forensics, Foundational vs. SOTA comparisons, and evidence evaluation |
| Foundations | 4 | Step 0 MacBook Pro agentic workflow, transformation contracts, MR physics ($T_1/T_2/T_2^*$) & neurovascular BOLD coupling, snippet auditing, and deterministic computational state |
| [Image processing](curriculum/processing_coverage.md) | 21 | Coordinate frames, affine & diffeomorphic registration, N4 bias, tissue/surface morphometry, fMRI motion/susceptibility/CompCor/ICA denoising, diffusion MRI (DTI/CSD/tractography), connectomes, and DAG provenance |
| [Research design](curriculum/design_coverage.md) | 16 | Potential-outcomes estimands, sampling & missingness, ICC reliability, power & Type M/S errors, HRF/FIR design efficiency, factorial confounding, GLS prewhitening, mixed effects, permutation/TFCE, circularity, Bayesian/TOST intervals, and multiverse analysis |
| [Data science](curriculum/data_science_coverage.md) | 16 | 4D tensor strides & broadcasting, relational BIDS joins, NIfTI binary precision, robust statistics, fold-isolated imputation, Bayes PPV, cluster bootstrap, SVD/PCA, feature-screening leakage, and SHA-256 reproducibility |
| [Modeling](curriculum/modeling_coverage.md) | 18 | Encoding/decoding & Haufe transforms, Ridge/Lasso/ElasticNet, kernels & ensembles, nested CV & ComBat harmonization, PCA/ICA, clustering stability, graph theory & CPM, Crossnobis RSA, searchlight MVPA, ISC/SRM alignment, HMM/Kalman/DCM dynamics, CNN backprop, Dice/Focal segmentation, 3D SSL transfer, Transformer attention, and calibration |
| Projects | 4 | MNI152 anatomical transformations, single-run task fMRI GLM, multi-site clinical cohort prediction & harmonization, and a preregistered multiverse research defense |

The [class index](curriculum/NOTEBOOK_INDEX.md) links all **83 original notebooks**: four reading seminars and 79 computational lessons and projects. Every computational notebook features **graduate-level theory and mathematical derivations**, a verified *"Why this technique matters"* literature rationale with **2–4 canonical and modern (2019+) citations**, **4–5 executable code cells** (synthetic phantom implementation, deliberate failure mode & forensic repair, parameter sensitivity / SOTA ablation sweep, and hands-on verification), a **publication-grade multi-panel `matplotlib` visualization dashboard**, and a lesson-specific **Agentic Deliverable Supervision Guide** (suggestive prompt, error-spotting & root-cause traceback, and expected outcome ranges with first-principles justification). Selected source notebooks from university courses are preserved with [attribution and license records](THIRD_PARTY_NOTICES.md).

## Coursework and assessment

Students keep an [evidence ledger](curriculum/coursework/EVIDENCE_LEDGER.md) for each paper and complete four integrated assignments:

1. **[Figure brief](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a1--first-pass-figure-brief):** explain the motivating question and evidence in the six opening papers.
2. **[Mechanism experiment](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a2--mechanism-experiment):** predict, delegate to Goose/Ollama with a suggestive prompt, spot and repair a deliberate failure, verify the outcome against its expected range, and explain a transformation relevant to a paper.
3. **[Figure or table reconstruction](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a3--figure-or-table-reconstruction-proposal):** plan and complete an agreed analysis with documented inputs, expected outcome ranges, and provenance.
4. **[Research review and defense](curriculum/coursework/PAPER_TO_EXPERIMENT.md#a4--reviewer-response-and-research-proposal):** connect the literature to a research question, analysis plan, and independent evaluation.

A separate [model evaluation worksheet](curriculum/coursework/SOTA_AUDIT.md) examines a method's inputs, training target, comparison, metrics, and generalization. The [AI workflow](curriculum/AI_WORKFLOW.md) details how to pair **Goose + Ollama (`qwen3.5:9b`/`qwen3.6:27b` and `gemma4:e4b`/`gemma4:26b`)** on your MacBook Pro for every deliverable.

## Teaching sources and university curriculum alignment

The pedagogical depth, mathematical rigor, and laboratory sequence synthesize best practices from leading graduate neuroimaging and computational neuroscience curricula:

| Teaching sequence | Source examples |
|---|---|
| University and open courses | USC NIIN (520/540/550/580), Stanford Psych 204A/B & CS231n, [DartBrains](https://github.com/ljchang/dartbrains), [Berkeley PSYCH214](https://bic-berkeley.github.io/psych-214-fall-2016/), [Data 8](https://inferentialthinking.com/) / Data 100, [MIT OpenCourseWare (9.07/9.63)](https://ocw.mit.edu/), [Neuromatch](https://compneuro.neuromatch.io/), [BrainIAK](https://github.com/brainiak/brainiak-tutorials) |
| Specialist practicals | [FSL](https://fsl.fmrib.ox.ac.uk/fslcourse/), [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial), [DIPY](https://docs.dipy.org/stable/examples_built/index.html), [Nipype](https://github.com/nipy/nipype_tutorial) |

The [source registry](curriculum/SOURCES.md) records selected materials and versions; the [coverage map](curriculum/COVERAGE_AUDIT.md) shows how each topic is taught.

## Verification

On your MacBook Pro, `./setup.sh --check` validates repository links and runs **82 offline notebooks** in fresh kernels: 78 current lessons and four from the introductory supplement. `./setup.sh --check-all` also runs the public-data fMRI project, for **83 computational notebooks** in total. The four reading seminars use instructor assessment. Preserved third-party notebooks are separate source assignments with their original tool and data requirements. See the [verification record](curriculum/VERIFICATION.md) for results.

## Reuse

Original lessons and notebooks are licensed [CC BY-SA 4.0](LICENSE); original standalone scripts use [MIT](LICENSES/MIT.txt). External publications, datasets, notebooks, and software retain their own terms, documented in [third-party notices](THIRD_PARTY_NOTICES.md).
