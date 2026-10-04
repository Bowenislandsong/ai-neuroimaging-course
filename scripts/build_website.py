#!/usr/bin/env python3
"""Build the complete static GitHub Pages website for Neuroimaging Research Methods with AI."""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlsplit, unquote

import markdown

from equation_decomposer import render_equation_with_breakdown_html
from site_theme import SITE_CSS, SITE_JS, render_pipeline_svg
from course_site import build_academic_pages, build_lecture_decks
from site_discovery import add_site_discovery

ROOT = Path(__file__).resolve().parents[1]

STRAND_LABELS = {
    "00_paper_orientation": ("R", "Paper Orientation Seminars (R00–R03)"),
    "00_foundations": ("F", "Foundations & MR Physics (F01–F04)"),
    "01_processing": ("PR", "Image Processing & Pipelines (PR01–PR21)"),
    "02_design": ("D", "Research Design & Inference (D01–D16)"),
    "03_data_science": ("DS", "Data Science & Computing (DS01–DS16)"),
    "04_modeling": ("M", "Computational Modeling & AI (M01–M18)"),
    "05_projects": ("P", "Capstone Projects (P01–P04)"),
}

NIPYPE_UPSTREAM_BASE = "https://github.com/nipy/nipype_tutorial/blob/f11c9c7b8e7a1983918f1d517ec9cf3dfcb78236/notebooks/"


def slugify(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text)
    clean = html.unescape(clean)
    clean = re.sub(r"[^\w\s-]", "", clean).strip().lower()
    return re.sub(r"[-\s]+", "-", clean) or "section"


def rewrite_href(href: str, current_rel_dir: str) -> str:
    """Rewrite relative .md and .ipynb links to their generated .html pages."""
    href = href.strip()
    u = urlsplit(href)
    if u.scheme or u.netloc or href.startswith("#") or href.startswith("mailto:") or href.startswith("data:"):
        return href
    path_part = u.path
    frag = f"#{u.fragment}" if u.fragment else ""
    base_dir = (ROOT / current_rel_dir).resolve() if current_rel_dir else ROOT
    resolved = (base_dir / unquote(path_part)).resolve()

    # Handle relative links in unedited upstream Nipype tutorials that point to unvendored upstream notebooks
    if not resolved.exists() and current_rel_dir.startswith("third_party/processing"):
        return NIPYPE_UPSTREAM_BASE + Path(unquote(path_part)).name + frag

    if path_part.endswith(".md"):
        path_part = path_part[:-3] + ".html"
    elif path_part.endswith(".ipynb") and not u.query:
        path_part = path_part[:-6] + ".html"
    return path_part + frag


def render_inline_md(text: str, current_rel_dir: str = "") -> str:
    """Convert a single inline Markdown string (headings/summaries) to HTML."""
    rendered, _, _ = render_markdown_to_html(text, current_rel_dir, 1, decompose_equations=False)
    rendered = rendered.strip()
    if rendered.startswith("<p>") and rendered.endswith("</p>") and rendered.count("<p>") == 1:
        rendered = rendered[3:-4]
    return rendered


def render_markdown_to_html(
    md_text: str,
    current_rel_dir: str = "",
    eq_counter_start: int = 1,
    decompose_equations: bool = True,
):
    """Convert full Markdown text into semantic HTML using Python-Markdown with Math/Code/Callout stashing."""
    toc: list[tuple[int, str, str]] = []
    used_ids: dict[str, int] = {}
    eq_counter = [eq_counter_start]

    # 1. Transform special comment callout markers into wrapper divs
    md_text = re.sub(
        r"<!--\s*gate\s*-->(.*?)<!--\s*/gate\s*-->",
        lambda m: f'\n\n<div class="gate-box">\n\n{m.group(1).strip()}\n\n</div>\n\n',
        md_text,
        flags=re.S,
    )
    md_text = re.sub(
        r"<!--\s*key-references\s*-->(.*?)<!--\s*/key-references\s*-->",
        lambda m: f'\n\n<div class="key-ref-box">\n\n{m.group(1).strip()}\n\n</div>\n\n',
        md_text,
        flags=re.S,
    )
    if "<!-- agentic-guide -->" in md_text:
        parts = md_text.split("<!-- agentic-guide -->", 1)
        md_text = f'{parts[0]}\n\n<div class="agentic-box">\n\n{parts[1].strip()}\n\n</div>\n\n'

    stash: list[str] = []

    def put(html_fragment: str) -> str:
        idx = len(stash)
        stash.append(html_fragment)
        return f"ZXQSTASH{idx}ENDZXQ"

    # 2. Stash fenced code blocks ```lang ... ```
    def repl_code_block(m: re.Match) -> str:
        lang = (m.group(1) or "").strip() or "code"
        code = m.group(2)
        block_html = (
            f'<div class="code-block-wrap">'
            f'<div class="code-header"><span>{html.escape(lang)}</span>'
            f'<button type="button" class="copy-btn">Copy</button></div>'
            f'<pre><code>{html.escape(code)}</code></pre>'
            f'</div>'
        )
        return "\n\n" + put(block_html) + "\n\n"

    md_text = re.sub(r"```([^\n`]*)\n(.*?)```", repl_code_block, md_text, flags=re.S)

    # 3. Stash display math $$ ... $$
    def repl_display_math(m: re.Match) -> str:
        tex = m.group(1).strip()
        idx = eq_counter[0]
        eq_counter[0] += 1
        if decompose_equations:
            eq_html = render_equation_with_breakdown_html(tex, idx)
        else:
            eq_html = f'<div class="equation-card"><div class="equation-display">\\[{html.escape(tex, quote=False)}\\]</div></div>'
        return "\n\n" + put(eq_html) + "\n\n"

    md_text = re.sub(r"\$\$(.*?)\$\$", repl_display_math, md_text, flags=re.S)

    # 4. Stash inline code ``...`` and `...`
    md_text = re.sub(
        r"``([^`\n]+?)``",
        lambda m: put(f"<code>{html.escape(m.group(1))}</code>"),
        md_text,
    )
    md_text = re.sub(
        r"`([^`\n]+?)`",
        lambda m: put(f"<code>{html.escape(m.group(1))}</code>"),
        md_text,
    )

    # 5. Stash inline math $...$ (prevents '|' or '*' or '_' inside math from colliding with tables/emphasis)
    md_text = re.sub(
        r"(?<!\$)\$(?!\$)([^\$\n]+?)(?<!\$)\$(?!\$)",
        lambda m: put(f"\\({html.escape(m.group(1), quote=False)}\\)"),
        md_text,
    )

    # 6. Stash explicit HTML anchor tags <a id="..."></a>
    md_text = re.sub(
        r'<a\s+id="([^"]+)"\s*>\s*</a>',
        lambda m: put(f'<a id="{html.escape(m.group(1))}"></a>'),
        md_text,
    )

    # 7. Stash callout wrapper divs and collapsible <details><summary>...</summary>...</details>
    for div_tag in ('<div class="gate-box">', '<div class="key-ref-box">', '<div class="agentic-box">', "</div>"):
        md_text = md_text.replace(div_tag, "\n\n" + put(div_tag) + "\n\n")

    def repl_details_summary(m: re.Match) -> str:
        raw_sum = m.group(1).strip()
        # Clean any <font> wrapper in summary
        raw_sum = re.sub(r"</?font[^>]*>", "", raw_sum)
        return "\n\n" + put(f'<details class="instructor-details"><summary>🎓 {raw_sum}</summary><div class="details-body">') + "\n\n"

    md_text = re.sub(
        r"<details>\s*<summary>(.*?)</summary>",
        repl_details_summary,
        md_text,
        flags=re.S,
    )
    md_text = re.sub(r"</details>", lambda m: "\n\n" + put("</div></details>") + "\n\n", md_text)

    # 8. Normalize 2-3 space indented sub-lists to 4 spaces so Python-Markdown nests them cleanly
    md_text = re.sub(r"(?m)^ {2,3}([-*+]\s+|\d+\.\s+)", r"    \1", md_text)

    # 9. Ensure blank lines before top-level lists, tables, and blockquotes
    lines = md_text.splitlines()
    norm_lines: list[str] = []
    for i, line in enumerate(lines):
        s = line.strip()
        prev = norm_lines[-1].strip() if norm_lines else ""
        is_top_list = bool(re.match(r"^(?:[-*+]|\d+\.)\s+", line))
        is_table_hdr = ("|" in s and i + 1 < len(lines) and bool(re.match(r"^\s*\|?[\s:-]+\|[\s|:-]*$", lines[i + 1])))
        if is_top_list and prev and not re.match(r"^\s*(?:[-*+]|\d+\.)\s+", norm_lines[-1]) and not prev.startswith((">", "#")):
            norm_lines.append("")
        elif is_table_hdr and prev and "|" not in prev:
            norm_lines.append("")
        norm_lines.append(line)
    md_text = "\n".join(norm_lines)

    # 10. Render Markdown via Python-Markdown
    rendered = markdown.markdown(md_text, extensions=["tables", "sane_lists"])

    # 11. Restore stashed tokens (in reverse order so nested tokens inside summaries resolve)
    for i in range(len(stash) - 1, -1, -1):
        rendered = rendered.replace(f"ZXQSTASH{i}ENDZXQ", stash[i])

    # Remove <p> wrappers around block-level stashed elements
    rendered = re.sub(r"<p>\s*(<(?:div|pre|details|/div|/details)\b[^>]*>)\s*</p>", r"\1", rendered)

    # 12. Add unique anchor IDs to headings and populate TOC
    def repl_heading(m: re.Match) -> str:
        level = int(m.group(1))
        inner = m.group(2)
        base_id = slugify(inner)
        count = used_ids.get(base_id, 0)
        used_ids[base_id] = count + 1
        hid = base_id if count == 0 else f"{base_id}-{count}"
        if level in (2, 3):
            clean_label = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
            toc.append((level, hid, clean_label))
        return f'<h{level} id="{hid}">{inner}</h{level}>'

    rendered = re.sub(r"<h([1-6])>(.*?)</h\1>", repl_heading, rendered, flags=re.S)

    # 13. Wrap standard Markdown tables in <div class="table-scroll">
    rendered = re.sub(
        r"<table>",
        '<div class="table-scroll"><table>',
        rendered,
    )
    rendered = re.sub(
        r"</table>(?!\s*</div>)",
        "</table></div>",
        rendered,
    )

    # 14. Rewrite relative hrefs on <a> tags and add external target attributes
    def repl_a_tag(m: re.Match) -> str:
        before = m.group(1)
        raw_href = html.unescape(m.group(2))
        after = m.group(3)
        new_href = rewrite_href(raw_href, current_rel_dir)
        ext = ""
        if new_href.startswith(("http://", "https://")) and "target=" not in before and "target=" not in after:
            ext = ' target="_blank" rel="noopener"'
        return f'<a{before}href="{html.escape(new_href, quote=True)}"{after}{ext}>'

    rendered = re.sub(r'<a(\s+[^>]*?)href="([^"]+)"([^>]*)>', repl_a_tag, rendered)

    return rendered, toc, eq_counter[0]


