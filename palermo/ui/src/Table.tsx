import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { closingLine, isKiller, logEntries, modelName, pace, replay, stops as stopsOf, type GameEvent, type SeatState, type TableState, type Winner } from './game.ts';
import { Card } from './Card.tsx';
import { placeOf, scoreboard } from './evenings.ts';
import type { Route } from './App.tsx';
import { Scoreboard } from './Scoreboard.tsx';
import { Face } from './Face.tsx';
import { Log } from './Log.tsx';
import { Seat } from './Seat.tsx';
import { markSeen } from './seen.ts';
import css from './Table.module.css';

// One game (DESIGN.md §7). The route (App.tsx) says which file and how: ?at=N holds a still, ?mode=guess, ?debug=1.
// `live`: the game is still being written (from the index, or ?live=1): poll it and follow the newest line.
// `place`: where it sits in its evening (Game 3 of 12, the games either side), from the index.
type Place = ReturnType<typeof placeOf> | null;
const fromRoot = (p: string) => p.replace(/^\/+/, '');   // page-relative: the viewer works under any path
type Mode = 'watch' | 'guess';
const SPEEDS = [1, 1.5, 2];

// DESIGN.md §7: wide = a horizontal table with the seats on its long sides; stack = cast grid, card, log (portrait, phone)
type Compo = 'wide' | 'stack';
// too short for a table with a card in its middle (a phone on its side): stack, so the card never covers a seat
const compoOf = (w: number, h: number): Compo => (w >= 760 && h >= 440 && w / h >= 1.2 ? 'wide' : 'stack');

