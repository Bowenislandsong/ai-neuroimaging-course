# Papers in neuroimaging processing

Begin with **PP01 and PP04** in the opening seminar, then revisit them after the corresponding notebooks. Read PP02 with motion and quality control, PP03 with tissue segmentation, PP06 with diffusion MRI, and PP05 as a fetal-imaging extension. For each paper, identify the input, transformation, output, and evidence used to evaluate the result.

The readings combine established methodological studies with recent published methods. The [source registry](processing_sources.json) records their publication dates, assigned manuscript versions, reading sections, and official code repositories.

Students read the papers at their publisher or author sites and submit original diagrams, analyses, and written interpretations.

## First meeting: a two-paper orientation, 60–75 minutes

Open fMRIPrep's **Figure 1** and BrainMorph's **Figure 1** in the original papers. Read their captions aloud. Draw your own four-box diagram for each: input → operation → output → evidence. Mark a box “I cannot yet explain this” instead of asking AI to hide the gap with terminology.

The student then answers, without equations: Which system coordinates a collection of processing operations? Which system predicts information used to align images? Where would an incorrect input assumption become visible? Compare the role of a report with the role of a learned keypoint. Make a list of three fundamentals she now wants to learn. A useful list might include coordinates, interpolation and independent validation; it need not match the instructor's list.

**Submit:** two diagrams, three learning questions, and one well-supported conclusion with a stated boundary for each paper. Ask Goose/Ollama or ChatGPT to challenge one conclusion using passages you supply. Check every paper-specific AI claim against a section. **Instructor check:** the student distinguishes a processing pipeline, a learned registration component, and the evidence supporting each.

<a id="pp01"></a>
## PP01 · fMRIPrep: why an automated pipeline still needs inspection

