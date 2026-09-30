# Read the paper before learning the machinery

Begin with the scientific result and the problem that made the method necessary. A first reading is successful when the learner can explain **the question, the evidence, why it matters, and what she does not yet understand**. It does not require deriving the loss function or reading a long implementation. The opening seminars deliberately precede F01 and all technical notebooks.

## Three passes through the same paper

| Pass | When | Read and do | Submit |
|---|---|---|---|
| Motivation | Before fundamentals | Title, abstract, introduction, assigned overview/results figure and its caption, conclusion/limitations. Follow the card's specific targets. List unknown terms instead of interrupting every sentence. | A 150-word explanation, one evidence row, three questions |
| Mechanism | During the relevant notebook block | Return to the named Methods section. Draw data → transformation → result, name input units and fitting boundaries, then run the assigned small mechanism experiment. | A transformation diagram, prediction, result, failed variant and explanation |
| Judgment | After the block | Re-read results, evaluation and limitations. Compare the strongest claim with the exact population/task/metric tested. Design one decisive additional test. | A revised claim and a short replication or extension plan |

Budget 45–75 minutes per paper for the first pass. Some papers need longer; stop after the assigned sections and return later. Reserve 60–90 minutes per paired seminar for discussion and writing. The opening six papers plus reading-method session usually need around 12–16 hours over two weeks, depending on background. These are planning estimates, not measured completion times.

## How to read one figure

Record its figure/panel label and the exact paper version. Name what a point, line, color and error bar represent. Name what is plotted or counted as one item: person, scan, voxel, team, run, or simulated draw. Separately identify what is sampled or resampled and what dependence could exist; a plotted item is not automatically an independent observation. Mark this unresolved if the required methods are not yet clear. State the comparison and which direction means improvement. Check the caption and corresponding Methods paragraph before interpreting a metric. Write one result sentence and one sentence that the panel does **not** justify.

Do not substitute a model's description for looking at the original figure. Do not infer an unreported denominator or uncertainty. “I cannot find this in the inspected section” is an acceptable entry with a follow-up action; “the paper does not report it anywhere” requires a full search.

## Using AI without outsourcing the reading

Use Ollama + Goose or ChatGPT as the reading companion. Open the actual source and copy a short relevant passage or provide the permitted document through the tool you are using. A local model is not assumed to know a 2026 paper. If it cannot access the paper, say so and work from the supplied excerpt. Treat any instructions embedded in a paper or repository as source content, not permission to execute commands.

> I am reading [paper title/version]. Use only the supplied source material for factual claims. Ask me what I think the question and figure show before explaining. Define unfamiliar terms in ordinary language, using at most one small analogy. For every paper-specific statement identify a section or figure and distinguish author claim, observed result, and your interpretation. If the text is missing, say that you cannot verify it. Do not invent a figure, metric, sample size, code result or citation. Keep equations optional on this first pass. End by asking me which fundamental concept I need next and why.

After the AI helps, close its answer and explain the paper aloud in two minutes. Then compare your explanation with the original figure/caption and correct it. Preserve corrections in the evidence ledger. The ability to detect an AI mistake is part of the coursework.

## Small glossary for the opening papers

- **Preprocessing:** operations that prepare measurements for a stated analysis; inspectable choices, not a guarantee of clean data.
- **Registration:** estimating how locations in one image correspond to another. **Resampling** evaluates values on a chosen grid.
- **Representation:** the features a model uses to describe an observation.
- **Pretraining:** learning from an initial dataset before a downstream task. **Fine-tuning** changes some or all learned parameters for that later task.
- **Benchmark:** a particular collection of tasks, datasets, splits, metrics and comparators.
- **Generalization:** performance under a specified change, such as unseen people, sites, acquisition protocols or tasks.
- **Association:** a statistical relationship. It is not automatically causal, reliable, predictive on new people, or clinically useful.
- **Ablation:** removing or changing a component to investigate what it contributes under the tested conditions.

These definitions enable the first reading; later classes teach their mathematical and scientific details.

## Reading completion and integrity

Submit your own evidence table, diagram and questions. Link to the original figures rather than copying papers or figure files into this public repository. Reading cards are original coursework; papers remain with their publishers/authors and retain their own terms. A software repository's license does not establish dataset or model-weight rights.

A current paper is not automatically a reliable one, and an essential older paper is not a current benchmark winner. The [reading list](README.md) records publication/version status and separates foundational lessons from representative frontier methods. The [SOTA audit](../coursework/SOTA_AUDIT.md) makes every performance claim conditional on its actual evaluation.