export function Table({ route, live: LIVE, place, onOpen }: { route: Route; live: boolean; place: Place; onOpen: (file: string | null) => void }) {
  const FILE = route.file!, AT = route.at, DEBUG = route.debug;
  const everLive = useRef(false);   // the game was being written while we watched: its evening is still going
  if (LIVE) everLive.current = true;
  const [events, setEvents] = useState<GameEvent[] | null>(null);
  const [pos, setPos] = useState(AT != null ? AT : -1);   // events applied; -1: not placed yet (the cast once loaded)
  const [playing, setPlaying] = useState(AT == null);
  const [speed, setSpeed] = useState(1);
  const [mode, setMode] = useState<Mode>(route.mode);
  const [viewport, setViewport] = useState([innerWidth, innerHeight]);
  const compo = compoOf(viewport[0], viewport[1]);
  const short = viewport[1] < 440 && viewport[0] >= 520;   // a phone on its side: cast left, card right, so the card has no speaker above or below to point at
  const [logOpen, setLogOpen] = useState(innerWidth >= 1100);

  useEffect(() => {   // load the game; a live game is polled (and loaded once more when it stops being live)
    let known = 0, head = '';
    const load = async () => {
      try {
        const r = await fetch(fromRoot(FILE) + (LIVE ? `?t=${Date.now()}` : ''), { cache: 'no-store' });
        if (!r.ok) return;
        const data: GameEvent[] = await r.json(), first = JSON.stringify(data[0] ?? null);
        if (data.length === known && first === head) return;
        known = data.length; head = first; setEvents(data);
      } catch { /* no game yet */ }
    };
    load();
    const poll = LIVE ? setInterval(load, 1000) : undefined;
    return () => clearInterval(poll);
  }, [FILE, LIVE]);
  useEffect(() => {
    const onResize = () => setViewport([innerWidth, innerHeight]);
    addEventListener('resize', onResize);
    return () => removeEventListener('resize', onResize);
  }, []);

  const stops = useMemo(() => (events ? stopsOf(events) : []), [events]);
  const start = events ? events.findIndex(e => e.type === 'cast') + 1 : 0;
  const at = pos < 0 ? start : pos;
  const t: TableState = useMemo(() => (events ? replay(events, at) : replay([])), [events, at]);
  const watch = mode === 'watch', over = !!t.winner;
  const speaker = t.bubble && (t.bubble.kind === 'say' || t.bubble.kind === 'whisper') ? t.bubble.name : null;
  const thought = watch && speaker && t.thought?.name === speaker ? t.thought.text : null;
  const entries = useMemo(() => (events ? logEntries(events.slice(0, at), watch, DEBUG) : []), [events, at, watch]);
  const next = stops.find(i => i + 1 > at), prev = [...stops].reverse().find(i => i + 1 < at);
  const go = (p: number | undefined) => { if (p != null) setPos(p + 1); };

  // a live game ended while we were more than 20 stops behind: offer "Jump to the end" (the ending still plays at 1×)
  const hasEnd = !!events?.some(e => e.type === 'end'), hadEnd = useRef<boolean | null>(null), [jump, setJump] = useState(false);
  useEffect(() => {
    if (!events) return;
    if (hadEnd.current === false && hasEnd && stops.filter(i => i >= at).length > 20) setJump(true);
    hadEnd.current = hasEnd;
  }, [events]);
  useEffect(() => { if (over) setJump(false); }, [over]);

  useEffect(() => {   // the clock: hold each stop long enough to read it, thought included, then move on
    if (!playing || !events) return;
    if (next == null) { if (!LIVE) setPlaying(false); return; }
    const last = events[at - 1], hold = last && stops.includes(at - 1) ? pace(last, thought ?? undefined) : 600;
    const behind = stops.filter(i => i >= at).length, k = LIVE ? (behind > 20 ? 1000 : behind > 6 ? 4 : behind > 2 ? 1.5 : 1) : speed;
    const timer = setTimeout(() => setPos(next + 1), hold / k);
    return () => clearTimeout(timer);
  }, [playing, at, events, speed, next, thought]);

  useEffect(() => {   // Space play/pause, ←/→ previous/next line
    const key = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement;
      if (el.closest('input')) return;
      if (e.code === 'Space') { if (el.closest('button, summary, [role="button"]')) return; e.preventDefault(); setPlaying(p => !p); }
      else if (e.key === 'ArrowRight') { setPlaying(false); go(next); }
      else if (e.key === 'ArrowLeft') { setPlaying(false); go(prev); }
    };
    addEventListener('keydown', key);
    return () => removeEventListener('keydown', key);
  });

  // the card points at its speaker: x of the speaker's portrait over the card, and which edge faces them
  const stageRef = useRef<HTMLElement>(null), [tail, setTail] = useState<{ x: number; edge: 'top' | 'bottom' }>();
  const target = t.seats.find(s => s.ring === 'speaking' || s.ring === 'ghost')?.name;
  useLayoutEffect(() => {
    const face = target && stageRef.current?.querySelector(`[data-name="${target}"] img`), card = stageRef.current?.querySelector('[data-card] > div');
    let v: typeof tail;
    if (face && card) {
      const f = face.getBoundingClientRect(), c = card.getBoundingClientRect();
      v = { x: Math.round(Math.max(28, Math.min(c.width - 28, f.left + f.width / 2 - c.left))), edge: f.top + f.height / 2 < c.top ? 'top' : 'bottom' };
    }
    if (JSON.stringify(v) !== JSON.stringify(tail)) setTail(v);
  });

  const night = t.phase?.kind === 'night', showRole = watch || over, ballots = showRole;   // who cast which secret ballot: the audience's to see, not the detective's
  const leaners = (name: string) => t.seats.filter(s => !s.dead && s.lean === name).map(s => s.name);
  const seat = (s: SeatState, row?: 'top' | 'bottom') => (
    <div key={s.name} className={css.place} data-name={s.name}><Seat seat={s} showRole={showRole} leaners={leaners(s.name)} row={row} ballots={ballots} /></div>);
  const n = t.seats.length, top = Math.ceil(n / 2);   // clockwise from the top left: the top row left to right, the bottom row right to left
  const card = t.bubble && !over && <div data-card className={css.cardSlot}><Card bubble={t.bubble} thought={thought} seats={t.seats} tail={short ? undefined : tail} ballots={ballots} /></div>;
  const log = events && <Log entries={entries} seats={t.seats} current={at - 1} ballots={ballots} onJump={i => { setPlaying(false); setPos(i + 1); }} />;

  return (
    <div className={css.root} data-theme={night ? 'night' : 'day'} data-compo={compo} data-log={(compo === 'wide' && logOpen) || undefined}>
      <div className={css.backdrop} aria-hidden><div data-theme="day" /><div data-theme="night" style={{ opacity: night ? 1 : 0 }} /></div>
      <Header t={t} events={events} stops={stops} at={at} playing={playing} speed={speed} mode={mode} compo={compo} logOpen={logOpen} live={LIVE} place={place} onOpen={onOpen}
        onJump={jump ? () => { setJump(false); setPos(events!.length); } : null}
        onPlay={() => { if (next == null && !LIVE) setPos(start); setPlaying(p => !p); }} onPrev={() => { setPlaying(false); go(prev); }} onNext={() => { setPlaying(false); go(next); }}
        onSeek={i => { setPlaying(false); setPos(i + 1); }} onSpeed={setSpeed} onMode={setMode} onLog={() => setLogOpen(o => !o)} />

      <main ref={stageRef} className={css.stage}>
        {!events && <div className={css.empty}>Loading the game…</div>}
        {events && compo === 'wide' && <>
          <div className={css.row}>{t.seats.slice(0, top).map(s => seat(s, 'top'))}</div>
          <div className={css.table}><div className={css.felt}>{card}</div></div>
          <div className={css.row}>{t.seats.slice(top).reverse().map(s => seat(s, 'bottom'))}</div>
        </>}
        {events && compo === 'stack' && <>
          <div className={css.cast} data-n={n}>{t.seats.map(s => seat(s))}</div>
          <div className={css.stackCard}>{card}</div>
          <div className={css.stackLog}>{log}</div>
        </>}
        {over && <EndCard file={FILE} closing={events ? closingLine(events) : null} t={t} place={place} wasLive={everLive.current} onAgain={() => { setPos(start); setPlaying(true); }} onOpen={onOpen} />}
      </main>
      {compo === 'wide' && logOpen && <aside className={css.side}>{log}</aside>}
    </div>
  );
}

