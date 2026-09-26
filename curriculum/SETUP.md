# Setup: one tutor, one notebook, one operation at a time

Written 24 September 2026. Model tags and interfaces can change; verify the linked provider page when installing. The lessons work with **Ollama + Goose + a tool-capable Qwen3.6 or Gemma4 model**, or with **ChatGPT** as the tutor. Model choice does not change the scientific checks.

## Start reading before installing Python

Open [R00: how to read](../notebooks/00_paper_orientation/00_how_to_read.ipynb), the [reading method](papers/READING_METHOD.md) and the [paper list](papers/README.md). The [26-week study plan](STUDY_PLAN.md) begins with two weeks of six motivating papers and R00–R03 before F01. GitHub can display these markdown-only seminars in a browser; no Python, model download or equation solving is needed for the first pass. Save questions and figure evidence in the [coursework templates](coursework/PAPER_TO_EXPERIMENT.md).

AI is optional for the reading itself. When using it, provide the assigned paper version or check that it can access the text. Follow the [reading tutor contract](AI_WORKFLOW.md#start-with-the-scientific-problem); a model's general knowledge does not establish that it has read a recent paper. Set up Python before the computational lessons begin.

## Choose a route

| Route | What each part does | Use it for |
| --- | --- | --- |
| Ollama + Goose | Ollama runs the selected model; Goose connects that model to approved local file/code tools; Python computes the result | Paper discussion and guided local notebook/code work |
| ChatGPT + local Jupyter | ChatGPT discusses an accessible paper or drafts a snippet; she later runs code in Jupyter and shares the toy result | Fast start, same readings, lessons and checks |

The language model is the tutor/code assistant. NumPy, SciPy, NiBabel, Nilearn, and scikit-learn do the numerical work. An LLM's fluent explanation is not an image-registration algorithm, and a general vision model seeing a screenshot is not validated volumetric MRI analysis. A neuroimaging foundation model later in the course is a different kind of model with its own data and validation requirements.

## Local AI route

1. Install [Ollama](https://docs.ollama.com/quickstart) and [Goose](https://goose-docs.ai/docs/quickstart/) using their official instructions for the learner's operating system.
2. Choose an explicit model tag. Current official listings include `gemma4:e2b`, `gemma4:e4b`, `qwen3.6:27b`, and `qwen3.6:35b`. Start with a model that fits the machine and passes the short exercise below. Exact hardware is not yet known.
3. Download **one** chosen model. For example:

```sh
ollama pull gemma4:e2b
ollama run gemma4:e2b
```

For a machine suited to the larger Qwen model, substitute `qwen3.6:27b` in both commands. “Qwen 3.6+” is a preference, not a literal Ollama tag. Newer versions can be substituted after checking their exact tags and tool support.

4. Keep the Ollama service running. Run `goose configure`, select the Ollama provider, enter `http://localhost:11434`, and select the **same installed model tag**. In Goose Desktop, configure the equivalent provider/model settings. See [official provider guidance](https://goose-docs.ai/docs/getting-started/providers/).
5. Open only this course folder for the session. Use a mode that lets her review execution and enable only the file/code tools needed for the exercise. The `.goosehints` in the repository root gives the tutor instructions; it is guidance, not a security boundary.
6. Run the smoke test below. If tool calls fail, she can use the model as a chat tutor and paste the snippet into Jupyter. A model's advertised tool capability does not guarantee reliable tool use in every integration.

The [Gemma4 listing](https://ollama.com/library/gemma4) currently shows roughly 7.2 GB and 9.6 GB downloads for e2b/e4b. The [Qwen3.6 listing](https://ollama.com/library/qwen3.6) shows roughly 18 GB and 23 GB for 27b/35b. Download size is **not total working memory**; the runtime and context also need memory. These are installation facts, not claims about neuroimaging accuracy. No large model download is required to read or execute this course's reference notebooks.

Use an ordinary local tag rather than a `cloud` tag when the intention is local inference. Goose's external tools can still send data outside the machine. The bundled exercises use synthetic data. For actual research data, use the lab's approved environment and data rules.

## ChatGPT route

Open ChatGPT, start a learning conversation, and paste the appropriate reading or computational tutor contract plus the current lesson. For a paper, work through one source-grounded figure question at a time. Later, ask it to work one prediction and one snippet at a time. Run reference snippets in local Jupyter, then paste the text output or a plot from the synthetic exercise. This route does not require Goose or configuring an OpenAI API key. Available tools and models vary with the account; the course does not require a particular paid tier. [Official ChatGPT guidance](https://learn.chatgpt.com/docs/use-chatgpt).

## Python notebooks

From the repository root on macOS, Linux, or Windows Subsystem for Linux:

```sh
./setup.sh
uv run --locked jupyter lab notebooks
```

The script installs uv when needed, selects Python 3.12, and installs the versions in [uv.lock](../uv.lock). Choose the course environment as the Jupyter kernel. The offline notebooks run without a dataset download; P02 retrieves a public fMRI teaching dataset. R00–R03 can be read in a browser.

The [project file](../pyproject.toml) lists direct dependencies, and `uv.lock` pins the complete environment. [requirements-tested.txt](../requirements-tested.txt) records the earlier Python 3.14 validation environment.

## The tutor contract

Copy this into the chosen AI at the beginning of each computational lesson. Use the separate [reading contract](AI_WORKFLOW.md#start-with-the-scientific-problem) for paper seminars:

> You are my neuroimaging tutor. I am learning to supervise AI-written analysis, not memorize programming syntax. Work on only the current lesson. Explain the input, named axes, units, output, parameters, and what information will be changed or lost. Ask me to predict one result and wait for my answer. Then propose one small operation, usually no more than 20 lines. Tell me how to inspect the code and show at least one numerical check and one visual check when relevant. Do not run ahead or reveal the answer key before I try. Use the supplied synthetic data first. Label simulations and assumptions. If I make a mistake, explain the missing concept in simpler terms and give a smaller example. Do not remove checks to make code pass. Do not invent a file, API, citation, execution result, diagnosis, or scientific conclusion. Preserve raw inputs, record actual versions/settings, and distinguish code you proposed from code we executed. When you suggest a method, name the research question that makes it appropriate.

## Ten-minute acceptance exercise

Ask: “For `[2,4,6]`, predict the mean and describe what z standardization does. Wait. Then provide a short snippet with ddof=0, verify its mean and SD, and explain why this is not a significance test.”

The tutor passes if it waits for a prediction, gives executable short code, recovers mean 4, produces standardized mean near 0 and SD near 1, and rejects the significance-test interpretation. This is a small usability check, not a model benchmark. If it fails, use the provided reference notebook and a stronger available tutor model; do not let the learner absorb the incorrect explanation.

## When something fails

- **Import error:** check which Python kernel is running and install into that environment.
- **Goose cannot reach the model:** confirm Ollama is running and the endpoint and installed tag match.
- **Slow or failed inference:** reduce model size/context, or use ChatGPT; keep notebook data small.
- **AI forgets the instructions:** start a fresh lesson conversation with the contract and current data card.
- **Wrong numbers or plots:** compare with the supplied checks; ask the AI to identify the first divergent step. Never ask it to simply make the assertions pass.


## Check the course

Run from the repository root:

```sh
./setup.sh --check
```

This checks repository structure and runs 82 offline computational notebooks in fresh Jupyter kernels: 78 from the current course and four from the introductory supplement. To include the public-data fMRI project:

```sh
./setup.sh --check-all
```

The full check executes 83 course-authored computational notebooks and labels the four reading seminars for instructor assessment. Preserved third-party notebooks use their original tool and data environments. Generated data, outputs, environments, and execution copies remain outside version control. Start with [R00](../notebooks/00_paper_orientation/00_how_to_read.ipynb) and follow the [study sequence](STUDY_PLAN.md).
