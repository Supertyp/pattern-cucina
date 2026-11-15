import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Pattern types: how a pattern helps.
//   ingredient  — choosing, buying, storing or understanding an ingredient
//   technique   — a concrete way of doing something
//   process     — an order of work for a multi-step task
//   preparation — what to plan, set up or check before you start
//   safety      — avoiding harm to people, food or equipment
//   etiquette   — customs at the Italian table
//   pairing     — matching wine or drinks with food
export const PATTERN_TYPES = ['ingredient', 'technique', 'process', 'preparation', 'safety', 'etiquette', 'pairing'] as const;

const patterns = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/patterns' }),
  schema: z.object({
    title: z.string(),
    type: z.enum(PATTERN_TYPES),
    cluster: z.string(),
    problem: z.string(),
    appliesWhen: z.array(z.string()).min(1),
    authors: z.array(z.string()).default(['Pattern Cucina team']),
    editors: z.array(z.string()).default([]),
    // Ids of closely related patterns. Links are shown in both directions on the pattern pages.
    related: z.array(z.string()).default([]),
    published: z.coerce.date(),
    draft: z.boolean().default(false),
  }),
});

const clusters = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/clusters' }),
  schema: z.object({
    title: z.string(),
    framing: z.string(),
    order: z.number().default(100),
  }),
});

// Journeys: one dish each, learnt by working through general patterns in order.
// Each step names a pattern and says what is specific to this dish. Unknown pattern ids fail the build.
export const LEVELS = ['first steps', 'building skills', 'confident cook'] as const;

const journeys = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/journeys' }),
  schema: z.object({
    title: z.string(),
    italian: z.string().optional(),
    region: z.string(),
    course: z.enum(['antipasto', 'primo', 'secondo', 'contorno', 'pizza and bread', 'dolce', 'whole meal']),
    level: z.enum(LEVELS),
    order: z.number(),
    time: z.string(),
    serves: z.string(),
    intro: z.string(),
    steps: z
      .array(z.object({ pattern: z.string(), note: z.string() }))
      .min(4),
    published: z.coerce.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { patterns, clusters, journeys };
