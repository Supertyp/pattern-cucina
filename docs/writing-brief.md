# Writing brief for patterns

Pattern Cucina is a website that teaches Italian cooking through **patterns**: general, reusable techniques, each
described as a recurring problem and a solution that reliably works. It is **not a cookbook**. Patterns are about the
skill, not about one dish. Separate "journeys" (written later) apply the patterns to particular dishes, so a pattern
must be useful for every dish that needs it. A well-known dish may appear as a passing example ("as in a carbonara"),
but never build a pattern's advice around one dish.

The audience: home cooks who want to do it right and understand why. Some are beginners, some are experienced cooks
who want to stop guessing.

## Files

- The master list of all 101 patterns, with ids, titles, types, areas and scope: `docs/pattern-plan.md`.
  Use the **exact title, type and cluster** from the plan. Stay within the scope given there and leave neighbouring
  topics to their own patterns (link to them instead).
- Write each pattern to `src/content/patterns/<id>.md`. Don't touch any other file.
- Format examples (from the sister site, written in the same house style; the dishwasher one is the user's own gold
  standard): `/home/u1018237/pattern_life/src/content/patterns/dishwasher-loading-unloading.md` and
  `/home/u1018237/pattern_life/src/content/patterns/boiling-pasta.md`. Read both before you start. Their ids and
  links don't exist on this site; don't copy those.
- Check your files with `python3 scripts/check-patterns.py <id> <id> ...` and fix everything it reports. Don't run
  `npm run build` (other writers work in the same folder at the same time).

## Frontmatter

```yaml
---
title: Salting the pasta water
type: technique
cluster: pasta
problem: One sentence describing the problem from the cook's point of view (what goes wrong).
appliesWhen:
  - three lowercase items
  - each a situation, not an instruction
  - no full stops
authors: [Pattern Cucina team]
published: 2026-11-15
related: [two-to-five, ids-from-the-plan]
---
```

## Body (fixed structure)

- `## Summary`: starts "This pattern is for … It describes …". Then a `| Recommendation | Why? |` table with **3 to
  6 rows (ideally 4 or 5)**. Each recommendation is concrete (quantities, temperatures, times), and the Why explains
  the reason, ideally the food science, in one or two sentences. Combine related rows and leave how-to detail for Usage.
- `## Context`: three short paragraphs starting "This pattern suits …", "It does not suit …", "There's a trade-off …".
  The trade-off is a real one (tradition vs convenience, flavour vs time, and so on), and says which side this pattern
  takes and when to choose the other.
- `## Usage`: 2 to 4 paragraphs, each starting with a **Bold label:** (for example `**Getting the heat right:**`).
  Practical how-to detail, what it looks, sounds, smells and feels like when it's right, and the common mistakes and
  how to fix them.
- `## References`: 3 to 5 bullets formatted exactly `- [Title](url), Publisher. One sentence on what it shows.`
  (if it's a video, write `Publisher (YouTube).`).

Length: about 450 to 700 words. Second person, plain and friendly, direct. No headings other than the four.

## Linking

- Cross-link generously to other patterns **inline**, using relative links `[Building a soffritto](../building-a-soffritto/)`,
  where the topic is handed off. Use only ids from the plan (others may not be written yet, which is fine).
- `related`: 2 to 5 ids of the closest patterns. Links show up in both directions automatically.
- The Summary table may contain inline links too.

## Style

- Australian/British spelling (colour, flavour, litre, centre, grey, -ise). Metric units and °C. Grams for dry
  ingredients. Give oven temperatures for conventional ovens and mention fan-forced (about 20 °C lower) where it matters.
- No em dashes (—). Use commas, colons, brackets or a new sentence.
- Italian terms in italics with a short translation the first time, e.g. *mantecatura* (beating in butter and cheese).
  Don't overdo Italian.
- Hemisphere-neutral: say "in summer", not month names.
- Neutral and practical about tradition: explain the traditional way and why, then say when deviating is fine.
  Avoid "authentic" policing and avoid national stereotypes.
- Ingredient substitutes for cooks outside Italy are welcome (e.g. pancetta or bacon for guanciale) with their
  trade-offs.

## Facts and safety

- Be accurate. If something is disputed among Italian cooks (oil in the pasta water, cream in carbonara, garlic in
  bolognese), say it's disputed rather than inventing a rule.
- Food safety follows **Food Standards Australia New Zealand (FSANZ)**: e.g. mince, sausages and poultry to 75 °C,
  the 2-hour/4-hour rule, cooling leftovers fast, raw or lightly cooked eggs and vulnerable people (pregnant women,
  young children, older people, people with weakened immunity). Safety advice comes first and is never optional.
- Heat, oil and knives: include the safety essentials where they apply.

## References: real and checked

- 3 to 5 per pattern, from varied, credible sources: Italian institutions and consortia (e.g. Consorzio del
  Parmigiano Reggiano, Associazione Verace Pizza Napoletana, Accademia Italiana della Cucina), producers' sites
  (e.g. Barilla, De Cecco, Caputo, Bialetti), reputable food writing (Serious Eats, The Guardian's Felicity Cloake,
  BBC Good Food, Eataly, Great Italian Chefs, Taste, King Arthur Baking), official guidance (FSANZ, foodsafety.asn.au,
  EU agriculture pages, Sustainable seafood guides) and YouTube videos from good channels (e.g. Pasta Grannies,
  Vincenzo's Plate, Italia Squisita, Gennaro Contaldo, Serious Eats, Kenji López-Alt).
- **Check every URL before you use it**: `curl -sL -o /dev/null -w '%{http_code} %{url_effective}\n' -A 'Mozilla/5.0' <url>`
  must give 200, and fetch the page (`curl -sL -A 'Mozilla/5.0' <url> | grep -io '<title>[^<]*'`) to confirm it's
  the page you mean. For YouTube, check with the oEmbed endpoint:
  `curl -s 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v=<ID>'` and use the
  returned title and author. Use WebSearch to find sources if you need to (load it with ToolSearch "select:WebSearch").
- **Never invent or guess a URL.** If a site blocks curl (403) and you can't confirm it, choose another source.
- Use the page's real title in the link text.

## AIdea badge

The site marks recommendations that are logical on paper but not something people actually do with an "AIdea"
badge. Don't add the badge yourself. Instead, avoid writing such recommendations, and if you're unsure about one,
list it in your final report.

## Your final report

Keep it short: the ids you wrote, the validator result, any fact you're not fully sure of, any possible AIdea
recommendations, and any topic that you think is missing from the plan.
