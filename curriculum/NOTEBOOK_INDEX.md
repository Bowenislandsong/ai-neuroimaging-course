# Every class

Use the [study sequence](STUDY_PLAN.md) to interleave the strands. Each link opens the actual lesson, not a placeholder. Offline notebooks include executed reference outputs; P02 requires its public-data download. [Setup](SETUP.md) · [AI workflow](AI_WORKFLOW.md) · [Assessments](ASSESSMENT.md)

## Foundations

| ID | Class | Execution |
|---|---|---|
| F01 | [What the AI does and what you must understand](../notebooks/00_foundations/01_learning_contract.ipynb) | offline |
| F02 | [From tissue to MRI contrast to BOLD](../notebooks/00_foundations/02_measurement_bridge.ipynb) | offline |
| F03 | [Read a snippet without becoming a software engineer](../notebooks/00_foundations/03_snippet_literacy.ipynb) | offline |
| F04 | [A notebook is an experiment with state](../notebooks/00_foundations/04_notebook_environment.ipynb) | offline |

## Processing

| ID | Class | Execution |
|---|---|---|
| PR01 | [Read an image without losing its location](../notebooks/01_processing/01_images_coordinates_metadata.ipynb) | offline |
| PR02 | [Estimate alignment, then choose how to sample](../notebooks/01_processing/02_registration_resampling.ipynb) | offline |
| PR03 | [Read a deformation field and detect folding](../notebooks/01_processing/03_nonlinear_warps.ipynb) | offline |
| PR04 | [Separate smooth intensity bias from tissue contrast](../notebooks/01_processing/04_bias_field.ipynb) | offline |
| PR05 | [A brain mask defines what the analysis can see](../notebooks/01_processing/05_brain_extraction.ipynb) | offline |
| PR06 | [Labels, posterior probabilities and partial volume are different](../notebooks/01_processing/06_tissue_segmentation.ipynb) | offline |
| PR07 | [Measure volume before making an atrophy claim](../notebooks/01_processing/07_morphometry_volume_jacobian.ipynb) | offline |
| PR08 | [Surfaces are meshes, not thin voxel masks](../notebooks/01_processing/08_surfaces_topology.ipynb) | offline |
| PR09 | [Correct time sampling without inventing slice metadata](../notebooks/01_processing/09_slice_timing.ipynb) | offline |
| PR10 | [Realign frames and identify what movement correction cannot repair](../notebooks/01_processing/10_motion.ipynb) | offline |
| PR11 | [Separate geometric unwarping from signal recovery](../notebooks/01_processing/11_susceptibility_distortion.ipynb) | offline |
| PR12 | [Choose a spatial scale and inspect boundaries](../notebooks/01_processing/12_spatial_smoothing.ipynb) | offline |
| PR13 | [Design a temporal filter using actual sampling](../notebooks/01_processing/13_temporal_filters.ipynb) | offline |
| PR14 | [Remove a modeled nuisance contribution without declaring the residual pure](../notebooks/01_processing/14_nuisance_ica.ipynb) | offline |
| PR15 | [Connect QC decisions to time, coverage and study design](../notebooks/01_processing/15_qc_censoring.ipynb) | offline |
| PR16 | [Keep diffusion volumes and gradient directions together](../notebooks/01_processing/16_diffusion_gradients.ipynb) | offline |
| PR17 | [Separate denoising, Gibbs removal, eddy correction and interpolation](../notebooks/01_processing/17_diffusion_preprocessing.ipynb) | offline |
| PR18 | [Fit a tensor and interpret FA and MD within its limits](../notebooks/01_processing/18_diffusion_tensor.ipynb) | offline |
| PR19 | [A streamline is a model trajectory, not an axon](../notebooks/01_processing/19_crossing_fibers_tractography.ipynb) | offline |
| PR20 | [Extract region signals with coverage and confounds visible](../notebooks/01_processing/20_parcellations_connectivity.ipynb) | offline |
| PR21 | [Audit the complete processing graph and its evidence](../notebooks/01_processing/21_workflow_provenance_reports.ipynb) | offline |

