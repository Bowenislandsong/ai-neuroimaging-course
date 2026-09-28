#!/usr/bin/env python3
"""Part 1 of course enrichment data: R00-R03, F01-F04, PR01-PR21, D01-D16."""

SCHEDULE_MAP = {
    "R00": (1, "Phase I · Paper Orientation & Foundations", 1),
    "R01": (1, "Phase I · Paper Orientation & Foundations", 2),
    "R02": (2, "Phase I · Paper Orientation & Foundations", 3),
    "R03": (2, "Phase I · Paper Orientation & Foundations", 4),
    "F01": (3, "Phase I · Paper Orientation & Foundations", 5),
    "F02": (3, "Phase I · Paper Orientation & Foundations", 6),
    "F03": (3, "Phase I · Paper Orientation & Foundations", 7),
    "F04": (3, "Phase I · Paper Orientation & Foundations", 8),
    "DS01": (4, "Phase II · Neuroimaging Data Science & Experimental Foundations", 9),
    "DS02": (4, "Phase II · Neuroimaging Data Science & Experimental Foundations", 10),
    "DS03": (4, "Phase II · Neuroimaging Data Science & Experimental Foundations", 11),
    "DS04": (4, "Phase II · Neuroimaging Data Science & Experimental Foundations", 12),
    "DS05": (5, "Phase II · Neuroimaging Data Science & Experimental Foundations", 13),
    "DS06": (5, "Phase II · Neuroimaging Data Science & Experimental Foundations", 14),
    "DS07": (5, "Phase II · Neuroimaging Data Science & Experimental Foundations", 15),
    "DS08": (5, "Phase II · Neuroimaging Data Science & Experimental Foundations", 16),
    "D01": (5, "Phase II · Neuroimaging Data Science & Experimental Foundations", 17),
    "D02": (5, "Phase II · Neuroimaging Data Science & Experimental Foundations", 18),
    "DS09": (6, "Phase II · Neuroimaging Data Science & Experimental Foundations", 19),
    "DS10": (6, "Phase II · Neuroimaging Data Science & Experimental Foundations", 20),
    "DS11": (6, "Phase II · Neuroimaging Data Science & Experimental Foundations", 21),
    "DS12": (6, "Phase II · Neuroimaging Data Science & Experimental Foundations", 22),
    "D03": (6, "Phase II · Neuroimaging Data Science & Experimental Foundations", 23),
    "D04": (6, "Phase II · Neuroimaging Data Science & Experimental Foundations", 24),
    "DS13": (7, "Phase II · Neuroimaging Data Science & Experimental Foundations", 25),
    "DS14": (7, "Phase II · Neuroimaging Data Science & Experimental Foundations", 26),
    "DS15": (7, "Phase II · Neuroimaging Data Science & Experimental Foundations", 27),
    "DS16": (7, "Phase II · Neuroimaging Data Science & Experimental Foundations", 28),
    "PR01": (8, "Phase III · Image Processing & Biophysical Pipelines", 29),
    "PR02": (8, "Phase III · Image Processing & Biophysical Pipelines", 30),
    "PR03": (8, "Phase III · Image Processing & Biophysical Pipelines", 31),
    "PR04": (8, "Phase III · Image Processing & Biophysical Pipelines", 32),
    "PR05": (9, "Phase III · Image Processing & Biophysical Pipelines", 33),
    "PR06": (9, "Phase III · Image Processing & Biophysical Pipelines", 34),
    "PR07": (9, "Phase III · Image Processing & Biophysical Pipelines", 35),
    "PR08": (9, "Phase III · Image Processing & Biophysical Pipelines", 36),
    "PR09": (10, "Phase III · Image Processing & Biophysical Pipelines", 37),
    "PR10": (10, "Phase III · Image Processing & Biophysical Pipelines", 38),
    "PR11": (10, "Phase III · Image Processing & Biophysical Pipelines", 39),
    "PR12": (10, "Phase III · Image Processing & Biophysical Pipelines", 40),
    "D05": (10, "Phase III · Image Processing & Biophysical Pipelines", 41),
    "PR13": (11, "Phase III · Image Processing & Biophysical Pipelines", 42),
    "PR14": (11, "Phase III · Image Processing & Biophysical Pipelines", 43),
    "PR15": (11, "Phase III · Image Processing & Biophysical Pipelines", 44),
    "D06": (11, "Phase III · Image Processing & Biophysical Pipelines", 45),
    "PR16": (12, "Phase III · Image Processing & Biophysical Pipelines", 46),
    "PR17": (12, "Phase III · Image Processing & Biophysical Pipelines", 47),
    "PR18": (12, "Phase III · Image Processing & Biophysical Pipelines", 48),
    "PR19": (12, "Phase III · Image Processing & Biophysical Pipelines", 49),
    "PR20": (13, "Phase III · Image Processing & Biophysical Pipelines", 50),
    "PR21": (13, "Phase III · Image Processing & Biophysical Pipelines", 51),
    "P01": (13, "Phase III · Image Processing & Biophysical Pipelines", 52),
    "D07": (14, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 53),
    "D08": (14, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 54),
    "D09": (14, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 55),
    "D10": (14, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 56),
    "D11": (15, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 57),
    "D12": (15, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 58),
    "D13": (15, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 59),
    "D14": (15, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 60),
    "D15": (16, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 61),
    "D16": (16, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 62),
    "P02": (16, "Phase IV · General Linear Modeling, Statistical Inference & Multiverse Design", 63),
    "M01": (17, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 64),
    "M02": (17, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 65),
    "M03": (17, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 66),
    "M04": (18, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 67),
    "M05": (18, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 68),
    "M06": (18, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 69),
    "M07": (19, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 70),
    "M08": (19, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 71),
    "M09": (19, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 72),
    "M10": (20, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 73),
    "M11": (20, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 74),
    "M12": (20, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 75),
    "M13": (21, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 76),
    "M14": (21, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 77),
    "M15": (21, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 78),
    "M16": (22, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 79),
    "M17": (22, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 80),
    "M18": (22, "Phase V · Multivariate Modeling, Dynamics & Foundation Models", 81),
    "P03": (23, "Phase VI · Capstone Generalization & Research Defense", 82),
    "P04": (25, "Phase VI · Capstone Generalization & Research Defense", 83),
}

