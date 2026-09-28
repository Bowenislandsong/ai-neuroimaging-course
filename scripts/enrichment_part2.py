#!/usr/bin/env python3
"""Part 2 of course enrichment data: DS01-DS16, M01-M18, P01-P04, plus Wikimedia Commons resolution."""
from pathlib import Path
import json
import urllib.parse
import urllib.request
from enrichment_part1 import SCHEDULE_MAP, ENRICHMENT_PART1

ROOT = Path(__file__).resolve().parents[1]

ENRICHMENT_PART2 = {
    "DS01": {
        "commons_file": "File:Components_stress_tensor.svg",
        "diagram_title": "4D Neuroimaging Tensor Axes, Memory Strides, Broadcasting & Boolean Brain Masks",
        "diagram_guide": "A 4D fMRI array has shape (X, Y, Z, T). Applying a 3D boolean brain mask M of shape (X, Y, Z) compresses the spatial dimensions into a 2D matrix X_masked of shape (V_brain, T). Confusing C-order reshape with transpose scrambles spatial and temporal axes!",
        "pipeline_steps": ["4D Volume (X, Y, Z, T)", "Apply 3D Boolean Mask M(X,Y,Z)", "2D Voxel-by-Time Matrix (V, T)", "Axis-Explicit Broadcasting (keepdims)", "Unmask Back to 3D/4D Brain Grid"],
        "equation": {
            "name": "Boolean Mask Indexing & Stride-Aware Tensor Broadcasting",
            "latex": r"Y_{\text{masked}} = \mathcal{M}(Y_{X\times Y\times Z\times T}, M_{X\times Y\times Z}) \in \mathbb{R}^{V_{\text{brain}} \times T}, \qquad \text{offset}(i_0,\dots,i_{d-1}) = \sum_{k=0}^{d-1} s_k \, i_k",
            "summary": "Maps a 4D volume through a 3D spatial mask into a 2D (V_brain, T) matrix and tracks byte stride offsets across array views.",
            "terms": [
                {"term": r"M_{X\times Y\times Z} \in \{0,1\}^{X\times Y\times Z}", "role": "3D Spatial Brain Mask", "meaning": "Boolean array selecting the V_brain = sum(M) in-brain voxels in a deterministic C-order traversal.", "failure": "Flattening with Fortran order ('F') on mask extraction and C order ('C') on reconstruction, scrambling brain anatomy."},
                {"term": r"\mathbb{R}^{V_{\text{brain}} \times T}", "role": "Masked Voxel-by-Time Matrix", "meaning": "Each row is one in-brain voxel's time series; each column is one volume across the brain mask.", "failure": "Calling .reshape(T, V) instead of .T to transpose a (V, T) matrix, mixing time points across different voxels."},
                {"term": r"\sum_{k=0}^{d-1} s_k \, i_k", "role": "Memory Byte-Stride Offset", "meaning": "Computes exact RAM address from index tuple i_k and byte strides s_k without copying array buffers.", "failure": "Subtracting a 1D vector of length V from a (V, T) matrix without [:, None] or keepdims=True."}
            ]
        }
    },
    "DS02": {
        "commons_file": "File:Comparison_of_join_algorithms.png",
        "diagram_title": "Relational BIDS Tables, Composite Keys (sub + ses + run) & Many-to-Many Join Explosions",
        "diagram_guide": "Neuroimaging cohorts store demographics in participants.tsv (1 row per person), clinical visits in sessions.tsv (1 row per visit), and QC metrics per run. Joining two multi-row tables on participant_id alone—without session_id—creates a Cartesian many-to-many row explosion that duplicates participants!",
        "pipeline_steps": ["Verify Primary Key Uniqueness", "Normalize ID Strings (sub-01)", "Specify Composite Key (sub, ses)", "Execute Merge with validate='1:m'", "Audit Unmatched / Orphaned Subjects"],
        "equation": {
            "name": "Relational Join Cardinality & Many-to-Many Cartesian Multiplication",
            "latex": r"|A \bowtie_{K} B| = \sum_{k \in K(A) \cap K(B)} n_A(k) \cdot n_B(k), \qquad \text{Valid } 1\text{:}m \iff \forall k, \; n_A(k) = 1",
            "summary": "Proves why joining two tables that both have multiple rows per key k multiplies row counts to n_A(k) * n_B(k) unless constrained by a composite key.",
            "terms": [
                {"term": r"K = (\text{participant\_id}, \text{session\_id})", "role": "Composite Relational Join Key", "meaning": "Uniquely identifies the observational unit across longitudinal visits and runs.", "failure": "Joining longitudinal behavioral sessions to longitudinal MRI scans on participant_id alone, cross-pairing Baseline with Year-2 visits."},
                {"term": r"n_A(k) \cdot n_B(k)", "role": "Row-Count Product per Key", "meaning": "If participant k has 3 sessions in table A and 3 scans in table B, an unkeyed join fabricates 3*3 = 9 rows for that person.", "failure": "Omitting validate='one_to_one' or 'one_to_many' in pd.merge, silently duplicating clinical subjects."},
                {"term": r"K(A) \cap K(B)", "role": "Inner vs. Left Join Overlap", "meaning": "Subjects whose ID formatting ('sub-01' vs '01' vs 'sub-1 ') mismatches are silently dropped by an inner join.", "failure": "Losing 20% of a cohort to trailing whitespace or zero-padding mismatches in subject IDs."}
            ]
        }
    },
    "DS03": {
        "commons_file": "File:Float_example.svg",
        "diagram_title": "NIfTI-1 Binary File Contracts, IEEE-754 Floating-Point Precision & Header Scaling (scl_slope)",
        "diagram_guide": "A NIfTI file stores raw disk integers (e.g., int16) plus affine metadata (sform/qform) and intensity scaling factors (scl_slope, scl_inter). Casting float32/float64 statistical maps or high-dynamic-range signals to int16 without scaling truncates fractional values to zero!",
        "pipeline_steps": ["Inspect Disk dtype & Shape", "Apply Header Scaling: m * Y_raw + b", "Verify sform_code & qform_code", "Compute in float32 / float64", "Save with Explicit Affine & Header"],
        "equation": {
            "name": "NIfTI Header Intensity Affine Scaling & Quantization Error Bound",
            "latex": r"I_{\text{true}}(\mathbf{i}) = \underbrace{\text{scl\_slope}}_{m} \cdot I_{\text{disk}}(\mathbf{i}) + \underbrace{\text{scl\_inter}}_{b}, \qquad |\varepsilon_{\text{quant}}| \le \frac{|m|}{2}",
            "summary": "Reconstructs physical floating-point voxel values from compact on-disk integer arrays via the NIfTI header slope and intercept.",
            "terms": [
                {"term": r"I_{\text{disk}}(\mathbf{i}) \in \mathbb{Z}", "role": "Raw Stored Array Buffer", "meaning": "Unscaled integer or float voxel values stored on disk (accessed raw via img.dataobj.get_unscaled()).", "failure": "Reading raw unscaled bytes directly while ignoring session-specific scl_slope variations across scanner runs."},
                {"term": r"\text{scl\_slope } (m), \; \text{scl\_inter } (b)", "role": "Header Linear Rescaling Factors", "meaning": "Applied automatically by img.get_fdata() to restore physical intensity or probability ranges.", "failure": "Writing floating-point probability maps (0.0 to 1.0) into an integer NIfTI header with scl_slope=1, truncating all probabilities < 1 to 0!"},
                {"term": r"\text{float32 vs. float64}", "role": "IEEE-754 Mantissa Precision", "meaning": "float32 provides 24 bits (~7 decimal digits) of significand precision; accumulating millions of voxel sums in float16/float32 can suffer catastrophic cancellation.", "failure": "Using low-precision accumulators for whole-brain variance or Gram matrix calculations."}
            ]
        }
    },
    "DS04": {
        "commons_file": "File:Boxplot_vs_PDF-be.svg",
        "diagram_title": "Exploratory Data Analysis (EDA), Heavy-Tailed Artifacts & Robust Summaries (Median / MAD / IQR)",
        "diagram_guide": "Neuroimaging quality metrics (FD, DVARS) and small-ROI summaries often contain extreme motion spikes or registration outliers. A single corrupted volume can shift the sample mean and explode the standard deviation (breakdown point 0%), whereas the median, IQR, and scaled MAD remain stable up to 50% contamination.",
        "pipeline_steps": ["Plot Full Distribution (Raincloud / Histogram)", "Compare Mean/SD vs. Median/MAD", "Compute Robust z-Score z_rob", "Inspect Flagged Scans Visually", "Compare OLS vs. Huber Robust Fit"],
        "equation": {
            "name": "Gaussian-Consistent Median Absolute Deviation (MAD) & Robust Z-Score",
            "latex": r"\text{MAD}(\mathbf{x}) = \operatorname{median}\!\big(|x_i - \operatorname{median}(\mathbf{x})|\big), \qquad \hat{\sigma}_{\text{MAD}} = 1.4826 \cdot \text{MAD}(\mathbf{x}), \qquad z_{\text{rob}, i} = \frac{x_i - \operatorname{median}(\mathbf{x})}{1.4826 \cdot \text{MAD}(\mathbf{x})}",
            "summary": "Estimates dispersion via the median distance from the median, scaled by 1 / Phi^{-1}(0.75) = 1.4826 to match standard deviation under a Gaussian distribution.",
            "terms": [
                {"term": r"\operatorname{median}(\mathbf{x})", "role": "50%-Breakdown Location Estimator", "meaning": "Middle order statistic unaffected by extreme motion or hardware spike values in either tail.", "failure": "Reporting only bar charts of sample means +/- SEM, which conceal bimodal site splits and extreme outliers."},
                {"term": r"1.4826 \cdot \text{MAD}(\mathbf{x})", "role": "Consistent Robust Scale Estimator", "meaning": "Multiplies raw MAD by 1/0.67449 = 1.4826 so it equals sigma when the bulk distribution is normal.", "failure": "Using unscaled MAD as sigma, underestimating spread by ~33%, or using classical z = (x - mean)/sd where the outlier inflates sd and masks itself!"},
                {"term": r"z_{\text{rob}, i}", "role": "Outlier-Resistant Anomaly Score", "meaning": "Flags anomalous scans or ROI values without being swamped by the very outliers being detected.", "failure": "Automatically deleting biological extremes (e.g., severe atrophy in a patient) without visual QC."}
            ]
        }
    },
    "DS05": {
        "commons_file": "File:Missing_not_at_random.png",
        "diagram_title": "Missingness Mechanisms (MCAR, MAR, MNAR) & Fold-Isolated Train-Only Imputation",
        "diagram_guide": "When clinical covariates or regional imaging features have missing values, fitting an imputer on the entire dataset before cross-validation leaks test-fold distribution moments into training, and naïve mean imputation shrinks variance and distorts correlations.",
        "pipeline_steps": ["Tabulate Missingness by Group & Site", "Test Association of R_i with Covariates", "Split Train and Test Folds First", "Fit Imputer Strictly on X_train", "Transform X_test & Propagate Uncertainty"],
        "equation": {
            "name": "Missingness Mechanism Taxonomy & Train-Only Imputation Boundary",
            "latex": r"P(R \mid Y_{\text{obs}}, Y_{\text{miss}}) = \begin{cases} P(R) & \text{MCAR} \\ P(R \mid Y_{\text{obs}}) & \text{MAR} \\ P(R \mid Y_{\text{obs}}, Y_{\text{miss}}) & \text{MNAR} \end{cases}, \qquad \hat{\boldsymbol{\theta}}_{\text{imp}}^{(k)} = \operatorname{fit}\!\left(X_{\text{train}}^{(k)}\right)",
            "summary": "Classifies missing data by whether drop-out depends on observed or unobserved values, and restricts imputer estimation to each training fold.",
            "terms": [
                {"term": r"P(R \mid Y_{\text{obs}})", "role": "Missing At Random (MAR) Condition", "meaning": "Probability of missingness depends on observed variables (e.g., older or higher-motion subjects fail QC more often), recoverable via conditioning or IPW.", "failure": "Treating MAR clinical dropout as MCAR complete-case data, biasing cohort estimates toward healthy low-motion subjects."},
                {"term": r"P(R \mid Y_{\text{obs}}, Y_{\text{miss}})", "role": "Missing Not At Random (MNAR)", "meaning": "Missingness depends directly on the unobserved value itself (e.g., severe cognitive impairment causing skipped cognitive tests); requires sensitivity bounds.", "failure": "Assuming standard imputation cures MNAR selection bias without sensitivity analysis."},
                {"term": r"\hat{\boldsymbol{\theta}}_{\text{imp}}^{(k)} = \operatorname{fit}(X_{\text{train}}^{(k)})", "role": "Fold-Isolated Imputation Parameters", "meaning": "Means, medians, or iterative regression weights fitted exclusively on fold k's training rows and applied to fold k's test rows.", "failure": "Calling SimpleImputer().fit_transform(X_all) before cross-validation."}
            ]
        }
    },
    "DS06": {
        "commons_file": "File:Roc_curve.svg",
        "diagram_title": "Conditional Probability, Base-Rate Neglect, Positive Predictive Value (PPV) & ROC vs. PR Curves",
        "diagram_guide": "A neuroimaging classifier with 90% sensitivity and 90% specificity sounds accurate—until you apply it to a clinical screening population where disease prevalence is 1%: the Positive Predictive Value P(Disease | Positive Scan) is only ~8.3%! Always separate P(Data | Hypothesis) from P(Hypothesis | Data).",
        "pipeline_steps": ["State Disorder Prevalence pi = P(D+)", "Measure Sensitivity & Specificity", "Apply Bayes' Rule for PPV & NPV", "Plot ROC Curve (Prevalence-Invariant)", "Plot Precision-Recall Curve (Imbalance-Sensitive)"],
        "equation": {
            "name": "Bayes' Theorem for Positive Predictive Value (PPV) Under Low Base Rates",
            "latex": r"\text{PPV} = P(D^+ \mid T^+) = \frac{\overbrace{P(T^+ \mid D^+)}^{\text{Sensitivity}} \cdot \overbrace{\pi}^{\text{Prevalence}}}{\underbrace{P(T^+ \mid D^+)\,\pi}_{\text{True Positives}} + \underbrace{\big(1 - P(T^- \mid D^-)\big)(1 - \pi)}_{\text{False Positives}}}",
            "summary": "Transforms test sensitivity and specificity into the actual posterior probability that a positive scan comes from a true case given population prevalence pi.",
            "terms": [
                {"term": r"\pi = P(D^+)", "role": "Population Base Rate (Prevalence)", "meaning": "Prior probability of the condition in the deployment population (often 1%–5% in population screening vs. 50% in balanced case-control studies).", "failure": "Reporting balanced 50/50 case-control accuracy as if it were the predictive value in a real hospital clinic."},
                {"term": r"P(T^+ \mid D^+) \cdot \pi", "role": "True-Positive Joint Mass", "meaning": "Fraction of the total population that both has the disorder and tests positive.", "failure": "Confusing sensitivity P(T+ | D+) with PPV P(D+ | T+) (the Prosecutor's / Reverse-Inference Fallacy)."},
                {"term": r"(1 - \text{Spec})(1 - \pi)", "role": "False-Positive Flood Term", "meaning": "When prevalence pi is small, even a tiny false-positive rate (1 - Spec = 0.05) multiplied by the huge healthy majority (1 - pi = 0.99) overwhelms true positives.", "failure": "Relying only on ROC-AUC under severe class imbalance instead of inspecting the Precision-Recall curve and PPV."}
            ]
        }
    },
    "DS07": {
        "commons_file": "File:Dice_sum_central_limit_theorem.svg",
        "diagram_title": "Sampling Distributions, Temporal Autocorrelation & Effective Sample Size (N_eff)",
        "diagram_guide": "The standard error of a mean shrinks as sigma / sqrt(N) only when observations are independent. In fMRI time series with positive autocorrelation rho_1, adjacent TRs carry redundant information, shrinking the effective sample size N_eff and widening the true sampling distribution.",
        "pipeline_steps": ["Measure Sample Size N & Autocorrelation rho", "Compute Bayley-Hammersley Effective N_eff", "Evaluate True SE = sigma / sqrt(N_eff)", "Compare Naive vs. Adjusted Confidence Intervals", "Check Small-N Correlation Instability"],
        "equation": {
            "name": "Autocorrelation-Adjusted Effective Sample Size & Standard Error",
            "latex": r"T_{\text{eff}} = \frac{T}{1 + 2\sum_{k=1}^{T-1}\left(1 - \frac{k}{T}\right)\rho_k} \xrightarrow{\text{AR(1)}} T \cdot \frac{1 - \rho_1}{1 + \rho_1}, \qquad \text{SE}(\bar{y}) = \frac{\sigma}{\sqrt{T_{\text{eff}}}}",
            "summary": "Reduces the nominal number of time points T by the integrated autocorrelation time to reflect the true number of independent degrees of freedom.",
            "terms": [
                {"term": r"\rho_k = \operatorname{Corr}(y_t, y_{t-k})", "role": "Lag-k Temporal Autocorrelation", "meaning": "Correlation between fMRI samples separated by k TRs; positive due to the sluggish ~6 s hemodynamic response.", "failure": "Treating 1,000 multiband TRs (TR=0.5 s) as 1,000 independent draws when computing correlation p-values."},
                {"term": r"\frac{1 - \rho_1}{1 + \rho_1}", "role": "AR(1) Information Reduction Factor", "meaning": "At lag-1 autocorrelation rho_1 = 0.6, each TR provides only (0.4/1.6) = 25% of an independent observation!", "failure": "Using unadjusted sqrt(T - 2) in Fisher-z standard errors 1/sqrt(T - 3), wildly inflating connectivity significance."},
                {"term": r"\sigma / \sqrt{T_{\text{eff}}}", "role": "True Sampling Standard Error", "meaning": "Governs the actual width of the sampling distribution across repeated runs or participants.", "failure": "Confusing the standard deviation of the data (sigma) with the standard error of the mean (SE)."}
            ]
        }
    },
    "DS08": {
        "commons_file": "File:Illustration_bootstrap.svg",
        "diagram_title": "Nonparametric Bootstrap Uncertainty & Cluster Resampling at the Participant Unit",
        "diagram_guide": "Bootstrapping estimates sampling uncertainty by drawing B resamples with replacement of size N. In hierarchical neuroimaging data (multiple runs, trials, or parcels per person), you MUST resample whole participants (cluster bootstrap) rather than individual rows!",
        "pipeline_steps": ["Identify Independent Cluster Unit (Participant i)", "Sample N Participants with Replacement (b=1..B)", "Include All Runs/Rows of Selected Participants", "Recompute Estimator theta-hat*_b on Each Resample", "Form 95% Percentile / BCa Confidence Interval"],
        "equation": {
            "name": "Participant-Level Cluster Bootstrap Resampling & Percentile Interval",
            "latex": r"\mathcal{D}^{*(b)} = \bigcup_{m=1}^{N} \mathcal{D}_{i_m^{*(b)}}, \quad i_m^{*(b)} \stackrel{\text{iid}}{\sim} \operatorname{Uniform}\{1,\dots,N\}, \qquad \text{CI}_{1-\alpha} = \left[\hat{\theta}_{(\alpha/2)}^{*}, \; \hat{\theta}_{(1-\alpha/2)}^{*}\right]",
            "summary": "Resamples complete participant data blocks with replacement to preserve within-participant covariance across runs, time points, and brain regions.",
            "terms": [
                {"term": r"i_m^{*(b)} \sim \operatorname{Uniform}\{1,\dots,N\}", "role": "Participant-Unit Resampling Draw", "meaning": "Draws N participant IDs with replacement (~63.2% unique participants per bootstrap replicate).", "failure": "Resampling individual fMRI volumes or multi-run table rows independently, destroying within-subject dependence and narrowing CIs."},
                {"term": r"\mathcal{D}_{i_m^{*(b)}}", "role": "Intact Within-Participant Data Block", "meaning": "Carries all runs, visits, and voxels of chosen participant i_m together into replicate b.", "failure": "Using bootstrap replicates as a cross-validation split (where duplicates appear in both train and test sets!)."},
                {"term": r"[\hat{\theta}_{(\alpha/2)}^*, \hat{\theta}_{(1-\alpha/2)}^*]", "role": "Empirical Bootstrap Confidence Interval", "meaning": "Spans the central (1 - alpha) quantiles of the B bootstrap estimates without parametric normality assumptions.", "failure": "Running too few bootstrap replicates (e.g., B=50 instead of B>=1,000–5,000) for tail quantile stability."}
            ]
        }
    },
    "DS09": {
        "commons_file": "File:The_Normal_Distribution.svg",
        "diagram_title": "Temporal z-Standardization vs. Percent Signal Change (PSC) & Baseline Reference Choices",
        "diagram_guide": "Raw fMRI scanner units are arbitrary. Converting a voxel time series to Percent Signal Change (PSC = 100 * (Y_t - B_v) / B_v) preserves interpretable physiological magnitude (~1–3% BOLD change), whereas temporal z-scoring divides by the voxel's total temporal SD (which mixes task signal and noise variance!).",
        "pipeline_steps": ["Define Baseline Reference B_v (Mean vs. Rest)", "Compute Percent Signal Change (PSC %)", "Compare Temporal z-Score (Signal / Total SD)", "Mask Out-of-Brain Low-Baseline Voxels", "Verify Effect on Group GLM Betas"],
        "equation": {
            "name": "Percent Signal Change (PSC) vs. Temporal z-Standardization",
            "latex": r"\text{PSC}_{v,t} = 100 \times \frac{Y_{v,t} - B_v}{B_v}, \qquad Z_{v,t} = \frac{Y_{v,t} - \mu_v}{\sqrt{\sigma_{\text{signal},v}^2 + \sigma_{\text{noise},v}^2}} \implies \beta_{\text{PSC}} \neq \beta_Z",
            "summary": "Contrasts baseline-normalized percentage units against variance-normalized z-units whose denominator depends on both task amplitude and scanner noise.",
            "terms": [
                {"term": r"B_v \text{ (Baseline Intensity)}", "meaning": "Voxel v's temporal mean (or explicit pre-stimulus rest baseline) representing equilibrium T2* signal intensity.", "role": "Physical Baseline Anchor", "failure": "Computing PSC after mean-centering the time series (where B_v = 0!), causing division by zero."},
                {"term": r"100 \times (Y_{v,t} - B_v) / B_v", "role": "Percent Signal Change (PSC)", "meaning": "Expresses BOLD fluctuations as a percentage of local baseline intensity (typically 0.5%–3.0% in cortex at 3T).", "failure": "Dividing by tiny out-of-brain or sinus-dropout baselines without a brain mask guard, creating +5000% edge spikes."},
                {"term": r"\sqrt{\sigma_{\text{signal},v}^2 + \sigma_{\text{noise},v}^2}", "role": "Confounded Z-Score Denominator", "meaning": "Temporal z-scoring divides by total temporal SD; therefore a voxel with huge task activation increases its own denominator and self-attenuates its beta!", "failure": "Interpreting z-scored GLM betas as pure response amplitudes when thermal noise varies across coils or groups."}
            ]
        }
    },
    "DS10": {
        "commons_file": "File:Orthogonal_projection.svg",
        "diagram_title": "Linear Algebra of Design Matrices: Column Space Projection, Rank Deficiency & Identifiability",
        "diagram_guide": "In linear regression y = X beta + e, the fitted signal y-hat = P_X y is unique because the orthogonal projection matrix P_X = X X^+ depends only on the column space C(X). However, the individual parameter vector beta-hat is uniquely identifiable if and only if X has full column rank (rank(X) == p)!",
        "pipeline_steps": ["Inspect Singular Values sigma_i of X", "Verify Column Rank: rank(X) == p", "Compute Orthogonal Projector P_X = X X^+", "Separate Identifiable vs. Nullspace Contrasts", "Reparameterize Collinear Columns"],
        "equation": {
            "name": "Moore-Penrose Pseudoinverse Projection & Contrast Estimability Condition",
            "latex": r"\hat{\mathbf{y}} = P_{\mathcal{C}(X)}\,\mathbf{y} = X X^{+} \mathbf{y}, \qquad \hat{\boldsymbol{\beta}} = X^{+}\mathbf{y} + \left(I_p - X^{+}X\right)\mathbf{w}, \qquad \mathbf{c}^T\boldsymbol{\beta} \text{ is estimable} \iff \mathbf{c} \in \mathcal{R}(X^T)",
            "summary": "Shows that while fitted values y-hat are always unique, parameter vector beta has an arbitrary nullspace component (I - X^+ X)w whenever columns of X are linearly dependent.",
            "terms": [
                {"term": r"P_{\mathcal{C}(X)} = X X^{+}", "role": "Unique Column-Space Projector", "meaning": "Symmetric idempotent matrix (P^2 = P, P^T = P) projecting y orthogonally onto the subspace spanned by columns of X.", "failure": "Calling np.linalg.inv(X.T @ X) on a rank-deficient design matrix, raising LinAlgError or exploding to 1e16."},
                {"term": r"(I_p - X^{+}X)\mathbf{w}", "role": "Nullspace Parameter Ambiguity", "meaning": "When a regressor equals the sum of two other regressors (e.g., Intercept + Dummy_A + Dummy_B), infinitely many beta vectors yield the exact same fit y-hat.", "failure": "Interpreting individual coefficients from a rank-deficient design where np.linalg.lstsq arbitrarily picks the minimum-norm solution."},
                {"term": r"\mathbf{c} \in \mathcal{R}(X^T) \iff X^+ X \mathbf{c} = \mathbf{c}", "role": "Contrast Estimability Invariant", "meaning": "A linear contrast c^T beta is invariant to nullspace ambiguity if and only if c lies entirely in the row space of X.", "failure": "Testing a non-estimable contrast that depends on how redundant columns were parameterized."}
            ]
        }
    },
    "DS11": {
        "commons_file": "File:MLfunctionbinomial-en.svg",
        "diagram_title": "Maximum Likelihood Estimation (MLE): Choosing the Noise Distribution Before Fitting",
        "diagram_guide": "Every loss function is a disguised probability model: minimizing squared error (OLS) is Maximum Likelihood under Gaussian noise, minimizing absolute error (L1) is MLE under heavy-tailed Laplace noise, and binary cross-entropy is MLE under a Bernoulli likelihood.",
        "pipeline_steps": ["Inspect Data Domain & Residual Tails", "Specify Parametric Likelihood p(y | X, theta)", "Sum Log-Likelihood Across Independent Units", "Maximize l(theta) == Minimize Negative Log-Likelihood", "Compare AIC / BIC Across Noise Models"],
        "equation": {
            "name": "Equivalence of Negative Log-Likelihood and Loss Minimization",
            "latex": r"\hat{\boldsymbol{\theta}}_{\text{MLE}} = \arg\max_{\boldsymbol{\theta}} \sum_{i=1}^{N} \ln p(y_i \mid \mathbf{x}_i, \boldsymbol{\theta}) = \arg\min_{\boldsymbol{\theta}} \begin{cases} \frac{1}{2\sigma^2}\sum_i (y_i - \hat{y}_i)^2 & \text{Gaussian (L2)} \\[4pt] \frac{1}{b}\sum_i |y_i - \hat{y}_i| & \text{Laplace (L1)} \\[4pt] -\sum_i \big[y_i\ln \hat{p}_i + (1-y_i)\ln(1-\hat{p}_i)\big] & \text{Bernoulli (BCE)} \end{cases}",
            "summary": "Unifies regression and classification losses as negative log-likelihoods under explicit data-generating noise distributions.",
            "terms": [
                {"term": r"\sum_{i=1}^{N} \ln p(y_i \mid \mathbf{x}_i, \boldsymbol{\theta})", "role": "Additive Log-Likelihood Objective", "meaning": "Converts a product of tiny probabilities (which underflows float64 to 0.0) into a numerically stable sum of log-probabilities.", "failure": "Multiplying raw likelihoods prod_i p(y_i) across N=500 subjects, causing immediate floating-point underflow to 0.0."},
                {"term": r"\frac{1}{2\sigma^2}\sum_i (y_i - \hat{y}_i)^2 \text{ vs. } \frac{1}{b}\sum_i |y_i - \hat{y}_i|", "role": "Tail-Sensitivity Commitment", "meaning": "Gaussian L2 squares large residuals (optimal for thermal noise, fragile to spikes); Laplace L1 grows linearly (robust to outlier scans).", "failure": "Using Gaussian OLS on spike-contaminated or skewed count data without checking residual normality."},
                {"term": r"\hat{\sigma}_{\text{MLE}}^2 = \frac{1}{N}\text{RSS} \;\text{vs.}\; \frac{1}{N-p}\text{RSS}", "role": "Finite-Sample Variance Bias", "meaning": "Raw MLE divides by N and underestimates variance when p parameters are fitted; REML/OLS divides by N - p.", "failure": "Ignoring parameter degrees of freedom p when estimating residual variance in high-dimensional designs."}
            ]
        }
    },
    "DS12": {
        "commons_file": "File:Gradient_descent.svg",
        "diagram_title": "Gradient-Based Optimization, Lipschitz Learning-Rate Bounds, Conditioning & Early Stopping",
        "diagram_guide": "Registration, deep learning, and regularized GLMs minimize an objective L(theta) iteratively along the negative gradient -grad L. If features have wildly different scales, the Hessian eigenvalues stretch into a narrow canyon (high condition number kappa), causing gradient descent to zig-zag or diverge unless features are standardized or preconditioned!",
        "pipeline_steps": ["Standardize Input Feature Scales", "Check Hessian Condition Number kappa", "Set Step Size eta < 2 / L_max", "Verify Analytic Gradient vs. Finite Differences", "Monitor Both Train Loss & Validation Generalization"],
        "equation": {
            "name": "Gradient Descent Update & Largest-Eigenvalue Stability Bound",
            "latex": r"\boldsymbol{\theta}^{(t+1)} = \boldsymbol{\theta}^{(t)} - \eta \, \nabla_{\boldsymbol{\theta}}\mathcal{L}\!\left(\boldsymbol{\theta}^{(t)}\right), \qquad \text{Convergence requires } 0 < \eta < \frac{2}{\lambda_{\max}(\nabla^2 \mathcal{L})}, \qquad \kappa(H) = \frac{\lambda_{\max}(H)}{\lambda_{\min}(H)}",
            "summary": "Steps opposite the gradient with learning rate eta bounded by the inverse of the largest Hessian curvature eigenvalue.",
            "terms": [
                {"term": r"-\eta \, \nabla_{\boldsymbol{\theta}}\mathcal{L}(\boldsymbol{\theta}^{(t)})", "role": "First-Order Descent Step", "meaning": "Moves parameters in the direction of steepest local decrease of the training objective.", "failure": "Getting trapped in a bad local minimum during 3D image registration when starting far from overlap without multi-resolution pyramids."},
                {"term": r"\eta < 2 / \lambda_{\max}(\nabla^2\mathcal{L})", "role": "Lipschitz Curvature Stability Ceiling", "meaning": "If learning rate eta exceeds 2 / lambda_max, updates overshoot the valley walls with growing amplitude and explode to NaN/Inf.", "failure": "Leaving raw unscaled covariates (e.g., TIV in 1,500,000 mm^3 alongside age in years), which explodes lambda_max and causes divergence."},
                {"term": r"\mathcal{L}_{\text{train}} \downarrow \;\text{vs.}\; \mathcal{L}_{\text{val}} \uparrow", "role": "Optimization vs. Generalization Split", "meaning": "Driving training loss to zero only proves the optimizer worked; validation loss reveals when the model starts memorizing noise.", "failure": "Equating a low training loss with a scientifically valid or generalizable model."}
            ]
        }
    },
    "DS13": {
        "commons_file": "File:Effect_of_multicollinearity_on_coefficients_of_linear_model.png",
        "diagram_title": "Regression Diagnostics: Collinearity (VIF), High-Leverage Points & Cook's Distance",
        "diagram_guide": "Even when a regression model has a high overall R^2, near-collinear predictors (high Variance Inflation Factor, VIF) make individual beta weights wildly unstable and sign-flip across samples, while a single high-leverage participant (high hat-value h_{ii} and Cook's distance D_i) can dictate the entire regression line.",
        "pipeline_steps": ["Compute Variance Inflation Factor VIF_j", "Compute Leverage Hat Diagonal h_ii", "Evaluate Studentized Residuals r_i", "Compute Cook's Distance Influence D_i", "Compare OLS vs. Leave-One-Out / Ridge"],
        "equation": {
            "name": "Variance Inflation Factor (VIF) & Cook's Distance Influence Metric",
            "latex": r"\text{VIF}_j = \frac{1}{1 - R_{j \mid -j}^2}, \qquad h_{ii} = \big[X(X^T X)^{-1}X^T\big]_{ii}, \qquad D_i = \frac{e_i^2}{p\,\hat{\sigma}^2} \cdot \frac{h_{ii}}{(1 - h_{ii})^2}",
            "summary": "Quantifies how much predictor j's variance is inflated by correlation with other predictors (VIF) and how strongly observation i pulls the fitted parameter vector (Cook's D_i).",
            "terms": [
                {"term": r"\text{VIF}_j = (1 - R_{j \mid -j}^2)^{-1}", "role": "Collinearity Variance Multiplier", "meaning": "Factor by which Var(beta-hat_j) is multiplied compared to an orthogonal design; VIF > 5–10 signals severe instability.", "failure": "Entering both global brain volume and sum of left+right hemisphere volumes into the same OLS model."},
                {"term": r"h_{ii} = \mathbf{x}_i^T (X^T X)^{-1} \mathbf{x}_i", "role": "Covariate Space Leverage (Hat Value)", "meaning": "Measures how far participant i's predictors sit from the sample centroid; bounded in [1/N, 1] with sum(h_ii) = p.", "failure": "Checking only vertical residual size e_i while missing an extreme leverage point that pulled the line straight through itself (small e_i, huge h_ii)!"},
                {"term": r"D_i = \frac{\|\hat{\mathbf{y}} - \hat{\mathbf{y}}_{(-i)}\|_2^2}{p\,\hat{\sigma}^2}", "role": "Cook's Leave-One-Out Influence", "meaning": "Combines residual magnitude and leverage to measure how much all fitted values shift if participant i is removed.", "failure": "Publishing a brain-behavior correlation driven entirely by 1–2 high-Cook's-distance subjects."}
            ]
        }
    },
    "DS14": {
        "commons_file": "File:GaussianScatterPCA.svg",
        "diagram_title": "Singular Value Decomposition (SVD), Principal Component Analysis (PCA) & Train-Only Basis Fitting",
        "diagram_guide": "SVD factors a centered data matrix X_c = U S V^T into orthogonal sample scores (U S) and principal spatial patterns (V). Because PCA is purely variance-maximizing, high-variance head motion or site offsets will dominate PC1 unless cleaned—and fitting V on the full dataset before cross-validation leaks test-fold covariance structure.",
        "pipeline_steps": ["Center Columns Using Train Mean mu_train", "Compute Economy SVD: X_c = U S V^T", "Inspect Explained Variance Ratio lambda_k", "Project Test Data: Z_test = (X_test - mu_train) V_K", "Verify Reconstruction Error & Sign Indeterminacy"],
        "equation": {
            "name": "Centered Singular Value Decomposition & Out-of-Sample PCA Projection",
            "latex": r"X_{\text{train}, c} = U \Sigma V^T, \qquad \lambda_k = \frac{\sigma_k^2}{N_{\text{train}} - 1}, \qquad Z_{\text{test}} = \left(X_{\text{test}} - \mathbf{1}\hat{\boldsymbol{\mu}}_{\text{train}}^T\right) V_{(:, 1:K)}",
            "summary": "Decomposes centered training data into orthogonal singular vectors and projects held-out test data onto the frozen top-K training axes V_K.",
            "terms": [
                {"term": r"X - \mathbf{1}\hat{\boldsymbol{\mu}}_{\text{train}}^T", "role": "Mandatory Feature Centering", "meaning": "Subtracts the training-fold feature mean before SVD so PC1 captures covariance around the centroid rather than the origin offset.", "failure": "Running SVD on uncentered raw MRI intensities, where PC1 merely points from zero to the grand mean image."},
                {"term": r"\sigma_k^2 / \sum_j \sigma_j^2", "role": "Explained Variance Fraction", "meaning": "Proportion of total Frobenius energy captured by orthogonal axis k; high variance does NOT guarantee biological relevance over artifact.", "failure": "Assuming '90% variance explained' means task or clinical signal was preserved when the top PCs are scanner drift and motion."},
                {"term": r"V_{(:, 1:K)} \text{ (Frozen Train Basis)}", "role": "Fold-Isolated Projection Matrix", "meaning": "Orthonormal loading vectors estimated strictly on X_train (note that each column v_k has arbitrary +/-1 sign indeterminacy across folds).", "failure": "Fitting PCA on the combined train+test matrix before splitting, or comparing raw PC signs across folds without Procrustes alignment."}
            ]
        }
    },
    "DS15": {
        "commons_file": "File:Feature_selection_Wrapper_Method.png",
        "diagram_title": "High-Dimensional Feature Screening (P >> N) & Global vs. Fold-Isolated Selection Leakage",
        "diagram_guide": "In connectomics and voxelwise decoding, features P (10,000–100,000) vastly outnumber participants N (50–200). If you screen the 'top K most correlated edges' across all N participants before running K-fold cross-validation, a pure random-noise dataset will achieve >85% 'cross-validated accuracy'!",
        "pipeline_steps": ["Generate Pure Null Test Case (X_null, y_null)", "Demonstrate Global Screening Leakage (~85% Acc)", "Move Feature Selector Inside CV Loop", "Fit Screen + Model Strictly on X_train^(k)", "Verify Permutation Null Centers at Chance (50% / r=0)"],
        "equation": {
            "name": "Nested Within-Fold Feature Screening vs. Leaky Global Screening",
            "latex": r"\hat{S}_{\text{valid}}^{(k)} = \operatorname{TopK}_{j \in \{1..P\}}\!\left(\big|r(X_{\text{train}, j}^{(k)}, \, \mathbf{y}_{\text{train}}^{(k)})\big|\right), \qquad \hat{y}_i = f_{\hat{\boldsymbol{\theta}}^{(k)}}\!\left(\mathbf{x}_{i, \hat{S}_{\text{valid}}^{(k)}}\right) \quad \forall i \in \text{Fold } k",
            "summary": "Re-estimates the selected feature subset S^(k) from scratch inside every training fold k without ever consulting test-fold labels y_test^(k).",
            "terms": [
                {"term": r"\hat{S}_{\text{valid}}^{(k)} \subset \{1,\dots,P\}", "role": "Fold-Specific Screened Feature Set", "meaning": "Indices of the K features showing strongest association with y_train inside training fold k only.", "failure": "Screening features once on (X_all, y_all) before cross-validation—the single most common fatal leakage bug in neuroimaging ML!"},
                {"term": r"P \gg N \text{ Extreme Order Statistics}", "role": "High-Dimensional Spurious Correlation Floor", "meaning": "Among P=50,000 pure noise edges and N=60 subjects, the maximum sample correlation E[max_j |r_j|] exceeds 0.50 by chance alone.", "failure": "Trusting high in-sample correlations or leaky CV scores without running a full-pipeline label-permutation test."},
                {"term": r"\operatorname{Jaccard}(\hat{S}^{(k)}, \hat{S}^{(k')})", "role": "Cross-Fold Feature Stability Audit", "meaning": "Measures overlap of selected edges across folds; low overlap reveals that multiple collinear edges trade places across splits.", "failure": "Over-interpreting the exact biological identity of 10 unstable Lasso/screened edges when 500 correlated edges carry the same information."}
            ]
        }
    },
    "DS16": {
        "commons_file": "File:Directed_acyclic_graph_2.svg",
        "diagram_title": "End-to-End Computational Reproducibility, Cryptographic Manifests & AI Analysis Auditing",
        "diagram_guide": "A computational result is reproducible only when an independent researcher (or automated CI runner) can regenerate the exact numerical tables and figures from raw inputs using a locked environment (uv.lock), fixed seeds, and a cryptographic audit manifest.",
        "pipeline_steps": ["Lock Dependencies (pyproject.toml + uv.lock)", "Hash Raw Input Files (SHA-256)", "Isolate Train/Test Split Indices", "Run Automated Assertion Suite", "Export Signed JSON Audit Manifest"],
        "equation": {
            "name": "End-to-End Reproducibility Contract & Audit Verification Function",
            "latex": r"\mathcal{A}_{\text{manifest}} = \Big\{\operatorname{SHA256}(\mathcal{D}_{\text{in}}), \; \operatorname{SHA256}(\text{uv.lock}), \; s_{\text{RNG}}, \; \text{split\_ids}, \; \operatorname{SHA256}(\mathcal{R}_{\text{out}})\Big\}, \qquad \mathcal{V}(\mathcal{A}) \in \{\text{PASS}, \text{FAIL}\}",
            "summary": "Binds input data hashes, locked dependency versions, random seeds, split boundaries, and output artifact digests into a verifiable provenance record.",
            "terms": [
                {"term": r"\operatorname{SHA256}(\mathcal{D}_{\text{in}}) \text{ \& } \operatorname{SHA256}(\text{uv.lock})", "role": "Input & Environment Fingerprint", "meaning": "Guarantees that the exact same input bytes and library versions (NumPy, SciPy, scikit-learn, NiBabel) are used.", "failure": "Using unpinned pip install commands or mutating input files in place without version hashes."},
                {"term": r"\text{split\_ids} \cap \text{test\_ids} = \emptyset", "role": "Explicit Disjoint Partition Verification", "meaning": "Asserts programmatic disjointness of participant and site IDs between training and evaluation sets.", "failure": "Relying on AI-generated pipeline code without programmatically asserting zero participant overlap across splits."},
                {"term": r"\mathcal{V}(\mathcal{A})", "role": "Automated Invariant & Range Check", "meaning": "Executes assertions on shapes, units, null-permutation baselines, and expected numerical outcome ranges.", "failure": "Accepting an AI-written analysis because the code ran without throwing a Python exception."}
            ]
        }
    },
    "M01": {
        "commons_file": "File:Orthogonal_projection.svg",
        "diagram_title": "Encoding vs. Decoding Directions & The Haufe Forward-Model Transformation",
        "diagram_guide": "An encoding model predicts brain activity from stimulus features (S -> X), whereas a decoding model predicts the stimulus/label from multivoxel patterns (X -> Y). Crucially, raw discriminative decoding weights W are NOT maps of neural representation—because a decoder places non-zero weights on pure noise channels to cancel correlated noise in signal channels! Applying the Haufe transform A = Sigma_X W Sigma_{Y-hat}^{-1} recovers the true forward encoding pattern (Haufe et al., 2014).",
        "pipeline_steps": ["Define Stimulus S and Multivoxel Pattern X", "Fit Encoding (S -> X) vs. Decoding (X -> Y)", "Demonstrate Noise-Suppressor Weight Artifact", "Apply Haufe Transform A = Cov(X, Y-hat)", "Verify Out-of-Sample Generalization"],
        "equation": {
            "name": "Encoding Model, Linear Decoder & Haufe Forward Pattern Transformation",
            "latex": r"\text{Encoding: } X = S A^T + E, \qquad \text{Decoding: } \hat{Y} = X W, \qquad \text{Haufe Pattern: } \hat{A} = \Sigma_X W \Sigma_{\hat{Y}}^{-1} \propto \operatorname{Cov}(X, \hat{Y})",
            "summary": "Distinguishes forward generative activation patterns A from backward discriminative filter weights W and converts any linear decoder into an interpretable activation map via the data covariance Sigma_X.",
            "terms": [
                {"term": r"W \text{ (Backward Decoding Filter)}", "role": "Discriminative Extraction Weights", "meaning": "Combines voxels to maximize signal-to-noise ratio of Y-hat; assigns strong weights to noise-only suppressor voxels that share correlated physiological noise with signal voxels.", "failure": "Plotting raw SVM/Ridge/Logistic weight maps W on a brain surface and claiming 'these voxels encode the stimulus' (Haufe et al., 2014)!"},
                {"term": r"\Sigma_X = \operatorname{Cov}(X)", "role": "Spatial Voxel Covariance Matrix", "meaning": "Captures how voxels co-fluctuate across trials; multiplying Sigma_X by W projects the filter back onto the forward data-generating subspace.", "failure": "Ignoring spatial noise covariance across voxels when interpreting multivariate classifiers."},
                {"term": r"\hat{A} = \Sigma_X W \Sigma_{\hat{Y}}^{-1}", "role": "Haufe Forward Activation Pattern", "meaning": "Recovers the exact marginal covariance between each voxel and the decoded variable Y-hat, assigning zero weight to pure noise suppressor channels.", "failure": "Confusing predictive accuracy of a decoder with spatial localization of individual weights."}
            ]
        }
    },
    "M02": {
        "commons_file": "File:L1_and_L2_balls.svg",
        "diagram_title": "Regularized Linear Models: Ridge (L2), Lasso (L1), Elastic Net & Classification Log-Odds",
        "diagram_guide": "Look at how the elliptical loss contours touch the constraint region: the round L2 ball (Ridge) shrinks correlated voxel weights smoothly together without zeroing them, whereas the sharp corners of the L1 diamond (Lasso) force most weights to exact zero—arbitrarily picking one voxel from a correlated brain region and dropping its neighbors!",
        "pipeline_steps": ["Standardize Features Inside Train Fold", "Compare Ridge (L2), Lasso (L1) & Elastic Net", "Tune Hyperparameter lambda via Inner CV", "Inspect Weight Sparsity & Fold Stability", "Evaluate Held-Out MSE / Log-Loss"],
        "equation": {
            "name": "Elastic Net Regularized Objective (Unifying Ridge L2 and Lasso L1)",
            "latex": r"\hat{\mathbf{w}} = \arg\min_{\mathbf{w}} \left\{ \underbrace{\frac{1}{2N}\| \mathbf{y} - X\mathbf{w} \|_2^2}_{\text{Empirical Data Fit}} + \lambda \Big( \underbrace{\alpha \|\mathbf{w}\|_1}_{\text{Lasso Sparsity}} + \underbrace{\frac{1-\alpha}{2}\|\mathbf{w}\|_2^2}_{\text{Ridge Grouping}} \Big) \right\}, \qquad \hat{\mathbf{w}}_{\text{Ridge}} = (X^T X + \lambda I_p)^{-1} X^T \mathbf{y}",
            "summary": "Balances data fidelity against an L1 sparsity penalty (alpha=1) and an L2 Tikhonov grouping penalty (alpha=0) that adds lambda to every eigenvalue of X^T X.",
            "terms": [
                {"term": r"(X^T X + \lambda I_p)^{-1}", "role": "Ridge Eigenvalue Stabilization", "meaning": "Shifts every singular value sigma_j^2 of X^T X upward to sigma_j^2 + lambda, making inversion well-conditioned even when P >> N.", "failure": "Fitting regularized models without standardizing feature scales first, which penalizes small-unit features unfairly."},
                {"term": r"\lambda \alpha \|\mathbf{w}\|_1", "role": "L1 Diamond Corner Sparsity Penalty", "meaning": "Drives weak weights to exact 0 via soft-thresholding, but exhibits unstable selection when brain voxels are strongly correlated.", "failure": "Claiming the 95% of voxels zeroed by Lasso are 'not involved in the task' when they were merely collinear with the surviving 5%."},
                {"term": r"\lambda \text{ (Tuned in Inner CV)}", "role": "Regularization Strength Hyperparameter", "meaning": "Controls the bias-variance trade-off; must be selected inside an inner cross-validation loop.", "failure": "Tuning lambda on the test fold and reporting the best test score."}
            ]
        }
    },
    "M03": {
        "commons_file": "File:Kernel_trick_idea.svg",
        "diagram_title": "Nonlinear Boundaries: SVM Kernel Trick (RBF) & Random Forest Ensemble Variance Reduction",
        "diagram_guide": "When classes are not linearly separable in input space, an RBF kernel maps samples implicitly into an infinite-dimensional similarity space via pairwise distances ||x_i - x_j||^2, while Random Forests average B decorrelated decision trees trained on bootstrap samples. However, in high-dimensional noisy neuroimaging (P >> N), flexible nonlinear models easily memorize training noise unless strictly regularized!",
        "pipeline_steps": ["Establish Linear Ridge/SVM Baseline", "Fit RBF-Kernel SVM (Tune C and gamma)", "Fit Random Forest (B Trees, Feature Subsampling)", "Diagnose High-Dimension Overfitting (gamma too large)", "Compare Calibration & Held-Out ROC-AUC"],
        "equation": {
            "name": "Dual Kernel SVM Decision Function & RBF Bandwidth vs. Bagging Variance",
            "latex": r"f(\mathbf{x}) = \sum_{i=1}^{N_{\text{train}}} \alpha_i y_i \, \underbrace{\exp\!\left(-\gamma \|\mathbf{x}_i - \mathbf{x}\|_2^2\right)}_{K_{\text{RBF}}(\mathbf{x}_i, \mathbf{x})} + b, \qquad \operatorname{Var}\!\left(\frac{1}{B}\sum_{b=1}^{B} T_b(\mathbf{x})\right) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2",
            "summary": "Expresses nonlinear classification entirely through pairwise RBF kernel similarities to training support vectors, and shows how tree bagging reduces variance to the inter-tree correlation floor rho*sigma^2.",
            "terms": [
                {"term": r"K_{\text{RBF}}(\mathbf{x}_i, \mathbf{x}) = \exp(-\gamma\|\mathbf{x}_i - \mathbf{x}\|_2^2)", "role": "Local Gaussian Similarity Kernel", "meaning": "Measures proximity between test subject x and training subject x_i; bandwidth gamma controls locality.", "failure": "Setting gamma too large in high dimensions (P >> N), turning the kernel matrix into an identity matrix where every training point is an isolated island (100% train acc, 50% test acc)."},
                {"term": r"\alpha_i y_i \text{ (Support Vector Weights)}", "role": "Sparse Dual Margin Multipliers", "meaning": "Non-zero only for training subjects lying on or inside the margin boundary.", "failure": "Assuming nonlinear RBF kernels automatically beat linear Ridge/SVM on small-N whole-brain connectomes (PM04 benchmark shows linear baselines often tie or win!)."},
                {"term": r"\rho\sigma^2 + \frac{1-\rho}{B}\sigma^2", "role": "Ensemble Variance Floor", "meaning": "Averaging B trees eliminates the (1-rho)/B variance term, while random feature subsampling lowers inter-tree correlation rho.", "failure": "Using impurity-based tree feature importances without permutation testing, which biases toward high-cardinality noise features."}
            ]
        }
    },
    "M04": {
        "commons_file": "File:K-fold_cross_validation_EN.svg",
        "diagram_title": "Nested Cross-Validation, Leave-One-Site-Out Generalization & ComBat Harmonization Limits",
        "diagram_guide": "Multi-site neuroimaging cohorts suffer from additive (gamma) and multiplicative (delta) scanner site effects. ComBat adjusts location and scale across sites—but if clinical diagnosis is confounded with scanner site, or if ComBat is fitted using outcome labels across train+test splits, harmonization either erases biological signal or leaks test information!",
        "pipeline_steps": ["Audit Site-by-Diagnosis Contingency Table", "Outer Loop: Leave-One-Site-Out (LOSO) Split", "Inner Loop: Tune Hyperparameters on Train Sites", "Fit ComBat / Standardization Without Outcome Leakage", "Report Per-Site & Worst-Site Generalization"],
        "equation": {
            "name": "ComBat Empirical Bayes Location-Scale Site Adjustment (Johnson et al., 2007; Fortin et al., 2018)",
            "latex": r"y_{ijv}^{\text{ComBat}} = \frac{y_{ijv} - \hat{\alpha}_v - \mathbf{x}_{ij}^T\hat{\boldsymbol{\beta}}_v - \gamma_{iv}^*}{\delta_{iv}^*} + \hat{\alpha}_v + \mathbf{x}_{ij}^T\hat{\boldsymbol{\beta}}_v",
            "summary": "Subtracts empirical-Bayes-shrunk site additive shift gamma_{iv}^* and divides by site multiplicative scale delta_{iv}^* while preserving biological covariate effects X beta.",
            "terms": [
                {"term": r"\gamma_{iv}^*, \; \delta_{iv}^*", "role": "Empirical Bayes Site Location & Scale", "meaning": "Scanner-specific mean offset and variance multiplier for site i at feature v, shrunk across features to stabilize small sites.", "failure": "Fitting ComBat across the entire dataset with the target diagnosis Y in X before cross-validation, which leaks test labels into every feature!"},
                {"term": r"\mathbf{x}_{ij}^T\hat{\boldsymbol{\beta}}_v", "role": "Preserved Covariate Design Term", "meaning": "Biological covariates (e.g., age, sex) protected during site estimation—valid ONLY for observed covariates, never the held-out prediction target!", "failure": "Including the target label in ComBat's design matrix during predictive modeling, fabricating high cross-validated accuracy out of pure noise."},
                {"term": r"\text{Site} \perp\!\!\!\perp \text{Diagnosis}", "role": "Positivity & Unconfounded Site Requirement", "meaning": "If Site A scanned 90% patients and Site B scanned 90% controls, no statistical harmonization can separate scanner physics from disease.", "failure": "Training a deep model that achieves high pooled CV accuracy by covertly classifying scanner site as a shortcut for diagnosis."}
            ]
        }
    },
    "M05": {
        "commons_file": "File:Independent_component_analysis_in_EEGLAB.png",
        "diagram_title": "Blind Source Separation: Orthogonal Gaussian PCA vs. Non-Gaussian Independent Component Analysis (ICA)",
        "diagram_guide": "PCA finds orthogonal axes of maximum variance (2nd-order covariance), which leaves non-Gaussian sources mixed up to an arbitrary orthogonal rotation. Spatial ICA (MELODIC / FastICA) rotates the whitened subspace to maximize non-Gaussianity (kurtosis / negentropy), separating spatially sparse resting-state networks from vascular, CSF, and motion rim artifacts.",
        "pipeline_steps": ["Center & Whiten Data via PCA (Z = S^{-1/2} U^T X)", "Verify Second-Order Rotation Ambiguity", "Maximize Non-Gaussianity J(w^T Z) (FastICA)", "Extract Spatial Maps S & Time Courses A", "Classify Neural Networks vs. Artifact Rims"],
        "equation": {
            "name": "Spatial ICA Generative Mixing Model & Negentropy Maximization",
            "latex": r"X_{T \times V} = \underbrace{A_{T \times K}}_{\text{Time Courses}} \, \underbrace{S_{K \times V}}_{\text{Spatial Maps}} + E, \qquad \mathbf{w}_k^* = \arg\max_{\|\mathbf{w}\|_2=1} \Big\{\mathbb{E}\!\big[G(\mathbf{w}^T Z)\big] - \mathbb{E}\!\big[G(\nu)\big]\Big\}^2",
            "summary": "Unmixes whitened fMRI data Z into K statistically independent, super-Gaussian spatial maps S by maximizing contrast function G (negentropy approximation) over orthogonal rotations.",
            "terms": [
                {"term": r"Z = \Sigma^{-1/2} X_c \implies \operatorname{Cov}(Z) = I_K", "role": "PCA Whitening Pre-Stage", "meaning": "Decorrelates second-order variance and scales all K principal directions to unit variance; any further orthogonal rotation W preserves Cov(WZ) = I_K.", "failure": "Stopping at PCA and assuming orthogonal variance components correspond to distinct biological sources."},
                {"term": r"\mathbb{E}[G(\mathbf{w}^T Z)] - \mathbb{E}[G(\nu)]", "role": "Non-Gaussianity (Negentropy) Contrast", "meaning": "By the Central Limit Theorem, a mixture of independent sources is more Gaussian than the individual sources; maximizing super-Gaussian sparsity recovers the unmixed sources.", "failure": "Trying to use ICA to separate purely Gaussian sources (where all rotations have identical distribution and ICA is unidentifiable)."},
                {"term": r"(\pm \alpha_k \mathbf{a}_k)\left(\pm \frac{1}{\alpha_k}\mathbf{s}_k^T\right)", "role": "Sign & Scale Indeterminacy", "meaning": "ICA components have arbitrary sign (+1/-1), arbitrary amplitude scaling, and arbitrary ordering.", "failure": "Comparing raw ICA map signs or amplitudes across subjects without dual regression or template matching."}
            ]
        }
    },
    "M06": {
        "commons_file": "File:Cluster-2.svg",
        "diagram_title": "Unsupervised Clustering (k-Means / Spectral / Hierarchical), Label Permutation & Split-Sample Stability",
        "diagram_guide": "A clustering algorithm will happily partition a continuous unimodal Gaussian cloud into K='subtypes' and produce highly significant ANOVA p-values between the clusters (because the clusters were defined to maximize between-cluster separation!). Validating clinical subtypes requires testing out-of-sample replication stability (Adjusted Rand Index, ARI) and testing against a continuous unimodal null.",
        "pipeline_steps": ["Fit Clustering on Discovery Split", "Align Arbitrary Cluster IDs (Hungarian Match)", "Compute Out-of-Sample Adjusted Rand Index (ARI)", "Test Against Unimodal Gaussian Continuum Null", "Verify External Clinical Utility"],
        "equation": {
            "name": "k-Means Within-Cluster Objective & Chance-Corrected Adjusted Rand Index (ARI)",
            "latex": r"\mathcal{J}_K = \sum_{k=1}^{K}\sum_{i \in C_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|_2^2, \qquad \text{ARI}(U, V) = \frac{\text{Index} - \mathbb{E}[\text{Index}]}{\max(\text{Index}) - \mathbb{E}[\text{Index}]} \in [-1, 1]",
            "summary": "Minimizes within-cluster sum of squares (which monotonically decreases with K) and evaluates partition reproducibility across resamples via chance-adjusted pair agreement (ARI).",
            "terms": [
                {"term": r"\mathcal{J}_K \downarrow \text{ monotonically with } K", "role": "Non-Inferential Within-Cluster Loss", "meaning": "Adding more clusters K always reduces within-cluster variance, even on a single isotropic Gaussian ball.", "failure": "Running a post-hoc t-test or ANOVA on the features used to form the clusters to 'prove' the clusters are distinct (circular!)."},
                {"term": r"\text{ARI}(U, V)", "role": "Permutation-Invariant Partition Agreement", "meaning": "Measures pairwise co-assignment agreement between two clusterings independent of arbitrary integer label numbering (0.0 = random chance, 1.0 = identical).", "failure": "Comparing raw cluster integers (Cluster 1 vs Cluster 1) across bootstrap runs without Hungarian label matching or ARI."},
                {"term": r"H_0: \text{Single Multivariate Gaussian}", "role": "Continuum vs. Discrete Subtype Null", "meaning": "Tests whether the observed silhouette or gap statistic exceeds what arises when slicing a continuous severity spectrum into K bins.", "failure": "Declaring '3 biological biotypes' when the data simply follow a continuous 1D severity gradient."}
            ]
        }
    },
    "M07": {
        "commons_file": "File:White_Matter_Connections_Obtained_with_MRI_Tractography.png",
        "diagram_title": "Connectome Graph Theory: Thresholding Choices, Degree-Preserving Nulls & Connectome-Based Predictive Modeling (CPM)",
        "diagram_guide": "Turning a P x P correlation matrix into a graph requires choosing how to handle negative edges, proportional vs. absolute thresholds, and weighted vs. binary metrics. A proportional threshold (e.g., top 10% edges) fixes edge density across participants, but shifts overall mean correlation shifts into spurious topology changes unless checked against Maslov-Sneppen degree-preserving null networks!",
        "pipeline_steps": ["Construct P x P Fisher-z Connectome", "Compare Absolute vs. Proportional Density Thresholds", "Compute Clustering C & Path Length L", "Normalize Against Maslov-Sneppen Rewired Nulls", "Run Fold-Isolated CPM Behavior Prediction"],
        "equation": {
            "name": "Weighted Clustering Coefficient, Small-Worldness & Maslov-Sneppen Null Normalization",
            "latex": r"C_i = \frac{2\,t_i}{k_i(k_i - 1)}, \qquad \sigma_{\text{SW}} = \frac{C / C_{\text{rand}}}{L / L_{\text{rand}}}, \qquad S_{\text{CPM}, i}^{+} = \sum_{(p,q) \in \hat{E}_{\text{pos}}^{(\text{train})}} z_{i, pq}",
            "summary": "Measures local triangle density C_i, normalizes global clustering and path length against degree-preserving random graphs, and summarizes predictive edges inside training folds (CPM).",
            "terms": [
                {"term": r"k_i = \sum_j A_{ij}, \; t_i = \frac{1}{2}(A^3)_{ii}", "role": "Node Degree & Local Triangle Count", "meaning": "Counts connected neighbors k_i and closed triads t_i around parcel i; strongly driven by total network density.", "failure": "Comparing unnormalized clustering C or path length L across groups that differ in mean edge weight or network density."},
                {"term": r"C_{\text{rand}}, \, L_{\text{rand}}", "role": "Degree-Distribution-Preserving Reference", "meaning": "Ensemble average over graphs randomized via double-edge swaps that preserve every node's exact degree k_i.", "failure": "Using Erdos-Renyi uniform random graphs that ignore heavy-tailed hub degree distributions."},
                {"term": r"\hat{E}_{\text{pos}}^{(\text{train})}", "role": "Train-Only CPM Edge Mask (Shen et al., 2017)", "meaning": "Set of connectome edges significantly correlated with behavior inside the training fold, summed to predict held-out participants.", "failure": "Selecting predictive CPM edges across all participants before cross-validation."}
            ]
        }
    },
    "M08": {
        "commons_file": "File:Orthogonal_projection.svg",
        "diagram_title": "Representational Similarity Analysis (RSA), Cross-Validated Mahalanobis (Crossnobis) Distance & Noise Ceilings",
        "diagram_guide": "RSA abstracts away from individual voxel locations by comparing the K x K Representational Dissimilarity Matrix (RDM) of pairwise condition distances against computational models. Critically, ordinary Euclidean/squared distance d^2 is strictly positive even under pure noise—whereas the cross-validated Mahalanobis (Crossnobis) estimator multiplies pattern differences across independent runs (Run A x Run B) so its expected value under zero true distance is exactly 0.0 (Walther et al., 2016)!",
        "pipeline_steps": ["Estimate Condition Betas per Run", "Spatial Noise Whitening via Sigma_V^{-1/2}", "Compute Cross-Run Inner Product (Crossnobis)", "Vectorize Upper Triangle of K x K RDM", "Compare to Model RDM Within Noise Ceiling"],
        "equation": {
            "name": "Unbiased Cross-Validated Mahalanobis (Crossnobis) Representational Distance",
            "latex": r"\hat{d}_{\text{cross}}^2(j, k) = \frac{1}{M(M-1)}\sum_{m \neq m'} \left(\hat{\boldsymbol{\beta}}_{j}^{(m)} - \hat{\boldsymbol{\beta}}_{k}^{(m)}\right)^T \hat{\Sigma}_{V}^{-1} \left(\hat{\boldsymbol{\beta}}_{j}^{(m')} - \hat{\boldsymbol{\beta}}_{k}^{(m')}\right)",
            "summary": "Eliminates positive squared-noise bias by taking the noise-whitened inner product of condition-difference patterns across independent imaging runs m != m'.",
            "terms": [
                {"term": r"\left(\hat{\boldsymbol{\beta}}_j^{(m)} - \hat{\boldsymbol{\beta}}_k^{(m)}\right)", "role": "Run-Specific Multivoxel Condition Contrast", "meaning": "Difference pattern between Stimulus j and Stimulus k in run m; contains true neural separation delta_{jk} plus run-specific noise epsilon^{(m)}.", "failure": "Using non-cross-validated squared Euclidean distance ||beta_j - beta_k||^2, where unequal condition trial counts or noise variances create false RDM structure!"},
                {"term": r"\hat{\Sigma}_V^{-1} \text{ (Shrinkage Spatial Precision)}", "role": "Multivariate Voxel Noise Whitening", "meaning": "Downweights noisy voxels and decorrelates spatial covariance estimated from GLM residuals via Ledoit-Wolf shrinkage.", "failure": "Inverting sample voxel covariance without shrinkage when V_roi > T."},
                {"term": r"\mathbb{E}[\boldsymbol{\varepsilon}^{(m)T}\Sigma^{-1}\boldsymbol{\varepsilon}^{(m')}] = 0", "role": "Cross-Run Zero-Bias Guarantee", "meaning": "Because noise in run m is independent of noise in run m', the cross-product has zero expectation under H0: delta_{jk} = 0 (allowing small negative sample estimates around zero).", "failure": "Clamping negative Crossnobis distances to zero, which re-introduces positive bias."}
            ]
        }
    },
    "M09": {
        "commons_file": "File:Gaussian_2d_0_degrees.png",
        "diagram_title": "Multivariate Searchlight Mapping: Neighborhood Radius, Rim Smearing & Directionality Confounds",
        "diagram_guide": "A searchlight steps a spherical window of radius R (e.g., 3–4 voxels) across the brain, running cross-validated MVPA/RSA inside each sphere and writing the score at the sphere's center voxel (Kriegeskorte et al., 2006). Consequently, a center voxel that contains ZERO true signal will still score above chance if its sphere overlaps a neighboring informative voxel a few millimeters away (rim smearing)!",
        "pipeline_steps": ["Define Spherical Neighborhood B_R(v)", "Intersect Sphere with Brain Mask", "Run Cross-Validated Decoder Inside Sphere", "Assign Score to Center Voxel v", "Audit Spatial Rim Dilation & Mean-Difference Confound"],
        "equation": {
            "name": "Searchlight Neighborhood Support & Spatial Dilation Bound",
            "latex": r"s_R(v) = \mathcal{A}_{\text{CV}}\!\left(X_{(:, \, \mathcal{B}_R(v) \cap M)}, \, \mathbf{y}\right), \qquad \operatorname{supp}(s_R > \text{chance}) = \operatorname{supp}(\text{Signal}) \oplus \mathcal{B}_R(0)",
            "summary": "Maps each voxel v to the cross-validated score of its spherical neighborhood B_R(v), which dilates any point source by the searchlight radius R.",
            "terms": [
                {"term": r"\mathcal{B}_R(v) = \{u \in M : \|\mathbf{x}_u - \mathbf{x}_v\|_2 \le R\}", "role": "Local Spherical Voxel Patch", "meaning": "All in-mask voxels within physical radius R (mm) of center voxel v.", "failure": "Defining searchlight spheres in voxel indices on anisotropic grids, creating ellipsoids instead of physical spheres."},
                {"term": r"\operatorname{supp}(\text{Signal}) \oplus \mathcal{B}_R(0)", "role": "Minkowski Dilation Rim Effect", "meaning": "A single informative voxel at u0 makes every center voxel v within distance R appear informative, dilating the apparent region by +R in every direction.", "failure": "Claiming fine-grained anatomical boundary localization from the outer rim of a 10 mm searchlight map (Etzel et al., 2013)."},
                {"term": r"\bar{x}_{\text{patch}} \text{ vs. Fine Pattern}", "role": "Univariate vs. Multivariate Confound", "meaning": "A linear searchlight classifier succeeds both when a region has a fine-grained multivoxel pattern AND when all voxels simply shift their mean together.", "failure": "Concluding a searchlight hit proves 'distributed multivariate coding' without comparing against the univariate regional mean."}
            ]
        }
    },
    "M10": {
        "commons_file": "File:Acf_new.svg",
        "diagram_title": "Naturalistic Paradigms: Inter-Subject Correlation (ISC), Shared Response Model (SRM) & Phase Randomization",
        "diagram_guide": "During continuous movie watching or story listening, time-locked stimulus fluctuations drive shared brain dynamics across viewers. Leave-One-Out Inter-Subject Correlation (ISC) isolates stimulus-locked signal from intrinsic noise, while the Shared Response Model (SRM) learns orthogonal subject-specific spatial bases W_i to align idiosyncratic functional topographies into a low-dimensional shared time course S.",
        "pipeline_steps": ["Align Movie Timestamps Across Viewers", "Compute Leave-One-Out ISC_i = corr(x_i, x-bar_{-i})", "Generate Phase-Randomized Surrogate Nulls", "Fit Orthogonal SRM Bases W_i on Train TRs", "Evaluate Shared Time-Segment Matching on Test TRs"],
        "equation": {
            "name": "Leave-One-Out Inter-Subject Correlation (ISC) & Shared Response Model (SRM)",
            "latex": r"\text{ISC}_i(v) = \operatorname{corr}\!\left(\mathbf{x}_{i,v}, \; \frac{1}{N-1}\sum_{j \neq i}\mathbf{x}_{j,v}\right), \qquad \min_{W_i, S} \sum_{i=1}^{N} \|X_i - W_i S\|_F^2 \quad \text{s.t. } W_i^T W_i = I_k",
            "summary": "Measures stimulus-locked temporal synchrony via leave-one-out group correlation and aligns fine-scale functional topography across subjects via orthogonal transformations W_i.",
            "terms": [
                {"term": r"\frac{1}{N-1}\sum_{j \neq i}\mathbf{x}_{j,v}", "role": "Leave-One-Out Group Template", "meaning": "Averages all OTHER N-1 viewers to suppress subject-specific spontaneous noise while preventing participant i from correlating with themselves.", "failure": "Correlating participant i with the full group mean including participant i, which injects a positive 1/N self-correlation bias!"},
                {"term": r"W_i^T W_i = I_k \text{ (Orthogonal Basis)}", "role": "Geometry-Preserving Functional Hyperalignment", "meaning": "Maps subject i's V voxels into k shared latent features without stretching variance arbitrarily, fitted strictly on training movie segments.", "failure": "Fitting SRM transformation matrices W_i on the full movie and then evaluating classification on the same movie segments."},
                {"term": r"\tilde{x}(t) = \mathcal{F}^{-1}\!\left\{|\hat{x}(\omega)| e^{i\phi_{\text{rand}}(\omega)}\right\}", "role": "Phase-Randomized Autocorrelation Null", "meaning": "Preserves the exact power spectrum and temporal autocorrelation of slow movie BOLD signals while destroying cross-subject phase locking.", "failure": "Using naive time-point shuffling or parametric t-tests that ignore the massive autocorrelation of continuous movie fMRI."}
            ]
        }
    },
    "M11": {
        "commons_file": "File:Reparameterized_Variational_Autoencoder.png",
        "diagram_title": "Generative Latent-Variable Models, Posterior Predictive Checks & Prior vs. Data Dominance",
        "diagram_guide": "A generative model specifies a joint distribution p(z, x) = p(z) p(x | z) capable of synthesizing realistic new data. Fitting a generative model requires more than matching the sample mean: Posterior Predictive Checks (PPCs) test whether simulated datasets x_rep drawn from the fitted model reproduce variance, covariance, skewness, and tail behavior!",
        "pipeline_steps": ["Specify Latent Prior p(z) & Likelihood p(x | z)", "Infer Posterior p(z | x) (Exact / Variational ELBO)", "Draw Replicated Datasets x_rep ~ p(x_rep | x)", "Run Posterior Predictive Discrepancy Checks T(x_rep)", "Audit Prior Sensitivity Under Low SNR"],
        "equation": {
            "name": "Linear-Gaussian Generative Factor Model & Evidence Lower Bound (ELBO)",
            "latex": r"\mathbf{x} = \Lambda\mathbf{z} + \boldsymbol{\varepsilon} \implies \Sigma_X = \underbrace{\Lambda\Lambda^T}_{\text{Low-Rank Shared}} + \underbrace{\Psi}_{\text{Diagonal Noise}}, \qquad \ln p(\mathbf{x}) \ge \mathbb{E}_{q(\mathbf{z}\mid\mathbf{x})}[\ln p(\mathbf{x}\mid\mathbf{z})] - D_{\text{KL}}\!\big(q(\mathbf{z}\mid\mathbf{x}) \,\|\, p(\mathbf{z})\big)",
            "summary": "Partitions observed covariance into low-rank latent structure Lambda*Lambda^T plus idiosyncratic sensor noise Psi, and decomposes marginal log-evidence into reconstruction accuracy minus KL divergence from the prior.",
            "terms": [
                {"term": r"\Lambda\Lambda^T + \Psi", "role": "Structured Covariance Decomposition", "meaning": "Generates off-diagonal correlations across brain regions using K << P latent factors z while isolating region-specific noise in diagonal Psi.", "failure": "Judging a generative model solely by whether its mean matches the data mean while its simulated covariance is completely wrong."},
                {"term": r"\mathbb{E}_{q}[\ln p(\mathbf{x}\mid\mathbf{z})]", "role": "Expected Log-Likelihood (Reconstruction Term)", "meaning": "Encourages latent codes z to explain the observed neuroimaging measurements x.", "failure": "Over-weighting the KL penalty (beta-VAE collapse), where q(z|x) collapses to the prior p(z) and ignores the input scan."},
                {"term": r"p_{\text{PPC}} = P\big(T(\mathbf{x}_{\text{rep}}) \ge T(\mathbf{x}_{\text{obs}}) \mid \mathbf{x}_{\text{obs}}\big)", "role": "Posterior Predictive Check (PPC)", "meaning": "Tests whether summary statistics T (e.g., max correlation, kurtosis, spectral slope) of synthetic draws match the real data.", "failure": "Interpreting latent variables as biological truth when Posterior Predictive Checks fail."}
            ]
        }
    },
    "M12": {
        "commons_file": "File:HMMGraph.svg",
        "diagram_title": "Hidden Markov Models (HMM), Viterbi State Segmentation & Event Dwell-Time Dynamics",
        "diagram_guide": "Brain network configurations and narrative event representations transition between discrete metastable states z_t in {1..K} governed by a Markov transition matrix A_{jk} = P(z_t = k | z_{t-1} = j) (Vidaurre et al., 2017; Baldassano et al., 2017). The Viterbi dynamic-programming algorithm finds the globally most probable state sequence, whereas greedy frame-by-frame classification ignores transition continuity and chatters on noise!",
        "pipeline_steps": ["Specify State Count K & Emission Model p(x_t | z_t=k)", "Run Forward-Backward Baum-Welch (EM) in Log-Space", "Decode Global State Sequence via Viterbi", "Extract Fractional Occupancy & Mean Dwell Time", "Align Permuted State Labels Across Subjects"],
        "equation": {
            "name": "HMM Log-Domain Viterbi Recursion & State Dwell-Time Distribution",
            "latex": r"\delta_t(k) = \ln p(\mathbf{x}_t \mid z_t = k) + \max_{j \in \{1..K\}}\!\big(\delta_{t-1}(j) + \ln A_{jk}\big), \qquad \mathbb{E}[\text{Dwell}_k] = \frac{\text{TR}}{1 - A_{kk}}",
            "summary": "Propagates log-probabilities of the most likely state path through time using transition log-probabilities ln A_{jk}, with expected state duration governed by self-transition probability A_{kk}.",
            "terms": [
                {"term": r"\ln p(\mathbf{x}_t \mid z_t = k)", "role": "State-Conditional Emission Log-Likelihood", "meaning": "Measures how well frame t's multivoxel pattern or regional covariance matches state k's distribution.", "failure": "Multiplying raw emission probabilities across T=500 frames without log-sum-exp scaling, which underflows to 0.0 within 20 TRs."},
                {"term": r"\max_j (\delta_{t-1}(j) + \ln A_{jk})", "role": "Markov Transition Regularization", "meaning": "Penalizes implausible rapid state jumps when self-transition probability A_{kk} is high.", "failure": "Taking independent argmax_k p(x_t | k) at each frame without transition matrix A, creating rapid high-frequency state chattering."},
                {"term": r"\text{TR} / (1 - A_{kk})", "role": "Geometric Mean Dwell Time (Seconds)", "meaning": "Expected duration the brain remains in state k before switching; constrained by hemodynamic sluggishness unless deconvolved.", "failure": "Interpreting 1-TR HMM jumps in raw BOLD as millisecond neural microstates without accounting for HRF autocorrelation."}
            ]
        }
    },
    "M13": {
        "commons_file": "File:DCM_for_fMRI.svg",
        "diagram_title": "State-Space Latent Dynamics, Kalman Filtering & Dynamic Causal Modeling (DCM)",
        "diagram_guide": "In Dynamic Causal Modeling (Friston et al., 2003) and linear dynamical systems, unobserved neural states z_t evolve via directed effective connectivity A and stimulus-modulated coupling B^{(u)}, and pass through a region-specific hemodynamic forward model to produce observed BOLD y_t. Because each region has its own sluggish hemodynamic transit time, lag-based Granger causality on raw BOLD can get the direction of neural information flow completely backward!",
        "pipeline_steps": ["State Latent Neural Dynamics dz/dt = (A + u B)z + C u", "Couple to Hemodynamic Observation Model y_t", "Run Kalman Filter (Predict -> Innovation -> Gain Update)", "Compare Candidate Circuit Graphs via Free Energy / BIC", "Audit Hemodynamic Lag Confounding"],
        "equation": {
            "name": "Dynamic Causal Modeling (DCM) Bilinear State Equation & Kalman Gain Update",
            "latex": r"\dot{\mathbf{z}}(t) = \Big(\underbrace{A}_{\text{Intrinsic}} + \sum_{m} u_m(t)\underbrace{B^{(m)}}_{\text{Modulatory}}\Big)\mathbf{z}(t) + \underbrace{C}_{\text{Driving}}\mathbf{u}(t), \qquad \hat{\mathbf{z}}_{t\mid t} = \hat{\mathbf{z}}_{t\mid t-1} + K_t\big(\mathbf{y}_t - H\hat{\mathbf{z}}_{t\mid t-1}\big)",
            "summary": "Separates baseline directed coupling A, context-dependent modulation B^{(m)}, and external sensory input C in latent neural space, and updates state estimates via Kalman gain K_t.",
            "terms": [
                {"term": r"A + \sum_m u_m(t) B^{(m)}", "role": "Effective Connectivity & Context Modulation", "meaning": "Matrix A encodes fixed directed synaptic drive between regions (with negative self-inhibition A_{ii} < 0 for stability); B^{(m)} changes specific directed pathways under task context u_m.", "failure": "Allowing positive real eigenvalues in A, causing latent neural states to explode exponentially."},
                {"term": r"K_t = P_{t\mid t-1} H^T (H P_{t\mid t-1} H^T + R)^{-1}", "role": "Optimal Kalman Precision Gain", "meaning": "Weights the prediction error (innovation y_t - H z-hat) by the ratio of state uncertainty P to observation noise R.", "failure": "Confusing directed effective connectivity in a small hypothesis-driven 3-node DCM with unconstrained whole-brain causal discovery."},
                {"term": r"\text{Region-Specific HRF Delay } \tau_r", "role": "Vascular-Lag Confound Separator", "meaning": "If Region 1 drives Region 2 neurally (+20 ms), but Region 1 has a slower venous transit time (+1.5 s), Region 2's BOLD peak precedes Region 1's BOLD peak!", "failure": "Inferring directed neural causality from temporal lag (Granger causality) on raw, un-deconvolved BOLD time series."}
            ]
        }
    },
    "M14": {
        "commons_file": "File:Comparison_image_neural_networks.svg",
        "diagram_title": "Convolutional Neural Networks (CNNs), Receptive Fields, Backpropagation & Numerical Gradient Checking",
        "diagram_guide": "A convolutional layer slides shared local kernel weights W across spatial coordinates, preserving translation equivariance while reducing parameter count by orders of magnitude compared to a dense layer. Training relies on the chain rule (backpropagation)—which must always be verified against central finite differences and checked for vanishing/exploding norms and small-sample overfitting!",
        "pipeline_steps": ["Forward Pass: Conv -> ReLU -> Pool -> Linear", "Compute Cross-Entropy / MSE Loss L", "Backward Pass: Chain-Rule Gradients dL/dW", "Verify Against Central Finite Differences", "Audit Train-vs-Validation Generalization Gap"],
        "equation": {
            "name": "Spatial Convolution, Backpropagation Chain Rule & Central Finite-Difference Check",
            "latex": r"h_{c, x} = \sigma\!\left(b_c + \sum_{m}\sum_{u=-k}^{k} W_{c, m, u} \, X_{m, x+u}\right), \qquad \frac{\partial \mathcal{L}}{\partial W_{ij}} \approx \frac{\mathcal{L}(W + \epsilon E_{ij}) - \mathcal{L}(W - \epsilon E_{ij})}{2\epsilon} + \mathcal{O}(\epsilon^2)",
            "summary": "Applies shared local filter weights W across spatial positions x and verifies analytical backpropagation gradients to O(epsilon^2) accuracy via central finite differences.",
            "terms": [
                {"term": r"W_{c, m, u} \text{ (Shared Spatial Kernel)}", "role": "Translation-Equivariant Local Filter", "meaning": "Detects local edge/texture motifs using the same small parameter tensor across the volume.", "failure": "Assuming translation invariance is always desirable in registered MNI brains where absolute anatomical coordinates carry meaning."},
                {"term": r"\frac{\partial \mathcal{L}}{\partial W} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}} \cdot \frac{\partial \mathbf{z}}{\partial W}", "role": "Backpropagation Chain Rule", "meaning": "Propagates error sensitivities backward from the output loss through each layer's local Jacobian.", "failure": "Calling optimizer.step() without zeroing previous gradients, or omitting ReLU derivative masks (z > 0) during backward pass."},
                {"term": r"\frac{\|\nabla_{\text{analytic}} - \nabla_{\text{numeric}}\|_2}{\|\nabla_{\text{analytic}}\|_2 + \|\nabla_{\text{numeric}}\|_2} < 10^{-6}", "role": "Relative Gradient Verification Gate", "meaning": "Certifies that analytical backprop matches central finite differences before training.", "failure": "Training a 5-million-parameter 3D CNN on N=80 subjects without comparing against a simple Ridge baseline."}
            ]
        }
    },
    "M15": {
        "commons_file": "File:Example_architecture_of_U-Net_for_producing_k_256-by-256_image_masks_for_a_256-by-256_RGB_image.png",
        "diagram_title": "3D Medical Segmentation (U-Net), Severe Class Imbalance, Soft Dice Loss & Subject-Level Splits",
        "diagram_guide": "In white-matter lesion, tumor, or small-nucleus segmentation, the target structure often occupies <0.5% of the volume (99.5% background). Optimizing unweighted voxelwise Cross-Entropy rewards a lazy network that predicts 100% background (achieving 99.5% voxel accuracy and 0.00 Dice!), whereas Soft Dice + Focal loss directly optimizes overlap—and splits MUST be at the participant level, never slicing 2D axial slices from the same brain across train and test!",
        "pipeline_steps": ["Partition Strictly by Participant ID (Never by 2D Slice!)", "Audit Foreground Voxel Fraction (<1%)", "Train with Combined Soft Dice + BCE/Focal Loss", "Evaluate Soft Dice, Calibration & Hausdorff Distance", "Inspect False-Positive & False-Negative Overlays"],
        "equation": {
            "name": "Differentiable Soft Dice Loss & Combined Dice + Cross-Entropy Objective",
            "latex": r"\mathcal{L}_{\text{SoftDice}}(\mathbf{p}, \mathbf{g}) = 1 - \frac{2\sum_{v=1}^{V} p_v g_v + \epsilon}{\sum_{v=1}^{V} p_v + \sum_{v=1}^{V} g_v + \epsilon}, \qquad \mathcal{L}_{\text{seg}} = \lambda_{\text{Dice}}\mathcal{L}_{\text{SoftDice}} + \lambda_{\text{CE}}\mathcal{L}_{\text{BCE}}",
            "summary": "Directly maximizes foreground intersection-over-sum using continuous predicted probabilities p_v while preserving smooth probability calibration via cross-entropy.",
            "terms": [
                {"term": r"2\sum_v p_v g_v / (\sum_v p_v + \sum_v g_v)", "role": "Class-Imbalance-Resistant Overlap Term", "meaning": "Evaluates overlap over foreground support rather than averaging over millions of trivial true-negative background voxels.", "failure": "Reporting 99.7% voxelwise accuracy on a lesion dataset where the model predicted an empty mask everywhere!"},
                {"term": r"\epsilon > 0 \text{ (Laplace Smoothing Guard)}", "role": "Empty-Mask Zero-Division Guard", "meaning": "Prevents 0/0 NaN gradients on slices or subjects that contain zero foreground lesion voxels.", "failure": "Training with pure Soft Dice without BCE calibration, which pushes all probabilities to extreme 0.0 or 1.0 saturation."},
                {"term": r"\text{Subject-Level Split}", "role": "Anti-Slice-Leakage Partition", "meaning": "All 2D slices or 3D patches from participant i must reside in the same split.", "failure": "Randomly splitting 2D axial slices across train and test sets, where adjacent slices 1 mm apart memorize the patient's skull and cortical folds!"}
            ]
        }
    },
    "M16": {
        "commons_file": "File:Denoising-autoencoder.png",
        "diagram_title": "Self-Supervised Pretraining (3D Masked Autoencoders / Contrastive SSL), Linear Probing vs. Fine-Tuning",
        "diagram_guide": "Neuroimaging foundation models (BrainIAC `PM03`, MindEye2 `PM06`) pretrain a backbone f_theta on tens of thousands of unlabeled brain scans via 3D Masked Autoencoding (reconstructing masked patches) or contrastive learning, then adapt to small clinical cohorts via frozen linear probing or low-learning-rate fine-tuning.",
        "pipeline_steps": ["Verify Zero Subject/Site Overlap with Pretrain Cohort", "Pretrain Encoder f_theta on Masked 3D Patches", "Stage 1: Frozen Linear Probe on Downstream Task", "Stage 2: Low-LR End-to-End Fine-Tuning", "Ablate Against Matched Scratch & Ridge Baselines"],
        "equation": {
            "name": "Masked Autoencoder (MAE) Pretraining Objective & Linear Probe vs. Fine-Tuning",
            "latex": r"\mathcal{L}_{\text{MAE}}(\theta, \phi) = \frac{1}{|M_{\text{mask}}|}\sum_{p \in M_{\text{mask}}} \left\| \mathbf{x}_p - g_{\phi}\!\big(f_{\theta}(\mathbf{x}_{\text{vis}})\big)_p \right\|_2^2, \qquad \hat{y} = \mathbf{w}^T f_{\theta^*}(\mathbf{x}) + b",
            "summary": "Trains encoder f_theta to compress visible brain patches x_vis into latent representations that reconstruct masked anatomical/functional patches, then adapts to downstream labels.",
            "terms": [
                {"term": r"p \in M_{\text{mask}}", "role": "Masked Patch Reconstruction Target", "meaning": "Computes MSE loss strictly on the held-out masked 3D patches (e.g., 75% masked) so the encoder must learn anatomical context rather than copying input voxels.", "failure": "Computing reconstruction loss on visible unmasked patches, which learns a trivial identity copy."},
                {"term": r"f_{\theta^*}(\mathbf{x}) \text{ (Frozen Linear Probe)}", "role": "Representation Quality Diagnostic", "meaning": "Freezes pretrained weights theta* and fits only a regularized linear head w, preventing catastrophic forgetting on tiny N=50 clinical datasets.", "failure": "Unfreezing all layers with a large learning rate on N=40 subjects, destroying pretrained representations in 3 epochs."},
                {"term": r"\mathcal{D}_{\text{pretrain}} \cap \mathcal{D}_{\text{test}} = \emptyset", "role": "Biobank Pretraining Contamination Audit", "meaning": "Verifies that downstream test participants (e.g., UK Biobank / ABCD / ADNI) were not already inside the foundation model's pretraining checkpoint.", "failure": "Evaluating a 'zero-shot' foundation model on participants whose scans were used during self-supervised pretraining."}
            ]
        }
    },
    "M17": {
        "commons_file": "File:The-Transformer-model-architecture.png",
        "diagram_title": "Transformer Self-Attention on Brain Tokens (Omni-fMRI) & Foundation Model Card Auditing",
        "diagram_guide": "Neuroimaging Transformers tokenize parcel time segments or 3D patches into embeddings X, add spatial/temporal positional encodings, and mix information globally via Scaled Dot-Product Self-Attention. However, attention weights A = softmax(QK^T / sqrt(d_k)) are context-mixing weights—NOT causal synaptic connectivity or feature-importance proofs!",
        "pipeline_steps": ["Tokenize Brain Parcels/Patches + Positional Encoding", "Project Queries Q, Keys K, Values V", "Compute Scaled Dot-Product Attention A = softmax(QK^T/sqrt(d_k))", "Verify Permutation Equivariance Without Pos-Encoding", "Complete SOTA Model Card & Baseline Audit"],
        "equation": {
            "name": "Scaled Dot-Product Self-Attention (Vaswani et al., 2017)",
            "latex": r"\operatorname{Attention}(Q, K, V) = \underbrace{\operatorname{softmax}\!\left(\frac{Q K^T}{\sqrt{d_k}}\right)}_{A \in \mathbb{R}^{L \times L} \text{ (Row-Stochastic)}} V, \qquad Q = X W_Q, \; K = X W_K, \; V = X W_V",
            "summary": "Computes pairwise token compatibility Q K^T, scales by 1/sqrt(d_k) to prevent softmax saturation, and takes a convex combination of Value vectors V.",
            "terms": [
                {"term": r"1 / \sqrt{d_k}", "role": "Variance-Stabilizing Temperature Scale", "meaning": "For unit-variance d_k-dimensional vectors, dot products Q_i . K_j have variance d_k; dividing by sqrt(d_k) keeps logits O(1) so softmax gradients do not vanish.", "failure": "Omitting 1/sqrt(d_k), causing large d_k dot products to saturate softmax into hard one-hot spikes with near-zero gradients."},
                {"term": r"A_{ij} = \operatorname{softmax}(QK^T/\sqrt{d_k})_{ij}", "role": "Row-Stochastic Token Mixing Matrix", "meaning": "Non-negative weights summing to 1 across j for each query token i; depends on positional encodings and value norms ||V_j||.", "failure": "Interpreting raw attention matrix A_{ij} as directed effective brain connectivity or causal importance without value-norm and ablation checks."},
                {"term": r"X + E_{\text{pos}}", "role": "Anatomical & Temporal Coordinate Injection", "meaning": "Without positional encodings E_pos, self-attention is strictly permutation-equivariant and cannot tell visual cortex apart from motor cortex!", "failure": "Permuting parcel orders across datasets without matching the foundation model's fixed atlas parcellation."}
            ]
        }
    },
    "M18": {
        "commons_file": "File:Calibration_plot.png",
        "diagram_title": "Probability Calibration (ECE & Temperature Scaling), Explanation Fragility & Final Reproducibility Audit",
        "diagram_guide": "A clinical neuroimaging model with 0.85 ROC-AUC can still be dangerously miscalibrated—predicting 95% disease probability when only 60% of such patients actually have the condition! Post-hoc Temperature Scaling (dividing logits by T > 0 on a validation fold) calibrates probabilities (reducing Expected Calibration Error and Brier score) without changing rank order or AUC.",
        "pipeline_steps": ["Plot Reliability Diagram (Predicted p vs. Empirical Freq)", "Compute Expected Calibration Error (ECE) & Brier Score", "Fit Temperature T on Held-Out Validation Logits", "Test Explanation Map Perturbation & Collinearity Stability", "Freeze Final Model Card & Provenance Bundle"],
        "equation": {
            "name": "Expected Calibration Error (ECE), Brier Score & Logit Temperature Scaling",
            "latex": r"\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \Big|\operatorname{acc}(B_m) - \operatorname{conf}(B_m)\Big|, \qquad \hat{p}_i^{(T)} = \sigma\!\left(\frac{z_i}{T}\right), \qquad \text{Brier} = \frac{1}{N}\sum_{i=1}^{N}(\hat{p}_i - y_i)^2",
            "summary": "Measures the weighted gap between predicted confidence and empirical accuracy across M probability bins, and rescales overconfident logits z_i via validation temperature T.",
            "terms": [
                {"term": r"|\operatorname{acc}(B_m) - \operatorname{conf}(B_m)|", "role": "Within-Bin Calibration Gap", "meaning": "Absolute difference between the actual fraction of positive cases in confidence bin B_m and the model's average predicted probability in that bin.", "failure": "Deploying raw uncalibrated deep network or SVM scores as clinical risk probabilities based solely on ROC-AUC."},
                {"term": r"\sigma(z_i / T) \text{ with } T > 1", "role": "Order-Preserving Temperature Softening", "meaning": "Dividing overconfident logits z_i by T > 1 pulls extreme probabilities toward the base rate while preserving strict monotonic ranking (AUC unchanged).", "failure": "Fitting temperature T or isotonic calibration on the final test set instead of an inner validation split."},
                {"term": r"\operatorname{CosSim}\big(g(\mathbf{x}), g(\mathbf{x}+\boldsymbol{\delta})\big)", "role": "Explanation Perturbation Robustness", "meaning": "Tests whether saliency/attribution maps remain stable under small measurement noise or across bootstrap resamples.", "failure": "Presenting a single fragile gradient saliency map as definitive biological mechanism without stability and ablation checks."}
            ]
        }
    },
    "P01": {
        "commons_file": "File:Human_brain_anatomical_planes_letter_annotations.jpg",
        "diagram_title": "Project 1 · End-to-End Anatomical Transformation Pipeline & Provenance Audit",
        "diagram_guide": "Integrates PR01–PR08 and PR21 on a real structural template: verifying NIfTI RAS+ affine geometry, applying composite rigid/affine/nonlinear transformations, auditing interpolation order on continuous intensities vs. discrete labels, and checking Jacobian volume conservation.",
        "pipeline_steps": ["Load Anatomical Template & Audit RAS+ Affine", "Compose Rigid/Affine/Nonlinear Warps", "Resample Intensity (Spline) vs. Atlas (Nearest)", "Verify Jacobian Determinants (min J > 0)", "Emit Complete Transformation & QC Ledger"],
        "equation": {
            "name": "End-to-End Anatomical Volume & Coordinate Conservation Audit",
            "latex": r"\mathbf{x}_{\text{world}} = A_{\text{tpl}}\,\mathbf{i}_{\text{tpl}}, \qquad V_{\text{native}}(c) = |\det(A_{\text{nat}})|\sum_{\mathbf{i}} p_{\text{nat}, c}(\mathbf{i}) = |\det(A_{\text{tpl}})|\sum_{\mathbf{j}} p_{\text{unmod}, c}(\mathbf{j})\,J(\mathbf{j})",
            "summary": "Verifies physical coordinate mapping and proves that Jacobian-modulated template probabilities conserve exact native tissue volume in mm^3.",
            "terms": [
                {"term": r"A_{\text{tpl}}\,\mathbf{i}_{\text{tpl}}", "role": "World Coordinate Anchor", "meaning": "Guarantees every slice overlay and anatomical landmark is plotted in physical RAS+ millimeters.", "failure": "Misaligning template and overlay grids due to ignored qform/sform offsets."},
                {"term": r"p_{\text{unmod}, c}(\mathbf{j})\,J(\mathbf{j})", "role": "Jacobian-Modulated Voxel Mass", "meaning": "Restores local volume expansion/compression induced by nonlinear registration.", "failure": "Comparing unmodulated warped probabilities as if they measured total regional volume."},
                {"term": r"\text{Interpolation Contract}", "role": "Data-Type-Specific Resampler", "meaning": "Continuous spline interpolation for T1w intensities; order-0 nearest-neighbor for integer parcellation masks.", "failure": "Corrupting atlas ROI boundaries with linear interpolation."}
            ]
        }
    },
    "P02": {
        "commons_file": "File:Haemodynamic_response_function.svg",
        "diagram_title": "Project 2 · Single-Run Real Task fMRI GLM: Events, HRF Convolution, Drift, Residuals & Inference",
        "diagram_guide": "Applies D05–D10 and PR09–PR15 to the real SPM MoAEpilot auditory fMRI dataset: verifying BIDS TR and slice timing, convolving auditory blocks with the canonical HRF, adding cosine drift regressors, estimating the auditory > rest contrast map, and auditing lag-1 residual autocorrelation.",
        "pipeline_steps": ["Verify BIDS sub-01_task-auditory_bold.nii (TR=7s)", "Build HRF-Convolved Auditory + Cosine Drift Design X", "Fit Voxelwise GLM Inside Brain Mask", "Compute Contrast, SE, t-Map & Effect Size", "Audit Raw Residual Lag-1 Autocorrelation"],
        "equation": {
            "name": "Single-Run Task fMRI General Linear Model & Residual Autocorrelation Diagnostic",
            "latex": r"\mathbf{y}_v = \underbrace{X_{\text{task}}\boldsymbol{\beta}_{\text{task}, v}}_{\text{HRF-Convolved Auditory}} + \underbrace{X_{\text{drift}}\boldsymbol{\beta}_{\text{drift}, v}}_{\text{DCT Low-Freq Drift}} + \boldsymbol{\varepsilon}_v, \qquad \hat{\rho}_1(v) = \frac{\sum_{t=2}^{T} \hat{\varepsilon}_{v,t}\hat{\varepsilon}_{v,t-1}}{\sum_{t=1}^{T}\hat{\varepsilon}_{v,t}^2}",
            "summary": "Models each voxel's BOLD time series as a sum of HRF-convolved task predictors and discrete cosine drift terms, then audits temporal autocorrelation in the residuals.",
            "terms": [
                {"term": r"X_{\text{task}} = (s_{\text{auditory}} * h)\big|_{t_n}", "role": "Scan-Sampled Hemodynamic Predictor", "meaning": "Auditory block boxcar convolved with canonical double-gamma HRF and sampled at the 84 retained TRs (TR=7.0 s).", "failure": "Misaligning event onsets when initial dummy scans were already discarded."},
                {"term": r"X_{\text{drift}}", "role": "Discrete Cosine High-Pass Basis", "meaning": "Models slow scanner baseline drift jointly inside the GLM design matrix.", "failure": "Omitting drift terms, allowing slow baseline ramps to inflate residual variance sigma-hat^2."},
                {"term": r"\hat{\rho}_1(v)", "role": "Lag-One Residual Autocorrelation Map", "meaning": "Quantifies serial correlation remaining in OLS residuals to determine whether GLS prewhitening is required.", "failure": "Claiming single-subject OLS t-values represent population-level inference."}
            ]
        }
    },
    "P03": {
        "commons_file": "File:K-fold_cross_validation_EN.svg",
        "diagram_title": "Project 3 · Multi-Site Cohort Prediction, Unseen-Site Generalization & Harmonization Audit",
        "diagram_guide": "Synthesizes DS05, DS08, DS15, and M02–M04 on a multi-site clinical cohort: demonstrating how site-confounded sampling tricks a pooled CV model into learning scanner site shortcuts, and implementing strict Leave-One-Site-Out (LOSO) evaluation with fold-isolated preprocessing and participant-level bootstrap intervals.",
        "pipeline_steps": ["Audit Site x Outcome Confounding", "Compare Pooled K-Fold vs. Leave-One-Site-Out (LOSO)", "Fit Imputer, Scaler & Feature Screen Inside Train Sites", "Apply Label-Free Per-Site / Train-Only Harmonization", "Compute Participant Bootstrap CIs & Permutation p"],
        "equation": {
            "name": "Leave-One-Site-Out (LOSO) Risk & Shortcut-Confounded Pooled Bias",
            "latex": r"\mathcal{R}_{\text{LOSO}}(s^*) = \frac{1}{|S_{s^*}|}\sum_{i \in S_{s^*}} \ell\!\left(f_{\hat{\boldsymbol{\theta}}_{(-s^*)}}\!\big(\mathcal{H}_{(-s^*)}(\mathbf{x}_i)\big), \, y_i\right), \qquad \Delta_{\text{shortcut}} = \text{AUC}_{\text{pooled CV}} - \text{AUC}_{\text{LOSO}}",
            "summary": "Evaluates predictive performance on a completely held-out scanner site s* using parameters theta_{(-s*)} fitted exclusively on the remaining training sites.",
            "terms": [
                {"term": r"S_{s^*} \text{ (Held-Out Scanner Site)}", "role": "External Site Generalization Test Set", "meaning": "Participants scanned on an unseen scanner s* that never contributed a single training row or outcome label.", "failure": "Using random pooled K-fold CV across a multi-site dataset where site prevalence differs, inflating AUC via scanner-fingerprinting shortcuts."},
                {"term": r"\mathcal{H}_{(-s^*)}(\mathbf{x}_i)", "role": "Label-Free / Train-Fitted Harmonizer", "meaning": "Site standardization or harmonization that never peeks at test-site outcome labels y_{s*}.", "failure": "Running ComBat with target diagnosis y included in the covariate matrix across all sites before splitting."},
                {"term": r"\Delta_{\text{shortcut}}", "role": "Site-Shortcut Inflation Gap", "meaning": "Drop in performance between pooled random CV and unseen-site LOSO evaluation, quantifying how much the model relied on site confounding.", "failure": "Deploying a clinical classifier without reporting worst-site and unseen-site performance."}
            ]
        }
    },
    "P04": {
        "commons_file": "File:Generic_forest_plot.png",
        "diagram_title": "Project 4 · Preregistered Multiverse Research Proposal, SOTA Audit & Oral Defense",
        "diagram_guide": "Culminating capstone synthesis: connecting a foundational paper and a SOTA model paper to a concrete, falsifiable neuroimaging research plan with frozen estimand, causal graph, BIDS/QC exclusion rules, primary + multiverse analysis branches, leakage-free validation split, and explicit claim boundaries.",
        "pipeline_steps": ["Freeze Estimand, Causal DAG & Target Population", "Specify BIDS Metadata & Pre-Analysis QC Gate", "Define Primary Pipeline + Multiverse Grid Pi", "Verify Null Calibration & Out-of-Sample Split", "Defend Claim Boundaries Against Reviewer Audit"],
        "equation": {
            "name": "Preregistered Decision & Claim-Boundary Verification Contract",
            "latex": r"\text{Claim}(\mathcal{D}_{\text{test}}) \iff \underbrace{\text{QC}(\mathcal{D}_{\text{test}}) = 1}_{\text{Pre-Specified Gate}} \;\wedge\; \underbrace{\hat{\theta}(\pi_0) \notin [-\Delta, +\Delta]}_{\text{Primary Estimand Effect}} \;\wedge\; \underbrace{\text{Share}_{\text{robust}}(\Pi_{\text{valid}}) \ge \gamma_{\min}}_{\text{Multiverse Stability}}",
            "summary": "Requires a scientific claim to pass pre-specified data quality gates, exceed the smallest effect size of interest on the primary pipeline pi_0, and remain stable across the pre-committed multiverse Pi_valid.",
            "terms": [
                {"term": r"\text{QC}(\mathcal{D}_{\text{test}}) = 1", "role": "Blinded Pre-Outcome Quality Gate", "meaning": "All participant/run exclusion criteria (FD, coverage, Euler number) are frozen and executed before inspecting any outcome or group contrast.", "failure": "Tweaking motion exclusion thresholds after seeing the p-value."},
                {"term": r"\hat{\theta}(\pi_0) \notin [-\Delta, +\Delta]", "role": "Primary Estimand & SESOI Test", "meaning": "Evaluates the pre-committed primary estimator against a biologically meaningful effect-size margin Delta with family-wise / FDR error control.", "failure": "Conflating statistical significance with biological or clinical effect magnitude."},
                {"term": r"\text{Share}_{\text{robust}}(\Pi_{\text{valid}}) \ge \gamma_{\min}", "role": "Multiverse Specification Robustness", "meaning": "Verifies that the scientific conclusion does not depend on a single fragile smoothing, parcellation, or denoising choice.", "failure": "Overclaiming causal or clinical universality beyond the sampled population and scanner domain."}
            ]
        }
    },
}


