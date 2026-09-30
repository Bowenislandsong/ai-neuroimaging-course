# What was verified

## Locked uv environment (macOS MacBook Pro target + CI runner)

The [macOS uv validation run](uv_validation.json) used `darwin` (macOS), Python 3.12.13, and the committed [lockfile](../uv.lock). **All 83 course-authored computational notebooks passed in fresh Jupyter kernels:** 79 in the current course, including the public-data fMRI project, and four in the introductory supplement. The four reading seminars are assessed by an instructor. On your MacBook Pro, run `./setup.sh --check-all` to repeat the complete computational check.

The source notebooks preserved in `third_party/` are assignments from other courses and retain their original software and data requirements.

## Latest fresh-kernel validation record

**Computational baseline (upgraded graduate curriculum): 83/83 computational notebooks passed (78 offline lessons + 1 network project + 4 companion labs), 371 main-course code cells, and 80 captured multi-panel figures across 100% of offline computational notebooks.** Each notebook ran in a fresh real Jupyter kernel using `nbclient`, in source order, with no allowed cell errors and zero saved `stderr` warnings. The complete machine-readable record is [validation.json](validation.json).

New installations on macOS use the [uv lockfile](../uv.lock) and Python 3.12 via `./setup.sh`. The earlier [environment snapshot](../requirements-tested.txt) records the historical Python 3.14 baseline run.

## Paper-first, SOTA, and Agentic Supervision expansion

The course contains **83 notebooks: 79 computational notebooks and four reading-only seminars**. The seminars require human assessment and are explicitly skipped by the executor, including when `--include-network` is supplied. A skipped seminar is not a passed assignment. Every computational notebook includes:
- Graduate-level mathematical derivations and physical/statistical intuition;
- A deterministic *"Why this technique matters"* section with 2–4 verified canonical and modern (2019+) citations;
- Explicit SOTA paper motivations and 4–5 multi-step lab code cells;
- Embedded multi-panel diagnostic visualizations; and
- A lesson-specific **Agentic Deliverable Supervision Guide (Goose + Ollama Qwen/Gemma on macOS)** containing a **Suggestive Prompt ("in the spirit of")**, **What to Look For & Root-Cause Error Traceback**, and **Expected Outcome Ranges & First-Principles "Why"**.

The [paper registry](papers/paper_registry.json) contains **24 foundational and SOTA sources** (`PP01`–`PP08`, `PD01`–`PD07`, `PM01`–`PM08`, `PB01`) with publication/assigned-version distinctions and exact reading targets, complemented by [key_references.json](papers/key_references.json) and [REFERENCES.md](papers/REFERENCES.md) (**310 lesson reference entries across 263 distinct works; 277/277 total distinct references verified `MATCH` against Crossref, OpenAlex, and arXiv in [reference_verification.json](papers/reference_verification.json) by [verify_references.py](../scripts/verify_references.py)**). Source records state which primary passages, captions and publication/code records were inspected, including access limitations. The coursework does not claim complete visual inspection of all paper figures, a systematic review of all frontier models, or execution of author implementations.

Structural checks cover reading metadata, paper IDs, notebook mappings, agentic supervision guides, local links, saved `stderr`/path-leak hygiene, LaTeX math integrity, reference verification status, and all preserved upstream hashes. See the dated [paper update checks](paper_update_validation.json) for this addition's checks.

## Scope of the checks

| Check | Result and interpretation |
|---|---|
| Computational notebooks | All 79 passed fresh-kernel execution and their encoded assertions (plus all 4 companion labs in `course/labs/`, for 83/83 computational notebooks total); 78 offline plus one opt-in data-download project |
| Repo structure & hygiene | Notebook schemas, unique IDs, local teaching links, agentic supervision guides (`agentic_guides.json`), zero saved `stderr` outputs, zero local home-path leaks, zero stripped-math signatures, and 25 upstream byte hashes checked by [check_repository.py](../scripts/check_repository.py) |
| Reference & citation audit | All 277 distinct works across the 24-paper library and 310 lesson key references verified `MATCH` against Crossref, OpenAlex, and arXiv by [verify_references.py](../scripts/verify_references.py) |
| Code/model mechanics | Assertions cover geometry, units, matching rows, rank, fitting boundaries, numerical recovery, gradient checks and deliberate failure contrasts where appropriate |
| Source integrity | All 25 preserved file hashes in the manifests match; 13 upstream `.ipynb` files plus one Marimo `.py` and source/license evidence are separately identified |
| Source accuracy | Actual syllabi/TOCs and pinned notebook headings inspected; independent spot-check of representative chapter links and official setup/model links (`ollama.com/library/qwen3.6`, `qwen3.5`, `gemma4`, and `goose-docs.ai`) |
| Visual review | Representative real-template slices, TFCE demonstration and CNN training curves inspected; strand-level figure checks are recorded separately |
| Public-data project | SPM download, sidecar/events, design, AR(1) GLM, effects/z map, two-sided voxel FDR and residual diagnostic executed locally |
| GitHub Actions CI | Automated CI workflow executes the offline verification suite on every push/PR; consult the live Actions badge for status |

The strand-specific JSON files describe earlier direct Python/Agg checks. The repository-wide Jupyter record above is the integrated execution evidence and includes the final core cells. Neither record is a learner's completed assessment.

## Real fMRI execution and its limits

The delivered SPM image has **84 volumes**, TR **7 seconds**, and metadata recording **12 already discarded volumes**. Its supplied events align with that delivered time axis. The executed design has 13 columns including listening, cosine drifts and intercept. The fitted mask contains 61,335 voxels. The [numeric run summary](real_fmri_run.json) preserves the output and configuration scope without redistributing raw images.

These are implementation results, not biological validation. P02 intentionally models the supplied **raw teaching images** and omits full motion/distortion correction, anatomical registration and measured nuisance regressors. Its AR(1) and smoothing settings do not repair those omissions. A single run from one person does not establish population effects. The course requires a full upstream preprocessing practical before treating this as a research workflow.

## Explicitly not verified here

The 13 preserved upstream Jupyter notebooks and one Marimo lesson were not run with their external data/tools; some retain student exercises and historical dependencies. FSL, FreeSurfer, DIPY, fMRIPrep, DCM, ComBat, SRM and external imaging checkpoints are not certified installed or executed by this build. Official macOS setup instructions and model tags for Ollama (`qwen3.5:9b`, `qwen3.6:27b`, `gemma4:e4b`, `gemma4:26b`) and Goose were verified against live documentation, while the scientific Python code runs deterministically without requiring live LLM calls during automated notebook validation.

Run `./setup.sh --check` on your MacBook Pro for the offline suite or `./setup.sh --check-all` for all original computational notebooks, including the public-data project. Results and executed copies go to ignored `build/`; downloaded and derived data go to ignored `data/` and `outputs/`.
