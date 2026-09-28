#!/usr/bin/env python3
"""Decompose any LaTeX display equation ($$ ... $$) into its logical terms and explain what each part does."""
import html
import re

# Domain-aware neuroimaging, physics, statistics, and ML mathematical term dictionary.
# Each entry: (regex_pattern, default_symbol_tex, use_matched_tex, role_badge, explanation)
SYMBOL_ONTOLOGY = [
    (r"\\text\{TR\}|\bTR\b", r"\text{TR}", False, "Repetition Time (Sampling Period)", "Time interval between successive RF excitation pulses on the same slice; governs longitudinal T1 recovery and sets the Nyquist temporal sampling limit 1/(2*TR)."),
    (r"\\text\{TE\}|\bTE\b", r"\text{TE}", False, "Echo Time (T2 / T2* Decay Window)", "Delay between RF excitation and k-space echo readout; controls how long transverse spin coherence decays via T2 or T2* (BOLD sensitivity)."),
    (r"T_2\^\*", r"T_2^*", False, "Effective Transverse Relaxation Time", "Combined spin-spin + magnetic field inhomogeneity decay constant sensitive to paramagnetic deoxyhemoglobin (dHb)."),
    (r"\bT_1\b", r"T_1", False, "Longitudinal (Spin-Lattice) Relaxation Time", "Time constant for protons to exchange thermal energy with the surrounding macromolecular/myelin lattice and recover along B0."),
    (r"\bT_2\b(?!\^\*)", r"T_2", False, "Irreversible Transverse (Spin-Spin) Relaxation", "True spin-spin phase coherence decay time constant after 180-degree spin-echo refocusing."),
    (r"\bM_0\b|\bS_0\b", None, True, "Equilibrium / Baseline Signal (M0 / S0)", "Maximum available longitudinal magnetization or unattenuated baseline signal (b=0 or TE=0) prior to relaxation or diffusion weighting."),
    (r"\\Delta B_0|B_0", r"B_0, \; \Delta B_0", False, "Static Magnetic Field & Off-Resonance Inhomogeneity", "Main scanner field (e.g., 3T) and local susceptibility field perturbations near air-tissue sinuses or venous deoxyhemoglobin."),
    (r"\\theta_E|\b\\theta\b", r"\theta", False, "RF Excitation Flip Angle / Model Parameter", "Angle by which longitudinal magnetization M_z is tipped into the transverse receiver plane (or parameter vector in statistical models)."),
    (r"h\(\\tau\)|h\(t\)|\\text\{HRF\}", r"h(\tau)", False, "Hemodynamic Response Function (HRF)", "Sluggish neurovascular impulse response (~5-6 s peak, ~16 s undershoot) acting as a biological low-pass filter (<0.18 Hz) on neural activity."),
    (r"\\mathbf\{x\}_\{\\text\{ras\}\}|\\mathbf\{x\}_\{\\text\{world\}\}", r"\mathbf{x}_{\text{ras}}", False, "Physical World Coordinate (mm, RAS+)", "Continuous millimeter coordinate (Right+, Anterior+, Superior+) in scanner/template space."),
    (r"\\mathbf\{i\}_\{\\text\{ijk\}\}", r"\mathbf{i}_{\text{ijk}}", False, "Discrete Voxel Array Index", "Zero-based integer grid subscript (i, j, k) indexing the 3D NIfTI storage array."),
    (r"\\det\(M\)|\\det\(R\)|\\det\(A\)", r"\det(M) = \pm(\Delta i\,\Delta j\,\Delta k)", False, "Affine Determinant (Voxel Volume & Handedness)", "Magnitude |det(M)| gives physical voxel volume in mm^3; sign(det(M)) encodes coordinate handedness (+1 right-handed RAS+, -1 left-handed LAS)."),
    (r"\\det\(\\nabla|J\(\\mathbf\{x\}\)|J\(x,\s*y\)", r"J(\mathbf{x}) = \det(\nabla\boldsymbol{\phi})", False, "Deformation Jacobian Determinant (Volume Scaling)", "Ratio of deformed elemental volume to initial volume; J=1 preserves volume, J>1 expands, 0<J<1 compresses, and J<=0 warns of topological grid folding."),
    (r"\\boldsymbol\{\\phi\}|\\mathbf\{u\}\(\\mathbf\{x\}\)", r"\boldsymbol{\phi}(\mathbf{x}) = \mathbf{x} + \mathbf{u}(\mathbf{x})", False, "Nonlinear Deformation / Displacement Field", "Maps each template coordinate x to its corresponding native anatomical location via displacement vector u(x)."),
    (r"B\(\\mathbf\{x\}\)|\\hat\{B\}", r"B(\mathbf{x})", False, "Multiplicative RF Coil Bias Field", "Smooth spatial intensity shading caused by receiver coil sensitivity profiles and B1+ inhomogeneity."),
    (r"\\text\{DSC\}|\\text\{SoftDice\}|\\text\{Dice\}", r"\text{DSC}", False, "Sørensen–Dice Overlap Coefficient", "Harmonic mean of sensitivity and precision (2|A cap B| / (|A| + |B|)), invariant to vast true-negative background regions."),
    (r"\\text\{HD\}|\\text\{ASSD\}", r"\text{HD}, \; \text{ASSD}", False, "Surface Boundary Distance Metric (mm)", "Measures worst-case (Hausdorff) or average symmetric millimeter excursion between predicted and reference anatomical boundaries."),
    (r"\\gamma_\{ic\}|p_\{ic\}|\\pi_c", r"\gamma_{ic}, \; \pi_c", False, "Tissue Class Prior & Posterior Responsibility", "Continuous partial-volume probability that voxel i belongs to tissue class c (CSF, GM, or WM) given its intensity and spatial prior."),
    (r"\\text\{TIV\}|\\overline\{\\text\{TIV\}\}", r"\text{TIV}_i - \overline{\text{TIV}}", False, "Total Intracranial Volume Covariate", "Global head-size scaling covariate centered and regressed out of regional morphometry before testing group atrophy."),
    (r"\\text\{FD\}_t|\\text\{DVARS\}_t", r"\text{FD}_t, \; \text{DVARS}_t", False, "Framewise Motion & Intensity Spike Metrics", "Quantifies frame-to-frame head movement in millimeters (FD, using a 50 mm cortical radius for rotations) and RMS signal change (DVARS)."),
    (r"\\text\{FWHM\}", r"\text{FWHM}", False, "Full Width at Half Maximum (Spatial Scale)", "Spatial smoothing kernel width in millimeters; related to Gaussian standard deviation by sigma = FWHM / sqrt(8 ln 2) approx FWHM / 2.3548."),
    (r"f_\{\\text\{Nyquist\}\}|f_\{\\text\{alias\}\}", r"f_{\text{Nyquist}} = \frac{1}{2\,\text{TR}}", False, "Nyquist Folding Frequency", "Highest temporal frequency resolvable without aliasing at sampling interval TR."),
    (r"P_N\^\{\\perp\}|P_\{\\mathcal\{C\}\(X\)\}|X X\^\+", r"P_X, \; P_N^\perp", False, "Orthogonal Subspace Projection Matrix", "Idempotent linear operator projecting time series onto (or orthogonal to) the column space spanned by design/nuisance regressors."),
    (r"b_k|\\text\{ADC\}", r"b_k \cdot \text{ADC}(\mathbf{g}_k)", False, "Diffusion Weighting & Apparent Diffusivity", "Stejskal-Tanner b-value (s/mm^2) multiplied by directional water diffusivity along unit gradient vector g_k."),
    (r"\\text\{FA\}|\\text\{MD\}|\\lambda_1", r"\lambda_1, \lambda_2, \lambda_3 \to \text{FA}, \text{MD}", False, "Diffusion Tensor Eigenvalues & Anisotropy", "Principal diffusivities of the 3x3 tensor ellipsoid summarizing isotropic mean diffusivity (MD) and directional coherence (FA)."),
    (r"\\operatorname\{arctanh\}|z_\{pq\}", r"z_{pq} = \operatorname{arctanh}(r_{pq})", False, "Fisher r-to-z Variance Stabilization", "Transforms bounded Pearson correlations r in (-1, 1) into unbounded Gaussian-like scores with variance ~1/(T_eff - 3)."),
    (r"Y_i\(1\)\s*-\s*Y_i\(0\)|\\tau_\{\\text\{ATE\}\}", r"Y_i(1) - Y_i(0)", False, "Potential-Outcomes Causal Contrast", "Counterfactual difference between unit i's outcome under exposure A=1 vs. A=0 before choosing a statistical estimator."),
    (r"\\text\{ICC\}|\\rho_\{\\text\{ICC\}\}", r"\text{ICC}", False, "Intraclass Correlation (Reliability Ratio)", "Proportion of total variance attributable to true stable between-person differences rather than within-person scan noise."),
    (r"X\^(?:T|\\top)\s*V\^\{-1\}\s*X|\(X\^(?:T|\\top)\s*W?\s*X\)\^\{-1\}|\\left\(X\^(?:T|\\top)\s*W?\s*X\\right\)\^\{-1\}", r"(X^\top X)^{-1}", True, "Design Gram Matrix Inverse / Precision", "Inverts the design matrix cross-product (weighted by W or V^{-1} in WLS/GLS) to decorrelate collinear regressors and scale parameter variance."),
    (r"\\mathbf\{c\}\^(?:T|\\top)\s*\\hat\{\\boldsymbol\{\\beta\}\}|c\^(?:T|\\top)\\hat\{\\beta\}|\\mathbf\{c\}\^(?:T|\\top)\s*\(X\^(?:T|\\top)\s*X\)\^\{-1\}\s*\\mathbf\{c\}", r"\mathbf{c}^\top\hat{\boldsymbol{\beta}}", True, "Linear Contrast & Contrast Variance Projection", "Projects parameter estimates or inverse design covariance onto the directional scientific contrast vector c."),
    (r"\\text\{TFCE\}", r"\text{TFCE}(v)", False, "Threshold-Free Cluster Enhancement", "Integrates cluster spatial extent e(h)^E times height h^H across all thresholds h so FWER permutation avoids an arbitrary primary threshold."),
    (r"\\text\{VIF\}_j|D_i|h_\{ii\}", r"\text{VIF}_j, \; h_{ii}, \; D_i", False, "Collinearity, Leverage & Cook's Influence", "Diagnoses variance inflation from correlated predictors (VIF) and single-observation leverage/influence on the regression fit."),
    (r"U\s*\\Sigma\s*V\^(?:T|\\top)|\\sigma_k\^2", r"U \Sigma V^\top", False, "Singular Value Decomposition (SVD)", "Factorizes centered data into orthonormal sample modes U, singular values Sigma, and spatial loading basis V."),
    (r"\\Sigma_X W|\\text\{Haufe\}", r"\hat{A} = \Sigma_X W \Sigma_{\hat{Y}}^{-1}", False, "Haufe Forward Activation Transformation", "Multiplies discriminative decoding weights W by data covariance Sigma_X to eliminate noise-suppressor weights and recover true encoding patterns."),
    (r"\\gamma_\{iv\}\^\*|\\delta_\{iv\}\^\*|\\text\{ComBat\}", r"\gamma_{iv}^*, \; \delta_{iv}^*", False, "ComBat Empirical-Bayes Site Parameters", "Scanner-specific additive location shift (gamma*) and multiplicative scale factor (delta*) removed during multi-site harmonization."),
    (r"\\hat\{\\Sigma\}_V\^\{-1\}|\\hat\{d\}_\{\\text\{cross\}\}\^2", r"\hat{d}_{\text{cross}}^2", False, "Cross-Validated Mahalanobis (Crossnobis) RDM", "Noise-whitened inner product of condition differences across independent runs, yielding an unbiased zero expectation under the null."),
    (r"\\text\{ISC\}_i|W_i S", r"\text{ISC}_i, \; W_i S", False, "Inter-Subject Correlation & Shared Response", "Isolates stimulus-locked neural dynamics shared across participants watching the same naturalistic movie from idiosyncratic noise."),
    (r"D_\{\\text\{KL\}\}|\\text\{ELBO\}", r"D_{\text{KL}}\big(q(\mathbf{z}\mid\mathbf{x}) \,\|\, p(\mathbf{z})\big)", False, "Kullback-Leibler Divergence Penalty", "Information-theoretic complexity penalty measuring how far the approximate posterior q(z|x) departs from the prior p(z)."),
    (r"A_\{jk\}|\\delta_t\(k\)", r"A_{jk} = P(z_t=k \mid z_{t-1}=j)", False, "Markov State Transition Probability", "Governs the persistence (self-transition A_kk) and switching dynamics between latent brain states in an HMM."),
    (r"K_t|\\dot\{\\mathbf\{z\}\}", r"K_t, \; \dot{\mathbf{z}}(t)", False, "Latent State Derivative & Optimal Kalman Gain", "Updates latent neural state estimates by weighting measurement innovation against state vs. observation uncertainty."),
    (r"\\operatorname\{softmax\}|Q K\^(?:T|\\top)|\\sqrt\{d_k\}", r"\operatorname{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right)V", False, "Scaled Dot-Product Self-Attention", "Computes variance-stabilized query-key token compatibility weights (scaled by 1/sqrt(d_k)) to form a convex combination of Value vectors."),
    (r"\\text\{ECE\}|\\text\{Brier\}", r"\text{ECE}, \; \text{Brier}", False, "Probability Calibration & Proper Scoring Metrics", "Quantifies the discrepancy between predicted confidence probabilities and empirical outcome frequencies."),
    (r"R\s*\\mathbf\{g\}|R\s*D\s*R\^(?:T|\\top)|G\s*R\^(?:T|\\top)", r"R\mathbf{g}, \; R D R^\top", True, "SO(3) Head-Motion Rotation Operator", "Rotates diffusion B-vectors g or diffusion tensors D by the rigid-body rotation component R of the eddy/motion transform so fiber orientations align with resampled anatomy."),
    (r"\\mathcal\{F\}\s*\\\{[^}]+\\\}(?:\(\\omega\))?", r"\mathcal{F}\{\cdot\}(\omega)", True, "Fourier Domain Transform Operator", "Maps time-domain signals and impulse responses into the frequency domain omega where temporal convolution becomes pointwise multiplication."),
    (r"\\mathcal\{N\}(?:_p)?", r"\mathcal{N}(\mu, \Sigma)", False, "Gaussian Sampling / Posterior Distribution", "Specifies the normal probability law parameterized by its mean vector (first argument) and variance/covariance structure (second argument)."),
    (r"\\begin\{cases\}", r"\begin{cases} \text{branch}_1 \\ \text{branch}_2 \end{cases}", False, "Piecewise Conditional Indicator / Lag Rule", "Evaluates distinct algebraic branches depending on whether the lag index or threshold condition is satisfied."),
    (r"\\begin\{[bpvV]?matrix\}", r"\text{Structured Matrix Operator}", False, "Explicit Matrix / Toeplitz Covariance Block", "Explicit matrix representation encoding spatial affine transformation, autoregressive Toeplitz correlation, or finite-impulse lag taps."),
    (r"\\mathcal\{H\}|canonical\\_json|SHA256", r"\mathcal{H}(\operatorname{canonical\_json}(\cdot))", False, "Cryptographic Provenance Hash Function", "Computes a deterministic content-addressed digest over canonicalized node operation, parameters, and parent hashes."),
    (r"\be\(x\)", r"e(x) = P(T=1 \mid X=x)", False, "Propensity Score (Assignment Probability)", "Conditional probability of exposure/group assignment given baseline covariates X; bounded strictly in (0, 1) under positivity."),
    (r"\\sigma\^2|\\sigma_\{\\text\{SE\}\}\^2", r"\sigma^2", True, "Residual / Sampling Error Variance Scale", "Scales parameter or contrast uncertainty by the underlying observation noise variance."),
]


