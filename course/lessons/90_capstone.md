# Capstone: make one defensible neuroimaging claim

Two 75-minute sessions plus independent practice. Use a toy project first, then the [real-data bridge](../REAL_DATA.md) with supervision. A full original research study will require more time than these two sessions.

## Session A — Plan and inspect

**0–15 min:** Choose one question. Beginner option: “In a simulated task run with known truth, can our planned contrast recover the planted effect?” Real-data option: “In this documented single-subject auditory teaching run, how does the fitted listening contrast depend on a predefined processing choice?” The latter is a methodological replication, not a population claim about hearing.

**15–30 min:** Fill the [project plan](../templates/project_plan.md). Identify observations, dependent time samples, acquisition metadata, contrast direction, one primary outcome, and one sensitivity analysis before opening the final result. For the real-data option record dataset citation, downloaded version/files, event timing, TR, and processing history. Do not infer missing metadata from image appearance.

**30–50 min:** Ask AI:

> Review my plan as a methods tutor. List the steps in input → operation → output form. Identify one ambiguity about the scientific question, one dependence issue, and one operation that might remove my signal. Do not implement the full pipeline. Ask me to resolve the most consequential ambiguity first.

Use the 520 and 540 notebooks to demonstrate the risky step on toy data. Make two transformation cards. If the plan concerns prediction instead, substitute participant/site grouping, a simple baseline, training-only transformations, a primary metric, and an untouched test set.

**50–65 min:** Instructor/mentor reviews the plan. Record revisions and lock the intended analysis. This is a teaching review, not a requirement to seek new approval for every small command. A learner without a mentor can finish the toy replication and document unanswered real-data questions.

**65–75 min:** Exit questions: “Which result would refute my expectation?” and “What could change the apparent answer without changing the underlying biology?” Expected responses name actual checks or alternative outcomes, not generic statements that AI can be wrong.

## Session B — Execute, challenge, and explain

**0–25 min:** Have AI help implement one planned step at a time. Use the provided notebook section for the toy project, or the documented external workflow for the real-data project. Save actual outputs. Inspect shape, coordinates, display scales, design columns, residual behavior, and model assumptions where relevant. Do not silently switch methods after seeing an inconvenient result.

**25–40 min:** Perform the planned sensitivity analysis. For the toy run, vary a confound's overlap with the task while keeping the planted effect explicit; show why recoverability becomes difficult. For the auditory tutorial, compare one predeclared processing setting while keeping the data, design, inference rule, and plotting scale fixed. The tutorial uses its documented modeling approach; the hand-built iid toy t test is not a substitute for temporal noise modeling.

**40–55 min:** Ask AI to challenge the interpretation:

> Use only my executed results and analysis record. Give one alternative explanation, one unchecked assumption, and one claim these data cannot support. Separate reported observations from your inferences. Do not invent additional participants or claim causal or clinical validation.

**55–65 min:** Close the chat. Give a five-minute presentation: question; data; three important transformations; checks; result; uncertainty; limitation. Explain one deliberate failure you caught. If the project is predictive, show the baseline and evaluation split before the model's score.

**65–75 min:** Score with the [rubric](../ASSESSMENT.md). Deliver: plan; data/processing provenance; notebook; three transformation cards; two informative figures with axes/units; a 300-word methods/results note; and a failure log. Distinguish planned analysis from exploration.

**A good final claim:** “In this teaching example, the result changes when this specified operation changes, consistent with this proposed mechanism; these data and checks do not establish broader clinical performance.” Replace every “this” with the actual operation/result. A valid negative or inconclusive result passes.
