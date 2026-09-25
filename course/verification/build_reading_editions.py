"""Build the combined coursebook and four offline notebook reading companions.

Run after verify_course.py has finished updating notebook outputs:
    .venv/bin/python course/verification/build_reading_editions.py

Requires the `markdown` package. No network, JavaScript, CDN, notebook execution,
or upstream content downloads are used. Original Markdown and notebooks stay intact.
"""
from __future__ import annotations

import base64
import html
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    "README.md", "SETUP.md", "lessons/00_bridge.md", "lessons/580.md",
    "lessons/540.md", "lessons/520.md", "lessons/550.md", "lessons/90_capstone.md",
    "REAL_DATA.md", "TRANSFORMATIONS.md", "GLOSSARY.md", "ASSESSMENT.md", "verification/REPORT.md",
    "templates/transformation_card.md", "templates/analysis_record.md",
    "templates/project_plan.md", "answer_keys/520.md", "SOURCES.md",
    "sources/580.md", "sources/540.md", "sources/520.md", "sources/550.md",
]
DOC_IDS = {name: "doc-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
           for name in DOCUMENTS}
EXTENSIONS = ["tables", "fenced_code", "sane_lists", "toc"]
CSS = """
:root{color-scheme:light;--ink:#172e38;--muted:#51666e;--paper:#fffef9;
--ground:#eef3f1;--line:#d7e1dd;--accent:#096b63;--wash:#e7f2ed}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--ground);
color:var(--ink);font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
font-size:16px;line-height:1.7}a{color:var(--accent);text-underline-offset:.18em}
a:hover{color:#004f4a}a:focus-visible,summary:focus-visible{outline:3px solid #ce9b35;outline-offset:4px}
.cover{max-width:1160px;margin:0 auto;padding:64px 46px 38px;border-bottom:1px solid var(--line)}
.eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:.75rem;font-weight:750;color:var(--accent)}
.cover h1{font-family:ui-serif,Georgia,serif;font-weight:500;font-size:clamp(2.2rem,5vw,3.8rem);
line-height:1.12;max-width:850px;margin:.45em 0}.lede{max-width:760px;color:var(--muted);font-size:1.07rem}
.layout{max-width:1160px;margin:auto;display:grid;grid-template-columns:245px minmax(0,1fr);gap:32px;padding:30px 28px 60px}
nav{font-size:.82rem;line-height:1.45;align-self:start;position:sticky;top:18px;max-height:calc(100vh - 36px);overflow:auto}
nav h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.12em;margin:1.2em 0 .75em}
nav ol,nav ul{list-style:none;margin:0;padding:0}nav li{padding:.3em 0}nav a{text-decoration:none}
nav .lab-links{padding-top:12px;margin-top:12px;border-top:1px solid var(--line)}
main{min-width:0}.chapter,.notebook{padding:32px 36px;background:var(--paper);border:1px solid var(--line);
border-radius:10px;margin-bottom:24px}.chapter>h2:first-of-type{font-size:1.85rem;line-height:1.25}
h1,h2,h3,h4,h5,h6{line-height:1.3;scroll-margin-top:22px}h2,h3,h4{margin-top:1.6em}h2{font-size:1.55rem}
h3{font-size:1.22rem}h4{font-size:1.08rem}p{margin:.9em 0}strong{font-weight:720}
.chapter-meta,.cell-label,.footer{font-size:.76rem;color:var(--muted)}.chapter-meta{margin:0 0 22px}
.back-top{display:block;margin-top:28px;font-size:.78rem}blockquote{margin:1.2em 0;padding:.2em 18px;
border-left:3px solid var(--accent);background:var(--wash)}blockquote p{margin:.6em 0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.86em;
background:#eaf0ed;padding:.12em .28em;border-radius:3px;overflow-wrap:anywhere}
pre{background:#132c34;color:#edf6f2;padding:17px 19px;border-radius:7px;overflow:auto;line-height:1.5;
tab-size:4;font-size:.84rem}pre code{background:transparent;color:inherit;padding:0;overflow-wrap:normal}
.output pre{background:#eef4f1;color:#173a32;border:1px solid var(--line);white-space:pre-wrap;
overflow-wrap:anywhere}.table-scroll{max-width:100%;overflow-x:auto;margin:1.2em 0}
table{border-collapse:collapse;width:100%;font-size:.87rem}th,td{text-align:left;vertical-align:top;
border:1px solid var(--line);padding:10px 12px;min-width:100px}th{background:var(--wash)}
tbody tr:nth-child(even){background:#f5f8f5}hr{border:0;border-top:1px solid var(--line);margin:2em 0}
img{max-width:100%;height:auto}.cell{padding:8px 0 20px}.cell+.cell{border-top:1px solid #e3ebe7}
.cell-label{font-family:ui-monospace,monospace;letter-spacing:.04em}.output{margin-top:12px}
.output figure{margin:16px 0;background:white;padding:8px;border:1px solid var(--line);border-radius:6px}
.output img{display:block;margin:auto}.error{border-left:4px solid #9e3b37;padding-left:12px}
details{margin:12px 0}summary{cursor:pointer;color:var(--accent)}.footer{max-width:1160px;margin:auto;padding:0 30px 35px}
@media(max-width:850px){.layout{display:block;padding:18px 14px 38px}.cover{padding:34px 24px 25px}
nav{position:static;max-height:none;padding:18px 22px;margin-bottom:20px;border:1px solid var(--line);
border-radius:8px;background:#f8faf8}nav ol{columns:2;column-gap:25px}nav li{break-inside:avoid}
.chapter,.notebook{padding:24px 22px}}@media(max-width:480px){body{font-size:15px}nav ol{columns:1}
.chapter,.notebook{padding:20px 16px}.cover{padding:28px 20px}pre{padding:13px}}
@media print{body{background:white;font-size:10pt}.cover{padding:0 0 20px}.layout{display:block;padding:0}
nav,.back-top{display:none}.chapter,.notebook{border:0;padding:16px 0;break-before:page}
pre{white-space:pre-wrap;background:#eee!important;color:black!important}a{color:inherit}
.table-scroll{overflow:visible}table{font-size:8pt}.output figure{break-inside:avoid}}
"""