def build_sidebar_html(
    records: list[dict],
    enrichment: dict,
    root_prefix: str,
    current_cid: str | None = None,
    current_rel_path: str = "",
) -> str:
    """Render the 3-tab left sidebar: 26-Week Study Path, By Strand, and All Repo Docs."""
    # 1. Chronological grouped by Phase
    by_chrono = sorted(records, key=lambda r: enrichment[r["id"]]["chronological_order"])
    phases: dict[str, list[dict]] = {}
    for r in by_chrono:
        ph = enrichment[r["id"]]["phase"]
        phases.setdefault(ph, []).append(r)

    chrono_groups = [
        f'<div class="nav-group"><div class="nav-group-title">Step 0 · macOS Dev &amp; AI Setup</div>'
        f'<ul class="nav-list">'
        f'<li class="nav-item"><a href="{root_prefix}curriculum/SETUP.html" class="{"current" if current_rel_path == "curriculum/SETUP.md" else ""}">'
        f'<span class="nav-cid">MAC</span><span>Apple Dev + Ollama &amp; Goose</span><span class="nav-week-tag">Wk 0</span></a></li>'
        f'<li class="nav-item"><a href="{root_prefix}curriculum/ALL_MATERIALS.html" class="{"current" if current_rel_path == "curriculum/ALL_MATERIALS.html" else ""}">'
        f'<span class="nav-cid">ALL</span><span>All 250 Repo Materials</span><span class="nav-week-tag">Index</span></a></li>'
        f'</ul></div>'
    ]
    for ph_title, items in phases.items():
        lis = []
        for r in items:
            cid = r["id"]
            info = enrichment[cid]
            href = root_prefix + r["path"][:-6] + ".html"
            cls = ' class="current"' if cid == current_cid else ""
            lis.append(
                f'<li class="nav-item"><a href="{href}"{cls}>'
                f'<span class="nav-cid">{cid}</span>'
                f'<span>{html.escape(r["title"])}</span>'
                f'<span class="nav-week-tag">W{info["week"]}</span>'
                f'</a></li>'
            )
        chrono_groups.append(
            f'<div class="nav-group">'
            f'<div class="nav-group-title">{html.escape(ph_title)}</div>'
            f'<ul class="nav-list">{"".join(lis)}</ul>'
            f'</div>'
        )

    # 2. Strand grouped by Subject Strand
    by_strand: dict[str, list[dict]] = {}
    for r in records:
        by_strand.setdefault(Path(r["path"]).parts[1], []).append(r)

    strand_groups = [
        f'<div class="nav-group"><div class="nav-group-title">Step 0 · macOS Dev &amp; AI Setup</div>'
        f'<ul class="nav-list"><li class="nav-item"><a href="{root_prefix}curriculum/SETUP.html">'
        f'<span class="nav-cid">MAC</span><span>Apple Dev + Ollama &amp; Goose</span><span class="nav-week-tag">Wk 0</span></a></li></ul></div>'
    ]
    for strand_key, (short_code, strand_title) in STRAND_LABELS.items():
        items = by_strand.get(strand_key, [])
        lis = []
        for r in items:
            cid = r["id"]
            info = enrichment[cid]
            href = root_prefix + r["path"][:-6] + ".html"
            cls = ' class="current"' if cid == current_cid else ""
            lis.append(
                f'<li class="nav-item"><a href="{href}"{cls}>'
                f'<span class="nav-cid">{cid}</span>'
                f'<span>{html.escape(r["title"])}</span>'
                f'<span class="nav-week-tag">#{info["chronological_order"]}</span>'
                f'</a></li>'
            )
        strand_groups.append(
            f'<div class="nav-group">'
            f'<div class="nav-group-title">{html.escape(strand_title)}</div>'
            f'<ul class="nav-list">{"".join(lis)}</ul>'
            f'</div>'
        )

    # 3. Complete Repository Documents, Supplement Labs & Third-Party Tutorials
    repo_doc_sections = [
        ("Complete Repository Index", [
            ("ALL", "All 250 Repository Materials", "curriculum/ALL_MATERIALS.html"),
            ("EQS", "Equation & Diagram Atlas (83)", "curriculum/EQUATION_ATLAS.html"),
            ("README", "Course Overview (README)", "README.html"),
        ]),
        ("Curriculum & Coursework Guides", [
            ("SETUP", "Step 0: macOS Apple Dev + AI", "curriculum/SETUP.html"),
            ("PLAN", "26-Week Study Plan", "curriculum/STUDY_PLAN.html"),
            ("AI", "Agentic AI Supervision Guide", "curriculum/AI_WORKFLOW.html"),
            ("IDX", "83-Class Notebook Index", "curriculum/NOTEBOOK_INDEX.html"),
            ("RUBRIC", "Assessment & Grading Rubrics", "curriculum/ASSESSMENT.html"),
            ("LEDGER", "Paper Evidence Ledger", "curriculum/coursework/EVIDENCE_LEDGER.html"),
            ("A1-A4", "Paper-to-Experiment Projects", "curriculum/coursework/PAPER_TO_EXPERIMENT.html"),
            ("SOTA", "SOTA Model Audit Worksheet", "curriculum/coursework/SOTA_AUDIT.html"),
            ("AUDIT", "Curriculum Coverage Audit", "curriculum/COVERAGE_AUDIT.html"),
            ("SRC", "University Teaching Sources", "curriculum/SOURCES.html"),
            ("VERIF", "83-Notebook Verification Log", "curriculum/VERIFICATION.html"),
        ]),
        ("24 Papers & 310 Citations", [
            ("LIB", "24-Paper Library Overview", "curriculum/papers/README.html"),
            ("3PASS", "Three-Pass Reading Method", "curriculum/papers/READING_METHOD.html"),
            ("310REF", "All 310 Verified References", "curriculum/papers/REFERENCES.html"),
            ("PB01", "Measurement & BOLD Physics", "curriculum/papers/measurement.html"),
            ("PP01-08", "Processing Papers (fMRIPrep–BrainMorph)", "curriculum/papers/processing.html"),
            ("PD01-07", "Design & Generalization Papers", "curriculum/papers/design.html"),
            ("PM01-08", "Modeling & Foundation AI Papers", "curriculum/papers/modeling.html"),
        ]),
        ("Strand Coverage Ledgers", [
            ("COV-PR", "Processing Coverage (PR01–PR21)", "curriculum/processing_coverage.html"),
            ("COV-D", "Design Coverage (D01–D16)", "curriculum/design_coverage.html"),
            ("COV-DS", "Data Science Coverage (DS01–DS16)", "curriculum/data_science_coverage.html"),
            ("COV-M", "Modeling Coverage (M01–M18)", "curriculum/modeling_coverage.html"),
        ]),
        ("Introductory Coursebook & Labs (course/)", [
            ("BOOK", "Unified Introductory Coursebook", "course/COURSEBOOK.html"),
            ("LAB520", "Lab 520: Experimental Design", "course/labs/520_design.html"),
            ("LAB540", "Lab 540: Image Processing", "course/labs/540_processing.html"),
            ("LAB550", "Lab 550: Modeling & ML", "course/labs/550_modeling.html"),
            ("LAB580", "Lab 580: Data Science", "course/labs/580_data_science.html"),
            ("GLOSS", "Neuroimaging Glossary", "course/GLOSSARY.html"),
            ("XFORM", "Transformation Contracts", "course/TRANSFORMATIONS.html"),
            ("REAL", "Real fMRI Data Guide", "course/REAL_DATA.html"),
            ("PLOTS", "Verification Report & 22 Plots", "course/verification/REPORT.html"),
        ]),
        ("Pinned Upstream Tutorials (third_party/)", [
            ("3P-ALL", "Third-Party Provenance Overview", "third_party/README.html"),
            ("3P-PR", "Nipype & DartBrains Processing (4)", "third_party/processing/README.html"),
            ("3P-D", "Poldrack & DartBrains Design (3)", "third_party/design/README.html"),
            ("3P-DS", "Neuromatch Data Science (3)", "third_party/data_science/README.html"),
            ("3P-M", "BrainIAK & Neuromatch Modeling (4)", "third_party/modeling/README.html"),
            ("NOTICES", "Complete Third-Party Notices", "THIRD_PARTY_NOTICES.html"),
        ]),
    ]
    repo_groups = []
    for sec_title, links in repo_doc_sections:
        lis = []
        for code, label, target_html in links:
            cls = ' class="current"' if current_rel_path.replace(".md", ".html").replace(".ipynb", ".html") == target_html else ""
            lis.append(
                f'<li class="nav-item"><a href="{root_prefix}{target_html}"{cls}>'
                f'<span class="nav-cid">{html.escape(code)}</span>'
                f'<span>{html.escape(label)}</span>'
                f'</a></li>'
            )
        repo_groups.append(
            f'<div class="nav-group"><div class="nav-group-title">{html.escape(sec_title)}</div>'
            f'<ul class="nav-list">{"".join(lis)}</ul></div>'
        )

    return f"""
    <aside class="sidebar-left" aria-label="Course and Repository Navigation">
      <input type="search" id="sidebar-filter-input" class="sidebar-search" placeholder="Filter 83 classes &amp; docs (press /)..." aria-label="Filter classes and documents">
      <div class="sidebar-mode-tabs" role="tablist">
        <button type="button" class="sidebar-mode-btn active" data-mode="chronological">26-Week Path</button>
        <button type="button" class="sidebar-mode-btn" data-mode="strand">By Strand</button>
        <button type="button" class="sidebar-mode-btn" data-mode="repodocs">Repo Docs</button>
      </div>
      <div class="sidebar-nav-panel" data-panel="chronological">
        {"".join(chrono_groups)}
      </div>
      <div class="sidebar-nav-panel" data-panel="strand" style="display:none">
        {"".join(strand_groups)}
      </div>
      <div class="sidebar-nav-panel" data-panel="repodocs" style="display:none">
        {"".join(repo_groups)}
      </div>
    </aside>
    """


