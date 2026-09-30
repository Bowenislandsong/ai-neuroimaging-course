"""Academic course front door and browser lecture decks for the existing static build."""
from __future__ import annotations
import base64
import html
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
E = html.escape

NAV = [('index.html', 'Overview'), ('curriculum/SYLLABUS.html', 'Syllabus'),
       ('schedule.html', 'Schedule'), ('lectures.html', 'Lectures & slides'),
       ('curriculum/papers/README.html', 'Readings'), ('assignments.html', 'Assignments'),
       ('curriculum/SETUP.html', 'Setup')]


def shell(title, body, active='Overview', prefix=''):
    links = ''.join(f'<a href="{prefix}{path}"' + (' aria-current="page"' if label == active else '') + f'>{label}</a>' for path, label in NAV)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · Neuroimaging Research Methods with AI</title><meta name="description" content="A 26-week open course in neuroimaging research methods, with lecture slides, notebooks, readings and research assignments."><link rel="stylesheet" href="{prefix}assets/course.css"></head><body>
<a class="skip" href="#main">Skip to content</a><header class="masthead"><div class="masthead-inner"><a class="wordmark" href="{prefix}index.html">Neuroimaging Research Methods</a><small>Open course / AI-assisted research</small></div></header><div class="nav-wrap"><nav class="course-nav" aria-label="Course navigation">{links}</nav></div><main class="course-wrap" id="main">{body}</main><footer class="course-footer"><div><span>Independent open course · Original materials CC BY-SA 4.0<br>26 weeks of study, discussion and reproducible experiments</span><span><a href="https://github.com/Bowenislandsong/ai-neuroimaging-course">GitHub repository</a> · <a href="{prefix}curriculum/ALL_MATERIALS.html">All materials</a><br><a href="{prefix}THIRD_PARTY_NOTICES.html">Sources &amp; licenses</a> · <a href="https://github.com/Bowenislandsong/ai-neuroimaging-course/issues">Report an issue</a></span></div></footer></body></html>'''


def lesson_links(record):
    cid = record['id']
    notes = record['path'].replace('.ipynb', '.html')
    return f'<span class="materials"><a href="slides/{cid}.html">Slides</a> · <a href="{notes}">Notes</a> · <a href="{record["path"]}" download>Notebook</a></span>'


def study_rows():
    rows = {}
    for line in (ROOT / 'curriculum/STUDY_PLAN.md').read_text().splitlines():
        cols = [c.strip() for c in line.strip().strip('|').split('|')]
        if line.startswith('|') and len(cols) == 4 and cols[0].isdigit():
            rows[int(cols[0])] = cols
    return rows


WEEK_TITLES = ['Reading research evidence', 'Generalization and analytical choices', 'Measurement and computational foundations',
 'Arrays, tables and image data', 'Missingness and sampling', 'Estimation, reliability and power', 'Regression and reproducibility',
 'Geometry, registration and bias', 'Segmentation and cortical surfaces', 'Timing, motion and distortion', 'Nuisance signals and quality control',
 'Diffusion and tractography', 'Reproducible anatomical workflows', 'Experimental design and temporal noise', 'Group inference and selection',
 'Single-run fMRI analysis', 'Encoding, decoding and baselines', 'Validation and representation learning', 'Connectomes and representational similarity',
 'Naturalistic data and latent states', 'Dynamics, CNNs and segmentation', 'Transfer and foundation models', 'Cohort generalization',
 'Specialist practical and reconstruction', 'Research proposal and review', 'Reproducibility and final defense']
MILESTONES = {2: 'A1 · Figure brief', 13: 'A2 · Mechanism experiment', 22: 'A3 · Agree reconstruction scope',
              24: 'A3 · Completed reconstruction', 25: 'A4 · Research proposal', 26: 'A4 · Independent defense'}


def schedule_table(records, enrichment, render, weeks=range(1, 27)):
    study = study_rows()
    papers = {p['id']: p for p in json.loads((ROOT / 'curriculum/papers/paper_registry.json').read_text())['papers']}
    rows = []
    for week in weeks:
        lessons = [r for r in records if enrichment[r['id']]['week'] == week]
        items = ''.join(f'<div class="lesson-link"><a href="{r["path"].replace(".ipynb", ".html")}">{r["id"]} · {E(r["title"])}</a>{lesson_links(r)}</div>' for r in lessons)
        if not lessons:
            items = f'<a href="curriculum/STUDY_PLAN.html">{E(study[week][1])}</a>'
        reading = render(study[week][2], 'curriculum', decompose_equations=False)[0]
        # The Markdown renderer emits paths relative to curriculum; schedule lives at the root.
        reading = re.sub(r'href="(?!https?:|#)([^"]+)"', lambda m: f'href="curriculum/{m[1]}"', reading)
        def link_paper(match):
            pid = match[0]
            guide = papers[pid]['guide'].replace('.md', '.html')
            return f'<a href="curriculum/papers/{guide}">{pid}</a>'
        reading = ''.join(part if part.startswith('<') else re.sub(r'\b(?:PP|PD|PM|PB)\d{2}\b', link_paper, part) for part in re.split(r'(<[^>]*>)', reading))
        evidence = render(study[week][3], 'curriculum', decompose_equations=False)[0]
        evidence = re.sub(r'href="(?!https?:|#)([^"]+)"', lambda m: f'href="curriculum/{m[1]}"', evidence)
        milestone = f'<div class="milestone">{MILESTONES[week]}</div>' if week in MILESTONES else ''
        rows.append(f'<tr id="week-{week}"><td>{week:02d}</td><td><div class="week-topic">{WEEK_TITLES[week-1]}</div>{items}</td><td>{reading}</td><td>{milestone}{evidence}</td></tr>')
    return '<div class="course-table-wrap"><table class="course-table"><thead><tr><th scope="col">Week</th><th scope="col">Lectures &amp; materials</th><th scope="col">Reading focus</th><th scope="col">Work &amp; evidence</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'


def build_academic_pages(records, enrichment, out, render):
    for asset in ['course.css', 'slides.css', 'slides.js', 'reader.css']:
        shutil.copy2(ROOT / 'website' / asset, out / 'assets' / asset)
    overview = f'''<section class="intro-grid"><div><p class="eyebrow">26-week open course</p><h1>Neuroimaging Research Methods with AI</h1><p class="lead">Read the research. Understand the measurement. Build an analysis you can defend.</p><p class="lead">A paper-led course in structural, functional and diffusion MRI, experimental design, data science, and computational modeling. Lecture slides introduce the ideas; Jupyter labs put them to the test.</p><div class="action-row"><a class="course-button solid" href="schedule.html">View course schedule</a><a class="course-button" href="curriculum/SYLLABUS.html">Read the syllabus</a></div></div><aside class="course-facts" aria-label="Course at a glance"><h3>Course at a glance</h3><dl><div><dt>Format</dt><dd>Self-paced or supervised seminar</dd></div><div><dt>Duration</dt><dd>26 weeks</dd></div><div><dt>Workload</dt><dd>8–12 hours most weeks</dd></div><div><dt>Materials</dt><dd>{len(records)} lessons with slides</dd></div><div><dt>Research</dt><dd>24 core papers</dd></div><div><dt>Assessment</dt><dd>Four integrated assignments</dd></div></dl></aside></section>
