# AI-guided neuroimaging: understand every transformation

A notebook-first course for a learner who uses **Ollama + Goose + Qwen/Gemma, or ChatGPT**, to write small analysis snippets—and learns to explain, inspect, and challenge what those snippets do.

**79 original teaching notebooks** cover foundations, image processing, experimental design, data science, modeling, and integrated projects. Each strand pairs digestible explanations and executable experiments with existing university or workshop materials. **13 original upstream notebooks and one Marimo lesson** are included unchanged with attribution, licenses, version pins, and hashes. Longer source assignments are part of the learning plan, not implied completed work.

[![Notebook checks](https://github.com/Bowenislandsong/ai-neuroimaging-course/actions/workflows/notebooks.yml/badge.svg)](https://github.com/Bowenislandsong/ai-neuroimaging-course/actions/workflows/notebooks.yml)

**Start:** [First class](notebooks/00_foundations/01_learning_contract.ipynb) · [Every notebook](curriculum/NOTEBOOK_INDEX.md) · [Study sequence](curriculum/STUDY_PLAN.md) · [Setup](curriculum/SETUP.md) · [AI tutor workflow](curriculum/AI_WORKFLOW.md)

## What is taught

| Strand | Notebooks | Substantive coverage |
|---|---:|---|
| Foundations | 4 | MRI measurement/contrast, BOLD, snippet literacy, transformations, notebook state |
| [Processing](curriculum/processing_coverage.md) | 21 | NIfTI geometry; registration and nonlinear warps; bias fields, brain extraction, tissue segmentation, morphometry, surfaces; slice timing, motion, distortion, smoothing, temporal filters, nuisance/ICA, censoring/QC; diffusion gradients, denoising, tensors, crossing fibers, tractography; parcellations and workflows |
| [Research design](curriculum/design_coverage.md) | 16 | Estimands, sampling, missingness, reliability, power; block/event/HRF/FIR design, efficiency, factorials; GLM/contrasts, temporal noise, hierarchical/repeated data, permutation, multiplicity/TFCE, ROI circularity, Bayesian/equivalence reasoning, reproducibility |
| [Data science](curriculum/data_science_coverage.md) | 16 | Arrays, participant tables, NIfTI I/O, EDA, missingness, probability, sampling and bootstrap, standardization, linear algebra, likelihood, optimization, regression diagnostics, PCA, selection, provenance |
| [Modeling](curriculum/modeling_coverage.md) | 18 | Encoding/decoding, regularization, kernels/ensembles, grouped/nested/site validation, PCA/ICA/clustering, connectomes, RSA, searchlights, naturalistic ISC, latent/generative models, HMMs/dynamics, CNN training, segmentation, self-supervision/transfer, attention/foundation models, calibration/explanations |
| Projects | 4 | Real anatomical-template transformations; real single-run fMRI GLM; held-out-site cohort prediction; supervised research plan and defense |

Classes follow **predict → ask AI → run a short operation → inspect → break → explain → transfer**. The local examples isolate mechanics; the upstream assignments provide longer practicals. The learner is assessed on scientific understanding, not on whether an assistant can produce code that runs.

## The actual source curricula

The selection favors public syllabi, substantial lesson sequences, available code, and clear reuse terms. It is not a ranking by popularity or a claim that every source is a graduate course.

| Source | Why it anchors this course |
|---|---|
| [Dartmouth PSYC60 / DartBrains](https://github.com/ljchang/dartbrains/blob/b72537ad25deee0281248a415a052cd87ff325de/content/Syllabus.md) | Actual syllabus, comprehensive brain-mapping lessons and notebooks; legacy Jupyter version distinguished from current Marimo version |
| [Berkeley PSYCH214](https://bic-berkeley.github.io/psych-214-fall-2016/syllabus.html) | Actual imaging-analysis syllabus, classes/labs, coordinate transforms, GLM and reproducible projects |
| [Berkeley Data 8](https://inferentialthinking.com/chapters/intro.html) | Extensive accessible data-science textbook and exercises; linked in its original form under its own terms |
| [MIT 9.07](https://ocw.mit.edu/courses/9-07-statistics-for-brain-and-cognitive-science-fall-2016/pages/syllabus/) and [9.63](https://ocw.mit.edu/courses/9-63-laboratory-in-visual-cognition-fall-2009/pages/lecture-notes/) | Dated statistics and experimental-design course schedules and lecture materials |
| [Neuromatch computational neuroscience](https://compneuro.neuromatch.io/) and [deep learning](https://deeplearning.neuromatch.io/) | Full open notebook curricula, exercises, models, optimization, CNNs and attention |
| [BrainIAK tutorials](https://github.com/brainiak/brainiak-tutorials) | Advanced imaging analysis materials based on courses at Princeton and Yale |
| [Oxford FSL](https://fsl.fmrib.ox.ac.uk/fslcourse/), [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial), [DIPY](https://docs.dipy.org/stable/examples_built/index.html), [Nipype](https://github.com/nipy/nipype_tutorial) | Specialist processing workshops and workflows that short Python simulations cannot replace |

See the [source and reuse registry](curriculum/SOURCES.md), [upstream assignments](third_party/README.md), and [coverage audit](curriculum/COVERAGE_AUDIT.md) for exact versions, source topics, local depth, and remaining work.

## What “thorough” means here

USC NIIN 540/520/580/550 inspired the four strands. **Detailed public USC syllabi were not found**, so this repository does not claim to reproduce their weekly coverage or replace the master's program. It expands against inspectable parallel curricula and explicitly records gaps.

The 79 notebooks are a substantial guided foundation. Full FSL/FreeSurfer/DIPY processing, real cohort inference, DCM/ComBat, large 3D neural networks, and external imaging checkpoints remain named specialist extensions where appropriate. The real fMRI project deliberately exposes what a GLM on supplied raw teaching images omits; it is not presented as a fully preprocessed research result. The [coverage audit](curriculum/COVERAGE_AUDIT.md) prevents a toy demonstration from being mistaken for completed method training.

## Run and verify

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab notebooks
```

Windows: use `.venv\Scripts\python.exe`. No local LLM is needed to run the notebooks. See [setup](curriculum/SETUP.md) for AI configuration and the course environment.

```sh
.venv/bin/python scripts/check_repository.py
.venv/bin/python scripts/validate_notebooks.py
```

The default check runs **78 offline notebooks** in fresh Jupyter kernels. The real fMRI project is opt-in with `--include-network`. All **79 notebooks / 150 code cells** passed the delivered local Jupyter run; see [verification](curriculum/VERIFICATION.md). The 13 upstream reference notebooks are preserved material, not included in that execution claim. GitHub Actions independently checks the offline core on Linux.

The earlier short [introductory pack](course/README.md) remains as a supplement. The `notebooks/` tree and this README are the expanded course.

## Reuse

Original teaching text and notebooks: [CC BY-SA 4.0](LICENSE). Original standalone scripts: [MIT](LICENSES/MIT.txt). Third-party files retain their original licenses and notices; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Linked readings and downloaded datasets do not inherit this repository's license. No institutional endorsement is implied.