def wrap_page_html(
    title: str,
    main_html: str,
    sidebar_html: str,
    toc: list[tuple[int, str, str]],
    root_prefix: str,
    active_top: str = "",
) -> str:
    """Wrap page content in the master HTML5 shell with KaTeX, Google Fonts, Topbar, Reader Controls, and Lightbox."""
    toc_items = []
    for level, hid, label in toc:
        sub_cls = ' class="toc-sub"' if level == 3 else ""
        toc_items.append(f'<li{sub_cls}><a href="#{hid}">{html.escape(label)}</a></li>')

    right_sidebar = ""
    shell_cls = "page-shell"
    if toc_items:
        right_sidebar = (
            f'<aside class="sidebar-right" aria-label="On this page">'
            f'<h3>On This Page</h3>'
            f'<ul class="toc-list">{"".join(toc_items)}</ul>'
            f'</aside>'
        )
    else:
        shell_cls = "page-shell wide-shell"

    def nav_cls(key: str) -> str:
        return ' class="active"' if active_top == key else ""

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · Neuroimaging Research Methods with AI</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,400&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <link rel="stylesheet" href="{root_prefix}assets/site.css">
  <link rel="stylesheet" href="{root_prefix}assets/reader.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{root_prefix}index.html">
      <span class="brand-badge">NEURO+AI</span>
      <span>Neuroimaging Research Methods with AI</span>
    </a>
    <nav class="top-links" aria-label="Primary Navigation">
      <a href="{root_prefix}index.html"{nav_cls("home")}>Overview</a>
      <a href="{root_prefix}curriculum/SYLLABUS.html">Syllabus</a>
      <a href="{root_prefix}schedule.html"{nav_cls("plan")}>Schedule</a>
      <a href="{root_prefix}lectures.html"{nav_cls("classes")}>Lectures &amp; slides</a>
      <a href="{root_prefix}curriculum/papers/README.html"{nav_cls("papers")}>Readings</a>
      <a href="{root_prefix}assignments.html">Assignments</a>
      <a href="{root_prefix}curriculum/SETUP.html"{nav_cls("setup")}>Setup</a>
    </nav>
    <div class="reader-controls" aria-label="Reading Comfort Controls">
      <button type="button" id="eq-logic-toggle-btn" class="ctrl-btn active" title="Expand or collapse all inline equation logic breakdown tables">∑ Logic: Expanded</button>
      <button type="button" id="focus-mode-btn" class="ctrl-btn" title="Toggle distraction-free wide reading mode">⇄ Focus Width</button>
      <button type="button" id="theme-cycle-btn" class="ctrl-btn" title="Switch reading theme (Light / Warm Sepia / Dark)">☀ Light</button>
    </div>
  </header>

  <div class="{shell_cls}">
    <button type="button" class="mobile-nav-toggle" id="mobile-nav-toggle" aria-expanded="false">
      <span>☰ Browse 83 Classes, 26-Week Path &amp; Repo Docs</span>
      <span class="mobile-toggle-hint" style="font-family:var(--font-mono);font-size:0.76rem">Show ▾</span>
    </button>
    {sidebar_html}
    <main class="main-content" id="top">
      {main_html}
    </main>
    {right_sidebar}
  </div>

  <div class="lightbox-overlay" id="img-lightbox" role="dialog" aria-label="Zoomed figure view">
    <img id="img-lightbox-target" src="" alt="Enlarged scientific diagram">
  </div>

  <footer class="site-footer">
    <div>
      <strong>Neuroimaging Research Methods with AI</strong> · Independent open course.
      Lecture slides, research readings and reproducible notebook experiments.
    </div>
    <div>
      <a href="{root_prefix}curriculum/ALL_MATERIALS.html">All materials</a> ·
      <a href="{root_prefix}curriculum/SETUP.html">Setup</a> ·
      <a href="{root_prefix}curriculum/EQUATION_ATLAS.html">Equation Atlas</a> ·
      <a href="{root_prefix}course/COURSEBOOK.html">Compact Coursebook</a> ·
      <a href="{root_prefix}THIRD_PARTY_NOTICES.html">Licenses &amp; Provenance</a>
    </div>
  </footer>

  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters: [{{left: '\\\\[', right: '\\\\]', display: true}}, {{left: '\\\\(', right: '\\\\)', display: false}}], throwOnError: false}});"></script>
  <script defer src="{root_prefix}assets/site.js"></script>