**Esteban et al. — *fMRIPrep: a robust preprocessing pipeline for functional MRI*. Nature Methods 16, 111–116 (2019).** Peer-reviewed; online publication 10 December 2018. [DOI: 10.1038/s41592-018-0235-4](https://doi.org/10.1038/s41592-018-0235-4) · [Author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC6319393/) · [Official code](https://github.com/nipreps/fmriprep). **Role:** essential; orientation selection.

**Motivation and evidence.** The paper connects automated, metadata-aware workflow construction with visible quality checks. Its experiment concerns preprocessing robustness and controlled comparison with another configured pipeline; it does not certify any downstream biological conclusion. The software described is historical: current behavior must be checked against the version actually used.

**Reading path, before mathematics:** Figure 1 → Results, “A modular design alongside BIDS allow for a flexible, adaptive workflow” → “Visual reports ease quality control and maximize transparency” → Figure 3 and its comparison setup. Later read “Preprocessing functional runs” and “Protocol for manual assessment.” These named sections and captions were consulted for this card.

**Discuss:**

1. If an alignment looks plausible in one slice, what additional evidence would you require before accepting it?
2. Which result could distinguish improvement in anatomical correspondence from extra blurring?
3. Why can two identical preprocessing runs still support different downstream statistical claims?

**Assignment — an audit before an analysis (90 minutes after PR21).** Use [PR21](../../notebooks/01_processing/21_workflow_provenance_reports.ipynb) and the [public sample report](https://fmriprep.org/en/stable/_static/SampleReport/sample_report.html). Record the report's actual software version; do not infer current defaults from it. Choose three checkpoints and write an input/operation/output/evidence row for each. For every row add a possible failure, the view or number that would expose it, and a decision you cannot make from the available report alone. Then use [P02](../../notebooks/05_projects/02_real_fmri_glm.ipynb) to identify two preprocessing assumptions its teaching GLM leaves unresolved. No full fMRIPrep installation is needed for this audit.

**Deliverable:** a one-page QC memo, three evidence rows, and a revised methods paragraph that distinguishes observed results from missing checks. Cite report sections; draw original diagrams rather than copying figures.

**AI prompt:** “Using only my three evidence rows, identify where my conclusion exceeds my observation. Ask one question at a time. Do not invent a preprocessing step or software version.”

**Instructor notes:** a passing submission can say “cannot determine.” Reject the inference that completion without errors proves correct processing, or that the example report supplies evidence for the student's separate dataset. Award credit for a traceable uncertainty rather than a confident guess. Extend with PR09–PR15, DS03 and DS16; reread the paper's comparison setup before transferring a numerical performance claim to a current pipeline.

<a id="pp02"></a>
## PP02 · Motion can change the story a connectivity map tells

**Power, Barnes, Snyder, Schlaggar and Petersen — *Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion*. NeuroImage 59, 2142–2154 (2012).** Peer-reviewed; online publication 14 October 2011. [DOI: 10.1016/j.neuroimage.2011.10.018](https://doi.org/10.1016/j.neuroimage.2011.10.018) · [Author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC3254728/) · [Author's paper page](https://www.jonathanpower.net/2012-ni-motion-1.html). **Role:** essential. A dedicated original-paper code repository was not verified; do not substitute an unrelated motion package and call it original code.

**Motivation and evidence.** Movement-related signal changes altered correlations after conventional correction. The paper used frame-quality measures, targeted removal and a random-removal comparison to examine this problem. It is a motivation for testing residual artifact; its historical thresholds are not universal recommendations for present-day acquisitions.

**Reading path:** Abstract → the results around Figures 1–2 → Figure 4 → Figure 5's targeted-versus-random removal comparison → Figure 9 and the discussion of regression. The full-text passages and captions associated with these analyses were consulted; no figures are reproduced here.

**Discuss:**

1. What would random removal of the same number of frames control for, and what would it leave uncontrolled?
2. How could unequal censoring across participant groups change both measurement quality and the population being studied?
3. Why does a small motion estimate not establish that a frame is artifact-free?

**Assignment — remove information on purpose (90–120 minutes after PR15).** Extend the synthetic data in [PR15](../../notebooks/01_processing/15_qc_censoring.ipynb). Generate two independent clean regional signals with a fixed seed; retain this ground truth. Add shared spikes at known frames. Compare correlations for clean, contaminated, spike-censored and count-matched randomly censored data. Repeat the random control 200 times and show its distribution. The known spike mask supplies an oracle benchmark, not a realistic artifact detector. Finally substitute PR15's observable quality rule and report how its decisions differ. Preserve original timestamps and apply each mask to both signals together.

**Deliverable:** one comparison plot, a table of retained frames and correlations, the random seed, and a 150-word account of what this toy experiment cannot establish about distance-dependent brain networks. Add a three-row participant-retention policy for a hypothetical group comparison.

**AI prompt:** “Implement one comparison at a time in cells of at most 20 lines. Preserve clean signals and acquisition times. Explain why matching the number of removed frames is a control rather than proof of unbiased censoring.”

**Instructor notes:** compare error relative to the clean correlation, not merely whether the result becomes numerically smaller. The random distribution need not have a predetermined mean; it depends on spike size and prevalence. Reject selectively rerunning seeds until a desired ordering appears. Students must separate this original shared-spike demonstration from a reproduction of the paper's spatial or developmental findings. Links forward: PR10, PR14, PR15, PR20, DS07, DS08 and P02.

<a id="pp03"></a>
## PP03 · SynthSeg: can deliberately unrealistic images teach useful anatomy?

**Billot et al. — *SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining*. Medical Image Analysis 86, 102789 (2023).** Peer-reviewed. [DOI: 10.1016/j.media.2023.102789](https://doi.org/10.1016/j.media.2023.102789) · [Full text, arXiv v3](https://arxiv.org/html/2107.09559v3) · [Publication record](https://pubmed.ncbi.nlm.nih.gov/36857946/) · [Official code](https://github.com/BBillot/SynthSeg). **Role:** essential bridge to recent segmentation papers; not labeled the newest model.

**Motivation and evidence.** SynthSeg trains from label-conditioned synthetic images with varied acquisition appearances. The paper tests robustness across contrasts and resolutions. Its Discussion explicitly identifies substantial use of automated evaluation labels as a limitation. “Without retraining” is a tested deployment property, not a guarantee of accuracy on every anatomy or scan.

**Reading path:** Figures 2–3 → Sections 3.1.2–3.1.4, following operations rather than equations → Sections 5.1–5.2 → Discussion. Those sections and their figure captions were consulted. Notice which information comes from anatomy labels and which variability is generated.

**Discuss:**

1. What information can a label-conditioned simulator vary without changing the intended tissue identity?
2. If a reference segmentation contains an error, what does agreement with that reference establish?
3. Which shift would intensity augmentation alone fail to represent?

**Assignment — a controlled failure catalog (two hours after PR06).** Use the distinction between labels and generated intensities from [PR06](../../notebooks/01_processing/06_tissue_segmentation.ipynb), adding the bias mechanism from [PR04](../../notebooks/01_processing/04_bias_field.ipynb). Create an original two-dimensional label map with three nested asymmetric regions. Construct six cases from that preserved map: baseline, contrast reversal, smooth multiplicative bias, noise, blur/downsampling, and a changed anatomical shape. For each, predict whether a fixed intensity threshold should fail and why. Test that threshold, measure class-specific overlap with the known labels, and inspect the boundaries. State whether any geometry change requires transforming labels as well. This experiment interrogates augmentation assumptions; it does **not** train or run SynthSeg.

**Deliverable:** six original image/label panels, a prediction-versus-observation table, and a proposed train/validation/test split that holds out an entire shift type. Add a separate checklist for an eventual supervised SynthSeg run: exact version, compatible input, label definitions, checkpoint provenance and independent QC evidence. Mark that run unexecuted unless performed.

**AI prompt:** “Construct only the next synthetic perturbation. State whether labels should remain fixed. Check units and class identities. Do not describe the threshold baseline as SynthSeg.”

**Instructor notes:** class permutation is not a successful segmentation simply because two masks exist. A high average overlap can hide a small structure's failure. The shape case is especially useful if its difficulty is not reduced by changing contrast. Require the student to explain both a failed and a successful baseline without claiming a universal conclusion. Connect PR04/PR06/PR07/PR12, DS03 and P01; the paper motivates studying what preprocessing can and cannot preserve.

<a id="pp04"></a>
## PP04 · BrainMorph: inspect the correspondence that drives an AI transform

**Wang, Saluja, Kim, He, Dalca and Sabuncu — *BrainMorph: A Foundational Keypoint Model for Robust and Flexible Brain MRI Registration*. Machine Learning for Biomedical Imaging (MELBA), 2025.** Peer-reviewed, published 27 May 2025; first preprint May 2024. [DOI: 10.59275/j.melba.2025-59g7](https://doi.org/10.59275/j.melba.2025-59g7) · [Full journal text](https://www.melba-journal.org/papers/2025:010.html) · [arXiv v3](https://arxiv.org/abs/2405.14019v3) · [Official code](https://github.com/alanqrwang/brainmorph). **Role:** frontier; orientation selection.

**Motivation and evidence.** Learned keypoints drive a selectable transformation and image resampling. Evaluation varies alignment difficulty and uses regional correspondence measures. The paper acknowledges weaker nonlinear performance in some already well-aligned, skull-stripped settings. These results support a conditional comparison; they do not identify a universal registration winner.

**Reading path:** Figure 1 → Figure 2 → Figures 3–5 → Sections 5.1–5.4 → Section 7, Discussion. We consulted those captions and the named methods/results, including the use of automated reference regions. Postpone Section 3's equations until PR02–PR03.

**Discuss:**

1. If predicted landmarks align perfectly, what anatomy between them could still be wrong?
2. What must be matched before comparing two registration methods' runtime or accuracy?
3. How could using another model's regional labels as an evaluation reference limit the conclusion?

**Assignment — make the correspondence error visible (two hours after PR02).** Construct six non-collinear 2D landmarks inside a synthetic asymmetric shape. Apply a known translation and rotation to create the moving points. Ask AI for a short least-squares affine fit from moving to fixed coordinates; verify the prediction on three *held-out* landmarks generated by the same known transform. Deliberately swap two training correspondences, refit, and compare training residuals, held-out location error and the affine determinant. Draw the transformed outline, not just the six fitted dots. Explain why six points constrain the fit more than the minimal three. This is a correspondence experiment, not a BrainMorph reproduction or neural-network implementation.

**Deliverable:** two overlay plots, units and transform-direction diagram, held-out error table, and a four-condition benchmark proposal crossing small/large misalignment with same/different contrast, evaluated separately in independently specified healthy and clinical populations. Record which conditions the paper actually tested and which you are proposing. Do not claim a local speed or accuracy comparison without running it.

**AI prompt:** “Fit the specified moving-to-fixed landmark map. Keep held-out landmarks out of the fit. Explain what the determinant tells us and what it cannot certify. Separate landmark estimation, transformation fitting and image resampling.”

**Instructor notes:** inspect whether homogeneous coordinates and transform direction agree; lower fitted error is insufficient. An affine map can have low error yet reflect or distort anatomy. The full BrainMorph benchmark is much richer than this lab, and learned keypoints are not established anatomical landmarks merely because they are plotted. Map to PR01–PR03, PR21, DS10 and P01. For the pre-fundamentals orientation, use only the earlier diagram comparison; the coding assignment comes later.

<a id="pp05"></a>
## PP05 · A 2026 segmentation paper where improvement has a cost

**Shang et al. — *Towards contrast- and pathology-agnostic clinical fetal brain MRI segmentation using SynthSeg*. NeuroImage 327, 121729 (2026).** Peer-reviewed journal article, issue date 15 February 2026; first preprint April 2025, revised January 2026. [DOI: 10.1016/j.neuroimage.2026.121729](https://doi.org/10.1016/j.neuroimage.2026.121729) · [arXiv v2 and journal metadata](https://arxiv.org/abs/2504.10244v2) · [Full manuscript](https://arxiv.org/pdf/2504.10244v2) · [Official code](https://github.com/ZiyaoShang/synthseg-for-clinical-fetal-brains). **Role:** frontier, focused on fetal anatomy and domain shift.

**Motivation and evidence.** The study changes training-template sampling and augmentation, then compares performance across imaging/anatomical domains. Gains on severe abnormalities can accompany losses elsewhere. Evaluation uses mixed reference-generation procedures and includes private data. This is a valuable robustness tradeoff, not evidence of superiority for all fetal pathologies or adult MRI.

**Reading path:** Figures 1–2 → Methods 2.1 → Results 3.4 → Figure 6/Table 3 → Discussion → Data and Code Availability. Those portions of arXiv v2 were read; journal status was cross-checked. Figure numbering refers to that manuscript version.

**Discuss:**

1. Why can the model with the best overall mean be the wrong choice for a proposed deployment population?
2. How would you distinguish a shape-domain shift from a change in scanner contrast?
3. Which part of a reproduction is limited when some test data cannot be obtained?

**Assignment — a benchmark whose winner changes (90 minutes after PR06 and DS07).** Create an explicitly fictional two-domain table with two candidate segmenters. Use mean Dice scores of A=0.90/B=0.87 for domain N and A=0.55/B=0.70 for domain P. These numbers are teaching inputs, **not paper results**. Plot the population-weighted mean for P prevalence from 0 to 1 and identify where the ranking reverses. Then make a study plan specifying separate domain results, a worst-domain criterion, boundary-error checks and a small expert audit. Open the real paper's Table 3 and independently record one comparison whose interpretation changes across domains; label its row/column and version instead of copying the full table.

**Deliverable:** the fictional weighting plot, the crossing point, a one-page evaluation plan and the single paper comparison with its caveat. Identify whether the proposed deployment population is adult, neonatal or fetal; justify that distinction before selecting a checkpoint.

**AI prompt:** “Use only the four fictional scores supplied. Derive the crossover in plain language and check it numerically. Do not present population weighting as a statistical significance test or invent a clinical threshold.”

**Instructor notes:** the fictional difference A−B is `0.03−0.18*p`; equality occurs at `p=1/6`. This is deterministic arithmetic, so no p-value follows. Ask what subject-level uncertainty would require and why a smaller boundary error can matter even when Dice is similar. The actual experiment has more domains, structures and ablations; the student's one-dimensional plot is a motivation, not its reconstruction. Map to PR06–PR07, PR15, DS04/DS07/DS08 and P03–P04.

<a id="pp06"></a>
## PP06 · Diffusion tractography: a plausible path is not proof of a connection

**Maier-Hein et al. — *The challenge of mapping the human connectome based on diffusion tractography*. Nature Communications 8, 1349 (2017).** Peer-reviewed, published 7 November 2017. [DOI and open full text](https://doi.org/10.1038/s41467-017-01285-x) · [2019 author-name correction](https://doi.org/10.1038/s41467-019-12867-2). **Role:** essential diffusion paper; read before PR16–PR19. The publisher lists Supplementary Software 1 and the paper's Data availability section links challenge resources; they are not downloaded or executed here. No single repository is asserted to contain all participating pipelines.

**Motivation and evidence.** A simulated challenge with known bundles revealed that recovering existing pathways can coexist with many false connections. Errors persisted when tracking used known local directions. The phantom's construction and incomplete anatomy limit generalization; the observed rates are not universal in-vivo error rates. This 2017 benchmark motivates questions, not a ranking of 2026 algorithms.

**Reading path:** Abstract → Figure 1 and dataset construction → Figure 4's distinct metrics → Figure 7's ambiguity diagrams → Figure 6 → Discussion. The relevant Results, Methods, figure captions and correction were read. First-pass readers can skip equations. The correction concerns an author's name, not the benchmark results.

**Discuss:**

1. What information about end-to-end connections can remain unknown even if local directions are measured accurately?
2. Why could a method recover more true bundles while becoming less trustworthy as a complete connectivity map?
3. What evidence would be needed to transfer a simulated benchmark's numerical error rate to a new human dataset?

**Assignment — build a connectome with the wrong edges (90 minutes, returning after PR19).** Draw four endpoint regions, A/B/C/D, and a shared central corridor. Declare two true paths in your **fictional graph**: A–B and C–D. Draw two alternative paths through the same corridor: A–D and C–B. This is a reasoning diagram; it is not an anatomical model or a diffusion simulation. Before coding, explain what additional observation could determine the correct pairings.

Create three undirected adjacency matrices: the declared truth, a liberal reconstruction containing all four paths, and a strict reconstruction retaining only A–B. Calculate edge precision and recall against your declared truth, node degrees and the number of connected components. Count each unordered edge once. Then assign 100 streamlines to A–B and one to every other retained edge. Compare binary connectivity with this arbitrary weighted graph. Explain why increasing a streamline count has not supplied new anatomical evidence.

**Deliverable:** the original corridor drawing, three labeled adjacency matrices, a metric table and a 200-word account of the competing errors. Add an evidence row for one actual Figure 4 panel: what is its unit and denominator? Distinguish bundles, individual streamlines and spatial coverage. Do not copy the paper's images or claim that the fictional graph reproduces its phantom.

**AI prompt:** “Use my explicitly declared fictional edges. Build symmetric adjacency matrices with zero diagonals and count each undirected edge once. Explain why precision, recall and connectivity answer different questions. Do not call a streamline an axon or infer pathway direction from an undirected graph.”

**Instructor notes:** liberal precision is 1/2 and recall is 1; strict precision is 1 and recall is 1/2. Truth/liberal/strict graphs have 2/1/3 connected components, respectively. Liberal reconstruction creates a connected network although truth consists of two disconnected pairs; strict reconstruction isolates two nodes. These known answers concern the invented graph only. A student's observation that both reconstruction policies can mislead is more useful than declaring one universally preferable. Revisit [PR16](../../notebooks/01_processing/16_diffusion_gradients.ipynb), [PR17](../../notebooks/01_processing/17_diffusion_preprocessing.ipynb), [PR18](../../notebooks/01_processing/18_diffusion_tensor.ipynb) and [PR19](../../notebooks/01_processing/19_crossing_fibers_tractography.ipynb) to separate gradient bookkeeping, preprocessing, local modeling and tracking. Continue with [M07](../../notebooks/04_modeling/07_connectomes_graphs.ipynb) to see why a graph statistic inherits the uncertainty of its edges.

## Assessment and reading record

For each paper retain: its exact version, one claim in your words, the evidence location, one limitation, three discussion answers and the named coursework artifact. Score each on a four-part rubric: accurate scope, traceable evidence, reproducible artifact and a limitation that changes the interpretation. A fluent abstract summary alone does not pass. Orientation artifacts are completed before the fundamentals; computational assignments are completed after their prerequisites.

The registry distinguishes bibliographic verification, sections read and code location. Official code being available does not imply that it has been installed, its checkpoint is appropriate, or its benchmark has been reproduced. Additional 2026 work was considered during the search, including [deepmriprep](https://doi.org/10.1038/s43588-026-00953-7); it is an extension reading, not an additional assessed paper in this six-paper strand.
