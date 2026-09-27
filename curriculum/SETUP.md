# Step 0 · macOS (MacBook Pro) Agentic Setup: Goose + Ollama with Qwen & Gemma

This course targets **macOS on a standard Apple Silicon MacBook Pro (`M1` / `M2` / `M3` / `M4`)**. In **Step 0**, you will configure your MacBook Pro with:
1. **[Ollama](https://ollama.com/download/mac)** serving both **Qwen** (`qwen3.5:9b` or `qwen3.6:27b`) and **Gemma 4** (`gemma4:e4b` or `gemma4:26b`) locally on Apple Silicon unified memory.
2. **[Goose](https://goose-docs.ai/docs/quickstart/)** (`goose` CLI or Goose Desktop for macOS Apple Silicon) connected to your local Ollama server and guided by the repository's [`.goosehints`](../.goosehints).
3. **Locked Python 3.12 + JupyterLab** (`./setup.sh`) so your agentic assistant and your Jupyter kernel operate on the exact same workspace.

> **Why we pull both Qwen and Gemma on your MacBook Pro:**
> - **Qwen (`qwen3.5:9b` / `qwen3.6:27b`) — Your Primary Coding & Tool Agent:** Optimized for multi-step agentic tool execution, reading repository files, writing NumPy/SciPy/NiBabel/Nilearn code, and generating multi-panel diagnostic plots inside Goose.
> - **Gemma 4 (`gemma4:e4b` / `gemma4:26b`) — Your Scientific Auditor & Second Opinion:** Optimized for analytical reasoning, reading paper figure captions, checking transformation contracts, and auditing whether a snippet written by Qwen contains a silent methodological flaw (such as an axis swap, affine reset, or cross-validation leakage).

---

## 1. Check your MacBook Pro's Unified Memory (`macOS`)

Apple Silicon MacBook Pros share unified memory between the CPU, GPU, and Neural Engine. Because you will run **macOS + JupyterLab + Ollama + Goose** simultaneously, choose the Qwen + Gemma model pair that fits comfortably inside your MacBook Pro's RAM without swapping to SSD.

Open **Terminal.app** on your MacBook Pro and check your unified memory in GB:

```zsh
sysctl -n hw.memsize | awk '{printf "MacBook Pro Unified Memory: %.0f GB\n", $1/1073741824}'
```

| MacBook Pro Unified Memory | Primary Goose Coding Agent (Qwen) | Scientific Audit & Reasoning Model (Gemma 4) | Combined Disk / Active Memory Footprint |
| :--- | :--- | :--- | :--- |
| **16 GB – 24 GB** *(Standard M1/M2/M3/M4 MacBook Pro)* | [`qwen3.5:9b`](https://ollama.com/library/qwen3.5) (`6.6 GB`, 256K context, Tools + Thinking) | [`gemma4:e4b`](https://ollama.com/library/gemma4) (`9.6 GB`, `gemma4:latest`, 128K context, Multimodal + Tools + Thinking) | One model loaded in RAM at a time (`~7–10 GB`), leaving `6–14 GB` free for macOS & JupyterLab |
| **32 GB – 36 GB+** *(M1/M2/M3/M4 Pro or Max MacBook Pro)* | [`qwen3.6:27b`](https://ollama.com/library/qwen3.6) (`18 GB`, 256K context, flagship agentic coder) | [`gemma4:26b`](https://ollama.com/library/gemma4) (`19 GB`, MoE reasoning) or [`gemma4:e4b`](https://ollama.com/library/gemma4) (`9.6 GB`) | `~18–22 GB` active when running a 26B/27B model; `qwen3.6:35b` (`23 GB`) / `gemma4:31b` (`20 GB`) for 48 GB+ Macs |
| **8 GB** *(Entry Air / older MacBook Pro fallback)* | [`qwen3.5:4b`](https://ollama.com/library/qwen3.5) (`3.4 GB`, 256K context) | [`gemma4:e2b`](https://ollama.com/library/gemma4) (`7.2 GB`, 128K context) | Lightweight fallback so Jupyter kernels never run out of memory |

---

## 2. Install Ollama and pull Qwen + Gemma on macOS

You can run `./setup.sh --setup-ai` from the repository root to automate Steps 2–4 on macOS, or run the explicit commands below in **Terminal.app**:

```zsh
# 1. Install Ollama for macOS (via Homebrew Cask or https://ollama.com/download/mac)
brew install --cask ollama
open -a Ollama

# 2. Pull the Standard MacBook Pro (16–24 GB) Qwen + Gemma pair:
ollama pull qwen3.5:9b
ollama pull gemma4:e4b

# (If sysctl reported 32 GB+ unified memory on your MacBook Pro, also pull the 27B/26B pair):
# ollama pull qwen3.6:27b
# ollama pull gemma4:26b

# 3. Verify both models are registered locally in Ollama:
ollama list
```

> **Local privacy note:** Always pull standard local weight tags (`qwen3.5:9b`, `qwen3.6:27b`, `gemma4:e4b`, `gemma4:26b`) rather than `-cloud` tags so inference stays 100% on your MacBook Pro.

---

## 3. Install and configure Goose on macOS

[Goose](https://goose-docs.ai/docs/quickstart/) connects your local Ollama models to the course repository so the agent can inspect notebooks, run verification snippets, and help you build and debug class deliverables.

```zsh
# 1. Install the Goose CLI on macOS (or install via Homebrew: brew install --cask block-goose)
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
export PATH="$HOME/.local/bin:$PATH"

# 2. Configure Goose to point to your local Ollama server
goose configure
```

When `goose configure` prompts you:
1. Choose **Configure Providers** $\to$ **Ollama**.
2. Set `OLLAMA_HOST` to `http://localhost:11434`.
3. Select your primary coding model (`qwen3.5:9b` on a 16–24 GB MacBook Pro, or `qwen3.6:27b` on a 32 GB+ MacBook Pro).
4. Enable the **Developer** extension when working on computational notebooks so Goose can read files and run small verification checks inside this repository.

To switch between your **Qwen** coding agent and your **Gemma 4** scientific auditor during a session, either run `goose configure` to switch the active model to `gemma4:e4b` (or `gemma4:26b`), or keep a second Terminal tab open with `ollama run gemma4:e4b` to cross-examine claims and equations!

---

## 4. Install the locked Python 3.12 + JupyterLab environment on macOS

From the repository root on your MacBook Pro:

```zsh
./setup.sh
uv run --frozen jupyter lab notebooks
```

- `./setup.sh` installs [`uv`](https://docs.astral.sh/uv/) if needed, creates `.venv` with Python 3.12, and syncs the exact package versions pinned in [`uv.lock`](../uv.lock) (`numpy`, `scipy`, `pandas`, `matplotlib`, `scikit-learn`, `nibabel`, `nilearn`, `jupyterlab`, `nbclient`, `ipykernel`).
- Keep **JupyterLab** running in Terminal Tab 1 (`uv run --frozen jupyter lab notebooks`) and run **Goose** in Terminal Tab 2 (`goose session`) from the repository root so `.goosehints` is automatically loaded.
- **Alternative ChatGPT route:** If you ever work away from your local Ollama setup, you can paste the [supervisory contracts](AI_WORKFLOW.md#start-with-the-scientific-problem) into ChatGPT alongside local JupyterLab on your MacBook Pro; the scientific checks, error-tracing protocol, and expected outcome ranges are identical.

---

## The tutor contract

Our [`.goosehints`](../.goosehints) file automatically loads the course supervision rules into Goose when you launch `goose session` from the repository root. If you start a fresh chat or use `ollama run` / ChatGPT directly, paste this contract at the start of a computational lesson (or use the [reading contract](AI_WORKFLOW.md#start-with-the-scientific-problem) for `R00`–`R03`):

> You are my neuroimaging pair-programming agent and scientific tutor on macOS. My goal is to use you efficiently for class deliverables—delegating coding and plotting grunt work to you while I verify the transformation contract, spot silent errors immediately, trace bugs back to their root cause, and check outcomes against expected ranges. Work on the current lesson only. Before writing code, state the input shape, output shape, axis semantics, physical units, coordinate space, fitted parameters (and which subset of data they are fitted on), preserved invariants, and destroyed information. Propose concise, readable code (10–25 lines per step) with at least one numerical `assert` check and one diagnostic plot check. Never delete or weaken an `assert` to make code pass. If an output falls outside the expected range, help me trace the error back to the exact line, axis, unit, or split where the bug entered.

---

## Ten-minute acceptance exercise

Before opening [`R00`](../notebooks/00_paper_orientation/00_how_to_read.ipynb) and [`F01`](../notebooks/00_foundations/01_learning_contract.ipynb), run this 10-minute **Step 0 Agentic Supervision Smoke Test** on your MacBook Pro to practice the exact three-part workflow used in every class deliverable:

### 1. Give Goose a Suggestive Prompt (*in the spirit of what to ask, not a rigid script*)
In your repo directory (`goose session`), ask something in the spirit of:
> *"Let's run a quick 2D fMRI centering and $z$-standardization check on a synthetic `(V=3 voxels, T=4 time points)` matrix `X = np.array([[98., 100., 102., 104.], [196., 200., 204., 208.], [300., 300., 300., 300.]])`. Write a short snippet that standardizes each voxel's time course (`ddof=0`), and show me what goes wrong if someone standardizes along `axis=0` instead of `axis=1` or fails to guard against a zero-variance constant voxel."*

### 2. What to Look For & How to Trace the Error Back Down
- **Red Flag 1 (Wrong Axis `axis=0` vs. `axis=1`):** If the AI writes `(X - X.mean(axis=0)) / X.std(axis=0)`, it standardizes across the *3 voxels at each time point* instead of across each voxel's *4 time points*. Even worse, `X_wrong.mean()` across the whole matrix is still `0.0`!
  - *Traceback:* Check per-voxel row means `X_std.mean(axis=1)`—under `axis=0`, row means are non-zero (`[-1.20, -0.02, +1.22]`), proving static tissue baseline differences were mixed across time instead of removed within each voxel. Fix by specifying `axis=1, keepdims=True`.
- **Red Flag 2 (Zero-Variance Voxel `NaN`/`Inf`):** Voxel 2 (`[300., 300., 300., 300.]`, e.g., an out-of-brain or saturated voxel) has temporal standard deviation $\sigma_{v=2} = 0.0$. Naive division raises a `RuntimeWarning: invalid value encountered in divide` and fills row 2 with `nan`.
  - *Traceback:* Inspect `np.isnan(X_std).any()` and `X.std(axis=1)`. Fix with `np.divide(X - mu, sd, out=np.zeros_like(X), where=sd > 1e-12)`.

### 3. Expected Outcome Range & Why It Must Look That Way
- **Expected Valid Outcome:**
  - Voxels 0 and 1 have **identical standardized time courses** `[-1.3416, -0.4472, +0.4472, +1.3416]` (mean $= 0.0$ within $\pm 10^{-12}$, `ddof=0` SD $= 1.0$ within $\pm 10^{-12}$, range $\in [-1.35, +1.35]$), even though Voxel 1 had twice the raw baseline (`200` vs. `100`) and twice the raw step (`4` vs. `2`).
  - Voxel 2 is cleanly `0.0` across all 4 time points with zero `NaN`s.
- **Why It Must Look That Way:** For any equally spaced 4-point linear ramp $x_t = \mu + c \cdot (-1.5, -0.5, +0.5, +1.5)$ with $c > 0$, subtracting $\mu$ removes the baseline offset and dividing by $\sigma = c \sqrt{\frac{1}{4}(2.25 + 0.25 + 0.25 + 2.25)} = c \sqrt{1.25}$ cancels the slope $c$ completely, leaving $z_t = (-1.5, -0.5, +0.5, +1.5) / \sqrt{1.25} \approx (-1.3416, -0.4472, +0.4472, +1.3416)$. Notice also why this $z$-score is a *descriptive within-voxel rescaling*, **not** an inferential $z$-statistic testing a population hypothesis!

---

## When something fails on macOS

- **`ollama: command not found` or `goose cannot connect to localhost:11434`:** Launch `Ollama.app` from `/Applications` (`open -a Ollama`) or run `ollama serve` in a background terminal tab, then verify with `ollama list`.
- **MacBook Pro fan spin / memory pressure in Activity Monitor:** Check *Activity Monitor $\to$ Memory*. If Memory Pressure turns yellow/red while running a 27B model alongside Jupyter, switch Goose to `qwen3.5:9b` or `gemma4:e4b` and unload idle models with `ollama stop <model>`.
- **`ModuleNotFoundError` in JupyterLab:** Confirm the notebook kernel in the top-right corner of JupyterLab is **Python 3 (ipykernel)** launched via `uv run --frozen jupyter lab notebooks`.
- **AI output disagrees with a notebook assertion:** Never ask Goose to delete or loosen the `assert`. Use the lesson's **What to Look For & Error Traceback** checklist to find the first intermediate array whose shape, units, axis, or fitting boundary diverged.

---

## Check the course on your MacBook Pro

From the repository root:

```zsh
./setup.sh --check
```

This validates repository links, citations, and math hygiene, and executes **82 offline computational notebooks** in fresh Jupyter kernels (78 main-course lessons + 4 introductory supplement labs). To include the public-data fMRI project (`P02`):

```zsh
./setup.sh --check-all
```

Once Step 0 is complete, open **[R00: Reading a research paper](../notebooks/00_paper_orientation/00_how_to_read.ipynb)** and follow the **[26-week study sequence](STUDY_PLAN.md)**.