// "Day 2 · 5 at the table · 2 killers left", then the controls (every target ≥ 44 px)
function Header({ t, events, stops, at, playing, speed, mode, compo, logOpen, live: LIVE, place, onOpen, onJump, onPlay, onPrev, onNext, onSeek, onSpeed, onMode, onLog }: {
  t: TableState; events: GameEvent[] | null; stops: number[]; at: number; playing: boolean; speed: number; mode: Mode; compo: Compo; logOpen: boolean;
  live: boolean; place: Place; onOpen: (file: string | null) => void; onJump: (() => void) | null;
  onPlay: () => void; onPrev: () => void; onNext: () => void; onSeek: (i: number) => void; onSpeed: (s: number) => void; onMode: (m: Mode) => void; onLog: () => void;
}) {
  const alive = t.seats.filter(s => !s.dead);
  const killers = mode === 'watch' || t.winner ? alive.filter(s => isKiller(s.role)).length
    : t.killers - t.seats.filter(s => s.dead && s.revealed && isKiller(s.role)).length;   // Guess: what the table knows
  const status = t.seats.length ? [t.phase?.text ?? 'The table', `${alive.length} at the table`, `${killers} killer${killers === 1 ? '' : 's'} left`].join(' · ') : '';
  const k = Math.max(0, stops.filter(i => i < at).length - 1), last = Math.max(1, stops.length - 1);
  const marks = events ? stops.flatMap((i, j) => {
    const e = events[i];
    return e.type === 'phase' ? [{ j, kind: e.kind, label: e.text }] : e.type === 'death' ? [{ j, kind: 'death', label: `${e.name} out` }] : [];
  }) : [];
  return (
    <header className={css.bar} data-live={LIVE || undefined}>
      <div className={css.where}>
        <button className={`${css.btn} ${css.home}`} onClick={() => onOpen(null)} aria-label="All games" title="all games">
          <svg viewBox="0 0 16 16" aria-hidden><path d="M8 1.5 15 7.5h-2V14H9.5v-4h-3v4H3V7.5H1z" /></svg><span>Games</span>
        </button>
        <h1 className={css.title}>One Night in Palermo</h1>
        {place?.evening && place.game && (
          <nav className={css.evening} aria-label="Games of this evening">
            <button className={css.btn} disabled={!place.prev} onClick={() => place.prev && onOpen(place.prev.file)} aria-label="Previous game">‹</button>
            <span><b><i className={css.wide}>Game </i>{place.game.n}</b> of {place.evening.games.length}{place.evening.live && !place.game.live && <i className={css.wide}> so far</i>}</span>
            <button className={css.btn} disabled={!place.next} onClick={() => place.next && onOpen(place.next.file)} aria-label="Next game">›</button>
          </nav>
        )}
        {LIVE && <span className={css.liveTag}>live</span>}
        {onJump && <button className={`${css.btn} ${css.jump}`} onClick={onJump}>Jump to the end</button>}
      </div>
      <p className={css.status} aria-live="polite">{t.phase?.kind === 'night' && <i className={css.moon} />}{status && <>
        <span>{t.phase?.text ?? 'The table'}</span><span className={css.atTable}> · {alive.length} at the table</span><span> · {killers} killer{killers === 1 ? '' : 's'} left</span>
      </>}</p>
      <nav className={css.controls} aria-label="Replay">
        {!LIVE && <>
          <button className={css.btn} onClick={onPrev} aria-label="Previous line"><svg viewBox="0 0 16 16" aria-hidden><path d="M3 3h2v10H3zM13 3v10L6 8z" /></svg></button>
          <button className={`${css.btn} ${css.play}`} onClick={onPlay} aria-label={playing ? 'Pause' : 'Play'}>
            <svg viewBox="0 0 16 16" aria-hidden>{playing ? <path d="M4 3h3v10H4zM9 3h3v10H9z" /> : <path d="M4 2.5v11l9-5.5z" />}</svg>
          </button>
          <button className={css.btn} onClick={onNext} aria-label="Next line"><svg viewBox="0 0 16 16" aria-hidden><path d="M11 3h2v10h-2zM3 3v10l7-5z" /></svg></button>
          <button className={css.btn} onClick={() => onSpeed(SPEEDS[(SPEEDS.indexOf(speed) + 1) % SPEEDS.length])} aria-label={`Speed ${speed}×, change`} title="speed: 1×, 1.5×, 2×">{speed}×</button>
        </>}
        <div className={css.seg} role="group" aria-label="Viewing mode">
          <button aria-pressed={mode === 'watch'} onClick={() => onMode('watch')} title="every role and thought shown: watch the liars lie">Watch</button>
          <button aria-pressed={mode === 'guess'} onClick={() => onMode('guess')} title="only what the table knows; all revealed at the end">Guess</button>
        </div>
        {compo === 'wide' && <button className={css.btn} aria-pressed={logOpen} onClick={onLog}>Log</button>}
      </nav>
      {!LIVE && stops.length > 1 && (
        <div className={css.scrub}>
          <input type="range" min={0} max={last} value={k} aria-label="Position" onChange={e => onSeek(stops[Number(e.target.value)])} />
          <div className={css.marks} aria-hidden>{marks.map(m => <i key={m.j} data-kind={m.kind} title={m.label} style={{ left: `${(100 * m.j) / last}%` }} />)}</div>
        </div>
      )}
    </header>
  );
}

