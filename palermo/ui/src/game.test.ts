// The reducer against saved games (three six-seat, one old lean game, the seven-seat fixture, r5a-1 from the 2026-11-15 engine): node --test src/*.test.ts
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { closingIndex, closingLine, initial, isHighlight, logEntries, modelName, pace, reduce, replay, stops, voteGroups, type GameEvent, type TableState } from './game.ts';

const load = (name: string): GameEvent[] => JSON.parse(readFileSync(new URL(`../../games/${name}.json`, import.meta.url), 'utf8'));
const games = { showcase: load('archive/showcase'), 'reh-3': load('archive/reh-3'), 'val-1': load('archive/val-1'), 'lean3-1': load('archive/lean3-1'), fixture: load('ui-fixture-7'), 'r5a-1': load('r5a-1') };   // r5a-1: no doctor on night 1, day 1 cut short at 8 of 30
const seat = (s: TableState, name: string) => s.seats.find(x => x.name === name)!;
const freeze = <T>(o: T): T => { if (o && typeof o === 'object' && !Object.isFrozen(o)) { Object.freeze(o); Object.values(o).forEach(freeze); } return o; };

for (const [name, events] of Object.entries(games)) {
  test(`${name}: pure; every state frozen, nothing mutated`, () => {
    freeze(events);
    let s = freeze(initial);
    for (const ev of events) s = freeze(reduce(s, ev));   // a mutation of a frozen state throws in strict mode
    assert.deepEqual(s, replay(events));
  });

  test(`${name}: the end state matches the engine's`, () => {
    const s = replay(events), deaths = events.filter(e => e.type === 'death');
    const end = events.at(-1)!, recap = events.findLast(e => e.type === 'recap');
    assert.equal(s.winner, end.type === 'end' ? end.winner : 'no end event');
    assert.equal(s.recap, recap?.type === 'recap' ? recap.text : 'no recap event');
    assert.deepEqual(s.seats.filter(x => x.dead).map(x => x.name).sort(), deaths.map(d => d.type === 'death' && d.name).sort());
    for (const d of deaths) if (d.type === 'death') assert.equal(seat(s, d.name).revealed, d.role !== null, `${d.name} revealed`);
    const days = events.flatMap(e => (e.type === 'phase' && e.kind === 'day' ? (e.text.match(/\d+/) ?? []).map(Number) : []));
    assert.equal(s.day, Math.max(...days));
  });

  test(`${name}: the vote-out is the seat with the most votes on the table`, () => {
    let s = initial, last: TableState | null = null, checked = 0;
    for (const ev of events) {
      if (ev.type === 'votes') {
        const after = reduce(s, ev);
        const weight = ev.votes.reduce((n, [a]) => n + (ev.weights?.[a] || 1), 0);
        assert.equal(after.seats.reduce((n, x) => n + (x.tally?.count ?? 0), 0), weight, 'every ballot lands, the mayor twice');
        assert.ok(after.seats.every(x => !x.tally || x.tally.voters.length === x.tally.count), 'one face per vote');
        last = after;
      }
      if (ev.type === 'death' && ev.how === 'vote') {
        const top = [...last!.seats].sort((a, b) => (b.tally?.count ?? 0) - (a.tally?.count ?? 0));
        assert.equal(top[0].name, ev.name);
        assert.ok((top[0].tally?.count ?? 0) > (top[1].tally?.count ?? 0), 'a vote-out is never a tie');
        checked++;
      }
      s = reduce(s, ev);
      if (ev.type === 'phase') {
        assert.ok(s.seats.every(x => !x.lean && !x.tally && !x.ring), 'a new phase clears the table');
      }
    }
    assert.ok(checked > 0);
  });
}

