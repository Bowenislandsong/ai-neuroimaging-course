# Design papers: learn the reason for the methods first

Start each paper's first pass **before its mapped methods block**. The first encounter is a guided evidence discussion, with no prerequisite programming or equations. Read PD01 and PD02 during the course orientation; first encounter PD03–PD06 before their assigned blocks in the study plan, then return after the linked technical lessons. These are five essential methodological anchors and one newer methodological follow-up, not a list of today's best-performing models. The course's frontier-model readings ask whether newer systems solve the problems raised here.

For each first pass, allow 60–75 minutes: predict the answer to the opening question (5 minutes), inspect the assigned figure and caption (15), read the specified parts (20), prepare the coursework artifact (20), and explain it aloud (10). An unfamiliar term goes into a question list; it does not require completing a statistics textbook first. Later, budget 90–120 minutes for the linked computational assignment. These are our original assignments, not the papers' official exercises, and completing them does not replicate the published studies.

Ask Goose/Ollama or ChatGPT: **“Tutor me through this paper one figure at a time. Ask what I think its axes and observations mean before explaining. Separate the authors' result, their interpretation, and your speculation. Give a section or figure locator for every paper-specific claim. Do not invent numbers, supply my coursework answers, or claim our synthetic demonstration reproduces the paper.”** Open the full paper yourself; an AI summary is not the reading.

Every submission uses an evidence card: question; measured object; comparison; figure/section locator; supported claim; remaining uncertainty; proposed next test. Keep the paper's images on the linked publisher or author site. Submit your own diagrams and prose, without copying its PDF or figures into the public course repository. Bibliographic records, versions, access notes, and later lesson IDs are in [design_sources.json](design_sources.json).

<a id="pd01"></a>

## PD01 · Would two competent analysts reach the same conclusion?