## Research design

| ID | Class | Execution |
|---|---|---|
| D01 | [The question is an estimand, not a button](../notebooks/02_design/01_questions_estimands_causality.ipynb) | offline |
| D02 | [Sampling, missingness, and the people behind rows](../notebooks/02_design/02_sampling_missingness_units.ipynb) | offline |
| D03 | [Reliability is about differences between people](../notebooks/02_design/03_reliability_measurement.ipynb) | offline |
| D04 | [Plan sample size from effects and precision](../notebooks/02_design/04_power_precision.ipynb) | offline |
| D05 | [Event logs, blocks, convolution, and scan sampling](../notebooks/02_design/05_block_event_hrf.ipynb) | offline |
| D06 | [Let the response shape vary: FIR versus a fixed HRF](../notebooks/02_design/06_fir_hrf_misspecification.ipynb) | offline |
| D07 | [Efficiency belongs to a contrast](../notebooks/02_design/07_design_efficiency.ipynb) | offline |
| D08 | [Factorial questions and the meaning of an interaction](../notebooks/02_design/08_factorial_confounding.ipynb) | offline |
| D09 | [From coefficients to a defensible contrast](../notebooks/02_design/09_glm_contrasts_inference.ipynb) | offline |
| D10 | [Correlated residuals and prewhitening](../notebooks/02_design/10_temporal_noise_prewhitening.ipynb) | offline |
| D11 | [People, runs, visits, and hierarchical uncertainty](../notebooks/02_design/11_group_hierarchy_repeated.ipynb) | offline |
| D12 | [Permutation tests must preserve the experiment](../notebooks/02_design/12_permutation_exchangeability.ipynb) | offline |
| D13 | [Voxel families, clusters, and TFCE are different targets](../notebooks/02_design/13_multiplicity_clusters_tfce.ipynb) | offline |
| D14 | [Region selection and evaluation must be independent](../notebooks/02_design/14_roi_selection_circularity.ipynb) | offline |
| D15 | [Intervals, Bayesian updating, and meaningful effects](../notebooks/02_design/15_bayesian_intervals_equivalence.ipynb) | offline |
| D16 | [Make analytical choices visible before publication](../notebooks/02_design/16_multiverse_prereg_reproducibility.ipynb) | offline |

## Data science

| ID | Class | Execution |
|---|---|---|
| DS01 | [Arrays, axes, broadcasting, and masks](../notebooks/03_data_science/01_arrays_axes.ipynb) | offline |
| DS02 | [Participant identity, tidy tables, and join cardinality](../notebooks/03_data_science/02_tables_identity.ipynb) | offline |
| DS03 | [NIfTI file contracts, metadata, and precision](../notebooks/03_data_science/03_nifti_io.ipynb) | offline |
| DS04 | [Visual distributions, outliers, and robust summaries](../notebooks/03_data_science/04_eda.ipynb) | offline |
| DS05 | [Missing values, selection, and train-only imputation](../notebooks/03_data_science/05_missingness.ipynb) | offline |
| DS06 | [Probability, conditional evidence, and base rates](../notebooks/03_data_science/06_probability.ipynb) | offline |
| DS07 | [Sampling distributions, dependence, and effective information](../notebooks/03_data_science/07_sampling.ipynb) | offline |
| DS08 | [Bootstrap uncertainty at the right unit](../notebooks/03_data_science/08_bootstrap.ipynb) | offline |
| DS09 | [Standardization, percent signal change, and reference choices](../notebooks/03_data_science/09_standardization.ipynb) | offline |
| DS10 | [Linear algebra: rank, projection, and identifiability](../notebooks/03_data_science/10_projections.ipynb) | offline |
| DS11 | [Likelihood: state the noise model before fitting](../notebooks/03_data_science/11_likelihood.ipynb) | offline |
| DS12 | [Optimization, gradients, and learning rates](../notebooks/03_data_science/12_optimization.ipynb) | offline |
| DS13 | [Regression diagnostics and coefficient instability](../notebooks/03_data_science/13_regression_diagnostics.ipynb) | offline |
| DS14 | [SVD, PCA, compression, and train-only representations](../notebooks/03_data_science/14_pca_svd.ipynb) | offline |
| DS15 | [Feature selection and the full null pipeline](../notebooks/03_data_science/15_selection.ipynb) | offline |
| DS16 | [Reproducible computation and an AI analysis audit](../notebooks/03_data_science/16_reproducibility.ipynb) | offline |