test('showcase: the officer claims with her thought, the killer counter-claims', () => {
  const ev = games.showcase;
  let s = replay(ev, 71);                                   // event 70: Terra thinks (not a stop: it folds into her line)
  assert.deepEqual(s.thought, { name: 'Terra', text: 'I have to say it before they bury me.' });
  assert.ok(!stops(ev).includes(70) && stops(ev).includes(71));
  s = replay(ev, 72);                                       // event 71: the claim, answering Sonnet, her thought kept
  assert.equal(seat(s, 'Terra').ring, 'speaking');
  assert.equal(seat(s, 'Sonnet').ring, 'addressed');
  assert.equal(s.thought?.name, 'Terra');
  assert.deepEqual(s.bubble, { kind: 'say', name: 'Terra', text: "I'm the officer. Sol is a killer; vote Sol.", why: undefined, replyTo: 'Sonnet' });
  assert.equal(s.seats.filter(x => x.ring).length, 2, 'only the speaker and the addressed are lit');
  s = replay(ev, 136);                                      // event 135: day-1 vote, the mayor counts double
  assert.deepEqual(seat(s, 'Terra').tally, { count: 6, voters: ['Sonnet', 'Sonnet', 'Haiku', 'Gemma', 'Sol', 'Luna'], secret: false });
  assert.equal(s.bubble?.kind === 'votes' && s.bubble.groups.map(g => `${g.target} ${g.count}`).join(' · '), 'Terra 6 · Sol 1');
  s = replay(ev, 139);                                      // event 138: Terra is out, the officer
  assert.deepEqual(s.bubble, { kind: 'death', name: 'Terra', role: 'officer', how: 'vote' });
  assert.ok(seat(s, 'Terra').dead && seat(s, 'Terra').revealed);
  assert.deepEqual(seat(s, 'Terra').out, { how: 'vote', when: 'Day 1' });
  assert.equal(seat(s, 'Terra').tally?.count, 6, 'the tally stays up through the death until the phase changes');
  const k = replay(ev, 151);                                // event 150: Sonnet killed, role hidden
  assert.deepEqual(k.bubble, { kind: 'death', name: 'Sonnet', role: null, how: 'night' });
  assert.ok(seat(k, 'Sonnet').dead && !seat(k, 'Sonnet').revealed);
});

test('val-1: a dead killer still whispers, and the bubble says so', () => {
  const ev = games['val-1'], i = ev.findIndex((e, k) => e.type === 'whisper' && ev.slice(0, k).some(d => d.type === 'death' && d.name === e.name));
  assert.ok(i > 0);
  const b = replay(ev, i + 1).bubble;
  assert.ok(b?.kind === 'whisper' && b.out);
  assert.ok(!('out' in replay(ev, 72).bubble!), 'the living are not out');
});

// the seven-seat fixture: the new line types
const fx = games.fixture, find = (f: (e: GameEvent) => boolean) => fx.findIndex(f);

test('fixture: seven seats, the opening beat before night 1', () => {
  const i = find(e => e.type === 'say' && e.why === 'before the game');
  const s = replay(fx, i + 1);
  assert.equal(s.seats.length, 7);
  assert.equal(s.killers, 2);
  assert.deepEqual(s.phase, { text: 'Before the game', kind: 'day' });
  assert.equal(s.bubble?.kind === 'say' && s.bubble.why, 'before the game');
  assert.equal(replay(fx, find(e => e.type === 'phase') + 1).phase?.text, 'Night 1');
});

test('fixture: a night death turns the card, then the note (no host aside after a death)', () => {
  const d = find(e => e.type === 'death' && e.name === 'Opus');
  assert.deepEqual(replay(fx, d + 1).bubble, { kind: 'death', name: 'Opus', role: 'citizen', how: 'night' });
  assert.ok(seat(replay(fx, d + 1), 'Opus').revealed);
  assert.equal(fx.filter(e => e.type === 'gm' && e.aside).length, 1, 'one aside: the closing one');
  const n = find(e => e.type === 'note');
  const s = replay(fx, n + 1);
  assert.deepEqual(s.bubble, { kind: 'note', name: 'Opus', text: "Night one kills the loud citizen — officer, speak early, you won't get a second morning." });
  assert.ok(s.seats.every(x => !x.ring), 'a note is paper: nobody at the table speaks');
  assert.ok(seat(s, 'Opus').revealed, 'the seat keeps the turned card');
});

test('fixture: lean and claim at the seats', () => {
  const c = find(e => e.type === 'say' && !!e.claim);
  const s = replay(fx, c + 1);
  assert.equal(seat(s, 'Terra').claim, 'officer');
  assert.equal(seat(s, 'Terra').lean, 'Sol');
  const v = find(e => e.type === 'votes');
  const before = replay(fx, v);
  assert.ok(before.seats.filter(x => x.lean === 'Terra').length >= 3, 'the pile builds on Terra before the vote');
  assert.equal(replay(fx, find(e => e.type === 'phase' && e.text === 'Night 2') + 1).seats.filter(x => x.lean).length, 0, 'leans clear with the phase');
});

