// The saved games as a person thinks of them (DESIGN.md §5 Home): evenings of numbered games, a scoreboard per evening,
// and the old single games. Pure functions over games/index.json (view.py builds it).
import type { Role, Winner } from './game.ts';

export interface GameInfo {
  file: string; name: string; tag: string | null; n: number | null;
  started: number; mtime: number;                     // epoch seconds: the first event, the last write
  seats: number; cast: { name: string; model: string; role: Role }[]; killers: string[];
  winner: Winner | null; days: number; minutes: number; live: boolean; finished: boolean;
  fun?: { score: number; why: string; quote?: { name: string; text: string } };   // the fun meter (funmeter.py), when the game was scored
}
export interface Evening { key: string; tag: string; games: GameInfo[]; started: number; live: boolean }

// group by tag; games come back in number order. A tag reused by a later sitting (its numbers start again) is a new evening.
export function groupIndex(games: GameInfo[]): { evenings: Evening[]; singles: GameInfo[] } {
  const byTag = new Map<string, GameInfo[][]>();
  const singles: GameInfo[] = [];
  for (const g of [...games].sort((a, b) => a.started - b.started)) {
    if (!g.tag || g.n == null) { singles.push(g); continue; }
    const runs = byTag.get(g.tag) ?? [];
    const cur = runs[runs.length - 1];
    if (cur && !cur.some(x => x.n === g.n)) cur.push(g); else runs.push([g]);
    byTag.set(g.tag, runs);
  }
  const evenings = [...byTag.entries()].flatMap(([tag, runs]) => runs.map((gs, i) => {
    const sorted = gs.sort((a, b) => a.n! - b.n!);
    return { key: runs.length > 1 ? `${tag}#${i + 1}` : tag, tag, games: sorted, started: Math.min(...sorted.map(g => g.started)), live: sorted.some(g => g.live) };
  }));
  const latest = (e: Evening) => Math.max(...e.games.map(g => g.mtime));
  evenings.sort((a, b) => Number(b.live) - Number(a.live) || latest(b) - latest(a));
  singles.sort((a, b) => b.started - a.started);
  return { evenings, singles };
}

export const killerSide = (role: string) => role === 'killer' || role === 'accomplice';
export const won = (role: string, winner: Winner | null) =>
  winner === 'killer' ? killerSide(role) : winner === 'town' ? !killerSide(role) && role !== 'jester' : winner === 'jester' ? role === 'jester' : false;

export interface Score { town: number; killer: number; other: number; played: number;
  players: { name: string; won: number; killer: number; played: number }[] }

// the evening so far: only finished games, and only those the viewer may know about (`upTo`: game numbers ≤ upTo).
// Watching game 3, pass upTo 2 (or 3 once its end card is up): later results never show.
export function scoreboard(evening: Evening, upTo = Infinity): Score {
  const done = evening.games.filter(g => g.finished && g.n != null && g.n <= upTo && g.winner && g.winner !== 'stopped');
  const players = new Map<string, Score['players'][number]>();
  for (const g of done) for (const p of g.cast) {
    const s = players.get(p.name) ?? { name: p.name, won: 0, killer: 0, played: 0 };
    s.played++; if (won(p.role, g.winner)) s.won++; if (killerSide(p.role)) s.killer++;
    players.set(p.name, s);
  }
  return {
    town: done.filter(g => g.winner === 'town').length, killer: done.filter(g => g.winner === 'killer').length,
    other: done.filter(g => g.winner !== 'town' && g.winner !== 'killer').length, played: done.length,
    players: [...players.values()].sort((a, b) => b.won - a.won || a.killer - b.killer || a.name.localeCompare(b.name)),
  };
}

// where a game sits in its evening: "Game 3 of 12", the games either side
export function placeOf(index: { evenings: Evening[]; singles: GameInfo[] }, file: string) {
  for (const e of index.evenings) {
    const i = e.games.findIndex(g => g.file === file);
    if (i >= 0) return { evening: e, game: e.games[i], prev: e.games[i - 1] ?? null, next: e.games[i + 1] ?? null };
  }
  const game = index.singles.find(g => g.file === file) ?? null;
  return { evening: null, game, prev: null, next: null };
}

// "Saturday 15 November", "evening" (a sitting is named by the day it started and the time of day)
export function when(epoch: number, now = Date.now() / 1000) {
  const d = new Date(epoch * 1000), h = d.getHours();
  const part = h < 5 ? 'night' : h < 12 ? 'morning' : h < 17 ? 'afternoon' : h < 22 ? 'evening' : 'night';
  const days = Math.floor((new Date(now * 1000).setHours(0, 0, 0, 0) - new Date(d).setHours(0, 0, 0, 0)) / 864e5);
  const day = days === 0 ? 'Today' : days === 1 ? 'Yesterday'
    : d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' })   // Sat 14 Nov;
  return { day, part, time: d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) };
}

export const winnerWord = (g: Pick<GameInfo, 'winner' | 'live'>) =>
  g.live ? 'playing now' : g.winner === 'town' ? 'Town wins' : g.winner === 'killer' ? 'Killers win' : g.winner === 'jester' ? 'Jester wins' : 'Stopped';
