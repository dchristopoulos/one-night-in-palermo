import { useState, type CSSProperties } from 'react';
import { seenGames, setShowResults, showResults } from './seen.ts';
import { scoreboard, when, winnerWord, type Evening, type GameInfo } from './evenings.ts';
import { modelName } from './game.ts';
import { Face } from './Face.tsx';
import { Scoreboard } from './Scoreboard.tsx';
import css from './Home.module.css';

type Index = { evenings: Evening[]; singles: GameInfo[] };
type Open = (file: string) => void;
const seat = (g: GameInfo, name: string) => ({ '--seat-color': `var(--seat-${Math.max(0, g.cast.findIndex(p => p.name === name)) % 7})` }) as CSSProperties;
const length = (g: GameInfo) => `${g.days} day${g.days === 1 ? '' : 's'} · ${Math.max(1, Math.round(g.minutes))} min`;

// Home (DESIGN.md §5, §7), top to bottom: what this is and one button to start watching; how a game goes; the best
// games by the fun meter, each with a line a player really said; then every evening with its games and scoreboard.
export function Home({ index, failed, onOpen }: { index: Index | null; failed: boolean; onOpen: Open }) {
  const games = index?.evenings.flatMap(e => e.games.map(g => ({ g, e }))) ?? [];
  const live = games.filter(x => x.g.live);
  const done = games.filter(x => x.g.finished && !x.g.live);
  const best = done.filter(x => x.g.fun).sort((a, b) => b.g.fun!.score - a.g.fun!.score).slice(0, 6);
  const featured = best[0] ?? done[0] ?? null;
  const [shown, setShown] = useState(showResults), [seen] = useState(seenGames);
  // a result shows when results are shown, or this device watched that game to its end card
  const reveal: Reveal = g => shown || seen.has(g.file);
  const toggle = (on: boolean) => { setShown(on); setShowResults(on); };
  return (
    <div className={css.home} data-theme="day">
      <Hero featured={featured?.g ?? null} ranked={best.length > 0} live={live[0]?.g ?? null} cast={(live[0] ?? featured ?? games[0])?.g.cast ?? []} played={done.length} onOpen={onOpen} />
      {!index && <p className={css.note}>{failed ? <>No games list here. Serve the viewer with <code>python3 view.py</code> or <code>python3 game.py --serve</code>.</> : 'Looking for games…'}</p>}
      <ol className={css.how}>
        <li><b>Night</b><span>The two killers choose a victim. The doctor guards one player and hopes it is the right one.</span></li>
        <li><b>Day</b><span>The table argues, bluffs and votes one player out. That player's card is turned over.</span></li>
        <li><b>You</b><span>See every private thought as it happens, or hide them and try to spot the killers yourself.</span></li>
      </ol>
      {live.map(({ g, e }) => <LiveRow key={g.file} g={g} e={e} onOpen={onOpen} />)}
      {best.length > 0 && (
        <section>
          <div className={css.sec}><h2>Start with these</h2><p>Ranked by the fun meter: an AI judge that watched every game.</p></div>
          <div className={css.picks}>{best.map(({ g, e }) => <Pick key={g.file} g={g} e={e} onOpen={onOpen} />)}</div>
        </section>
      )}
      {index && index.evenings.length > 0 && (
        <div className={css.sec}>
          <h2>Every evening</h2>
          <div className={css.switch} role="group" aria-label="Results">
            <span>Results</span>
            <button aria-pressed={!shown} onClick={() => toggle(false)}>Hidden</button>
            <button aria-pressed={shown} onClick={() => toggle(true)}>Shown</button>
          </div>
        </div>
      )}
      {index?.evenings.map((e, i) => <EveningBlock key={e.key} e={e} open={i < 1 || e.live} reveal={reveal} onOpen={onOpen} />)}
      {index && index.singles.length > 0 && (
        <details className={css.evening}>
          <summary><span className={css.day}>Older games</span><span className={css.meta}>{index.singles.length} single games</span></summary>
          <ol className={css.rows}>{index.singles.map(g => <Row key={g.file} g={g} label={when(g.started).day} reveal={reveal(g)} onOpen={onOpen} />)}</ol>
        </details>
      )}
      <p className={css.foot}>Nobody scripted these games. Every line, lie and mistake is the models' own.</p>
    </div>
  );
}