</body>
</html>
"""


def render_notebook_cells(nb: dict, current_rel_dir: str, label_prefix: str) -> tuple[list[str], list[tuple[int, str, str]], int]:
    """Render all markdown and code cells of a Jupyter notebook into HTML sections + TOC."""
    toc: list[tuple[int, str, str]] = []
    cell_sections: list[str] = []
    eq_counter = 1
    code_step = 0

    for idx, cell in enumerate(nb.get("cells", [])):
        src = "".join(cell.get("source", [])) if isinstance(cell.get("source"), list) else cell.get("source", "")
        if cell.get("cell_type") == "markdown":
            if idx == 0:
                lines = src.splitlines()
                if lines and lines[0].startswith("# "):
                    src = "\n".join(lines[1:]).lstrip()
            md_html, cell_toc, eq_counter = render_markdown_to_html(src, current_rel_dir, eq_counter, decompose_equations=True)
            toc.extend(cell_toc)
            cell_sections.append(f'<section class="nb-cell" id="cell-{idx}">{md_html}</section>')
        elif cell.get("cell_type") == "code":
            code_step += 1
            outs_html = []
            for o in cell.get("outputs", []):
                otype = o.get("output_type")
                if otype == "stream":
                    if o.get("name") == "stderr":
                        continue
                    txt = "".join(o.get("text", [])) if isinstance(o.get("text"), list) else o.get("text", "")
                    if txt.strip():
                        outs_html.append(f'<div class="cell-output-stream"><pre>{html.escape(txt)}</pre></div>')
                elif otype in ("display_data", "execute_result"):
                    data = o.get("data", {})
                    if "image/png" in data:
                        b64 = ("".join(data["image/png"]) if isinstance(data["image/png"], list) else data["image/png"]).strip()
                        outs_html.append(
                            f'<figure class="cell-output-figure">'
                            f'<img src="data:image/png;base64,{b64}" alt="{html.escape(label_prefix)} diagnostic plot step {code_step}" loading="lazy">'
                            f'<figcaption>Executed diagnostic figure · {html.escape(label_prefix)} Step {code_step} (click figure to zoom)</figcaption>'
                            f'</figure>'
                        )
                    elif "text/plain" in data and otype == "execute_result":
                        txt = "".join(data["text/plain"]) if isinstance(data["text/plain"], list) else data["text/plain"]
                        if txt.strip() and not txt.strip().startswith("<Figure"):
                            outs_html.append(f'<div class="cell-output-stream"><pre>{html.escape(txt)}</pre></div>')
            cell_sections.append(
                f'<section class="nb-cell" id="cell-{idx}">'
                f'<div class="code-block-wrap">'
                f'<div class="code-header"><span>Python · Executable Cell {code_step}</span><button type="button" class="copy-btn">Copy Code</button></div>'
                f'<pre><code>{html.escape(src)}</code></pre>'
                f'</div>'
                f'{"".join(outs_html)}'
                f'</section>'
            )
    return cell_sections, toc, code_step


def build_notebook_page(
    record: dict,
    all_records: list[dict],
    by_chrono: list[dict],
    enrichment: dict,
    papers_by_id: dict,
    out_dir: Path,
):
    """Render one of the 83 main classes into an enriched HTML page."""
    cid = record["id"]
    info = enrichment[cid]
    rel_ipynb = record["path"]
    nb_path = ROOT / rel_ipynb
    nb = json.loads(nb_path.read_text())

    current_rel_dir = str(Path(rel_ipynb).parent)
    depth = len(Path(rel_ipynb).parent.parts)
    root_prefix = "../" * depth

    # Also copy the raw .ipynb file so the "Download .ipynb" button works
    dst_ipynb = out_dir / rel_ipynb
    dst_ipynb.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(nb_path, dst_ipynb)

    diag = info["online_diagram"]
    eq_info = info["equation"]
    pipeline_svg = render_pipeline_svg(info["pipeline_steps"], cid)

    paper_pills = []
    for pid in record.get("paper_ids", []):
        p = papers_by_id.get(pid)
        if p:
            p_href = root_prefix + "curriculum/papers/" + p["guide"].replace(".md", ".html")
            paper_pills.append(
                f'<a class="btn-action" href="{p_href}" title="{html.escape(p["title"])}">'
                f'{pid} · Reading guide ({p["year"]})</a>'
            )

    master_rows = []
    for t in eq_info["terms"]:
        master_rows.append(
            f'<tr>'
            f'<td class="eq-term-cell">\\({html.escape(t["term"], quote=False)}\\)</td>'
            f'<td><span class="eq-role-badge">{html.escape(t["role"])}</span></td>'
            f'<td>{html.escape(t["meaning"])}</td>'
            f'<td class="eq-failure-cell">{html.escape(t["failure"])}</td>'
            f'</tr>'
        )

    toc: list[tuple[int, str, str]] = [
        (2, "concept-diagram-showcase", "Scientific Concept Diagram & Pipeline"),
        (2, "master-equation-anatomy", f"Equation Logic: {eq_info['name']}"),
    ]
    cell_sections, cell_toc, _ = render_notebook_cells(nb, current_rel_dir, cid)
    toc.extend(cell_toc)

    c_idx = next(i for i, r in enumerate(by_chrono) if r["id"] == cid)
    prev_r = by_chrono[c_idx - 1] if c_idx > 0 else None
    next_r = by_chrono[c_idx + 1] if c_idx + 1 < len(by_chrono) else None

    prev_html = (
        f'<a class="prev-next-card" href="{root_prefix}{prev_r["path"][:-6]}.html">'
        f'<span class="prev-next-label">← Previous in 26-Week Study Path (Week {enrichment[prev_r["id"]]["week"]})</span>'
        f'<span class="prev-next-title">{prev_r["id"]} · {html.escape(prev_r["title"])}</span></a>'
        if prev_r
        else f'<a class="prev-next-card" href="{root_prefix}curriculum/SETUP.html">'
             f'<span class="prev-next-label">← Before Class 1</span>'
             f'<span class="prev-next-title">Step 0 · macOS (MacBook Pro) Dev &amp; AI Setup</span></a>'
    )
    next_html = (
        f'<a class="prev-next-card" href="{root_prefix}{next_r["path"][:-6]}.html" style="text-align:right">'
        f'<span class="prev-next-label">Next in 26-Week Study Path (Week {enrichment[next_r["id"]]["week"]}) →</span>'
        f'<span class="prev-next-title">{next_r["id"]} · {html.escape(next_r["title"])}</span></a>'
        if next_r
        else f'<a class="prev-next-card" href="{root_prefix}curriculum/EQUATION_ATLAS.html" style="text-align:right">'
             f'<span class="prev-next-label">Course Complete →</span>'
             f'<span class="prev-next-title">Review the Complete Equation &amp; Diagram Atlas</span></a>'
    )

    main_html = f"""
    <section class="class-banner">
      <div class="badge-row">
        <span class="badge badge-primary">{cid} · Class #{info['chronological_order']} of 83</span>
        <span class="badge badge-week">Week {info['week']} of 26</span>
        <span class="badge badge-phase">{html.escape(info['phase'])}</span>
        <span class="badge badge-tier">Execution tier: {html.escape(record['execution_tier'])}</span>
      </div>
      <h1>{cid} · {html.escape(record['title'])}</h1>
      <div class="banner-actions">
        <a class="btn-action primary" href="{root_prefix}slides/{cid}.html">Lecture slides</a>
        <a class="btn-action primary" href="{Path(rel_ipynb).name}" download>⬇ Download Notebook (.ipynb)</a>
        <a class="btn-action" href="#master-equation-anatomy">∑ Jump to Equation Logic Breakdown</a>
        <a class="btn-action" href="#concept-diagram-showcase">◫ Scientific Concept Diagram</a>
        {"".join(paper_pills)}
      </div>
    </section>

    <section class="concept-showcase" id="concept-diagram-showcase">
      <div class="section-eyebrow">Visual Concept &amp; Transformation Architecture</div>
      <h2>{html.escape(diag['title'])}</h2>
      <div class="concept-grid">
        <figure class="commons-figure">
          <img src="{html.escape(diag['image_url'])}" data-fullsrc="{html.escape(diag['original_url'])}" alt="{html.escape(diag['title'])}" loading="lazy" referrerpolicy="no-referrer">
          <figcaption class="commons-caption">
            <strong>Existing Scientific Diagram:</strong> <a href="{html.escape(diag['source_page'])}" target="_blank" rel="noopener">{html.escape(diag['commons_title'].replace('File:', ''))}</a>
            · Wikimedia Commons ({html.escape(diag['license'])}). Click diagram to enlarge.
          </figcaption>
        </figure>
        <div>
          <div class="diagram-guide-box" style="margin-bottom:0">
            <strong>How to read this scientific diagram &amp; connect it to {cid}:</strong><br>
            {html.escape(diag['guide'])}
            <div style="margin-top:0.75rem;padding-top:0.65rem;border-top:1px solid var(--line);font-size:0.86rem;color:var(--ink-secondary)">
              <strong>Governing Formulation Preview:</strong> {html.escape(eq_info['name'])} — {html.escape(eq_info['summary'])}
            </div>
          </div>
        </div>
      </div>
      <div class="section-eyebrow" style="margin-top:1.15rem">5-Stage Transformation Pipeline for {cid} (Input → Operator → Invariant Audit)</div>
      <div class="pipeline-svg-wrap">
        {pipeline_svg}
      </div>
    </section>

    <section class="master-equation-card" id="master-equation-anatomy">
      <div class="section-eyebrow">Governing Mathematical Formulation &amp; Term-by-Term Logic</div>
      <h2>{html.escape(eq_info['name'])}</h2>
      <p style="margin:0.35rem 0 0.75rem;color:var(--ink-secondary)">{html.escape(eq_info['summary'])}</p>
      <div class="master-eq-box">
        \\[{html.escape(eq_info['latex'], quote=False)}\\]
      </div>
      <div class="table-scroll">
        <table class="eq-breakdown-table">
          <thead>
            <tr>
              <th>Logical Term</th>
              <th>Role in Equation</th>
              <th>What This Part Is Doing (Mechanism &amp; Units)</th>
              <th>What Breaks If Omitted or Mis-Specified (Failure Mode)</th>
            </tr>
          </thead>
          <tbody>
            {"".join(master_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <article class="content-card">
      {"".join(cell_sections)}
    </article>

    <nav class="prev-next-grid" aria-label="Lesson Pagination">
      {prev_html}
      {next_html}
    </nav>
    """

    sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_cid=cid, current_rel_path=rel_ipynb)
    full_html = wrap_page_html(
        f"{cid} · {record['title']}",
        main_html,
        sidebar_html,
        toc,
        root_prefix,
        active_top="classes",
    )
    dst_html = out_dir / (rel_ipynb[:-6] + ".html")
    dst_html.parent.mkdir(parents=True, exist_ok=True)
    dst_html.write_text(full_html)


def build_extra_notebook_pages(all_records: list[dict], enrichment: dict, out_dir: Path):
    """Render the 4 course/labs/*.ipynb supplement notebooks and 13 third_party/**/*.ipynb upstream notebooks as styled HTML pages."""
    extra_nbs = sorted(list((ROOT / "course" / "labs").glob("*.ipynb")) + list((ROOT / "third_party").rglob("*.ipynb")))
    for nb_path in extra_nbs:
        rel_path = nb_path.relative_to(ROOT).as_posix()
        current_rel_dir = str(Path(rel_path).parent)
        depth = len(Path(rel_path).parent.parts)
        root_prefix = "../" * depth

        nb = json.loads(nb_path.read_text())
        title = nb_path.stem
        for c in nb.get("cells", []):
            if c.get("cell_type") == "markdown":
                src = "".join(c.get("source", []))
                for line in src.splitlines():
                    if line.startswith("#"):
                        title = re.sub(r"^#+\s*", "", line).strip()
                        title = re.sub(r"<[^>]+>", "", title).strip()
                        break
                if title != nb_path.stem:
                    break

        is_third_party = rel_path.startswith("third_party/")
        badge_label = "Pinned Upstream University Tutorial" if is_third_party else "Introductory Bridge Supplement Lab"
        provenance_note = (
            "This is a byte-for-byte preserved upstream teaching notebook from an external university curriculum (retained under its original open license; see <a href=\""
            + root_prefix
            + "THIRD_PARTY_NOTICES.html\">Third-Party Notices</a> and the folder README). Rendered below for convenient reading on the web alongside the downloadable original <code>.ipynb</code>."
            if is_third_party
            else "Executed introductory bridge companion lab from <code>course/labs/</code>, linking core Python array/table/plotting concepts to the 83-lesson graduate curriculum."
        )

        # Find nearest ancestor README.md
        cur_p = nb_path.parent
        readme_rel = "README.html"
        while cur_p != ROOT:
            if (cur_p / "README.md").exists():
                readme_rel = root_prefix + (cur_p / "README.html").relative_to(ROOT).as_posix()
                break
            cur_p = cur_p.parent

        cell_sections, toc, code_count = render_notebook_cells(nb, current_rel_dir, nb_path.stem)
        main_html = f"""
        <section class="class-banner">
          <div class="badge-row">
            <span class="badge badge-primary">{html.escape(badge_label)}</span>
            <span class="badge badge-phase"><code>{html.escape(rel_path)}</code></span>
            <span class="badge badge-tier">{len(nb.get('cells', []))} cells ({code_count} code cells)</span>
          </div>
          <h1>{html.escape(title)}</h1>
          <p style="margin:0.4rem 0 0.8rem;color:var(--ink-secondary);max-width:80ch">{provenance_note}</p>
          <div class="banner-actions">
            <a class="btn-action primary" href="{nb_path.name}" download>⬇ Download Original Notebook ({html.escape(nb_path.name)})</a>
            <a class="btn-action" href="{readme_rel}">📖 Folder Overview &amp; Provenance</a>
            <a class="btn-action" href="{root_prefix}curriculum/ALL_MATERIALS.html">🗂 All Repository Materials</a>
          </div>
        </section>
        <article class="content-card">
          {"".join(cell_sections)}
        </article>
        """
        sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path=rel_path)
        full_html = wrap_page_html(title, main_html, sidebar_html, toc, root_prefix, active_top="materials")
        dst_html = out_dir / (rel_path[:-6] + ".html")
        dst_html.parent.mkdir(parents=True, exist_ok=True)
        dst_html.write_text(full_html)

    # Also build an HTML reading companion for third_party/processing/DartBrains_Preprocessing.py
    py_path = ROOT / "third_party/processing/DartBrains_Preprocessing.py"
    if py_path.exists():
        rel_path = py_path.relative_to(ROOT).as_posix()
        root_prefix = "../../"
        code_src = py_path.read_text()
        main_html = f"""
        <section class="class-banner">
          <div class="badge-row">
            <span class="badge badge-primary">Pinned Upstream Marimo Chapter</span>
            <span class="badge badge-phase"><code>{html.escape(rel_path)}</code></span>
            <span class="badge badge-tier">CC BY-SA 4.0 · Luke Chang &amp; DartBrains</span>
          </div>
          <h1>DartBrains Preprocessing Chapter (Marimo <code>.py</code> Notebook)</h1>
          <p style="margin:0.4rem 0 0.8rem;color:var(--ink-secondary);max-width:80ch">
            Unmodified upstream Dartmouth <em>DartBrains</em> preprocessing chapter in reactive Marimo format, preserved alongside <a href="README.html">third_party/processing/README</a>.
          </p>
          <div class="banner-actions">
            <a class="btn-action primary" href="DartBrains_Preprocessing.py" download>⬇ Download Original DartBrains_Preprocessing.py</a>
            <a class="btn-action" href="README.html">← Back to Processing Upstream Materials</a>
          </div>
        </section>
        <article class="content-card">
          <div class="code-block-wrap">
            <div class="code-header"><span>Python · third_party/processing/DartBrains_Preprocessing.py</span><button type="button" class="copy-btn">Copy Code</button></div>
            <pre><code>{html.escape(code_src)}</code></pre>
          </div>
        </article>
        """
        sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path=rel_path)
        full_html = wrap_page_html("DartBrains Preprocessing (Marimo)", main_html, sidebar_html, [], root_prefix, active_top="materials")
        (out_dir / "third_party/processing/DartBrains_Preprocessing.html").write_text(full_html)


def build_coursebook_combined_page(all_records: list[dict], enrichment: dict, out_dir: Path):
    """Build course/COURSEBOOK.html containing both COURSEBOOK.md and the 22 unified course/ chapters with #doc-... anchors."""
    course_docs = [
        "README.md", "SETUP.md", "lessons/00_bridge.md", "lessons/580.md",
        "lessons/540.md", "lessons/520.md", "lessons/550.md", "lessons/90_capstone.md",
        "REAL_DATA.md", "TRANSFORMATIONS.md", "GLOSSARY.md", "ASSESSMENT.md", "verification/REPORT.md",
        "templates/transformation_card.md", "templates/analysis_record.md",
        "templates/project_plan.md", "answer_keys/520.md", "SOURCES.md",
        "sources/580.md", "sources/540.md", "sources/520.md", "sources/550.md",
    ]
    root_prefix = "../"
    intro_md = (ROOT / "course/COURSEBOOK.md").read_text()
    intro_html, toc, eq_counter = render_markdown_to_html(intro_md, "course", 1, decompose_equations=True)

    chapters_html = [f'<article class="content-card">{intro_html}</article>']
    for rel_doc in course_docs:
        doc_path = ROOT / "course" / rel_doc
        if not doc_path.exists():
            continue
        doc_id = "doc-" + re.sub(r"[^a-z0-9]+", "-", rel_doc.lower()).strip("-")
        raw_md = doc_path.read_text()
        ch_html, ch_toc, eq_counter = render_markdown_to_html(raw_md, str(( Path("course") / rel_doc ).parent), eq_counter, decompose_equations=True)
        # Re-Adjust links relative to course/ directory since COURSEBOOK.html lives in course/
        sub_dir = Path(rel_doc).parent.as_posix()
        if sub_dir != ".":
            ch_html = re.sub(
                r'href="(?!http|#|mailto:)([^"]+)"',
                lambda m: f'href="{(Path(sub_dir) / m.group(1)).as_posix()}"' if not m.group(1).startswith("../") else f'href="{m.group(1)[3:]}"',
                ch_html,
            )
        toc.append((2, doc_id, f"Coursebook: {rel_doc[:-3]}"))
        chapters_html.append(
            f'<article class="content-card" id="{doc_id}">'
            f'<div class="section-eyebrow">Coursebook Chapter · <code>course/{html.escape(rel_doc)}</code> · <a href="{rel_doc[:-3]}.html">Open Standalone Page</a></div>'
            f'{ch_html}'
            f'</article>'
        )

    sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path="course/COURSEBOOK.md")
    full_html = wrap_page_html(
        "Complete Introductory Bridge Coursebook (22 Chapters)",
        "".join(chapters_html),
        sidebar_html,
        toc,
        root_prefix,
        active_top="materials",
    )
    (out_dir / "course/COURSEBOOK.html").write_text(full_html)


def build_all_materials_page(all_records: list[dict], by_chrono: list[dict], enrichment: dict, out_dir: Path):
    """Build curriculum/ALL_MATERIALS.html cataloging all 250 tracked repository files and visual verification plots."""
    root_prefix = "../"
    tracked = sorted(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())

    # 1. Verification Plots Gallery from course/verification/
    plot_files = [f for f in tracked if f.endswith(".png")]
    plot_cards = []
    for pf in plot_files:
        plot_cards.append(
            f'<figure class="commons-figure" style="margin:0">'
            f'<img src="{root_prefix}{html.escape(pf)}" alt="{html.escape(Path(pf).name)}" loading="lazy" style="max-height:180px">'
            f'<figcaption class="commons-caption"><code>{html.escape(pf)}</code><br><a href="{root_prefix}{html.escape(pf)}" target="_blank">Open full PNG</a></figcaption>'
            f'</figure>'
        )

    # 2. Group all 250 tracked files by repository directory
    groups = [
        ("1. Main Graduate Curriculum Notebooks & Strand Indexes (`notebooks/` — 83 Classes + 5 Indexes)", [f for f in tracked if f.startswith("notebooks/")]),
        ("2. Curriculum Guides, Coursework Rubrics, Paper Library & Validation Records (`curriculum/`)", [f for f in tracked if f.startswith("curriculum/")]),
        ("3. Introductory Bridge Coursebook, Lessons, 4 Supplement Labs, Templates & 22 Verification Plots (`course/`)", [f for f in tracked if f.startswith("course/")]),
        ("4. Pinned Upstream University Tutorials & Provenance Records (`third_party/`)", [f for f in tracked if f.startswith("third_party/")]),
        ("5. Build/Verification Scripts, Root Documentation, Licenses & Environment Lockfiles", [f for f in tracked if not f.startswith(("notebooks/", "curriculum/", "course/", "third_party/"))]),
    ]

    toc: list[tuple[int, str, str]] = [
        (2, "Complete-Repository-Overview", "Repository Inventory Summary"),
        (2, "Supplement-Labs-and-Upstream-Notebooks", "Supplement Labs & 14 Upstream Tutorials"),
        (2, "Verification-Plot-Gallery", "22 Executed Verification Diagnostic Plots"),
    ]

    group_sections = []
    for idx, (g_title, files) in enumerate(groups, 1):
        gid = f"repo-group-{idx}"
        toc.append((2, gid, g_title.split("(")[0].strip()))
        rows = []
        for f in files:
            p = Path(f)
            web_link = ""
            if f.endswith((".md", ".ipynb")) or f == "third_party/processing/DartBrains_Preprocessing.py":
                html_rel = p.with_suffix(".html").as_posix()
                web_link = f'<a class="btn-action primary" style="padding:0.2rem 0.55rem;font-size:0.74rem" href="{root_prefix}{html.escape(html_rel)}">📖 Read Web Page</a>'
            elif f.endswith(".html"):
                web_link = f'<a class="btn-action primary" style="padding:0.2rem 0.55rem;font-size:0.74rem" href="{root_prefix}{html.escape(f)}">📖 Open HTML</a>'
            elif f.endswith(".png"):
                web_link = f'<a class="btn-action" style="padding:0.2rem 0.55rem;font-size:0.74rem" href="{root_prefix}{html.escape(f)}" target="_blank">🖼 View Plot</a>'

            raw_link = f'<a class="btn-action" style="padding:0.2rem 0.55rem;font-size:0.74rem" href="{root_prefix}{html.escape(f)}" target="_blank">⬇ Raw ({html.escape(p.suffix or p.name)})</a>'
            size_kb = (ROOT / f).stat().st_size / 1024.0
            rows.append(
                f'<tr>'
                f'<td><code>{html.escape(f)}</code></td>'
                f'<td>{html.escape(p.suffix or "file")}</td>'
                f'<td style="font-family:var(--font-mono);font-size:0.78rem">{size_kb:.1f} KB</td>'
                f'<td style="display:flex;gap:0.4rem;flex-wrap:wrap">{web_link} {raw_link}</td>'
                f'</tr>'
            )
        group_sections.append(
            f'<section class="content-card" id="{gid}">'
            f'<h2>{html.escape(g_title)} ({len(files)} files)</h2>'
            f'<div class="table-scroll"><table>'
            f'<thead><tr><th>Repository Path</th><th>Type</th><th>Size</th><th>Web View &amp; Raw File Access</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            f'</table></div>'
            f'</section>'
        )

    main_html = f"""
    <section class="class-banner" id="Complete-Repository-Overview">
      <div class="badge-row">
        <span class="badge badge-primary">100% Repository Coverage</span>
        <span class="badge badge-week">{len(tracked)} Git-Tracked Files + Enrichments</span>
        <span class="badge badge-tier">100 Jupyter Notebooks · 61 Markdown Docs · 28 JSON Registries · 22 PNG Plots</span>
      </div>
      <h1>Complete Repository Materials &amp; File Explorer</h1>
      <p style="margin:0.4rem 0 0;color:var(--ink-secondary);max-width:82ch">
        Every single file in the <code>ai-neuroimaging-course</code> repository is included in this static website. All <strong>100 Jupyter notebooks</strong> (83 main graduate lessons, 4 introductory supplement labs, and 13 pinned upstream university tutorials), all <strong>61 Markdown documents</strong>, and the Marimo chapter are rendered as styled, readable web pages with KaTeX math and Equation Logic Breakdowns, alongside direct links to the raw files.
      </p>
    </section>

    <section class="content-card" id="Supplement-Labs-and-Upstream-Notebooks">
      <div class="section-eyebrow">Beyond the 83 Main Classes</div>
      <h2>4 Introductory Bridge Labs &amp; 14 Pinned Upstream University Tutorials</h2>
      <p>In addition to the 83 main classes (<a href="NOTEBOOK_INDEX.html">R00–P04</a>), the repository includes 4 executed introductory supplement labs (<code>course/labs/</code>) and 14 unmodified upstream tutorials from Dartmouth DartBrains, Stanford/Poldrack <code>fmri-analysis-vm</code>, Princeton/Yale BrainIAK, Neuromatch Academy, and Nipype (<code>third_party/</code>)—all rendered into readable web pages:</p>
      <div class="table-scroll">
        <table>
          <thead>
            <tr><th>Collection</th><th>Notebook / Tutorial</th><th>Source / Role</th><th>Read on Website</th><th>Download Raw</th></tr>
          </thead>
          <tbody>
            <tr><td><code>course/labs</code></td><td><strong>Lab 520: Experimental Design &amp; GLM</strong></td><td>Introductory Bridge Companion Lab</td><td><a href="../course/labs/520_design.html">📖 Read Web Page</a></td><td><a href="../course/labs/520_design.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>course/labs</code></td><td><strong>Lab 540: Image Processing &amp; Coordinates</strong></td><td>Introductory Bridge Companion Lab</td><td><a href="../course/labs/540_processing.html">📖 Read Web Page</a></td><td><a href="../course/labs/540_processing.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>course/labs</code></td><td><strong>Lab 550: Predictive Modeling &amp; Validation</strong></td><td>Introductory Bridge Companion Lab</td><td><a href="../course/labs/550_modeling.html">📖 Read Web Page</a></td><td><a href="../course/labs/550_modeling.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>course/labs</code></td><td><strong>Lab 580: Neuroimaging Data Science</strong></td><td>Introductory Bridge Companion Lab</td><td><a href="../course/labs/580_data_science.html">📖 Read Web Page</a></td><td><a href="../course/labs/580_data_science.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/processing</code></td><td><strong>Nipype: Basic Workflow</strong></td><td>Michael Notter &amp; Nipype Tutorial (BSD-3)</td><td><a href="../third_party/processing/basic_workflow.html">📖 Read Web Page</a></td><td><a href="../third_party/processing/basic_workflow.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/processing</code></td><td><strong>Nipype: Basic Data Input (BIDS)</strong></td><td>Michael Notter &amp; Nipype Tutorial (BSD-3)</td><td><a href="../third_party/processing/basic_data_input_bids.html">📖 Read Web Page</a></td><td><a href="../third_party/processing/basic_data_input_bids.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/processing</code></td><td><strong>Nipype: Example Preprocessing Workflow</strong></td><td>Michael Notter &amp; Nipype Tutorial (BSD-3)</td><td><a href="../third_party/processing/example_preprocessing.html">📖 Read Web Page</a></td><td><a href="../third_party/processing/example_preprocessing.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/processing</code></td><td><strong>DartBrains: Preprocessing (Marimo .py)</strong></td><td>Luke Chang &amp; DartBrains (CC BY-SA 4.0)</td><td><a href="../third_party/processing/DartBrains_Preprocessing.html">📖 Read Web Page</a></td><td><a href="../third_party/processing/DartBrains_Preprocessing.py" download>⬇ .py</a></td></tr>
            <tr><td><code>third_party/design</code></td><td><strong>Design Efficiency</strong></td><td>Russ Poldrack · fmri-analysis-vm (MIT)</td><td><a href="../third_party/design/fmri-analysis-vm/analysis/efficiency/DesignEfficiency.html">📖 Read Web Page</a></td><td><a href="../third_party/design/fmri-analysis-vm/analysis/efficiency/DesignEfficiency.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/design</code></td><td><strong>Efficiency &amp; Predictor Correlation</strong></td><td>Russ Poldrack · fmri-analysis-vm (MIT)</td><td><a href="../third_party/design/fmri-analysis-vm/analysis/efficiency/EfficiencyCorrelation.html">📖 Read Web Page</a></td><td><a href="../third_party/design/fmri-analysis-vm/analysis/efficiency/EfficiencyCorrelation.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/design</code></td><td><strong>Resampling Statistics</strong></td><td>Luke Chang · DartBrains (CC BY-SA 4.0)</td><td><a href="../third_party/design/dartbrains/content/Resampling_Statistics.html">📖 Read Web Page</a></td><td><a href="../third_party/design/dartbrains/content/Resampling_Statistics.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/data_science</code></td><td><strong>W1D2 Tutorial 1: Linear Regression &amp; MSE</strong></td><td>Neuromatch Academy (CC-BY 4.0 / BSD-3)</td><td><a href="../third_party/data_science/W1D2_Tutorial1.html">📖 Read Web Page</a></td><td><a href="../third_party/data_science/W1D2_Tutorial1.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/data_science</code></td><td><strong>W1D2 Tutorial 2: Multiple Regression &amp; CV</strong></td><td>Neuromatch Academy (CC-BY 4.0 / BSD-3)</td><td><a href="../third_party/data_science/W1D2_Tutorial2.html">📖 Read Web Page</a></td><td><a href="../third_party/data_science/W1D2_Tutorial2.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/data_science</code></td><td><strong>W1D4 Tutorial 1: Dimensionality Reduction &amp; PCA</strong></td><td>Neuromatch Academy (CC-BY 4.0 / BSD-3)</td><td><a href="../third_party/data_science/W1D4_Tutorial1.html">📖 Read Web Page</a></td><td><a href="../third_party/data_science/W1D4_Tutorial1.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/modeling</code></td><td><strong>BrainIAK Tutorial 06: Representational Similarity Analysis (RSA)</strong></td><td>BrainIAK Princeton/Yale (Apache-2.0)</td><td><a href="../third_party/modeling/brainiak-tutorials/tutorials/06-rsa.html">📖 Read Web Page</a></td><td><a href="../third_party/modeling/brainiak-tutorials/tutorials/06-rsa.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/modeling</code></td><td><strong>BrainIAK Tutorial 10: Inter-Subject Correlation (ISC &amp; ISFC)</strong></td><td>BrainIAK Princeton/Yale (Apache-2.0)</td><td><a href="../third_party/modeling/brainiak-tutorials/tutorials/10-isc.html">📖 Read Web Page</a></td><td><a href="../third_party/modeling/brainiak-tutorials/tutorials/10-isc.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/modeling</code></td><td><strong>W3D3 Tutorial 2: Hidden Markov Models (HMM)</strong></td><td>Neuromatch Academy (CC-BY 4.0 / BSD-3)</td><td><a href="../third_party/modeling/course-content/tutorials/W3D3_HiddenDynamics/student/W3D3_Tutorial2.html">📖 Read Web Page</a></td><td><a href="../third_party/modeling/course-content/tutorials/W3D3_HiddenDynamics/student/W3D3_Tutorial2.ipynb" download>⬇ .ipynb</a></td></tr>
            <tr><td><code>third_party/modeling</code></td><td><strong>W2D2 Tutorial 1: Convolutional Neural Networks (CNNs)</strong></td><td>Neuromatch Academy Deep Learning (CC-BY 4.0)</td><td><a href="../third_party/modeling/course-content-dl/tutorials/W2D2_Convnets/student/W2D2_Tutorial1.html">📖 Read Web Page</a></td><td><a href="../third_party/modeling/course-content-dl/tutorials/W2D2_Convnets/student/W2D2_Tutorial1.ipynb" download>⬇ .ipynb</a></td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="content-card" id="Verification-Plot-Gallery">
      <div class="section-eyebrow">Visual Verification Suite (<code>course/verification/</code>)</div>
      <h2>All 22 Executed Supplement Verification Diagnostic Figures</h2>
      <p>Click any figure below to enlarge it in the interactive lightbox (or view the <a href="../course/verification/REPORT.html">Verification Report</a>):</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem">
        {"".join(plot_cards)}
      </div>
    </section>

    {"".join(group_sections)}
    """

    sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path="curriculum/ALL_MATERIALS.html")
    full_html = wrap_page_html(
        "All Repository Materials (250 Files)",
        main_html,
        sidebar_html,
        toc,
        root_prefix,
        active_top="materials",
    )
    dst_html = out_dir / "curriculum" / "ALL_MATERIALS.html"
    dst_html.parent.mkdir(parents=True, exist_ok=True)
    dst_html.write_text(full_html)


