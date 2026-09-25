# What each transformation actually changes

This is an original quick reference. Use it to ask a better AI question; it is not a default pipeline order. Choices depend on the acquisition, question, and downstream model.

| Operation | Input → output | What changes / can be lost | What to inspect |
| --- | --- | --- | --- |
| Reorientation | image + affine → reordered axes + updated affine | Storage order; physical locations should be preserved if done correctly | World coordinates, orientation labels, affine, left/right landmarks |
| Registration | moving and fixed images → estimated spatial mapping | Estimated correspondence; rigid preserves shape, affine permits global scaling/shear, nonlinear permits local deformation | Overlay boundaries; transformation direction, reference space, deformation plausibility |
| Resampling | image + mapping + output grid → samples on new grid | Values through interpolation; no creation of measured spatial resolution | Grid/affine, coverage, labels vs continuous data, interpolation, repeated interpolation |
| Spatial smoothing | image + kernel → local weighted averages | Blurs detail and mixes nearby tissues; may increase useful signal-to-noise for some targets | FWHM in mm, voxel conversion, common display limits, edge/ROI contamination |
| Temporal filtering | sampled series + TR + filter → attenuated frequency components | Some signal and noise frequencies removed; edge effects and changed dependence | Hz vs seconds, Nyquist, task frequencies, spectral comparison, filtered regressors |
| Nuisance regression | signal + nuisance design → residual signal | Removes the modeled subspace, including shared biological variance | Design rank, confound selection, residual associations, signal loss, filter compatibility |
| Z standardization | values + reference mean/SD → dimensionless values | Absolute scale and offset removed; distribution shape largely retained | Axis, reference sample, ddof, zero variance, training-only fitting where applicable |
| ROI extraction | aligned image/time series + mask → region summary | Spatial detail collapsed; mixtures depend on ROI | Coordinate match, independent ROI definition, coverage, averaging weights |
| GLM fit | measurements + design → coefficients/residuals | Decomposes according to chosen model; interpretation depends on design | Column names/rank, units, nuisance choices, noise assumptions |
| Contrast | coefficients + weights → targeted effect estimate | Selects a question; combines specified coefficients | Exact column order, sign, effect units, estimability |
| Statistical map | estimate + uncertainty/null assumptions → statistic or p values | Expresses evidence under a model; not an effect magnitude | Type of map, degrees of freedom, multiplicity family, model validity |
| Thresholding | map + rule → displayed/retained values | Hides information; apparent boundaries depend on rule | Unthresholded map, threshold type, correction, predefined rule |
| Feature scaling/PCA | training features → fitted transform → train/test representation | Changes scale or reduces dimensions; can discard informative variation | Fit inside training folds; retained variance not equivalent to biological validity |
| CNN convolution | image + learned/local kernel → feature maps | Encodes local patterns; downsampling may lose spatial precision | Dimensions, physical resolution, training provenance, shifted inputs |
| Foundation-model encoder | modality-compatible input + pretrained weights → features/prediction | Carries pretraining assumptions; may encode nuisance/domain factors | License, input contract, pretraining cohort, overlap, frozen vs tuned, external validation |

“Normalization” is ambiguous. Ask whether the speaker means spatial normalization to a template, intensity scaling, feature standardization, or something else. A preprocessing step can be appropriate in one experiment and harmful in another.

Read the supporting primary references in [the materials ledger](SOURCES.md) and the block-specific source files before using a method on real data.
