# Vinay's Newsletter

A weekly digest of posts Vinay bookmarked on X. This repository is a static site served by GitHub Pages from the root of `main` at <https://vinayshah1998.github.io/vinays-newsletter/>.

Pages must be set to deploy from the `main` branch and the `/` (root) folder. `.nojekyll` is an empty file so GitHub Pages serves the HTML as-is and does not run Jekyll. There is no GitHub Actions workflow and no build step on Pages. `index.html` in the repo is the page that gets served.

Use relative links only (`issues/2026-10-18.html`, not `/issues/2026-10-18.html` or a full GitHub Pages URL) so the same files work at the project-site path above.

## Add an issue

Issues are named by publication date in `YYYY-MM-DD` form, for example `2026-10-25`. There are no issue numbers.

1. Add both files:

   - `issues/YYYY-MM-DD.html` — the self-contained issue page (inline CSS, no JavaScript).
   - `issues/YYYY-MM-DD.md` — the same issue in Markdown.

2. Add one object to the `issues` array in `issues.json`. Order in the file does not matter; the index sorts newest first by `date`.

```json
{
  "date": "2026-10-25",
  "title": "Bookmark Digest, Oct 25, 2026: Title Goes Here",
  "coverage": "Oct 19–24, 2026",
  "dek": "One or two sentences from the issue standfirst.",
  "bookmarks": 20
}
```

`date` is a unique `YYYY-MM-DD` string. `title` and `coverage` are required strings. `dek` is an optional string. `bookmarks` is an optional non-negative integer. The script derives the link from the date (`issues/2026-10-25.html`). Both the `.html` and `.md` files must already exist or the script exits with an error.

3. Rebuild the front page and commit the output with the new files:

```bash
python3 scripts/build-index.py
git add issues.json issues/2026-10-25.html issues/2026-10-25.md index.html
git commit -m "Add Bookmark Digest for Oct 25, 2026"
git push origin main
```

`python3 scripts/build-index.py --check` exits non-zero if `index.html` does not match `issues.json`.

The script rewrites the block between these comments in `index.html`:

```html
<!-- BEGIN issues: generated from issues.json by scripts/build-index.py. Newest first. -->
<!-- END issues -->
```

Do not edit that block by hand. The next run replaces it. For reference, this is the entry the script writes (the newest issue gets `class="story lead"`; older ones get `class="story"`):

```html
<article class="story lead">
<p class="kicker">Oct 25, 2026</p>
<h3><a href="issues/2026-10-25.html">Bookmark Digest, Oct 25, 2026: Title Goes Here</a></h3>
<p class="meta"><span class="who">Oct 19–24, 2026</span><span class="sep" aria-hidden="true">·</span><span>20 bookmarks</span></p>
<p class="dek">One or two sentences from the issue standfirst.</p>
</article>
```

The headline `href` is the only link in the entry. It is relative and must point at the HTML file from step 1.

## Layout

| File | Role |
| --- | --- |
| `index.html` | Front page, generated |
| `issues.json` | Issue manifest |
| `scripts/build-index.py` | Regenerates `index.html` |
| `issues/YYYY-MM-DD.html` | Issue page |
| `issues/YYYY-MM-DD.md` | Issue source in Markdown |
| `issues/issue-01.html` | Redirect from the old numbered URL to `2026-10-18.html` |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll |
