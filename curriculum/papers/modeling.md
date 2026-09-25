# Modeling: five papers before the mathematics

Read the problem first, predict what evidence would persuade you, and only then study the transformation. This pack contains two foundations and three recent papers, checked on **2026-09-25 UTC**. The recent choices are representative frontier work and a benchmark study; this is not a claim that they are the best available model for every neuroimaging task. Current searches included 2025 and 2026 work, rather than using a 2024 list as a proxy for the frontier.

**Suggested first encounter:** PM03 → PM05 → PM01 → PM02 → PM04. Spend 60–75 minutes per paper: 10 minutes on the motivating problem, 15 on the assigned passages, 15 on the evidence worksheet, 15 on discussion, and 5–20 on revision. Equations are optional on this first pass. Keep a question list for the later notebooks instead of asking AI to erase every unfamiliar term immediately.

Each card separates a short source-based orientation from original coursework. Open figures in the linked paper; no paper PDFs, figure files, or model weights are redistributed here. Full model reproduction is an optional later project requiring a separate environment, data permissions, hardware planning, and license review. The course notebooks below are deliberately small demonstrations, not reproductions of these papers.

For every reading, submit a one-page **evidence sheet** with five boxes: scientific question; input → operations → output; what was compared; who or what was held out; claim supported versus claim still untested. Mark every statement **paper evidence**, **your inference**, or **unknown**. A cited section is required for the first category. AI can help organize evidence, but the learner owns the final explanation.

<a id="pm01"></a>
## PM01 — What does it mean to decode a brain signal?

