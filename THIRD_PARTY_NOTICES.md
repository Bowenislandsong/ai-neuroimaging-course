# Attribution and third-party licenses

Original lesson explanations, examples and prompts were written for this course. Source curricula informed their scope; source files preserved below remain separately identifiable and unchanged. The original authors and institutions do not endorse this repository.

| Preserved material | Credit | Applicable terms and evidence |
|---|---|---|
| Nipype tutorial, three notebooks | Michael Notter and Nipype tutorial developers; retain original in-file credits | [BSD 3-Clause](third_party/processing/LICENSE.nipype_tutorial.txt); [provenance](third_party/processing/PROVENANCE.json) |
| DartBrains current preprocessing Marimo chapter | Luke Chang and DartBrains contributors, Dartmouth | [CC BY-SA 4.0](third_party/processing/LICENSE.CC-BY-SA-4.0.txt); [original declaration and hashes](third_party/processing/PROVENANCE.json) |
| DartBrains legacy resampling notebook, syllabus, TOC and introduction | Luke Chang and DartBrains contributors | [CC BY-SA declaration](third_party/design/dartbrains/LICENSE_NOTICE.md), original [introduction](third_party/design/dartbrains/content/intro.md); full text also [here](LICENSES/CC-BY-SA-4.0.txt) |
| fMRI analysis education, two efficiency notebooks | Russell A. Poldrack and repository contributors; retain all original credits | [Original MIT license](third_party/design/fmri-analysis-vm/LICENSE); [source hashes](third_party/design/manifest.json) |
| Neuromatch computational neuroscience and deep learning notebooks | Neuromatch Academy and the authors/contributors credited in each notebook | [CC BY 4.0 content](third_party/data_science/LICENSE.md), [BSD 3-Clause code](third_party/data_science/LICENSE-CODE.md); both licenses preserved for each modeling source repository |
| BrainIAK RSA and ISC notebooks | BrainIAK tutorial authors/contributors; original notebook author lists retained | [Apache 2.0](third_party/modeling/brainiak-tutorials/LICENSE); [provenance](third_party/modeling/sources_manifest.json) |

The files above are byte-for-byte source copies, with the current DartBrains file renamed locally. SHA-256 manifests identify the original commits and paths. No claim is made that historical outputs were produced in this project. Some upstream notebooks reference remote media or exercise helpers that are not included in this partial copy.

**Linked only:** Berkeley Data 8's textbook carries CC BY-NC-ND 4.0; its chapters are assigned through original links, not copied or adapted into this repository. Berkeley PSYCH214, MIT OCW, Oxford FSL, FreeSurfer, DIPY, naturalistic-data-analysis and other documentation retain their original terms. Public availability is not treated as blanket permission to mirror material.

**Datasets and models:** the UCL SPM auditory dataset is fetched for personal educational/evaluation use under its source terms and is not committed. The MNI152 template is loaded from the Nilearn installation, with its upstream provenance; it is not added as a raw dataset to the repository. Data and model-weight licenses are distinct from notebook/software licenses. No Ollama model, imaging foundation-model checkpoint, private scan, credential or virtual environment is distributed here.

**Changes and reuse:** new surrounding teaching text identifies its source assignments and its scope. If modifying the preserved files, make a separate copy, retain attribution/license notices, indicate changes and follow the applicable license, including ShareAlike where relevant. This notice describes the publication choices made for this course; it is not a claim that all external content can be reused under the root license.

## Anatomical-template visualizations

P01 and the earlier template demonstration visualize Nilearn's rescaled/skullstripped ICBM152 nonlinear 2009a asymmetric template. Credit the McConnell Brain Imaging Centre, Montreal Neurological Institute, McGill University, and Fonov et al. [2011](https://doi.org/10.1016/j.neuroimage.2010.07.033) and [2009](https://doi.org/10.1016/S1053-8119(09)70884-5). The source [atlas page and permission terms](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009) apply to that material and its displayed derivatives; the repository does not claim ownership or replace those terms. Required source copyright notice: Copyright (C) 1993–2004 Louis Collins, McConnell Brain Imaging Centre, Montreal Neurological Institute, McGill University.