def external(target: str) -> bool:
    parts = urlsplit(target)
    return bool(parts.scheme or parts.netloc) or target.startswith("//")


def root_target(target: str, source: str) -> str:
    """Resolve a link in source relative to course/, retaining query and fragment."""
    if not target or external(target) or target.startswith("/"):
        return target
    parts = urlsplit(target)
    path = unquote(parts.path)
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path)) if path else source
    return urlunsplit(("", "", quote(resolved, safe="/@:+~"), parts.query, parts.fragment))


def html_target(target: str, source: str, output_dir: str, book: bool, image: bool = False) -> str:
    rebased = root_target(target, source)
    if external(rebased) or rebased.startswith("/"):
        return rebased
    parts = urlsplit(rebased)
    path = unquote(parts.path)
    if book and not image:
        if path == "COURSEBOOK.md":
            return "#top"
        if path in DOC_IDS:
            return "#" + DOC_IDS[path] + ("-" + parts.fragment if parts.fragment else "")
    relative = posixpath.relpath(path, output_dir or ".")
    if not image and relative.endswith(".ipynb"):
        # Reading links lead to the offline snapshot; each snapshot links its notebook.
        relative = relative[:-6] + ".html"
    return urlunsplit(("", "", quote(relative, safe="/@:+~"), parts.query, parts.fragment))


class RebaseHTML(HTMLParser):
    """Adjust generated Markdown anchors/links and add accessible scrolling tables."""
    def __init__(self, source: str, output_dir: str, book: bool):
        super().__init__(convert_charrefs=False)
        self.source, self.output_dir, self.book = source, output_dir, book
        self.prefix = DOC_IDS.get(source, "") if book else ""
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.parts.append('<div class="table-scroll" role="region" aria-label="Scrollable table" tabindex="0">')
        converted = []
        for key, value in attrs:
            if value is not None and key in {"href", "src"}:
                value = html_target(value, self.source, self.output_dir, self.book, key == "src")
            elif key == "id" and value and self.prefix:
                value = self.prefix + "-" + value
            converted.append(key if value is None else f'{key}="{html.escape(value, quote=True)}"')
        rendered_tag = f"h{min(int(tag[1])+1,6)}" if self.book and re.fullmatch(r"h[1-6]",tag) else tag
        self.parts.append("<" + rendered_tag + (" " + " ".join(converted) if converted else "") + ">")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        rendered_tag = f"h{min(int(tag[1])+1,6)}" if self.book and re.fullmatch(r"h[1-6]",tag) else tag
        self.parts.append("</" + rendered_tag + ">")
        if tag == "table":
            self.parts.append("</div>")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append("&" + name + ";")

    def handle_charref(self, name):
        self.parts.append("&#" + name + ";")

    def handle_comment(self, data):
        self.parts.append("<!--" + data + "-->")


