# Vinay's Newsletter

A weekly digest of posts Vinay bookmarked on X. This repository is a static site served by GitHub Pages from the root of `main` at <https://vinayshah1998.github.io/vinays-newsletter/>.

Pages must be set to deploy from the `main` branch and the `/` (root) folder. `.nojekyll` is an empty file so GitHub Pages serves the HTML as-is and does not run Jekyll. There is no GitHub Actions workflow and no build step on Pages. `index.html` in the repo is the page that gets served.

Use relative links only (`issues/issue-01.html`, not `/issues/issue-01.html` or a full GitHub Pages URL) so the same files work at the project-site path above.

## Add an issue

File names are zero-padded to at least two digits. Issue 1 is `01`, issue 2 is `02`, issue 10 is `10`.

1. Add both files:

   - `issues/issue-NN.html` — the self-contained issue page (inline CSS, no JavaScript).
   - `issues/issue-NN.md` — the same issue in Markdown.

2. Add one object to the `issues` array in `issues.json`. Order in the file does not matter; the index sorts newest first by `number`.

```json
{
  "number": 2,
  "title": "Bookmark Digest, Issue #2: Title Goes Here",
  "coverage": "Oct 19–24, 2026",
  "dek": "One or two sentences from the issue standfirst.",
  "bookmarks": 20
}
```

`number` is a positive integer. `title` and `coverage` are required strings. `dek` is an optional string. `bookmarks` is an optional non-negative integer. The script derives the link from the number (`issues/issue-02.html`). Both the `.html` and `.md` files must already exist or the script exits with an error.

3. Rebuild the front page and commit the output with the new files:

```bash
python3 scripts/build-index.py
git add issues.json issues/issue-02.html issues/issue-02.md index.html
git commit -m "Add Bookmark Digest issue 2"
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
<p class="kicker">Issue #2</p>
<h3><a href="issues/issue-02.html">Bookmark Digest, Issue #2: Title Goes Here</a></h3>
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
| `issues/issue-NN.html` | Issue page |
| `issues/issue-NN.md` | Issue source in Markdown |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll |
