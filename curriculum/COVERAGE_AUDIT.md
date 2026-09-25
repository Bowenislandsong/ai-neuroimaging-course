# Coverage audit: scope, depth, and omissions

The first 24-class pack was an introduction. This expanded edition has **71 strand notebooks plus 4 foundations and 4 projects**, a complete class sequence, code, failure exercises, AI prompts, answer guides and named upstream assignments. Notebook count is not a measure of degree equivalence.

**We cannot honestly claim every topic in all four USC syllabi:** detailed public NIIN 540/520/580/550 syllabi were not located. What we can audit is the coverage of specific topics in the parallel public curricula we inspected. The [source registry](SOURCES.md) separates dated university syllabi from course repositories, workshops and documentation.

## Evidence levels

- **Worked locally:** original explanation, executable experiment, prediction, numerical/visual inspection, deliberate error, repair and transfer question. The delivered Jupyter run checks execution, not learner mastery.
- **Guided source practical:** an exact existing course/tutorial assignment and required submission, with its original environment/data. Its inclusion does not mean it has been run.
- **Conceptual boundary:** a method is explained and contrasted with related methods, but the full estimator or pipeline is not implemented locally.
- **Outside scope:** additional specialist teaching is required; mention of a topic does not count as full instruction.

## Crosswalk for the four requested areas

| USC subject-area inspiration | Actual course anchors | Local class count | Detailed audit |
|---|---|---:|---|
| NIIN 540 processing | Berkeley PSYCH214; DartBrains; FSL; FreeSurfer; DIPY; Nipype | 21 | [Every processing topic, check, source and limitation](processing_coverage.md) |
| NIIN 520 design | Dartmouth PSYC60; Berkeley PSYCH214; MIT 9.07/9.63; Poldrack teaching notebooks | 16 | [Every design topic, check, source and limitation](design_coverage.md) |
| NIIN 580 data science | Berkeley Data 8; Neuromatch fitting/geometry; official imaging/software references | 16 | [Every data-science topic, check, source and limitation](data_science_coverage.md) |
| NIIN 550 modeling | Neuromatch computational/deep learning; BrainIAK; Dartmouth naturalistic course | 18 | [Every modeling topic, check, source and limitation](modeling_coverage.md) |

## Important depth boundaries

| Area | What is genuinely implemented here | What still requires the upstream/supervised work |
|---|---|---|
| Image transformations | Geometry, resampling, known-transform correction, small registration search, warps/Jacobians, masks, smoothing, filtering, projections, metadata and QC experiments | Full image-based 3D rigid/affine/nonlinear optimization; production motion/distortion correction and pipeline validation |
| Structural/diffusion | Small segmentation/morphometry/surface experiments; gradient frames, tensor fitting, crossing ambiguity and tracking limits | Actual N4/BET/FAST/FreeSurfer/TOPUP/EDDY/CSD/tractography/TBSS pipelines and real-anatomy QC |
| fMRI inference | HRF/FIR/design/contrasts, known-covariance whitening, hierarchy/partial pooling, exchangeable permutation and a 1D TFCE experiment; a real raw-input single-run GLM | Estimated covariance validation, full mixed effects, 3D spatial inference, multiple-run/cohort analysis and independently justified preprocessing |
| Data science | Arrays/tables/files, sampling/missingness demonstrations, bootstrap, likelihood/optimization, regression/PCA/selection, provenance | Full multiple imputation/MNAR sensitivity, advanced probability proofs, large database/distributed workflows |
| Imaging ML | Trained regularized/kernel/ensemble/latent models; grouped/site splits; small real CNN backprop, denoising pretraining and fine-tuning; attention mechanics | Full real-image 3D CNN/segmentation training, external checkpoint inference and validation, robust domain adaptation, deployment |
| Specialized models | HMM filtering, Kalman mechanics, DCM distinction, harmonization/confounding audit | HMM parameter learning, fitted DCM, ComBat/neuroHarmonize, SRM/hyperalignment and population naturalistic inference unless upstream track completed |
| Real data | Packaged anatomical template workflow; downloaded SPM run and explicitly limited GLM | A fully processed research cohort and independently validated biological conclusion |

Broader topics found in the source curricula—cellular dynamics, reinforcement learning, extensive visual-perception experiments, full probability theory—and imaging modalities such as PET, ASL, spectroscopy, EEG/MEG and histology are not silently counted as covered. The original user scope focuses on neuroimaging processing/design/data science/modeling, with an MRI emphasis. Those extensions need additional classes if the research question requires them.

## Completion rule

For a topic to be “learned,” the student must explain its transformation and failure, complete the named transfer artifact, and pass the relevant checkpoint. For a full-tool practical to be “completed,” she must use its actual environment/data, retain QC and outputs, and defend the interpretation. A course can supply the material and checks; it cannot pre-complete a learner's supervised competence.

The [24-week plan](STUDY_PLAN.md) includes source assignments and a specialist track. Completing only the small local experiments is a broad conceptual and computational foundation, not completion of every source curriculum. See [assessment](ASSESSMENT.md) for independent performance criteria.
