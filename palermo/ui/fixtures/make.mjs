// One-off: turn a seven-seat prototype game into the final event contract the viewer is built against.
//   node ui/fixtures/make.mjs [games/lab/fun7t-34.json] [games/ui-fixture-7.json]   (paths from the palermo folder)
// - `gm` lines "X left a note behind: "…"" become {type: "note", name, text}
// - ghost lines with no words ("…", "[dead]") get a hand-written line, as the finished engine would say one
// - Terra's first officer claim gets `claim: "officer"`
// - the host's closing aside ({aside: true}, after "The game is over."; engine 2026-11-15: no aside after each death) and one
//   "before the game" line per player are added by hand (the stress file keeps one mid-game aside, as older games have)
import { readFileSync, writeFileSync } from 'node:fs';

const root = new URL('../../', import.meta.url).pathname;
const [src = 'games/lab/fun7t-34.json', out = 'games/ui-fixture-7.json'] = process.argv.slice(2);
const events = JSON.parse(readFileSync(root + src, 'utf8'));

const BEFORE = {   // one line each about "the previous game"
  Sonnet: 'Last game I trusted the first claim. Not making that mistake twice.',
  Haiku: 'Last time I called it on day one and nobody listened. Again?',
  Gemma: 'i saved the wrong person last game. tonight i guess better.',
  Sol: 'Last game I was too quiet. Expect to hear from me.',
  Luna: 'Whoever talked most last game was lying. Watching the loud ones.',
  Terra: 'I sat on my check last time. Never again.',
  Opus: 'I have seen every way this table loses. Let us try a new one.',
};
const GHOST = {   // the prototype's empty ghost lines
  Terra: 'I gave you both names on day one. Enjoy the next two days.',
  Gemma: 'i left a note saying doctor. one word. still too long for them.',
};
const ASIDE = {   // after this narrator line (by its start), the host's remark on the whole game
  'The game is over.': 'Two killers, named on day one, by the officer. Nobody wrote it down.',
};

const result = [];
for (const ev of events) {
  if (ev.type === 'gm') {
    const m = ev.text.match(/^(\w+) left a note behind: "(.*)"$/s);
    if (m) { result.push({ type: 'note', name: m[1], text: m[2], t: ev.t }); continue; }
    if (/^The game begins\./.test(ev.text)) ev.text = ev.text.replace(/^The game begins\. Six/, 'The game begins. Seven');
  }
  if (ev.type === 'say' && ev.name === 'Terra' && /^Sol is a killer; I checked/.test(ev.text)) ev.claim = 'officer';   // the claim field the engine is adding
  if (ev.type === 'ghost' && !/\p{L}{2}/u.test(ev.text.replace(/\[dead\]/, ''))) ev.text = GHOST[ev.name] ?? ev.text;
  result.push(ev);
  if (ev.type === 'gm') {
    const key = Object.keys(ASIDE).find(k => ev.text.startsWith(k));
    if (key) result.push({ type: 'gm', text: ASIDE[key], aside: true, t: ev.t });
    if (/^The game begins\./.test(ev.text)) {
      const cast = events.find(e => e.type === 'cast');
      for (const p of cast.players) result.push({ type: 'say', name: p.name, text: BEFORE[p.name], why: 'before the game', t: ev.t });
    }
  }
}
writeFileSync(root + out, JSON.stringify(result, null, 1) + '\n');
const count = t => result.filter(e => e.type === t).length;
console.log(`${out}: ${result.length} events, ${count('note')} notes, ${count('ghost')} ghost lines, ${result.filter(e => e.aside).length} asides, ${result.filter(e => e.why === 'before the game').length} before-the-game lines`);

// A second, hand-made stress file for the longest content the new engine allows (games/ui-fixture-7-stress.json):
// a 20-word line under a two-line thought, a 28-word claim, a vote of seven split three ways, 28-word last words and note.
{
  const cast = events.find(e => e.type === 'cast');
  const stress = [
    { ...cast, players: cast.players.map(p => ({ ...p })) },
    { type: 'phase', text: 'Day 1', kind: 'day' },
    { type: 'thought', name: 'Sol', text: 'Terra is the real officer and she just named me. If I attack her claim head-on I look guilty, so I will sound reasonable and steer the table toward Gemma instead.' },
    { type: 'say', name: 'Sol', text: 'Terra, I hear you, but naming two killers on the first morning sounds like a guess dressed up as a check, and I would rather hear Gemma explain her night.', why: 'answers Terra', reply_to: 'Terra', lean: 'Gemma' },
    { type: 'say', name: 'Terra', text: 'I am the officer. I was shown Sol at the start and I checked Sonnet last night, and both of them are killers, so please vote Sol today.', why: 'answers Sol', reply_to: 'Sol', lean: 'Sol', claim: 'officer' },
    { type: 'say', name: 'Luna', text: 'Two names at once is too neat for me.', why: 'takes the floor', lean: 'Terra' },
    { type: 'votes', votes: [['Sonnet', 'Gemma', 'quiet all day'], ['Haiku', 'Terra', 'too neat'], ['Gemma', 'Terra', 'two names is a bluff'], ['Sol', 'Gemma', 'never answers'], ['Luna', 'Terra', 'too neat'], ['Terra', 'Sol', 'shown to me as a killer'], ['Opus', 'Sol', 'the officer named him']] },
    { type: 'say', name: 'Terra', text: 'You are voting out the only person who knows anything. Sol and Sonnet are the killers, and tomorrow morning you will find out the hard way.', why: 'last words' },
    { type: 'death', name: 'Terra', role: 'officer', how: 'vote' },
    { type: 'gm', text: 'Palermo has voted: Terra is out. Terra shows the card: officer.' },
    { type: 'gm', text: 'Somewhere, a killer exhales.', aside: true },
    { type: 'ghost', name: 'Terra', text: 'Three votes on the officer. I would laugh if I still had lungs.' },
    { type: 'phase', text: 'Night 2', kind: 'night' },
    { type: 'death', name: 'Haiku', role: 'citizen', how: 'night' },
    { type: 'note', name: 'Haiku', text: 'If you are reading this, Terra was right about Sol and you all let it slide. Check who pushed Gemma hardest on day one, then vote them.' },
    { type: 'end', winner: 'killer' },
  ];
  writeFileSync(root + 'games/ui-fixture-7-stress.json', JSON.stringify(stress, null, 1) + '\n');
  console.log(`games/ui-fixture-7-stress.json: ${stress.length} events`);
}
