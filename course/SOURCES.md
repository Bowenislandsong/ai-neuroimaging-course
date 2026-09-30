# Materials and source map

Research checked 24 September 2026, Los Angeles. The lessons, prompts, toy data, exercises, and answer keys are newly authored. References are linked where used. This pack borrows the broad curriculum structure and directs the learner to primary teaching resources; it does not redistribute a USC course, textbook, slide collection, or restricted model weights.

## What was verified at USC

The [official curriculum](https://niin.usc.edu/about#curriculum) identifies processing/workflows (540), experimental design (520), data science (580), and computational modeling (550). The [FAQ](https://niin.usc.edu/faq) describes a one-year, 26-unit program and no formal prerequisites. These facts support the blueprint, not equivalence to a master's program.

**Detailed public syllabi for these four courses were not located.** Searches used exact course names/numbers and USC's syllabus, schedule, and archive domains; some schedule endpoints were inaccessible. The four source records below document searches and limitations. No weekly USC schedule, assignment, reading list, or grading scheme has been invented. If an authorized syllabus is later obtained, it can be compared against this clearly labeled original course.

| Block | Full source record | Teaching resources selected |
| --- | --- | --- |
| 540 | [Processing ledger](sources/540.md) | NiBabel coordinates; FSL registration; SciPy filtering; Nilearn cleaning; real fMRIPrep sample report |
| 520 | [Design ledger](sources/520.md) | SPM design/contrasts; FSL exchangeability; primary pseudoreplication/circularity papers; COS preregistration |
| 580 | [Data science ledger](sources/580.md) | NumPy arrays/least squares; pandas joins; SciPy standardization/SE; scikit-learn leakage |
| 550 | [Modeling ledger](sources/550.md) | scikit-learn baselines/validation/metrics; MONAI input contract; PyTorch transfer learning; BrainSegFounder model card |

## Setup and bridge references

| Primary source | Used for | Treatment |
| --- | --- | --- |
| [Ollama quickstart](https://docs.ollama.com/quickstart) | Installation and local model operation | Link, concise independently worded setup |
| [Qwen3.6 registry](https://ollama.com/library/qwen3.6) | Verified explicit model tags and displayed download sizes | Time-sensitive facts; recheck when installing |
| [Gemma4 registry](https://ollama.com/library/gemma4) | Verified explicit model tags and displayed download sizes | Time-sensitive facts; no model weights bundled |
| [Goose quickstart](https://goose-docs.ai/docs/quickstart/) | Installation path | Link only |
| [Goose providers](https://goose-docs.ai/docs/getting-started/providers/) | Ollama connection, endpoint, tool requirement | Short setup guidance; no claim the chosen integration was tested here |
| [Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt) | Conversation/file workflow | Link and original tutoring prompt; no API app built |
| [Oxford FMRIB signal primer](https://www.fmrib.ox.ac.uk/primers/intro_primer/ExBox3/IntroBox3.html) | Contrast dependence | Link; independently chosen hypothetical tissue numbers |
| [BIDS MRI specification](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-imaging-data.html) | Timing metadata and units | Link, no copied specification |
| [Nilearn packaged template loader](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.load_mni152_template.html) | First real anatomical file exercise | Resource provided by installed package; source file not redistributed in this pack |
| [UCL/SPM auditory data](https://www.fil.ion.ucl.ac.uk/spm/data/auditory/) | Optional functional dataset provenance | External archive; no raw scans bundled |
| [Nilearn auditory fetcher](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_spm_auditory.html) | Supported data access | Documented download step, not a claimed executed download |
| [Nilearn first-level tutorial](https://nilearn.github.io/stable/auto_examples/00_tutorials/plot_single_subject_single_run.html) | Optional real fMRI workflow | Linked external teaching sequence; not copied or claimed replicated |

## What “all materials” means in this pack

Everything required for the **core teaching exercises** is local: lesson explanations, prompts, data generators, runnable examples, expected checks, output plots, answer keys, and assessment templates. External references are short assigned readings and extensions. The optional real-data exercises require their specified software/resources; downloading the auditory scans, running a full preprocessing workflow, and training an actual pretrained imaging model have not been represented as completed work.

Public access and redistribution permission are different. The source records preserve links and note reuse terms where verified. The published figures, full lectures, proprietary course files, actual participant scan archives, and pretrained checkpoints are not copied into the pack. Original scientific plots show the synthetic exercises; the template illustration is an attributed derivative used for this teaching comparison.