test('fixture: last words, the death, the dead watch', () => {
  const l = find(e => e.type === 'say' && e.why === 'last words');
  let s = replay(fx, l + 1);
  assert.equal(s.bubble?.kind === 'say' && s.bubble.out, true);
  assert.ok(seat(s, 'Terra').dead && !seat(s, 'Terra').revealed, 'out while speaking, card not yet turned');
  s = replay(fx, l + 2);
  assert.deepEqual(s.bubble, { kind: 'death', name: 'Terra', role: 'officer', how: 'vote' });
  const g = find(e => e.type === 'ghost');
  s = replay(fx, g + 1);
  assert.deepEqual(s.bubble, { kind: 'ghost', name: 'Terra', text: 'I gave you both names on day one. Enjoy the next two days.' });
  assert.equal(seat(s, 'Terra').ring, 'ghost');
  const silentGhost: GameEvent = { type: 'ghost', name: 'Gemma', text: '…' };
  assert.equal(reduce(s, silentGhost), s, 'a ghost line with no words changes nothing');
  assert.equal(pace(silentGhost), 0);
  assert.ok(!isHighlight(silentGhost, undefined, s.seats));
  assert.ok(isHighlight(fx[g], fx[g + 1], s.seats), 'the dead watching is a highlight');
  assert.ok(isHighlight(fx[find(e => e.type === 'note')], undefined, s.seats), 'so is a note');
});

test('fixture: the log, one entry per turn', () => {
  const all = logEntries(fx, true), plain = logEntries(fx, false);
  const lines = all.filter(e => e.kind === 'line');
  assert.equal(lines.length, fx.filter(e => e.type === 'say' || e.type === 'whisper').length);
  assert.ok(lines.some(e => e.kind === 'line' && e.thought), 'Watch folds thoughts in');
  assert.ok(plain.every(e => e.kind !== 'line' || !e.thought), 'Guess does not');
  assert.ok(!all.some(e => (e as { kind: string }).kind === 'memory'));
  assert.equal(all.filter(e => e.kind === 'note').length, 3);
  assert.equal(all.filter(e => e.kind === 'ghost').length, 5);
  assert.ok(all.some(e => e.kind === 'line' && e.tag === 'last words'));
  assert.ok(all.some(e => e.kind === 'narration' && e.aside));
  assert.deepEqual(all.filter(e => e.kind === 'phase').map(e => e.kind === 'phase' && `${e.text} ${e.alive}`),
    ['Before the game 7', 'Night 1 7', 'Day 1 6', 'Night 2 5', 'Day 2 4', 'Night 3 3']);
  assert.ok(!logEntries(fx, true).some(e => e.kind === 'line' && e.tag === 'takes the floor'), 'engine labels only with debug');
  assert.ok(logEntries(fx, true, true).some(e => e.kind === 'line' && e.tag === 'takes the floor'));
});

test('voteGroups: by target, most first, double votes weigh twice', () => {
  const g = voteGroups([['A', 'X', ''], ['B', 'Y', ''], ['C', 'X', ''], ['D', 'Y', '']], { D: 2 });
  assert.deepEqual(g.map(x => [x.target, x.count]), [['Y', 3], ['X', 2]]);
});

test('pace: by words, the thought counts, a turned card holds', () => {
  const line: GameEvent = { type: 'say', name: 'X', text: Array(20).fill('word').join(' ') };
  assert.equal(pace(line), 1400 + 300 * 20);
  assert.equal(pace(line, Array(10).fill('w').join(' ')), 1400 + 300 * 20 + 240 * 10);
  assert.equal(pace({ type: 'say', name: 'X', text: 'ok' }), 2500);
  assert.ok(pace({ type: 'death', name: 'X', role: 'killer', how: 'vote' }) > pace({ type: 'death', name: 'X', role: null, how: 'vote' }));
});

test('highlights: the claim, the vote, a killer giving it away', () => {
  const ev = games.showcase, players = replay(ev, 1).seats;
  const hi = (i: number) => isHighlight(ev[i], ev[i + 1], players);
  assert.ok(hi(71) && hi(79) && hi(135) && hi(138) && hi(143));
  assert.ok(hi(77), 'Sol (killer) thinks about the shown killer');
  assert.ok(!hi(69) && !hi(78), 'clock and memory are filler');
});

test('modelName', () => {
  assert.equal(modelName('claude:sonnet'), 'Claude Sonnet');
  assert.equal(modelName('claude:opus'), 'Claude Opus');
  assert.equal(modelName('claude:claude-haiku-5-5'), 'Claude Haiku 5.5');
  assert.equal(modelName('codex:gpt-6-sol'), 'GPT-6 Sol');
  assert.equal(modelName('codex:gpt-5.6-terra'), 'GPT-5.6 Terra');
  assert.equal(modelName('local:google/gemma-4-26b-a4b-qat'), 'Gemma 4 26B · local');
});

