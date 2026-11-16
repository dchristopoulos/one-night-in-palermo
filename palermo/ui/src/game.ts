// The engine's event stream (games/*.json, a JSON array) and everything the viewer derives from it, as pure functions:
// the table state (reduce), where the playhead stops (stops), how long a stop stays up (pace), the log (logEntries).
// The engine decides everything; this only displays it.

export type Role = 'killer' | 'officer' | 'police' | 'doctor' | 'citizen' | 'jester' | 'mayor' | 'accomplice';
export type Winner = 'town' | 'killer' | 'jester' | 'stopped';
export interface Player { name: string; model: string; role: Role; seat: number; tagline?: string; shown?: boolean }
export type Ballot = [voter: string, target: string, why: string];
export type NightAction = { action: 'kill' | 'save' | 'check' | 'propose'; target: string; result?: string };

export type GameEvent = { t?: number } & (
  | { type: 'cast'; players: Player[]; roles?: string }
  | { type: 'phase'; text: string; kind: 'day' | 'night' }
  | { type: 'gm'; text: string; aside?: boolean }                  // aside: the host's dry remark on top of the facts (colour, not information)
  | { type: 'recap'; text: string }
  | { type: 'note'; name: string; text: string }                    // a night victim's one line, read by the table in the morning
  | { type: 'ghost'; name: string; text: string }                   // a dead player to the audience after the vote; the living cannot hear it
  | { type: 'thought'; name: string; text: string }
  // why: the engine's turn label ("answers Terra", "last words", "confession", "before the game"…); lean: who the speaker
  // would vote for right now; claim: the role the speaker says they have, from this line on
  | { type: 'say'; name: string; text: string; why?: string; reply_to?: string; lean?: string | null; claim?: string }
  | { type: 'whisper'; name: string; to: string; text: string }
  | { type: 'pass'; name: string; declines?: string }
  | { type: 'clock'; left: number; total: number; seconds: number }
  | { type: 'memory'; name: string; level: number; text: string }
  | ({ type: 'night_action'; name: string } & NightAction)
  | { type: 'votes'; votes: Ballot[]; weights?: Record<string, number>; runoff?: boolean; secret?: boolean }   // secret: the table saw only the counts
  | { type: 'death'; name: string; role: Role | null; how: 'vote' | 'night' }
  | { type: 'vindicated'; name: string; text: string }
  | { type: 'end'; winner: Winner }
);

export type Ring = 'speaking' | 'addressed' | 'ghost';   // ghost: a dead seat talking to the audience
export interface SeatState extends Player {
  dead: boolean;
  revealed: boolean;                                   // the card was turned (role public)
  out: { how: 'vote' | 'night'; when: string } | null; // when: the phase it happened in ("Day 2")
  ring: Ring | null;
  lean: string | null;                                 // who this seat would vote for right now (from its last line)
  claim: string | null;                                // the role this seat says it has
  tally: { count: number; voters: string[]; secret: boolean } | null;   // the ballots on this seat, one name per vote (a double vote twice)
}

export type Bubble =
  | { kind: 'say'; name: string; text: string; why?: string; replyTo?: string; out?: true }   // out: the speaker is already out
  | { kind: 'whisper'; name: string; to: string; text: string; out?: true }
  | { kind: 'pass'; name: string; declines: string }
  | { kind: 'narrator'; title: string; text: string; aside?: true }
  | { kind: 'note'; name: string; text: string }
  | { kind: 'ghost'; name: string; text: string }
  | { kind: 'votes'; groups: VoteGroup[]; runoff: boolean; secret: boolean }
  | { kind: 'death'; name: string; role: Role | null; how: 'vote' | 'night' };

export interface VoteGroup { target: string; count: number; voters: { name: string; why: string; weight: number }[] }

export interface TableState {
  seats: SeatState[];
  killers: number;                                     // killers dealt (public: the cast says how many)
  phase: { text: string; kind: 'day' | 'night' } | null;
  day: number;
  bubble: Bubble | null;
  thought: { name: string; text: string } | null;      // the last thought; shown with the line only if it is the speaker's
  vindicated: Record<string, string>;
  recap: string;
  winner: Winner | null;
}

export const initial: TableState = { seats: [], killers: 0, phase: null, day: 0, bubble: null, thought: null, vindicated: {}, recap: '', winner: null };

const calm = (seats: SeatState[]) => seats.map(s => (s.ring ? { ...s, ring: null } : s));
const mark = (seats: SeatState[], name: string | undefined, ring: Ring | null) => seats.map(s => (s.name === name ? { ...s, ring } : s));
// a ghost line with no words in it ("…", "[dead]"): the engine had nothing to say, so neither does the viewer
export const silent = (ev: GameEvent) => ev.type === 'ghost' && !/\p{L}{2}/u.test(ev.text.replace(/\[dead\]/gi, ''));
export const isKiller = (role: string) => /killer|accomplice/.test(role);

