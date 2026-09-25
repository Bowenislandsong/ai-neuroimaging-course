# Verification report

Verified 24 September 2026 (Los Angeles), Python 3.14.7. Exact package versions are in [results.json](results.json) and [requirements-tested.txt](../requirements-tested.txt).

| Notebook | Lesson sections | Executed code cells | Embedded figures | Result |
| --- | ---: | ---: | ---: | --- |
| 520 experimental design | 6 | 16 | 7 | All assertions passed |
| 540 processing | 6 | 13 | 6 | All assertions passed |
| 550 modeling | 6 | 18 | 4 | All assertions passed |
| 580 data science | 6 | 12 | 3 | All assertions passed |
| **Total** | **24** | **59** | **20** | **Passed** |

All notebook files passed nbformat validation. Every code cell contains at most 20 lines. Each notebook was executed from fresh state; 520, 550, and 580 also use fresh namespaces per numbered lesson. The 540 notebook intentionally runs in order with its shared setup and intermediate arrays. Its sections should not be run from an empty kernel in isolation.

Execution used Python `exec` with Matplotlib's noninteractive Agg backend, capturing actual stdout and figures into the notebooks. A Jupyter kernel launch was unavailable under the authoring sandbox's socket restrictions; the Jupyter interface itself was not tested. The standalone runner is [verify_course.py](verify_course.py). It raises on failed cell assertions rather than concealing them. The numerical code does not require a running LLM.

Independent content reviews checked transformation direction, interpolation type, temporal filtering, nuisance projection, independent sampling units, contrast order, statistical-map interpretation, multiplicity, leakage, grouped validation, metrics, and toy-versus-real claims. Corrections included Butterworth design-order wording and clarifying that grouped splitting prevents participant overlap without proving independence.

Plots were visually inspected in a [contact sheet](contact_sheet.png), with representative individual figures inspected during module authoring. These checks address legibility and whether the figures represent the intended demonstrations; they do not certify a research pipeline.

## Foundation and real-image checks

- The simplified MRI signal example reproduces the four stated values within rounding tolerance.
- The packaged MNI152 template loaded without a data download. Shape: `(99,117,95)`; voxel dimensions: `(2,2,2)` mm; axis codes: `RAS`.
- Six-millimeter smoothing preserved shape and affine and changed intensities, as intended. Original and smoothed images were plotted with the same cuts and scale and visually inspected.
- The [real-template comparison](real_template_demo.png) is an attributed instructional illustration using Nilearn's packaged MNI152 reference, not an individual participant scan.

## Documented but not executed here

Ollama/Goose installation or inference, the learner's hardware/model performance, ChatGPT tutoring sessions, the SPM auditory dataset download/analysis, fMRIPrep processing, FSL registration, pretrained imaging-model inference/training, and a learner's capstone submission. Source links and current model tags were researched; none of these activities is presented as a successful run.

No detailed public USC syllabus was located for the four named courses. The teaching sequence is original and its NIIN relationship is explicitly limited to published subject descriptions.
