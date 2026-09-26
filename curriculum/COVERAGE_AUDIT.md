# Curriculum coverage

This map shows where students study each method and what evidence they produce. The course has **83 original notebooks**: 79 computational lessons and projects, and four reading seminars. An [18-paper library](papers/README.md), practical assignments, and [A1–A4 coursework](coursework/PAPER_TO_EXPERIMENT.md) connect the methods to current research.

The four subject areas correspond to image processing, research design, data science, and modeling. The [source registry](SOURCES.md) identifies the university courses, workshops, and software materials used to develop each strand.

## Forms of instruction

- **Reading seminar:** students interpret a figure, identify the study question, and prepare an evidence record for discussion.
- **Computational lesson:** students predict a result, run a focused experiment, inspect diagnostics, and explain a deliberate error.
- **Source practical:** students complete an assigned university or software tutorial with its original data and tools.
- **Specialist extension:** students pursue an advanced method through supervised work and a documented project.

## Subject-area map

| Area | Teaching sources | Classes | Topic map |
|---|---|---:|---|
| Image processing | Berkeley PSYCH214; DartBrains; FSL; FreeSurfer; DIPY; Nipype | 21 | [Processing topics and exercises](processing_coverage.md) |
| Research design | Dartmouth PSYC60; Berkeley PSYCH214; MIT 9.07/9.63; Poldrack teaching notebooks | 16 | [Design topics and exercises](design_coverage.md) |
| Data science | Berkeley Data 8; Neuromatch fitting/geometry; imaging and software references | 16 | [Data science topics and exercises](data_science_coverage.md) |
| Modeling | Neuromatch computational/deep learning; BrainIAK; Dartmouth naturalistic course | 18 | [Modeling topics and exercises](modeling_coverage.md) |

## Practical depth

The table distinguishes work completed in the original notebooks from the advanced work assigned through source practicals and the supervised project. The [verification record](VERIFICATION.md) covers repository execution; student performance is evaluated through the [assessment rubric](ASSESSMENT.md).

| Area | Original notebook work | Specialist practical or project work |
|---|---|---|
| Image transformations | Geometry, resampling, known-transform correction, small registration search, warps/Jacobians, masks, smoothing, filtering, projections, metadata and QC experiments | Full image-based 3D rigid/affine/nonlinear optimization; production motion/distortion correction and pipeline validation |
| Structural/diffusion | Small segmentation/morphometry/surface experiments; gradient frames, tensor fitting, crossing ambiguity and tracking limits | Actual N4/BET/FAST/FreeSurfer/TOPUP/EDDY/CSD/tractography/TBSS pipelines and real-anatomy QC |
| fMRI inference | HRF/FIR/design/contrasts, known-covariance whitening, hierarchy/partial pooling, exchangeable permutation and a 1D TFCE experiment; a real raw-input single-run GLM | Estimated covariance validation, full mixed effects, 3D spatial inference, multiple-run/cohort analysis and independently justified preprocessing |
| Data science | Arrays/tables/files, sampling/missingness demonstrations, bootstrap, likelihood/optimization, regression/PCA/selection, provenance | Full multiple imputation/MNAR sensitivity, advanced probability proofs, large database/distributed workflows |
| Imaging ML | Trained regularized/kernel/ensemble/latent models; grouped/site splits; small real CNN backprop, denoising pretraining and fine-tuning; attention mechanics | Full real-image 3D CNN/segmentation training, external checkpoint inference and validation, robust domain adaptation, deployment |
| Specialized models | HMM filtering, Kalman mechanics, DCM distinction, harmonization/confounding audit | HMM parameter learning, fitted DCM, ComBat/neuroHarmonize, SRM/hyperalignment and population naturalistic inference unless upstream track completed |
| Real data | Packaged anatomical template workflow; downloaded SPM run and explicitly limited GLM | A fully processed research cohort and independently validated biological conclusion |

Future electives could address cellular dynamics, reinforcement learning, visual-perception experiments, advanced probability, and other modalities such as PET, ASL, spectroscopy, EEG/MEG, and histology. The current sequence emphasizes MRI-based processing, research design, data science, and modeling.

## Assessment standard

Students demonstrate mastery by explaining a transformation and its failure conditions, submitting the assigned practical with outputs and quality checks, and defending the interpretation at a checkpoint.

The [study plan](STUDY_PLAN.md) schedules paper discussions, computational lessons, source assignments, and a specialist track. Instructors assess both first-pass and revised evidence records alongside the technical work. The [assessment guide](ASSESSMENT.md) gives the criteria for each checkpoint.