def build_equation_atlas_page(all_records: list[dict], by_chrono: list[dict], enrichment: dict, out_dir: Path):
    """Build curriculum/EQUATION_ATLAS.html showcasing all 83 class equations and scientific diagrams."""
    root_prefix = "../"
    cards_html = []
    toc: list[tuple[int, str, str]] = []

    phases: dict[str, list[dict]] = {}
    for r in by_chrono:
        ph = enrichment[r["id"]]["phase"]
        phases.setdefault(ph, []).append(r)

    for ph_idx, (ph_title, items) in enumerate(phases.items(), 1):
        ph_id = f"phase-{ph_idx}"
        toc.append((2, ph_id, ph_title))
        cards_html.append(f'<h2 id="{ph_id}" style="font-family:var(--font-serif);margin-top:2rem">{html.escape(ph_title)}</h2>')
        for r in items:
            cid = r["id"]
            info = enrichment[cid]
            diag = info["online_diagram"]
            eq = info["equation"]
            toc.append((3, f"atlas-{cid.lower()}", f"{cid}: {eq['name']}"))
            rows = []
            for t in eq["terms"]:
                rows.append(
                    f'<tr>'
                    f'<td class="eq-term-cell">\\({html.escape(t["term"], quote=False)}\\)</td>'
                    f'<td><span class="eq-role-badge">{html.escape(t["role"])}</span></td>'
                    f'<td>{html.escape(t["meaning"])}</td>'
                    f'<td class="eq-failure-cell">{html.escape(t["failure"])}</td>'
                    f'</tr>'
                )
            nb_href = root_prefix + r["path"][:-6] + ".html"
            cards_html.append(f"""
            <section class="master-equation-card" id="atlas-{cid.lower()}" style="margin-bottom:1.5rem">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem">
                <div class="badge-row" style="margin:0">
                  <span class="badge badge-primary">{cid} · #{info['chronological_order']}</span>
                  <span class="badge badge-week">Week {info['week']}</span>
                </div>
                <a class="btn-action primary" href="{nb_href}">Open {cid} Lesson &amp; Code →</a>
              </div>
              <h3 style="margin:0.6rem 0 0.25rem;font-size:1.22rem"><a href="{nb_href}" style="text-decoration:none;color:var(--ink)">{cid} · {html.escape(r['title'])}</a> — {html.escape(eq['name'])}</h3>
              <p style="margin:0.25rem 0 0.65rem;color:var(--ink-secondary);font-size:0.92rem">{html.escape(eq['summary'])}</p>
              <div class="master-eq-box">\\[{html.escape(eq['latex'], quote=False)}\\]</div>
              <div class="concept-grid" style="margin-bottom:0.85rem">
                <figure class="commons-figure">
                  <img src="{html.escape(diag['image_url'])}" data-fullsrc="{html.escape(diag['original_url'])}" alt="{html.escape(diag['title'])}" loading="lazy" referrerpolicy="no-referrer" style="max-height:190px">
                  <figcaption class="commons-caption">
                    <a href="{html.escape(diag['source_page'])}" target="_blank" rel="noopener">{html.escape(diag['title'])}</a> ({html.escape(diag['license'])})
                  </figcaption>
                </figure>
                <div>
                  <div class="diagram-guide-box" style="margin-bottom:0;font-size:0.9rem">
                    <strong>Diagram &amp; Equation Connection ({cid}):</strong><br>
                    {html.escape(diag['guide'])}
                  </div>
                </div>
              </div>
              <div class="table-scroll">
                <table class="eq-breakdown-table">
                  <thead>
                    <tr>
                      <th>Logical Term</th>
                      <th>Role in Equation</th>
                      <th>What This Part Is Doing (Mechanism &amp; Units)</th>
                      <th>What Breaks If Omitted (Failure Mode)</th>
                    </tr>
                  </thead>
                  <tbody>{"".join(rows)}</tbody>
                </table>
              </div>
            </section>
            """)

    main_html = f"""
    <section class="class-banner">
      <div class="badge-row">
        <span class="badge badge-primary">83 Master Equations &amp; 434 Inline Dissections</span>
        <span class="badge badge-week">83 Wikimedia Commons Scientific Diagrams</span>
      </div>
      <h1>Complete Equation Logic &amp; Scientific Diagram Atlas</h1>
      <p style="margin:0.4rem 0 0;color:var(--ink-secondary);max-width:80ch">
        Every class in the 26-week curriculum is anchored by an existing open-licensed scientific concept diagram and a governing mathematical formulation broken down into its logical terms—showing <strong>which part of the equation is doing what</strong>, its physical or statistical units, and what silently breaks when a term is omitted or mis-specified.
      </p>
    </section>
    {"".join(cards_html)}
    """
    sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path="curriculum/EQUATION_ATLAS.html")
    full_html = wrap_page_html(
        "Equation Logic & Scientific Diagram Atlas",
        main_html,
        sidebar_html,
        toc,
        root_prefix,
        active_top="equations",
    )
    dst = out_dir / "curriculum" / "EQUATION_ATLAS.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(full_html)