def resolve_commons_metadata(file_titles):
    """Fetch canonical image URLs, descriptions, and licenses from Wikimedia Commons API."""
    unique_titles = sorted(set(file_titles))
    resolved = {}
    for i in range(0, len(unique_titles), 45):
        batch = unique_titles[i:i + 45]
        params = urllib.parse.urlencode({
            "action": "query",
            "titles": "|".join(batch),
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": 960,
            "format": "json",
        })
        url = f"https://commons.wikimedia.org/w/api.php?{params}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AINeuroimagingCourseBot/1.0 (https://github.com/Bowenislandsong/ai-neuroimaging-course)"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for page in data.get("query", {}).get("pages", {}).values():
            ii = page.get("imageinfo", [{}])[0]
            if not ii.get("url"):
                continue
            meta = ii.get("extmetadata", {})
            lic = meta.get("LicenseShortName", {}).get("value", "CC BY-SA / Public Domain")
            artist = meta.get("Artist", {}).get("value", "Wikimedia Commons")
            orig_url = ii.get("url", "").split("?")[0]
            thumb_url = (ii.get("thumburl") or orig_url).split("?")[0]
            desc_url = ii.get("descriptionurl", "").split("?")[0]
            resolved[page["title"]] = {
                "url": orig_url,
                "thumb_url": thumb_url,
                "page_url": desc_url,
                "license": lic,
            }
    return resolved


