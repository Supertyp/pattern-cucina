# Pattern Cucina: project notes for Claude

Read this first when picking the project back up. Keep it up to date at the end of each working session.

## What the project is

- A website that teaches **Italian cooking** through **patterns**: general techniques, each a recurring problem plus a
  solution, covering the whole path from shopping through preparation and cooking to eating and wine pairing.
- **Journeys** are how people learn here: each journey is one dish, cooked by working through the patterns it needs
  in order, with a dish-specific note per step. The user was explicit: **not a conventional cookbook**; the focus is
  on doing it right and learning the techniques.
- A sister site of Pattern Life (`/home/u1018237/pattern_life`, https://supertyp.github.io/pattern-life/), and built
  from a copy of its code (Astro 7.4, Pagefind, same layout and pattern format). Owner: Wolfgang Barth, GitHub user
  **Supertyp**. Australian/British spelling.
- The user asked for **101 patterns**. Planned in `docs/pattern-plan.md` (ids, titles, types, areas, scope) and
  27 journeys in `docs/journey-plan.md`.

## Where it lives

- Local: `/home/u1018237/pattern_life_italian_food` (WSL2). Git repo on branch `main`.
- Planned GitHub repo: `Supertyp/pattern-cucina`, live at https://supertyp.github.io/pattern-cucina/. The `base` in
  `astro.config.mjs` must match the repo name. The user has to create the repo and enable Pages
  (Settings → Pages → Source: GitHub Actions) on github.com; the `gh` CLI isn't installed.
- `.github/workflows/deploy.yml` builds and deploys on every push to `main`.

## Content model

- **Patterns** `src/content/patterns/<id>.md`. Same fixed structure as Pattern Life: Summary (starts "This pattern is
  for …", `| Recommendation | Why? |` table with 3 to 6 rows), Context (suits / does not suit / trade-off), Usage
  (2 to 4 **Bold label:** paragraphs), References (3 to 5 checked links). Types: `ingredient | technique | process |
  preparation | safety | etiquette | pairing`. Patterns are about the skill, never built around one dish (a dish may be
  a passing example). House style in `docs/writing-brief.md`.
- **Areas** (clusters) `src/content/clusters/`: shopping, preparation, fresh-pasta, pasta, sauces, pizza-bread,
  rice-grains, meat-fish, vegetables, dolci, table, wine (ordered from the shop to the table).
- **Journeys** `src/content/journeys/<id>.md` (a content collection, unlike Pattern Life's `journeys.ts`). Frontmatter:
  title, italian, region, course, level (`first steps | building skills | confident cook`), order, time, serves, intro,
  steps (`- pattern: <id>` + `note:`). Body: About the dish / What you need / Where it usually goes wrong. Notes support
  **bold**, *italics*, `[t](../../patterns/<id>/)` and `[t](../<journey-id>/)` (rendered by `inlineMarkdown()` in
  `src/lib/patterns.ts`). Brief: `docs/journey-brief.md`.
- Pattern pages show "Practise it in these journeys" (from `getJourneysByPattern()`); unknown ids fail the build.
- Validators: `python3 scripts/check-patterns.py` and `python3 scripts/check-journeys.py` (the latter also reports
  patterns that no journey uses; currently every pattern is used).

## Conventions and gotchas (same as Pattern Life)

- Internal links in `.astro` files go through `url()` (adds the `/pattern-cucina` base). Markdown links are relative.
- Astro 7 renders Markdown with Sätteri; plugins go in `satteri({ hastPlugins })`. External links open in a new tab.
- `npm run preview` starts a background server; stop it with `npx astro preview stop`.
- Copying `node_modules` from Pattern Life broke the Astro CLI silently (exit 1, no output). `rm -rf node_modules &&
  npm ci` fixed it.
- WebSearch is capped at 200 searches per session, shared by all subagents; it ran out while the patterns were written.
  Many food sites block curl (Serious Eats 402, taste.com.au, Barilla, De Cecco, The Guardian), so references lean on
  Great Italian Chefs, Eataly, Vincenzo's Plate, King Arthur, BBC Good Food, FSANZ / Food Safety Information Council and
  YouTube (checked through oEmbed).

## History

### Session 2026-11-15: site built

- Scaffolded from Pattern Life, rebranded (terracotta accent, "Pattern·Cucina" wordmark), journeys made a collection
  with their own pages, home page rewritten around journeys.
- 101 patterns drafted by 9 parallel subagents from `docs/writing-brief.md`; 27 journeys by 3 subagents from
  `docs/journey-brief.md`. Every reference URL was checked with curl.
- The user hasn't reviewed the content yet.

## Open points

- Facts the writers flagged as uncertain (to review): see the list in the session summary / commit message; the main
  ones are rules-of-thumb numbers (gelatine, yeast %, doneness temperatures, portion sizes, salt-crust ratio) and
  garlic-in-oil storage times.
- Possible AIdea candidates flagged by writers: salt in the wine ice bucket, chilling the blender jug for pesto, 0.1 g
  scale, thermometer ice-water check, dipping the moka pot in cold water, warming bowls at 60 to 70 °C.
- Topics suggested for later patterns: anchovies and capers, preserving sott'olio / sott'aceto (botulism), zabaione and
  crema pasticcera, gelato/semifreddo, octopus, frying batters (pastella), roasting meat (arrosto), soups (minestrone),
  rice safety (Bacillus cereus), ricotta gnocchi, dessert wines, storing opened wine, water at the table, beer with pizza,
  balsamic vinegar, buying meat from a butcher.
- References are thin in places (no videos for shopping and wine patterns) because search ran out; a later pass could
  add Italian and video sources.
