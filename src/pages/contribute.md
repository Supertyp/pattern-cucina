---
layout: ../layouts/PageLayout.astro
title: Contribute
description: Suggest a new pattern or improve an existing one.
---

Pattern Cucina grows through contributions. If you know a technique that reliably works, a correction, or a dish that would make a good journey, we'd like to hear about it.

## Pattern template

Patterns link to each other instead of repeating each other. To link to another pattern inside the text, use a relative link with its id, for example `[Sharp knife, stable board](../sharp-knife-and-stable-board/)`. Links appear automatically in both directions under "Related patterns", and the build fails if a link points to a pattern that doesn't exist.

Each pattern is a markdown file in `src/content/patterns/`. Copy the template below and fill it in.

```markdown
---
title: Short, descriptive name
type: technique        # ingredient | technique | process | preparation | safety | etiquette | pairing
cluster: pasta         # id of an area in src/content/clusters/
problem: One sentence describing the recurring problem.
appliesWhen:
  - first condition
  - second condition
authors: [Your Name]
published: 2026-11-15
related: [other-pattern-id]   # optional: ids of closely related patterns
---

## Summary

This pattern is for <who>. It describes <what the pattern covers>.

| Recommendation | Why? |
| --- | --- |
| What to do. | The reason it works. |

<!-- 3 to 6 recommendations. Combine related ones, and move how-to detail to Usage. -->

## Context

This pattern suits <situations>.

It does not suit <situations where it doesn't apply>.

There's a trade-off with <...>. <Explain the choice this pattern makes.>

## Usage

**First step:** ...

**Second step:** ...

## References

- [Page or video title](https://example.com/), Publisher or channel. What it covers.

<!-- 3 to 5 real sources people can open: producers and consortia, food writing, YouTube videos, official guidance. -->
```

## Journey template

A journey is one dish, learnt by working through general patterns in order. Each journey is a markdown file in `src/content/journeys/`. Every step names a pattern id and a note saying what's specific to this dish. The note is the only place for dish-specific advice; the build fails if a step names a pattern that doesn't exist.

```markdown
---
title: Spaghetti with garlic, oil and chilli
italian: Spaghetti aglio, olio e peperoncino
region: Lazio and Campania
course: primo          # antipasto | primo | secondo | contorno | pizza and bread | dolce | whole meal
level: first steps     # first steps | building skills | confident cook
order: 10              # position in the list of journeys
time: 20 minutes
serves: "2"
intro: One or two sentences on the dish and what you'll learn by cooking it.
published: 2026-11-15
steps:
  - pattern: salting-pasta-water
    note: What's specific to this dish at this step, in one to three sentences.
  - pattern: infusing-oil-with-garlic-and-chilli
    note: ...
---

## About the dish

A short paragraph: where it comes from and what it should be like.

## What you need

- 200 g spaghetti
- ...

## Where it usually goes wrong

- One or two common mistakes and which step prevents them.
```