// the vote grouped by target, most votes first: "Gemma 4 · Sonnet 2"
export function voteGroups(votes: Ballot[], weights: Record<string, number> = {}): VoteGroup[] {
  const by = new Map<string, VoteGroup>();
  for (const [voter, target, why] of votes) {
    const w = weights[voter] || 1, g = by.get(target) ?? { target, count: 0, voters: [] };
    g.count += w; g.voters.push({ name: voter, why, weight: w }); by.set(target, g);
  }
  return [...by.values()].sort((a, b) => b.count - a.count);
}

export function reduce(s: TableState, ev: GameEvent): TableState {
  // a vote is resolved once the death after it has been shown: the next event clears the faces and counts off the seats
  if (s.bubble?.kind === 'death' && ev.type !== 'death' && s.seats.some(x => x.tally)) s = { ...s, seats: s.seats.map(x => ({ ...x, tally: null })) };
  const seat = 'name' in ev ? s.seats.find(x => x.name === ev.name) : undefined;
  const keep = (name: string) => (s.thought?.name === name ? s.thought : null);   // a line keeps its speaker's thought
  switch (ev.type) {
    case 'cast':
      return { ...initial, killers: ev.players.filter(p => isKiller(p.role)).length,
        seats: ev.players.map(p => ({ ...p, shown: !!p.shown, dead: false, revealed: false, out: null, ring: null, lean: null, claim: null, tally: null })) };
    case 'phase': {
      const n = ev.kind === 'day' ? ev.text.match(/\d+/) : null;
      return { ...s, phase: { text: ev.text, kind: ev.kind }, day: n ? Number(n[0]) : s.day, thought: null,
        seats: s.seats.map(x => ({ ...x, ring: null, lean: null, tally: null })),
        bubble: { kind: 'narrator', title: ev.text, text: ev.kind === 'night' ? 'The town sleeps.' : 'Discussion begins.' } };
    }
    case 'gm':
      return { ...s, seats: calm(s.seats), thought: null, bubble: { kind: 'narrator', title: 'Narrator', text: ev.text, ...(ev.aside && { aside: true as const }) } };
    case 'note':
      if (!seat) return s;
      return { ...s, seats: calm(s.seats), thought: null, bubble: { kind: 'note', name: ev.name, text: ev.text } };
    case 'ghost':
      if (!seat || silent(ev)) return s;
      return { ...s, seats: mark(calm(s.seats), ev.name, 'ghost'), thought: null, bubble: { kind: 'ghost', name: ev.name, text: ev.text } };
    case 'thought':
      if (!seat) return s;
      return { ...s, thought: { name: ev.name, text: ev.text } };
    case 'say': {
      if (!seat) return s;
      const why = ev.reply_to && /^answers /.test(ev.why ?? '') ? undefined : ev.why;   // "answers X" is carried by replyTo
      // last words: the speaker has been voted out but stays lit at the table until the card turns at the death
      const opening = ev.why === 'before the game' && !s.phase ? { phase: { text: 'Before the game', kind: 'day' as const } } : {};   // the opening beat, before night 1
      const seats = mark(mark(calm(s.seats), ev.name, 'speaking'), ev.reply_to, 'addressed').map(x => x.name !== ev.name ? x : {
        ...x, ...('lean' in ev && { lean: ev.lean ?? null }), ...(ev.claim && { claim: ev.claim }) });
      return { ...s, ...opening, seats, thought: keep(ev.name),
        bubble: { kind: 'say', name: ev.name, text: ev.text, why, replyTo: ev.reply_to, ...(seat.dead && { out: true as const }) } };
    }
    case 'whisper':
      if (!seat) return s;
      return { ...s, seats: mark(mark(calm(s.seats), ev.name, 'speaking'), ev.to, 'addressed'), thought: keep(ev.name),
        bubble: { kind: 'whisper', name: ev.name, to: ev.to, text: ev.text, ...(seat.dead && { out: true as const }) } };
    case 'pass':
      if (!seat || !ev.declines) return s;
      return { ...s, seats: mark(calm(s.seats), ev.declines, 'addressed'), thought: null, bubble: { kind: 'pass', name: ev.name, declines: ev.declines } };
    case 'votes': {
      const weights = ev.weights ?? {}, groups = voteGroups(ev.votes, weights);
      const seats = calm(s.seats).map(x => {
        const g = groups.find(g => g.target === x.name);
        return { ...x, tally: g ? { count: g.count, voters: g.voters.flatMap(v => Array<string>(v.weight).fill(v.name)), secret: !!ev.secret } : null };
      });
      return { ...s, seats, thought: null, bubble: { kind: 'votes', groups, runoff: !!ev.runoff, secret: !!ev.secret } };
    }
    case 'death': {
      if (!seat) return s;
      const when = s.phase?.text ?? '';
      return { ...s, thought: null, bubble: { kind: 'death', name: ev.name, role: ev.role, how: ev.how },
        seats: calm(s.seats).map(x => x.name === ev.name ? { ...x, dead: true, revealed: ev.role != null, out: { how: ev.how, when }, lean: null }
          : x.lean === ev.name ? { ...x, lean: null } : x) };
    }
    case 'vindicated':
      return { ...s, vindicated: { ...s.vindicated, [ev.name]: ev.text } };
    case 'recap':
      return { ...s, recap: ev.text };
    case 'end':   // the game is over: no suspicion, no counts, no glow left on the seats
      return { ...s, winner: ev.winner, seats: s.seats.map(x => ({ ...x, tally: null, lean: null, ring: null })) };
    default:
      return s;   // clock, memory, night_action: engine internals, not shown
  }
}

