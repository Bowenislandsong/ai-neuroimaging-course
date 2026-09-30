# Setup: Step 0 on macOS (MacBook Pro) — Goose + Ollama with Qwen & Gemma

This introductory supplement shares the same **macOS (Apple Silicon MacBook Pro)** environment and **Step 0 agentic setup** as the main 83-notebook curriculum ([full setup guide](../curriculum/SETUP.md)). The lessons work with **Ollama + Goose running the latest Qwen (`qwen3.5:9b` / `qwen3.6:27b`) and Gemma 4 (`gemma4:e4b` / `gemma4:26b`) models** on your MacBook Pro, or with **ChatGPT** alongside local JupyterLab.

## Choose a route on your MacBook Pro

| Route | What each part does | Use it for |
| --- | --- | --- |
| **Ollama + Goose on macOS** *(Recommended)* | Ollama runs **Qwen** (primary coding/tool agent) and **Gemma 4** (scientific auditor) on Apple Silicon unified memory; Goose connects the model to local repo files; Python computes the result | Agentic notebook execution, error tracing, and class deliverables |
| **ChatGPT + local Jupyter on macOS** | ChatGPT drafts or critiques a snippet under the tutor contract; you run it in local JupyterLab and verify the output against expected ranges | Fast fallback with the exact same lessons and checks |

The language model is your coding assistant and reasoning partner; NumPy, SciPy, NiBabel, Nilearn, and scikit-learn perform the numerical computation. A fluent LLM explanation is not an image-registration algorithm, and a neuroimaging foundation model later in the course (`BrainIAC`, `BrainMorph`, `Omni-fMRI`, `MindEye2`) is a distinct scientific model with its own input contract and validation rules.

## Step 0 · Local AI route on macOS (MacBook Pro)

0. **Minimal Apple Developer Setup (~5 min, no full Xcode needed):** Install [Apple Command Line Tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools) (`xcode-select --install`, ~600 MB) for `git` and `clang` without downloading the 12+ GB Xcode.app bundle, and confirm native [Apple Silicon](https://support.apple.com/en-us/116943) (`uname -m` $\to$ `arm64`) in [Terminal.app](https://support.apple.com/guide/terminal/welcome/mac). Built-in [Apple Metal](https://developer.apple.com/metal/) and [Accelerate](https://developer.apple.com/documentation/accelerate) handle GPU/BLAS compute automatically ([macOS Gatekeeper & Privacy guide](https://support.apple.com/en-us/102445)).
1. Check your MacBook Pro's unified memory in **Terminal.app** ([Activity Monitor Memory guide](https://support.apple.com/guide/activity-monitor/view-memory-usage-actmntr1004/mac)):
   ```zsh
   xcode-select -p >/dev/null 2>&1 || xcode-select --install
   sysctl -n hw.memsize | awk '{printf "MacBook Pro Unified Memory: %.0f GB\n", $1/1073741824}'
   ```
2. Install [Ollama for macOS](https://ollama.com/download/mac) (`brew install --cask ollama && open -a Ollama`) and pull **both** the latest **Qwen** and **Gemma 4** models sized for your MacBook Pro:
   - **Standard 16 GB – 24 GB MacBook Pro:**
     ```zsh
     ollama pull qwen3.5:9b
     ollama pull gemma4:e4b
     ```
   - **32 GB+ MacBook Pro (`M1/M2/M3/M4` Pro or Max):**
     ```zsh
     ollama pull qwen3.6:27b
     ollama pull gemma4:26b
     ```
   *(Or run `./setup.sh --setup-ai` from the repository root to detect your MacBook Pro RAM and pull both models automatically.)*
3. Install [Goose](https://goose-docs.ai/docs/quickstart/) on macOS (`curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash`), run `goose configure`, select **Ollama** (`http://localhost:11434`), and choose `qwen3.5:9b` (or `qwen3.6:27b`) as your coding agent. Use `gemma4:e4b` (or `gemma4:26b`) when you want a second-opinion scientific audit of a figure or transformation contract.
4. Open only this repository folder for your session. The root [`.goosehints`](../.goosehints) configures Goose to follow our three-part supervision workflow: **Suggestive Prompts ("in the spirit of")**, **Immediate Error Spotting & Root-Cause Traceback**, and **Expected Outcome Ranges & Why**.

## ChatGPT route

Open ChatGPT, start a learning conversation, and paste the tutor contract below plus the current lesson. Ask it to work one prediction and one snippet at a time, run the code in local JupyterLab on your MacBook Pro, and verify the result against the expected range. [Official ChatGPT guidance](https://learn.chatgpt.com/docs/use-chatgpt).

## Python notebooks on macOS

From the repository root in **Terminal.app**:

```zsh
./setup.sh
uv run --frozen jupyter lab course/labs
```

Choose the locked `uv` environment as the Jupyter kernel. Each notebook runs cleanly from top to bottom, and the exported `.html` companions display saved reference outputs. Run `./setup.sh --check` from the repository root to execute these four notebooks along with the main course's 78 offline lessons.

## The tutor contract

Copy this into your AI assistant at the beginning of each lesson (or launch `goose session` from the repository root so `.goosehints` loads automatically):

> You are my neuroimaging tutor and pair-programming agent on macOS. I am learning to supervise AI-written analysis for class deliverables: you handle the coding boilerplate while I verify the transformation contract, spot silent errors immediately, trace bugs back to their root cause, and check outcomes against expected ranges. Work on only the current lesson. Explain the input, named axes, units, output, parameters, and what information will be changed or lost. Ask me to predict one result and wait for my answer. Then propose one small operation, usually no more than 20 lines, with at least one numerical check and one visual check. Do not remove checks to make code pass. Do not invent a file, API, citation, execution result, diagnosis, or scientific conclusion.

## Ten-minute acceptance exercise

Give Goose (or your tutor) a prompt **in the spirit of**:
> *"For the 1D array `[2.0, 4.0, 6.0]`, ask me to predict the mean and what $z$-standardization (`ddof=0`) will produce, and wait. Then write a 10-line snippet that computes the standardized array, contrasts `ddof=0` vs. `ddof=1`, and explains why a standardized array is not a hypothesis test."*

- **What to look for & trace back:** Check whether the snippet used `ddof=0` ($\sigma = \sqrt{8/3} \approx 1.6330$) vs. `ddof=1` ($s = 2.0$). If the output values are `[-1.0, 0.0, +1.0]` instead of `[-1.2247, 0.0, +1.2247]`, trace the discrepancy directly to the `ddof` argument in `np.std()`.
- **Expected outcome range & why:** The mean must be `4.0`, the standardized mean must lie within `0.0 ± 1e-12`, the `ddof=0` standard deviation must be `1.0 ± 1e-12`, and the standardized values must be `[-1.2247, 0.0, +1.2247]` because $\frac{6 - 4}{\sqrt{8/3}} = \sqrt{3/2} \approx 1.2247$.

## When something fails

- **Import error:** check that JupyterLab was started via `uv run --frozen jupyter lab`.
- **Goose cannot reach the model:** confirm `Ollama.app` is running on macOS (`ollama list`) and the endpoint (`http://localhost:11434`) and installed tag (`qwen3.5:9b`, `qwen3.6:27b`, `gemma4:e4b`, or `gemma4:26b`) match.
- **High memory pressure on MacBook Pro:** switch to `qwen3.5:9b` or `gemma4:e4b` and close unused applications.
- **Wrong numbers or plots:** compare with the lesson's expected outcome range and trace back to the first divergent array shape, axis, unit, or split. Never delete an assertion to force a pass.
