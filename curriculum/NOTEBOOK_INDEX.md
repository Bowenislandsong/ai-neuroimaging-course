# Every class

**Start with R00–R03 before F01.** Use the [26-week study sequence](STUDY_PLAN.md) to interleave the strands. These 83 notebooks contain 79 computational lessons/projects and four human-assessed reading seminars. The [18-paper library](papers/README.md) supplies exact readings, questions and assignments. Paper links motivate a question; they do not mean each paper implements every local method.

Offline computational notebooks include reference outputs; P02 requires a public-data download. Reading seminars are submitted for discussion and assessment, not marked as executed. [Setup](SETUP.md) · [AI workflow](AI_WORKFLOW.md) · [Assessments](ASSESSMENT.md)

## Paper orientation — start here

| ID | Class | Type | Paper questions |
|---|---|---|---|
| R00 | [Read for the question before the equations](../notebooks/00_paper_orientation/00_how_to_read.ipynb) | reading | [PP01](papers/processing.md#pp01), [PP04](papers/processing.md#pp04), [PD02](papers/design.md#pd02), [PM03](papers/modeling.md#pm03), [PD01](papers/design.md#pd01), [PM05](papers/modeling.md#pm05) |
| R01 | [Why does a scan need a processing workflow?](../notebooks/00_paper_orientation/01_why_processing.ipynb) | reading | [PP01](papers/processing.md#pp01), [PP04](papers/processing.md#pp04) |
| R02 | [When will a brain result work for a new person?](../notebooks/00_paper_orientation/02_why_generalization.ipynb) | reading | [PD02](papers/design.md#pd02), [PM03](papers/modeling.md#pm03) |
| R03 | [Which choices stand between a result and a claim?](../notebooks/00_paper_orientation/03_why_evidence_audits.ipynb) | reading | [PD01](papers/design.md#pd01), [PM05](papers/modeling.md#pm05) |

## Foundations

| ID | Class | Type | Paper questions |
|---|---|---|---|
| F01 | [What the AI does and what you must understand](../notebooks/00_foundations/01_learning_contract.ipynb) | offline | [PD01](papers/design.md#pd01) |
| F02 | [From tissue to MRI contrast to BOLD](../notebooks/00_foundations/02_measurement_bridge.ipynb) | offline | [PB01](papers/measurement.md#pb01) |
| F03 | [Read a snippet without becoming a software engineer](../notebooks/00_foundations/03_snippet_literacy.ipynb) | offline | [PD01](papers/design.md#pd01) |
| F04 | [A notebook is an experiment with state](../notebooks/00_foundations/04_notebook_environment.ipynb) | offline | [PP01](papers/processing.md#pp01), [PD01](papers/design.md#pd01) |

## Processing

| ID | Class | Type | Paper questions |
|---|---|---|---|
| PR01 | [Read an image without losing its location](../notebooks/01_processing/01_images_coordinates_metadata.ipynb) | offline | [PP01](papers/processing.md#pp01), [PP04](papers/processing.md#pp04) |
| PR02 | [Estimate alignment, then choose how to sample](../notebooks/01_processing/02_registration_resampling.ipynb) | offline | [PP04](papers/processing.md#pp04) |
| PR03 | [Read a deformation field and detect folding](../notebooks/01_processing/03_nonlinear_warps.ipynb) | offline | [PP04](papers/processing.md#pp04) |
| PR04 | [Separate smooth intensity bias from tissue contrast](../notebooks/01_processing/04_bias_field.ipynb) | offline | [PP03](papers/processing.md#pp03) |
| PR05 | [A brain mask defines what the analysis can see](../notebooks/01_processing/05_brain_extraction.ipynb) | offline | [PP03](papers/processing.md#pp03) |
| PR06 | [Labels, posterior probabilities and partial volume are different](../notebooks/01_processing/06_tissue_segmentation.ipynb) | offline | [PP03](papers/processing.md#pp03) |
| PR07 | [Measure volume before making an atrophy claim](../notebooks/01_processing/07_morphometry_volume_jacobian.ipynb) | offline | [PP03](papers/processing.md#pp03) |
| PR08 | [Surfaces are meshes, not thin voxel masks](../notebooks/01_processing/08_surfaces_topology.ipynb) | offline | [PP03](papers/processing.md#pp03) |
| PR09 | [Correct time sampling without inventing slice metadata](../notebooks/01_processing/09_slice_timing.ipynb) | offline | [PP01](papers/processing.md#pp01), [PB01](papers/measurement.md#pb01) |
| PR10 | [Realign frames and identify what movement correction cannot repair](../notebooks/01_processing/10_motion.ipynb) | offline | [PP02](papers/processing.md#pp02) |
| PR11 | [Separate geometric unwarping from signal recovery](../notebooks/01_processing/11_susceptibility_distortion.ipynb) | offline | [PP01](papers/processing.md#pp01) |
| PR12 | [Choose a spatial scale and inspect boundaries](../notebooks/01_processing/12_spatial_smoothing.ipynb) | offline | [PP01](papers/processing.md#pp01) |
| PR13 | [Design a temporal filter using actual sampling](../notebooks/01_processing/13_temporal_filters.ipynb) | offline | [PP02](papers/processing.md#pp02), [PB01](papers/measurement.md#pb01) |
| PR14 | [Remove a modeled nuisance contribution without declaring the residual pure](../notebooks/01_processing/14_nuisance_ica.ipynb) | offline | [PP02](papers/processing.md#pp02), [PD01](papers/design.md#pd01) |
| PR15 | [Connect QC decisions to time, coverage and study design](../notebooks/01_processing/15_qc_censoring.ipynb) | offline | [PP02](papers/processing.md#pp02), [PP01](papers/processing.md#pp01) |
| PR16 | [Keep diffusion volumes and gradient directions together](../notebooks/01_processing/16_diffusion_gradients.ipynb) | offline | [PP06](papers/processing.md#pp06) |
| PR17 | [Separate denoising, Gibbs removal, eddy correction and interpolation](../notebooks/01_processing/17_diffusion_preprocessing.ipynb) | offline | [PP06](papers/processing.md#pp06) |
| PR18 | [Fit a tensor and interpret FA and MD within its limits](../notebooks/01_processing/18_diffusion_tensor.ipynb) | offline | [PP06](papers/processing.md#pp06) |
| PR19 | [A streamline is a model trajectory, not an axon](../notebooks/01_processing/19_crossing_fibers_tractography.ipynb) | offline | [PP06](papers/processing.md#pp06) |
| PR20 | [Extract region signals with coverage and confounds visible](../notebooks/01_processing/20_parcellations_connectivity.ipynb) | offline | [PP02](papers/processing.md#pp02), [PP06](papers/processing.md#pp06) |
| PR21 | [Audit the complete processing graph and its evidence](../notebooks/01_processing/21_workflow_provenance_reports.ipynb) | offline | [PP01](papers/processing.md#pp01) |

## Research design

| ID | Class | Type | Paper questions |
|---|---|---|---|
| D01 | [The question is an estimand, not a button](../notebooks/02_design/01_questions_estimands_causality.ipynb) | offline | [PD01](papers/design.md#pd01) |
| D02 | [Sampling, missingness, and the people behind rows](../notebooks/02_design/02_sampling_missingness_units.ipynb) | offline | [PD02](papers/design.md#pd02), [PD06](papers/design.md#pd06) |
| D03 | [Reliability is about differences between people](../notebooks/02_design/03_reliability_measurement.ipynb) | offline | [PD03](papers/design.md#pd03) |
| D04 | [Plan sample size from effects and precision](../notebooks/02_design/04_power_precision.ipynb) | offline | [PD02](papers/design.md#pd02), [PD06](papers/design.md#pd06) |
| D05 | [Event logs, blocks, convolution, and scan sampling](../notebooks/02_design/05_block_event_hrf.ipynb) | offline | [PB01](papers/measurement.md#pb01), [PD03](papers/design.md#pd03) |
| D06 | [Let the response shape vary: FIR versus a fixed HRF](../notebooks/02_design/06_fir_hrf_misspecification.ipynb) | offline | [PB01](papers/measurement.md#pb01) |
| D07 | [Efficiency belongs to a contrast](../notebooks/02_design/07_design_efficiency.ipynb) | offline | [PD06](papers/design.md#pd06), [PD01](papers/design.md#pd01) |
| D08 | [Factorial questions and the meaning of an interaction](../notebooks/02_design/08_factorial_confounding.ipynb) | offline | [PD06](papers/design.md#pd06) |
| D09 | [From coefficients to a defensible contrast](../notebooks/02_design/09_glm_contrasts_inference.ipynb) | offline | [PD01](papers/design.md#pd01) |
| D10 | [Correlated residuals and prewhitening](../notebooks/02_design/10_temporal_noise_prewhitening.ipynb) | offline | [PD05](papers/design.md#pd05) |
| D11 | [People, runs, visits, and hierarchical uncertainty](../notebooks/02_design/11_group_hierarchy_repeated.ipynb) | offline | [PD02](papers/design.md#pd02), [PD06](papers/design.md#pd06) |
| D12 | [Permutation tests must preserve the experiment](../notebooks/02_design/12_permutation_exchangeability.ipynb) | offline | [PD05](papers/design.md#pd05) |
| D13 | [Voxel families, clusters, and TFCE are different targets](../notebooks/02_design/13_multiplicity_clusters_tfce.ipynb) | offline | [PD05](papers/design.md#pd05) |
| D14 | [Region selection and evaluation must be independent](../notebooks/02_design/14_roi_selection_circularity.ipynb) | offline | [PD04](papers/design.md#pd04) |
| D15 | [Intervals, Bayesian updating, and meaningful effects](../notebooks/02_design/15_bayesian_intervals_equivalence.ipynb) | offline | [PD01](papers/design.md#pd01) |
| D16 | [Make analytical choices visible before publication](../notebooks/02_design/16_multiverse_prereg_reproducibility.ipynb) | offline | [PD01](papers/design.md#pd01) |

## Data science

| ID | Class | Type | Paper questions |
|---|---|---|---|
| DS01 | [Arrays, axes, broadcasting, and masks](../notebooks/03_data_science/01_arrays_axes.ipynb) | offline | [PP01](papers/processing.md#pp01), [PM05](papers/modeling.md#pm05) |
| DS02 | [Participant identity, tidy tables, and join cardinality](../notebooks/03_data_science/02_tables_identity.ipynb) | offline | [PD02](papers/design.md#pd02) |
| DS03 | [NIfTI file contracts, metadata, and precision](../notebooks/03_data_science/03_nifti_io.ipynb) | offline | [PP01](papers/processing.md#pp01) |
| DS04 | [Visual distributions, outliers, and robust summaries](../notebooks/03_data_science/04_eda.ipynb) | offline | [PD02](papers/design.md#pd02) |
| DS05 | [Missing values, selection, and train-only imputation](../notebooks/03_data_science/05_missingness.ipynb) | offline | [PD02](papers/design.md#pd02), [PM03](papers/modeling.md#pm03) |
| DS06 | [Probability, conditional evidence, and base rates](../notebooks/03_data_science/06_probability.ipynb) | offline | [PM03](papers/modeling.md#pm03) |
| DS07 | [Sampling distributions, dependence, and effective information](../notebooks/03_data_science/07_sampling.ipynb) | offline | [PD02](papers/design.md#pd02) |
| DS08 | [Bootstrap uncertainty at the right unit](../notebooks/03_data_science/08_bootstrap.ipynb) | offline | [PD02](papers/design.md#pd02) |
| DS09 | [Standardization, percent signal change, and reference choices](../notebooks/03_data_science/09_standardization.ipynb) | offline | [PB01](papers/measurement.md#pb01) |
| DS10 | [Linear algebra: rank, projection, and identifiability](../notebooks/03_data_science/10_projections.ipynb) | offline | [PD03](papers/design.md#pd03) |
| DS11 | [Likelihood: state the noise model before fitting](../notebooks/03_data_science/11_likelihood.ipynb) | offline | [PD02](papers/design.md#pd02) |
| DS12 | [Optimization, gradients, and learning rates](../notebooks/03_data_science/12_optimization.ipynb) | offline | [PP04](papers/processing.md#pp04) |
| DS13 | [Regression diagnostics and coefficient instability](../notebooks/03_data_science/13_regression_diagnostics.ipynb) | offline | [PD02](papers/design.md#pd02) |
| DS14 | [SVD, PCA, compression, and train-only representations](../notebooks/03_data_science/14_pca_svd.ipynb) | offline | [PM02](papers/modeling.md#pm02), [PM03](papers/modeling.md#pm03) |
| DS15 | [Feature selection and the full null pipeline](../notebooks/03_data_science/15_selection.ipynb) | offline | [PD04](papers/design.md#pd04) |
| DS16 | [Reproducible computation and an AI analysis audit](../notebooks/03_data_science/16_reproducibility.ipynb) | offline | [PD01](papers/design.md#pd01), [PP01](papers/processing.md#pp01) |

## Modeling

| ID | Class | Type | Paper questions |
|---|---|---|---|
| M01 | [What is represented, and in which direction?](../notebooks/04_modeling/01_representations_encoding_decoding.ipynb) | offline | [PM01](papers/modeling.md#pm01) |
| M02 | [Ridge, lasso, and logistic models are different commitments](../notebooks/04_modeling/02_regularized_linear_models.ipynb) | offline | [PM01](papers/modeling.md#pm01), [PM03](papers/modeling.md#pm03) |
| M03 | [Curved boundaries: SVM kernels and tree ensembles](../notebooks/04_modeling/03_kernels_ensembles.ipynb) | offline | [PM04](papers/modeling.md#pm04) |
| M04 | [Nested validation and the limits of site adjustment](../notebooks/04_modeling/04_nested_sites_harmonization.ipynb) | offline | [PM03](papers/modeling.md#pm03), [PD02](papers/design.md#pd02) |
| M05 | [PCA reconstruction versus ICA source assumptions](../notebooks/04_modeling/05_pca_ica.ipynb) | offline | [PM02](papers/modeling.md#pm02) |
| M06 | [Clusters, labels, and stability under changed measurements](../notebooks/04_modeling/06_clustering_stability.ipynb) | offline | [PD03](papers/design.md#pd03) |
| M07 | [From regional signals to a graph: every edge is a choice](../notebooks/04_modeling/07_connectomes_graphs.ipynb) | offline | [PP06](papers/processing.md#pp06), [PP02](papers/processing.md#pp02) |
| M08 | [RSA compares relationships, not matching voxel labels](../notebooks/04_modeling/08_rsa_crossvalidated_distances.ipynb) | offline | [PM02](papers/modeling.md#pm02) |
| M09 | [Searchlight decoding: a center score describes a neighborhood](../notebooks/04_modeling/09_searchlight.ipynb) | offline | [PM02](papers/modeling.md#pm02), [PD04](papers/design.md#pd04) |
| M10 | [Shared movies: ISC, temporal encoding, and alignment](../notebooks/04_modeling/10_naturalistic_isc_encoding.ipynb) | offline | [PM01](papers/modeling.md#pm01), [PD03](papers/design.md#pd03) |
| M11 | [A generative model must reproduce more than a mean](../notebooks/04_modeling/11_generative_latent_models.ipynb) | offline | [PM01](papers/modeling.md#pm01) |
| M12 | [Hidden states, emissions, and the meaning of an event](../notebooks/04_modeling/12_hmm_event_segmentation.ipynb) | offline | [PM01](papers/modeling.md#pm01) |
| M13 | [Latent dynamics, Kalman updates, and what DCM adds](../notebooks/04_modeling/13_latent_dynamics_dcm.ipynb) | offline | [PB01](papers/measurement.md#pb01), [PM01](papers/modeling.md#pm01) |
| M14 | [Train a small convolutional network and check its gradients](../notebooks/04_modeling/14_cnn_backprop_training.ipynb) | offline | [PM03](papers/modeling.md#pm03), [PM04](papers/modeling.md#pm04) |
| M15 | [Segmentation, imbalance, Dice, and image-level splits](../notebooks/04_modeling/15_segmentation_losses.ipynb) | offline | [PP03](papers/processing.md#pp03), [PM03](papers/modeling.md#pm03) |
| M16 | [Pretraining, frozen features, and actual fine-tuning](../notebooks/04_modeling/16_selfsupervision_transfer.ipynb) | offline | [PM03](papers/modeling.md#pm03), [PM04](papers/modeling.md#pm04) |
| M17 | [Attention transforms tokens; a model card constrains claims](../notebooks/04_modeling/17_attention_foundation_models.ipynb) | offline | [PM05](papers/modeling.md#pm05) |
| M18 | [Calibrate probabilities, challenge explanations, preserve the evidence](../notebooks/04_modeling/18_calibration_explanation_reproducibility.ipynb) | offline | [PM03](papers/modeling.md#pm03), [PM04](papers/modeling.md#pm04) |

## Projects

| ID | Class | Type | Paper questions |
|---|---|---|---|
| P01 | [Inspect a real anatomical template through spatial transformations](../notebooks/05_projects/01_anatomical_workflow.ipynb) | offline | [PP01](papers/processing.md#pp01), [PP04](papers/processing.md#pp04) |
| P02 | [A real fMRI run: metadata, design, model, and statistical map](../notebooks/05_projects/02_real_fmri_glm.ipynb) | network | [PP01](papers/processing.md#pp01), [PD01](papers/design.md#pd01), [PB01](papers/measurement.md#pb01) |
| P03 | [A cohort prediction workflow with an unseen site](../notebooks/05_projects/03_cohort_generalization.ipynb) | offline | [PD02](papers/design.md#pd02), [PM03](papers/modeling.md#pm03) |
| P04 | [Turn the notebooks into a defensible supervised research plan](../notebooks/05_projects/04_research_defense.ipynb) | offline | [PD01](papers/design.md#pd01), [PM03](papers/modeling.md#pm03) |