def is_balanced_latex(tex: str) -> bool:
    """Return True if braces, parentheses, brackets, \\left/\\right, and \\begin/\\end are balanced."""
    if not tex:
        return False
    if tex.count("{") != tex.count("}") or tex.count("(") != tex.count(")") or tex.count("[") != tex.count("]"):
        return False
    if tex.count("\\begin{") != tex.count("\\end{"):
        return False
    if len(re.findall(r"\\left(?![a-zA-Z])", tex)) != len(re.findall(r"\\right(?![a-zA-Z])", tex)):
        return False
    if "&" in tex and "\\begin{" not in tex and "\\&" not in tex:
        return False
    return True


def extract_brace_group(s: str, start_brace_idx: int):
    """Given s[start_brace_idx] == '{', return (content_inside_braces, index_after_closing_brace) or None."""
    if start_brace_idx >= len(s) or s[start_brace_idx] != "{":
        return None
    depth = 0
    for i in range(start_brace_idx, len(s)):
        if s[i] == "{" and (i == 0 or s[i - 1] != "\\"):
            depth += 1
        elif s[i] == "}" and (i == 0 or s[i - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return s[start_brace_idx + 1 : i], i + 1
    return None


def find_first_fraction(s: str):
    """Find the first \\frac{num}{den} or \\dfrac{num}{den} with full nested brace balancing."""
    for m in re.finditer(r"\\d?frac\s*\{", s):
        brace1_start = m.end() - 1
        g1 = extract_brace_group(s, brace1_start)
        if not g1:
            continue
        num, pos = g1
        while pos < len(s) and s[pos].isspace():
            pos += 1
        g2 = extract_brace_group(s, pos)
        if not g2:
            continue
        den, _ = g2
        return num.strip(), den.strip()
    return None


def split_top_level_relations(clause: str) -> list[tuple[str, str]]:
    """Split a clause by top-level relations (=, \\propto, \\approx, \\equiv, \\sim, \\ge, \\le, \\in, \\neq, <, >) at depth 0.
    Returns list of (segment_str, relation_that_preceded_it_or_empty).
    """
    depth = 0
    env_depth = 0
    left_depth = 0
    i = 0
    n = len(clause)
    relations = [
        r"\stackrel{\text{i.i.d.}}{\sim}",
        r"\leftarrow",
        r"\propto",
        r"\approx",
        r"\equiv",
        r"\sim",
        r"\neq",
        r"\ge",
        r"\le",
        r"\in",
        "=",
        "<",
        ">",
    ]
    segments = []
    last_idx = 0
    last_rel = ""
    while i < n:
        if clause.startswith(r"\begin{", i):
            env_depth += 1
        elif clause.startswith(r"\end{", i):
            env_depth = max(0, env_depth - 1)
        elif clause.startswith(r"\left", i) and (i + 5 == n or not clause[i + 5].isalpha()):
            left_depth += 1
        elif clause.startswith(r"\right", i) and (i + 6 == n or not clause[i + 6].isalpha()):
            left_depth = max(0, left_depth - 1)
        ch = clause[i]
        if ch in "{([":
            depth += 1
        elif ch in "})]":
            depth = max(0, depth - 1)
        elif depth == 0 and env_depth == 0 and left_depth == 0:
            matched_rel = None
            for rel in relations:
                if clause.startswith(rel, i):
                    if rel.startswith("\\") and i + len(rel) < n and clause[i + len(rel)].isalpha():
                        continue
                    if rel == "=" and ((i > 0 and clause[i - 1] in "<>!:") or (i + 1 < n and clause[i + 1] == "=")):
                        continue
                    matched_rel = rel
                    break
            if matched_rel:
                seg = clause[last_idx:i].strip()
                if seg:
                    segments.append((seg, last_rel))
                last_rel = matched_rel
                i += len(matched_rel)
                last_idx = i
                continue
        i += 1
    tail = clause[last_idx:].strip()
    if tail:
        segments.append((tail, last_rel))
    return segments


def split_top_level_additive(expr: str) -> list[tuple[str, str]]:
    """Split an RHS expression by top-level '+' or '-' at depth 0 into [(sign, term), ...]."""
    depth = 0
    env_depth = 0
    left_depth = 0
    i = 0
    n = len(expr)
    terms = []
    last_idx = 0
    cur_sign = "+"
    while i < n:
        if expr.startswith(r"\begin{", i):
            env_depth += 1
        elif expr.startswith(r"\end{", i):
            env_depth = max(0, env_depth - 1)
        elif expr.startswith(r"\left", i) and (i + 5 == n or not expr[i + 5].isalpha()):
            left_depth += 1
        elif expr.startswith(r"\right", i) and (i + 6 == n or not expr[i + 6].isalpha()):
            left_depth = max(0, left_depth - 1)
        ch = expr[i]
        if ch in "{([":
            depth += 1
        elif ch in "})]":
            depth = max(0, depth - 1)
        elif depth == 0 and env_depth == 0 and left_depth == 0 and ch in "+-":
            prev_nonspace = expr[:i].rstrip()
            # Ignore unary leading sign or sign after an operator like '=', '\times', '\cdot', '^', '_'
            if prev_nonspace and not prev_nonspace.endswith(("=", "^", "_", r"\times", r"\cdot", r"\pm", r"\mp")):
                seg = expr[last_idx:i].strip()
                if seg:
                    terms.append((cur_sign, seg))
                    cur_sign = ch
                    last_idx = i + 1
        i += 1
    tail = expr[last_idx:].strip()
    if tail:
        terms.append((cur_sign, tail))
    return terms


def describe_rhs_term(term_tex: str, sign: str, idx: int, total: int) -> tuple[str, str]:
    """Generate a domain-aware role badge and clear explanation for an extracted RHS sub-expression."""
    t = term_tex
    if r"\mathcal{R}" in t or r"\lambda" in t or r"\|\mathbf" in t or r"\|W" in t or r"\|\boldsymbol{\beta}" in t:
        return (
            "Regularization / Complexity Penalty",
            "Penalizes roughness, parameter magnitude, or model complexity (weighted by hyperparameter lambda) to enforce smoothness or prevent overfitting.",
        )
    if r"\mathcal{D}" in t or r"\mathcal{L}" in t or "I_{\\text{fix}}" in t or "I_{\\text{mov}}" in t:
        return (
            "Data Fidelity / Alignment Objective",
            "Measures discrepancy or statistical dependence between observed data (or fixed vs. moving images) and model predictions.",
        )
    if re.search(r"\\varepsilon|\\epsilon|\\eta|\\sigma|\\text\{Var\}|\\operatorname\{Var\}", t):
        return (
            "Variance / Noise / Error Contribution",
            "Captures measurement noise variance, biological variability, or residual uncertainty that propagates into the total signal dispersion.",
        )
    if re.search(r"e\^\{-|\\exp\s*\\?\(|\\exp\{", t):
        return (
            "Exponential Relaxation / Attenuation Factor",
            "Models continuous-time exponential signal decay (T2/T2* dephasing), longitudinal recovery (1 - exp(-TR/T1)), or Stejskal-Tanner diffusion attenuation.",
        )
    if re.search(r"\\sum|\\int", t):
        return (
            "Weighted Aggregation / Marginalization Term",
            "Sums or integrates contributions across discrete states, spatial neighbors, basis functions, or time points.",
        )
    if re.search(r"\\begin\{[bpvV]?matrix\}", t):
        return (
            "Matrix / Vector Operator Block",
            "Explicit matrix or homogeneous vector representation governing linear scaling, rotation, shear, or coordinate projection.",
        )
    if sign == "-":
        return (
            "Subtractive Offset / Baseline Adjustment",
            "Subtracts reference baseline, covariate confounding effect, or counter-directional component from the preceding term.",
        )
    if total == 1:
        return (
            "Governing Transformation Expression (RHS)",
            "Computes the target quantity from the input variables, operators, and parameters on the right-hand side.",
        )
    return (
        f"Additive Component {idx + 1} of {total}",
        "Contributes additively to the composite mathematical expression on the right-hand side.",
    )


def decompose_latex_equation(latex_str: str):
    """Break any LaTeX display equation into 3-5 clear logical parts showing what each part does."""
    s = latex_str.strip()
    parts: list[dict] = []

    def add_part(term: str, role: str, explanation: str):
        term_clean = term.strip().rstrip(",;.")
        if not term_clean or len(term_clean) > 155 or not is_balanced_latex(term_clean):
            return
        if any(p["term"] == term_clean for p in parts):
            return
        parts.append({"term": term_clean, "role": role, "explanation": explanation})

    # 0. Handle multi-stage arrow pipelines (\xrightarrow, \longrightarrow, \mapsto)
    if (r"\xrightarrow" in s or r"\longrightarrow" in s) and "=" not in s:
        stages = [st.strip() for st in re.split(r"\\xrightarrow\{[^}]*\}|\\longrightarrow", s) if st.strip()]
        for idx, st in enumerate(stages[:5]):
            add_part(
                st,
                f"Pipeline Stage {idx + 1} of {len(stages)}",
                "Sequential stage in the analytical transformation or evidence-auditing chain; any failure at this stage invalidates downstream stages.",
            )
        if len(parts) >= 2:
            return parts[:5]

    # 0b. Extract explicit \underbrace{expr}_{label} annotated terms
    if r"\underbrace{" in s:
        for ub_m in re.finditer(r"\\underbrace\s*\{", s):
            g_expr = extract_brace_group(s, ub_m.end() - 1)
            if not g_expr:
                continue
            ub_expr, pos = g_expr
            while pos < len(s) and s[pos].isspace():
                pos += 1
            if pos < len(s) and s[pos] == "_":
                pos += 1
                while pos < len(s) and s[pos].isspace():
                    pos += 1
                g_lbl = extract_brace_group(s, pos)
                if g_lbl:
                    raw_lbl = re.sub(r"\\text\s*\{([^}]*)\}", r"\1", g_lbl[0]).replace(r"\&", "&").strip()
                    add_part(
                        ub_expr,
                        raw_lbl or "Annotated Equation Block",
                        f"Explicitly annotated structural block ({raw_lbl}) within the governing equation.",
                    )

    # 1. Split across multi-equation statements (\qquad, \implies, \Longleftrightarrow, \iff)
    top_clauses = [c.strip() for c in re.split(r"\\qquad|\\implies|\\Longleftrightarrow|\\iff", s) if c.strip()]
    first_clause = top_clauses[0] if top_clauses else s

    # 2. Split first_clause by top-level relations (=, \propto, \approx, \sim, \equiv, \ge, \le, \in)
    rel_segments = split_top_level_relations(first_clause)
    op_names = {
        "=": "Exact Equality",
        r"\leftarrow": "Iterative Fixed-Point Update",
        r"\stackrel{\text{i.i.d.}}{\sim}": "i.i.d. Sampling Law",
        r"\propto": "Proportional Scaling",
        r"\approx": "First-Order / Asymptotic Approximation",
        r"\sim": "Distributional Law",
        r"\neq": "Inequality / Bias Proof",
        r"\equiv": "Definitional Identity",
        r"\ge": "Lower-Bound / Threshold Gate",
        r"\le": "Upper-Bound / Constraint Gate",
        r"\in": "Set / Space Membership",
        "<": "Strict Inequality Bound",
        ">": "Strict Inequality Bound",
    }

    if len(rel_segments) >= 2:
        lhs, _ = rel_segments[0]
        rhs, first_op = rel_segments[1]
        op_label = op_names.get(first_op, "Mathematical Relation")
        add_part(
            lhs,
            f"Target Quantity (LHS · {op_label})",
            "The output quantity, transformed signal, or statistical estimator being defined or solved for on the left-hand side.",
        )

        # If this is a chain of equalities (e.g. x_ras = [x,y,z,1]^T = A i_ijk = ...), include intermediate forms
        if len(rel_segments) >= 3:
            for mid_idx, (mid_seg, _) in enumerate(rel_segments[1:-1], start=1):
                add_part(
                    mid_seg,
                    f"Equivalent Form {mid_idx} (Chain Identity)",
                    "Intermediate algebraic or matrix-operator representation linking the left-hand target to the expanded right-hand formulation.",
                )
            rhs = rel_segments[-1][0]

        # Check for top-level fraction \frac{num}{den} inside rhs
        frac_info = find_first_fraction(rhs)
        if frac_info:
            num, den = frac_info
            add_part(
                num,
                "Numerator (Signal / Contrast / Joint Evidence)",
                "Drives the magnitude and sign of the ratio—representing the contrast effect, overlap intersection, or joint likelihood.",
            )
            add_part(
                den,
                "Denominator (Normalization / Noise Scale / Marginal)",
                "Normalizes the numerator by dispersion, standard error, total volume, or marginal probability; must be guarded against zero division.",
            )

        # Split RHS into top-level additive/subtractive components
        rhs_clean = re.sub(r"^\\(?:arg\\min|arg\\max|min|max)_\{[^}]*\}\s*\\?;?\s*", "", rhs).strip()
        add_terms = split_top_level_additive(rhs_clean)
        if len(add_terms) >= 2:
            for idx, (sgn, t_str) in enumerate(add_terms[:4]):
                display_t = f"-{t_str}" if (sgn == "-" and idx > 0) else t_str
                role, expl = describe_rhs_term(t_str, sgn, idx, len(add_terms))
                add_part(display_t, role, expl)
        elif not frac_info:
            role, expl = describe_rhs_term(rhs_clean, "+", 0, 1)
            add_part(rhs_clean, role, expl)

    # 3. Check for secondary clauses (\qquad or \implies)
    if len(top_clauses) > 1:
        for sec_idx, sec in enumerate(top_clauses[1:], start=2):
            sec_segs = split_top_level_relations(sec)
            if len(sec_segs) >= 2:
                sec_lhs = sec_segs[0][0]
                sec_rhs = sec_segs[-1][0]
                add_part(
                    f"{sec_lhs} {sec_segs[1][1]} {sec_rhs}" if len(sec) < 115 else sec_lhs,
                    "Coupled Constraint / Implied Identity",
                    "Defines the coupled consequence, auxiliary parameter, or boundary condition paired with the primary equation.",
                )
            else:
                add_part(
                    sec,
                    "Auxiliary Condition / Domain Constraint",
                    "Specifies the domain constraint or parameter condition under which the primary relation holds.",
                )

    # 4. Match domain-specific neuroimaging symbols present in this equation
    for pattern, sym_tex, use_matched, role, explanation in SYMBOL_ONTOLOGY:
        m = re.search(pattern, s)
        if m:
            term_to_show = m.group(0) if (use_matched or not sym_tex) else sym_tex
            add_part(term_to_show, role, explanation)
        if len(parts) >= 5:
            break

    # 5. Structural operator fallbacks so every equation has at least 3 informative logical rows when possible
    if r"\arg\min" in s or r"\arg\max" in s or r"\min_" in s or r"\max_" in s:
        add_part(
            r"\arg\min / \arg\max",
            "Optimization Objective Operator",
            "Searches over the feasible parameter space for the configuration that minimizes loss/energy or maximizes likelihood/similarity.",
        )
    if r"\sum" in s or r"\int" in s or r"\prod" in s:
        add_part(
            r"\sum / \prod / \int",
            "Aggregation / Factorization Operator",
            "Accumulates contributions across discrete indices (voxels, time points, participants, folds), multiplies independent factors, or integrates over continuous domains.",
        )
    if r"\mathbb{E}" in s or r"\mathbb{P}" in s:
        add_part(
            r"\mathbb{E}[\cdot], \; \mathbb{P}(\cdot)",
            "Expectation / Probability Measure",
            "Evaluates the population expectation or conditional probability law over the specified random variables and conditioning set.",
        )
    if re.search(r"\\varepsilon|\\eta\(|\+\\epsilon", s):
        add_part(
            r"\varepsilon, \; \eta, \; \epsilon",
            "Residual Noise / Numerical Regularization Term",
            "Accounts for unmodeled biological/thermal measurement error (varepsilon, eta) or adds a positive machine-precision floor (epsilon) to prevent 0/0.",
        )

    # Extract multiplicative (\cdot) factors or parenthesized arguments if still < 3 parts
    if len(parts) < 3 and r"\cdot" in s and len(rel_segments) >= 2:
        factors = [f.strip() for f in rel_segments[-1][0].split(r"\cdot") if f.strip()]
        if len(factors) >= 2:
            for f_idx, fac in enumerate(factors[:3], start=1):
                add_part(
                    fac,
                    f"Multiplicative Factor {f_idx}",
                    "Scales the product expression as an independent likelihood ratio, transfer function, or gain factor.",
                )
                if len(parts) >= 4:
                    break

    if len(parts) < 3:
        for sub_m in re.finditer(r"\\(?:exp|ln|log|det|operatorname\{[A-Za-z]+\})\s*(?:\\!\s*)?\\left\((.+?)\\right\)", s):
            inner = sub_m.group(1).strip()
            add_part(
                inner,
                "Inner Operator Argument",
                "Inner mathematical quantity passed into the outer nonlinear function, logarithm, determinant, or statistical operator.",
            )
            if len(parts) >= 3:
                break

    if not parts:
        fallback_term = first_clause if (len(first_clause) < 120 and is_balanced_latex(first_clause)) else r"\mathcal{T}(\text{Input}) \longrightarrow \text{Output}"
        parts.append({
            "term": fallback_term,
            "role": "Core Mathematical Transformation",
            "explanation": "Maps the input tensor/variables through the lesson's analytical operator to produce the verified output quantity.",
        })

    return parts[:5]


def render_equation_with_breakdown_html(latex_str: str, eq_index: int) -> str:
    """Render a display equation block plus its interactive term-by-term logic breakdown."""
    clean_tex = latex_str.strip()
    parts = decompose_latex_equation(clean_tex)
    rows_html = []
    for p in parts:
        rows_html.append(
            f'<tr>'
            f'<td class="eq-term-cell">\\({html.escape(p["term"], quote=False)}\\)</td>'
            f'<td class="eq-role-cell"><span class="eq-role-badge">{html.escape(p["role"])}</span></td>'
            f'<td class="eq-desc-cell">{html.escape(p["explanation"])}</td>'
            f'</tr>'
        )
    rows_joined = "".join(rows_html)
    term_word = "logical term" if len(parts) == 1 else "logical terms"
    return (
        f'<div class="equation-card" id="eq-block-{eq_index}">'
        f'<div class="equation-display">\\[{html.escape(clean_tex, quote=False)}\\]</div>'
        f'<details class="equation-logic-details" open>'
        f'<summary class="equation-logic-summary">'
        f'<span class="eq-logic-icon">∑</span> '
        f'<strong>Equation Logic Breakdown</strong> · Which part of this equation is doing what ({len(parts)} {term_word})'
        f'</summary>'
        f'<div class="table-scroll eq-table-wrap">'
        f'<table class="eq-breakdown-table">'
        f'<thead><tr><th>Equation Term</th><th>Logical Role</th><th>What This Part Is Doing</th></tr></thead>'
        f'<tbody>{rows_joined}</tbody>'
        f'</table>'
        f'</div>'
        f'</details>'
        f'</div>'
    )