**Botvinik-Nezer et al. (2020). _Variability in the analysis of a single neuroimaging dataset by many teams._ Nature.** Peer-reviewed research article. [DOI](https://doi.org/10.1038/s41586-020-2314-9) · [Full author-hosted paper](https://kuhllab.com/wp-content/uploads/2020/09/Botvinik-Nezer-et-al.-2020.pdf) · [PMC manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC7771346/).

**What the paper contributes.** NARPS gave the same dataset and hypotheses to multiple teams. Their analysis choices produced differing binary conclusions; similarity of underlying statistical maps did not guarantee agreement about significance. This motivates making choices inspectable, rather than treating a software output as the only possible answer.

**First reading path.** Read the abstract, Figure 1 and its caption, Figure 2 and its caption, then the results about unthresholded maps and the Discussion. Postpone the prediction-market methods and detailed image meta-analysis until the second pass.

**Evidence questions.** In Figure 1, what is being counted, and what do the prediction-market points predict? In Figure 2, can similar map values lead to different reported decisions? Identify one statement about biological truth that neither figure can establish.

**Coursework now: an analysis-decision hearing.** Invent one research question about whether a task changes a prespecified brain-region response. Draw a six-step path from scan to claim. At each step, record a choice that must be specified, what output it changes, and the evidence needed to judge it. Mark one decision that could alter the scientific question itself. Your AI may suggest candidate choices; you must reject at least one irrelevant suggestion and explain why. Submit the diagram, a 250-word evidence card using the paper, and a two-minute explanation of why voting among pipelines would not automatically establish truth.

**Coursework later.** Complete [D09: contrasts](../../notebooks/02_design/09_glm_contrasts_inference.ipynb) and [D16: analysis alternatives](../../notebooks/02_design/16_multiverse_prereg_reproducibility.ipynb). Freeze one primary specification before running four defensible alternatives. Submit the frozen plan, all four results, a table distinguishing changed estimands from changed estimators, and a conclusion that accounts for the complete table. Do not discard a branch because its result is inconvenient. This is a synthetic sensitivity exercise, not a rerun of NARPS.

**Rubric, 10 points.** Correct figure interpretation (2); traceable decision diagram (2); relevant rejected AI suggestion (2); complete alternative-results record (2); appropriately limited conclusion (2). First-pass feedback uses the first three criteria; final credit requires both passes.

**Instructor check.** Figure 1 concerns 70 reporting teams; Figure 2 uses 64 usable unthresholded maps. A fraction of teams is neither a posterior probability nor a count of independent participant replications. A good answer preserves the unknown truth and explains the distinction between a continuous map and a thresholded decision.

<a id="pd02"></a>

## PD02 · How many people make a brain–behavior association believable?

**Marek et al. (2022). _Reproducible brain-wide association studies require thousands of individuals._ Nature.** Peer-reviewed research article. [DOI and full paper](https://doi.org/10.1038/s41586-022-04492-9) · [Publisher full text](https://www.nature.com/articles/s41586-022-04492-9) · [Publisher correction](https://www.nature.com/articles/s41586-022-04692-3).

**What the paper contributes.** Across large datasets, the authors examine how between-person brain–phenotype associations vary with sample size. Small samples can produce unstable or inflated associations. The scope is BWAS: its sample-size message is not a universal rule for lesions, interventions, or within-person effects. The correction addresses publication metadata and open-access licensing.

**First reading path.** Read the abstract and the opening definition of BWAS. Inspect Figure 1, especially panels e–h, followed by Figure 3. Read the surrounding results and Discussion. On the later pass, study how the Methods define replication and errors relative to the full sample.

**Evidence questions.** Which axis in Figure 1 changes the amount of evidence? Can two small subsamples suggest different directions? In Figure 3, what operational definition counts as replication? Why is the full dataset a reference estimate rather than known biological truth?

**Coursework now: three different study proposals.** Write separate questions for an average task effect, an association across people, and prediction in new people. For each, name the independent unit, target population, outcome, and evidence that could fail. Choose which proposal is closest to this paper and explain your choice in ordinary language. Then draft a 200-word response to a collaborator who says, “This paper proves our 30-person within-person experiment is worthless.” Your response must narrow the claim without promising that the proposed experiment has adequate power. Submit the three-row proposal table, response, and one annotated figure-reading worksheet using words rather than copied graphics.

**Coursework later.** Complete [D04: power and precision](../../notebooks/02_design/04_power_precision.ipynb), then extend [DS07: sampling](../../notebooks/03_data_science/07_sampling.ipynb). Ask AI for a short simulation of two normally distributed variables with a prespecified weak correlation. Before running, fix three sample sizes, repetitions, seed, and summaries of error. Plot all sampled correlation estimates and compare an independent validation sample. Report the assumed population and uncertainty; do not present a toy normal model as the paper's empirical effect distribution or use its result as a whole-brain power calculation.

**Rubric, 10 points.** Three distinct estimands (2); correct figure axes and reference (2); scoped collaborator response (2); fixed simulation specification and complete results (2); explicit transfer limits (2).

**Instructor check.** Require a distinction between estimating an association and discovering one after searching. More observations reduce sampling error under assumptions; they do not by themselves remove selection, confounding, measurement bias, or a mismatch between sampled and target populations.

<a id="pd03"></a>

## PD03 · A task activates the brain; does it measure a stable difference between people?

**Elliott et al. (2020). _What Is the Test-Retest Reliability of Common Task-Functional MRI Measures? New Empirical Evidence and a Meta-Analysis._ Psychological Science.** Peer-reviewed empirical study and meta-analysis. [DOI](https://doi.org/10.1177/0956797620916786) · [Full study-hosted paper](https://dunedinstudy.otago.ac.nz/files/1598912609210.pdf) · [PMC manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC7370246/).

**What the paper contributes.** The authors combine a reliability meta-analysis with repeat-session task data. Their results distinguish detecting group activation from measuring dependable individual differences. The chosen reliability definition and task contrasts matter; one aggregate estimate cannot describe every possible fMRI measure.

**First reading path.** Begin with Figure 4 and its caption, then read the abstract. Look at Figure 3 to see the evidence across studies. Read the Discussion's comparison of experimental and individual-difference research. Save the ICC formula and Appendix for the second pass.

**Evidence questions.** In Figure 4, what do the warm and cool maps measure? Are their color scales and display thresholds interchangeable? What information is concealed by an uncolored voxel? What extra evidence would you need before using one person's score to make a decision?

**Coursework now: choose the instrument for the question.** A fictional lab wants both to show that a task changes average response and to rank participants by a stable trait. Specify what repeated observations would test each goal. Draw two participant-by-session sketches: one with a clear average task response but unstable rankings, another with stable rankings. These are your invented diagrams, labeled as such. Submit a one-page measurement plan naming the score, sessions, possible practice effect, missing-session rule, and uncertainty you would report. Add a paragraph explaining why a colorful activation map alone is insufficient for the second goal.

**Coursework later.** Complete [D03: reliability](../../notebooks/02_design/03_reliability_measurement.ipynb) and [D11: repeated observations](../../notebooks/02_design/11_group_hierarchy_repeated.ipynb). Independently vary person differences, session noise, and a constant session shift in the synthetic measurement model. Predict which change alters rank consistency and which alters agreement before executing. Submit before/after plots, the prediction log, and a short explanation of why simple correlation is not a complete replacement for a specified ICC model. An optional advanced extension may fit a clearly named ICC; it requires an independent reference check.

**Rubric, 10 points.** Correct map quantities and display interpretation (2); distinct measurement goals (2); defensible repeated-session plan (2); predicted versus observed changes (2); consistency/agreement distinction (2).

**Instructor check.** In Figure 4, absent ICC color means below the display cutoff, not necessarily exactly zero reliability. The paper's new-data analysis uses a consistency ICC; a uniform session shift is therefore a useful challenge question. Do not infer that strong mean effects guarantee stable rankings, or that this paper rules out every future task measure.

<a id="pd04"></a>

## PD04 · Could the analysis select the answer it later claims to discover?

**Kriegeskorte, Simmons, Bellgowan, and Baker (2009). _Circular analysis in systems neuroscience: the dangers of double dipping._ Nature Neuroscience.** Peer-reviewed methodological paper with simulations. [DOI](https://doi.org/10.1038/nn.2303) · [Full author manuscript with supplement](https://www.mrc-cbu.cam.ac.uk/personal/nikolaus.kriegeskorte/Kriegeskorte_Simmons_Bellgowan_Baker_Circular_analysis_in_systems_neuroscience_incl_supplement_author_version.pdf) · [PMC manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC2841687/).

**What the paper contributes.** Selection using noisy observations can bias a later estimate or test using dependent information. The paper demonstrates the issue for pattern classification and regional activation. Correcting a selection map for multiple comparisons does not automatically make subsequent selective estimation independent.

**First reading path.** Inspect Figure 3 before reading Example 2 on regional activation. Then examine Figure 2 and Example 1 on pattern information. Finish with Figure 4 and the policy discussion. Save the supplementary contrast-covariance details for D09.

**Evidence questions.** In Figure 3, distinguish the simulated true responses, selection comparison, and later comparison. Which arrow introduces dependence? In Figure 2, is separating classifier training from testing sufficient if feature selection has already inspected both sets?

**Coursework now: put information boundaries on a workflow.** Draw two pipelines for a fictional ROI study. In the first, highlight a region using the observed effect and report that effect from the same observations. In the second, design an independently justified selection rule and show exactly which observations may inform each step. Mark where AI is allowed to propose code and where a scientific decision must be fixed first. Submit both diagrams, a 150-word critique of the first, and a table listing what the second design gains and what it sacrifices. Merely renaming the selected data “validation” does not repair the first design.

**Coursework later.** Complete [D14: selection and circularity](../../notebooks/02_design/14_roi_selection_circularity.ipynb) and [DS15: the full null pipeline](../../notebooks/03_data_science/15_selection.ipynb). Use the provided null simulation to compare a fixed location, same-data selection, independent evaluation, and selection repeated on evaluation data. Submit all four distributions and a written trace of what information each selection used. Then inspect one AI-generated workflow and locate selection outside a validation fold. Repair the placement and explain the repair without reading the AI response. This tests a mechanism, not the original article's numerical results.

**Rubric, 10 points.** Correct distinction among the figure's comparisons (2); complete information-flow diagrams (2); defensible independence argument (2); all failure and repair results (2); oral explanation of leakage (2).

**Instructor check.** Independence concerns the relevant statistics and sampling structure. Two different filenames, nominally different contrasts, or a train/test label do not establish it. Orthogonal contrast-weight vectors alone are not a general proof of independent estimates. A prespecified anatomical ROI can avoid this selection mechanism while still leaving other threats to validity.

<a id="pd05"></a>

## PD05 · Does a corrected statistical map actually control its claimed error rate?

**Eklund, Nichols, and Knutsson (2016). _Cluster failure: Why fMRI inferences for spatial extent have inflated false-positive rates._ PNAS.** Peer-reviewed research article, with an important correction. [DOI and full publisher paper](https://doi.org/10.1073/pnas.1602413113) · [Publisher text](https://www.pnas.org/doi/10.1073/pnas.1602413113) · [Correction](https://pmc.ncbi.nlm.nih.gov/articles/PMC4995979/).

**What the paper contributes.** The authors empirically tested error control using task-free scans and imposed analysis designs. Some tested cluster procedures exceeded their nominal familywise error rate. Findings depend on the procedure and setting; permutation methods also require assumptions. The correction withdraws the broad “40,000 studies” extrapolation. The study is not a test of every current software release.

**First reading path.** Read the corrected Significance statement, Table 1, Figure 1 and its caption, then Figure 2. Read the Results subsection about the one-sample permutation test and the Discussion. Read the correction before writing any headline about the paper.

**Evidence questions.** What counts as one false-positive analysis in Figure 1? Separate the cluster-forming threshold from the final corrected threshold. Does Figure 2 evaluate the same procedure? Why must a null-data benchmark's assumptions also be examined?

**Coursework now: inspect the claim behind “corrected.”** Draft a methods checklist for an imagined map: tested family, statistic, one- or two-sided test, cluster-forming rule if any, correction procedure, independent unit, and software/version. Ask AI for a plausible incomplete methods paragraph and identify the missing decisions. Then write a corrected paragraph and a two-sentence public explanation of the paper that avoids universal claims. Submit both paragraphs, the annotated checklist, and an evidence card that distinguishes calibration of a procedure from deciding whether one particular biological result is true.

**Coursework later.** Complete [D12: exchangeability](../../notebooks/02_design/12_permutation_exchangeability.ipynb) and [D13: multiplicity and spatial enhancement](../../notebooks/02_design/13_multiplicity_clusters_tfce.ipynb). Before running, explain what an allowed rearrangement preserves. For an instructor-approved extension, repeat an entirely null synthetic experiment and record whether **any** location is declared significant in each repetition. Submit the per-experiment decisions, estimated error rate with binomial uncertainty, and an assumptions table. Compare this with counting significant locations within one experiment. Our one-dimensional exercise is not a reconstruction of the paper's software benchmark, three-dimensional random-field methods, or clinical data.

**Rubric, 10 points.** Correct denominator and threshold distinctions (2); complete methods checklist (2); scoped public explanation including correction (2); experiment-level calibration record (2); valid rearrangement and transfer limits (2).

**Instructor check.** Reject “70% of all fMRI findings are false” and “permutation is assumption-free.” The relevant familywise event is at least one false rejection in a declared family. A nominal threshold, empirical error rate, and probability that a particular finding is false are different quantities.

<a id="pd06"></a>

## PD06 · Can better sampling and repeated measurement change the sample-size problem?

**Kang et al. (2024). _Study design features increase replicability in brain-wide association studies._ Nature.** Peer-reviewed research article, published 27 November 2024. A newer methodological follow-up to PD02, **not a claim of the latest global state of the art**. [DOI and full paper](https://doi.org/10.1038/s41586-024-08260-9) · [Publisher full text](https://www.nature.com/articles/s41586-024-08260-9) · [Authors' analysis code](https://github.com/KaidiK/RESI_BWAS).

**What the paper contributes.** Sampling distributions and longitudinal model specification can alter standardized effect sizes and replicability. The results emphasize distinguishing between-person differences from within-person change. This complements PD02: design and the target association matter alongside participant count. It does not justify selecting whichever sample produces a preferred result.

**First reading path.** Read the abstract, Figure 2, Figure 5, and their captions. Read the discussion of optimal design and longitudinal interpretation. Later inspect the Methods definition of replicability and the separate between/within-person model. Here replicability is the modeled probability that two independent studies both reach significance.

**Evidence questions.** What changes across the sampling schemes in Figure 2 besides sample size? What do the two coefficient axes in Figure 5e–f represent? Is a larger standardized association necessarily a larger biological effect in the original population?

**Coursework now: a design-budget meeting.** A fictional project can afford 200 scans. Compare 200 people once, 100 people twice, and a two-stage recruitment plan that measures a covariate cheaply before selecting imaging participants. Choose a scientific question first; then state what each design can estimate, what information is missing, and what recruitment or attrition could distort. Do not choose a winner from scan count alone. Submit a one-page decision memo and an explicit statement of the population to which you intend to generalize. Add one sentence explaining why PD02 and PD06 need not disagree.

**Coursework later.** Revisit [D01: estimands](../../notebooks/02_design/01_questions_estimands_causality.ipynb), [D02: sampling](../../notebooks/02_design/02_sampling_missingness_units.ipynb), and [D11: repeated observations](../../notebooks/02_design/11_group_hierarchy_repeated.ipynb). For an original extension, hold the slope and noise in a synthetic linear relationship fixed while varying predictor spread. Compare raw slopes, correlations, and their sampling uncertainty. Predict before running. Next sketch a model with separate baseline and change variables; explain why simply adding visit rows does not estimate both effects. Submit plots, the unchanged data-generating rule, and a population-transport caveat. This does not implement the authors' RESI estimator or reproduce their participant-data analyses.

**Rubric, 10 points.** Matched question and design (2); correct figure quantities (2); transparent recruitment/target-population distinction (2); fixed simulation with uncertainty (2); separate within/between-person interpretation (2).

**Instructor check.** A change in covariate spread can change a standardized effect without changing a fixed raw slope. Enriched samples may require weighting for population summaries. Repeated observations demand a model and an estimand; they are not automatically extra independent people or a guarantee of improved replication.

## Finish with a research decision, not a reading list

After all six first passes, submit a two-page proposal for one supervised project. Include a measurement plan, an independent unit, an information-flow diagram, a declared inferential family, and a frozen primary analysis with justified alternatives. In a five-minute oral defense, the instructor introduces one unexpected change: a second visit, a new site, a different ROI selection rule, or a stricter threshold. Predict which part of the claim changes and which new evidence becomes necessary.

The final portfolio contains six evidence cards, six first-pass artifacts, the later simulation records, a prompt/correction log, and the proposal. Passing requires at least 8/10 on each completed paper assignment and correction of every unresolved independence, denominator, or source-attribution error. These are course assessment criteria, not research certification. No original paper's code or full empirical replication has been executed by adding this reading strand.
