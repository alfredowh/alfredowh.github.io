---
name: project-showcase
description: Add or update a project showcase card on the personal home page (index.html, projects.html) from a GitHub repo or local project folder, following the owner's wishes (concept only or full, stacks, status such as work in progress, event or hackathon link, no dates). Use when the user asks to show, feature, or add a project to the home page or portfolio.
---

# Project showcase for the personal home page

Turns a project's repo into one card on the portfolio, shaped by the owner's wishes.
The site is plain HTML/CSS/JS with no build step (see `README.md`).

## Inputs

Collect these from the user's request. Ask only if the repo location is missing.

- **Repo**: a local folder (e.g. `~/alfredo/workspace/ANTS`) or a GitHub URL.
- **Wishes** (defaults in brackets):
  - what to show: `concept` and `stack` only [yes], `details` (results, images) [no]
  - status badge, e.g. "Work in progress" [none]
  - event link and label, e.g. Meta Global Hackathon `https://dev.meta.ai/events/global-hackathon` [none]
  - dates [omit]
  - where to place it: featured on `index.html` and `projects.html` [both, first position]

## Steps

1. **Read the repo's facts, do not invent them.**
   - `README.md`: one-line pitch, main idea, the architecture image path.
   - Stack: take it from the manifests that exist (`pyproject.toml`, `package.json`,
     `requirements.txt`, `Cargo.toml`, `go.mod`, ...) and the README. List software only
     (frameworks, models, libraries, tools), not hardware, unless the user asks.
   - Link: GitHub URL from `git remote get-url origin` (convert SSH to HTTPS).
   - Image: a diagram from `docs/images/` or the README, if present.
2. **Copy the image** (if used) to `assets/images/projects/<slug>/`. The slug is the repo name in lowercase with dashes.
3. **Write the card** in the existing card markup (`<div class="card">` with `card-thumb`,
   `card-body`, `card-links`), placed first in `.project-grid` on `index.html` and `projects.html`.
   - Title: `<Name>: <subtitle from README>`.
   - Text: the main concept in 1–2 sentences. No results unless the user asked and they come from logged runs.
   - Stack line: `<p class="stack"><strong>Stack:</strong> ...</p>`.
   - Status: `<span class="badge">Work in progress</span>` inside `.badge-row`.
   - Event: `<span class="badge">...</span>` plus a link in `card-links`.
   - No dates.
4. **Keep the CSS classes** `badge-row`, `badge`, `stack` in `css/style.css`. Add them only if missing.
5. **Check**: `python -m http.server` from the site folder, then confirm the page returns 200
   and the image path resolves. Check that the HTML is well formed (every `<div>` closed).
6. **Report** the files changed and the local preview command. Do not commit or push unless
   the user asks. This repo has no commit rules of its own.

## Rules

- Never add a date unless the user asks for one.
- Keep the card short: one screen of text at most.
- Do not add results, numbers or claims that are not in the repo or the user's wishes.
- Use relative paths for local assets (no leading slash), and `target="_blank" rel="noopener"` for external links.
- Keep the same card in `index.html` and `projects.html`, so the two pages stay in sync.
