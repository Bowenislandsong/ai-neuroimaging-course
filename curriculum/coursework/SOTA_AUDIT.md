# Assignment: turn “state of the art” into a checkable comparison

**When:** first pass in R02/R03; revise after M04 and M16–M18. **Time:** 60–90 minutes initially, 90 minutes for the revision. **Output:** a one-page comparison card and a 300-word recommendation. No coding is required for the first pass.

Prepare one card for one chosen model, then revise that same card. During orientation, complete the source/version, intended task, inspected comparison and claim boundary; mark technical details unknown with a source location and a question. The later revision resolves fitting, split, metric and implementation details as far as the available evidence permits. A missing report in the paper may remain an explicitly documented limitation.

Choose BrainIAC, BrainMorph, Omni-fMRI, or another verified current paper in the course. The task is not to decide which model is globally “best.” Decide whether one specific reported advantage answers a specific intended research use.

| Field | Record from the paper, supplement or official repository | Why it matters |
|---|---|---|
| Version and status | Date, venue, DOI/arXiv version; distinguish acceptance from the version read | Claims or experiments can change between versions |
| Task and input | MRI contrast/modality, dimension, spatial resolution, timing and required preprocessing | A different input contract can invalidate transfer |
| Learning target | What is predicted/reconstructed/contrasted during pretraining and downstream fitting | Training success need not answer the scientific question |
| Data scale | People, scans, sessions and datasets separately; deduplication if described | Repeated scans are not new independent people |
| Split | Person/site/run boundaries; tuning and external evaluation | Controls leakage and defines generalization |
| Comparators | Named methods, pretrained data, training budget, tuning protocol | A weak or uneven comparison can overstate an advantage |
| Metric | Units, direction, uncertainty, per-task vs aggregate result | A mean can hide failure on the task you need |
| Ablation | Which component was removed or changed; whether budget/data are comparable | Tests a component's contribution under those conditions; it does not establish a biological mechanism |
| Access | Code commit, environment, data restrictions, checkpoint and license actually found | “Code available” does not mean a result is immediately reproducible |
| Boundary | A population, scanner, task or failure case not established by the evaluation | Prevents a benchmark result becoming a universal claim |

Mark unknown fields as unknown and identify the location you checked. Do not insert an attractive number from an AI answer without locating it in the source. If you transcribe a result table row, preserve metric direction and uncertainty, and cite the row/table precisely; do not silently combine different evaluation protocols.

## Decision exercise

A collaborator wants to use the model on an unseen scanner and a smaller local cohort. For a prediction model, propose a different downstream target; for a registration model, propose a changed image contrast or alignment condition instead. Write **use as a candidate / insufficient evidence / unsuitable input**, with conditions and evidence. On the first pass, describe a simple comparison and a failure you would want to detect in ordinary language; unresolved choices may remain questions. In the revision, name the baseline, data split, one QC criterion and one result that would make you reject the model. The choice is hypothetical; no actual clinical deployment is authorized by this coursework.

Ask the AI to argue for the opposite decision, restricted to the same evidence. Check each counterargument against the paper, then revise only when the evidence warrants it. A newer publication date is not an argument about validity.

## Marking: 20 points

Five areas scored 0–4: source/version accuracy; input/target understanding; split/independence; fair comparison/metric; justified decision and limits. Use the [common rubric levels](PAPER_TO_EXPERIMENT.md). A 3 means correct and independently explained for the assigned stage; a 4 adds a concrete discriminating follow-up test or well-justified limitation. Orientation feedback assesses the inspected evidence and quality of unresolved questions, not prior knowledge of validation methods. Apply the final passing requirement—at least 3 in every area—after the revised card. Unsupported claims of universal superiority, hidden test-set tuning or invented source numbers must be corrected before passing.

## Instructor checks

Accept multiple defensible recommendations. Require a named task and actual comparator rather than “beats SOTA.” A conference-listed article read via an arXiv version should retain both facts. An author-released benchmark result is evidence about that evaluation, not an independent reproduction performed by this course. Attention or saliency pictures do not by themselves identify a biological mechanism. A code link and a data-download link have different access and reuse implications.
