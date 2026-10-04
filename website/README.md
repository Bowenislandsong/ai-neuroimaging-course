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

## Search visibility and traffic tracking

The build adds unique descriptions, canonical URLs, Open Graph / social sharing metadata,
a Course structured-data record on the overview, `sitemap.xml`, and `robots.txt`.
`SITE_URL` can override the production URL when moving to a custom domain.

To activate Google integrations, set repository **Settings → Secrets and variables →
Actions → Variables** (these IDs are public, not passwords):

- `GOOGLE_ANALYTICS_ID`: the `G-…` measurement ID from a Google Analytics 4 Web data stream for the live site.
- `GOOGLE_SITE_VERIFICATION`: the content value of the HTML verification meta tag from a Search Console **URL-prefix property** for `https://bowenislandsong.github.io/ai-neuroimaging-course/`.

Run the Pages workflow after configuring these values. Then verify ownership in Search
Console and submit `https://bowenislandsong.github.io/ai-neuroimaging-course/sitemap.xml`.
Use Analytics Realtime to check visits; Search Console reports search impressions,
clicks, queries and indexing. Without a measurement ID, no Analytics script is emitted.
For a local integration check, pass the same variables to the build command.

SEO supports organic discovery; paid promotion is managed separately in Google Ads.

Page titles and search/social descriptions can be edited in `website/seo.json`.
Keys are generated HTML paths. Indexed lessons and lecture decks otherwise derive
metadata from their lesson title and method summary in the curriculum source files.
The same title and description populate search metadata and social sharing tags.

The build also generates `llms.txt`, a Markdown guide to course navigation and all
indexed lessons, and links it from page heads using `rel="describedby"`. This is an
optional AI-reader convention, not a guarantee of inclusion in AI answers.

Robots rules are read at the origin root (`https://bowenislandsong.github.io/robots.txt`),
not the course subdirectory. The generated course `robots.txt` is useful if the course
moves to its own domain; on the current project Pages URL, submit the sitemap directly
in Search Console and manage any crawler rules in the user Pages site's root.
