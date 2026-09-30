# Two bridge classes before the core course

These are original introductory lessons. They provide the minimum vocabulary needed to supervise the processing and modeling exercises. They do not replace anatomy, acquisition, or research training.

## Bridge A — What an MRI number measures (60 minutes)

**Outcome:** Explain why the same tissue can have different intensities in different scans, and why a bright voxel alone is not evidence of increased neural activity.

**0–10 minutes: predict.** Imagine two photographs of one room with different lighting. Brightness can change without the objects changing. MRI contrast also depends on how the measurement is made, although the underlying physics is different. Ask the learner whether a brighter region must contain more neurons. Keep her answer to revisit.

**10–25 minutes: minimum explanation.** A voxel is a small volume represented by one stored value. Tissue may contain mixtures within that voxel. A structural image records spatial contrast; an fMRI run samples spatial volumes repeatedly. The affine connects voxel indices to physical coordinates. A filename is not enough to establish that coordinate system.

T1 is a longitudinal recovery time constant; T2 describes transverse decay from intrinsic interactions; T2* includes additional dephasing associated with field inhomogeneity. TR is a sequence repetition interval and, in ordinary single-echo volume-based fMRI, the interval used to describe volume sampling; TE is echo time. T1-weighted and T2-weighted images emphasize different contrast relationships, and are not automatically quantitative maps of T1 or T2. Standard gradient-echo BOLD imaging is sensitive to T2* effects associated with blood oxygenation. BOLD is an indirect hemodynamic measurement, with timing and other physiological influences. The duplicated “T2” in the original topic list is treated here as **T2 and T2***.

Use a deliberately simplified spin-echo-like signal expression, `S = (1-exp(-TR/T1))*exp(-TE/T2)`, with equal proton density. It illustrates contrast dependence, not a scanner simulator. It omits sequence-specific effects, flip angles, receive sensitivity, and many other influences. A gradient-echo BOLD model would require different assumptions.

**25–40 minutes: AI-guided experiment.** Ask:

> Use this simplified expression only as a teaching model. Assume hypothetical tissue A has T1=800 ms, T2=80 ms and tissue B has T1=1400 ms, T2=120 ms. Ask me to predict the effect of changing TR from 500 to 3000 ms while TE stays 20 ms. Then give at most 15 lines computing four signals. Explain the units and what the model omits. Do not label these numbers as measurements of real gray or white matter.

Reference snippet:

```python
import numpy as np
t1 = np.array([800., 1400.])  # hypothetical ms
t2 = np.array([80., 120.])
for tr in [500., 3000.]:
    signal = (1 - np.exp(-tr / t1)) * np.exp(-20. / t2)
    print(tr, signal.round(3))
```

At TR=500 ms the values are approximately `[0.362,0.254]`; at 3000 ms they are `[0.760,0.747]`. Both increase but the relative contrast changes. Repeat at TE=80 ms; the longer-T2 tissue loses signal more slowly. Plot TE from 10 to 120 ms at a fixed TR, using identical plot scales.

**40–50 minutes: break it.** Mix a TR expressed in seconds with T1 values expressed in milliseconds. Detect the nonsensical change and fix units, not plot limits. Say why this toy cannot predict a clinical diagnosis.

**50–60 minutes: explain back.** (1) Does a T1-weighted image directly report each voxel's T1 in milliseconds? **Answer:** not generally; a quantitative mapping acquisition/model is needed. (2) Can a BOLD peak be interpreted as the exact instant neurons fired? **Answer:** no; it reflects a delayed, indirect vascular response. Deliver a measurement card distinguishing tissue property, acquisition setting, and stored intensity.

**Read:** [Oxford FMRIB's signal explanation](https://www.fmrib.ox.ac.uk/primers/intro_primer/ExBox3/IntroBox3.html) and [BIDS MRI metadata](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-imaging-data.html), especially RepetitionTime/EchoTime units. Our numerical example is original and uses milliseconds consistently; BIDS timing metadata uses specified units, commonly seconds for these fields.

## Bridge B — Ask AI to teach rather than finish (60 minutes)

**Outcome:** Use the tutor contract to obtain a short, inspectable snippet and defend one result without AI assistance.

**0–10 minutes:** Complete the [setup smoke test](../SETUP.md#ten-minute-acceptance-exercise), or read the supplied notebook output if setup is not ready. Say aloud: “The model proposes code; the numerical library computes; I check whether this answers the question.” Ask for one operation at a time. A tutorial answer can sound convincing while using the wrong axis or units.

**10–20 minutes:** Learn just five coding ideas: a variable names data; a function performs an operation; a parameter chooses behavior; an array has shape and axes; an assertion checks a stated condition. A traceback is a report of a failure, not proof that the entire approach is wrong. The learner's task is to explain the calculation, not remember punctuation.

**20–40 minutes:** Copy 580.1's first code cell, run it, and change one number. Ask AI to describe the expected shape before execution. Then request:

> Explain every line of this cell using input → operation → output. Point out exactly where the axis is selected. Give me one plausible wrong version and ask me how I would detect it. Wait for my answer before explaining the fix.

Save the original and modified outputs. If the tutor provides a large script, ask it to reduce the task to the smallest operation you can check. If it claims a file was loaded, require the actual filename and reported metadata. If a source is cited, open the link and check it supports the statement.

**40–50 minutes:** Ask for an intentionally wrong answer: “Average all numbers and call that a 3D image.” The learner must reject the interpretation using the output's shape. Repeat with “the code ran, so the method is valid.” Describe a case where correct code computes the wrong quantity.

**50–60 minutes:** Close the chat and explain what happened in one minute. Deliver the [transformation card](../templates/transformation_card.md). (1) Who decides whether smoothing is appropriate for the research question? **Answer:** the researcher with methodological supervision, aided by evidence; successful AI execution does not decide it. (2) What should AI say if it has not executed a snippet? **Answer:** that it is proposed code, with checks to run, not a fabricated result.

**Passing condition:** The learner can name the inputs, operation, output, one failure, and one independent check. If not, repeat with three numbers and a mean. Do not advance merely because the notebook ran.