ENRICHMENT_PART1 = {
    "R00": {
        "commons_file": "File:The_Scientific_Method.svg",
        "diagram_title": "The Scientific Cycle & Three-Pass Paper Forensics",
        "diagram_guide": "Notice how empirical measurement sits between a theoretical question and a falsifiable claim. In Pass 1–2 of reading a neuroimaging paper, map the main figure's axes, physical units, and transformation chain before reading the authors' narrative interpretation.",
        "pipeline_steps": ["Research Question & Estimand", "Raw MRI Acquisition (k-space / NIfTI)", "Mathematical Transformation Chain", "Figure Axis & Unit Forensics", "Bounded Scientific Claim"],
        "equation": {
            "name": "The Evidence-to-Claim Decomposition",
            "latex": r"\text{Claim Validity} = \underbrace{\text{Measurement Fidelity}}_{\text{Physics \& Metadata}} \times \underbrace{\text{Transformation Contract}}_{\text{Invariants Preserved}} \times \underbrace{\text{Out-of-Sample Generalization}}_{\text{Independent Evaluation}}",
            "summary": "Breaks any published neuroimaging conclusion into three multiplicative logical gates: if any single stage fails, the downstream claim collapses.",
            "terms": [
                {"term": r"\text{Measurement Fidelity}", "role": "Biophysical Input Gate", "meaning": "Captures what the scanner physically recorded (TR, TE, voxel size, B0 field) versus what was lost before software ever touched the file.", "failure": "Confusing BOLD T2* hemodynamic contrast with direct millisecond neuronal spiking."},
                {"term": r"\text{Transformation Contract}", "role": "Mathematical Operator Gate", "meaning": "Specifies the exact domain, codomain, fitted parameters, preserved invariants, and destroyed degrees of freedom of the processing/modeling pipeline.", "failure": "Applying a black-box script that silently alters coordinate frames or smooths across tissue boundaries."},
                {"term": r"\text{Out-of-Sample Generalization}", "role": "Inferential Boundary Gate", "meaning": "Tests whether the estimated effect or prediction survives on unseen participants and independent scanners without data leakage.", "failure": "Reporting in-sample or circularly selected statistics as generalizable population truth."}
            ]
        }
    },
    "R01": {
        "commons_file": "File:1206_FMRI.jpg",
        "diagram_title": "From Scanner Acquisition to Standardized fMRI Workflow (fMRIPrep & BrainMorph)",
        "diagram_guide": "Raw functional and structural scans contain head motion, susceptibility warping, intensity bias, and arbitrary scanner coordinates. A transparent processing pipeline aligns anatomy and function while exposing visual quality-control checkpoints at every stage.",
        "pipeline_steps": ["Raw BIDS NIfTI + JSON", "Bias & Skull-Strip (T1w)", "Susceptibility & Motion Correction", "EPI-to-T1w & MNI Registration", "Visual QC & Confound Table"],
        "equation": {
            "name": "Composite Spatial Preprocessing Operator",
            "latex": r"I_{\text{analysis}}(\mathbf{x}) = \left(\mathcal{R}_{\text{interp}} \circ T_{\text{MNI}\leftarrow\text{T1w}} \circ T_{\text{T1w}\leftarrow\text{EPI}} \circ T_{\text{SDC}} \circ T_{\text{motion}, t}\right)\!\big[I_{\text{raw}}(\mathbf{i}, t)\big]",
            "summary": "Chains every spatial transformation into a single composite pullback mapping so voxel intensities are interpolated only once rather than blurred repeatedly.",
            "terms": [
                {"term": r"I_{\text{raw}}(\mathbf{i}, t)", "role": "Raw Scanner Tensor", "meaning": "The discrete 4D integer/float array on the scanner's native voxel lattice i=(i,j,k) at frame t.", "failure": "Treating raw voxel indices as matched anatomical locations across time or participants."},
                {"term": r"T_{\text{SDC}} \circ T_{\text{motion}, t}", "role": "Within-Run Rigid + Distortion Transforms", "meaning": "6-DOF head motion realignment composed with phase-encoding B0 susceptibility unwarping.", "failure": "Ignoring residual spin-history and B0-by-motion interactions after rigid realignment."},
                {"term": r"T_{\text{MNI}\leftarrow\text{T1w}} \circ T_{\text{T1w}\leftarrow\text{EPI}}", "role": "Cross-Modal & Template Transforms", "meaning": "Boundary-based EPI-to-T1w registration composed with nonlinear diffeomorphic warp to standard template space.", "failure": "Resampling after each individual step, which compounds interpolation smoothing."},
                {"term": r"\mathcal{R}_{\text{interp}}", "role": "Single-Shot Resampling Kernel", "meaning": "Evaluates the continuous interpolation kernel (Lanczos/B-spline for images, nearest-neighbor for integer labels) once on the target grid.", "failure": "Using linear interpolation on discrete parcellation labels, inventing blended ROI integers."}
            ]
        }
    },
    "R02": {
        "commons_file": "File:K-fold_cross_validation_EN.svg",
        "diagram_title": "Out-of-Sample Generalization & Cross-Validation Partitioning (Marek et al. & BrainIAC)",
        "diagram_guide": "In K-fold and multi-site cross-validation, every preprocessing parameter, feature screen, and model weight must be estimated strictly inside the training folds (blue) and evaluated once on held-out participants/sites (orange).",
        "pipeline_steps": ["Target Population & Sites", "Participant/Site Split Boundary", "Train-Only Feature & Model Fit", "Held-Out Site Evaluation", "Replication Confidence Interval"],
        "equation": {
            "name": "Attenuated Out-of-Sample Brain-Wide Association Correlation",
            "latex": r"r_{\text{obs}} = r_{\text{true}} \sqrt{\text{ICC}_X \cdot \text{ICC}_Y} + \varepsilon_{\text{sample}}(N)",
            "summary": "Shows why observed brain-behavior correlations are bounded by measurement reliability and why small-N studies suffer massive sampling dispersion.",
            "terms": [
                {"term": r"r_{\text{true}}", "role": "Latent Biological Association", "meaning": "The true population correlation between the noiseless neural trait and the noiseless behavioral phenotype.", "failure": "Assuming a small latent effect (e.g., r=0.10) will look large in a small sample without winner's curse inflation."},
                {"term": r"\sqrt{\text{ICC}_X \cdot \text{ICC}_Y}", "role": "Reliability Attenuation Factor", "meaning": "Geometric mean of brain-measure test-retest reliability (ICC_X) and behavioral reliability (ICC_Y), shrinking the observable correlation.", "failure": "Using noisy short-scan resting-state edges (low ICC_X) that cap observable correlation near zero."},
                {"term": r"\varepsilon_{\text{sample}}(N)", "role": "Finite-Sample Estimation Noise", "meaning": "Sampling error of order O(1/sqrt(N)) that causes small samples (N=25) to produce wildly inflated or sign-reversed significant hits.", "failure": "Thresholding small-N correlations at p<0.05, which guarantees high Type M (magnitude) and Type S (sign) errors."}
            ]
        }
    },
    "R03": {
        "commons_file": "File:Generic_forest_plot.png",
        "diagram_title": "Analytical Variability & Multiverse Evidence Audits (NARPS & Omni-fMRI)",
        "diagram_guide": "When 70 independent research teams analyze the exact same neuroimaging dataset (NARPS), legitimate variations in smoothing, motion modeling, and thresholding create a forest of divergent effect estimates. Auditing evidence requires separating data signal from researcher degrees of freedom.",
        "pipeline_steps": ["Shared Raw Dataset (NARPS)", "Branching Pipeline Choices", "Team-Specific Statistical Maps", "Multiverse Specification Curve", "Consensus vs. Fragile Claims"],
        "equation": {
            "name": "Total Variance Across Analytical Pipelines (Multiverse Decomposition)",
            "latex": r"\operatorname{Var}(\hat{\theta}) = \underbrace{\mathbb{E}_{\pi}\!\left[\operatorname{Var}(\hat{\theta} \mid \pi)\right]}_{\text{Sampling Variance Within Pipeline}} + \underbrace{\operatorname{Var}_{\pi}\!\left(\mathbb{E}[\hat{\theta} \mid \pi]\right)}_{\text{Pipeline / Vibration Variance Across Choices}}",
            "summary": "Decomposes total uncertainty into standard within-pipeline sampling error plus the hidden variance across defensible analysis pipelines.",
            "terms": [
                {"term": r"\operatorname{Var}(\hat{\theta})", "role": "Total Claim Uncertainty", "meaning": "True total variance of the reported scientific estimate across both participant sampling and analytical branches.", "failure": "Reporting only the first term and pretending the pipeline choice had zero impact."},
                {"term": r"\mathbb{E}_{\pi}[\operatorname{Var}(\hat{\theta} \mid \pi)]", "role": "Conventional Standard Error Term", "meaning": "Average sampling variance printed by software assuming a single fixed pipeline pi.", "failure": "Treating a narrow single-pipeline p-value as proof that the scientific conclusion is robust."},
                {"term": r"\operatorname{Var}_{\pi}(\mathbb{E}[\hat{\theta} \mid \pi])", "role": "Analytical Vibration Variance", "meaning": "Dispersion of the expected estimate across valid preprocessing, design, and inference specifications (NARPS).", "failure": "Cherry-picking the single pipeline branch pi* that maximizes statistical significance."}
            ]
        }
    },
    "F01": {
        "commons_file": "File:The_Scientific_Method.svg",
        "diagram_title": "The Human-AI Scientific Supervision Loop",
        "diagram_guide": "In agentic neuroimaging workflows, the AI coding assistant (Goose + Qwen) translates your explicit mathematical contract into executable code, while you (backed by Gemma 4 auditing and numerical assertions) verify invariants, axes, and physical units.",
        "pipeline_steps": ["State Transformation Contract", "Predict Numerical Outcome", "Delegate Snippet to Goose/Qwen", "Run Shape & Invariant Asserts", "Verify Visual & Physical Range"],
        "equation": {
            "name": "Explicit Transformation Contract Specification",
            "latex": r"\mathcal{T}_{\boldsymbol{\theta}}: \mathcal{X}_{(d_1 \times \dots \times d_k)}^{[\text{units}, \text{space}]} \longrightarrow \mathcal{Y}_{(m_1 \times \dots \times m_r)}^{[\text{units}', \text{space}']}, \quad \boldsymbol{\theta} = \operatorname{fit}\!\left(\mathcal{X}_{\text{train}}\right)",
            "summary": "Defines every neuroimaging code step as a typed mathematical mapping with explicit array dimensions, physical units, coordinate frame, and training-only fit scope.",
            "terms": [
                {"term": r"\mathcal{X}_{(d_1 \times \dots \times d_k)}^{[\text{units}, \text{space}]}", "role": "Domain & Input Metadata", "meaning": "Input array with named axis dimensions (e.g., X,Y,Z,T), physical units (e.g., mm, s, arb. intensity), and coordinate space (e.g., native RAS+).", "failure": "Passing unnamed NumPy arrays where voxel and time axes are silently transposed."},
                {"term": r"\boldsymbol{\theta} = \operatorname{fit}(\mathcal{X}_{\text{train}})", "role": "Fitted Parameter Scope", "meaning": "Parameters (means, scalers, PCA axes, ComBat shifts, model weights) estimated strictly on the training partition.", "failure": "Fitting parameters on the full dataset before splitting, causing data leakage."},
                {"term": r"\mathcal{Y}_{(m_1 \times \dots \times m_r)}^{[\text{units}', \text{space}']}", "role": "Codomain & Verified Output", "meaning": "Transformed output whose shape, units, preserved invariants, and destroyed information are verified by assertions.", "failure": "Accepting plausible-looking AI plots without checking numerical invariants."}
            ]
        }
    },
    "F02": {
        "commons_file": "File:Magnetization_Relaxation_Longitudinal_Transversal_T1_T2.png",
        "diagram_title": "Bloch Longitudinal (T1) Recovery & Transverse (T2 / T2*) Relaxation Curves",
        "diagram_guide": "Compare the rising longitudinal recovery curve M_z(t) = M_0(1 - e^{-t/T1}) against the decaying transverse coherence curve M_xy(t) = M_0 e^{-t/T2}. Repetition Time (TR) samples the T1 recovery curve; Echo Time (TE) samples the T2/T2* decay curve.",
        "pipeline_steps": ["Proton Density & B0 Alignment", "RF Flip Angle Excitation", "T1 Longitudinal Recovery (TR)", "T2* Transverse Decay (TE)", "Logothetis LFP -> HRF -> BOLD"],
        "equation": {
            "name": "Spoiled Gradient-Echo (GRE / EPI) Steady-State Signal Equation",
            "latex": r"S_{\text{GRE}}(\text{TR}, \text{TE}, \theta) \propto \underbrace{\rho}_{\text{Spin Density}} \cdot \underbrace{\frac{\sin\theta\left(1 - e^{-\text{TR}/T_1}\right)}{1 - \cos\theta\, e^{-\text{TR}/T_1}}}_{\text{Steady-State } T_1 \text{ \& Flip-Angle Gain}} \cdot \underbrace{e^{-\text{TE}/T_2^*}}_{\text{BOLD } T_2^* \text{ Dephasing Decay}}",
            "summary": "Governs how sequence timing (TR, TE, flip angle theta) interacts with tissue relaxation (T1, T2*) to produce anatomical contrast and functional BOLD sensitivity.",
            "terms": [
                {"term": r"\rho", "role": "Equilibrium Proton Density", "meaning": "Baseline concentration of mobile 1H water/lipid spins setting the maximum available magnetization M0.", "failure": "Mistaking raw voxel intensity for absolute proton density without accounting for T1, T2*, and coil bias."},
                {"term": r"\frac{\sin\theta(1 - e^{-\text{TR}/T_1})}{1 - \cos\theta\,e^{-\text{TR}/T_1}}", "role": "Longitudinal T1 Recovery & Ernst Gain", "meaning": "Determines how much longitudinal magnetization recovers between pulses spaced by TR and projects into the receiver plane via sin(theta); maximized at the Ernst angle arccos(e^{-TR/T1}).", "failure": "Using a 90-degree flip angle at short TR, saturating long-T1 gray matter and CSF."},
                {"term": r"e^{-\text{TE}/T_2^*}", "role": "Transverse T2* & Deoxyhemoglobin Decay", "meaning": "Exponential signal attenuation over echo time TE driven by spin-spin relaxation (1/T2) plus local magnetic field inhomogeneities (gamma Delta B0 from paramagnetic deoxyhemoglobin).", "failure": "Setting TE too short (no BOLD contrast) or too long (total susceptibility dropout near sinuses)."}
            ]
        }
    },
    "F03": {
        "commons_file": "File:The_Normal_Distribution.svg",
        "diagram_title": "Auditing Code Snippets: Descriptive Standardization vs. Inferential Statistics",
        "diagram_guide": "Standardizing an array to mean 0 and standard deviation 1 rescales its units (horizontal axis), but does not change its distribution shape or compute a p-value. Auditing AI code requires reading every axis argument, degree-of-freedom flag (ddof), and division guard.",
        "pipeline_steps": ["Inspect Input Shape & Axis", "Center by Axis Mean", "Scale by Protected Std (ddof)", "Verify Zero-Variance Guard", "Distinguish z-Score vs. t-Test"],
        "equation": {
            "name": "Axis-Specific Protected z-Standardization",
            "latex": r"Z_{v, t} = \begin{cases} \dfrac{X_{v, t} - \mu_v}{\sigma_v} & \text{if } \sigma_v > \epsilon \\[6pt] 0 & \text{if } \sigma_v \le \epsilon \end{cases}, \qquad \mu_v = \frac{1}{T}\sum_{t=1}^{T} X_{v, t}, \quad \sigma_v = \sqrt{\frac{1}{T - \delta}\sum_{t=1}^{T}(X_{v, t} - \mu_v)^2}",
            "summary": "Removes each voxel's static baseline offset and scales its temporal fluctuation to unit variance while guarding against out-of-brain zero-variance voxels.",
            "terms": [
                {"term": r"X_{v, t} - \mu_v", "role": "Within-Voxel Temporal Centering", "meaning": "Subtracts voxel v's temporal mean across T time points so static T1/T2* baseline brightness is removed.", "failure": "Computing X.mean(axis=0) across voxels instead of axis=1 across time, mixing anatomy with dynamics."},
                {"term": r"\sigma_v \text{ with } \delta \in \{0, 1\}", "role": "Temporal Dispersion & ddof Choice", "meaning": "Divides by the voxel's temporal standard deviation (population ddof=0 vs. sample ddof=1).", "failure": "Leaving ddof unspecified when comparing code outputs against analytical formulas."},
                {"term": r"\sigma_v > \epsilon \text{ Guard}", "role": "Zero-Variance Numerical Safety Gate", "meaning": "Replaces 0/0 division in constant background masks with 0.0 instead of propagating NaN/Inf across the volume.", "failure": "Allowing a single masked background voxel to poison downstream matrix multiplications with NaNs."}
            ]
        }
    },
    "F04": {
        "commons_file": "File:Jupyter_Notebook.png",
        "diagram_title": "Deterministic Execution State & Hidden Kernel Mutation in Notebooks",
        "diagram_guide": "A Jupyter notebook is an interactive REPL with mutable global state in memory. Out-of-order cell execution, in-place array mutation, and unseeded random number generators destroy reproducibility unless verified in a clean top-to-bottom kernel.",
        "pipeline_steps": ["Fresh Kernel Initialization", "Pinned Environment (uv.lock)", "Explicit PRNG Seed (default_rng)", "Non-Mutating Pure Functions", "Top-to-Bottom nbclient Audit"],
        "equation": {
            "name": "Deterministic Computational State Transition",
            "latex": r"S_k = f_k\!\left(S_{k-1}, \, \mathcal{D}_{\text{immutable}}, \, \text{RNG}(s_0)\right), \qquad \operatorname{SHA256}\!\left(S_K^{\text{fresh}}\right) = \operatorname{SHA256}\!\left(S_K^{\text{saved}}\right)",
            "summary": "Formalizes a reproducible notebook as a pure composition of state transitions from a fixed random seed s0 and immutable input data.",
            "terms": [
                {"term": r"S_{k-1} \to S_k", "role": "Sequential Cell State Transition", "meaning": "Each cell k must depend only on definitions executed in cells 1..k-1 in strict linear order.", "failure": "Running Cell 8 before Cell 4 or deleting a cell whose variable still lingers in RAM."},
                {"term": r"\mathcal{D}_{\text{immutable}}", "role": "Unmutated Input Buffer", "meaning": "Input arrays are copied or treated as read-only rather than modified in-place across re-runs.", "failure": "In-place operations like X -= X.mean() that change results when a cell is run twice."},
                {"term": r"\text{RNG}(s_0)", "role": "Isolated Random Stream", "meaning": "Local Generator instance np.random.default_rng(s0) supplying deterministic draws independent of global state.", "failure": "Relying on unseeded global np.random calls that shift every time a cell is re-executed."}
            ]
        }
    },
    "PR01": {
        "commons_file": "File:Human_brain_anatomical_planes_letter_annotations.jpg",
        "diagram_title": "Anatomical Coordinate Planes (Axial, Coronal, Sagittal) & RAS+ Voxel-to-World Mapping",
        "diagram_guide": "A NIfTI file stores a 3D/4D grid of numbers (i, j, k) whose physical orientation in millimeters (Right-Anterior-Superior, RAS+) exists only through the 4x4 homogeneous affine matrix A in the header.",
        "pipeline_steps": ["Discrete Voxel Grid (i, j, k)", "4x4 Homogeneous Affine Matrix A", "Rotation R · Scaling S · Shear K", "Origin Translation Vector t", "Physical World Space (x, y, z mm)"],
        "equation": {
            "name": "NIfTI Homogeneous Voxel-to-World Affine Transformation",
            "latex": r"\begin{bmatrix} x_{\text{R}} \\ y_{\text{A}} \\ z_{\text{S}} \\ 1 \end{bmatrix} = \underbrace{\begin{bmatrix} M_{3\times 3} & \mathbf{t}_{3\times 1} \\ \mathbf{0}^T & 1 \end{bmatrix}}_{A \text{ (4}\times\text{4 Affine)}} \begin{bmatrix} i \\ j \\ k \\ 1 \end{bmatrix} = \underbrace{(R \, S \, K)}_{\text{Linear Submatrix } M}\mathbf{i} + \underbrace{\mathbf{t}}_{\text{Origin Offset}}",
            "summary": "Maps discrete array indices (i,j,k) to continuous physical coordinates (x,y,z) in millimeters in the scanner's RAS+ coordinate frame.",
            "terms": [
                {"term": r"\mathbf{i} = [i, j, k, 1]^T", "role": "Homogeneous Voxel Index", "meaning": "Zero-based integer array subscripts along the three storage axes, augmented with 1 to enable translation via matrix multiplication.", "failure": "Assuming axis 0 is always Left-to-Right without checking the affine matrix."},
                {"term": r"M = R\,S\,K", "role": "Orientation, Voxel Size & Oblique Shear", "meaning": "3x3 linear matrix encoding orthogonal slice rotation R, voxel spacing S=diag(di,dj,dk), and oblique gantry shear K; |det(M)| is voxel volume in mm^3.", "failure": "Flipping an image array with np.flip without updating M, silently swapping Left and Right hemispheres."},
                {"term": r"\mathbf{t} = [t_x, t_y, t_z]^T", "role": "Physical Origin Translation", "meaning": "World RAS+ coordinates (in mm) of the center of corner voxel (0,0,0).", "failure": "Constructing nib.Nifti1Image(data, np.eye(4)), which resets voxel spacing to 1mm and shifts the origin to (0,0,0)."}
            ]
        }
    },
    "PR02": {
        "commons_file": "File:Bilinear_Interpolation_example.png",
        "diagram_title": "Pullback Resampling & Continuous Interpolation on Discrete Grids",
        "diagram_guide": "When registering a moving image to a fixed target grid, we iterate over each target voxel center x_m, project it backward into the moving image via the inverse transform T^{-1}(x_m), and interpolate surrounding moving voxel intensities.",
        "pipeline_steps": ["Target Grid Coordinates x_m", "Inverse Pullback T^{-1}(x_m)", "Continuous Moving Coordinates", "Interpolation Kernel psi (Spline/NN)", "Resampled Output Volume"],
        "equation": {
            "name": "Pullback (Backward) Image Resampling & Interpolation",
            "latex": r"I_{\text{out}}(\mathbf{x}_m) = I_{\text{mov}}\!\left(T_{\text{fix}\leftarrow\text{mov}}^{-1}(\mathbf{x}_m)\right) = \sum_{\mathbf{k} \in \Omega_{\text{mov}}} I_{\text{mov}}[\mathbf{k}] \; \psi\!\left(A_{\text{mov}}^{-1} T_{\text{fix}\leftarrow\text{mov}}^{-1}(\mathbf{x}_m) - \mathbf{k}\right)",
            "summary": "Evaluates every voxel of the output grid by pulling coordinates backward into the moving image and convolving with an interpolation kernel psi.",
            "terms": [
                {"term": r"T_{\text{fix}\leftarrow\text{mov}}^{-1}(\mathbf{x}_m)", "role": "Inverse Pullback Coordinate Map", "meaning": "Maps each regular grid point x_m in fixed space back to its source location in moving space so no output voxel is left with holes.", "failure": "Applying the forward transform вместо the inverse, moving the brain in the opposite direction or leaving unvisited grid holes."},
                {"term": r"A_{\text{mov}}^{-1}(\cdot)", "role": "World-to-Voxel Index Conversion", "meaning": "Converts continuous physical coordinates in moving space into fractional moving-array indices.", "failure": "Mixing millimeter translations with voxel-index offsets when grids have different resolutions."},
                {"term": r"\psi(\cdot)", "role": "Interpolation Kernel", "meaning": "Weights neighboring discrete samples (order 0 nearest-neighbor for integer masks/atlases; order 1–3 linear/B-spline for continuous intensities).", "failure": "Using trilinear interpolation (order=1) on an integer parcellation atlas, creating invalid intermediate label IDs at region borders."}
            ]
        }
    },
    "PR03": {
        "commons_file": "File:Jacobian_determinant_and_distortion.svg",
        "diagram_title": "Nonlinear Deformation Fields, Diffeomorphisms & Jacobian Determinant Folding Checks",
        "diagram_guide": "A nonlinear warp bends a coordinate grid locally via a displacement field u(x). The Jacobian determinant J(x) = det(I + grad u(x)) measures local volume expansion (J > 1) or compression (0 < J < 1); if J(x) <= 0, the grid has folded over itself and destroyed anatomical topology.",
        "pipeline_steps": ["Identity Grid x", "Displacement Field u(x)", "Deformation Gradient I + grad u", "Jacobian Determinant J(x)", "Topology Check (J > 0 Everywhere)"],
        "equation": {
            "name": "Deformation Field & Local Jacobian Volume Change",
            "latex": r"\boldsymbol{\phi}(\mathbf{x}) = \mathbf{x} + \mathbf{u}(\mathbf{x}), \qquad J(\mathbf{x}) = \det\!\big(\nabla \boldsymbol{\phi}(\mathbf{x})\big) = \det\!\big(I_d + \nabla \mathbf{u}(\mathbf{x})\big)",
            "summary": "Quantifies the local volumetric scaling factor induced by a nonlinear warp and certifies whether the transformation is a topology-preserving diffeomorphism.",
            "terms": [
                {"term": r"\mathbf{u}(\mathbf{x})", "role": "Dense Displacement Vector Field", "meaning": "3D vector at every voxel specifying the local millimeter shift from template space to native anatomy.", "failure": "Over-penalizing or under-penalizing bending energy, leading to either residual misregistration or unphysical grid tearing."},
                {"term": r"I_d + \nabla \mathbf{u}(\mathbf{x})", "role": "Local Jacobian Matrix", "meaning": "First-order linearization of the warp combining the identity matrix with spatial partial derivatives of the displacement.", "failure": "Computing finite differences without dividing by physical voxel spacing (mm)."},
                {"term": r"J(\mathbf{x}) = \det(\nabla\boldsymbol{\phi})", "role": "Volumetric Scaling & Topology Invariant", "meaning": "Ratio of deformed elemental volume to original volume: J=1 preserves volume, J>1 expands, 0<J<1 compresses, and J<=0 indicates non-invertible folding.", "failure": "Accepting a nonlinear registration without checking min(J) > 0 across the brain mask."}
            ]
        }
    },
    "PR04": {
        "commons_file": "File:MRI_with_B0_inhomogeneity.jpg",
        "diagram_title": "RF Coil Sensitivity Shading & Multiplicative Bias Field Correction (N4ITK)",
        "diagram_guide": "Phased-array receiver coils and B1+ RF inhomogeneity multiply the true tissue contrast by a smooth spatial shading field B(x). Because the bias is multiplicative, a single tissue class (e.g., white matter) spans different intensity ranges across the brain until corrected in log-space.",
        "pipeline_steps": ["Observed Shaded MRI I_obs", "Log-Transform Additive Split", "Smooth B-Spline Field Fit", "Exponentiate Estimated Bias", "Divide to Restore Tissue Contrast"],
        "equation": {
            "name": "Multiplicative Bias Field Model & Log-Domain N4 Decomposition",
            "latex": r"I_{\text{obs}}(\mathbf{x}) = B(\mathbf{x}) \cdot I_{\text{true}}(\mathbf{x}) + \eta(\mathbf{x}) \;\xrightarrow{\;\ln\;}\; \ln I_{\text{obs}}(\mathbf{x}) \approx \ln I_{\text{true}}(\mathbf{x}) + \ln B(\mathbf{x})",
            "summary": "Converts a spatially varying multiplicative coil gain B(x) into an additive low-frequency offset in log-space that can be estimated with smooth B-splines.",
            "terms": [
                {"term": r"B(\mathbf{x}) > 0", "role": "Smooth Multiplicative Bias Field", "meaning": "Spatially slowly varying RF reception/transmission sensitivity field that scales both tissue means and within-tissue variances.", "failure": "Attempting additive background subtraction instead of multiplicative division."},
                {"term": r"\ln I_{\text{true}}(\mathbf{x}) + \ln B(\mathbf{x})", "role": "Log-Space Additive Separation", "meaning": "Logarithmic transform turns multiplication into addition so low-frequency B-spline smoothing isolates ln B(x).", "failure": "Taking log(I_obs) without clamping zero/negative background noise voxels above epsilon."},
                {"term": r"I_{\text{corr}}(\mathbf{x}) = I_{\text{obs}}(\mathbf{x}) / \hat{B}(\mathbf{x})", "role": "Homogenized Intensity Restoration", "meaning": "Divides out the smooth bias estimate to sharpen white/gray matter histogram peaks prior to tissue segmentation.", "failure": "Using an overly flexible spline knot spacing that erases true biological focal lesions or cortical contrast."}
            ]
        }
    },
    "PR05": {
        "commons_file": "File:Brainanim.gif",
        "diagram_title": "Brain Extraction (Skull Stripping) & Boundary Distance Metrics (Dice vs. Hausdorff)",
        "diagram_guide": "A brain mask defines the computational universe for registration, bias correction, and statistical testing. High overall Dice overlap (>0.95) can still hide localized dural inclusions or cortical over-stripping that only surface boundary metrics (Hausdorff Distance, ASSD) detect.",
        "pipeline_steps": ["Full-Head Structural Volume", "Brain Extraction (BET / SynthStrip)", "Binary Mask & Boundary Surface", "Dice Volume Overlap Audit", "Hausdorff & ASSD Rim Audit"],
        "equation": {
            "name": "Sørensen–Dice Overlap vs. Directed Hausdorff Boundary Distance",
            "latex": r"\text{DSC}(\hat{M}, M) = \frac{2|\hat{M} \cap M|}{|\hat{M}| + |M|}, \qquad \text{HD}(\partial\hat{M}, \partial M) = \max\!\left\{\max_{\mathbf{p}\in\partial\hat{M}}\min_{\mathbf{q}\in\partial M}\|\mathbf{p}-\mathbf{q}\|_2, \; \max_{\mathbf{q}\in\partial M}\min_{\mathbf{p}\in\partial\hat{M}}\|\mathbf{p}-\mathbf{q}\|_2\right\}",
            "summary": "Pairs a bulk volumetric overlap ratio (Dice) with a worst-case millimeter boundary excursion metric (Hausdorff distance).",
            "terms": [
                {"term": r"\frac{2|\hat{M} \cap M|}{|\hat{M}| + |M|}", "role": "Bulk Volumetric Overlap (DSC)", "meaning": "Harmonic mean of sensitivity and precision over interior brain voxels; dominated by the large deep brain core.", "failure": "Relying solely on DSC, which remains ~0.97 even when 3 mm of superior parietal cortex is shaved off."},
                {"term": r"\partial\hat{M}, \partial M", "role": "Extracted vs. Reference Surfaces", "meaning": "Boundary voxel sets where pial gray matter meets CSF, dura, and skull.", "failure": "Including bright neck fat or optic nerves that pull downstream registration off-target."},
                {"term": r"\max_{\mathbf{p}} \min_{\mathbf{q}} \|\mathbf{p}-\mathbf{q}\|_2", "role": "Worst-Case Boundary Error (mm)", "meaning": "Maximum Euclidean distance in millimeters from any point on one mask boundary to the closest point on the other.", "failure": "Computing boundary distances in raw voxel counts instead of physical millimeters."}
            ]
        }
    },
    "PR06": {
        "commons_file": "File:GMM_Training_on_artificial_data.gif",
        "diagram_title": "Gaussian Mixture Model (GMM) Expectation-Maximization & Partial Volume Tissue Posteriors",
        "diagram_guide": "Instead of forcing every boundary voxel into a binary integer label, probabilistic tissue segmentation models the intensity histogram as a mixture of CSF, Gray Matter, and White Matter Gaussians coupled with a spatial Markov Random Field prior.",
        "pipeline_steps": ["Skull-Stripped & N4-Corrected T1w", "Initialize Tissue Gaussians (CSF/GM/WM)", "E-Step: Posterior Responsibilities gamma_ic", "M-Step: Update Means, Variances & Priors", "Soft Partial-Volume Maps vs. Hard Labels"],
        "equation": {
            "name": "Bayes Posterior Tissue Responsibility (EM E-Step)",
            "latex": r"\gamma_{ic} = P(Z_i = c \mid y_i, \boldsymbol{\Theta}) = \frac{\overbrace{\pi_c}^{\text{Prior}} \, \overbrace{\mathcal{N}(y_i \mid \mu_c, \sigma_c^2)}^{\text{Intensity Likelihood}}}{\underbrace{\sum_{k \in \{\text{CSF,GM,WM}\}} \pi_k \, \mathcal{N}(y_i \mid \mu_k, \sigma_k^2)}_{\text{Marginal Evidence at Voxel } i}}",
            "summary": "Computes the continuous posterior probability that voxel i belongs to tissue class c by weighting its Gaussian intensity likelihood by the class prior.",
            "terms": [
                {"term": r"\pi_c", "role": "Spatial / Mixing Prior", "meaning": "Prior probability of tissue class c (from global mixing proportions or a tissue probability atlas / MRF neighborhood).", "failure": "Using flat priors on low-contrast scans where deep gray nuclei overlap white matter intensities."},
                {"term": r"\mathcal{N}(y_i \mid \mu_c, \sigma_c^2)", "role": "Class-Conditional Intensity Likelihood", "meaning": "Gaussian density of observing voxel intensity y_i given tissue class mean mu_c and variance sigma_c^2.", "failure": "Fitting GMMs before N4 bias correction, causing shaded white matter to be misclassified as gray matter."},
                {"term": r"\gamma_{ic} \in [0, 1]", "role": "Soft Posterior Probability", "meaning": "Continuous tissue responsibility summed across voxels to estimate unbiased partial-volume tissue volume.", "failure": "Thresholding gamma_ic via argmax (hard labels), which systematically biases volume estimates in thin cortical ribbons."}
            ]
        }
    },
    "PR07": {
        "commons_file": "File:VBM1.jpg",
        "diagram_title": "Voxel-Based Morphometry (VBM), Jacobian Modulation & Total Intracranial Volume (TIV) Adjustment",
        "diagram_guide": "Nonlinear registration warps every participant's brain to match the template's shape. Without multiplying the warped tissue map by the Jacobian determinant J(x) (modulation), regional volume differences are erased by the warp itself.",
        "pipeline_steps": ["Native GM Probability Map", "Warp to Template Space (Unmodulated)", "Multiply by Jacobian J(x) (Modulated)", "Verify Total Volume Conservation", "Regress Out Head Size (TIV)"],
        "equation": {
            "name": "Jacobian-Modulated Tissue Density & TIV Allometric Residualization",
            "latex": r"p_{\text{mod}}(\mathbf{x}) = \underbrace{p_{\text{nat}}\!\big(\boldsymbol{\phi}(\mathbf{x})\big)}_{\text{Unmodulated Tissue Concentration}} \cdot \underbrace{\big|\det(\nabla\boldsymbol{\phi}(\mathbf{x}))\big|}_{\text{Local Jacobian Volume Factor } J(\mathbf{x})}, \qquad V_{\text{adj}, i} = V_i - \hat{\beta}_{\text{TIV}}\!\left(\text{TIV}_i - \overline{\text{TIV}}\right)",
            "summary": "Preserves native tissue volume (mm^3) after spatial normalization via Jacobian modulation, then adjusts regional volume for global head size (TIV).",
            "terms": [
                {"term": r"p_{\text{nat}}(\boldsymbol{\phi}(\mathbf{x}))", "role": "Unmodulated Warped Concentration", "meaning": "Resampled tissue probability at template coordinate x; reflects local concentration but loses native size differences.", "failure": "Interpreting unmodulated VBM maps as regional gray matter volume (mm^3) rather than concentration."},
                {"term": r"J(\mathbf{x}) = |\det(\nabla\boldsymbol{\phi}(\mathbf{x}))|", "role": "Jacobian Volume Conservation Factor", "meaning": "Scales template voxels up if native tissue was compressed into a smaller template region, ensuring integral(p_mod) equals native volume.", "failure": "Modulating by 1/J(x) instead of J(x), which inverts atrophy into apparent hypertrophy."},
                {"term": r"-\hat{\beta}_{\text{TIV}}(\text{TIV}_i - \overline{\text{TIV}})", "role": "Head-Size Confound Residualization", "meaning": "Removes linear scaling with Total Intracranial Volume (estimated on the reference group) before testing group atrophy.", "failure": "Dividing crudely by TIV when scaling is non-proportional, or failing to account for sex-by-TIV collinearity."}
            ]
        }
    },
    "PR08": {
        "commons_file": "File:Spherical_Registration.png",
        "diagram_title": "Cortical Surface Meshes, Euler Characteristic Topology & Geodesic vs. Euclidean Distance",
        "diagram_guide": "The cerebral cortex is a folded 2D sheet (~2.5 mm thick). Representing it as a genus-0 triangular mesh (white and pial surfaces inflated to a sphere) prevents smoothing across sulcal CSF banks that are close in 3D Euclidean space but centimeters apart along the cortical sheet.",
        "pipeline_steps": ["WM Segmentation & Tessellation", "Topological Defect Repair (chi = 2)", "Deform White & Pial Surfaces", "Vertex Thickness & Area Metrics", "Spherical Inflation & Geodesic Smoothing"],
        "equation": {
            "name": "Euler-Poincaré Topological Invariant & Symmetric Cortical Thickness",
            "latex": r"\chi = \underbrace{|V|}_{\text{Vertices}} - \underbrace{|E|}_{\text{Edges}} + \underbrace{|F|}_{\text{Faces}} = 2 - 2g = 2 \quad (g=0), \qquad \tau(v) = \frac{1}{2}\!\left(\min_{\mathbf{p}\in\mathcal{S}_{\text{pial}}}\|\mathbf{w}_v - \mathbf{p}\|_2 + \min_{\mathbf{w}\in\mathcal{S}_{\text{white}}}\|\mathbf{p}_v - \mathbf{w}\|_2\right)",
            "summary": "Enforces that each cortical hemisphere mesh is topologically equivalent to a hole-free sphere (genus g=0, Euler characteristic chi=2) before measuring vertex-wise cortical thickness.",
            "terms": [
                {"term": r"|V| - |E| + |F| = 2", "role": "Euler-Poincaré Sphere Invariant", "meaning": "Alternating sum of mesh vertices, edges, and triangular faces; equals exactly 2 for any closed surface without handles or bridges (genus g=0).", "failure": "Skipping topological defect correction, leaving segmentation handles/holes that corrupt spherical registration."},
                {"term": r"\min_{\mathbf{p}\in\mathcal{S}_{\text{pial}}}\|\mathbf{w}_v - \mathbf{p}\|_2", "role": "Shortest White-to-Pial Distance", "meaning": "Euclidean distance in mm from white-surface vertex w_v to the nearest point on the pial surface (not merely along one voxel axis).", "failure": "Measuring thickness by counting voxels along a single grid axis, which overestimates thickness in obliquely tilted sulci."},
                {"term": r"d_{\text{geodesic}}(u, v) \gg \|\mathbf{x}_u - \mathbf{x}_v\|_2", "role": "Sulcal Bank Separation", "meaning": "Surface-constrained geodesic path travels around the fundus of a sulcus rather than jumping across the 2 mm CSF gap between opposing gyral banks.", "failure": "Applying 3D volumetric Gaussian smoothing that blends functional signals from opposing sulcal walls."}
            ]
        }
    },
    "PR09": {
        "commons_file": "File:SpinEcho_GWM_stills.jpg",
        "diagram_title": "Slice-Timing Acquisition Offsets & Temporal Phase Interpolation",
        "diagram_guide": "A 2D echo-planar fMRI volume is not captured instantaneously: sequential or interleaved slices are acquired across the entire Repetition Time (TR). Shifting each slice's time series to a common reference time aligns the hemodynamic response with the event design matrix.",
        "pipeline_steps": ["Read BIDS SliceTiming Metadata (s)", "Choose Reference Time t_ref", "Compute Slice Offset Delta t_z", "Sinc / Fourier Phase Shift in Time", "Aligned 4D Volume + Updated Events"],
        "equation": {
            "name": "Fourier Phase-Shift Slice-Timing Correction",
            "latex": r"x_{\text{corr}}(z, t) = \mathcal{F}^{-1}\!\left\{\mathcal{F}\{x(z, t)\}(\omega) \cdot \underbrace{e^{+i \omega \Delta t_z}}_{\text{Linear Phase Shift}}\right\}, \qquad \Delta t_z = t_z - t_{\text{ref}}, \quad |\omega| \le \frac{\pi}{\text{TR}}",
            "summary": "Shifts slice z's time series by its exact acquisition offset Delta t_z using the Fourier shift theorem within the Nyquist band.",
            "terms": [
                {"term": r"\Delta t_z = t_z - t_{\text{ref}}", "role": "Slice Acquisition Time Offset", "meaning": "Signed delay (in seconds) between when slice z was physically excited and the chosen volume reference time t_ref.", "failure": "Guessing sequential vs. interleaved slice order instead of reading the BIDS SliceTiming JSON array, or applying the shift with the wrong sign."},
                {"term": r"e^{+i \omega \Delta t_z}", "role": "Frequency-Domain Phase Ramp", "meaning": "Pure phase rotation proportional to angular frequency omega that shifts a bandlimited signal in time without attenuating its amplitude.", "failure": "Applying slice-timing correction BEFORE motion realignment when large head movements shift tissue across slices."},
                {"term": r"|\omega| \le \pi / \text{TR}", "role": "Nyquist Sampling Limit", "meaning": "Maximum temporal frequency representable at sampling interval TR; rapid motion spikes violate bandlimitedness and cause temporal ringing.", "failure": "Ignoring temporal derivatives in the GLM when long TRs (>2 s) leave residual slice-timing phase errors."}
            ]
        }
    },
    "PR10": {
        "commons_file": "File:Six_degrees_of_freedom.jpg",
        "diagram_title": "Rigid-Body Head Motion (6 DOF), Framewise Displacement (FD) & Spin-History Artifacts",
        "diagram_guide": "Head movement during an fMRI run is parameterized by 3 translations (x, y, z in mm) and 3 rotations (pitch, roll, yaw in radians). Even after rigid realignment puts the brain back on the grid, out-of-plane motion disrupts steady-state T1 longitudinal magnetization (spin-history artifacts).",
        "pipeline_steps": ["Estimate 6-DOF Rigid Params per TR", "Convert Rotations (r = 50 mm Arc)", "Compute Framewise Displacement FD_t", "Resample Volumes to Reference Frame", "Audit Residual DVARS & Spin-History"],
        "equation": {
            "name": "Power et al. (2012) Framewise Displacement (FD) & Volterra Expansion",
            "latex": r"\text{FD}_t = \underbrace{|\Delta d_{x,t}| + |\Delta d_{y,t}| + |\Delta d_{z,t}|}_{\text{Translational Step (mm)}} + \underbrace{R_{\text{arc}}\!\left(|\Delta\alpha_t| + |\Delta\beta_t| + |\Delta\gamma_t|\right)}_{\text{Rotational Arc Step at } R_{\text{arc}}=50\text{ mm}}, \qquad \mathbf{m}_{24}(t) = \big[\mathbf{m}_t, \mathbf{m}_{t-1}, \mathbf{m}_t^2, \mathbf{m}_{t-1}^2\big]",
            "summary": "Combines frame-to-frame translational and rotational head movements into a single millimeter displacement index and expands motion into 24 nonlinear/delayed nuisance regressors.",
            "terms": [
                {"term": r"|\Delta d_{x,t}| + |\Delta d_{y,t}| + |\Delta d_{z,t}|", "role": "L1 Translational Displacement", "meaning": "Sum of absolute frame-to-frame shifts (in mm) along the three Cartesian axes between volume t-1 and volume t.", "failure": "Differencing cumulative position poorly or failing to set FD_0 = 0 at the first time point."},
                {"term": r"R_{\text{arc}}(|\Delta\alpha_t| + |\Delta\beta_t| + |\Delta\gamma_t|)", "role": "Cortical Arc-Length Conversion", "meaning": "Converts angular rotations (in radians) to millimeter displacement on a cortical sphere of radius R_arc = 50 mm.", "failure": "Adding raw degrees or unscaled radians directly to millimeter translations without the 50 mm radius conversion."},
                {"term": r"\mathbf{m}_{24}(t)", "role": "Friston 24-Parameter Spin-History Basis", "meaning": "Includes current, 1-TR delayed, and squared motion terms to capture nonlinear partial-volume and T1 spin-history disturbances.", "failure": "Assuming rigid realignment alone removes motion artifacts from functional connectivity."}
            ]
        }
    },
    "PR11": {
        "commons_file": "File:MRI_with_B0_inhomogeneity.jpg",
        "diagram_title": "Susceptibility Distortion Correction (SDC): Geometric Unwarping vs. Signal Dropout",
        "diagram_guide": "Air-tissue interfaces near the sinuses warp the static B0 field. Because EPI has tiny bandwidth along the phase-encoding (PE) axis, field offsets Delta B0 shift voxels by several millimeters along PE and pile/stretch intensities—while through-slice dephasing causes irreversible T2* signal dropout.",
        "pipeline_steps": ["B0 Fieldmap or Reversed-PE Pair (AP/PA)", "Estimate Voxel Shift Map d_PE(x)", "Pullback Geometric Unwarping", "Jacobian Intensity Pile-Up Scaling", "Flag Irrecoverable Dropout Mask"],
        "equation": {
            "name": "EPI Phase-Encoding Voxel Shift & Jacobian Pile-Up Correction",
            "latex": r"\Delta y_{\text{PE}}(\mathbf{x}) = \frac{\gamma \, \Delta B_0(\mathbf{x})}{\text{BW}_{\text{PE}}} = \gamma \, \Delta B_0(\mathbf{x}) \cdot T_{\text{readout}}, \qquad I_{\text{corr}}(\mathbf{x}) = I_{\text{dist}}\!\big(\mathbf{x} + \Delta y_{\text{PE}}(\mathbf{x})\hat{\mathbf{e}}_{\text{PE}}\big) \cdot \left(1 + \frac{\partial \Delta y_{\text{PE}}}{\partial y_{\text{PE}}}\right)",
            "summary": "Relates local magnetic field inhomogeneity Delta B0 to millimeter displacement along the phase-encoding axis and corrects compression pile-up via the 1D Jacobian.",
            "terms": [
                {"term": r"\gamma \, \Delta B_0(\mathbf{x}) \cdot T_{\text{readout}}", "role": "Phase-Encoding Voxel Displacement", "meaning": "Off-resonance phase accumulated over the slow effective EPI readout time translates directly into spatial shift along the PE axis.", "failure": "Applying unwarping along the frequency-encoding axis or reversing the PE polarity sign (+y vs. -y), doubling the distortion."},
                {"term": r"1 + \frac{\partial \Delta y_{\text{PE}}}{\partial y_{\text{PE}}}", "role": "1D Jacobian Intensity Modulation", "meaning": "Corrects artificial intensity brightening where multiple native voxels were compressed into one distorted voxel.", "failure": "Shifting voxel positions without Jacobian scaling, leaving artificial hyperintensities in compressed frontal regions."},
                {"term": r"\text{Dropout vs. Distortion}", "role": "Irreversible Physics Boundary", "meaning": "Geometric unwarping moves surviving signal back to its true location, but cannot recreate signal destroyed by through-slice T2* dephasing.", "failure": "Claiming fieldmap unwarping restored orbitofrontal/ventral temporal signal that had already dropped to the noise floor."}
            ]
        }
    },
    "PR12": {
        "commons_file": "File:Gaussian_2d_0_degrees.png",
        "diagram_title": "Spatial Gaussian Smoothing, FWHM-to-Sigma Conversion & Boundary Bleed",
        "diagram_guide": "Convolving an image with an isotropic 3D Gaussian kernel suppresses high-frequency thermal noise and increases overlap across participants at the matched spatial scale (Matched Filter Theorem), but blurs signal across sulcal CSF boundaries and white matter.",
        "pipeline_steps": ["Specify Target FWHM (mm)", "Convert to Physical Sigma & Voxel Sigma", "Apply 3D Gaussian Convolution", "Measure Effective Smoothness (RESELs)", "Audit Cortical Boundary Contamination"],
        "equation": {
            "name": "Gaussian Kernel FWHM Conversion & Anisotropic Voxel Scaling",
            "latex": r"\sigma_{\text{mm}} = \frac{\text{FWHM}_{\text{mm}}}{\sqrt{8 \ln 2}} \approx \frac{\text{FWHM}_{\text{mm}}}{2.3548}, \qquad \sigma_{\text{vox}, d} = \frac{\sigma_{\text{mm}}}{\Delta x_d}, \qquad G(\mathbf{x}) = \frac{1}{(2\pi)^{3/2}\sigma_{\text{mm}}^3}\exp\!\left(-\frac{\|\mathbf{x}\|_2^2}{2\sigma_{\text{mm}}^2}\right)",
            "summary": "Converts a user-specified Full Width at Half Maximum (FWHM in mm) into the Gaussian standard deviation sigma in physical and per-axis voxel units.",
            "terms": [
                {"term": r"\sqrt{8 \ln 2} \approx 2.3548", "role": "FWHM-to-Sigma Conversion Constant", "meaning": "Exact ratio between the width where a Gaussian falls to 50% of its peak and its standard deviation sigma.", "failure": "Passing FWHM directly into scipy.ndimage.gaussian_filter(img, sigma=FWHM), over-smoothing by 2.35x in every dimension (13x in volume!)."},
                {"term": r"\sigma_{\text{vox}, d} = \sigma_{\text{mm}} / \Delta x_d", "role": "Anisotropic Voxel-Size Normalization", "meaning": "Divides physical millimeter sigma by each axis's voxel spacing Delta x_d so smoothing is isotropic in physical space.", "failure": "Using a single scalar voxel sigma on anisotropic slices (e.g., 2x2x4 mm), blurring twice as far through-plane."},
                {"term": r"\text{Boundary Bleed}", "role": "Spatial Resolution Trade-off", "meaning": "Volumetric smoothing averages gray matter with adjacent CSF and white matter; masked or surface-based smoothing prevents cross-tissue bleed.", "failure": "Smoothing before fine-grained MVPA/RSA or laminar analysis, destroying high-frequency spatial pattern information."}
            ]
        }
    },
    "PR13": {
        "commons_file": "File:Butterworth_filter_wp.svg",
        "diagram_title": "Temporal Frequency Filtering, Nyquist Aliasing & Passband Degrees of Freedom",
        "diagram_guide": "Slow scanner drift (<0.01 Hz) and physiological pulsations (respiration ~0.3 Hz, cardiac ~1.0 Hz) contaminate fMRI time series. Designing a digital filter requires knowing the exact sampling period TR, checking whether cardiac frequencies alias into the passband, and reducing effective degrees of freedom.",
        "pipeline_steps": ["Read Actual TR from Header", "Compute Nyquist f_N = 1/(2 TR)", "Check Physiological Aliasing", "Apply Zero-Phase Filter / DCT Drift Basis", "Update Effective Degrees of Freedom"],
        "equation": {
            "name": "Nyquist Folding Frequency & Zero-Phase Butterworth Magnitude Response",
            "latex": r"f_{\text{Nyquist}} = \frac{1}{2\,\text{TR}}, \qquad f_{\text{alias}} = \left|f_{\text{phys}} - k \cdot \frac{1}{\text{TR}}\right|, \qquad |H_{\text{filt}}(f)|^2 = \left(\frac{1}{1 + (f_{\text{c}} / f)^{2n}}\right)^2",
            "summary": "Determines the highest unaliased frequency at sampling interval TR, predicts where fast cardiac/respiratory rhythms fold back, and characterizes zero-phase high-pass filtering.",
            "terms": [
                {"term": r"f_{\text{Nyquist}} = \frac{1}{2\,\text{TR}}", "role": "Nyquist Bandwidth Ceiling", "meaning": "Maximum temporal frequency resolvable at sampling period TR (e.g., 0.25 Hz at TR=2.0 s; 0.625 Hz at TR=0.8 s).", "failure": "Hardcoding TR=2.0 s in filter design when the actual dataset was acquired at TR=0.72 s."},
                {"term": r"f_{\text{alias}} = |f_{\text{phys}} - k / \text{TR}|", "role": "Aliased Physiological Frequency", "meaning": "At long TR (e.g., 2.0 s), a 1.1 Hz cardiac pulse folds into 0.1 Hz—right inside the resting-state passband (0.01–0.10 Hz) where a bandpass filter cannot remove it.", "failure": "Assuming a 0.01–0.10 Hz bandpass filter removes cardiac noise from slow-TR fMRI."},
                {"term": r"\text{DOF}_{\text{eff}} = T \cdot \frac{\Delta f_{\text{pass}}}{f_{\text{Nyquist}}}", "role": "Passband Degree-of-Freedom Loss", "meaning": "Removing frequency bins restricts residual variance to a lower-dimensional subspace, reducing statistical degrees of freedom.", "failure": "Computing t-statistics or correlations after aggressive bandpass filtering without adjusting effective degrees of freedom."}
            ]
        }
    },
    "PR14": {
        "commons_file": "File:Independent_component_analysis_in_EEGLAB.png",
        "diagram_title": "Nuisance Regression, Orthogonal Subspace Projection & Joint vs. Modular Denoising",
        "diagram_guide": "Denoising removes variance spanned by nuisance regressors N (motion, WM/CSF CompCor, ICA noise components). However, if you bandpass-filter the data and then regress out unfiltered nuisance columns sequentially, the nuisance step re-injects stopband frequencies into your cleaned time series (Lindquist et al., 2019)!",
        "pipeline_steps": ["Assemble Nuisance Matrix N (Motion/CompCor/ICA)", "Combine Filter & Nuisance into X_nuis", "Form Orthogonal Projector P_perp", "Project Data y_clean = P_perp y", "Verify Stopband & Residual DOF"],
        "equation": {
            "name": "Joint Orthogonal Nuisance & Filter Subspace Projection",
            "latex": r"\mathbf{y}_{\text{clean}} = P_{N}^{\perp}\,\mathbf{y} = \left(I_T - N\left(N^T N\right)^{+} N^T\right)\mathbf{y}, \qquad \text{DOF}_{\text{resid}} = T - \operatorname{rank}(N)",
            "summary": "Projects the time series orthogonally onto the complement of the combined filter-and-nuisance column space in a single simultaneous linear operation.",
            "terms": [
                {"term": r"N = [N_{\text{motion}}, N_{\text{CompCor}}, N_{\text{filter}}]", "role": "Unified Nuisance & Drift Matrix", "meaning": "Concatenates motion expansions, anatomical WM/CSF PCA components, spike deltas, and frequency-filter bases into one design matrix.", "failure": "Sequential modular denoising (filtering Y first, then regressing out unfiltered N), which re-introduces filtered noise frequencies."},
                {"term": r"P_N^{\perp} = I_T - N(N^T N)^+ N^T", "role": "Idempotent Orthogonal Projector", "meaning": "Annihilates all components of y lying in column space C(N); satisfies (P_N^perp)^2 = P_N^perp.", "failure": "Subtracting non-orthogonalized nuisance fits sequentially, allowing shared variance to leak back in."},
                {"term": r"T - \operatorname{rank}(N)", "role": "Remaining Temporal Degrees of Freedom", "meaning": "Each linearly independent nuisance column consumes one temporal degree of freedom from the T time points.", "failure": "Consuming >70% of temporal DOF with aggressive nuisance models without accounting for variance inflation."}
            ]
        }
    },
    "PR15": {
        "commons_file": "File:Six_degrees_of_freedom.jpg",
        "diagram_title": "Quality Control (QC), Motion Scrubbing / Spike Censoring & Exclusion Bias",
        "diagram_guide": "High-motion frames (e.g., FD > 0.2 or 0.5 mm, high DVARS) cause distance-dependent functional connectivity artifacts. Censoring contaminated frames via one-hot spike regressors preserves temporal continuity, whereas naive array slicing before filtering corrupts temporal lag structure.",
        "pipeline_steps": ["Compute FD_t & DVARS_t Curves", "Flag Suprathreshold Frames & Neighbors", "Construct One-Hot Spike Matrix S_censor", "Enforce Minimum Retained Minutes (>4–5 min)", "Audit Retained vs. Excluded Sample Bias"],
        "equation": {
            "name": "One-Hot Spike Regression Censoring & Retained Effective Time",
            "latex": r"X_{\text{aug}} = \big[X_{\text{task/nuis}}, \; \mathbf{e}_{t_1}, \dots, \mathbf{e}_{t_C}\big], \qquad T_{\text{retained}} = (T - C)\cdot\text{TR} \ge T_{\min}, \qquad \text{DVARS}_t = \sqrt{\frac{1}{V}\sum_{v=1}^{V}\left(Y_{v,t} - Y_{v,t-1}\right)^2}",
            "summary": "Zeroes the influence of C motion-corrupted volumes via one-hot delta columns while tracking remaining clean scan duration and sample selection bias.",
            "terms": [
                {"term": r"\text{DVARS}_t", "role": "Whole-Brain RMS Intensity Derivative", "meaning": "Root-mean-square frame-to-frame signal change across all in-brain voxels, indexing global intensity spikes alongside kinematic FD_t.", "failure": "Checking only FD_t and missing non-kinematic coil spikes or delayed spin-history bursts."},
                {"term": r"\mathbf{e}_{t_c} \in \mathbb{R}^T", "role": "One-Hot Spike Censor Regressor", "meaning": "Indicator column with 1 at bad frame t_c and 0 elsewhere; absorbs 100% of frame t_c's residual without breaking uniform TR spacing.", "failure": "Deleting rows from the 4D array before temporal filtering or AR(1) modeling, which stitches non-adjacent time points together."},
                {"term": r"T_{\text{retained}} = (T - C)\cdot\text{TR}", "role": "Clean Scan Duration Gate", "meaning": "Total surviving seconds of clean data; participants falling below ~4–5 minutes have unstable connectivity estimates and must be flagged.", "failure": "Retaining participants with 30 seconds of uncensored data, or ignoring that excluding high-motion participants systematically drops younger/clinical individuals."}
            ]
        }
    },
    "PR16": {
        "commons_file": "File:DTschematic.jpg",
        "diagram_title": "Diffusion MRI Stejskal-Tanner Gradients, b-Values & B-Table Rotation Invariance",
        "diagram_guide": "Diffusion MRI sensitizes each volume to water molecule Brownian motion along a specific unit gradient vector g_k = (g_x, g_y, g_z) at diffusion weighting b_k (s/mm^2). If you rotate a participant's head during motion correction or registration, you must apply the exact same 3x3 rotation R to the gradient table!",
        "pipeline_steps": ["Verify Volume Count == bval == bvec", "Identify b=0 Baseline Shells", "Compute Stejskal-Tanner Attenuation", "Rotate DWIs by Rigid Matrix R", "Rotate Gradient Vectors g' = R g"],
        "equation": {
            "name": "Stejskal-Tanner Diffusion Attenuation & Gradient Rotation Rule",
            "latex": r"S(\mathbf{g}_k, b_k) = S_0 \exp\!\left(-b_k \, \text{ADC}(\mathbf{g}_k)\right), \qquad b = \gamma^2 G^2 \delta^2\!\left(\Delta - \frac{\delta}{3}\right), \qquad \mathbf{g}_k^{\text{rot}} = \frac{R\,\mathbf{g}_k}{\|R\,\mathbf{g}_k\|_2}",
            "summary": "Links directional signal attenuation to the apparent diffusion coefficient along gradient g_k and enforces coupled rotation of image volumes and gradient vectors.",
            "terms": [
                {"term": r"b = \gamma^2 G^2 \delta^2(\Delta - \delta/3)", "role": "Diffusion Weighting Factor (s/mm^2)", "meaning": "Summarizes gradient strength G, pulse duration delta, and diffusion time Delta; b=0 is the non-diffusion-weighted T2 reference.", "failure": "Treating b=5 s/mm^2 hardware crushers as heavy diffusion shells or failing to normalize by S0."},
                {"term": r"\exp(-b_k\,\text{ADC}(\mathbf{g}_k))", "role": "Directional Signal Attenuation", "meaning": "Water diffusing rapidly parallel to white-matter axons (g_k || fiber) dephases strongly, producing dark signal and high ADC.", "failure": "Reversing the physical interpretation and thinking bright DWI signal means high diffusivity."},
                {"term": r"\mathbf{g}_k^{\text{rot}} = R\,\mathbf{g}_k / \|R\,\mathbf{g}_k\|_2", "role": "Coupled B-Matrix Reorientation", "meaning": "Applies the rotational component of the image alignment transform to each unit gradient vector in .bvec.", "failure": "Rotating the 4D diffusion image volumes without rotating the .bvec table, misaligning all downstream fiber orientations."}
            ]
        }
    },
    "PR17": {
        "commons_file": "File:Gibbs_phenomenon_50.svg",
        "diagram_title": "Diffusion Preprocessing Order: Thermal Denoising, Gibbs Unringing & Eddy-Current Correction",
        "diagram_guide": "Each dMRI artifact arises at a specific physical stage: thermal noise is independent in raw k-space/voxel space (MP-PCA), sharp skull/CSF edges truncated in k-space create oscillating Gibbs rings, and rapid diffusion gradients induce eddy-current shears. Interpolating before denoising correlations thermal noise across voxels and breaks MP-PCA!",
        "pipeline_steps": ["1. Raw DWI Thermal Denoising (MP-PCA)", "2. Gibbs Ringing Removal (Subvoxel Shifts)", "3. Eddy Current + Motion + B0 Unwarping", "4. Single-Shot Interpolation + bvec Rotation", "5. N4 Bias Field Normalization"],
        "equation": {
            "name": "Sequential Operator Non-Commutativity in dMRI Preprocessing",
            "latex": r"I_{\text{clean}} = \left(\mathcal{E}_{\text{eddy+motion+SDC}} \circ \mathcal{U}_{\text{Gibbs}} \circ \mathcal{D}_{\text{MP-PCA}}\right)[I_{\text{raw}}] \neq \left(\mathcal{D}_{\text{MP-PCA}} \circ \mathcal{E}_{\text{eddy+motion+SDC}}\right)[I_{\text{raw}}]",
            "summary": "Demonstrates why Marchenko-Pastur PCA denoising and Gibbs unringing must precede spatial interpolation and eddy-current unwarping.",
            "terms": [
                {"term": r"\mathcal{D}_{\text{MP-PCA}}", "role": "First-Stage Thermal Noise Removal", "meaning": "Separates bulk Marchenko-Pastur random matrix noise eigenvalues from low-rank signal; requires spatially independent voxel noise.", "failure": "Running eddy/interpolation before MP-PCA, which correlates neighboring voxel noise and breaks the Marchenko-Pastur eigenvalue bound."},
                {"term": r"\mathcal{U}_{\text{Gibbs}}", "role": "Fourier Truncation Unringing", "meaning": "Removes sinc-oscillation ripples parallel to high-contrast CSF/white-matter boundaries via local subvoxel grid shifts.", "failure": "Leaving Gibbs rings uncorrected, creating artificial low-FA/negative-diffusivity bands in the corpus callosum."},
                {"term": r"\mathcal{E}_{\text{eddy+motion+SDC}}", "role": "Joint Geometric & Outlier Correction", "meaning": "Corrects gradient-direction-dependent eddy-current shears, head motion, slice dropout outliers, and susceptibility distortion in one resampling step.", "failure": "Resampling separately at each substep, compounding spatial blurring."}
            ]
        }
    },
    "PR18": {
        "commons_file": "File:DTI-axial-ellipsoids.jpg",
        "diagram_title": "Diffusion Tensor Ellipsoids, Eigenvalues (lambda_1, lambda_2, lambda_3), FA & Mean Diffusivity",
        "diagram_guide": "The 3x3 symmetric positive-definite diffusion tensor D models water displacement within each voxel as a 3D ellipsoid with principal axes (e_1, e_2, e_3) and eigenvalues (lambda_1 >= lambda_2 >= lambda_3 > 0). In coherent white matter tracts, water diffuses freely along axons (lambda_1 >> lambda_2, lambda_3), yielding high Fractional Anisotropy (FA).",
        "pipeline_steps": ["Log-Linear / WLS Tensor Fit (6+ dirs)", "Eigendecomposition D = V Lambda V^T", "Check Positive-Definiteness (lambda_i > 0)", "Compute MD, AD, RD & FA Maps", "Audit Crossing-Fiber Breakdown"],
        "equation": {
            "name": "Diffusion Tensor Model, Mean Diffusivity (MD) & Fractional Anisotropy (FA)",
            "latex": r"\ln\!\left(\frac{S(\mathbf{g}_k, b_k)}{S_0}\right) = -b_k\,\mathbf{g}_k^T D\,\mathbf{g}_k, \qquad \text{MD} = \frac{\lambda_1 + \lambda_2 + \lambda_3}{3}, \qquad \text{FA} = \sqrt{\frac{3}{2}\frac{(\lambda_1-\text{MD})^2 + (\lambda_2-\text{MD})^2 + (\lambda_3-\text{MD})^2}{\lambda_1^2 + \lambda_2^2 + \lambda_3^2}}",
            "summary": "Fits a 6-parameter symmetric diffusion tensor D to directional attenuations and summarizes its ellipsoid shape via Mean Diffusivity (trace/3) and normalized eigenvalue variance (FA).",
            "terms": [
                {"term": r"\mathbf{g}_k^T D\,\mathbf{g}_k", "role": "Quadratic Form Directional Diffusivity", "meaning": "Projects the symmetric 3x3 tensor D=[Dxx,Dxy,Dxz; Dyx,Dyy,Dyz; Dzx,Dzy,Dzz] onto unit gradient direction g_k (noting off-diagonal factor-of-2 in the 6-column design matrix).", "failure": "Omitting the factor of 2 on off-diagonal terms (2*gx*gy*Dxy) when constructing the linear least-squares design matrix."},
                {"term": r"\text{MD} = \bar{\lambda}", "role": "Isotropic Mean Diffusivity (mm^2/s)", "meaning": "Average diffusivity across all three principal axes; elevated in CSF and chronic tissue loss, reduced in acute cytotoxic edema.", "failure": "Allowing noise/Gibbs ringing to produce negative eigenvalues (lambda_3 < 0) without SPD projection."},
                {"term": r"\text{FA} \in [0, 1]", "role": "Normalized Anisotropy Ratio", "meaning": "Dimensionless index equal to 0 for an isotropic sphere (lambda_1=lambda_2=lambda_3) and approaching 1 for a thin cigar-shaped bundle.", "failure": "Interpreting low FA as 'myelin damage' in centrum semiovale voxels where two intact fiber bundles cross orthogonally."}
            ]
        }
    },
    "PR19": {
        "commons_file": "File:Tractography_animated_lateral_view.gif",
        "diagram_title": "Crossing Fibers, Orientation Distribution Functions (ODFs) & Tractography False Positives",
        "diagram_guide": "Roughly 60–90% of white-matter voxels contain crossing, kissing, or fanning fiber populations. While a single tensor collapses into an oblate pancake at a 90-degree crossing, Constrained Spherical Deconvolution (CSD) resolves multiple Orientation Distribution Function (ODF) lobes—yet streamlines remain macroscopic model trajectories, not microscopic axons (Maier-Hein et al., 2017).",
        "pipeline_steps": ["Multi-Shell / High-Angular DWI", "Spherical Deconvolution -> fODF Peaks", "Deterministic vs. Probabilistic Integration", "Anatomical Stopping & Angle Criteria", "Audit False-Positive Bottlenecks (PP06)"],
        "equation": {
            "name": "Spherical Deconvolution & Streamline Euler/Runge-Kutta Integration",
            "latex": r"S(\mathbf{g}) = \int_{S^2} \underbrace{F(\mathbf{u})}_{\text{Fiber ODF}} \, \underbrace{R(\mathbf{g}\cdot\mathbf{u})}_{\text{Single-Fiber Response}}\,d\mathbf{u}, \qquad \mathbf{r}(s + \Delta s) = \mathbf{r}(s) + \Delta s \cdot \mathbf{v}_{\text{peak}}\!\big(\mathbf{r}(s)\big)",
            "summary": "Deconvolves the measured spherical diffusion signal with a single-fiber response kernel to recover sharp fiber ODF peaks, then integrates streamline trajectories step-by-step.",
            "terms": [
                {"term": r"F(\mathbf{u}) \text{ on } S^2", "role": "Fiber Orientation Distribution Function", "meaning": "Continuous angular density of fiber bundles along unit direction u, capable of resolving 2–3 distinct crossing peaks per voxel.", "failure": "Using single-tensor deterministic tracking through crossing regions, causing premature termination or wrong turns."},
                {"term": r"\mathbf{r}(s + \Delta s) = \mathbf{r}(s) + \Delta s\,\mathbf{v}_{\text{peak}}", "role": "Streamline Step Integration", "meaning": "Propagates a curve in physical millimeter space along local ODF peak directions subject to curvature and WM mask constraints.", "failure": "Equating raw streamline count with physical axon count or synaptic connection strength without SIFT2/COMMIT weighting."},
                {"term": r"\text{Bottleneck Ambiguity}", "role": "Structural False-Positive Mechanism (PP06)", "meaning": "Multiple distinct anatomical tracts enter the same white-matter bottleneck with identical orientations and exit along all combinations.", "failure": "Assuming higher angular resolution or probabilistic sampling automatically eliminates false-positive bundles."}
            ]
        }
    },
    "PR20": {
        "commons_file": "File:Connectome_extraction_procedure.jpg",
        "diagram_title": "Brain Parcellations, Regional Time-Series Aggregation & Functional/Structural Connectomes",
        "diagram_guide": "Parcellation compresses ~100,000 noisy voxels into P=100–400 anatomically or functionally homogeneous parcels. Extracting regional signals requires verifying parcel coverage against susceptibility dropout masks and choosing a connectivity estimator (Pearson, Partial/Graphical Lasso, or Fisher-z).",
        "pipeline_steps": ["Verify Atlas Grid & Nearest-Neighbor Resampling", "Audit Parcel Voxel Coverage (>=80%)", "Aggregate Clean Regional Signals X_p(t)", "Estimate Full vs. Regularized Partial Correlation", "Apply Fisher r-to-z Transform"],
        "equation": {
            "name": "Parcel Signal Aggregation, Precision-Matrix Partial Correlation & Fisher z-Transform",
            "latex": r"\bar{x}_p(t) = \frac{1}{|\Omega_p \cap M_{\text{good}}|}\sum_{v \in \Omega_p \cap M_{\text{good}}} Y_{v,t}, \qquad \rho_{pq \mid \text{rest}} = -\frac{\Theta_{pq}}{\sqrt{\Theta_{pp}\,\Theta_{qq}}}, \qquad z_{pq} = \operatorname{arctanh}(r_{pq}) = \frac{1}{2}\ln\frac{1+r_{pq}}{1-r_{pq}}",
            "summary": "Averages surviving in-mask voxels within each parcel, distinguishes direct partial correlations (via inverse covariance Theta = Sigma^{-1}) from marginal Pearson correlations, and variance-stabilizes edges via Fisher's z.",
            "terms": [
                {"term": r"\Omega_p \cap M_{\text{good}}", "role": "Coverage-Verified Parcel Mask", "meaning": "Restricts parcel p's average to voxels surviving the brain and susceptibility-dropout mask; flags parcels losing >20–50% of their voxels.", "failure": "Averaging over zeroed/dropped-out orbitofrontal voxels and interpreting low correlation as biological disconnection."},
                {"term": r"\rho_{pq \mid \text{rest}} = -\Theta_{pq}/\sqrt{\Theta_{pp}\Theta_{qq}}", "role": "Direct Partial Correlation", "meaning": "Conditional correlation between parcels p and q after removing linear mediating effects of all other P-2 regions via precision matrix Theta = (Sigma + lambda I)^{-1}.", "failure": "Inverting sample covariance when T < P without Ledoit-Wolf or L1/L2 shrinkage."},
                {"term": r"z_{pq} = \operatorname{arctanh}(r_{pq})", "role": "Fisher Variance-Stabilizing Transform", "meaning": "Maps bounded correlations r in (-1,1) to (-inf,+inf) with approximate variance 1/(T_eff - 3) for group averaging and modeling.", "failure": "Averaging raw bounded correlation coefficients r_pq near +-1 directly across participants."}
            ]
        }
    },
    "PR21": {
        "commons_file": "File:Directed_acyclic_graph_2.svg",
        "diagram_title": "Reproducible Processing Graphs (DAGs), Provenance Manifests & Automated QC Audits",
        "diagram_guide": "A neuroimaging pipeline (Nipype / fMRIPrep / QSIPrep) is a Directed Acyclic Graph (DAG) of deterministic nodes. Any change to an upstream input file, software version, or parameter invalidates all downstream nodes and updates their cryptographic provenance hashes.",
        "pipeline_steps": ["BIDS Input + SHA-256 Digest", "Topological Sort of Pipeline DAG", "Execute Node & Record Parameter Hash", "Generate Visual + Quantitative QC Report", "Emit W3C PROV / BIDS Derivatives Manifest"],
        "equation": {
            "name": "Merkle-DAG Provenance Hash & Two-Stage QC Gate",
            "latex": r"h(u) = \operatorname{SHA256}\!\Big(\text{code}(u) \;\|\; \boldsymbol{\theta}_u \;\|\; \big\|_{v \in \operatorname{Pa}(u)} h(v)\Big), \qquad \text{Pass}(s) = \mathbb{I}\!\left(\text{QC}_{\text{quant}}(s) \in \mathcal{R}_{\text{valid}}\right) \wedge \mathbb{I}\!\left(\text{QC}_{\text{visual}}(s) = \text{OK}\right)",
            "summary": "Computes each pipeline node's cache key recursively from its parents' hashes and requires both quantitative thresholds and visual overlay inspection before analysis.",
            "terms": [
                {"term": r"\operatorname{Pa}(u)", "role": "Upstream Parent Dependencies", "meaning": "Set of all immediate predecessor nodes feeding into step u in the Directed Acyclic Graph.", "failure": "Re-running a downstream GLM after changing brain extraction without recomputing intermediate registration and denoising nodes."},
                {"term": r"h(u)", "role": "Recursive Cryptographic Provenance Digest", "meaning": "Uniquely fingerprints the exact input bytes, parameter dictionary theta_u, and parent hashes that produced artifact u.", "failure": "Overwriting output filenames in-place with no record of which parameter version generated the map."},
                {"term": r"\text{QC}_{\text{quant}} \wedge \text{QC}_{\text{visual}}", "role": "Conjunctive Quality-Control Gate", "meaning": "Requires passing both automated metrics (FD, Dice, tSNR, Euler number) and human visual inspection of pial/white and EPI-to-T1w overlays.", "failure": "Trusting green exit codes (return code 0) or summary numbers alone without inspecting visual registration overlays."}
            ]
        }
    },
    "D01": {
        "commons_file": "File:Comparison_confounder_mediator.svg",
        "diagram_title": "Causal Estimands, Potential Outcomes & Confounder vs. Mediator vs. Collider Structure",
        "diagram_guide": "Before choosing a statistical test, state the scientific question as a formal estimand: the target population, the exposure/contrast, the unit of analysis, and the causal graph. Adjusting for a common-cause confounder Z removes bias, whereas conditioning on a post-treatment mediator M or common-effect collider C creates bias!",
        "pipeline_steps": ["Define Target Population & Unit i", "State Potential Outcomes Y_i(1), Y_i(0)", "Draw Causal DAG (Confounder vs. Collider)", "Select Minimal Adjustment Set Z", "Map Estimand to Statistical Estimator"],
        "equation": {
            "name": "Average Treatment Effect (ATE) & Backdoor Adjustment Formula",
            "latex": r"\tau_{\text{ATE}} = \mathbb{E}\!\big[Y_i(1) - Y_i(0)\big] = \sum_{z} \Big(\mathbb{E}[Y \mid A=1, Z=z] - \mathbb{E}[Y \mid A=0, Z=z]\Big) P(Z=z)",
            "summary": "Links the unobservable counterfactual causal estimand to observable conditional expectations when all backdoor confounding paths Z are blocked.",
            "terms": [
                {"term": r"Y_i(1) - Y_i(0)", "role": "Individual Counterfactual Contrast", "meaning": "Difference between participant i's brain outcome under exposure A=1 versus A=0; only one potential outcome is ever observed per person at a fixed time.", "failure": "Jumping straight to a software button (e.g., 'run two-sample t-test') without defining the causal or descriptive target estimand."},
                {"term": r"Z \text{ (Backdoor Confounder Set)}", "role": "Pre-Exposure Common Causes", "meaning": "Variables (e.g., age, scanner site, head motion tendency) that cause both exposure A and brain outcome Y and must be adjusted for.", "failure": "Conditioning on a collider C (A -> C <- Y, e.g., hospital admission or QC selection driven by both disease and scan quality), inducing spurious association."},
                {"term": r"\sum_z (\dots) P(Z=z)", "role": "Target-Population Standardization", "meaning": "Averages stratum-specific differences over the marginal distribution of Z in the target population.", "failure": "Interpreting observational neuroimaging correlations as causal intervention effects when unmeasured confounders remain open."}
            ]
        }
    },
    "D02": {
        "commons_file": "File:Stratified_sampling.PNG",
        "diagram_title": "Sampling Frames, Missingness Mechanisms (MCAR / MAR / MNAR) & Participant vs. Row Units",
        "diagram_guide": "Neuroimaging tables often contain multiple rows per participant (runs, visits, parcels). Treating rows as independent participants inflates sample size, and dropping participants who fail motion QC alters the target population unless missingness is properly weighted.",
        "pipeline_steps": ["Target Population vs. Convenience Sample", "Audit Row-to-Participant Hierarchy", "Diagnose Missingness (MCAR / MAR / MNAR)", "Compute Inverse Probability Weights (IPW)", "Aggregate Uncertainty at Participant Level"],
        "equation": {
            "name": "Horvitz-Thompson Inverse Probability Weighting (IPW) & Design Effect",
            "latex": r"\hat{\mu}_{\text{IPW}} = \frac{\sum_{i=1}^{N} \dfrac{R_i}{\hat{\pi}(\mathbf{X}_i)} Y_i}{\sum_{i=1}^{N} \dfrac{R_i}{\hat{\pi}(\mathbf{X}_i)}}, \qquad N_{\text{eff}} = \frac{N \cdot m}{1 + (m - 1)\rho_{\text{ICC}}}",
            "summary": "Reweights retained participants (R_i=1) by the inverse of their retention probability pi(X_i) under MAR and adjusts effective sample size for within-participant clustering.",
            "terms": [
                {"term": r"R_i \in \{0, 1\}", "role": "Retention / QC Survival Indicator", "meaning": "Equals 1 if participant i's scan survives acquisition and motion QC, and 0 if missing/excluded.", "failure": "Assuming complete-case analysis is unbiased when motion exclusion (R_i=0) correlates with age or clinical symptom severity."},
                {"term": r"1 / \hat{\pi}(\mathbf{X}_i)", "role": "Inverse Retention Propensity Weight", "meaning": "Upweights retained participants from demographic/clinical strata X_i that had higher exclusion rates, restoring target-population balance under MAR.", "failure": "Ignoring extreme propensity weights near zero without stabilization or positivity checks."},
                {"term": r"1 + (m - 1)\rho_{\text{ICC}}", "role": "Cluster Variance Inflation (Design Effect)", "meaning": "Factor by which m repeated scans/rows per person inflate variance when within-person correlation rho_ICC > 0.", "failure": "Running df = N*m - 2 across all rows as if 4 runs from 20 people were 80 independent humans."}
            ]
        }
    },
    "D03": {
        "commons_file": "File:Intraclass_correlation_coefficient_graph_improved.svg",
        "diagram_title": "Test-Retest Reliability, Intraclass Correlation (ICC) & Group vs. Individual Paradox",
        "diagram_guide": "A robust group-level task effect (e.g., Stroop or Flanker activation) occurs when within-subject differences are consistent across everyone (small between-subject variance sigma_B^2). Paradoxically, that same low between-subject variance makes the measure unreliable for ranking individual differences (low ICC; Hedge et al., 2018)!",
        "pipeline_steps": ["Repeated Session Measurements Y_{ij}", "Partition Variance (sigma_B^2, sigma_S^2, sigma_E^2)", "Compute ICC(3,1) Consistency vs. ICC(2,1) Agreement", "Evaluate Bland-Altman Bias & Limits", "Check Attenuation of Brain-Behavior r"],
        "equation": {
            "name": "Intraclass Correlation Coefficient: Consistency ICC(3,1) vs. Absolute Agreement ICC(2,1)",
            "latex": r"\text{ICC}(3,1) = \frac{\sigma_{\text{between}}^2}{\sigma_{\text{between}}^2 + \sigma_{\text{error}}^2}, \qquad \text{ICC}(2,1) = \frac{\sigma_{\text{between}}^2}{\sigma_{\text{between}}^2 + \sigma_{\text{session}}^2 + \sigma_{\text{error}}^2}",
            "summary": "Expresses individual-difference reliability as the fraction of total measurement variance attributable to true stable differences between people.",
            "terms": [
                {"term": r"\sigma_{\text{between}}^2", "role": "True Between-Person Variance", "meaning": "Variance of stable trait levels across individuals in the population; must be large for a biomarker to rank people reliably.", "failure": "Assuming a task with a huge group t-statistic automatically has high individual-difference reliability (the Reliability Paradox)."},
                {"term": r"\sigma_{\text{session}}^2", "role": "Systematic Session / Scanner Shift", "meaning": "Global offset between Session 1 and Session 2 (e.g., scanner upgrade or habituation); penalized by ICC(2,1) agreement but ignored by Pearson r and ICC(3,1).", "failure": "Using Pearson r to claim longitudinal measurement equivalence when Session 2 is systematically shifted."},
                {"term": r"\sigma_{\text{error}}^2", "role": "Residual Within-Person Noise", "meaning": "Participant-by-session interaction plus thermal/physiological scan noise; shrinks by 1/k when averaging k repeat sessions in ICC(2,k).", "failure": "Entering low-ICC contrast scores (ICC < 0.4) into small-sample brain-behavior correlations."}
            ]
        }
    },
    "D04": {
        "commons_file": "File:False_positives_and_false_negatives.svg",
        "diagram_title": "Statistical Power, Precision Planning & The Winner's Curse (Type M and Type S Errors)",
        "diagram_guide": "When statistical power is low (e.g., 15–20% in small-N neuroimaging studies), the few results that cross the p < 0.05 significance threshold are guaranteed by conditional truncation to have massively exaggerated effect sizes (Type M error / Winner's Curse) and an elevated risk of having the wrong sign (Type S error)!",
        "pipeline_steps": ["Specify Realistic Attenuated Effect delta", "Compute Noncentrality Parameter lambda", "Evaluate Power 1 - beta at Stringent alpha", "Audit Type M Exaggeration & Type S Sign Error", "Plan Sample Size for CI Half-Width w"],
        "equation": {
            "name": "Noncentral-t Power, Winner's Curse Exaggeration (Type M) & Precision Sample Size",
            "latex": r"\lambda = d_{\text{obs}}\sqrt{N_{\text{eff}}}, \qquad \text{Type M} = \frac{\mathbb{E}\!\left[|\hat{d}| \;\middle|\; |T| > t_{1-\alpha/2}\right]}{|d_{\text{true}}|} \gg 1 \text{ when Power is low}, \qquad N_{\text{CI}} \ge \left(\frac{z_{1-\alpha/2}\,\sigma}{w}\right)^2",
            "summary": "Connects sample size and effect size to the noncentrality parameter lambda, explains why significant hits in underpowered studies overestimate true effects, and sizes studies for confidence-interval width.",
            "terms": [
                {"term": r"\lambda = d_{\text{obs}}\sqrt{N_{\text{eff}}}", "role": "Signal-to-Noise Noncentrality Parameter", "meaning": "Ratio of true (reliability-attenuated) effect size to standard error; governs the shift of the alternative t-distribution.", "failure": "Plugging an inflated pilot-study effect size (d=0.9 from N=20) into a power calculator."},
                {"term": r"\mathbb{E}[|\hat{d}| \mid |T| > t_{\text{crit}}] / |d_{\text{true}}|", "role": "Type M Exaggeration Ratio (Winner's Curse)", "meaning": "Conditioning on crossing a strict significance threshold truncates the sampling distribution to its outer tails, inflating observed effects by 2x–5x at low power.", "failure": "Interpreting a significant p<0.001 voxel in N=25 as proof that the true population effect is large."},
                {"term": r"(z_{1-\alpha/2}\,\sigma / w)^2", "role": "Precision-Based Sample Size Target", "meaning": "Sample size required to guarantee that the 95% confidence interval half-width does not exceed a scientifically tolerable margin w.", "failure": "Planning for alpha=0.05 single-test power when the real analysis tests 50,000 voxels or edges."}
            ]
        }
    },
    "D05": {
        "commons_file": "File:Haemodynamic_response_function.svg",
        "diagram_title": "Block vs. Event-Related Designs, HRF Convolution & Sub-TR Microtime Sampling",
        "diagram_guide": "Neuronal events s(t) stored in BIDS events.tsv (onset and duration in seconds) pass through the sluggish canonical double-gamma Hemodynamic Response Function h(t) (peaking at ~5–6 s with a ~16 s undershoot). Convolving on a fine sub-TR microtime grid before sampling at slice acquisition times preserves sub-second onset precision.",
        "pipeline_steps": ["Read BIDS events.tsv (Seconds)", "Rasterize Stimulus on Sub-TR Grid dt", "Convolve with Canonical HRF h(t)", "Sample at TR + Slice Offset", "Check Condition Collinearity"],
        "equation": {
            "name": "Continuous Neural-to-BOLD HRF Convolution & Discrete Scan Sampling",
            "latex": r"x_c(t) = (s_c * h)(t) = \int_{0}^{\infty} s_c(t - \tau)\,h(\tau)\,d\tau, \qquad X_{n, c} = x_c\!\left(n\cdot\text{TR} + t_{\text{ref}}\right), \qquad h(\tau) = \frac{\tau^{a_1-1}e^{-\tau/b_1}}{\Gamma(a_1)b_1^{a_1}} - \frac{1}{c}\frac{\tau^{a_2-1}e^{-\tau/b_2}}{\Gamma(a_2)b_2^{a_2}}",
            "summary": "Convolves the neural boxcar/stick stimulus train s_c(t) with the double-gamma hemodynamic impulse response h(tau) in continuous time, then samples at each volume acquisition timestamp.",
            "terms": [
                {"term": r"s_c(t - \tau)", "role": "Microtime Neural Stimulus Function", "meaning": "Indicator or parametric modulation train in seconds built from onset and duration columns of events.tsv.", "failure": "Rounding event onsets to the nearest integer TR before convolution, destroying jittered event-related timing."},
                {"term": r"h(\tau) \text{ (Double-Gamma HRF)}", "role": "Hemodynamic Low-Pass Impulse Response", "meaning": "Difference of a positive gamma peak (~5–6 s delay) and a smaller delayed undershoot gamma (~16 s delay), acting as a ~0.18 Hz low-pass filter.", "failure": "Using closely spaced fixed-ISI trials without jitter, causing overlapping HRFs to merge into a flat constant."},
                {"term": r"X_{n, c} = x_c(n\cdot\text{TR} + t_{\text{ref}})", "role": "Scan-Time Design Matrix Entry", "meaning": "Samples the continuous convolved predictor at the exact reference timestamp of scan n (and truncates the tail to length N_scans).", "failure": "Forgetting to slice np.convolve(s, h)[:N_scans], producing a design vector longer than the fMRI time series."}
            ]
        }
    },
    "D06": {
        "commons_file": "File:SPM_hemodynamic_response_function.png",
        "diagram_title": "HRF Shape Misspecification: Canonical Basis Sets vs. Finite Impulse Response (FIR) Deconvolution",
        "diagram_guide": "Hemodynamic latency and dispersion vary across brain regions and age groups. If a region's true response peaks 2 seconds late, a rigid 1-column canonical HRF underestimates amplitude and spills structured waves into the residuals—whereas adding temporal/dispersion derivatives or a flexible FIR basis captures the true waveform.",
        "pipeline_steps": ["Audit Canonical HRF Residual Waves", "Augment with Temporal & Dispersion Derivatives", "Fit K-Lag FIR Toeplitz Deconvolution Matrix", "Compute Bias-Corrected Steffener Amplitude", "Compare AIC/BIC Bias-Variance Trade-off"],
        "equation": {
            "name": "Taylor Basis Expansion vs. Finite Impulse Response (FIR) Deconvolution",
            "latex": r"y(t) = \beta_1 (s * h)(t) + \beta_2 \left(s * \frac{\partial h}{\partial t}\right)\!(t) + \beta_3 \left(s * \frac{\partial h}{\partial w}\right)\!(t) + \varepsilon(t) \quad \text{vs.} \quad y_t = \sum_{k=0}^{K-1} \theta_k \, s_{t - k} + \varepsilon_t",
            "summary": "Contrasts a 3-parameter Taylor expansion around the canonical HRF against a model-free K-bin Finite Impulse Response (FIR) lagged indicator basis.",
            "terms": [
                {"term": r"\beta_2 \left(s * \frac{\partial h}{\partial t}\right)", "role": "First-Order Latency Shift Term", "meaning": "Linear combination with the temporal derivative captures small (+/- 1 s) onset latency shifts; combined magnitude is sign(beta_1)*sqrt(beta_1^2 + beta_2^2).", "failure": "Adding the derivative to the GLM design matrix but testing only beta_1 at the group level, which still penalizes delayed regions."},
                {"term": r"\sum_{k=0}^{K-1} \theta_k \, s_{t-k}", "role": "Model-Free FIR Toeplitz Basis", "meaning": "Estimates a separate free parameter theta_k at every post-stimulus time bin k=0..K-1 with zero parametric shape assumptions.", "failure": "Using FIR on an unjittered periodic design where Toeplitz lag columns are collinear (rank-deficient)."},
                {"term": r"1 \text{ param vs. } K \text{ params}", "role": "Bias-Variance Trade-off", "meaning": "Canonical HRF has low variance (1 DOF) but high bias under latency shift; FIR has zero shape bias but K-fold higher parameter estimation variance.", "failure": "Fitting a 12-bin FIR model to only a handful of trials without checking design conditioning."}
            ]
        }
    },
    "D07": {
        "commons_file": "File:Comparison_convolution_correlation.svg",
        "diagram_title": "Contrast-Specific Experimental Design Efficiency: Detection vs. HRF Estimation",
        "diagram_guide": "Design efficiency is not a property of a stimulus schedule in isolation—it belongs to a specific contrast vector c under a specific noise covariance V! Block designs concentrate power at low frequencies to maximize detection of A vs. Baseline, whereas jittered m-sequence event designs spread spectrum to maximize A - B contrast and FIR shape estimation.",
        "pipeline_steps": ["Define Candidate Stimulus Schedules", "Specify Target Contrast Vector c", "Include Drift & AR(1) Noise Matrix V", "Evaluate Efficiency [c^T (X^T V^{-1} X)^{-1} c]^{-1}", "Optimize Jitter & Null-Trial Fraction"],
        "equation": {
            "name": "Contrast-Specific Generalized Least-Squares Design Efficiency",
            "latex": r"\operatorname{Eff}(\mathbf{c}, X, V) = \frac{\sigma^2}{\operatorname{Var}(\mathbf{c}^T\hat{\boldsymbol{\beta}})} = \left[\mathbf{c}^T \left(X^T V^{-1} X\right)^{-1} \mathbf{c}\right]^{-1}",
            "summary": "Measures the inverse variance of a specific linear contrast c^T beta-hat given the convolved design matrix X and temporal noise autocorrelation structure V.",
            "terms": [
                {"term": r"\mathbf{c} \in \mathbb{R}^p", "role": "Target Contrast Vector", "meaning": "Weights defining the exact scientific comparison (e.g., [1, -1, 0] for Condition A minus Condition B, or [0.5, 0.5, 0] for task vs. rest).", "failure": "Optimizing trace((X^T X)^{-1}) globally without specifying whether the study cares about A-B difference or A+B detection."},
                {"term": r"X^T V^{-1} X", "role": "Noise-Weighted Fisher Information Matrix", "meaning": "Measures how much signal energy the convolved regressors X retain after downweighting autocorrelated and high-pass-filtered frequencies via V^{-1}.", "failure": "Using ultra-long 60 s blocks whose fundamental frequency (0.008 Hz) gets erased by the 0.01 Hz high-pass drift filter."},
                {"term": r"\left[\mathbf{c}^T (X^T V^{-1} X)^{-1} \mathbf{c}\right]^{-1}", "role": "Precision of the Contrast Estimate", "meaning": "Doubling design efficiency cuts the contrast variance in half—equivalent to doubling scan duration or participant count for within-run precision.", "failure": "Evaluating design efficiency on unconvolved binary stimulus sticks instead of HRF-convolved predictors."}
            ]
        }
    },
    "D08": {
        "commons_file": "File:GSS_sealevel_interaction.png",
        "diagram_title": "Factorial Designs, Interaction Contrasts, Parameterization & Unbalanced Confounding",
        "diagram_guide": "In a 2x2 factorial design (Factor A x Factor B), an interaction tests whether the effect of A changes across levels of B: (A2B2 - A1B2) - (A2B1 - A1B1). In dummy (treatment) coding, 'main effect' coefficients represent simple effects at the reference level, whereas sum-to-zero effects coding (+1/-1) estimates marginal main effects directly.",
        "pipeline_steps": ["Specify 2x2 Cell Means Matrix", "Compare Dummy (0/1) vs. Sum (+1/-1) Coding", "Form Difference-of-Differences Contrast c_AB", "Audit Cell Sample-Size Balance n_{ab}", "Separate Type I vs. Type III Sums of Squares"],
        "equation": {
            "name": "2x2 Factorial Interaction Estimand & Coding Invariance",
            "latex": r"\theta_{A \times B} = \underbrace{(\mu_{11} - \mu_{01})}_{\text{Effect of } A \text{ at } B=1} - \underbrace{(\mu_{10} - \mu_{00})}_{\text{Effect of } A \text{ at } B=0} = \mu_{11} - \mu_{10} - \mu_{01} + \mu_{00} = \mathbf{c}_{\text{int}}^T \boldsymbol{\mu}",
            "summary": "Defines the 2x2 interaction as a symmetric difference-of-differences across the four cell means, invariant to whether the model uses cell-means, dummy, or sum coding.",
            "terms": [
                {"term": r"(\mu_{11} - \mu_{01}) - (\mu_{10} - \mu_{00})", "role": "Difference-of-Differences Estimand", "meaning": "Tests whether the slope of Factor A in condition B=1 differs from the slope of Factor A in condition B=0.", "failure": "Claiming an interaction because Condition B=1 had p=0.03 and B=0 had p=0.07 without testing the difference (Nieuwenhuis et al., 2011)!"},
                {"term": r"\beta_A^{\text{dummy}} = \mu_{10} - \mu_{00} \;\text{vs.}\; \beta_A^{\text{sum}}", "role": "Coding-Dependent Main Effect Meaning", "meaning": "Under 0/1 dummy coding with an interaction term, beta_A is the simple effect at B=0, NOT the grand marginal main effect of A.", "failure": "Interpreting beta_A from a dummy-coded model with A*B interaction as the overall main effect across both levels of B."},
                {"term": r"n_{ab} \text{ Unbalanced Confounding}", "role": "Non-Orthogonal Factor Collinearity", "meaning": "When cell counts n_{ab} are unequal (e.g., clinical patients mostly scanned on Scanner 2), Factor A and Factor B share variance and Type I SS depends on entry order.", "failure": "Scanning patients on one scanner and controls on another, where Group and Site become 100% collinear."}
            ]
        }
    },
    "D09": {
        "commons_file": "File:Least_squares_projection_geometry.png",
        "diagram_title": "General Linear Model (GLM) Orthogonal Projection, Contrast t-Statistics & Omnibus F-Tests",
        "diagram_guide": "Fitting a GLM Y = X beta + epsilon projects the T-dimensional fMRI time-series vector Y orthogonally onto the column space C(X) spanned by the design matrix. The residual vector e = Y - X beta-hat is strictly orthogonal to C(X), providing the noise variance estimate sigma-hat^2 with df = T - rank(X).",
        "pipeline_steps": ["Verify Design Rank & Column Names", "Project Y onto C(X): beta-hat = X^+ Y", "Compute Residual Variance sigma-hat^2 (df = T - p)", "Evaluate Directional Contrast t-Statistic", "Evaluate Multi-Row Omnibus F-Statistic"],
        "equation": {
            "name": "GLM Contrast t-Statistic & Multi-Row Omnibus F-Statistic",
            "latex": r"t = \frac{\mathbf{c}^T \hat{\boldsymbol{\beta}}}{\sqrt{\hat{\sigma}^2 \, \mathbf{c}^T (X^T X)^{-1} \mathbf{c}}}, \qquad \hat{\sigma}^2 = \frac{\|\mathbf{y} - X\hat{\boldsymbol{\beta}}\|_2^2}{T - \operatorname{rank}(X)}, \qquad F = \frac{(C\hat{\boldsymbol{\beta}})^T \big[C(X^T X)^{-1}C^T\big]^{-1} (C\hat{\boldsymbol{\beta}}) / q}{\hat{\sigma}^2}",
            "summary": "Divides the estimated linear contrast c^T beta-hat by its column-covariance-aware standard error, and generalizes to q-row matrix contrasts C via the F-statistic.",
            "terms": [
                {"term": r"\mathbf{c}^T \hat{\boldsymbol{\beta}}", "role": "Linear Contrast Effect Numerator", "meaning": "Signed linear combination of estimated regression weights answering the specific scientific question (preserve sign and units for group Level-2 models!).", "failure": "Passing thresholded t-maps instead of signed contrast estimates (con_*.nii / COPEs) to group-level analyses."},
                {"term": r"\hat{\sigma}^2 = \frac{\|\mathbf{e}\|_2^2}{T - \operatorname{rank}(X)}", "role": "Unbiased Residual Variance Estimator", "meaning": "Sum of squared orthogonal residuals divided by residual degrees of freedom df = T - rank(X).", "failure": "Dividing by T instead of T - rank(X), underestimating noise variance when many regressors are included."},
                {"term": r"\mathbf{c}^T (X^T X)^{-1} \mathbf{c}", "role": "Design Variance-Covariance Scaling", "meaning": "Includes off-diagonal covariance -2 c_1 c_2 [(X^T X)^{-1}]_{12} when predictors are correlated.", "failure": "Ignoring off-diagonal design covariance when computing the standard error of beta_A - beta_B."}
            ]
        }
    },
    "D10": {
        "commons_file": "File:Acf_new.svg",
        "diagram_title": "Temporal Autocorrelation in fMRI Residuals & Generalized Least Squares (GLS) Prewhitening",
        "diagram_guide": "Because hemodynamic physiology and unmodeled neural fluctuations evolve slowly, fMRI GLM residuals exhibit positive lag-1 autocorrelation (rho_1 > 0). Ordinary Least Squares (OLS) assumes independent errors (V = I), underestimating standard errors for low-frequency designs and inflating false-positive rates unless prewhitened via W = V^{-1/2}!",
        "pipeline_steps": ["Inspect OLS Residual ACF & Durbin-Watson", "Estimate AR(1) / ARMA / FAST Covariance V", "Construct Whitening Matrix W = V^{-1/2}", "Transform Both Data W y and Design W X", "Verify Flat White-Noise Residual Spectrum"],
        "equation": {
            "name": "GLS Prewhitening Transformation & OLS Variance Bias Under Autocorrelation",
            "latex": r"W\mathbf{y} = (WX)\boldsymbol{\beta} + W\boldsymbol{\varepsilon}, \quad W^T W = V^{-1} \implies \hat{\boldsymbol{\beta}}_{\text{GLS}} = \left(X^T V^{-1} X\right)^{-1} X^T V^{-1}\mathbf{y}, \quad \operatorname{Cov}(\hat{\boldsymbol{\beta}}_{\text{GLS}}) = \sigma^2\left(X^T V^{-1} X\right)^{-1}",
            "summary": "Left-multiplies both the time series y and design matrix X by the whitening filter W = V^{-1/2} so transformed residuals are spherical and t-statistics achieve nominal false-positive control.",
            "terms": [
                {"term": r"V_{t, s} = \rho^{|t-s|} \text{ or AR(p)+WN}", "role": "Temporal Error Correlation Matrix", "meaning": "Captures serial correlation across time points (particularly strong at fast multiband TR < 1 s, requiring FAST/higher-order AR models).", "failure": "Using naive OLS (V = I) on fMRI time series, which underestimates Var(c^T beta-hat) and inflates false positives."},
                {"term": r"W\mathbf{y} \text{ and } WX", "role": "Simultaneous Data & Design Prewhitening", "meaning": "Applies the whitening matrix W = V^{-1/2} to BOTH the fMRI data vector and every column of the design matrix X.", "failure": "Whitening only the data y while leaving the design matrix X unwhitened, which biases the regression slope estimates."},
                {"term": r"(X^T X)^{-1} X^T V X (X^T X)^{-1}", "role": "True OLS Sandwich Variance", "meaning": "Shows why naive OLS variance sigma^2 (X^T X)^{-1} is downward-biased whenever task regressors share low frequencies with positive autocorrelation in V.", "failure": "Assuming autocorrelation only affects parameter efficiency and not Type I error rates."}
            ]
        }
    },
    "D11": {
        "commons_file": "File:Mixedandfixedeffects.jpg",
        "diagram_title": "Multi-Level Hierarchy (Scans -> Runs -> Participants -> Sites), Mixed Effects & Pseudoreplication",
        "diagram_guide": "In group fMRI and longitudinal cohorts, trials and runs are nested inside participants, and participants are nested inside families or sites. Fixed-effects (FFX) pooling tests only the scanned individuals, whereas Random/Mixed-Effects (RFX / LMM) models between-participant variance tau^2 so claims generalize to the human population.",
        "pipeline_steps": ["Map Nesting Hierarchy (Run in Subject in Site)", "Compute Subject-Level Summary Contrast c_i", "Estimate Within-Subject s_i^2 & Between-Subject tau^2", "Fit DerSimonian-Laird / REML Mixed Model", "Verify Satterthwaite Degrees of Freedom"],
        "equation": {
            "name": "Two-Level Hierarchical Mixed-Effects Model (FLAME / DerSimonian-Laird)",
            "latex": r"\hat{c}_i = \mu_{\text{group}} + b_i + \varepsilon_i, \quad b_i \sim \mathcal{N}(0, \tau^2), \quad \varepsilon_i \sim \mathcal{N}(0, s_i^2) \implies w_i^* = \frac{1}{s_i^2 + \hat{\tau}^2}, \quad \hat{\mu}_{\text{MEMA}} = \frac{\sum_{i=1}^{N} w_i^* \hat{c}_i}{\sum_{i=1}^{N} w_i^*}",
            "summary": "Combines each participant's within-subject contrast variance s_i^2 with the between-participant biological variance tau^2 to form precision-weighted population inference.",
            "terms": [
                {"term": r"s_i^2 = \operatorname{Var}(\varepsilon_i)", "role": "Level-1 Within-Participant Variance", "meaning": "Estimation uncertainty of participant i's contrast from their run-level time series (higher if participant i had fewer clean TRs or higher noise).", "failure": "Ignoring dramatic differences in retained scan time across participants in clinical or pediatric cohorts."},
                {"term": r"\tau^2 = \operatorname{Var}(b_i)", "role": "Level-2 Between-Participant Variance", "meaning": "True population heterogeneity of brain responses across different humans; sets the irreducible variance floor as run length grows.", "failure": "Using Fixed-Effects (setting tau^2 = 0) or pooling runs as independent rows (pseudoreplication), inflating df from N-1 to N*m-1."},
                {"term": r"w_i^* = (s_i^2 + \hat{\tau}^2)^{-1}", "role": "Inverse Total Variance Weight", "meaning": "Optimal mixed-effects weight balancing within-subject measurement precision against between-subject population variance.", "failure": "Allowing one noisy outlier scan to dominate an unweighted OLS group average."}
            ]
        }
    },
    "D12": {
        "commons_file": "File:Permutation_test_example_animation.gif",
        "diagram_title": "Nonparametric Permutation Inference, Sign-Flipping & Exchangeability Block Constraints",
        "diagram_guide": "Permutation tests construct the exact empirical null distribution from the data without assuming Gaussian tails (Eklund et al., 2016)—provided the permutations respect the experimental exchangeability structure (e.g., permuting only within scanner sites or within twin/family blocks, never across repeated measures of different people).",
        "pipeline_steps": ["State Null Hypothesis & Exchangeability Blocks", "Generate B Valid Permutations / Sign-Flips", "Include Identity Permutation (+1 Rule)", "Compute Empirical p = (1 + #{T_b >= T_obs}) / (B + 1)", "Verify Monte Carlo Resolution 1/(B+1)"],
        "equation": {
            "name": "Exact Phipson-Smyth Permutation p-Value & Freedman-Lane Nuisance Permutation",
            "latex": r"p_{\text{perm}} = \frac{1 + \sum_{b=1}^{B} \mathbb{I}\!\left(|T(\pi_b \mathbf{y})| \ge |T_{\text{obs}}|\right)}{1 + B}, \qquad \mathbf{y}_b^* = \hat{\boldsymbol{\gamma}}_{\text{nuis}}^T Z + \Pi_b \, R_Z\,\mathbf{y} \quad \text{(Freedman-Lane)}",
            "summary": "Computes a strictly positive nonparametric p-value by counting permutations exceeding the observed statistic while preserving nuisance covariates via Freedman-Lane residual permutation.",
            "terms": [
                {"term": r"\frac{1 + \#\{\cdot\}}{1 + B}", "role": "Plus-One Exactness Rule (Phipson & Smyth)", "meaning": "Includes the observed unpermuted data as one valid configuration under H0 so p_perm is never 0.0 and Type I error is exact.", "failure": "Computing #{T_b >= T_obs}/B without +1, returning impossible p = 0.0 and anticonservative FDR thresholds."},
                {"term": r"\pi_b \in \mathcal{G}_{\text{block}}", "role": "Exchangeability-Preserving Group Action", "meaning": "Restricts label shuffles or sign flips to exchangeable units (e.g., within-site strata, within-subject paired swaps, or twin blocks).", "failure": "Permuting freely across multi-site cohorts where site sample sizes and group ratios differ, turning site effects into false group hits."},
                {"term": r"\Pi_b \, R_Z\,\mathbf{y}", "role": "Freedman-Lane Residual Permutation", "meaning": "Permutes residuals orthogonal to nuisance covariates Z before re-fitting the full model [X, Z].", "failure": "Permuting raw Y labels while holding nuisance covariates Z fixed when X and Z are correlated."}
            ]
        }
    },
    "D13": {
        "commons_file": "File:Benjamini-Hochberg-correction.png",
        "diagram_title": "Multiple Comparisons Across Voxels: FWER (Max-T), Benjamini-Hochberg FDR & TFCE",
        "diagram_guide": "Testing 100,000 brain voxels at uncorrected p < 0.05 produces ~5,000 false-positive voxels under a global null. Parametric cluster-extent RFT failed in Eklund et al. (2016) because real fMRI spatial autocorrelation has heavy non-Gaussian tails; nonparametric max-stat permutation with Threshold-Free Cluster Enhancement (TFCE) controls FWER without an arbitrary cluster-forming threshold.",
        "pipeline_steps": ["Define Family of M Voxel/Edge Tests", "Compare FWER (Max-T) vs. BH-FDR (q <= 0.05)", "Compute TFCE Score Across All Thresholds h", "Build Empirical Max-TFCE Null Distribution", "Report Complete Unthresholded + Thresholded Maps"],
        "equation": {
            "name": "Threshold-Free Cluster Enhancement (TFCE; Smith & Nichols, 2009) & Max-Stat FWER",
            "latex": r"\text{TFCE}(v) = \int_{h_0}^{h_v} \underbrace{e(h)^E}_{\text{Cluster Extent}} \cdot \underbrace{h^H}_{\text{Height}} \, dh \quad (E=0.5, H=2.0), \qquad p_{\text{FWER}}(v) = \frac{1 + \sum_{b=1}^{B} \mathbb{I}\!\left(\max_{u} \text{TFCE}_b(u) \ge \text{TFCE}_{\text{obs}}(v)\right)}{1 + B}",
            "summary": "Integrates cluster spatial extent e(h)^E weighted by statistical height h^H across all possible thresholds h, then controls Family-Wise Error Rate via the permutation distribution of the brain-wide maximum.",
            "terms": [
                {"term": r"e(h)^E \cdot h^H \, dh", "role": "Multi-Threshold Extent-by-Height Integrand", "meaning": "Combines local cluster size e(h) at threshold h (raised to E=0.5) with threshold height h (raised to H=2.0), eliminating the arbitrary p<0.001 cluster-forming threshold.", "failure": "Using parametric Gaussian Random Field cluster inference with a liberal p<0.01 primary threshold, which yields up to 70% false-positive brain maps (Eklund et al., 2016)."},
                {"term": r"\max_{u \in \Omega} \text{TFCE}_b(u)", "role": "Whole-Brain Maximum Null Statistic", "meaning": "Recording the single largest statistic across the entire brain on each permutation b automatically adapts to spatial smoothness and controls FWER across all voxels.", "failure": "Comparing voxel v only against its own local permutation distribution, which yields an uncorrected p-value."},
                {"term": r"\text{Spatial Specificity Caveat}", "role": "Cluster-Level vs. Voxel-Level Claim", "meaning": "A significant cluster or TFCE peak certifies that signal exists somewhere in the connected support region, not that every boundary voxel in the blob is truly active.", "failure": "Making precise anatomical sub-nuclear claims from the outer edge of a smoothed, cluster-enhanced blob."}
            ]
        }
    },
    "D14": {
        "commons_file": "File:Selection_Bias_-_Large_Net_Holes.jpg",
        "diagram_title": "Circular Analysis ('Double Dipping'), Selection-Conditional Winner's Curse & Independent ROI Splits",
        "diagram_guide": "Selecting the 'top voxels' or 'peak ROI' using a contrast across all participants and then plotting or testing the same contrast (or a non-orthogonal correlate) in that ROI on the same data is circular ('double dipping'; Vul et al., 2009; Kriegeskorte et al., 2009). Even in pure white noise, selecting voxels where T > 3 guarantees a highly 'significant' secondary test!",
        "pipeline_steps": ["Audit ROI Selection vs. Evaluation Dependency", "Demonstrate Null Inflation Under Peak Picking", "Check Contrast Orthogonality c_sel^T (X^T X)^{-1} c_eval", "Implement Leave-One-Subject-Out / Split-Half ROI", "Verify Zero Effect Under Full-Pipeline Null"],
        "equation": {
            "name": "Selection-Conditional Expectation Bias & Design-Weighted Contrast Orthogonality",
            "latex": r"\mathbb{E}\!\left[T_v \;\middle|\; T_v > \tau_{\text{sel}}, \, H_0\right] = \frac{\phi(\tau_{\text{sel}})}{1 - \Phi(\tau_{\text{sel}})} > 0, \qquad \operatorname{Cov}\!\left(\mathbf{c}_{\text{sel}}^T\hat{\boldsymbol{\beta}}, \, \mathbf{c}_{\text{eval}}^T\hat{\boldsymbol{\beta}}\right) = \sigma^2\,\mathbf{c}_{\text{sel}}^T (X^T V^{-1} X)^{-1} \mathbf{c}_{\text{eval}} = 0",
            "summary": "Proves why thresholding on T_v > tau shifts the null expectation to the inverse Mills ratio and states the exact covariance condition for independent contrast selection.",
            "terms": [
                {"term": r"\frac{\phi(\tau_{\text{sel}})}{1 - \Phi(\tau_{\text{sel}})}", "role": "Inverse Mills Ratio Truncation Bias", "meaning": "Expected z-score of a pure noise voxel given that it survived selection threshold tau_sel (e.g., E[Z | Z > 3.0] = +3.28 under pure noise!).", "failure": "Selecting a peak cluster at p<0.001 and then running a secondary t-test or brain-behavior correlation on the same subjects inside that cluster."},
                {"term": r"\mathbf{c}_{\text{sel}}^T (X^T V^{-1} X)^{-1} \mathbf{c}_{\text{eval}} = 0", "role": "Design-Weighted Contrast Orthogonality", "meaning": "Two contrasts on the same dataset are statistically independent only if their covariance through (X^T V^{-1} X)^{-1} is zero (AND sample variance selection bias is avoided).", "failure": "Checking only Euclidean dot product c_sel^T c_eval == 0 when the design columns in X are correlated."},
                {"term": r"\hat{\Omega}_{\text{ROI}}^{(-i)} = \operatorname{select}(\mathcal{D}_{-i})", "role": "Out-of-Fold / Functional Localizer Isolation", "meaning": "Defines participant i's ROI using an anatomical atlas, an independent functional localizer run, or the remaining N-1 participants.", "failure": "Re-using test participants during feature/ROI screening."}
            ]
        }
    },
    "D15": {
        "commons_file": "File:Equivalence_Test.png",
        "diagram_title": "Absence of Evidence vs. Evidence of Absence: TOST Equivalence, ROPE & Bayesian Shrinkage",
        "diagram_guide": "A non-significant p = 0.24 in a small sample does NOT prove the effect is zero—the confidence interval may still span huge biological effects. Proving practical equivalence requires Two One-Sided Tests (TOST) or a Bayesian Region of Practical Equivalence (ROPE) showing the entire interval falls inside [-Delta, +Delta].",
        "pipeline_steps": ["Pre-Specify Smallest Effect Size of Interest Delta", "Run Two One-Sided Tests (t_lower, t_upper)", "Check 90% CI Subset of [-Delta, +Delta]", "Compute Conjugate Bayesian Posterior & Shrinkage", "Evaluate Posterior Mass Inside ROPE"],
        "equation": {
            "name": "TOST Equivalence Test & Normal-Normal Bayesian Posterior Shrinkage",
            "latex": r"t_{\text{L}} = \frac{\hat{\theta} - (-\Delta)}{\text{SE}(\hat{\theta})} > t_{1-\alpha, \nu} \;\wedge\; t_{\text{U}} = \frac{\Delta - \hat{\theta}}{\text{SE}(\hat{\theta})} > t_{1-\alpha, \nu}, \qquad \mu_{\text{post}} = \underbrace{\frac{\tau_0^2}{\tau_0^2 + \text{SE}^2}}_{\text{Shrinkage } \lambda} \hat{\theta} + (1 - \lambda)\mu_0",
            "summary": "Certifies practical equivalence when both one-sided bounds reject effects outside [-Delta, +Delta], and shrinks noisy estimates toward a prior mean mu_0 inversely to their standard error.",
            "terms": [
                {"term": r"[-\Delta, +\Delta] \text{ (SESOI / ROPE)}", "role": "Smallest Effect Size of Interest", "meaning": "Scientifically pre-specifiedequivalence margin below which any brain difference is too small to matter biologically or clinically.", "failure": "Claiming 'Region X showed no effect (p = 0.18)' when the 95% CI spans [-0.45, +0.85]."},
                {"term": r"t_{\text{L}} > t_{1-\alpha,\nu} \wedge t_{\text{U}} > t_{1-\alpha,\nu}", "role": "Dual One-Sided Equivalence Gate", "meaning": "Rejects both theta <= -Delta and theta >= +Delta at level alpha, equivalent to the (1 - 2*alpha) = 90% CI lying strictly inside (-Delta, +Delta).", "failure": "Confusing an inconclusive wide confidence interval with a confirmed null effect."},
                {"term": r"\lambda = \frac{\tau_0^2}{\tau_0^2 + \text{SE}^2}", "role": "Precision-Weighted Bayesian Shrinkage Factor", "meaning": "Pulls high-variance small-sample estimates (large SE^2) strongly toward the prior mean mu_0, mitigating Winner's Curse exaggeration.", "failure": "Using an uncalibrated flat prior and claiming a Bayes Factor proves the null without checking prior scale sensitivity."}
            ]
        }
    },
    "D16": {
        "commons_file": "File:Generic_forest_plot.png",
        "diagram_title": "Multiverse Analysis, Specification Curves & Preregistration Before Viewing Results",
        "diagram_guide": "When multiple preprocessing and modeling choices are scientifically defensible, running all valid combinations (a multiverse / specification curve analysis) reveals whether a neuroimaging conclusion is invariant across choices or fragile to a single threshold or nuisance setting.",
        "pipeline_steps": ["Enumerate Valid Analytical Branches Pi", "Exclude Scientifically Invalid / Leaky Paths", "Execute Full Multiverse Grid", "Plot Ordered Specification Curve + Indicators", "Run Joint Permutation Across All Branches"],
        "equation": {
            "name": "Multiverse Specification Curve & Vibration of Effects Ratio",
            "latex": r"\mathcal{M} = \big\{\hat{\theta}(\pi), \, p(\pi) \;\big|\; \pi \in \Pi_{\text{valid}} = \Pi_{\text{FWHM}} \times \Pi_{\text{motion}} \times \Pi_{\text{HRF}} \times \Pi_{\text{thresh}}\big\}, \qquad \text{Share}_{\text{robust}} = \frac{1}{|\Pi_{\text{valid}}|}\sum_{\pi \in \Pi_{\text{valid}}} \mathbb{I}\!\left(\hat{\theta}(\pi) > 0 \wedge p(\pi) < \alpha\right)",
            "summary": "Evaluates the target estimand across the Cartesian product of scientifically justifiable analytical branches rather than reporting a single post-hoc path.",
            "terms": [
                {"term": r"\Pi_{\text{valid}}", "role": "Defensible Analytical Specification Space", "meaning": "Cartesian product of reasonable, non-leaky choices (e.g., 4 mm vs 8 mm FWHM; 6 vs 24 motion params; canonical vs derivative HRF).", "failure": "Including broken or leaky pipelines in the multiverse to artificially dilute or inflate the specification curve."},
                {"term": r"\hat{\theta}(\pi)", "role": "Branch-Conditional Effect Estimate", "meaning": "Estimated effect size under pipeline specification pi, sorted from smallest to largest to form the specification curve.", "failure": "Exploring 18 pipeline variations privately and publishing only the single branch with the smallest p-value ('garden of forking paths')."},
                {"term": r"\text{Share}_{\text{robust}}", "role": "Cross-Pipeline Concordance Metric", "meaning": "Fraction of valid analytical branches that agree in sign and statistical support, tested against a joint permutation null across the entire grid.", "failure": "Treating branches as independent replications rather than correlated views of the same underlying dataset."}
            ]
        }
    },
}