// "Claude, GPT and Gemma": the model families at the table, from the cast itself (anyone can seat other models)
const family = (model: string) => {
  const backend = model.split(':')[0];
  return backend === 'claude' ? 'Claude' : backend === 'codex' ? 'GPT' : (modelName(model).split(' ')[0] || 'a local model');
};
export const families = (cast: { model: string }[]) => {
  const f = [...new Set(cast.map(p => family(p.model)))];
  return f.length ? f.length === 1 ? `Seven ${f[0]} models`.replace('Seven', cast.length === 7 ? 'Seven' : String(cast.length))
    : `${f.slice(0, -1).join(', ')} and ${f[f.length - 1]}` : 'Seven AI models';
};

// the first screen: the name, what it is in one breath, the seven players, and one button that starts a game
function Hero({ featured, ranked, live, cast, played, onOpen }: { featured: GameInfo | null; ranked: boolean; live: GameInfo | null; cast: GameInfo['cast']; played: number; onOpen: Open }) {
  const start = live ?? featured;
  return (
    <header className={css.hero} data-theme="night">
      <p className={css.eyebrow}>{cast.length === 7 || !cast.length ? 'Seven' : cast.length} AI models · two secret killers · one table</p>
      <h1>One Night in Palermo</h1>
      <p className={css.lede}>{families(cast)} sit down to play Mafia. Two of them are killers and must lie to the rest. You hear what each one says, and what it really thinks.</p>
      {cast.length > 0 && (
        <ul className={css.players} aria-label="The players">
          {cast.map((p, i) => (
            <li key={p.name} style={{ '--seat-color': `var(--seat-${i % 7})` } as CSSProperties}>
              <Face name={p.name} /><b>{p.name}</b><small>{modelName(p.model)}</small>
            </li>
          ))}
        </ul>
      )}
      {start && (
        <div className={css.cta}>
          <button className={css.primary} onClick={() => onOpen(start.file)}>
            {live ? <><i className={css.dot} aria-hidden /> Watch the live game</> : ranked ? 'Watch the best game →' : 'Watch the latest game →'}
          </button>
          {!live && <button className={css.secondary} onClick={() => onOpen(`${start.file}&mode=guess`)}>Guess the killers</button>}
          <p className={css.ctaNote}>
            {live ? 'A game is being played right now.' : 'Guess mode hides the roles and thoughts: can you find the killers before the table does?'}
            {played > 1 && <> {played} games to watch, about ten minutes each.</>}
          </p>
        </div>
      )}
    </header>
  );
}

// 0–100 from the fun meter as five pips and the number
function Meter({ score }: { score: number }) {
  const on = Math.max(1, Math.min(5, Math.round(score / 20)));
  return (
    <span className={css.meter} role="img" aria-label={`Fun meter ${Math.round(score)} of 100`} title={`Fun meter ${Math.round(score)} of 100`}>
      {[1, 2, 3, 4, 5].map(i => <i key={i} data-on={i <= on || undefined} />)}<em>{Math.round(score)}</em>
    </span>
  );
}

// one of the best games: a line somebody really said at that table, and nothing that gives the ending away
function Pick({ g, e, onOpen }: { g: GameInfo; e: Evening; onOpen: Open }) {
  const q = g.fun?.quote, w = when(e.started);
  return (
    <button className={css.pick} onClick={() => onOpen(g.file)}>
      <span className={css.pickTop}><Meter score={g.fun!.score} /><span>{w.day}, {w.time} · Game {g.n}</span></span>
      {q ? (
        <>
          <span className={css.quote}>“{q.text}”</span>
          <span className={css.by} style={seat(g, q.name)}><Face name={q.name} />{q.name}</span>
        </>
      ) : (
        <span className={css.castline}>{g.cast.map(p => <Face key={p.name} name={p.name} />)}</span>
      )}
      <span className={css.pickFoot}><span>{length(g)}</span><b>Watch →</b></span>
    </button>
  );
}

