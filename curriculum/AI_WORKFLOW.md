# Agentic AI Workflow: Delegate the Grunt Work, Supervise the Science

The core skill of this course is **using an agentic AI setup on your MacBook Pro (Goose + Ollama running the latest Qwen and Gemma 4 models) to execute class deliverables efficiently—while being able to spot what is wrong immediately, trace errors back to their root cause and fix them, and understand why every outcome looks the way it does.**

Complete **[Step 0 in the macOS Setup Guide](SETUP.md)** first so that **Ollama** (`qwen3.5:9b` + `gemma4:e4b` on a standard 16–24 GB MacBook Pro, or `qwen3.6:27b` + `gemma4:26b` on a 32 GB+ MacBook Pro) and **Goose** (`goose session`) are ready alongside JupyterLab.

---

## How to pair Qwen and Gemma 4 on your MacBook Pro

1. **Qwen (`qwen3.5:9b` / `qwen3.6:27b`) inside Goose — The Implementation Workhorse:**
   Use Qwen inside Goose to handle the coding grunt work: slicing 4D NIfTI tensors, assembling GLM design matrices, running cross-validation loops, and drafting multi-panel `matplotlib` diagnostic figures.
2. **Gemma 4 (`gemma4:e4b` / `gemma4:26b`) — The Scientific Auditor:**
   Use Gemma 4 (either by switching models in Goose or running `ollama run gemma4:e4b` in a companion Terminal tab) to audit transformation contracts, check paper figure claims against supplied text, and verify whether Qwen's implementation quietly violated a physical or statistical assumption.
3. **Python (`numpy`, `scipy`, `nibabel`, `nilearn`, `scikit-learn`) — The Numerical Ground Truth:**
   Neither LLM executes math in its head. All numerical outputs come from the locked Python 3.12 environment on your MacBook Pro.

---

## The Three Pillars of Agentic Deliverable Supervision

Every computational lesson (`F01`–`P04`), reading seminar (`R00`–`R03`), and paper assignment (`A1`–`A4`) is structured around three practical pillars that train you to supervise AI like a principal investigator:

### Pillar 1 · Suggestive Prompts (*"In the Spirit Of," Not a Rigid Script*)
You do not need to paste a rigid, word-for-word incantation—and you should never ask an AI *"Do Homework PR02 for me."* Instead, each lesson gives you a **Suggestive Prompt** showing the *spirit* of how to brief Goose/Ollama on a task:
- **State the scientific goal and input/output contract:** Name the input array/image, physical units (`mm`, `s`, `Hz`, `% BOLD`), target axes, and coordinate frame (`RAS+`).
- **Delegate the implementation grunt work:** Let Goose write the loop, matrix algebra, or `matplotlib` boilerplate.
- **Demand built-in verification:** Always ask the agent to print or plot the specific invariant that proves the transformation worked—and to contrast the valid implementation against the lesson's common failure mode.

### Pillar 2 · What to Look For & How to Trace Errors Back to the Root Cause
When AI-generated neuroimaging code goes wrong, **it almost never crashes with a Python `SyntaxError` or `TypeError`**. Instead, it runs cleanly, produces a plausible-looking brain map or $R^2$ score, and silently corrupts the science. In every lesson, we train you to:
1. **Spot the Immediate Red Flag (Symptom):** Recognize the telltale visual or numerical signature right away in the plot or summary table (e.g., an eroded cortical rim after resampling a mask; a $42\text{ mm}$ left–right lesion jump; a suspiciously high $R^2 \approx 0.85$ on pure noise; a variance inflation factor $\text{VIF} > 50$ on an interaction column; temporal ringing in scrubbed frames).
2. **Trace the Error Back Down (Root-Cause Isolation):** Follow a deterministic 3-step traceback instead of guessing or asking the AI to "try again":
   - *Step A — Check the Boundary Invariant:* Compare the output's shape, physical affine determinant $|\det(\mathbf{M})|$, row/column means, or train/test index intersection against the input contract.
   - *Step B — Locate the First Divergent Tensor:* Print the intermediate array immediately before and after the suspect operation (`resample_img`, `reshape`, `butter`, `StandardScaler`, `KFold`).
   - *Step C — Pinpoint the Exact Bug:* Identify the exact parameter or ordering mistake (e.g., `interpolation='continuous'` instead of `'nearest'` on integer labels; `.reshape(V, T)` instead of `.T`; filtering before censoring; fitting `SelectKBest` or `ComBat` before splitting participants).