def build_home_page(all_records: list[dict], by_chrono: list[dict], enrichment: dict, out_dir: Path):
    """Build the main index.html landing page with the 26-Week Study Path, Apple Dev Setup, Equation & Diagram Showcase, and Full Repository Directory."""
    root_prefix = ""
    cards_html = []
    for r in by_chrono:
        cid = r["id"]
        info = enrichment[cid]
        diag = info["online_diagram"]
        eq = info["equation"]
        strand_code = STRAND_LABELS[Path(r["path"]).parts[1]][0]
        href = r["path"][:-6] + ".html"
        cards_html.append(f"""
        <article class="class-card" data-strand="{strand_code}" data-phase="W{info['week']}">
          <div>
            <div class="class-card-top">
              <span class="badge badge-primary">{cid}</span>
              <span class="badge badge-week">Week {info['week']} · #{info['chronological_order']}</span>
              <span class="badge badge-phase">{strand_code}</span>
            </div>
            <h3><a href="{href}">{cid} · {html.escape(r['title'])}</a></h3>
            <p style="font-size:0.84rem;color:var(--ink-secondary);margin:0.35rem 0 0.6rem">
              <strong>{html.escape(eq['name'])}:</strong> {html.escape(eq['summary'])}
            </p>
          </div>
          <div>
            <div style="background:var(--surface-alt);padding:0.45rem 0.65rem;border-radius:6px;font-size:0.78rem;overflow-x:auto">
              \\({html.escape(eq['terms'][0]['term'], quote=False)}\\) · <span style="color:var(--accent-dark);font-weight:600">{len(eq['terms'])} logical terms dissected</span>
            </div>
            <div class="class-card-meta">
              <span>◫ Diagram: {html.escape(diag['title'][:42])}</span> ·
              <a href="{href}" style="font-weight:700">Open Class →</a>
            </div>
          </div>
        </article>
        """)

    readme_html, _, _ = render_markdown_to_html((ROOT / "README.md").read_text(), "", 1, decompose_equations=True)

    main_html = f"""
    <section class="hero-box">
      <div class="badge-row">
        <span class="badge" style="background:rgba(255,255,255,0.16);color:#fff">26-Week Graduate Curriculum</span>
        <span class="badge" style="background:rgba(110,231,183,0.2);color:#6ee7b7">macOS on Apple Silicon + Goose &amp; Ollama (Qwen &amp; Gemma)</span>
        <span class="badge" style="background:rgba(255,255,255,0.16);color:#fff">100% Repository Coverage (250 Files)</span>
      </div>
      <h1>Neuroimaging Research Methods with AI</h1>
      <p>
        Master functional, structural, and diffusion neuroimaging from first principles. Read landmark and 2025–2026 SOTA papers, inspect every mathematical transformation broken down into its logical terms, examine verified scientific diagrams, and supervise local AI coding agents on your MacBook Pro.
      </p>
      <div style="display:flex;flex-wrap:wrap;gap:0.7rem">
        <a class="btn-action primary" style="background:#10b981;border-color:#10b981;color:#052e25;font-weight:800" href="curriculum/SETUP.html">⌘ Step 0: Minimal Mac &amp; Apple Dev Setup →</a>
        <a class="btn-action" style="background:rgba(255,255,255,0.12);color:#fff;border-color:rgba(255,255,255,0.3)" href="notebooks/00_paper_orientation/00_how_to_read.html">▶ Start Class #1 (R00: Reading a Paper)</a>
        <a class="btn-action" style="background:rgba(255,255,255,0.12);color:#fff;border-color:rgba(255,255,255,0.3)" href="curriculum/EQUATION_ATLAS.html">∑ Equation Logic &amp; Diagram Atlas</a>
        <a class="btn-action" style="background:rgba(255,255,255,0.12);color:#fff;border-color:rgba(255,255,255,0.3)" href="curriculum/ALL_MATERIALS.html">🗂 Browse All 250 Repo Materials</a>
      </div>
      <div class="hero-stats">
        <div class="stat-item"><strong>83 + 17</strong><span>83 Main Classes + 4 Bridge Labs + 13 Upstream Notebooks</span></div>
        <div class="stat-item"><strong>434</strong><span>Equations Broken Down by Logical Terms</span></div>
        <div class="stat-item"><strong>83 + 22</strong><span>Wikimedia Scientific Diagrams + 22 Verification Plots</span></div>
        <div class="stat-item"><strong>24 / 310</strong><span>Core Papers &amp; Verified Literature Citations</span></div>
      </div>
    </section>

    <section class="apple-setup-card" id="minimal-apple-dev-setup">
      <div class="section-eyebrow">Minimal Apple / macOS Developer Environment Setup (Step 0)</div>
      <h2 style="font-family:var(--font-serif);margin:0.2rem 0 0.5rem">Everything Required on a Standard Apple Silicon MacBook Pro — Nothing Bloated</h2>
      <p style="margin:0 0 0.9rem;color:var(--ink-secondary)">
        You do <strong>not</strong> need the 12+ GB full Xcode IDE, Docker Desktop, or external CUDA GPUs. Enable only these four official Apple components before running <code>./setup.sh</code>:
      </p>
      <div class="apple-links-grid">
        <div class="apple-link-tile">
          <h4>1. Command Line Tools for Xcode (~600 MB)</h4>
          <p>Provides <code>git</code>, Apple <code>clang</code>, and macOS SDK headers via <code>xcode-select --install</code> without installing full Xcode.app.</p>
          <div class="tile-links">
            <a href="https://developer.apple.com/documentation/xcode/installing-the-command-line-tools" target="_blank" rel="noopener">Apple Docs: Command Line Tools ↗</a> ·
            <a href="https://developer.apple.com/download/all/" target="_blank" rel="noopener">Apple Developer Downloads ↗</a>
          </div>
        </div>
        <div class="apple-link-tile">
          <h4>2. Native Apple Silicon (<code>arm64</code>) Terminal</h4>
          <p>Verify <code>uname -m</code> prints <code>arm64</code> in <code>Terminal.app</code> so Python wheels and Ollama avoid Rosetta 2 x86_64 translation.</p>
          <div class="tile-links">
            <a href="https://support.apple.com/en-us/116943" target="_blank" rel="noopener">Apple Silicon Mac Guide ↗</a> ·
            <a href="https://support.apple.com/guide/terminal/welcome/mac" target="_blank" rel="noopener">macOS Terminal Guide ↗</a>
          </div>
        </div>
        <div class="apple-link-tile">
          <h4>3. Built-In Apple Metal GPU &amp; Accelerate</h4>
          <p>Included in macOS 14+/15+: <strong>Metal</strong> accelerates local Qwen &amp; Gemma inference on unified memory; <strong>Accelerate</strong> powers NumPy/SciPy SVD &amp; GLM.</p>
          <div class="tile-links">
            <a href="https://developer.apple.com/metal/" target="_blank" rel="noopener">Apple Metal GPU ↗</a> ·
            <a href="https://developer.apple.com/documentation/accelerate" target="_blank" rel="noopener">Apple Accelerate BLAS/LAPACK ↗</a>
          </div>
        </div>
        <div class="apple-link-tile">
          <h4>4. macOS Gatekeeper &amp; Privacy Permissions</h4>
          <p>Standard macOS security approval for first-run developer CLI binaries (<code>Ollama.app</code>, <code>goose</code>, <code>uv</code>) and folder access.</p>
          <div class="tile-links">
            <a href="https://support.apple.com/en-us/102445" target="_blank" rel="noopener">Apple Gatekeeper Guide ↗</a> ·
            <a href="curriculum/SETUP.html">Full Step 0 Course Setup Guide →</a>
          </div>
        </div>
      </div>
    </section>

    <section class="content-card" id="repository-sections-hub">
      <div class="section-eyebrow">Complete Repository Directory</div>
      <h2 style="margin-top:0.2rem">Explore Every Section of the Repository</h2>
      <div class="apple-links-grid">
        <div class="apple-link-tile">
          <h4>📚 Curriculum &amp; Coursework (<code>curriculum/</code>)</h4>
          <p>26-Week Study Plan, AI Supervision Workflow, Grading Rubrics, Evidence Ledger, A1–A4 Assignments, SOTA Audit, and Coverage Maps.</p>
          <div class="tile-links">
            <a href="curriculum/STUDY_PLAN.html">Study Plan</a> ·
            <a href="curriculum/AI_WORKFLOW.html">AI Workflow</a> ·
            <a href="curriculum/ASSESSMENT.html">Assessment</a> ·
            <a href="curriculum/COVERAGE_AUDIT.html">Coverage Audit</a>
          </div>
        </div>
        <div class="apple-link-tile">
          <h4>📄 24 Core Papers &amp; 310 Citations (<code>curriculum/papers/</code>)</h4>
          <p>Three-Pass reading method, 24 foundational &amp; 2025–2026 SOTA papers, and 310 OpenAlex-verified references across all 83 lessons.</p>
          <div class="tile-links">
            <a href="curriculum/papers/README.html">24-Paper Library</a> ·
            <a href="curriculum/papers/REFERENCES.html">310 Citations</a> ·
            <a href="curriculum/papers/READING_METHOD.html">3-Pass Guide</a>
          </div>
        </div>
        <div class="apple-link-tile">
          <h4>📘 Introductory Bridge &amp; 4 Labs (<code>course/</code>)</h4>
          <p>Unified 22-chapter Coursebook, Glossary, Transformation Contracts, Real fMRI Guide, 4 executed Labs (520–580), and 22 Verification Plots.</p>
          <div class="tile-links">
            <a href="course/COURSEBOOK.html">Unified Coursebook</a> ·
            <a href="course/labs/520_design.html">Labs 520–580</a> ·
            <a href="course/verification/REPORT.html">22 Plots</a>
          </div>
        </div>
        <div class="apple-link-tile">
          <h4>🏛 14 Pinned Upstream Tutorials (<code>third_party/</code>)</h4>
          <p>Unmodified university notebooks from Poldrack, DartBrains, BrainIAK, Neuromatch Academy, and Nipype rendered as web pages.</p>
          <div class="tile-links">
            <a href="third_party/README.html">Provenance Hub</a> ·
            <a href="curriculum/ALL_MATERIALS.html">All 250 Repo Files →</a>
          </div>
        </div>
      </div>
    </section>

    <section id="interactive-class-roadmap">
      <div class="section-eyebrow">Interactive 83-Class Curriculum Navigator</div>
      <h2 style="font-family:var(--font-serif);font-size:1.65rem;margin:0.2rem 0 0.6rem">Follow the 26-Week Study Path (#1 to #83) or Filter by Subject Strand</h2>
      <div class="roadmap-controls">
        <div class="filter-pills" role="group" aria-label="Filter classes by strand">
          <button type="button" class="filter-pill active" data-filter="ALL">All 83 Classes (26-Week Order)</button>
          <button type="button" class="filter-pill" data-filter="R">R · Seminars (4)</button>
          <button type="button" class="filter-pill" data-filter="F">F · Foundations &amp; Physics (4)</button>
          <button type="button" class="filter-pill" data-filter="PR">PR · Image Processing (21)</button>
          <button type="button" class="filter-pill" data-filter="D">D · Design &amp; Inference (16)</button>
          <button type="button" class="filter-pill" data-filter="DS">DS · Data Science (16)</button>
          <button type="button" class="filter-pill" data-filter="M">M · Modeling &amp; AI (18)</button>
          <button type="button" class="filter-pill" data-filter="P">P · Projects (4)</button>
        </div>
        <input type="search" id="roadmap-search" class="sidebar-search" style="max-width:280px;margin:0" placeholder="Search equation, topic, or ID..." aria-label="Search classes">
      </div>
      <div class="class-grid">
        {"".join(cards_html)}
      </div>
    </section>

    <article class="content-card" style="margin-top:2rem">
      {readme_html}
    </article>
    """

    toc = [
        (2, "minimal-apple-dev-setup", "Minimal Apple / macOS Dev Setup"),
        (2, "repository-sections-hub", "Complete Repository Directory"),
        (2, "interactive-class-roadmap", "Interactive 83-Class Navigator"),
    ]
    sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path="index.html")
    full_html = wrap_page_html(
        "26-Week Graduate Course & Interactive Textbook",
        main_html,
        sidebar_html,
        toc,
        root_prefix,
        active_top="home",
    )
    (out_dir / "index.html").write_text(full_html)


