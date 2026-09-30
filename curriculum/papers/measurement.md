# Measurement bridge: what does BOLD measure?

<a id="pb01"></a>
## PB01 · Logothetis et al. (2001)

**Paper:** Nikos K. Logothetis, Jon Pauls, Mark Augath, Torsten Trinath and Axel Oeltermann, *Neurophysiological investigation of the basis of the fMRI signal*. Nature 412, 150–157. Peer-reviewed research article, published 12 July 2001. [Publisher and DOI](https://doi.org/10.1038/35084005) · [Public author-uploaded full text](https://www.researchgate.net/publication/11892860_Neurophysiological_Investigation_of_the_Basis_of_the_fMRI_Signal). The publisher page is a subscription preview; the inspected full-text copy was posted by coauthor Jon Pauls. Access interfaces may change. No accompanying analysis repository is assigned.

**Role:** essential measurement paper, read after the six-paper orientation and before F02/D05. This is a mechanism bridge, not a current benchmark competitor.

**Motivation in brief:** the study compares intracortical electrical measurements with simultaneous BOLD imaging in monkey visual cortex. It makes the relationship between an imaging signal and neural activity an empirical question. Different electrical summaries do not provide interchangeable accounts of the hemodynamic response. That motivates learning measurement models before interpreting a statistical map as a direct neural readout.

**First pass, 45–60 minutes:** read the abstract, inspect Figure 3 and its caption, then the Discussion. Notice the distinct observed signals and their time axes. Return later to Figure 4 and the linear-systems analysis. The author-uploaded text includes the full captions; do not rely on a secondary slide deck's panel labels.

### Coursework before equations

1. Draw three boxes: stimulus, electrical measurements, and imaging measurement. Add arrows only where you can explain what is observed or modeled. Use different line styles for a measurement relationship and a proposed mechanism.
2. For one Figure 3 panel, write what a time point and each curve represent. Locate the caption/Methods evidence before naming the units or experimental condition. State one conclusion restricted to this experiment and one tempting generalization that needs another experiment.
3. Explain the question “Can two neural processes generate similar imaging observations?” in ordinary language. Propose a measurement that could distinguish them; do not claim that the paper performed your proposed test.

**Discussion:** Why would temporal correspondence matter beyond a spatial overlay? Which assumptions are needed to transfer an observation across species, brain regions or acquisition conditions? What can an accurate prediction of BOLD establish, and what does it leave unresolved?

**AI prompt:** “Using only my supplied Figure 3 caption and excerpt, ask me which signals were measured directly. Help me label a measurement diagram. Do not tell me that BOLD universally equals firing rate or invent an experiment outside the text.”

**Return after fundamentals:** F02 measurement/contrast, DS09 signal scales, D05/D06 HRF/FIR, PR13 filtering and M01 encoding/decoding. Run the existing convolution example with two candidate inputs and explain what changed. Label it a synthetic mechanism experiment; it does not reproduce the original recordings.

**Submit:** one-page measurement diagram, one checked evidence row, three open questions, and a later 200-word correction to the first interpretation. Use the common [20-point figure-brief rubric](../coursework/PAPER_TO_EXPERIMENT.md#a1--first-pass-figure-brief).

<details><summary>Instructor notes—open after discussion</summary>

The key distinction is the measurement-to-mechanism inference. A faithful account names species, recording context and observables, and avoids treating every electrical measure as the same quantity. Accept a first-pass explanation with unresolved mathematics if it correctly separates observations from interpretations. Require the learner to locate supporting evidence, not repeat a memorized slogan about BOLD.

</details>

Source identity, abstract, Figure 3/4 captions and Discussion were inspected on 2026-09-25 UTC. Paper text and figures are linked, not redistributed; the worksheet is original course material.
