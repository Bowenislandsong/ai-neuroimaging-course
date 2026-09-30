# Borrowed design-course notebooks: provenance and status

These are **unmodified upstream copies**, separate from our newly written and executed notebooks in `notebooks/02_design`. Downloaded 2026-09-25 UTC. Exact bytes and SHA-256 values are recorded in [manifest.json](manifest.json). Original outputs are historical upstream outputs, not results produced by our environment. Do not run these legacy notebooks as if they were part of the tested core course.

| File | Author/source | Pinned commit | Licence and use here |
|---|---|---|---|
| [DesignEfficiency.ipynb](fmri-analysis-vm/analysis/efficiency/DesignEfficiency.ipynb) | Russ Poldrack, [fmri-analysis-vm](https://github.com/poldrack/fmri-analysis-vm) | `d93fcf8e818c850d0a1b4e96b01ac987f27e9d34` | MIT; original [LICENSE](fmri-analysis-vm/LICENSE) preserved. Read the blockiness, correlation, AR1 and FIR sections alongside our design labs05–07/10. |
| [EfficiencyCorrelation.ipynb](fmri-analysis-vm/analysis/efficiency/EfficiencyCorrelation.ipynb) | Russ Poldrack, same source | Same commit | MIT. Short reference on predictor correlation and reciprocal-trace efficiency; our lab07 deliberately teaches **contrast-specific** efficiency rather than equating all efficiency criteria. |
| [Resampling_Statistics.ipynb](dartbrains/content/Resampling_Statistics.ipynb) | Luke Chang, [DartBrains](https://github.com/ljchang/dartbrains) | `b72537ad25deee0281248a415a052cd87ff325de` | CC BY-SA4.0. Original licence statement preserved in [intro.md](dartbrains/content/intro.md); [licence notice](dartbrains/LICENSE_NOTICE.md). Read alongside lab12. |

The original Dartmouth [Fall2022 syllabus](dartbrains/content/Syllabus.md) and [book TOC](dartbrains/_toc.yml) are preserved unmodified as evidence of course organization. They describe the original course, not current enrollment policies or the curriculum being built here. Their linked third-party readings and videos have their own rights; those linked materials are not copied by this repository.

## Important reading notes

- Poldrack's `DesignEfficiency.ipynb` contains Python2 print syntax, IPython magics, historical `nipy`/`statsmodels` dependencies, and a relative `mkdesign` helper absent from this small excerpt. Its old function definitions and runtime are not asserted to work now. It is an inspectable historical source, not a portable replacement for the new lab.
- Poldrack's `EfficiencyCorrelation.ipynb` uses IPython magic and uncontrolled random draws. Its efficiency objective is reciprocal trace of a covariance-like matrix; that is different from the precision of an arbitrary specified contrast.
- DartBrains' old resampling notebook uses deprecated `seaborn.distplot` and removed `DataFrame.append`, as well as unseeded randomness. It is not executed in our core suite. Its statement suggesting the bootstrap is generally robust to outliers should **not** be adopted: resampling can duplicate outliers and a bootstrap mean remains sensitive to them. Our lab12 explicitly teaches this limitation and finite-permutation p-value resolution.
- We considered Poldrack's `BayesianInference.ipynb` but **did not vendor it**: its prose explicitly borrows examples from other teaching sources. It remains linked in the coverage record with its provenance distinction; our Bayesian exercise is original.

No upstream notebooks, outputs, or licences were edited. No large neuroimaging datasets or commercial textbooks were copied. Keeping upstream files unmodified preserves auditability; it is not an endorsement of every historical sentence or API choice. Redistribution of the Dartmouth content retains its CC BY-SA licence and attribution, while the Poldrack files retain MIT. The repository's licence for newly authored content does not override either source licence.