def render_markdown(text: str, source: str, output_dir: str = "", book: bool = False) -> str:
    raw = markdown.markdown(text, extensions=EXTENSIONS, output_format="html5")
    parser = RebaseHTML(source, output_dir, book)
    parser.feed(raw)
    parser.close()
    return "".join(parser.parts)


def rebase_markdown(text: str, source: str) -> str:
    """Rebase authored Markdown links while leaving fenced code verbatim."""
    inline = re.compile(r"(!?\[[^\]\n]*\]\()(<[^>\n]*>|[^)\s]+)([^)\n]*\))")
    definition = re.compile(r"^(\s*\[[^\]]+\]:\s*)(<[^>]+>|\S+)(.*)$")
    fence = None
    output = []
    def replace(match):
        raw = match.group(2)
        target = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
        mapped = root_target(target, source)
        return match.group(1) + ("<"+mapped+">" if raw.startswith("<") else mapped) + match.group(3)
    for line in text.splitlines(keepends=True):
        opening = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if opening:
            marks = opening.group(1)
            if fence is None:
                fence = marks
            elif marks[0] == fence[0] and len(marks) >= len(fence):
                fence = None
            output.append(line)
        elif fence is not None:
            output.append(line)
        else:
            output.append(definition.sub(replace, inline.sub(replace, line)))
    return "".join(output)