export const replay = (events: GameEvent[], n = events.length) => events.slice(0, n).reduce(reduce, initial);

// the events the playhead stops on (what a viewer sees change); thoughts fold into the line after them
export function isStop(ev: GameEvent): boolean {
  switch (ev.type) {
    case 'phase': case 'gm': case 'say': case 'whisper': case 'note': case 'votes': case 'death': case 'end': return true;
    case 'pass': return !!ev.declines;
    case 'ghost': return !silent(ev);
    default: return false;
  }
}
// The host's one remark on the whole game (engine 2026-11-15: no aside after each death, one at the very end): the last
// aside with no phase, vote or death after it. The end card shows it under the title, so the replay does not stop on it.
export function closingIndex(events: GameEvent[]): number {
  for (let i = events.length - 1; i >= 0; i--) {
    const e = events[i];
    if (e.type === 'phase' || e.type === 'votes' || e.type === 'death') return -1;
    if (e.type === 'gm' && e.aside) return i;
  }
  return -1;
}
export const closingLine = (events: GameEvent[]) => { const i = closingIndex(events); return i < 0 ? null : (events[i] as { text: string }).text; };

export const stops = (events: GameEvent[]) => { const c = closingIndex(events); return events.flatMap((e, i) => (isStop(e) && i !== c ? [i] : [])); };

// reading pace (ms) by word count, so a 20-word line is not rushed; `thought`: the speaker's thought shown with the line
const words = (t = '') => t.trim().split(/\s+/).filter(Boolean).length;
export function pace(ev: GameEvent, thought?: string): number {
  switch (ev.type) {
    case 'say': case 'whisper': return Math.max(2500, 1400 + 300 * words(ev.text) + 240 * words(thought));
    case 'ghost': return silent(ev) ? 0 : Math.max(2800, 1600 + 300 * words(ev.text));
    case 'note': return Math.max(3500, 2200 + 300 * words(ev.text));   // unfolding the paper
    case 'gm': return Math.max(2500, 1600 + 280 * words(ev.text));
    case 'votes': return 3500 + 600 * ev.votes.length;
    case 'death': return ev.role ? 4500 : 3000;                        // the card turns (900 ms) and then has to be read
    case 'phase': return 2200;
    case 'pass': return 1600;
    case 'end': return 0;
    default: return 0;
  }
}