<section class="section"><h2>Before your first class</h2><div class="start-grid"><article class="start-item"><span class="number">01 / PREPARE</span><h3>Set up your workspace</h3><p>Prepare Python, Jupyter and your AI study tools. Keep the notebook beside the lesson notes.</p><a href="curriculum/SETUP.html">Environment setup</a></article><article class="start-item"><span class="number">02 / READ</span><h3>Begin with a research question</h3><p>The opening seminars start with figures and scientific claims. Programming enters in week 3.</p><a href="notebooks/00_paper_orientation/00_how_to_read.html">R00 · Reading a research paper</a></article><article class="start-item"><span class="number">03 / RECORD</span><h3>Keep an evidence ledger</h3><p>Record the question, observation unit, comparison, and limits of each paper before asking AI.</p><a href="curriculum/coursework/EVIDENCE_LEDGER.html">Evidence ledger template</a></article></div></section>
<section class="section"><div class="section-heading"><h2>Opening classes</h2><a href="schedule.html">Full 26-week schedule</a></div>{schedule_table(records,enrichment,render,[1,2,3])}</section>
<section class="section two-column"><div><h2>What you will learn</h2><ul><li>Trace a scan through its spatial and temporal transformations.</li><li>Justify a design, statistical contrast, and validation strategy.</li><li>Compare models under independent participant or site evaluation.</li><li>Connect a paper’s figure to a reproducible research claim.</li></ul><a href="curriculum/SYLLABUS.html#learning-outcomes">Complete learning outcomes</a></div><div><h2>Course resources</h2><ul class="text-link-list"><li><a href="lectures.html">Lecture slides and notebooks</a><small>Every class in the study sequence</small></li><li><a href="curriculum/papers/README.html">Research paper library</a><small>Assigned figures, reading guides and source records</small></li><li><a href="assignments.html">Assignments and rubrics</a><small>Figure brief, mechanism experiment, reconstruction and defense</small></li><li><a href="curriculum/AI_WORKFLOW.html">AI-assisted study</a><small>Predictions, inspected outputs and independent explanations</small></li></ul></div></section>'''
    (out / 'index.html').write_text(shell('Course overview', overview))
    schedule = '<p class="eyebrow">Course calendar</p><h1>Schedule</h1><p class="lead">Each week connects a paper question to a method, a notebook experiment, and evidence you can explain.</p><p class="academic-note">Weeks are relative to your course start. Assignment checkpoints guide pacing; a supervised offering sets its own calendar dates. Allow extra time for specialist practicals in weeks 8–13.</p><nav class="schedule-index" aria-label="Jump to week">' + ''.join(f'<a href="#week-{w}">{w:02d}</a>' for w in range(1,27)) + '</nav>' + schedule_table(records,enrichment,render)
    (out / 'schedule.html').write_text(shell('Schedule', schedule, 'Schedule'))
    rows = []
    for r in records:
        cid = r['id']; info = enrichment[cid]
        strand = Path(r['path']).parts[1]
        rows.append(f'<article class="lecture-row" data-strand="{strand}" data-search="{E((cid+" "+r["title"]+" "+r["path"]+" "+info["equation"]["name"]+" "+info["equation"]["summary"]).lower())}"><div class="lecture-id">{cid}</div><div><a class="lecture-title" href="slides/{cid}.html">{E(r["title"])}</a><div class="subtle">Week {info["week"]} · {info["slide_count"]} slides · {"Reading seminar" if r["execution_tier"] == "reading" else "Notebook lab"}</div></div><div class="lecture-actions"><a href="slides/{cid}.html">Slides</a><a href="{r["path"].replace(".ipynb",".html")}">Notes</a><a href="{r["path"]}" download>Lab</a></div></article>')
    strands = {Path(r['path']).parts[1] for r in records}
    names = ['Paper seminars','Foundations','Image processing','Research design','Data science','Modeling','Projects']
    options = ''.join(f'<option value="{strand}">{name}</option>' for strand,name in zip(sorted(strands),names))
    lectures = f'''<p class="eyebrow">Lecture materials</p><h1>Lectures &amp; slides</h1><p class="lead">Presentation slides for all {len(records)} classes, paired with complete notes and downloadable notebook labs.</p><p class="subtle">Use the arrow keys to present. Handout view shows the whole deck; Print / PDF creates a slide handout.</p><div class="filters"><input id="lecture-search" type="search" placeholder="Search a topic or class ID" aria-label="Search lectures"><select id="lecture-strand" aria-label="Filter by course strand"><option value="">All strands</option>{options}</select></div><p class="count" id="lecture-count" role="status">{len(records)} lectures</p>{''.join(rows)}<p class="empty" id="lecture-empty" hidden>No lectures match. Try another topic or choose all strands.</p><script>
