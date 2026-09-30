# Course website maintenance

The website is a static build for GitHub Pages. Do not edit generated files in `build/site`.

## Sources

- `curriculum/SYLLABUS.md`: course format, outcomes, assessment and study policies.
- `curriculum/STUDY_PLAN.md`: the 26-week sequence, reading focus and expected evidence.
- `curriculum/notebook_index.json`: class IDs, paths, titles and assigned papers.
- `curriculum/course_enrichment.json`: class week, analysis sequence, equation and explanations.
- `notebooks/`: full experiments and stored diagnostic figures.
- `curriculum/papers/paper_registry.json`: original publication records and reading guides.
- `scripts/course_site.py`: academic pages and browser lecture-deck builder.
- `website/course.css`, `reader.css`, `slides.css`, `slides.js`: appearance and presentation controls.

The lecture builder creates a companion deck for every indexed class, with the method, formulation, mechanisms and failure conditions. It preserves short notebook prediction prompts and the first stored diagnostic plot where available. Seminar decks use figure-reading prompts. The full notebook remains the authority for exact experiment instructions and run conditions. These decks are lecture companions; they are not a substitute for completing the labs or reading the assigned papers.

## Build and verify

```sh
uv run --frozen python scripts/check_repository.py
uv run --frozen python scripts/build_website.py --output build/site
uv run --frozen python scripts/check_course_site.py build/site
python3 -m http.server 8765 --directory build/site
```

Open `http://localhost:8765/`. Check the overview, weekly schedule, lecture filtering, and a reading and computational deck. Check a narrow phone viewport as well as desktop. Decks support Previous / Next, arrow keys, Page Up / Page Down, Home / End, a slide selector, fullscreen and a handout view. Print / PDF includes all slides with landscape print styles.

The builder verifies all relative page links. The course-specific check additionally verifies 83-deck coverage, slide counts, all 26 weeks, local assets and the fragment targets used by the new pages. It runs in the Pages workflow too.

## Publish

In repository **Settings → Pages**, set the publishing source to **GitHub Actions**. The workflow builds on pull requests without publishing, and publishes only `main`. It uploads one artifact and deploys through `actions/deploy-pages`; no generated branch is required. The live site is:

https://bowenislandsong.github.io/ai-neuroimaging-course/

The previous comprehensive materials dashboard remains at `roadmap.html`. All lesson, paper and repository-material URLs remain available.