test('the vote faces stay through last words and the reveal, then clear; the end clears everything', () => {
  const ev = load('ui-fixture-7-stress');
  assert.ok(replay(ev, 7).seats.some(x => x.tally), 'after the vote');
  assert.ok(replay(ev, 9).seats.some(x => x.tally), 'during the reveal');
  assert.ok(!replay(ev, 10).seats.some(x => x.tally), 'after the reveal');
  const end = replay(ev);
  assert.ok(end.seats.every(x => !x.tally && !x.lean && !x.ring));
});

// 2026-11-15 engine: the doctor sleeps on night 1 (no night_action), a day can end before its line budget ("the table
// leans": the clock stops at 8 of 30 and the vote follows), and a death may come without a host aside.
test('engine 2026-11-15: no doctor on night 1, a day cut short, no aside', () => {
  const ev: GameEvent[] = [
    { type: 'cast', players: [
      { name: 'A', model: 'm', role: 'killer', seat: 0 }, { name: 'B', model: 'm', role: 'doctor', seat: 1 },
      { name: 'C', model: 'm', role: 'citizen', seat: 2 }, { name: 'D', model: 'm', role: 'officer', seat: 3 }] },
    { type: 'phase', text: 'Night 1', kind: 'night' },
    { type: 'gm', text: 'Night falls.' },
    { type: 'phase', text: 'Day 1', kind: 'day' },
    { type: 'clock', left: 30, total: 30, seconds: 10 },
    { type: 'say', name: 'C', text: 'A did it.', lean: 'A' },
    { type: 'clock', left: 8, total: 30, seconds: 10 },
    { type: 'votes', votes: [['C', 'A', 'sure'], ['D', 'A', 'yes'], ['B', 'A', 'ok'], ['A', 'C', 'no']] },
    { type: 'death', name: 'A', role: 'killer', how: 'vote' },
    { type: 'end', winner: 'town' },
  ] as GameEvent[];
  const s = replay(ev);
  assert.equal(s.winner, 'town');
  assert.ok(seat(s, 'A').dead && seat(s, 'A').revealed);
  const st = stops(ev);
  assert.ok(st.every(i => ev[i].type !== 'clock' && ev[i].type !== 'night_action'));
  assert.ok(st.every(i => pace(ev[i]) >= 0));
  const log = logEntries(ev, true);
  assert.deepEqual(log.map(e => e.kind), ['phase', 'narration', 'phase', 'line', 'votes', 'death', ...log.slice(6).map(e => e.kind)]);
});

test('closing line: the host\'s one remark, on the end card, not a stop', () => {
  assert.equal(closingLine(fx), 'Two killers, named on day one, by the officer. Nobody wrote it down.');
  assert.ok(!stops(fx).includes(closingIndex(fx)));
  const r7 = JSON.parse(readFileSync(new URL('../../games/r7a-8.json', import.meta.url), 'utf8')) as GameEvent[];
  assert.match(closingLine(r7)!, /^Sonnet kept answering Opus/, 'r7a-8: the last aside, not the one after the last death');
  const stress = JSON.parse(readFileSync(new URL('../../games/ui-fixture-7-stress.json', import.meta.url), 'utf8')) as GameEvent[];
  assert.equal(closingLine(stress), null, 'a mid-game aside followed by a phase is not a closing line');
  assert.ok(stops(stress).includes(stress.findIndex(e => e.type === 'gm' && !!e.aside)));
});

test('a secret ballot keeps its flag for the seats, the card and the log', () => {
  const evs: GameEvent[] = [
    { type: 'cast', players: [{ name: 'A', model: 'm', role: 'citizen', seat: 0 }, { name: 'B', model: 'm', role: 'killer', seat: 1 }, { name: 'C', model: 'm', role: 'citizen', seat: 2 }] },
    { type: 'votes', votes: [['A', 'B', 'x'], ['C', 'B', 'y'], ['B', 'A', 'z']], secret: true },
  ] as GameEvent[];
  const s = replay(evs, evs.length);
  assert.equal(s.bubble?.kind === 'votes' && s.bubble.secret, true);
  assert.equal(s.seats.find(x => x.name === 'B')!.tally!.secret, true);
  const log = logEntries(evs, true);
  assert.equal(log.some(e => e.kind === 'votes' && e.secret), true);
});
