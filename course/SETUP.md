# Setup: one tutor, one notebook, one operation at a time

Written 24 September 2026. Model tags and interfaces can change; verify the linked provider page when installing. The lessons work with **Ollama + Goose + a tool-capable Qwen3.6 or Gemma4 model**, or with **ChatGPT** as the tutor. Model choice does not change the scientific checks.

## Choose a route

| Route | What each part does | Use it for |
| --- | --- | --- |
| Ollama + Goose | Ollama runs the selected model; Goose connects that model to approved local file/code tools; Python computes the result | Guided local notebook/code work |
| ChatGPT + local Jupyter | ChatGPT explains or drafts a snippet; she runs it in Jupyter and shares the toy result for discussion | Fast start, same lessons and checks |

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
5. Open only this course folder for the session. Use a mode that lets her review execution and enable only the file/code tools needed for the exercise. The `.goosehints` in this folder gives the tutor instructions; it is guidance, not a security boundary.
6. Run the smoke test below. If tool calls fail, she can use the model as a chat tutor and paste the snippet into Jupyter. A model's advertised tool capability does not guarantee reliable tool use in every integration.

The [Gemma4 listing](https://ollama.com/library/gemma4) currently shows roughly 7.2 GB and 9.6 GB downloads for e2b/e4b. The [Qwen3.6 listing](https://ollama.com/library/qwen3.6) shows roughly 18 GB and 23 GB for 27b/35b. Download size is **not total working memory**; the runtime and context also need memory. These are installation facts, not claims about neuroimaging accuracy. No large model download is required to read or execute this course's reference notebooks.

Use an ordinary local tag rather than a `cloud` tag when the intention is local inference. Goose's external tools can still send data outside the machine. The bundled exercises use synthetic data. For actual research data, use the lab's approved environment and data rules.

## ChatGPT route

Open ChatGPT, start a learning conversation, and paste the tutor contract plus the current lesson. Ask it to work one prediction and one snippet at a time. Run reference snippets in local Jupyter, then paste the text output or a plot from the synthetic exercise. This route does not require Goose or configuring an OpenAI API key. Available tools and models vary with the account; the course does not require a particular paid tier. [Official ChatGPT guidance](https://learn.chatgpt.com/docs/use-chatgpt).

## Python notebooks

From the repository root, use the same locked environment as the current course:

```sh
./setup.sh
uv run --locked jupyter lab course/labs
```

Choose the uv environment as the Jupyter kernel. Each notebook can be run from top to bottom. The exported `.html` companions display saved reference outputs.

The root [uv.lock](../uv.lock) pins the environment. The earlier [requirements-tested.txt](requirements-tested.txt) records the supplement's original test environment.
Run `./setup.sh --check` from the repository root to execute these four notebooks along with the current course's offline lessons.

## The tutor contract

Copy this into the chosen AI at the beginning of each lesson:

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