## Modeling

| ID | Class | Execution |
|---|---|---|
| M01 | [What is represented, and in which direction?](../notebooks/04_modeling/01_representations_encoding_decoding.ipynb) | offline |
| M02 | [Ridge, lasso, and logistic models are different commitments](../notebooks/04_modeling/02_regularized_linear_models.ipynb) | offline |
| M03 | [Curved boundaries: SVM kernels and tree ensembles](../notebooks/04_modeling/03_kernels_ensembles.ipynb) | offline |
| M04 | [Nested validation and the limits of site adjustment](../notebooks/04_modeling/04_nested_sites_harmonization.ipynb) | offline |
| M05 | [PCA reconstruction versus ICA source assumptions](../notebooks/04_modeling/05_pca_ica.ipynb) | offline |
| M06 | [Clusters, labels, and stability under changed measurements](../notebooks/04_modeling/06_clustering_stability.ipynb) | offline |
| M07 | [From regional signals to a graph: every edge is a choice](../notebooks/04_modeling/07_connectomes_graphs.ipynb) | offline |
| M08 | [RSA compares relationships, not matching voxel labels](../notebooks/04_modeling/08_rsa_crossvalidated_distances.ipynb) | offline |
| M09 | [Searchlight decoding: a center score describes a neighborhood](../notebooks/04_modeling/09_searchlight.ipynb) | offline |
| M10 | [Shared movies: ISC, temporal encoding, and alignment](../notebooks/04_modeling/10_naturalistic_isc_encoding.ipynb) | offline |
| M11 | [A generative model must reproduce more than a mean](../notebooks/04_modeling/11_generative_latent_models.ipynb) | offline |
| M12 | [Hidden states, emissions, and the meaning of an event](../notebooks/04_modeling/12_hmm_event_segmentation.ipynb) | offline |
| M13 | [Latent dynamics, Kalman updates, and what DCM adds](../notebooks/04_modeling/13_latent_dynamics_dcm.ipynb) | offline |
| M14 | [Train a small convolutional network and check its gradients](../notebooks/04_modeling/14_cnn_backprop_training.ipynb) | offline |
| M15 | [Segmentation, imbalance, Dice, and image-level splits](../notebooks/04_modeling/15_segmentation_losses.ipynb) | offline |
| M16 | [Pretraining, frozen features, and actual fine-tuning](../notebooks/04_modeling/16_selfsupervision_transfer.ipynb) | offline |
| M17 | [Attention transforms tokens; a model card constrains claims](../notebooks/04_modeling/17_attention_foundation_models.ipynb) | offline |
| M18 | [Calibrate probabilities, challenge explanations, preserve the evidence](../notebooks/04_modeling/18_calibration_explanation_reproducibility.ipynb) | offline |

## Projects

| ID | Class | Execution |
|---|---|---|
| P01 | [Inspect a real anatomical template through spatial transformations](../notebooks/05_projects/01_anatomical_workflow.ipynb) | offline |
| P02 | [A real fMRI run: metadata, design, model, and statistical map](../notebooks/05_projects/02_real_fmri_glm.ipynb) | network |
| P03 | [A cohort prediction workflow with an unseen site](../notebooks/05_projects/03_cohort_generalization.ipynb) | offline |
| P04 | [Turn the notebooks into a defensible supervised research plan](../notebooks/05_projects/04_research_defense.ipynb) | offline |
