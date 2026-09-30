"""Execute the small offline notebook cells without opening a Jupyter server.

Run from the repository root: .venv/bin/python course/verification/verify_course.py
This records real stdout and figures, checks notebook structure and assertions,
and uses fresh namespaces for independent lessons; 540 runs sequentially. It does not test Goose,
an LLM, a Jupyter UI, or an external research pipeline.
"""
import base64
import contextlib
import io
import json
import os
import platform
import re
import tempfile
from importlib.metadata import version
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "neurocourse-matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "neurocourse-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat

ROOT = Path(__file__).resolve().parents[1]
PLOTS = ROOT / "verification" / "plots"
PLOTS.mkdir(exist_ok=True)
records = []
for path in sorted((ROOT / "labs").glob("*.ipynb")):
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    namespace = {"__name__": "__main__"}
    sections = count = plots = 0
    for cell_index, cell in enumerate(notebook.cells):
        if cell.cell_type == "markdown" and re.match(r"##\s+(?:\d{3}\.)?[1-6](?:[.\s])", cell.source):
            if not path.name.startswith("540_"):
                namespace = {"__name__": "__main__"}
            sections += 1
        if cell.cell_type != "code":
            continue
        assert len(cell.source.splitlines()) <= 20, (path.name, cell_index, "cell too long")
        captured = []
        def show(*args, **kwargs):
            global plots
            for number in plt.get_fignums():
                figure = plt.figure(number)
                buffer = io.BytesIO()
                figure.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
                png = buffer.getvalue()
                plots += 1
                (PLOTS / f"{path.stem}-{plots:02d}.png").write_bytes(png)
                captured.append(nbformat.v4.new_output(
                    "display_data", data={"image/png": base64.b64encode(png).decode()}, metadata={}))
            plt.close("all")
        plt.show = show
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            exec(compile(cell.source, f"{path.name}:cell{cell_index}", "exec"), namespace)
            if plt.get_fignums():
                show()
        count += 1
        cell.execution_count = count
        cell.outputs = ([nbformat.v4.new_output("stream", name="stdout", text=stream.getvalue())]
                        if stream.getvalue() else []) + captured
    assert sections == 6, (path.name, sections)
    notebook.metadata["course_verification"] = {
        "method": "Python exec, Agg plots; 540 sequential, other lessons independently; no Jupyter kernel sockets",
        "python": platform.python_version(), "code_cells": count, "sections": sections,
        "status": "passed all cell assertions"}
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    records.append({"notebook": path.name, "sections": sections, "code_cells": count,
                    "plots": plots, "status": "PASS"})

# Check the bridge's stated acquisition toy numbers independently.
import numpy as np
t1, t2 = np.array([800., 1400.]), np.array([80., 120.])
signal500 = (1-np.exp(-500/t1))*np.exp(-20/t2)
signal3000 = (1-np.exp(-3000/t1))*np.exp(-20/t2)
assert np.allclose(signal500, [.362, .254], atol=.0006)
assert np.allclose(signal3000, [.760, .747], atol=.0006)

# Execute the packaged anatomical-template bridge, with comparable plotting.
from nilearn.datasets import load_mni152_template
from nilearn import image, plotting
import nibabel as nib
img = load_mni152_template(resolution=2)
blurred = image.smooth_img(img, fwhm=6)
assert img.shape == blurred.shape
assert np.allclose(img.affine, blurred.affine)
assert not np.allclose(img.get_fdata(), blurred.get_fdata())
figure, axes = plt.subplots(2, 1, figsize=(10, 7))
vmin, vmax = 0., float(img.get_fdata().max())
for ax, data, label in zip(axes, [img, blurred], ["Original template", "6 mm FWHM smoothing"]):
    plotting.plot_anat(data, axes=ax, figure=figure, cut_coords=(0, -20, 10),
                       vmin=vmin, vmax=vmax, title=label)
figure.savefig(ROOT / "verification" / "real_template_demo.png", dpi=140, bbox_inches="tight")
plt.close("all")
template_record = {"shape": list(img.shape), "voxel_mm": list(map(float, img.header.get_zooms())),
                   "orientation": list(nib.aff2axcodes(img.affine)),
                   "source": "Nilearn packaged MNI152 template, resolution=2",
                   "checks": "same shape and affine, different intensities; comparable cuts and display scale"}
packages = {name: version(name) for name in ["numpy", "scipy", "matplotlib", "pandas",
            "scikit-learn", "nibabel", "nilearn", "nbformat"]}
report = {"python": platform.python_version(), "packages": packages,
          "notebooks": records, "bridge_signal_checks": "PASS", "template": template_record}
(ROOT / "verification" / "results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
