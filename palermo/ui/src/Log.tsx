import { useLayoutEffect, useRef, useState, type CSSProperties } from 'react';
import type { LogEntry, SeatState } from './game.ts';
import { Face } from './Face.tsx';
import { Emblem } from './Emblem.tsx';
import css from './Log.module.css';

// The log (DESIGN.md §5): one entry per turn, up to the live moment. Follows the live moment; scrolling up stops following
// and shows "back to live"; clicking an entry jumps the replay there (`onJump(i)`: the event index).
// `ballots`: false keeps a secret ballot to its counts (Guess mode, game still on).
export function Log({ entries, seats, current, onJump, ballots = true }: { entries: LogEntry[]; seats: SeatState[]; current: number; onJump: (i: number) => void; ballots?: boolean }) {
  const ref = useRef<HTMLDivElement>(null), [follow, setFollow] = useState(true);
  useLayoutEffect(() => { const el = ref.current; if (el && follow) el.scrollTop = el.scrollHeight; });
  const onScroll = () => { const el = ref.current!; const atEnd = el.scrollHeight - el.scrollTop - el.clientHeight < 40; if (atEnd !== follow) setFollow(atEnd); };
  const color = (name: string) => ({ '--seat-color': `var(--seat-${(seats.find(s => s.name === name)?.seat ?? 0) % 7})` } as CSSProperties);
  const Name = ({ name }: { name: string }) => <b className={css.name} style={color(name)}>{name}</b>;

  const go = (i: number) => { setFollow(true); onJump(i); };   // the jumped-to entry becomes the live end of the log
  const entry = (e: LogEntry) => {
    const jump = { onClick: () => go(e.i), 'data-current': e.i === current || undefined, role: 'button', tabIndex: 0,
      onKeyDown: (k: React.KeyboardEvent) => { if (k.key === 'Enter') go(e.i); } };
    switch (e.kind) {
      case 'phase': return <h3 key={e.i} className={css.phase} data-night={e.night || undefined}>{e.text}{e.text !== 'Before the game' && <small> · {e.alive} at the table</small>}</h3>;
      case 'line': return (
        <div key={e.i} className={css.line} data-whisper={e.whisper || undefined} data-tag={e.tag} {...jump}>
          <Face name={e.name} />
          <div>
            <div className={css.who}><Name name={e.name} />{e.to && <span className={css.to}>{e.whisper ? 'whispers to' : '→'} {e.to}</span>}{e.tag && <span className={css.tag}>{e.tag}</span>}</div>
            {e.thought && <p className={css.thought}>{e.thought}</p>}
            <p>{e.text}</p>
          </div>
        </div>);
      case 'pass': return <p key={e.i} className={css.pass} {...jump}>{e.name} declines to answer {e.declines}.</p>;
      case 'narration': return <p key={e.i} className={css.narration} data-aside={e.aside || undefined} {...jump}>{e.text}</p>;
      case 'votes': return (
        <div key={e.i} className={css.votes} {...jump}>
          <span className={css.label}>{e.runoff ? 'Runoff vote' : 'The vote'}{e.secret && ' · secret ballot'}</span>
          {e.groups.map(g => e.secret && !ballots ? (
            <div key={g.target} className={css.tally}><Face name={g.target} /><Name name={g.target} /><b className={css.count}>{g.count}</b></div>
          ) : (
            <details key={g.target} onClick={ev => ev.stopPropagation()}>
              <summary><Face name={g.target} /><Name name={g.target} /><b className={css.count}>{g.count}</b><span className={css.voters}>{g.voters.map(v => <Face key={v.name} name={v.name} />)}</span></summary>
              <ul>{g.voters.map(v => <li key={v.name}><Name name={v.name} /> {v.why}</li>)}</ul>
            </details>))}
        </div>);
      case 'death': return (
        <div key={e.i} className={css.death} {...jump}>
          <Face name={e.name} />
          <span><b>{e.name} is out</b> <small>{e.how === 'vote' ? 'voted out' : 'killed in the night'}</small></span>
          {e.role ? <span className={css.card} data-role={e.role}><Emblem role={e.role} />{e.role}</span> : <small>card face down</small>}
        </div>);
      case 'note': return <div key={e.i} className={css.note} {...jump}><span className={css.label}>A note from {e.name}</span><p>“{e.text}”</p></div>;
      case 'ghost': return <div key={e.i} className={css.ghost} {...jump}><Face name={e.name} /><div><span className={css.label}>{e.name}, from beyond</span><p>{e.text}</p></div></div>;
      case 'called': return <p key={e.i} className={css.narration} {...jump}>{e.name} called it on the day: “{e.text}”</p>;
    }
  };
  return (
    <div className={css.wrap}>
      <div ref={ref} className={css.feed} onScroll={onScroll} aria-label="Log">{entries.map(entry)}</div>
      {!follow && <button className={css.live} onClick={() => setFollow(true)}>Back to live ↓</button>}
    </div>
  );
}