**Thomas Naselaris, Kendrick N. Kay, Shinji Nishimoto, and Jack L. Gallant (2011). _Encoding and decoding in fMRI._** Peer-reviewed review, *NeuroImage* 56(2), 400–410; issue year 2011, online publication 2010. [DOI](https://doi.org/10.1016/j.neuroimage.2010.07.073) · [author manuscript, full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3037423/). No original paper-specific code repository was verified for this pack.

**Why start here?** A prediction about an image and a prediction about a voxel answer different questions. The review contrasts encoding and decoding through the direction of the mapping between stimulus features and activity. It also distinguishes successful prediction from a demonstration that an area is necessary for behavior. [Read sections 2–4, especially 4.2, and the Figure 1 caption.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3037423/)

**Before reading:** Imagine a model that predicts whether someone saw a face. Write two different reasons it could succeed, one involving the intended visual distinction and one involving an accidental feature of the experiment. Neither answer needs an equation.

**Reading path:** First locate the two ends of each prediction arrow. Next identify what must be observed while fitting the mapping and what will be available when making a new prediction. Finally inspect the authors' distinction between an informative signal and a behavioral explanation. Leave the probability notation for the second pass.

**Three discussion questions**

1. If image features are available and voxel responses are the target, what kind of model are you evaluating? What changes when the arrow reverses?
2. If category decoding succeeds, which additional experiment would help distinguish visual information from a correlated button response?
3. Could two models predict equally well while giving different explanations? State one observation that would help separate them.

**Coursework before mathematics — the arrow audit.** Make six cards: image, stimulus feature, brain measurement, experimental label, learned parameter, prediction. Arrange two pipelines using those cards. Circle the cards unavailable for a new participant or new stimulus. Then construct a three-row imaginary test sheet: familiar participant/new image; new participant/familiar image; new participant/new image. State which claim each test could support. Deliver two diagrams and the test sheet, plus a 100-word explanation for a non-programmer. Do not draw arrows from “AI” directly to “understanding.”

**Later notebook bridge:** [M01](../../notebooks/04_modeling/01_representations_encoding_decoding.ipynb), [M02](../../notebooks/04_modeling/02_regularized_linear_models.ipynb), and [M10](../../notebooks/04_modeling/10_naturalistic_isc_encoding.ipynb). Run M01, replace one target with a deliberately unrelated target, and save the resulting scores alongside your advance prediction. Deliver a revised arrow diagram naming the arrays and their axes. Success means correctly describing what the score tests, including its dependence on the split.

**Evidence-constrained AI prompt**

> Use only the excerpts I paste from PM01 and my proposed diagram. Identify the prediction direction, observed inputs, target, and one unsupported conclusion. Cite the pasted section label for each paper claim. If evidence is absent, write “not established by this excerpt.” Ask me to explain one arrow before suggesting a correction. Do not invent results, figures, or code. [Paste excerpts and diagram.]

**Instructor notes / answer guide:** Encoding predicts measured responses from features; decoding predicts features or labels from measured responses. A correlated motor response is an acceptable alternative explanation. Holding out an image and holding out a person challenge different kinds of generalization. Reward a clearly stated uncertainty over a confident mechanistic story. Historical discussion is useful for framing questions; do not treat its model assumptions as a universal description of contemporary neural networks.

<a id="pm02"></a>
## PM02 — How can we compare representations with different coordinates?

**Nikolaus Kriegeskorte, Marieke Mur, and Peter Bandettini (2008). _Representational similarity analysis – connecting the branches of systems neuroscience._** Peer-reviewed research, *Frontiers in Systems Neuroscience* 2:4. [DOI and full text](https://doi.org/10.3389/neuro.06.004.2008). No original paper-specific code release was verified here; the later class uses its own small implementation.

**Why read it?** A neural-network unit does not automatically correspond to a brain voxel. RSA compares the pattern of differences between conditions, allowing representations with different measurement coordinates to be related. [Read the Introduction's RDM explanation, Figure 2 caption, and the opening discussion of relationships among models, regions, and behavior.](https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/neuro.06.004.2008/full)

**Before reading:** Choose four everyday objects. Group them by use, then by shape. Explain why both organizations can be sensible even when their layouts disagree. These are your competing hypotheses, not facts about brain organization.

**Reading path:** Follow one pair of conditions into one matrix entry. Trace the row and column labels before interpreting any colors. Ask what a comparison retains and what it discards. On a later pass, distinguish the distance used within a representation from the statistic used to compare two matrices.

**Three discussion questions**

1. Why is matching condition identities essential even when matching individual voxels or model units is unnecessary?
2. Can similar distance patterns prove identical processing mechanisms? Propose a counterexample.
3. What happens if a researcher examines twenty model representations and reports only the closest match to the same noisy brain data?

**Coursework before mathematics — six comparisons, two stories.** Draw two blank 4×4 grids with the same four object names on both axes. Use only “similar,” “intermediate,” and “different” to fill the six distinct off-diagonal pairs under each hypothesis. Make the grids symmetric. Exchange one grid with a partner, or hide its hypothesis and revisit it tomorrow. Identify an object pair that would most clearly distinguish the explanations. Deliver the grids, a proposed stimulus comparison, and a paragraph explaining why a visually attractive grouping is not a statistical test.

**Later notebook bridge:** [M08](../../notebooks/04_modeling/08_rsa_crossvalidated_distances.ipynb) and [M09](../../notebooks/04_modeling/09_searchlight.ipynb). Use M08 to contrast within-sample distances with estimates from independent partitions. Deliberately scramble condition labels in only one representation and document the effect. Deliver labeled matrices and a brief account of the failure. The lab illustrates crossvalidated squared Euclidean distances; it does not implement a complete noise-normalized crossnobis workflow or reproduce this 2008 paper.

**Evidence-constrained AI prompt**

> Using only my pasted PM02 passage and labeled grids, explain what a single off-diagonal entry means. Separate the paper's proposal from my object-grouping hypothesis. Flag condition-label mistakes and any claim that similarity proves causation. Do not add unprovided numerical results. Ask me which comparison would falsify my preferred hypothesis. [Paste passage and grids.]

**Instructor notes / answer guide:** The two grids require the same ordered conditions, not the same number of features. Six unordered pairs are available for four conditions. Two different computations can preserve the same similarity structure; agreement is evidence about that structure, not unique identification of a mechanism. Model selection on the final evaluation data is circular. Matrix entries sharing a condition are dependent: do not let a student treat them as independent participants. Modern distance estimation and noise modeling belong in the later return to the paper.

<a id="pm03"></a>
## PM03 — Can prior MRI experience reduce the need for labels?

**Divyanshu Tak and colleagues (2026). _A generalizable foundation model for analysis of human brain MRI._** Peer-reviewed research, *Nature Neuroscience*, published 5 February 2026. [DOI and full text](https://doi.org/10.1038/s41593-026-02202-6) · [official BrainIAC code](https://github.com/AIM-KannLab/BrainIAC) · [research-only code license](https://github.com/AIM-KannLab/BrainIAC/blob/main/LICENSE).

**Why read it?** BrainIAC learns structural-MRI representations through self-supervised pretraining and adapts them to downstream tasks. The study compares adaptation with other initializations and tests limited-label settings. Its scope is structural sequences, not fMRI. [Read the Results overview, Figure 3 caption, Methods: Pretraining, and the Discussion limitations.](https://www.nature.com/articles/s41593-026-02202-6) Treat reported advantages as findings within the specified tasks and comparisons.

**Before reading:** Suppose you can label only twenty scans. Draw two ways to use a much larger collection without task labels. Mark exactly where information about the final test patients could accidentally enter either plan.

**Reading path:** First identify what the network practices before receiving task labels. Next use the figure caption to distinguish adapting all weights from training a head on fixed features. Then locate which tasks have external tests. Read limitations before deciding what “generalizable” permits you to say. A model learning from several sequence types is not automatically receiving all sequences together for every prediction.

**Three discussion questions**

1. Which weights may change during each comparison, and why does that matter for a fair label-budget comparison?
2. What would you check before claiming an improvement will transfer to a new hospital?
3. Could a plausible saliency map coexist with reliance on a scanner artifact? Describe a test.

**Coursework before mathematics — the transfer contract.** Draw boxes for unlabeled pretraining, task-specific fitting, model selection, and untouched testing. Give every imaginary participant one ID card; place repeated scans together. Construct a table with three rows—random initialization, frozen features plus a head, full fine-tuning—and columns for data access, trainable components, selection rule, and final test. Populate paper-supported cells with section references and mark remaining cells unknown. Choose one actual result panel and list the task, outcome unit, comparator, amount of labeled data, and uncertainty display. Do not copy its image. Deliver this contract and a 90-second explanation of the comparison you find most informative.

**Later notebook bridge:** [M04](../../notebooks/04_modeling/04_nested_sites_harmonization.ipynb), [M15](../../notebooks/04_modeling/15_segmentation_losses.ipynb), [M16](../../notebooks/04_modeling/16_selfsupervision_transfer.ipynb), and [M18](../../notebooks/04_modeling/18_calibration_explanation_reproducibility.ipynb). Use M16 to compare frozen and adapted toy representations at a fixed label budget. Record the fitting data and seed before running. Deliver the observed comparison even if fine-tuning loses. This is a mechanism exercise, not BrainIAC inference or a clinical assessment.

**Evidence-constrained AI prompt**

> Audit my transfer contract against only the PM03 excerpts below. For every cell, return supported, contradicted, or not specified, with its section label. Explain “frozen” and “fine-tuned” using the boxes I drew. Do not infer patient counts from scan counts, invent an external test, or call the model clinically validated. Give one question I must resolve in the methods. [Paste excerpts and contract.]

**Instructor notes / answer guide:** All repeated observations of a held-out person must remain outside task fitting; whether pretraining overlap occurred must be established from the paper rather than presumed. Matching labeled examples alone does not match compute or tuning effort. Saliency supports a hypothesis to investigate, not a causal conclusion. Code availability is verified; execution and checkpoint integrity were not tested here. The repository's custom license restricts use to non-commercial academic research and education, with separate commercial terms. Linking the research does not grant blanket reuse rights.

<a id="pm04"></a>
## PM04 — What must be equal before “better” is meaningful?

**Tassilo Wald and colleagues (2025). _An OpenMind for 3D Medical Vision Self-supervised Learning._** Peer-reviewed ICCV 2025 paper. [Conference publication](https://openaccess.thecvf.com/content/ICCV2025/html/Wald_An_OpenMind_for_3D_Medical_Vision_Self-supervised_Learning_ICCV_2025_paper.html) · [assigned full-text arXiv v2](https://arxiv.org/html/2412.17041v2) · [arXiv DOI](https://doi.org/10.48550/arXiv.2412.17041) · [official nnssl code](https://github.com/MIC-DKFZ/nnssl). The first preprint was 2024; the expanded assigned version is dated 18 April 2025. The arXiv DOI identifies the preprint record, not an IEEE proceedings DOI.

**Why read it?** This benchmark reduces differences in data and architecture when comparing self-supervised approaches. It finds that the preferred approach depends on the task and adaptation setting. [Read sections 3.1, 3.2, 4.1, 4.2, and 5 in v2.](https://arxiv.org/html/2412.17041v2) This is a useful counterweight to treating one successful foundation model as a universal winner.

**Before reading:** Two runners report different finishing times. List the conditions needed to compare their ability. Translate four of those conditions into machine-learning experiment choices without using an equation.

**Reading path:** Begin with what is held constant, not which model wins. Locate the distinction between a model architecture and its training objective. Next compare a classification evaluation with a segmentation evaluation. Finally read how adaptation schedules affect conclusions. The publication and version links matter: the initial dataset-only preprint is not the full benchmark assigned here.

**Three discussion questions**

1. If a new method uses more data, a larger backbone, and longer training, which causal claim about its training objective remains unresolved?
2. Why might preserving whole-image identity help one task while preserving local boundaries helps another?
3. What evidence would justify reporting several conditional winners rather than a single overall winner?

**Coursework before mathematics — design the fair contest.** Propose a four-run experiment that changes one factor at a time. Create columns for dataset and participant split, preprocessing, backbone, objective, training budget, selection budget, adaptation rule, and metric. Circle anything your budget cannot match. Read one result comparison from the assigned paper and identify which of your proposed controls it actually supplies. Then invent two explicit user priorities—few labeled cases versus fast inference—and write how they could alter model choice. Deliver the experiment table and a 150-word reviewer note stating one strength, one unresolved comparison, and the smallest useful follow-up.

**Later notebook bridge:** [M14](../../notebooks/04_modeling/14_cnn_backprop_training.ipynb), [M15](../../notebooks/04_modeling/15_segmentation_losses.ipynb), and [M16](../../notebooks/04_modeling/16_selfsupervision_transfer.ipynb). Change a single adaptation choice in M16 while preserving its data split. Keep an experiment ledger for baseline and changed runs. Deliver loss trajectories, held-out scores, and a statement separating optimization success from generalization. These small exercises teach controlled comparisons; they cannot rank the upstream architectures.

**Evidence-constrained AI prompt**

> From only the pasted PM04 comparison and my experiment table, identify which factors are controlled and which are not established. Do not import a leaderboard or declare a universal best model. Help me phrase a claim whose scope matches this comparison. Ask me to defend one proposed control before suggesting a follow-up. [Paste excerpts and table.]

**Instructor notes / answer guide:** Task, architecture, data, compute, selection, and adaptation all affect a comparison. “Best average” and “best for this task” are different claims. An objective comparison needs more control than two headline numbers. Equal steps do not necessarily mean equal compute; record the chosen fairness criterion. The upstream code repository identifies CC BY-SA 4.0 licensing. Its data and pretrained assets require their own terms to be checked. No upstream training or benchmark rerun was attempted for this reading pack.

<a id="pm05"></a>
## PM05 — What do we lose when we summarize voxels into regions?

**Mo Wang and colleagues (2026). _Omni-fMRI: A Universal Atlas-Free fMRI Foundation Model._** Listed in the official ICML 2026 program; assigned reading is the January 30, 2026 arXiv v1 manuscript. [Official conference listing](https://icml.cc/Downloads/2026) · [versioned full text](https://arxiv.org/html/2601.23090v1) · [arXiv DOI](https://doi.org/10.48550/arXiv.2601.23090) · [official code](https://github.com/OneMore1/Omni-fMRI) · [author project page](https://onemore1.github.io/Omni-fMRI/). A final proceedings version was not independently inspected.

**Why read it?** Omni-fMRI works with voxel-level fMRI and uses dynamic patching to manage computational cost, followed by masked reconstruction pretraining. The manuscript evaluates transfer on multiple tasks and studies frozen representations. [Read sections 3.2–3.3, 4.2–4.5, and the limitations in section 5.](https://arxiv.org/html/2601.23090v1) Its headline performance claim applies to the reported benchmarks and comparators; “atlas-free” does not mean free of preprocessing or representational choices.

**Before reading:** Put the numbers 1, 9, 9, 1 into a 2×2 square. Compare it with a square containing 5, 5, 5, 5. Both averages are five. List a question that the average can answer and one it cannot. Now imagine keeping all four numbers is expensive: propose a rule for deciding where detail is worth retaining.

**Reading path:** Follow a volume through selection, patches, embeddings, and downstream prediction. Separate values removed by the selection rule from values hidden only for the learning exercise. Next inspect one downstream evaluation and one ablation. Finish with the interpretation section: distinguish an attribution-map comparison from evidence that a biological mechanism has been identified.

**Three discussion questions**

1. What information can regional averaging discard, and what advantages might averaging still provide?
2. If a selection rule favors variation, how could movement or measurement noise receive extra attention? Which control would test this?
3. How would you distinguish new-session, new-person, and new-dataset generalization in the reported experiments?

**Coursework before mathematics — the representation budget.** Draw an 8×8 imaginary measurement grid. Mark one structured region, one quiet region, and one noisy region. You may retain sixteen patches: propose both a uniform allocation and an adaptive allocation. Explain what each loses and how a nuisance pattern could fool the adaptive rule. Then choose an actual task from section 4.2 and fill an evidence table with prediction target, input, baseline, split unit, adaptation, metric, and missing details. Inspect an ablation before writing a bounded performance claim. Deliver both grids, the table, and one proposed nuisance-control experiment. Your invented grid is not a reimplementation of the paper's tokenizer.

**Later notebook bridge:** [M01](../../notebooks/04_modeling/01_representations_encoding_decoding.ipynb), [M04](../../notebooks/04_modeling/04_nested_sites_harmonization.ipynb), [M16](../../notebooks/04_modeling/16_selfsupervision_transfer.ipynb), [M17](../../notebooks/04_modeling/17_attention_foundation_models.ipynb), and [M18](../../notebooks/04_modeling/18_calibration_explanation_reproducibility.ipynb). Use M17 to inspect what attention mixes, then explain which components of the paper that toy example omits. Deliver an input/output contract and a short proposed external-validation plan. The required work does not download the checkpoint or run the full model.

**Evidence-constrained AI prompt**

> Use only these PM05 excerpts and my evidence table. Trace the input through each transformation, marking any missing detail unknown. Distinguish an author performance claim, a reported comparison, and my proposed test. Do not call atlas-free preprocessing-free or turn attribution overlap into causal evidence. Quiz me about one plausible failure of my allocation rule. [Paste excerpts and table.]

**Instructor notes / answer guide:** Matching means does not preserve spatial pattern. Extra detail may help but can also preserve nuisance and increase variance. Good answers name a perturbation experiment plus independent participant/site evaluation; they do not infer these controls were performed unless cited. Table 3's SALD columns favor SwiFT over Omni-fMRI on both reported metrics: an explicit counterexample to “wins every task.” Ask the learner to check which direction is better before comparing values. The paper acknowledges heuristic selection, and attribution agreement should motivate further validation. The public repository and author checkpoint link were verified; neither was executed or downloaded. A code license was not established from the inspected repository page, so public visibility is not treated as permission to redistribute it. The assigned manuscript declares CC BY-NC-SA 4.0; we link it only.

## Assessment and return to fundamentals

Score each evidence sheet out of ten: correct prediction target and representation (2); traceable paper evidence (2); correct unit of independence (2); concrete failure test (2); restrained claim and understandable explanation (2). A polished AI summary without the cited evidence sheet does not satisfy the assignment. The learner should first explain the process aloud, then use AI to revise unclear wording.

After the relevant notebooks, revisit the same sheet in a different color. Add the actual shape of each array, identify which operation is fitted, and state where fitting stops before evaluation. Preserve the original misunderstanding and explain the correction. The final deliverable is a small portfolio of evolving explanations, not a collection of generated paper summaries.

**Orientation selections:** PM03 and PM05 are the strongest modern starting points. PM04 is the optional third reading when the orientation needs an explicit lesson in fair comparisons. PM01 and PM02 provide conceptual language for the return to fundamentals. These selections are editorial teaching choices, not a global ranking of research quality.
