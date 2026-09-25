# What was verified

**Delivered local result: 79/79 original notebooks passed, 150 code cells, 45 captured figures.** Each notebook ran in a fresh real Jupyter kernel using `nbclient`, in source order, with no allowed cell errors. The complete machine-readable record is [validation.json](validation.json). A targeted rerun after review verified DS03's added NIfTI millimeter metadata check. Markdown-only source-link corrections did not change executed calculations.

The run used Python 3.14.7, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.6, Matplotlib 3.11.2, scikit-learn 1.9.1, NiBabel 5.4.2, Nilearn 0.14.1, nbformat 5.11.1, nbclient 0.11.0 and ipykernel 7.3.0. The [tested environment snapshot](../requirements-tested.txt) includes platform-specific dependencies; use [requirements.txt](../requirements.txt) for a fresh portable installation and rerun checks. Dependency ranges are not a claim that every permitted combination has been tested.

## Scope of the checks

| Check | Result and interpretation |
|---|---|
| Core notebooks | All 79 passed fresh-kernel execution and their encoded assertions; 78 offline plus one opt-in data-download project |
| Repo structure | Notebook schemas, unique IDs, local teaching links and upstream byte hashes checked by [check_repository.py](../scripts/check_repository.py) |
| Code/model mechanics | Assertions cover geometry, units, matching rows, rank, fitting boundaries, numerical recovery, gradient checks and deliberate failure contrasts where appropriate |
| Source integrity | All 25 preserved file hashes in the manifests match; 13 upstream `.ipynb` files plus one Marimo `.py` and source/license evidence are separately identified |
| Source accuracy | Actual syllabi/TOCs and pinned notebook headings inspected; independent spot-check of representative chapter links and official setup/model links |
| Visual review | Representative real-template slices, TFCE demonstration and CNN training curves inspected; strand-level figure checks are recorded separately |
| Public-data project | SPM download, sidecar/events, design, AR(1) GLM, effects/z map, two-sided voxel FDR and residual diagnostic executed locally |
| GitHub Actions | Workflow supplied for an independent Linux/Python 3.12 offline run; consult the live Actions result for its status |

The strand-specific JSON files describe earlier direct Python/Agg checks. The repository-wide Jupyter record above is the integrated execution evidence and includes the final core cells. Neither record is a learner's completed assessment.

## Real fMRI execution and its limits

The delivered SPM image has **84 volumes**, TR **7 seconds**, and metadata recording **12 already discarded volumes**. Its supplied events align with that delivered time axis. The executed design has 13 columns including listening, cosine drifts and intercept. The fitted mask contains 61,335 voxels. The [numeric run summary](real_fmri_run.json) preserves the output and configuration scope without redistributing raw images.

These are implementation results, not biological validation. P02 intentionally models the supplied **raw teaching images** and omits full motion/distortion correction, anatomical registration and measured nuisance regressors. Its AR(1) and smoothing settings do not repair those omissions. A single run from one person does not establish population effects. The course requires a full upstream preprocessing practical before treating this as a research workflow.

## Explicitly not verified here

The 13 preserved upstream Jupyter notebooks and one Marimo lesson were not run with their external data/tools; some retain student exercises and historical dependencies. FSL, FreeSurfer, DIPY, fMRIPrep, DCM, ComBat, SRM and external imaging checkpoints are not certified installed or executed by this build. No live Ollama/Goose tutor integration, large-model download, or accuracy benchmark of Qwen/Gemma/ChatGPT was performed. Official setup instructions were checked, and the scientific code runs independently of a tutor model.

Reproduce the offline run with `python scripts/validate_notebooks.py`; add `--include-network` for the real-data project. Results and executed copies go to ignored `build/`, and downloaded/derived data go to ignored `data/` and `outputs/`. Do not modify preserved upstream bytes to make local checks pass.