const ENDS: Record<Winner, [string, string]> = {
  town: ['The town wins', 'Every killer was voted out.'],
  killer: ['The killers win', 'The killers outlasted the town.'],
  jester: ['The jester wins', 'The town voted out the jester.'],
  stopped: ['Stopped', 'The game was stopped early.'],
};

// the end: who won, who was who and when they went out, the recap, watch again
function EndCard({ file, closing, t, place, wasLive, onAgain, onOpen }: { file: string; closing: string | null; t: TableState; place: Place; wasLive: boolean; onAgain: () => void; onOpen: (file: string | null) => void }) {
  const [title, sub] = ENDS[t.winner!];
  const [scores, setScores] = useState(false);
  useEffect(() => markSeen(file), [file]);   // watched to the end on this device: Home may show its result
  const ev = place?.evening, n = place?.game?.n ?? 0;
  // the next game of the evening: offered as soon as the index lists it; while the evening is still being played, say it is coming
  const waiting = ev && !place?.next && (wasLive || ev.live);
  return (
    <div className={css.end}>
      <div className={css.endCard} role="dialog" aria-label={title}>
        <h2>{title}</h2>
        {closing && <p className={css.closing}><span>the host</span>{closing}</p>}
        <div className={css.endBody}>
        {ev && <p className={css.endOf}>Game {n} of {ev.games.length}{ev.live ? ' so far' : ''}
          <button className={css.link} aria-pressed={scores} onClick={() => setScores(v => !v)}>{scores ? 'Who was who' : 'The evening so far'}</button></p>}
        {scores && ev ? <Scoreboard score={scoreboard(ev, n)} title={`After game ${n}`} /> : <ul>
          {t.seats.map(s => (
            <li key={s.name} data-killer={isKiller(s.role) || undefined} data-dead={s.dead || undefined} style={{ '--seat-color': `var(--seat-${s.seat % 7})` } as CSSProperties}>
              <Face name={s.name} />
              <span className={css.endWho}><b>{s.name}</b><small>{modelName(s.model)}</small></span>
              <span className={css.endRole}>{s.role}{t.vindicated[s.name] && <em> · called it</em>}<small>{s.out ? `${s.out.how === 'vote' ? 'voted out' : 'killed'}, ${s.out.when}` : 'survived'}</small></span>
            </li>
          ))}
        </ul>}
        {!scores && <p className={css.recap}>{t.recap || sub}</p>}
        </div>
        <div className={css.endActions}>
          <button className={`${css.btn} ${place?.next ? '' : css.again}`} onClick={onAgain}>Watch again</button>
          {place?.next && <button className={`${css.btn} ${css.again}`} onClick={() => onOpen(place.next!.file)}>Next game: {place.next.n} →</button>}
          {waiting && <span className={css.soon}>Game {n + 1} starts soon…</span>}
          {!place?.next && !waiting && <button className={css.btn} onClick={() => onOpen(null)}>All games</button>}
        </div>
      </div>
    </div>
  );
}
