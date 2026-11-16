// What this device remembers (DESIGN.md §5, Home): whether Home shows results, and which games were watched to their end card.
// localStorage can be missing or throw (private window, blocked storage): then results stay hidden and nothing is remembered.
const SHOW = 'palermo.results', SEEN = 'palermo.seen';

function get(key: string): string | null {
  try { return localStorage.getItem(key); } catch { return null; }
}
function set(key: string, value: string) {
  try { localStorage.setItem(key, value); } catch { /* not remembered */ }
}

export const showResults = (): boolean => get(SHOW) === 'shown';
export const setShowResults = (on: boolean) => set(SHOW, on ? 'shown' : 'hidden');

export function seenGames(): Set<string> {
  try { const v = JSON.parse(get(SEEN) ?? '[]'); return new Set(Array.isArray(v) ? v.filter(x => typeof x === 'string') : []); } catch { return new Set(); }
}
export function markSeen(file: string) {
  const s = seenGames();
  if (s.has(file)) return;
  s.add(file);
  set(SEEN, JSON.stringify([...s].slice(-500)));
}
