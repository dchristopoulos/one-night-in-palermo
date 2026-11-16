// Evenings, the scoreboard and a game's place in its evening: node --test src/*.test.ts
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { groupIndex, placeOf, scoreboard, when, won, type GameInfo } from './evenings.ts';

const cast = (killers: string[]) => ['Sonnet', 'Haiku', 'Gemma', 'Sol'].map(name => ({ name, model: 'x', role: killers.includes(name) ? 'killer' as const : 'citizen' as const }));
let clock = 1_000_000;
const g = (name: string, winner: GameInfo['winner'], killers = ['Sonnet'], extra: Partial<GameInfo> = {}): GameInfo => {
  const m = name.match(/^(.+)-(\d+)$/);
  clock += 600;
  return { file: `games/${name}.json`, name, tag: m && !/^\d{8}$/.test(m[1]) ? m[1] : null, n: m && !/^\d{8}$/.test(m[1]) ? Number(m[2]) : null,
    started: clock, mtime: clock + 500, seats: 4, cast: cast(killers), killers, winner, days: 2, minutes: 8, live: false, finished: winner != null, ...extra };
};

test('evenings group by tag in number order, live first, then the most recent; old single games apart', () => {
  const games = [g('fin71-2', 'town'), g('fin71-1', 'killer'), g('20261027-044948', 'town'), g('run81-1', 'killer'), g('run81-2', null, ['Haiku'], { live: true })];
  const { evenings, singles } = groupIndex(games);
  assert.deepEqual(evenings.map(e => e.key), ['run81', 'fin71']);
  assert.deepEqual(evenings[1].games.map(x => x.n), [1, 2]);
  assert.ok(evenings[0].live);
  assert.deepEqual(singles.map(x => x.name), ['20261027-044948']);
});

test('a tag reused by a later sitting starts a new evening', () => {
  const { evenings } = groupIndex([g('tour-1', 'town'), g('tour-2', 'town'), g('tour-1', 'killer')]);
  assert.deepEqual(evenings.map(e => [e.key, e.games.length]).sort(), [['tour#1', 2], ['tour#2', 1]]);
});

test('who won: the side, and the jester alone', () => {
  assert.equal(won('killer', 'killer'), true);
  assert.equal(won('accomplice', 'killer'), true);
  assert.equal(won('officer', 'town'), true);
  assert.equal(won('killer', 'town'), false);
  assert.equal(won('jester', 'town'), false);
  assert.equal(won('jester', 'jester'), true);
  assert.equal(won('citizen', null), false);
});

test('the scoreboard counts finished games only, up to the game being watched', () => {
  const ev = groupIndex([g('e-1', 'killer', ['Sonnet', 'Haiku']), g('e-2', 'town', ['Gemma', 'Sonnet']), g('e-3', 'killer', ['Sol', 'Gemma']),
    g('e-4', 'stopped'), g('e-5', null, ['Sol'], { live: true })]).evenings[0];
  const all = scoreboard(ev);
  assert.deepEqual([all.town, all.killer, all.played], [1, 2, 3]);
  const by = Object.fromEntries(all.players.map(p => [p.name, [p.won, p.killer]]));
  assert.deepEqual(by, { Sonnet: [1, 2], Haiku: [2, 1], Gemma: [1, 2], Sol: [2, 1] });
  assert.equal(all.players[0].name, 'Haiku');                     // most wins, then fewest times killer
  const early = scoreboard(ev, 1);                                  // watching game 2: only game 1 is known
  assert.deepEqual([early.town, early.killer, early.played], [0, 1, 1]);
  assert.deepEqual(scoreboard(ev, 0).players, []);
});

test("a game's place: the evening, the games either side; a single game has none", () => {
  const ix = groupIndex([g('r-1', 'town'), g('r-2', 'killer'), g('r-3', null, ['Sol'], { live: true }), g('20261027-044948', 'town')]);
  const p = placeOf(ix, 'games/r-2.json');
  assert.equal(p.evening?.tag, 'r');
  assert.deepEqual([p.prev?.n, p.game?.n, p.next?.n], [1, 2, 3]);
  const s = placeOf(ix, 'games/20261027-044948.json');
  assert.equal(s.evening, null);
  assert.equal(s.game?.name, '20261027-044948');
  assert.equal(placeOf(ix, 'games/nope.json').game, null);
});

test('an evening is named by its day and the time of day', () => {
  const sat = new Date(2026, 10, 14, 20, 30).getTime() / 1000, now = new Date(2026, 10, 15, 9).getTime() / 1000;
  assert.deepEqual(when(sat, now), { day: 'Yesterday', part: 'evening', time: '20:30' });
  assert.equal(when(sat, sat + 60).day, 'Today');
  assert.match(when(sat, now + 5 * 864e2).day, /^Sat 14 Nov$/);
});