3. **Apply the Minimal Fix:** Repair the exact line or parameter that broke the contract—never delete or weaken an `assert` statement to hide the symptom.

### Pillar 3 · Expected Outcome Ranges & Why It Must Look That Way
A single point number (`r = 0.6142`) is brittle across random seeds, datasets, or floating-point reduction orders (`Apple Accelerate` on macOS `arm64` vs. `OpenBLAS`), and memorizing a magic number teaches nothing. Instead, every lesson specifies:
- **The Expected Valid Outcome Range:** The plausible numerical interval or structural pattern your deliverable should produce when implemented correctly (e.g., total physical brain volume conserved within $\pm 0.5\%$ after $2\text{ mm} \to 4\text{ mm}$ resampling; null permutation false-positive rate in $[0.03, 0.07]$ at $\alpha = 0.05$; Haufe pattern recovery correlation $r \in [0.95, 1.00]$ on suppressor channels).
- **The Broken Baseline Range:** What numerical range you will see if the AI committed the lesson's classic error (e.g., $5\text{–}10\%$ volume loss under linear mask truncation; $30\text{–}70\%$ false-positive clusters at $p < 0.01$ under underestimated spatial smoothness; negative held-out $R^2 < 0$ when event rows are scrambled).
- **Why It Must Look That Way (First-Principles Mechanism):** The mathematical, physical, or statistical reason *why* the outcome is constrained to that range—so you understand the outcome deeply and can defend it in an oral review without looking at the AI's text.

---

## Start with the scientific problem

Begin with [Step 0](SETUP.md), then open [R00](../notebooks/00_paper_orientation/00_how_to_read.ipynb) and the six opening papers in the [reading list](papers/README.md). The first two weeks of the [26-week plan](STUDY_PLAN.md) ask why the research matters, what a selected figure shows, and what you want to understand next. Use the [reading method](papers/READING_METHOD.md), then save an [evidence ledger](coursework/EVIDENCE_LEDGER.md) for each paper and a [SOTA audit](coursework/SOTA_AUDIT.md) for a modern-method comparison.

When using Goose/Ollama (`gemma4:e4b` or `qwen3.5:9b`) during paper reading, use a prompt in the spirit of this reading contract:

> Work from the specific paper version and text I provide or you can actually access. First ask me what problem it addresses and wait. Help me locate one figure or named section; separate its observation unit, comparison, result, and uncertainty. Cite locations for source claims. Explain unfamiliar terms in plain language, without requiring equations yet. Mark inaccessible methods, unverified claims, and unanswered questions explicitly. Do not invent a figure, sample size, benchmark, or access to the full paper. Keep the instructor notes hidden until I attempt the questions. Ask me to state a limited claim in my own words.

Later blocks follow **paper question → fundamentals → agent-assisted mechanism experiment → error trace & range verification → return to the paper**.

---

## The computational class cycle (with Goose + Ollama on macOS)

1. **Predict:** Look at the input tensor/table, name its axes and physical units, and predict the expected outcome range before running code.
2. **Prompt (in the spirit of):** Use the lesson's **Suggestive Prompt** to ask Goose (`qwen3.5:9b` / `qwen3.6:27b`) to implement or extend the transformation and its diagnostic check.
3. **Spot & Trace:** Inspect the numerical table and multi-panel plot against the lesson's **What to Look For & Error Traceback** guide. Spot the deliberate failure mode immediately and trace it back to the exact line/axis/unit/split.
4. **Verify the Range & Why:** Confirm that the repaired output falls inside the **Expected Outcome Range** and state in your own words *why* the mathematics or physics forces it into that range.
5. **Defend & Return:** Close the Goose terminal, explain the result aloud, and record how this mechanism refines your interpretation of the motivating paper in your [evidence ledger](coursework/EVIDENCE_LEDGER.md).