def build_markdown_pages(all_records: list[dict], enrichment: dict, out_dir: Path):
    """Convert all Markdown files in root, curriculum/, course/, third_party/, and data/ into styled HTML pages."""
    md_files = (
        list(ROOT.glob("*.md"))
        + list((ROOT / "curriculum").rglob("*.md"))
        + list((ROOT / "course").rglob("*.md"))
        + list((ROOT / "third_party").rglob("*.md"))
        + list((ROOT / "website").glob("*.md"))
        + list((ROOT / "data").glob("*.md"))
    )
    for md_path in sorted(set(md_files)):
        rel = md_path.relative_to(ROOT)
        current_rel_dir = "" if str(rel.parent) == "." else str(rel.parent)
        depth = 0 if str(rel.parent) == "." else len(rel.parent.parts)
        root_prefix = "../" * depth

        raw_md = md_path.read_text()
        lines = raw_md.splitlines()
        page_title = rel.stem
        if lines and lines[0].startswith("# "):
            page_title = re.sub(r"^#+\s*", "", lines[0]).strip()

        body_html, toc, _ = render_markdown_to_html(raw_md, current_rel_dir, 1, decompose_equations=True)
        active_top = ""
        if str(rel) == "curriculum/SETUP.md":
            active_top = "setup"
        elif str(rel) == "curriculum/STUDY_PLAN.md":
            active_top = "plan"
        elif str(rel) == "curriculum/NOTEBOOK_INDEX.md":
            active_top = "classes"
        elif str(rel).startswith("curriculum/papers/"):
            active_top = "papers"
        elif str(rel) == "curriculum/AI_WORKFLOW.md":
            active_top = "ai"
        elif str(rel).startswith(("course/", "third_party/")):
            active_top = "materials"

        main_html = (
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.75rem">'
            f'<span class="badge badge-phase">Source file: <code>{html.escape(rel.as_posix())}</code></span>'
            f'<a class="btn-action" style="padding:0.25rem 0.65rem;font-size:0.76rem" href="{html.escape(rel.name)}" download>⬇ Download Raw Markdown ({html.escape(rel.name)})</a>'
            f'</div>'
            f'<article class="content-card">{body_html}</article>'
        )
        sidebar_html = build_sidebar_html(all_records, enrichment, root_prefix, current_rel_path=rel.as_posix())
        full_html = wrap_page_html(page_title, main_html, sidebar_html, toc, root_prefix, active_top=active_top)

        dst_html = out_dir / rel.with_suffix(".html")
        dst_html.parent.mkdir(parents=True, exist_ok=True)
        dst_html.write_text(full_html)
        shutil.copy2(md_path, out_dir / rel)


