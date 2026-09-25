# Learn to supervise the analysis

The intended skill is **understanding and checking what AI-generated code does**. The learner does not need to memorize syntax. She does need to explain observations, axes, units, coordinate spaces, fitted parameters, independence, uncertainty, and limits. AI cannot choose those correctly from an ambiguous request.

Use either Ollama + Goose with a suitable Qwen3.6/Gemma4 tag, or ChatGPT beside Jupyter. The [setup guide](SETUP.md) covers both. A tutor model generates and explains snippets. NumPy, SciPy, NiBabel, Nilearn, and scikit-learn carry out the numerical operations. Later imaging foundation models are separate scientific models, with their own input contracts and validation requirements.

## The class cycle

1. **Predict:** look at the input, name its axes/units, and predict what the operation changes.
2. **Ask:** request a single small operation, usually 5–20 lines, and its checks.
3. **Read:** identify inputs, parameters, fitted quantities, output, and hidden assumptions.
4. **Run:** execute the actual code; keep its result distinct from the model's predicted result.
5. **Inspect:** compare a numerical invariant with a meaningful plot or diagnostic.
6. **Break:** make the lesson's deliberate wrong choice and explain why the result is misleading.
7. **Defend:** explain the result without reading AI prose; then open the answer guide.
8. **Transfer:** complete the named upstream assignment and connect its real data or specialist package to the local demonstration.

Copy this contract into the tutor:

> Teach only the current notebook. Ask me to predict one result and wait for my answer. Then propose one short operation with named input/output axes, units, coordinate space, parameters, fitting population, and information lost. Explain every line I cannot read. Include one numerical check and an appropriate visual diagnostic. Distinguish a mathematical check from scientific validity. Use the provided data. Do not invent metadata, sources, software behavior, completed preprocessing, or execution results. Do not remove an assertion to make a result pass. If something fails, isolate the first divergent step and explain its cause. Keep the answer key hidden until I attempt the questions. Before continuing, ask me to explain why this transformation belongs to the research question.

## Prompts that expose understanding

| Situation | Useful prompt | What the learner must decide |
|---|---|---|
| Resampling | “Show what changes when the target grid becomes 4 mm. Is any registration estimated?” | Image space, interpolation, lost resolution, alignment evidence |
| Filtering | “Plot the operation's frequency response and compare it with the task timing.” | Signal/nuisance overlap and effects of censoring |
| Regression | “Identify the design columns, contrast, residual assumptions, and observation unit.” | Estimand, confounds, dependence, uncertainty |
| Machine learning | “Draw every fitting boundary, including scaler, feature selection, and tuning.” | Independent split and intended deployment population |
| Model failure | “Give a tiny counterexample that reproduces the error. Do not rewrite everything.” | Whether the failure is numerical, bookkeeping, measurement, or design |
| New checkpoint | “Read its original model card; state training data, license, target, expected input, and missing validation.” | Whether an imaging model is appropriate for this task |

## The minimum independent literacy

She should be able to read a function call, index and shape, axis reduction, condition, and assertion; distinguish a mean from a variance and a parameter from an estimate; spot a unit/space/timing mismatch; recognize duplicated participants; explain training/test leakage; and interpret an effect separately from uncertainty. The foundations and data-science strands teach this in small pieces. Programming syntax can be looked up; these decisions cannot be delegated without understanding.

For a wrong answer, require a simpler explanation and a smaller example. For a correct answer, ask for a different dataset or parameter. More fluent wording is not the progression criterion. The [assessment guide](ASSESSMENT.md) specifies the evidence required.

## Session record

Save notebook ID, date, model/provider and exact tag where available, initial prediction, prompt, generated code, your edits, actual result, check, failure diagnosis, and interpretation. With local tools, limit the session to the course workspace and review external operations. For real participant data, use the institution's approved environment; public toy data support the same reasoning practice without exposing private inputs.

Neither Ollama nor a large tutor model is required to execute the reference notebooks. The delivered validation checks Python lessons, not the correctness of every possible AI response or a live Goose/Ollama integration.
