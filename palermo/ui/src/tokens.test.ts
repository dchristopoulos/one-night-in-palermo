// WCAG AA over the token file: every text/background pair the components use, in both themes (DESIGN.md §2.3).
// Both themes are dark; the cream card is the one light surface and carries its own ink set.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const css = readFileSync(new URL('./tokens.css', import.meta.url), 'utf8');
const block = (sel: string) => Object.fromEntries([...css.split(sel + ' {')[1].split('}')[0].matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m => [m[1], m[2].trim()]));
const root = block(':root'), day = block(':root, [data-theme="day"]'), night = block('[data-theme="night"]');

function hex(theme: Record<string, string>, name: string): string {
  const v = theme[name] ?? day[name] ?? root[name];   // night inherits what it does not redefine from the day block
  const ref = v?.match(/^var\(--([\w-]+)\)$/);
  return ref ? hex(theme, ref[1]) : v;
}
function lum(h: string) {
  const c = [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255).map(x => (x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
const ratio = (a: string, b: string) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

// [text, background]
const pairs = [
  ['text', 'bg'], ['text', 'surface'], ['text', 'surface-2'], ['text-muted', 'bg'], ['text-muted', 'surface'], ['text-muted', 'surface-2'],
  ['accent-strong', 'bg'], ['accent-strong', 'surface'], ['on-accent', 'accent-strong'], ['on-highlight', 'highlight'],
  ['thought-text', 'thought-bg'],
];

for (const [label, theme] of [['day', day], ['night', night]] as const) {
  test(`${label}: text pairs pass AA`, () => {
    for (const [fg, bg] of pairs) {
      const r = ratio(hex(theme, fg), hex(theme, bg));
      assert.ok(r >= 4.5, `${label} ${fg} on ${bg}: ${r.toFixed(2)}`);
    }
  });
}

test('seat colours: the bright set reads on every dark surface, the deep set on the cream card', () => {
  for (let i = 0; i < 7; i++) {
    for (const [label, theme] of [['day', day], ['night', night]] as const) for (const bg of ['bg', 'surface', 'surface-2']) {
      const r = ratio(hex(theme, `seat-${i}`), hex(theme, bg));
      assert.ok(r >= 4.5, `${label} seat-${i} on ${bg}: ${r.toFixed(2)}`);
    }
    for (const bg of ['cream', 'cream-dim']) {
      const r = ratio(hex(root, `seat-deep-${i}`), hex(root, bg));
      assert.ok(r >= 4.5, `seat-deep-${i} on ${bg}: ${r.toFixed(2)}`);
    }
  }
});

test('the cream card and the note: ink, soft ink and the deep coral (Card.module.css swaps these in)', () => {
  for (const fg of ['ink', 'ink-soft', 'coral-deep']) for (const bg of ['cream', 'cream-dim']) {
    const r = ratio(hex(root, fg), hex(root, bg));
    assert.ok(r >= 4.5, `${fg} on ${bg}: ${r.toFixed(2)}`);
  }
});

test('result and role colours on the dark surfaces (mint for the town, coral for the killers, sky, gold)', () => {
  for (const [label, theme] of [['day', day], ['night', night]] as const)
    for (const fg of ['ok', 'accent-strong', 'info', 'highlight']) for (const bg of ['bg', 'surface', 'surface-2']) {
      const r = ratio(hex(theme, fg), hex(theme, bg));
      assert.ok(r >= 4.5, `${label} ${fg} on ${bg}: ${r.toFixed(2)}`);
    }
});