def copy_static_and_supplement_files(out_dir: Path):
    """Copy all git-tracked static/supplement files so 100% of repository materials exist in out_dir."""
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "site.css").write_text(SITE_CSS.strip() + "\n")
    (assets_dir / "site.js").write_text(SITE_JS.strip() + "\n")
    (out_dir / ".nojekyll").write_text("")

    # Copy every single git-tracked file into out_dir (HTML builders will then write rendered .html alongside/over raw .html)
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    for rel_str in tracked:
        src = ROOT / rel_str
        if src.is_file():
            dst = out_dir / rel_str
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # Also copy newly added untracked enrichment/workflow files
    for extra in [
        ".github/workflows/pages.yml",
        "curriculum/course_enrichment.json",
        "scripts/build_website.py",
        "scripts/enrichment_part1.py",
        "scripts/enrichment_part2.py",
        "scripts/equation_decomposer.py",
        "scripts/site_theme.py",
    ]:
        if (ROOT / extra).exists():
            dst = out_dir / extra
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / extra, dst)


def verify_site_links(out_dir: Path) -> int:
    """Verify that all relative hrefs across all generated HTML files resolve inside out_dir."""
    html_files = sorted(out_dir.rglob("*.html"))
    broken = []
    checked = 0
    for hf in html_files:
        content = hf.read_text()
        for m in re.finditer(r'href="([^"]+)"', content):
            href = html.unescape(m.group(1)).strip()
            if not href or href.startswith(("#", "http://", "https://", "mailto:", "javascript:", "data:")):
                continue
            u = urlsplit(href)
            if not u.path:
                continue
            target = (hf.parent / unquote(u.path)).resolve()
            checked += 1
            if not target.exists():
                broken.append(f"{hf.relative_to(out_dir)} -> {href}")
    if broken:
        print("Broken links found in generated website:")
        for b in broken[:30]:
            print("  ", b)
        raise SystemExit(1)
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build/site", help="Output directory for static site")
    args = parser.parse_args()

    out_dir = (ROOT / args.output).resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    enrichment = json.loads((ROOT / "curriculum" / "course_enrichment.json").read_text())
    all_records = json.loads((ROOT / "curriculum" / "notebook_index.json").read_text())
    by_chrono = sorted(all_records, key=lambda r: enrichment[r["id"]]["chronological_order"])
    papers = json.loads((ROOT / "curriculum" / "papers" / "paper_registry.json").read_text())["papers"]
    papers_by_id = {p["id"]: p for p in papers}

    copy_static_and_supplement_files(out_dir)
    build_markdown_pages(all_records, enrichment, out_dir)
    build_coursebook_combined_page(all_records, enrichment, out_dir)
    for rec in all_records:
        build_notebook_page(rec, all_records, by_chrono, enrichment, papers_by_id, out_dir)
    build_extra_notebook_pages(all_records, enrichment, out_dir)
    build_equation_atlas_page(all_records, by_chrono, enrichment, out_dir)
    build_all_materials_page(all_records, by_chrono, enrichment, out_dir)
    build_home_page(all_records, by_chrono, enrichment, out_dir)
    # Preserve the comprehensive materials dashboard as a secondary resource.
    (out_dir / "index.html").rename(out_dir / "roadmap.html")
    build_lecture_decks(by_chrono, enrichment, papers_by_id, out_dir, render_markdown_to_html)
    build_academic_pages(by_chrono, enrichment, out_dir, render_markdown_to_html)

    add_site_discovery(out_dir)
    checked_links = verify_site_links(out_dir)
    html_count = len(list(out_dir.rglob("*.html")))
    print(
        f"Built {html_count} HTML pages (83 main classes + 4 bridge labs + 14 upstream tutorials + Equation Atlas + All Materials Explorer + 61 Markdown pages) in {out_dir.relative_to(ROOT)}; verified {checked_links} internal links with 0 errors."
    )


if __name__ == "__main__":
    main()