def main():
    combined = {}
    combined.update(ENRICHMENT_PART1)
    combined.update(ENRICHMENT_PART2)
    assert len(combined) == 83, f"Expected 83 classes, got {len(combined)}"

    all_files = [v["commons_file"] for v in combined.values()]
    commons_map = resolve_commons_metadata(all_files)

    out = {}
    for cid, (week, phase, order_idx) in sorted(SCHEDULE_MAP.items(), key=lambda x: x[1][2]):
        item = dict(combined[cid])
        cf = item["commons_file"].replace("_", " ")
        cmeta = commons_map.get(cf) or commons_map.get(item["commons_file"])
        if not cmeta:
            raise RuntimeError(f"Failed to resolve Wikimedia Commons diagram for {cid}: {item['commons_file']}")
        item["week"] = week
        item["phase"] = phase
        item["chronological_order"] = order_idx
        item["online_diagram"] = {
            "commons_title": cf,
            "image_url": cmeta["thumb_url"] if not cmeta["url"].endswith(".gif") else cmeta["url"],
            "original_url": cmeta["url"],
            "source_page": cmeta["page_url"],
            "license": cmeta["license"],
            "title": item.pop("diagram_title"),
            "guide": item.pop("diagram_guide"),
        }
        del item["commons_file"]
        out[cid] = item

    target = ROOT / "curriculum" / "course_enrichment.json"
    target.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(out)} enriched class records to {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