// the moments a viewer would cut a highlight reel from (bake.py mirrors these rules; also accepts the curly apostrophe)
export function isHighlight(ev: GameEvent, next: GameEvent | undefined, players: Player[]): boolean {
  switch (ev.type) {
    case 'phase': case 'gm': case 'votes': case 'death': case 'end': case 'recap': case 'vindicated': case 'whisper': case 'note': return true;
    case 'ghost': return !silent(ev);   // the dead watching is one of the best parts of the game
    case 'say': {
      if (/last word|confession/.test(ev.why ?? '') || ev.why === 'introduces themselves' || ev.claim) return true;
      const t = ev.text;
      let score = 0;
      if (/\b(i['’]?m|i am|i was) the (officer|doctor|killer)\b|\bi checked\b|\bi protected\b/i.test(t)) score += 3;
      if (/\bkiller\b/i.test(t) && players.some(p => new RegExp(`\\b${p.name}\\b`).test(t))) score += 2;
      if (/\bi(?:['’]m| am) voting\b|\bi vote\b|\bvote (for )?[A-Z]/.test(t)) score += 1;
      if (ev.reply_to && /\?/.test(t)) score += 1;
      return score >= 2;
    }
    case 'thought': {
      const p = players.find(x => x.name === ev.name);   // dramatic irony: the thought gives the game away
      if (p && isKiller(p.role) && /officer|doctor|mayor|killer|claim|kill|tonight|double vote|partner|shown/i.test(ev.text)) return true;
      return next?.type === 'say' && next.name === ev.name && isHighlight(next, undefined, players);
    }
    default: return false;
  }
}

// the log: one entry per turn, not per event. `thoughts`: fold each speaker's thought into their line (Watch mode).
// Thoughts with no line after them, memory notes, clocks and night actions are left out.
const TAGS: Record<string, string> = { 'last words': 'voted out · last words', confession: 'after the game', 'before the game': 'before the game' };
export type LogEntry = { i: number } & (
  | { kind: 'phase'; text: string; night: boolean; alive: number }
  | { kind: 'line'; name: string; text: string; to?: string; whisper?: boolean; tag?: string; thought?: string }
  | { kind: 'pass'; name: string; declines: string }
  | { kind: 'narration'; text: string; aside: boolean }
  | { kind: 'votes'; groups: VoteGroup[]; runoff: boolean; secret: boolean }
  | { kind: 'death'; name: string; role: Role | null; how: 'vote' | 'night' }
  | { kind: 'note' | 'ghost' | 'called'; name: string; text: string }
);
export function logEntries(events: GameEvent[], thoughts: boolean, debug = false): LogEntry[] {
  const out: LogEntry[] = [];
  let pending: { name: string; text: string } | null = null, alive = 0;
  events.forEach((ev, i) => {
    const thought = (name: string) => (thoughts && pending?.name === name ? pending.text : undefined);
    switch (ev.type) {
      case 'cast': alive = ev.players.length; break;
      case 'thought': pending = { name: ev.name, text: ev.text }; return;
      case 'phase': out.push({ i, kind: 'phase', text: ev.text, night: ev.kind === 'night', alive }); break;
      case 'say': {
        if (ev.why === 'before the game' && !out.some(e => e.kind === 'phase')) out.push({ i, kind: 'phase', text: 'Before the game', night: false, alive });
        const tag = TAGS[ev.why ?? ''] ?? (debug && ev.why && !/^answers /.test(ev.why) ? ev.why : undefined);
        out.push({ i, kind: 'line', name: ev.name, text: ev.text, to: ev.reply_to, tag, thought: thought(ev.name) });
        break;
      }
      case 'whisper': out.push({ i, kind: 'line', name: ev.name, text: ev.text, to: ev.to, whisper: true, thought: thought(ev.name) }); break;
      case 'pass': if (ev.declines) out.push({ i, kind: 'pass', name: ev.name, declines: ev.declines }); break;
      case 'gm': out.push({ i, kind: 'narration', text: ev.text, aside: !!ev.aside }); break;
      case 'votes': out.push({ i, kind: 'votes', groups: voteGroups(ev.votes, ev.weights), runoff: !!ev.runoff, secret: !!ev.secret }); break;
      case 'death': alive--; out.push({ i, kind: 'death', name: ev.name, role: ev.role, how: ev.how }); break;
      case 'note': out.push({ i, kind: 'note', name: ev.name, text: ev.text }); break;
      case 'ghost': if (!silent(ev)) out.push({ i, kind: 'ghost', name: ev.name, text: ev.text }); break;
      case 'vindicated': out.push({ i, kind: 'called', name: ev.name, text: ev.text }); break;
    }
    pending = null;   // a thought belongs to the very next line only
  });
  return out;
}

// "claude:claude-haiku-5-5" → "Claude Haiku 5.5", "claude:opus" → "Claude Opus", "codex:gpt-6-sol" → "GPT-6 Sol", "local:google/gemma-4-26b-a4b-qat" → "Gemma 4 26B · local"
export function modelName(m: string): string {
  const [backend, ...rest] = m.split(':');
  const id = rest.join(':'), cap = (w: string) => w[0].toUpperCase() + w.slice(1);
  if (backend === 'claude') { const w = id.replace(/^claude-/, '').split('-'); return 'Claude ' + cap(w[0]) + (w[1] ? ' ' + w.slice(1).join('.') : ''); }
  if (backend === 'codex') return id.replace(/^gpt-/, 'GPT-').replace(/-(\w+)$/, (_, w: string) => ' ' + cap(w));
  if (backend === 'local') {
    const w = id.split('/').pop()!.split('-'), size = w.find(x => /^\d+b$/i.test(x));
    return cap(w[0]) + (w[1] ? ' ' + w[1] : '') + (size ? ' ' + size.toUpperCase() : '') + ' · local';
  }
  return m;
}
