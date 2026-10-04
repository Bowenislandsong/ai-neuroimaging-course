"""Search metadata and optional Google integrations for every generated page."""
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import quote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_URL = 'https://bowenislandsong.github.io/ai-neuroimaging-course/'


def page_metadata(relative, original_title, overrides, lessons):
    if relative in overrides:
        entry = overrides[relative]
        return entry['title'], entry['description']
    if relative in lessons:
        record, summary = lessons[relative]
        kind = 'Lecture Slides' if relative.startswith('slides/') else 'Lesson Notes'
        title = f"{record['title']} | {kind} | Neuroimaging & AI"
        description = f"{record['title']}. {summary}"
    else:
        topic = original_title.removesuffix(' · Neuroimaging Research Methods with AI')
        title = f'{topic} | Neuroimaging & AI Course'
        description = f'{topic}: course material for studying neuroimaging research methods, MRI analysis and AI-assisted research.'
    description = re.sub(r'\s+', ' ', description).strip()
    if len(description) > 180:
        description = description[:177].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
    return title, description


def add_site_discovery(out_dir):
    overrides = json.loads((ROOT / 'website/seo.json').read_text())
    records = json.loads((ROOT / 'curriculum/notebook_index.json').read_text())
    enrichment = json.loads((ROOT / 'curriculum/course_enrichment.json').read_text())
    lessons = {}
    for record in records:
        entry = (record, enrichment[record['id']]['equation']['summary'])
        lessons[record['path'].replace('.ipynb', '.html')] = entry
        lessons[f"slides/{record['id']}.html"] = entry
    base = os.environ.get('SITE_URL', DEFAULT_URL).rstrip('/') + '/'
    parsed = urlsplit(base)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('SITE_URL must be an absolute HTTPS URL without query or fragment')
    measurement = os.environ.get('GOOGLE_ANALYTICS_ID', '').strip()
    if measurement and not re.fullmatch(r'G-[A-Z0-9]+', measurement):
        raise ValueError('GOOGLE_ANALYTICS_ID must be a GA4 measurement ID (G-…)')
    verification = os.environ.get('GOOGLE_SITE_VERIFICATION', '').strip()
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    sitemap = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for path in sorted(out_dir.rglob('*.html')):
        content = path.read_text()
        relative = path.relative_to(out_dir).as_posix()
        url = base + ('' if relative == 'index.html' else quote(relative, safe='/'))
        match = re.search(r'<title>(.*?)</title>', content, re.S)
        title = html.unescape(re.sub(r'<[^>]+>', '', match.group(1))) if match else 'Neuroimaging Research Methods with AI'
        title, description = page_metadata(relative, title, overrides, lessons)
        content = re.sub(r'<title>.*?</title>', lambda _: '<title>' + html.escape(title) + '</title>', content, count=1, flags=re.S)
        content = re.sub(r'<meta\s+name="description"[^>]*>', '', content, flags=re.I)
        esc = lambda value: html.escape(value, quote=True)
        tags = [f'<meta name="description" content="{esc(description)}">',
                f'<link rel="canonical" href="{esc(url)}">',
                f'<link rel="describedby" href="{esc(base)}llms.txt" type="text/markdown">',
                '<meta property="og:type" content="website">',
                f'<meta property="og:title" content="{esc(title)}">',
                f'<meta property="og:description" content="{esc(description)}">',
                f'<meta property="og:url" content="{esc(url)}">',
                '<meta name="twitter:card" content="summary">',
                f'<meta name="twitter:title" content="{esc(title)}">',
                f'<meta name="twitter:description" content="{esc(description)}">']
        if verification:
            tags.append(f'<meta name="google-site-verification" content="{esc(verification)}">')
        if measurement:
            tags.extend([f'<script async src="https://www.googletagmanager.com/gtag/js?id={measurement}"></script>',
                         '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config",' + json.dumps(measurement) + ');</script>'])
        if relative == 'index.html':
            course = {'@context': 'https://schema.org', '@type': 'Course', 'name': 'Neuroimaging Research Methods with AI', 'description': description, 'url': url, 'isAccessibleForFree': True, 'inLanguage': 'en'}
            tags.append('<script type="application/ld+json">' + json.dumps(course).replace('<', '\\u003c') + '</script>')
        content = content.replace('</head>', '\n' + '\n'.join(tags) + '\n</head>', 1)
        path.write_text(content)
        node = ET.SubElement(sitemap, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        ET.SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = url
    ET.ElementTree(sitemap).write(out_dir / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (out_dir / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n')

    guide = [
        '# Neuroimaging Research Methods with AI',
        '',
        '> Free, open 26-week course on structural, functional and diffusion MRI, research design, Python data science and computational modeling.',
        '',
        'Lecture slides introduce methods; lesson notes and downloadable Jupyter notebooks provide experiments. Reading seminars connect methods to published research. Weeks are relative to the learner’s start date.',
        '',
        '## Course navigation',
    ]
    for relative, label in [('index.html', 'Course overview'), ('curriculum/SYLLABUS.html', 'Syllabus and learning outcomes'), ('curriculum/SETUP.html', 'Environment setup'), ('schedule.html', '26-week schedule'), ('lectures.html', 'Lecture and notebook index'), ('assignments.html', 'Assignments and rubrics'), ('curriculum/papers/README.html', 'Research paper library')]:
        if (out_dir / relative).exists():
            guide.append(f'- [{label}]({base}{relative})')
    guide.extend(['', '## Lessons'])
    for record in records:
        relative = record['path'].replace('.ipynb', '.html')
        if (out_dir / relative).exists():
            guide.append(f"- [{record['id']}: {record['title']}]({base}{quote(relative, safe='/')}): {enrichment[record['id']]['equation']['summary']}")
    (out_dir / 'llms.txt').write_text('\n'.join(guide) + '\n')
