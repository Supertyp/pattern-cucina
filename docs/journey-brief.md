# Writing brief for journeys

Pattern Cucina teaches Italian cooking through **patterns** (general techniques, in `src/content/patterns/`) and
**journeys**. A journey is one dish: the learner cooks it by working through the patterns it needs, in order. People
learn on this site by following journeys, so journeys are the front door. They are **not recipes in disguise**: the
technique lives in the pattern, and the journey says only what is specific to this dish at each step.

## Files

- The list of journeys, with order, title, Italian name, course, level, region and the planned steps:
  `docs/journey-plan.md`. You may reorder steps, or add or drop one or two where the dish needs it, but keep a step if
  dropping it would leave a pattern used by no journey (the validator reports this when run with no arguments).
- The format: the journey template at the end of `src/pages/contribute.md`.
- **Read every pattern your journey links to** before writing its note, so the note applies that pattern correctly
  and agrees with it (quantities, temperatures, times). Don't repeat the pattern; build on it.
- Write each journey to `src/content/journeys/<id>.md`. Don't touch other files.
- Check with `python3 scripts/check-journeys.py <id> ...` and fix everything it reports. Don't run npm.

## Frontmatter

- `title`, `italian`, `course`, `level`, `region`, `order` exactly as in the plan.
- `time`: realistic total time, including resting or fermenting (e.g. "25 minutes", "3 hours, mostly simmering",
  "2 days, 30 minutes hands-on").
- `serves`: a quoted string, e.g. `"4"` or `"4 to 6"`.
- `intro`: one or two sentences: what the dish is and what the learner practises by cooking it.
- `published: 2026-11-15`.
- `steps`: a list of `- pattern: <id>` with `note: <text>` on the next line, indented 4 spaces. Each note is one line
  of YAML, 1 to 3 sentences (about 20 to 60 words), saying what's **specific to this dish** at this step: the
  quantity, the shape, the timing, the exception to the pattern's rule, what it should look like. Example:
  `note: Use about 7 g salt per litre rather than 10, because the pecorino is salty and the starchy water ends up in the sauce.`
  If a note contains ": " or starts with a quote, wrap the whole note in double quotes (and don't use double quotes
  inside it). The notes can use **bold**, *italics* and links to other patterns written `[text](../../patterns/<id>/)`.

## Body

Three sections, exactly:

- `## About the dish`: one short paragraph: origin, what it should be like when it's right (texture, look, taste),
  and any well-known debate about the "proper" version, stated neutrally.
- `## What you need`: a bullet list of ingredients with metric quantities for the stated servings, plus any
  special equipment in a final bullet ("Equipment: ..."). This is the only recipe-like part.
- `## Where it usually goes wrong`: 2 to 4 bullets: a common failure, its cause, and the step that prevents it,
  linking to the pattern with `[title](../../patterns/<id>/)`.

Length: about 400 to 800 words including the notes.

## Style and facts

- Australian/British spelling, metric, °C (conventional oven; give fan-forced where it matters). No em dashes.
- Second person, plain and friendly, encouraging for learners: say what to look, listen and taste for.
- Be accurate about the dish and its tradition. Where cooks disagree, say so neutrally.
- Food safety follows FSANZ. Where a dish uses raw or lightly cooked eggs (carbonara, tiramisù), say who should avoid
  it and suggest pasteurised eggs; meat temperatures as in the patterns.
- No invented facts. If you name a specific wine style, make sure it's a real one from that region.
- Every journey that ends in a meal should include, or link to, eating and wine where the plan has them.

## Your final report

Keep it short: the ids written, the validator result, any step changes you made compared with the plan, and any
problem you noticed in a pattern you read (factual error, contradiction with another pattern, missing advice the
dish needed). Don't fix patterns yourself; report them.
