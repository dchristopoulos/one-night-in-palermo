import type { CSSProperties, ReactNode } from 'react';
import type { Bubble, Role, SeatState } from './game.ts';
import { avatar, Face } from './Face.tsx';
import { Emblem } from './Emblem.tsx';
import css from './Card.module.css';

// The one reading place (DESIGN.md §5 Card): a cream card in the middle of the table. A spoken line with the speaker's
// thought as a tinted strip on top; narration, notes, last words, the dead watching, the vote and the card reveal all land
// here too. `tail`: where the speaker sits, so the card points at them.
const TAG: Record<string, string> = { 'last words': 'voted out · last words', confession: 'after the game', 'before the game': 'before the game', 'defends before the vote': 'defends before the vote' };

// `ballots`: show who cast which vote. False in Guess mode while a secret-ballot game is on: the table saw only the counts.
export function Card({ bubble: b, thought, seats, tail, ballots = true }: {
  bubble: Bubble; thought: string | null; seats: SeatState[]; tail?: { x: number; edge: 'top' | 'bottom' }; ballots?: boolean;
}) {
  const color = (name: string) => ({ '--seat-color': `var(--seat-${(seats.find(s => s.name === name)?.seat ?? 0) % 7})` } as CSSProperties);
  const To = ({ name }: { name: string }) => <b className={css.to} style={color(name)}><Face name={name} />{name}</b>;
  let body: ReactNode, why: string | undefined;
  switch (b.kind) {
    case 'say': case 'whisper': case 'pass': {
      why = b.kind === 'say' ? b.why : undefined;
      const tag = b.kind === 'say' && b.why ? TAG[b.why] : undefined;
      const context = b.kind === 'whisper' ? <>whispers to <To name={b.to} /></>
        : b.kind === 'pass' ? <>declines to answer <To name={b.declines} /></>
        : b.replyTo ? <>to <To name={b.replyTo} /></> : null;
      body = <>
        {thought && <div className={css.thought}><span>thinks</span>{thought}</div>}
        <div className={css.head}>
          <img className={css.face} src={avatar(b.name)} alt="" data-out={(b.kind !== 'pass' && b.out) || undefined} />
          <span className={css.who} style={color(b.name)}>{b.name}</span>
          {tag && <span className={css.tag}>{tag}</span>}
          {context && <span className={css.context}>{context}</span>}
        </div>
        <p className={css.line} aria-live="polite">{b.kind === 'pass' ? '…' : b.text}</p>
      </>;
      break;
    }
    case 'narrator': {
      const phase = b.title !== 'Narrator';
      body = <div className={css.narration}>
        {phase ? <h2>{b.title}</h2> : <span className={css.label}>{b.aside ? 'the host, aside' : 'the host'}</span>}
        <p aria-live="polite">{b.text}</p>
      </div>;
      why = b.aside ? 'aside' : phase ? 'phase' : undefined;
      break;
    }
    case 'note':
      body = <>
        <div className={css.head}><img className={css.face} src={avatar(b.name)} alt="" data-out /><span className={css.who}>A note from {b.name}</span><span className={css.context}>found in the morning</span></div>
        <p className={css.line} aria-live="polite">“{b.text}”</p>
      </>;
      break;
    case 'ghost':
      body = <>
        <div className={css.head}><img className={css.face} src={avatar(b.name)} alt="" data-out /><span className={css.who}>{b.name}</span><span className={css.tag}>out of the game · only you can hear</span></div>
        <p className={css.line} aria-live="polite">{b.text}</p>
      </>;
      break;
    case 'votes':
      body = <>
        <span className={css.label}>{b.runoff ? 'runoff vote' : 'the vote'}{b.secret && <em> · secret ballot</em>}</span>
        <ol className={css.votes}>{b.groups.map(g => (
          <li key={g.target}>
            <img className={css.face} src={avatar(g.target)} alt="" />
            <span className={css.who} style={color(g.target)}>{g.target}</span>
            <b className={css.count}>{g.count}</b>
            {(ballots || !b.secret) && <span className={css.voters}>{g.voters.map(v => <Face key={v.name} name={v.name} />)}</span>}
          </li>))}</ol>
        {b.secret && <p className={css.secret}>{ballots ? 'The table saw only the counts. You see who voted for whom.' : 'The table sees only the counts. So do you, until the game is over.'}</p>}
      </>;
      break;
    case 'death':
      body = <div className={css.reveal}>
        <RoleCard name={b.name} role={b.role} />
        <div>
          <span className={css.label}>{b.how === 'vote' ? 'voted out' : 'killed in the night'}</span>
          <p className={css.out} aria-live="polite">{b.name} is out.</p>
          <p className={css.was}>{b.role ? <>{b.name} was <em data-role={b.role}>{/^[aeiou]/.test(b.role) ? 'an' : 'a'} {b.role}</em>.</> : 'The card stays face down.'}</p>
        </div>
      </div>;
      break;
  }
  return (
    <div className={css.wrap} data-kind={b.kind} data-why={why} data-tail={tail?.edge}
      style={tail ? ({ '--tail': `${tail.x}px` } as CSSProperties) : undefined}>
      <div className={css.card}>{body}</div>
    </div>
  );
}

// the turned card: the portrait on its back, the role on its face in the role colour; it flips in and holds
export const RoleCard = ({ name, role }: { name: string; role: Role | null }) => (
  <div className={css.flip} data-role={role ?? undefined} data-down={role ? undefined : true} aria-hidden>
    <div>
      <img src={avatar(name)} alt="" />
      {role && <span><Emblem role={role} />{role}</span>}
    </div>
  </div>
);