---

## Quick Diagnostic Lookup: Common AI Mistakes & How to Trace Them

| Neuroimaging Task | Classic Silent AI Bug | Immediate Red Flag to Spot | Root-Cause Traceback & Fix |
| :--- | :--- | :--- | :--- |
| **NIfTI Geometry & Resampling (`PR01`–`PR03`, `P01`)** | Saving processed array with `np.eye(4)` or using `interpolation='continuous'` on a binary/atlas mask | Coordinates shift by $20\text{–}100+\text{ mm}$; integer labels contain fractional values (`0.12, 0.87`) and lose $5\text{–}15\%$ perimeter volume | Check `nib.aff2axcodes(img.affine)`, `np.linalg.det(img.affine[:3,:3])`, and `np.unique(mask_data)`. Preserve `img.affine` or use `interpolation='nearest'` on masks. |
| **4D Array Reshaping & Demeaning (`F01`, `DS01`)** | Calling `X_time_vox.reshape(V, T)` instead of `.T`, or demeaning along `axis=0` instead of `axis=-1` | Grand mean `output.mean()` is still `0.0`, but temporal autocorrelation drops to $\approx 0$ or static tissue contrast remains in per-voxel means | Check `output.mean(axis=-1)` (must be $\approx 0$ for every voxel) and round-trip `unmask(mask(Y)) == Y`. Use `.T` for transpose and `keepdims=True` on the time axis. |
| **Temporal Filtering & Scrubbing (`PR10`, `PR13`–`PR15`)** | Band-pass filtering the full time series *before* censoring high-motion (`FD > 0.2 mm`) frames, or passing `TR` in ms instead of s | High-amplitude motion spike rings across $\pm 3\text{–}5$ adjacent "clean" TRs; or `ValueError` / wrong cutoff frequency $f_c$ | Plot time series before/after filter around spike indices $t_0 \pm 4$; check Nyquist $f_N = 1/(2\cdot\text{TR}_{\text{sec}})$. Interpolate or orthogonalize censored frames *before* filtering (`Lindquist et al., 2019`). |
| **GLM Design & Contrasts (`D05`–`D10`, `P02`)** | Uncentered interaction terms ($A \times B$), sum-nonzero difference contrasts (`[1, 1, -1]`), or ignoring AR(1) autocorrelation | Main-effect $\text{VIF} > 10\text{–}60$; baseline intercept leaks into task contrast; false-positive rate $> 15\%$ at nominal $\alpha = 0.05$ | Check `np.sum(c) == 0` for difference contrasts, center covariates before multiplying, and inspect residual lag-1 autocorrelation $\hat{\rho}_1$ before trusting OLS standard errors. |
| **Cross-Validation & Harmonization (`DS05`, `DS15`, `M04`, `P03`)** | Row-wise `KFold` when subjects have multiple runs/slices, or fitting `SelectKBest` / `StandardScaler` / `ComBat` on the full dataset before splitting | Held-out accuracy or $R^2$ is $0.65\text{–}0.90$ even when target labels $y$ are randomly permuted! | Check `set(groups[train]) & set(groups[test]) == set()` and run a **label-permutation null test** (must average $R^2 \le 0$ / accuracy $\approx 50\%$). Wrap all preprocessing inside `sklearn.pipeline.Pipeline` with `GroupKFold`. |

---

## Session record & academic integrity

Save the notebook ID, date, macOS model tag used (`qwen3.5:9b`, `qwen3.6:27b`, `gemma4:e4b`, or `gemma4:26b`), your initial prediction, the suggestive prompt you used, the error you spotted and traced back, the observed outcome versus the expected range, and your own explanation. For real participant data, always use your institution's approved environment; the synthetic phantoms and public teaching datasets in this repository let you practice the full agentic workflow safely on your MacBook Pro.
