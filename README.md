# alfredowh.github.io

Personal portfolio site — plain HTML/CSS/JS, no build step. Deploys for free
via GitHub Pages once pushed to a repo named `alfredowh.github.io`.

## Structure

- `index.html` — home page (hero, skills, featured projects, experience)
- `projects.html` — full project grid
- `projects/*.html` — one page per project, each with **Images**,
  **Evaluation**, and **Notes** placeholder sections to fill in
- `css/style.css` — shared styles (light/dark mode via `prefers-color-scheme`)
- `js/main.js` — mobile nav toggle
- `assets/images/projects/<slug>/` — drop screenshots/plots here per project
- `assets/cv/` — drop an exported CV PDF here (linked from the hero "Download CV" button)

## Still TODO before publishing

- Add real images to `assets/images/projects/<slug>/` and reference them in
  each project page's `.gallery-grid` (replace the dashed placeholder slots)
- Fill in the `TBD` evaluation numbers and the Notes placeholder blocks
- Add a profile photo at `assets/images/profile.jpg` if desired
- Add a LinkedIn URL (currently marked `<!-- TODO -->` in `index.html`)
- Drop a CV PDF into `assets/cv/`

## Local preview

Open `index.html` directly in a browser, or serve it locally for routing
closer to how GitHub Pages serves it:

```
npx serve .
```

## Publish to GitHub Pages

1. Create a new GitHub repo named exactly `alfredowh.github.io`
2. From this folder: `git init`, `git add .`, `git commit -m "Initial site"`
3. `git remote add origin https://github.com/alfredowh/alfredowh.github.io.git`
4. `git push -u origin main`
5. Site will be live at `https://alfredowh.github.io` within a minute or two
   (Settings → Pages should already show it enabled by default for this repo name)
