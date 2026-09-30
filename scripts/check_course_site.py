#!/usr/bin/env python3
"""Verify course schedule coverage, lecture decks, local assets and new fragment links."""
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=set(); self.links=[]; self.slides=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='section' and 'slide' in a.get('class','').split():self.slides+=1
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag in ('img','script','link'):
            path=a.get('src') or a.get('href')
            if path:self.links.append(path)

root=Path(sys.argv[1] if len(sys.argv)>1 else 'build/site').resolve()
repo=Path(__file__).resolve().parents[1]
records=json.loads((repo/'curriculum/notebook_index.json').read_text())
manifest=json.loads((root/'slides/index.json').read_text())
assert {r['id'] for r in records}=={r['id'] for r in manifest},'Lecture manifest must cover every class'
cache={}
def page(path):
    if path not in cache:cache[path]=Page(path.read_text())
    return cache[path]
checked=0
pages=[root/'index.html',root/'schedule.html',root/'lectures.html',root/'assignments.html',root/'curriculum/SYLLABUS.html']+list((root/'slides').glob('*.html'))
for path in pages:
    p=page(path)
    for href in p.links:
        u=urlsplit(html.unescape(href))
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        assert target.is_relative_to(root),f'Link outside build: {path.name}: {href}'
        assert target.exists(),f'Missing target: {path.name}: {href}'
        if u.fragment and target.suffix=='.html':
            assert unquote(u.fragment) in page(target).ids,f'Missing fragment: {path.name}: {href}'
        checked+=1
for entry in manifest:
    assert page(root/entry['path']).slides==entry['slides']>=12,f'Incomplete deck: {entry["id"]}'
schedule=(root/'schedule.html').read_text()
for week in range(1,27):assert f'id="week-{week}"' in schedule
for r in records:assert f'slides/{r["id"]}.html' in schedule,f'Missing scheduled class: {r["id"]}'
print(f'Course checks passed: {len(manifest)} decks, {sum(r["slides"] for r in manifest)} slides, 26 weeks, {checked} links/assets including fragments.')
