# Teaching sources and research references

Source records were checked on 25 September 2026 UTC. Materials were selected for their published course structure, sustained lesson sequences, practical exercises, and documented reuse terms. The collection includes university courses, methods workshops, and advanced tutorials.

## Program context

USC's [NIIN curriculum](https://niin.usc.edu/about#curriculum) groups relevant study into neuroimaging processing, experimental design, data science, and computational modeling. This course develops those areas through its own lessons and the published teaching materials listed below.

Course numbers in the [introductory supplement](../course/README.md) identify the corresponding subject area. The current course uses its own class IDs, assignments, and source records.

## Primary papers and research evidence

The [paper registry](papers/README.md) contains **18 guides** with exact titles, publication/version status, primary full-text locations, reading paths and assignments. The strand registries record verification and notebook mappings. These research papers motivate and challenge the methods taught here; they are distinct from the teaching curricula below. Start with six papers in three comparisons:

| Opening comparison | Essential anchor | Newer-method reading |
|---|---|---|
| Processing and alignment | [PP01: fMRIPrep](papers/processing.md#pp01) | [PP04: BrainMorph](papers/processing.md#pp04) |
| Sampling and generalization | [PD02: Marek et al.](papers/design.md#pd02) | [PM03: BrainIAC](papers/modeling.md#pm03) |
| Analysis choices and evidence | [PD01: NARPS](papers/design.md#pd01) | [PM05: Omni-fMRI](papers/modeling.md#pm05) |

Students use the assigned paper version and identify the figure or section supporting each claim. The guides record publication status and code availability. [PD02](papers/design.md#pd02) focuses on associations between people; [PD06](papers/design.md#pd06) examines how study design affects replicability. [PD05](papers/design.md#pd05) is assigned with its published correction.

Paper text and publisher figures are linked at their source. For an [A3 reconstruction](coursework/PAPER_TO_EXPERIMENT.md#a3--figure-or-table-reconstruction-proposal), students record the permissions and terms that apply to the paper, code, data, and model weights.

## University courses with inspectable schedules

| Course | Actual public evidence | Revision used and teaching role |
|---|---|---|
| Dartmouth PSYC60 / DartBrains | [Fall 2022 syllabus](https://github.com/ljchang/dartbrains/blob/b72537ad25deee0281248a415a052cd87ff325de/content/Syllabus.md), [Jupyter TOC](https://github.com/ljchang/dartbrains/blob/b72537ad25deee0281248a415a052cd87ff325de/_toc.yml), [department syllabus](https://pbs.dartmouth.edu/sites/department_psychological_brain_sciences/files/department_psychological_brain_sciences/wysiwyg/psyc_60_-_brain_mapping_with_fmri.pdf) | Legacy Jupyter commit `b72537ad25deee0281248a415a052cd87ff325de`; broad imaging/GLM/group/resampling sequence. Current Marimo material separately pinned at `5d727f7a72a7f20bfb32603cac8509d78b9647f2`. |
| Berkeley PSYCH214 Fall 2016 | [Syllabus](https://bic-berkeley.github.io/psych-214-fall-2016/syllabus.html), [classes/labs](https://bic-berkeley.github.io/psych-214-fall-2016/classes_and_labs.html), [topics](https://bic-berkeley.github.io/psych-214-fall-2016/topics.html) | `ec44652addc92091183456fa04fcd41dca0e172e`; imaging geometry, processing, regression/HRF, hypothesis tests and reproducible project work. |
| Berkeley Data 8 | [Complete textbook contents](https://inferentialthinking.com/chapters/intro.html), [source repository](https://github.com/data-8/textbook/tree/5235b7653f8dfaeb90e43419b9aa069322f2d60b) | `5235b7653f8dfaeb90e43419b9aa069322f2d60b`; arrays, tables, distributions, sampling, bootstrap, regression, Bayes and prediction. Exact chapters appear in DS notebooks. **Linked only**, CC BY-NC-ND 4.0. |
| MIT 9.07 Statistics for Brain and Cognitive Science, Fall 2016 | [Syllabus and numbered calendar](https://ocw.mit.edu/courses/9-07-statistics-for-brain-and-cognitive-science-fall-2016/pages/syllabus/) | Dated OCW course by Emery Brown; probability, estimation, likelihood, simulation, tests, regression and ANOVA. Linked only. |
| MIT 9.63 Laboratory in Visual Cognition, Fall 2009 | [Lecture-note sequence](https://ocw.mit.edu/courses/9-63-laboratory-in-visual-cognition-fall-2009/pages/lecture-notes/) | Dated OCW course by Aude Oliva; variables/controls, single-factor/factorial design and ANOVA. Linked only. |

## Open curricula and specialist practicals

| Source | Exact version / evidence | Reuse in this course |
|---|---|---|
| Neuromatch computational neuroscience | [Published schedule](https://github.com/NeuromatchAcademy/course-content/blob/44634e960df7a14cd0bf7398187f2d209d26b0e8/tutorials/Schedule/daily_schedules.md); commit `44634e960df7a14cd0bf7398187f2d209d26b0e8` | MSE/MLE, geometry, model fitting, GLMs, dimension reduction and hidden dynamics; selected original notebooks preserved. Content CC BY 4.0; code BSD 3-Clause. |
| Neuromatch deep learning | [Published schedule](https://github.com/NeuromatchAcademy/course-content-dl/blob/caba36c513fb8139ac3c9e7503f7a769dadde25e/tutorials/Schedule/daily_schedules.md); commit `caba36c513fb8139ac3c9e7503f7a769dadde25e` | Optimization, CNNs, latent/generative models, attention and self-supervision; selected CNN notebook preserved with CC BY/BSD notices. |
| BrainIAK tutorials | [Repository curriculum and course origins](https://github.com/brainiak/brainiak-tutorials/blob/fb62ede943d9694fe703aee0df5f43ecf5558415/README.md); commit `fb62ede943d9694fe703aee0df5f43ecf5558415` | Princeton/Yale course-based tutorial collection; decoding, tuning, RSA, searchlights, connectivity, ISC, SRM and HMM. RSA/ISC notebooks preserved under Apache 2.0. |
| Dartmouth/OHBM naturalistic analysis course | [Curriculum](https://github.com/naturalistic-data-analysis/naturalistic_data_analysis/blob/88bd22741508b4d678202bde7530cee0511e283f/README.md); commit `88bd22741508b4d678202bde7530cee0511e283f` | Naturalistic timing, ISC, alignment and event segmentation; linked only, content CC BY-SA 4.0. |
| Poldrack fMRI analysis education | [Repository](https://github.com/poldrack/fmri-analysis-vm/tree/d93fcf8e818c850d0a1b4e96b01ac987f27e9d34); commit `d93fcf8e818c850d0a1b4e96b01ac987f27e9d34` | Two real efficiency notebooks preserved under MIT. A teaching repository with a historical VM; **not** presented as a verified Stanford Psych254 syllabus. |
| Oxford FSL course | [Online materials](https://pages.fmrib.ox.ac.uk/fslcourse/website/online_materials.html), registration/structural/FDT practical outlines | Live university practicals inspected; assigned full-tool work, linked only. No FSL execution or dataset redistribution implied. |
| FreeSurfer workshop | [Workshop/tutorial schedule](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial) | Surface reconstruction, measurements, troubleshooting and QC; linked full-tool work. |
| DIPY | [Examples](https://docs.dipy.org/stable/examples_built/index.html); code commit `05df74a36c48e38ef1aa7420440abb9f1d14e6d4` | Exact tensor/denoising/tracking source examples assigned; code BSD 3-Clause, linked only. |
| Nipype tutorial | [Repository](https://github.com/nipy/nipype_tutorial/tree/f11c9c7b8e7a1983918f1d517ec9cf3dfcb78236); commit `f11c9c7b8e7a1983918f1d517ec9cf3dfcb78236` | Three actual BIDS/workflow/preprocessing notebooks preserved under BSD 3-Clause. |

## Documentation and real-data projects

Official NiBabel, Nilearn, SciPy, scikit-learn, BIDS, fMRIPrep, SPM, and model-author documentation support the operations and transfer tasks. Links appear in the relevant notebooks and strand maps.

P01 uses the MNI152 template shipped in the installed Nilearn package. P02 follows the educational scope of the [Nilearn single-run GLM example](https://nilearn.github.io/stable/auto_examples/00_tutorials/plot_single_subject_single_run.html), with original inspection/assessment cells and explicit omissions. Its input is the [UCL SPM auditory dataset](https://www.fil.ion.ucl.ac.uk/spm/data/auditory/), credited to Geraint Rees, Karl Friston and the FIL methods group, downloaded under the source's personal education/evaluation terms. Raw dataset files are not in this repository.

[Goose](https://goose-docs.ai/docs/getting-started/providers/), [Ollama](https://docs.ollama.com/quickstart), [Qwen3.6](https://ollama.com/library/qwen3.6), [Gemma4](https://ollama.com/library/gemma4), and [ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt) documentation informs the setup guide. Students should check current model tags and interfaces when installing.

## Attribution and version records

The four strand maps connect topics to teaching sources. [Third-party materials](../third_party/README.md) retain their source versions, licenses, and file hashes; `scripts/check_repository.py` validates the preserved files. The course's original notebooks have a separate [execution record](VERIFICATION.md).