def title_of(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return re.sub(r"[`*_]", "", match.group(1)).strip() if match else fallback


def document(title: str, eyebrow: str, lede: str, navigation: str, body: str) -> str:
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head><body id="top">
<header class="cover"><div class="eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1>
<p class="lede">{lede}</p></header><div class="layout"><nav aria-label="Contents">{navigation}</nav>
<main>{body}</main></div><footer class="footer">Original AI-assisted neuroimaging course · Read, predict, run, inspect, explain.
 External reading links require internet; this reading edition uses no remote scripts, styles, or fonts.</footer></body></html>'''


def notebook_text(value) -> str:
    return "".join(value) if isinstance(value, list) else str(value)


def render_output(output: dict) -> str:
    kind = output.get("output_type", "")
    if kind == "stream":
        return '<div class="output"><pre>' + html.escape(notebook_text(output.get("text", ""))) + "</pre></div>"
    if kind == "error":
        message = "\n".join(output.get("traceback", [])) or str(output)
        message = re.sub(r"\x1b\[[0-9;]*m", "", message)
        return '<div class="output error"><pre>' + html.escape(message) + "</pre></div>"
    data = output.get("data", {})
    for mime in ("image/png", "image/jpeg", "image/svg+xml"):
        if mime in data:
            payload = notebook_text(data[mime])
            if mime == "image/svg+xml":
                payload = base64.b64encode(payload.encode()).decode()
            else:
                payload = "".join(payload.split())
            return f'<div class="output"><figure><img alt="Recorded notebook figure" src="data:{mime};base64,{payload}"></figure></div>'
    if "text/plain" in data:
        return '<div class="output"><pre>' + html.escape(notebook_text(data["text/plain"])) + "</pre></div>"
    if "text/markdown" in data:
        return '<div class="output">' + markdown.markdown(notebook_text(data["text/markdown"]), extensions=EXTENSIONS) + "</div>"
    if "text/html" in data:
        # Preserve the content for inspection without executing embedded HTML or JS.
        return '<div class="output"><pre>' + html.escape(notebook_text(data["text/html"])) + "</pre></div>"
    return ""


def build_notebook(path: Path, notebook: dict) -> None:
    cells, toc = [], []
    source = path.relative_to(ROOT).as_posix()
    notebook_title = path.stem.replace("_", " ")
    for index, cell in enumerate(notebook.get("cells", [])):
        text = notebook_text(cell.get("source", ""))
        if cell.get("cell_type") == "markdown":
            if index == 0:
                notebook_title = title_of(text, notebook_title)
            heading = re.search(r"^##\s+(.+)$", text, flags=re.MULTILINE)
            if heading:
                toc.append(f'<li><a href="#cell-{index}">{html.escape(heading.group(1))}</a></li>')
            # Notebook attachment images, if present, are embedded in the standalone file.
            for name, data in cell.get("attachments", {}).items():
                mime = next((m for m in ("image/png", "image/jpeg", "image/svg+xml") if m in data), None)
                if mime:
                    payload = notebook_text(data[mime])
                    if mime == "image/svg+xml":
                        payload = base64.b64encode(payload.encode()).decode()
                    text = text.replace("attachment:"+name, f"data:{mime};base64,{payload}")
            inner = render_markdown(text, source, "labs")
        elif cell.get("cell_type") == "code":
            count = cell.get("execution_count")
            label = f"Code · execution {count}" if count is not None else "Code · not executed"
            inner = '<div class="cell-label">' + html.escape(label) + '</div><pre><code>' + html.escape(text) + '</code></pre>'
            inner += "".join(render_output(output) for output in cell.get("outputs", []))
        else:
            inner = '<pre>' + html.escape(text) + '</pre>'
        cells.append(f'<section class="cell" id="cell-{index}">{inner}</section>')
    navigation = '<h2>Lab sections</h2><ol>' + "".join(toc) + '</ol><div class="lab-links">'
    navigation += '<p><a href="../COURSEBOOK.html">← Coursebook</a></p>'
    navigation += f'<p><a href="{html.escape(path.name)}">Download/open editable notebook</a></p></div>'
    status = notebook.get("metadata", {}).get("course_verification", {}).get("status", "Execution status not recorded")
    lede = f'Offline reading companion with recorded code, text output, and embedded figures. Verification record: <strong>{html.escape(status)}</strong>. Open the notebook to run or change a cell.'
    page = document(notebook_title, "Practical lab · recorded outputs", lede, navigation,
                    '<article class="notebook">' + "".join(cells) + '</article>')
    path.with_suffix(".html").write_text(page, encoding="utf-8")
    print("Built", path.with_suffix(".html").relative_to(ROOT))


def main() -> None:
    sources = {name: (ROOT/name).read_text(encoding="utf-8") for name in DOCUMENTS}
    notebooks = [(path, json.loads(path.read_text(encoding="utf-8")))
                 for path in sorted((ROOT/"labs").glob("*.ipynb"))]
    if len(notebooks) != 4:
        raise RuntimeError(f"Expected four course notebooks, found {len(notebooks)}")
    for path, notebook in notebooks:
        status = notebook.get("metadata", {}).get("course_verification", {}).get("status", "")
        if not status.startswith("passed"):
            raise RuntimeError(f"Wait for verify_course.py to finish before building: {path.name}")
    titles = {name: title_of(text, name) for name, text in sources.items()}
    md_parts = ["# AI-assisted neuroimaging — complete coursebook\n\n"
                "Original course materials, collected into one reading edition. "
                "Use the accompanying notebooks for executable exercises.\n\n## Contents\n\n"]
    md_parts += [f"- [{titles[name]}](#{DOC_IDS[name]})\n" for name in DOCUMENTS]
    chapters = []
    for name, text in sources.items():
        anchor = DOC_IDS[name]
        md_parts.append(f'\n\n---\n\n<a id="{anchor}"></a>\n\n' + rebase_markdown(text, name))
        rendered = render_markdown(text, name, book=True)
        meta = f'<p class="chapter-meta">Source: <a href="{quote(name)}">{html.escape(name)}</a></p>'
        chapters.append(f'<article class="chapter" id="{anchor}">{meta}{rendered}<a class="back-top" href="#top">Back to contents ↑</a></article>')
    navigation = '<h2>Course contents</h2><ol>' + "".join(
        f'<li><a href="#{DOC_IDS[name]}">{html.escape(titles[name])}</a></li>' for name in DOCUMENTS) + '</ol>'
    navigation += '<div class="lab-links"><h2>Recorded labs</h2><ul>' + "".join(
        f'<li><a href="labs/{path.stem}.html">{html.escape(path.stem.replace("_", " "))}</a></li>'
        for path, _ in notebooks) + '</ul></div>'
    lede = ('A course in understanding what AI-assisted analysis does to an image, a time series, and a research claim. '
            'Read the lessons here, then open a recorded lab or run its editable notebook. '
            'The syllabus, exercises, and explanations are original materials inspired by USC’s published NIIN course areas.')
    page = document("Understand every transformation", "AI-assisted neuroimaging · complete reading edition",
                    lede, navigation, "".join(chapters))
    (ROOT/"COURSEBOOK.md").write_text("".join(md_parts).rstrip()+"\n", encoding="utf-8")
    (ROOT/"COURSEBOOK.html").write_text(page, encoding="utf-8")
    print("Built COURSEBOOK.md and COURSEBOOK.html with", len(DOCUMENTS), "source documents")
    for path, notebook in notebooks:
        build_notebook(path, notebook)


if __name__ == "__main__":
    main()
