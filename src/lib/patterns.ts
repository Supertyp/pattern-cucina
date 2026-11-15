import { getCollection, type CollectionEntry } from 'astro:content';

export type Pattern = CollectionEntry<'patterns'>;
export type Cluster = CollectionEntry<'clusters'>;

export async function getPatterns(): Promise<Pattern[]> {
  const all = await getCollection('patterns', ({ data }) => !data.draft);
  return all.sort((a, b) => a.data.title.localeCompare(b.data.title));
}

export async function getClusters(): Promise<Cluster[]> {
  const all = await getCollection('clusters');
  return all.sort((a, b) => a.data.order - b.data.order || a.data.title.localeCompare(b.data.title));
}

/** Clusters paired with their (non-draft) patterns; empty clusters are dropped. */
export async function getClusterGroups() {
  const [clusters, patterns] = await Promise.all([getClusters(), getPatterns()]);
  return clusters
    .map((cluster) => ({ cluster, patterns: patterns.filter((p) => p.data.cluster === cluster.id) }))
    .filter((group) => group.patterns.length > 0);
}

// Inline cross-links in pattern bodies are written as relative links: [text](../other-pattern/)
const INLINE_LINK = /\]\(\.\.\/([a-z0-9-]+)\/(?:#[^)]*)?\)/g;

/** Ids a pattern points to, via its `related` field or inline links in its body. */
function outgoingIds(pattern: Pattern): Set<string> {
  const ids = new Set(pattern.data.related);
  for (const match of (pattern.body ?? '').matchAll(INLINE_LINK)) ids.add(match[1]);
  ids.delete(pattern.id);
  return ids;
}

/**
 * Related patterns for every pattern, in both directions: what it points to, plus everything that points to it.
 * Throws if a `related` id or inline link names a pattern that doesn't exist, so broken links fail the build.
 */
export async function getRelatedMap(): Promise<Map<string, Pattern[]>> {
  const patterns = await getPatterns();
  const byId = new Map(patterns.map((p) => [p.id, p]));
  const related = new Map(patterns.map((p) => [p.id, new Set<string>()]));
  for (const p of patterns) {
    for (const id of outgoingIds(p)) {
      if (!byId.has(id)) throw new Error(`Pattern "${p.id}" links to unknown pattern "${id}"`);
      related.get(p.id)!.add(id);
      related.get(id)!.add(p.id);
    }
  }
  return new Map(
    [...related].map(([id, ids]) => [id, [...ids].map((r) => byId.get(r)!).sort((a, b) => a.data.title.localeCompare(b.data.title))]),
  );
}

export type Journey = CollectionEntry<'journeys'>;

/** Journeys in learning order. Throws if a step names a pattern that doesn't exist. */
export async function getJourneys(): Promise<Journey[]> {
  const [all, patterns] = await Promise.all([getCollection('journeys', ({ data }) => !data.draft), getPatterns()]);
  const ids = new Set(patterns.map((p) => p.id));
  for (const j of all) {
    for (const step of j.data.steps) {
      if (!ids.has(step.pattern)) throw new Error(`Journey "${j.id}" refers to unknown pattern "${step.pattern}"`);
    }
  }
  return all.sort((a, b) => a.data.order - b.data.order);
}

/** For every pattern id, the journeys that use it. */
export async function getJourneysByPattern(): Promise<Map<string, Journey[]>> {
  const map = new Map<string, Journey[]>();
  for (const j of await getJourneys()) {
    for (const step of j.data.steps) {
      const list = map.get(step.pattern) ?? [];
      if (!list.includes(j)) list.push(j);
      map.set(step.pattern, list);
    }
  }
  return map;
}

/** Inline markdown for short notes: links, bold and italics only. Notes are written by us, not by visitors. */
export function inlineMarkdown(
  text: string,
  patternHref: (id: string) => string,
  journeyHref: (id: string) => string,
): string {
  const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return escaped
    .replace(/\[([^\]]+)\]\(\.\.\/\.\.\/patterns\/([a-z0-9-]+)\/\)/g, (_, t, id) => `<a href="${patternHref(id)}">${t}</a>`)
    .replace(/\[([^\]]+)\]\(\.\.\/([a-z0-9-]+)\/\)/g, (_, t, id) => `<a href="${journeyHref(id)}">${t}</a>`)
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}
