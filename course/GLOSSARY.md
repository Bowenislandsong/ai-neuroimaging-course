# Words she needs to explain

| Term | Working meaning |
| --- | --- |
| Voxel | A small volume represented by one stored sample; not necessarily one tissue type. |
| Affine | A matrix mapping between coordinates; a NIfTI image affine relates voxel indices to world coordinates. |
| Mask | A selection or weighting of spatial locations; may be binary, labeled, or probabilistic. |
| Atlas | A spatial reference defining regions or probabilities, in a declared coordinate space. |
| Registration | Estimating a spatial correspondence between images. |
| Resampling | Evaluating an image on an output grid using a mapping and interpolation. |
| Interpolation | Estimating values between stored samples. |
| FWHM | Full width at half maximum; a way to specify Gaussian smoothing width. |
| TR / TE | Acquisition timing parameters; check units and sequence context. |
| BOLD | Blood-oxygenation-sensitive contrast used as an indirect measure in fMRI. |
| HRF | A model of a hemodynamic response over time. |
| Confound | A factor that can distort interpretation of an association; not every covariate is a confound. |
| Nuisance regressor | A design column included to model unwanted variation. |
| Residual | Observed minus model-fitted value. |
| Estimand | The precisely defined quantity the study aims to estimate. |
| Design matrix | Columns representing predictors/model terms and rows representing observations. |
| Contrast | Weights selecting a question about model coefficients. |
| Effect estimate | Estimated magnitude of a relationship, with units where applicable. |
| Standard deviation | Spread of values around their center. |
| Standard error | Uncertainty scale of an estimator under stated assumptions. |
| p value | Under the null model, probability of a statistic at least as extreme as the observed one; not the probability the null is true. |
| FDR | Expected false-discovery proportion under the procedure's assumptions; not an error probability for each voxel. |
| Leakage | Information entering training/model selection that should have remained unavailable for the stated evaluation. |
| Baseline | A simple comparison method that a proposed model should justify improving upon. |
| Calibration | Agreement between predicted probabilities and observed frequencies in the evaluated population. |
| Domain shift | A relevant change between training and application data, such as scanner, site, or population. |
| Embedding | A numerical representation produced by an encoder. |
| Frozen encoder | A pretrained representation model whose weights are not updated in downstream training. |
| Fine-tuning | Updating pretrained weights using a downstream training dataset. |
| Provenance | A traceable record of data sources, transformations, versions, and decisions. |
