# Study sequence and workload

This is a substantial notebook curriculum, not four short survey classes. Use **24 weeks at roughly 8–12 hours per week** as a planning assumption, with extra time for specialist installations, harder upstream exercises, and a real supervised project. This estimate is a proposed schedule, not measured learner completion time. Compressing it requires more weekly time; skipping the upstream work changes the depth achieved.

Most strand notebooks take 75–100 minutes, plus 30–90 minutes for the named source assignment and transfer task. Some upstream practicals need a separate half-day or longer. Each notebook is independently runnable so a learner can revisit a weak concept without rebuilding a large pipeline.

Notebook IDs: **F** foundations, **PR** processing, **D** design, **DS** data science, **M** modeling, **P** projects. The [complete index](NOTEBOOK_INDEX.md) links every class. Use IDs below for sequence; directory order alone is not the teaching order.

| Week | Classes | Evidence before progressing |
|---:|---|---|
| 1 | F01–F04 | Explain a transformation contract; read a short cell; restart and rerun |
| 2 | DS01–DS04 | Correct axes, joins, NIfTI geometry and labeled EDA |
| 3 | DS05–DS08; D01–D02 | Explain missingness, observation unit, sampling and person bootstrap |
| 4 | DS09–DS12; D03–D04 | Distinguish scales/likelihood/optimization; defend reliability and power assumptions |
| 5 | DS13–DS16 | Diagnose regression, train-only PCA, selection bias and provenance |
| 6 | PR01–PR04 | Audit geometry, resampling, nonlinear transformations and bias fields |
| 7 | PR05–PR08 | Explain mask/segmentation/morphometry/surface contracts and QC |
| 8 | PR09–PR12; D05 | Connect acquisition timing, motion/distortion, smoothing and HRF design |
| 9 | PR13–PR15; D06 | Explain filtering, nuisance projection, censoring and HRF mismatch |
| 10 | PR16–PR19 | Defend gradient orientation, diffusion preprocessing, tensor and tractography limits |
| 11 | PR20–PR21; P01 | Submit spatial transformation manifest and a reproducible workflow graph |
| 12 | D07–D10 | Derive the intended contrast; inspect efficiency, rank and temporal noise |
| 13 | D11–D14 | Defend hierarchy, exchangeability, multiplicity and independent ROI selection |
| 14 | D15–D16; P02 | Record assumptions and sensitivity choices; audit a real-run GLM and its omissions |
| 15 | M01–M03 | Compare encoding/decoding, regularization, linear and nonlinear baselines |
| 16 | M04–M06 | Draw nested/group/site splits; explain decomposition and clustering stability |
| 17 | M07–M09 | Interpret connectomes, RDMs and overlapping searchlights |
| 18 | M10–M12 | Defend naturalistic timing, latent-model assumptions and state uncertainty |
| 19 | M13–M15 | Separate state estimation/DCM; check CNN gradients and segmentation evaluation |
| 20 | M16–M18 | Explain pretraining/fine-tuning, attention, calibration and explanation limits |
| 21 | P03 | Report failure at an unseen site alongside baseline and uncertainty |
| 22 | One specialist track below | Complete a full upstream practical with its real environment and data |
| 23 | P04: plan, execute selected supervised scope | Frozen question, metadata, QC, analysis and validation boundaries |
| 24 | Rerun, defend, revise | Independent explanation and reproducible project evidence |

## Required longer practicals

The selected original notebooks in [third_party](../third_party/README.md) are the concrete starting assignments. Work on copies outside the preserved source tree. Record what you actually executed; an upstream notebook containing incomplete student code is an exercise, not a ready result.

During the relevant weeks complete at least:

- **Processing:** Complete **all five guided blocks** in the [processing coverage map](processing_coverage.md): geometry/fMRI alignment, structural morphometry, cortical surfaces, diffusion, and reproducible workflow/QC. These use Nipype, FSL, FreeSurfer and DIPY materials and add roughly 19–29 hours plus compute. Spread them across weeks 6–11 and extend the schedule where needed. Choosing only one specialist track does not complete the full processing strand.
- **Design:** both Poldrack efficiency notebooks as conceptual/source walkthroughs, plus a current working reconstruction of the central experiment; DartBrains resampling exercises. Historical dependencies may require the upstream environment rather than this core environment.
- **Data science:** Neuromatch MSE/MLE and geometric-basis notebooks; assigned Data 8 chapters in the original reader. Continue through the Neuromatch dimensionality-reduction day for full PCA work.
- **Modeling:** BrainIAK RSA and ISC, Neuromatch HMM and CNN; choose the most relevant real-data continuation from the modeling coverage map.

## Select a specialist track in week 22

| Track | Required practical and delivered artifact | What remains beyond it |
|---|---|---|
| Structural MRI | Full FreeSurfer workshop subject or assigned FSL structural practical; surfaces/segmentation overlays and QC report | Cohort morphology, longitudinal pipelines, pathology-specific validation |
| Task fMRI | Full FSL FEAT or equivalent documented preprocessing/model practical; design, confounds, alignment, residual and inference audit | New study acquisition and independent group replication |
| Diffusion | DIPY reconstruction/tractography plus documented real-data preprocessing; gradients, tensor/ODF, tractogram and failure analysis | Biological validation of pathways and cohort connectome inference |
| Naturalistic/connectivity | BrainIAK/Dartmouth real dataset; timing/alignment, ISC or connectivity, correct independent validation | Full SRM/hyperalignment or population inference unless separately completed |
| Imaging machine learning | Real imaging input and label contract; participant/site split, baseline, preprocessing inside validation, model card | Large pretrained checkpoint or 3D network validation unless actually run |

Week 22 adds project-specific depth after the five processing blocks; it does not replace those blocks. Use extra weeks if tools, data or mentoring require more time. These tracks develop depth rather than pretending every specialist workflow has been completed. Finish the shared mechanics across strands, then pursue the methods the actual research question requires. The supervisor decides whether real-data competence is sufficient to progress.
