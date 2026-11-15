# Pattern Cucina

A static website that teaches Italian cooking through **patterns** (general techniques, from shopping to wine
pairing) and **journeys** (dishes learnt by working through the patterns they need). Built with
[Astro](https://astro.build/) and [Pagefind](https://pagefind.app/) search. A sister site of
[Pattern Life](https://github.com/Supertyp/pattern-life).

## Commands

| Command | What it does |
| --- | --- |
| `npm install` | Install dependencies |
| `npm run dev` | Local dev server at http://localhost:4321/pattern-cucina/ (search not available) |
| `npm run build` | Build the static site into `dist/` and generate the search index |
| `npm run preview` | Serve the built site in the background, including search (stop with `npx astro preview stop`) |
| `python3 scripts/check-patterns.py` | Check every pattern against the format and `docs/pattern-plan.md` |
| `python3 scripts/check-journeys.py` | Check every journey, and that every pattern is used by at least one journey |

## Adding content

- **Pattern:** a markdown file in `src/content/patterns/`. The file name becomes the URL. See `/contribute/` on the
  site for the template, and `docs/writing-brief.md` for the house style.
- **Journey:** a markdown file in `src/content/journeys/`: one dish, with steps that each name a pattern and say
  what's specific to the dish. See `docs/journey-brief.md`.
- **Area (cluster):** a markdown file in `src/content/clusters/`. A pattern's `cluster` must match its file name.
- **Cross-links:** link to another pattern inside a pattern with `[Title](../other-id/)`, or list ids in `related`.
  Related patterns are shown in both directions, and unknown ids fail the build.

## Deploying

Published by GitHub Actions (`.github/workflows/deploy.yml`) on every push to `main`. The base path is set in
`astro.config.mjs` (`base: '/pattern-cucina'`) and must match the repository name. Internal links in `.astro` files
must go through the `url()` helper in `src/lib/url.ts`.
