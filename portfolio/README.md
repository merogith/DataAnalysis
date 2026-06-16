# Portfolio landing page

This folder holds a simple, fast, framework-free web version of the portfolio.

## Files
- **`index.html`** — a self-contained landing page (all CSS is inline; no build step, no
  dependencies, no JavaScript). It introduces the analyst, summarises all three projects with a
  one-line hook + key result + tech stack, lists the skills demonstrated, and links to each
  project's notebook, write-up, and dashboard guide.

## How to view it
- **Locally:** just double-click `index.html`, or open it in any browser
  (`file:///.../portfolio/index.html`). No server needed.
- **On the web (free):** push this repo to GitHub and enable **GitHub Pages**
  (Settings → Pages → Branch: your branch → `/root` or `/docs`). The page will be served at
  `https://<your-username>.github.io/<repo>/portfolio/`.

## Notes
- The links use **relative paths** (`../project-3-finance/...`) so they work both locally and on
  GitHub once the repository is published.
- The main GitHub landing page is the repository's root [`README.md`](../README.md); this HTML
  page is the polished visual companion you can link from a résumé.
- Edit the name/email/contact line near the top of `index.html` if you'd like to personalise it
  further.
