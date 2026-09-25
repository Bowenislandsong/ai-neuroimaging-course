# Pinned upstream modeling tutorials

These are original, unmodified upstream notebook files retained as substantive reading and follow-on lab assignments. They are **not** the authored offline notebooks under `notebooks/04_modeling`, and they have **not been executed** in this course verification. Student versions may intentionally contain unfinished exercises. Their code can install packages, fetch data, or require specialist compute; read setup cells before running a separate working copy.

## Attribution and licenses

- **Neuromatch Academy and the contributors credited inside each notebook:** computational-neuroscience content at commit `44634e960df7a14cd0bf7398187f2d209d26b0e8`; deep-learning content at commit `caba36c513fb8139ac3c9e7503f7a769dadde25e`. Teaching content is CC-BY-4.0; software elements are additionally BSD-3-Clause. Complete `LICENSE.md` and `LICENSE-CODE.md` files are preserved for both repositories. The original notebooks, including author credits, figures, references, and notices, are unchanged.
- **BrainIAK tutorial authors and contributors, credited in the notebooks:** repository commit `fb62ede943d9694fe703aee0df5f43ecf5558415`, Apache-2.0. The original `LICENSE` is preserved. Its README identifies these materials as based on courses taught at Princeton and Yale. The two notebooks are unchanged.
- Dartmouth/OHBM naturalistic tutorials are linked in the course and manifest, not vendored. Their `content/` licensing is CC-BY-SA-4.0 according to the retrieved `content/Contributing.md`; that license is distinct from the licenses above.

No third-party tutorial is relicensed by a top-level license in this course repository. Upstream dataset terms and third-party assets may have additional notices: preserve those original references and inspect them before using or redistributing data.

## Four assigned originals

### M08: tutorials/06-rsa.ipynb

[Local unchanged notebook](brainiak-tutorials/tutorials/06-rsa.ipynb) · [Pinned original](https://github.com/brainiak/brainiak-tutorials/blob/fb62ede943d9694fe703aee0df5f43ecf5558415/tutorials/06-rsa.ipynb)

Read the similarity-matrix construction, condition ordering, dissimilarity, and representation-comparison sections. Trace the exact dataset and independent unit before computing your own RDM. Complete one upstream coding exercise in a separate copy and compare it with the crossvalidated-distance lab.

SHA-256: `d3fc70b62b0957d232badc4f6370a18be80e79d30171c4b244aca9e3c96ccd42`. Status: reference provided; upstream execution **not performed**.

### M10: tutorials/10-isc.ipynb

[Local unchanged notebook](brainiak-tutorials/tutorials/10-isc.ipynb) · [Pinned original](https://github.com/brainiak/brainiak-tutorials/blob/fb62ede943d9694fe703aee0df5f43ecf5558415/tutorials/10-isc.ipynb)

Read the Pieman data setup, ISC computation, inference, and ISFC sections. Identify what is averaged, how participants are excluded from their references, and which null structure is preserved. Execute only after installing the declared dependencies and obtaining the referenced data.

SHA-256: `47fd6cda4c2de2bd93b3d1311418e1c55823bd0f14e68b821289adcc72a88ce9`. Status: reference provided; upstream execution **not performed**.

### M12: tutorials/W3D3_HiddenDynamics/student/W3D3_Tutorial2.ipynb

[Local unchanged notebook](course-content/tutorials/W3D3_HiddenDynamics/student/W3D3_Tutorial2.ipynb) · [Pinned original](https://github.com/NeuromatchAcademy/course-content/blob/44634e960df7a14cd0bf7398187f2d209d26b0e8/tutorials/W3D3_HiddenDynamics/student/W3D3_Tutorial2.ipynb)

Complete the binary HMM with Gaussian measurements exercise, explaining the transition matrix and observation model. Compare its state assumptions with the separately linked BrainIAK event-segmentation model; do not conflate an arbitrary switching HMM with ordered event progression.

SHA-256: `054bdf1cfde15b2ce1d012ab64ce38d882db2adb7a15cf94aff2d9ed8169a05e`. Status: reference provided; upstream execution **not performed**.

### M14: tutorials/W2D2_Convnets/student/W2D2_Tutorial1.ipynb

[Local unchanged notebook](course-content-dl/tutorials/W2D2_Convnets/student/W2D2_Tutorial1.ipynb) · [Pinned original](https://github.com/NeuromatchAcademy/course-content-dl/blob/caba36c513fb8139ac3c9e7503f7a769dadde25e/tutorials/W2D2_Convnets/student/W2D2_Tutorial1.ipynb)

Study kernel application, convolution output size, padding, and the PyTorch CNN demonstration. Map the explicit NumPy forward/backward arrays to module calls. The optional image exercises need their original resources; no claim is made that they ran during core verification.

SHA-256: `4d9a2bb40de84b73e0142b5d3765bdfb3e7b1db3d9bdbbe1634e248cdf4fc748`. Status: reference provided; upstream execution **not performed**.

## Audit

`sources_manifest.json` records exact source commits, remote paths, hashes, and whether each file is vendored. It also records other tutorials read during curriculum construction. Only entries marked `vendored: true` should have a local path here. The authored teaching text and miniature datasets were written independently; the imported files retain the upstream license and attribution described above.