const query=document.querySelector('#lecture-search'),strand=document.querySelector('#lecture-strand'),rows=[...document.querySelectorAll('.lecture-row')];
function filterLectures(){{let count=0;const q=query.value.trim().toLowerCase();rows.forEach(row=>{{const show=row.dataset.search.includes(q)&&(!strand.value||row.dataset.strand===strand.value);row.hidden=!show;if(show)count++;}});document.querySelector('#lecture-count').textContent=count+(count===1?' lecture':' lectures');document.querySelector('#lecture-empty').hidden=count!==0;}}query.addEventListener('input',filterLectures);strand.addEventListener('change',filterLectures);
</script>'''
    (out / 'lectures.html').write_text(shell('Lectures & slides', lectures, 'Lectures & slides'))
    specs = [('A1','Figure brief','After week 2','Explain six opening papers using six evidence ledgers and three paired comparisons. Identify the research question, figure evidence, observation unit and limits of each claim.','a1--first-pass-figure-brief'),('A2','Mechanism experiment','Week 13','Predict a transformation, run a controlled experiment, introduce a meaningful failure, and justify a repair. Return to the motivating paper with a revised interpretation.','a2--mechanism-experiment'),('A3','Figure or table reconstruction','Scope by week 22 · Complete in week 24','Select an exact paper panel or table. Agree on an explanatory reconstruction, reanalysis or computational reproduction, then document the completed scope and run evidence.','a3--figure-or-table-reconstruction-proposal'),('A4','Research review and defense','Weeks 25–26','Connect the literature to a research question and an analysis plan. Defend measurement, QC, modeling and independent evaluation when an assumption changes.','a4--reviewer-response-and-research-proposal')]
    assignments = '<p class="eyebrow">Coursework</p><h1>Assignments</h1><p class="lead">Build a portfolio of evidence, experiments and research decisions. Each assignment develops the independent explanation needed for the final defense.</p>'
    for cid,title,timing,desc,anchor in specs:
        assignments += f'<article class="assignment-row"><p class="eyebrow">{cid}</p><div><h2>{title}</h2><p class="subtle">Suggested checkpoint: {timing}</p><p>{desc}</p><a href="curriculum/coursework/PAPER_TO_EXPERIMENT.html#{anchor}">Specification and rubric</a></div></article>'
    assignments += '<section class="section"><h2>For every computational class</h2><p>Submit a transformation card, a prediction before execution, one intentionally wrong run, a repair with a reason, and a short explanation of what transfers to research.</p><div class="action-row"><a class="course-button" href="course/templates/transformation_card.html">Transformation card</a><a class="course-button" href="curriculum/coursework/EVIDENCE_LEDGER.html">Evidence ledger</a><a class="course-button" href="curriculum/ASSESSMENT.html">Mastery criteria</a></div></section>'
    (out / 'assignments.html').write_text(shell('Assignments',assignments,'Assignments'))
    # Key course documents use the same restrained academic shell. Full computational lessons retain their reader tools.
    documents = [('curriculum/SYLLABUS.md','Syllabus'),('curriculum/papers/README.md','Readings'),('curriculum/SETUP.md','Setup'),('curriculum/ASSESSMENT.md','Assignments'),('curriculum/AI_WORKFLOW.md','Overview')]
    for path,active in documents:
        source=ROOT/path; body,_,_=render(source.read_text(),str(source.relative_to(ROOT).parent),decompose_equations=False)
        dest=out/Path(path).with_suffix('.html')
        dest.write_text(shell(source.read_text().splitlines()[0].removeprefix('# '),'<article class="content-prose">'+body+'</article>',active,'../'*len(Path(path).parent.parts)))


def slide_section(title, content, cid, number, total, kicker='Lecture'):
    return f'<section class="slide" id="slide-{number}" aria-label="Slide {number}: {E(title)}"'+(' hidden' if number>1 else '')+f'><div class="slide-kicker">{E(cid)} / {E(kicker)}</div><h2>{E(title)}</h2>{content}<footer class="slide-footer"><span>Neuroimaging Research Methods with AI</span><span>{number:02d} / {total:02d}</span></footer></section>'


def build_lecture_decks(records,enrichment,papers,out,render):
    slides_dir=out/'slides';slides_dir.mkdir(exist_ok=True)
    figures=out/'assets'/'lecture-figures';figures.mkdir(exist_ok=True)
    for record in records:
        cid=record['id'];info=enrichment[cid];eq=info['equation']
        nb=json.loads((ROOT/record['path']).read_text())
        notebook_href='../'+record['path'].replace('.ipynb','.html')
        deck=[]
        def add(title,content,kicker='Lecture'):
            deck.append((title,content,kicker))
        add(record['title'],f'<p class="cover-meta">Week {info["week"]} · {E(info["phase"])}</p><p>{E(eq["summary"])}</p><p class="caption">Companion materials: <a href="{notebook_href}">complete lesson and experiment</a></p>','Course lecture')
        add('The research question',f'<p>{E(record["title"])}</p><div class="boundary">What would you need to observe to support a claim about this question? Identify the measurement, comparison and evaluation boundary.</div>','Discussion')
        add('Learning goals','<ul>'+''.join(f'<li>{E(term["meaning"])}</li>' for term in eq['terms'][:3])+'</ul>','Concepts')
        # External diagrams remain attributed links, avoiding reliance on remote pixels for classroom use.
        add('The analysis sequence','<ol>'+''.join(f'<li>{E(step)}</li>' for step in info['pipeline_steps'])+'</ol>','Method')
        add(eq['name'],f'<p>{E(eq["summary"])}</p><div class="equation">\\[{E(eq["latex"])}\\]</div>'+ ('<p class="caption">Conceptual teaching framework, not a fitted statistical equation.</p>' if record['execution_tier']=='reading' else ''),'Formulation')
        for term in eq['terms']:
            add(term['role'],f'<div class="formula">\\({E(term["term"])}\\)</div><p>{E(term["meaning"])}</p><div class="boundary"><strong>Failure to inspect</strong><p>{E(term["failure"])}</p></div>','Mechanism')
        # A lesson-specific instruction is preserved as a short source excerpt, without cutting sentences.
        markdown_text='\n\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='markdown')
        selected=[]
        for block in re.split(r'\n\s*\n',markdown_text):
            block=block.strip()
            if not block or block.startswith(('#','<!--','<','|','```')):continue
            if re.search(r'predict|before.*run|change one|intentionally|deliberate',block,re.I) and 35 <= len(block.split()) <= 95:
                selected.append(block)
        if selected:
            text=render(selected[0],str(Path(record['path']).parent),decompose_equations=False)[0]
            text=re.sub(r'href="(?!https?:|#)([^"]+)"',lambda m:f'href="../{Path(record["path"]).parent}/{m[1]}"',text)
            add('Prediction before execution',text+f'<p class="caption">Lesson prompt · <a href="{notebook_href}">Full experiment instructions</a></p>','Notebook lab')
        else:
            add('Prediction before execution',f'<p>Choose one assumption in {E(eq["name"])}. Predict the effect of changing it on the output before running the notebook.</p><ol><li>Name the input and its units.</li><li>Record the parameter or comparison you will change.</li><li>Specify an observable diagnostic that would contradict your prediction.</li></ol>','Notebook lab')
        # Use actual, stored notebook plots as evidence. No synthetic decorative neuroscience imagery.
        figure_found=False
        for cell in nb['cells']:
            for output in cell.get('outputs',[]):
                data=output.get('data',{}).get('image/png')
                if data and not figure_found:
                    filename=f'{cid}.png';(figures/filename).write_bytes(base64.b64decode(''.join(data) if isinstance(data,list) else data))
                    add('Inspect the notebook output',f'<div class="figure-layout"><figure><img src="../assets/lecture-figures/{filename}" alt="Stored diagnostic output from the {cid} notebook"><figcaption class="caption">Reference output from the course notebook. Check the full lesson for the data and run conditions.</figcaption></figure><div><p>Which plotted quantity changes under the operation?</p><p>Identify the axes, units, baseline and visible failure. Compare your own run with this reference.</p><p class="caption"><a href="{notebook_href}">Open the complete analysis</a></p></div></div>','Evidence')
                    figure_found=True
        if not figure_found:
            add('Figure reading and evidence','<ol><li>Locate the assigned figure or table in the paper.</li><li>Name what one observation represents.</li><li>Explain the comparison and the uncertainty shown.</li><li>Write one supported claim and one unanswered question.</li></ol>','Paper seminar')
        failures=''.join(f'<li>{E(t["failure"])}</li>' for t in eq['terms'][:3])
        add('Failure cases to diagnose',f'<ul>{failures}</ul><p class="caption">Choose one case. Explain which diagnostic distinguishes it from a successful run.</p>','Critical evaluation')
        add('The transformation record','<ul><li>Input and output: shape, units, coordinates or time axis.</li><li>Operation: fitted parameters and the population used to estimate them.</li><li>Information: the invariant preserved and the information lost.</li><li>Evidence: a diagnostic, a failed run, and a justified repair.</li></ul><p class="caption"><a href="../course/templates/transformation_card.html">Transformation card template</a></p>','Lab deliverable')
        assigned=[]
        for pid in record.get('paper_ids',[]):
            p=papers[pid]
            guide=p['guide'].replace('.md','.html')
            assigned.append(f'<li><a href="../curriculum/papers/{guide}">{pid} · {E(p["title"])} ({p["year"]})</a></li>')
        for start in range(0,len(assigned),3):
            add('Return to the paper','<ul class="reading-list">'+''.join(assigned[start:start+3])+'</ul><p>How does the mechanism change your interpretation of the assigned figure? Keep the local experiment’s scope separate from the paper’s original analysis.</p>','Readings')
        add('Exit discussion',f'<ol><li>Explain {E(eq["name"])} in your own words.</li><li>Describe one failure you could detect without trusting an AI explanation.</li><li>State what additional evidence the research claim requires.</li></ol><div class="boundary">Next: <a href="{notebook_href}">complete the notebook experiment and source assignment</a>.</div>','Independent explanation')
        total=len(deck);info['slide_count']=total
        content=''.join(slide_section(title,body,cid,i,total,kicker) for i,(title,body,kicker) in enumerate(deck,1))
        page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{cid} · {E(record['title'])} · Lecture slides</title><link rel="stylesheet" href="../assets/slides.css"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"></head><body data-lesson="{cid}"><header class="deck-toolbar"><a href="../lectures.html">All lectures</a><span>{cid} · Week {info['week']}</span><div class="toolbar-actions"><button id="handout" aria-pressed="false">Handout view</button><button id="fullscreen">Fullscreen</button><button id="print">Print / PDF</button></div></header><main class="deck" aria-label="Lecture slides">{content}</main><nav class="deck-controls" aria-label="Slide navigation"><button id="previous">Previous</button><span id="slide-current" role="status" aria-live="polite">1 / {total}</span><input type="range" id="slide-range" min="1" max="{total}" value="1" aria-label="Slide number"><button id="next">Next</button></nav><p class="deck-help">Arrow keys or Page Up / Page Down to navigate. Home / End for first / last slide. <a href="{notebook_href}">Lesson notes</a> · <a href="../{record['path']}" download>Download notebook</a></p><script src="../assets/slides.js" defer></script><script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script><script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '\\\\[', right: '\\\\]', display: true}}, {{left: '\\\\(', right: '\\\\)', display: false}}], throwOnError: false}});"></script></body></html>'''
        (slides_dir/f'{cid}.html').write_text(page)
    manifest=[{'id':r['id'],'title':r['title'],'week':enrichment[r['id']]['week'],'slides':enrichment[r['id']]['slide_count'],'path':f'slides/{r["id"]}.html'} for r in records]
    (slides_dir/'index.json').write_text(json.dumps(manifest,indent=2)+'\n')