function LiveRow({ g, e, onOpen }: { g: GameInfo; e: Evening; onOpen: Open }) {
  return (
    <button className={css.live} onClick={() => onOpen(g.file)}>
      <span className={css.dot} aria-hidden />
      <span className={css.liveText}>
        <b>Live now</b>
        <span>{when(e.started).day}, {when(e.started).time} · Game {g.n} · {g.days ? `Day ${g.days}` : 'Night 1'} now</span>
      </span>
      <span className={css.cast} aria-label={`${g.seats} players`}>{g.cast.map(p => <Face key={p.name} name={p.name} />)}</span>
      <span className={css.go} aria-hidden>Watch →</span>
    </button>
  );
}

type Reveal = (g: GameInfo) => boolean;
const FOLD = 6;   // an evening of 8–12 games: the first six rows, then "Show all 12"

function EveningBlock({ e, open, reveal, onOpen }: { e: Evening; open: boolean; reveal: Reveal; onOpen: Open }) {
  const [isOpen, setOpen] = useState(open), [all, setAll] = useState(false);
  const w = when(e.started), score = scoreboard(e), done = e.games.filter(g => g.finished);
  const finished = done.length, results = done.every(reveal);   // the tally and the scoreboard only when every result in them may show
  const rows = all || e.games.length <= FOLD + 1 ? e.games : e.games.filter((g, i) => i < FOLD || g.live);
  return (
    <details className={css.evening} open={isOpen} onToggle={ev => setOpen((ev.target as HTMLDetailsElement).open)}>
      <summary>
        <span className={css.day}>{w.day}, {w.time}<span className={css.part}> · {w.part}</span></span>
        <span className={css.meta}>
          {e.games.length} game{e.games.length === 1 ? '' : 's'} · {e.games[0].seats} players
          {finished > 0 && results && <> · <b data-side="town">{score.town}</b> town – <b data-side="killer">{score.killer}</b> killers</>}
          {e.live && <> · <i className={css.dotSmall} aria-hidden /> playing</>}
        </span>
        <span className={css.tag} title="the engine's tag for this evening">{e.tag}</span>
      </summary>
      {isOpen && (
        <div className={css.body}>
          <div>
            <ol className={css.rows}>{rows.map(g => <Row key={g.file} g={g} label={`Game ${g.n}`} reveal={reveal(g)} onOpen={onOpen} />)}</ol>
            {rows.length < e.games.length && <button className={css.more} onClick={() => setAll(true)}>Show all {e.games.length} games</button>}
          </div>
          <div className={css.card}>{results ? <Scoreboard score={score} /> : <p className={css.hidden}>Results hidden. Watch the games, or switch results on above.</p>}</div>
        </div>
      )}
    </details>
  );
}

// one game: number, who won, how long, how fun, the killers' faces
function Row({ g, label, reveal, onOpen }: { g: GameInfo; label: string; reveal: boolean; onOpen: Open }) {
  const side = g.live ? 'live' : !reveal ? 'hidden' : g.winner ?? 'stopped';
  return (
    <li>
      <button className={css.row} data-side={side} onClick={() => onOpen(g.file)}>
        <span className={css.n}>{label}</span>
        <span className={css.won}>{g.live || reveal ? winnerWord(g) : ''}</span>
        <span className={css.len}>{length(g)}</span>
        <span className={css.fun}>{g.fun && <Meter score={g.fun.score} />}</span>
        {!g.live && reveal && g.killers.length > 0 && (
          <span className={css.killers} title={`killers: ${g.killers.join(' and ')}`}>
            {g.killers.map(k => <span key={k} style={seat(g, k)}><Face name={k} /><small>{k}</small></span>)}
          </span>
        )}
      </button>
    </li>
  );
}
